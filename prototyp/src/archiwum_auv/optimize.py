"""Optymalizacja wag koszyka AUV.

Dwuetapowa procedura na *poziomach* (wersja A funkcji celu, ustalona po EDA):

1. Frisch-Waugh-Lovell na log-poziomach.
   Dla każdego surowca `i` regresujemy `log p_i(t)` na log-poziomach
   wybranych agregatów monetarnych. Reszty `e_i(t)` reprezentują
   część zmienności surowca, której NIE da się wyjaśnić ekspansją
   monetarną — czyli "realny" komponent ceny.

2. Optymalizacja kwadratowa z ograniczeniami.
   Szukamy wag `w_i ≥ 0, Σw_i = 1`, dla których ważona suma reszt
   `Σ w_i e_i(t)` ma minimalną wariancję. Innymi słowy: szukamy
   takiego koszyka, którego "realny" komponent jest jak najbardziej
   stabilny.

Walidacja krzyżowa: pierwsza składowa PCA tej samej macierzy reszt
powinna dawać podobny kierunek (po znormalizowaniu do dodatnich wag).

Wszystkie obliczenia w skali miesięcznej (`monthly.parquet`) — daje
to wspólną częstotliwość z M2/M3.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import cvxpy as cp
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression

logger = logging.getLogger(__name__)


PROTOTYP_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROTOTYP_ROOT / "data" / "processed"
OUTPUTS_DIR = PROTOTYP_ROOT / "outputs"


@dataclass
class AUVResult:
    """Wynik pełnej procedury wyznaczania AUV."""

    commodities: List[str]
    money_aggregates: List[str]
    t0: pd.Timestamp
    weights_qp: pd.Series
    weights_pca: pd.Series
    betas: pd.DataFrame  # surowce × M2_aggregates
    residual_stats: pd.DataFrame
    auv_series: pd.Series
    auv_residual_std: float
    auv_residual_std_pca: float
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "commodities": self.commodities,
            "money_aggregates": self.money_aggregates,
            "t0": self.t0.strftime("%Y-%m-%d"),
            "weights_qp": self.weights_qp.to_dict(),
            "weights_pca": self.weights_pca.to_dict(),
            "auv_residual_std_qp": float(self.auv_residual_std),
            "auv_residual_std_pca": float(self.auv_residual_std_pca),
            "metadata": self.metadata,
        }

    def save(self, output_dir: Path = OUTPUTS_DIR) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        with (output_dir / "weights.json").open("w") as f:
            json.dump(self.to_dict(), f, indent=2)
        self.auv_series.rename("AUV").to_csv(
            output_dir / "auv_series.csv", header=True
        )
        self.betas.to_csv(output_dir / "betas_fwl.csv")
        self.residual_stats.to_csv(output_dir / "residual_stats.csv")
        logger.info(f"Zapisano: {output_dir}/weights.json, auv_series.csv, betas_fwl.csv")


# ---------------------------------------------------------------------
# Krok 1 — Frisch-Waugh-Lovell na poziomach
# ---------------------------------------------------------------------

def fwl_residuals(
    log_prices: pd.DataFrame,
    log_money: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Regresja log-poziomów surowców na log-poziomach M2.

    Zwraca:
        residuals: DataFrame z resztami dla każdego surowca, indeks = czas
        betas:     DataFrame ze współczynnikami β (surowce × M2)
    """
    common_idx = log_prices.dropna().index.intersection(
        log_money.dropna().index
    )
    if common_idx.empty:
        raise ValueError("Brak wspólnego okresu między cenami a M2")

    X = log_money.loc[common_idx].values  # (T, K)
    residuals = pd.DataFrame(index=common_idx)
    betas = pd.DataFrame(
        index=log_prices.columns,
        columns=log_money.columns,
        dtype=float,
    )

    for col in log_prices.columns:
        y = log_prices.loc[common_idx, col].dropna()
        idx = y.index
        X_sub = log_money.loc[idx].values
        model = LinearRegression()
        model.fit(X_sub, y.values)
        betas.loc[col, log_money.columns] = model.coef_
        residuals[col] = y - model.predict(X_sub)

    return residuals, betas


# ---------------------------------------------------------------------
# Krok 2 — Optymalizacja QP na resztach
# ---------------------------------------------------------------------

def solve_qp(residuals: pd.DataFrame) -> pd.Series:
    """Minimalizuj wariancję ważonej sumy reszt przy w_i >= 0, Σw_i = 1.

    Formalnie: minimalizujemy w' Σ w, gdzie Σ to kowariancja reszt.
    To jest klasyczna optymalizacja portfela typu minimum-variance.
    """
    R = residuals.dropna().values  # (T, N)
    cov = np.cov(R.T)
    n = cov.shape[0]

    w = cp.Variable(n, nonneg=True)
    objective = cp.Minimize(cp.quad_form(w, cp.psd_wrap(cov)))
    constraints = [cp.sum(w) == 1]
    problem = cp.Problem(objective, constraints)
    problem.solve()

    if problem.status not in {"optimal", "optimal_inaccurate"}:
        raise RuntimeError(
            f"QP nie znalazł rozwiązania (status: {problem.status})"
        )

    return pd.Series(w.value, index=residuals.columns, name="weight_qp")


# ---------------------------------------------------------------------
# Walidacja krzyżowa — PCA na resztach
# ---------------------------------------------------------------------

def pca_weights(residuals: pd.DataFrame) -> pd.Series:
    """Wagi z PCA — kierunek MINIMALNEJ wariancji (ostatnia składowa).

    Sens metodologiczny: PCA znajduje ortogonalne kierunki, ostatnia
    główna składowa to kierunek o najmniejszej wariancji w przestrzeni
    reszt. Po normalizacji do nieujemnych wag i unormowaniu sumy do 1,
    powinna być zbliżona do rozwiązania QP, jeśli oba zadania są
    matematycznie zgodne.
    """
    R = residuals.dropna().values
    pca = PCA(n_components=R.shape[1])
    pca.fit(R)
    # Ostatni komponent = najmniej wariancji
    loadings = pca.components_[-1]
    # Bierzemy wartości bezwzględne (kierunek umowny), klipujemy do 0,
    # normalizujemy do sumy 1
    weights = np.abs(loadings)
    weights = weights / weights.sum()
    return pd.Series(weights, index=residuals.columns, name="weight_pca")


# ---------------------------------------------------------------------
# Konstrukcja AUV(t)
# ---------------------------------------------------------------------

def construct_auv(
    prices: pd.DataFrame,
    weights: pd.Series,
    t0: pd.Timestamp,
    base_value: float = 100.0,
) -> pd.Series:
    """AUV(t) = (Σ w_i p_i(t)) / (Σ w_i p_i(t_0)) * base_value."""
    # Sprawdź, że wagi i kolumny się zgadzają
    cols = weights.index.tolist()
    if not all(c in prices.columns for c in cols):
        missing = [c for c in cols if c not in prices.columns]
        raise ValueError(f"Brak kolumn w prices: {missing}")

    basket = prices[cols].dot(weights)
    if t0 not in basket.index:
        # Znajdź najbliższy dostępny dzień
        idx_pos = basket.index.get_indexer([t0], method="nearest")[0]
        t0_actual = basket.index[idx_pos]
        logger.warning(
            f"t_0={t0:%Y-%m-%d} nie istnieje w siatce — używam {t0_actual:%Y-%m-%d}"
        )
        t0 = t0_actual

    basket_t0 = basket.loc[t0]
    return (basket / basket_t0) * base_value


# ---------------------------------------------------------------------
# Główna procedura
# ---------------------------------------------------------------------

def run_auv_pipeline(
    monthly: pd.DataFrame,
    commodities: Sequence[str],
    money_aggregates: Sequence[str],
    t0: str = "2017-06-30",
) -> AUVResult:
    """Pełny pipeline: FWL → QP → PCA → AUV(t).

    Args:
        monthly: DataFrame z miesięcznymi danymi (jak `monthly.parquet`).
        commodities: nazwy kolumn-składników koszyka.
        money_aggregates: nazwy kolumn-agregatów monetarnych.
        t0: dzień bazowy AUV = 100.

    Returns:
        AUVResult z kompletem wyników gotowym do zapisu / wizualizacji.
    """
    logger.info(
        f"Pipeline AUV: {len(commodities)} surowców, "
        f"{len(money_aggregates)} agregatów M2, t_0={t0}"
    )

    # Filtruj dane do dostępnych kolumn
    available_commodities = [c for c in commodities if c in monthly.columns]
    available_money = [m for m in money_aggregates if m in monthly.columns]

    if len(available_commodities) < 2:
        raise ValueError(
            f"Za mało dostępnych surowców: {available_commodities}"
        )
    if not available_money:
        raise ValueError("Brak dostępnych agregatów monetarnych")

    if len(available_commodities) != len(commodities):
        missing = set(commodities) - set(available_commodities)
        logger.warning(f"Pomijam surowce niedostępne: {missing}")

    log_prices = np.log(monthly[available_commodities]).dropna()
    log_money = np.log(monthly[available_money]).dropna()

    # Krok 1 — FWL
    residuals, betas = fwl_residuals(log_prices, log_money)
    logger.info(
        f"FWL: {residuals.shape[0]} obserwacji × "
        f"{residuals.shape[1]} surowców"
    )

    # Krok 2 — QP
    weights_qp = solve_qp(residuals)
    logger.info(f"QP: rozwiązanie znalezione, max waga = {weights_qp.max():.3f}")

    # Walidacja PCA
    weights_pca = pca_weights(residuals)

    # Konstrukcja AUV — używamy oryginalnych (nielogarytmicznych) cen
    t0_ts = pd.Timestamp(t0)
    auv_qp = construct_auv(monthly[available_commodities], weights_qp, t0_ts)
    auv_pca = construct_auv(monthly[available_commodities], weights_pca, t0_ts)

    # Diagnostyka — odchylenie standardowe reszt dla obu koszyków
    basket_residual_qp = residuals.dot(weights_qp)
    basket_residual_pca = residuals.dot(weights_pca)

    # Statystyki reszt per surowiec
    residual_stats = pd.DataFrame({
        "mean": residuals.mean(),
        "std": residuals.std(),
        "min": residuals.min(),
        "max": residuals.max(),
    })

    return AUVResult(
        commodities=available_commodities,
        money_aggregates=available_money,
        t0=t0_ts,
        weights_qp=weights_qp,
        weights_pca=weights_pca,
        betas=betas,
        residual_stats=residual_stats,
        auv_series=auv_qp,
        auv_residual_std=float(basket_residual_qp.std()),
        auv_residual_std_pca=float(basket_residual_pca.std()),
        metadata={
            "n_observations": int(residuals.shape[0]),
            "period_start": str(residuals.index.min().date()),
            "period_end": str(residuals.index.max().date()),
        },
    )


# ---------------------------------------------------------------------
# Uruchomienie z linii komend
# ---------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    )

    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")

    DEFAULT_COMMODITIES = [
        "brent", "wti", "natgas_us",
        "wheat", "corn",
        "copper", "aluminum", "iron_ore",
    ]
    DEFAULT_MONEY = ["M2_USA", "M3_EU", "M3_UK", "M2_JP"]

    result = run_auv_pipeline(
        monthly=monthly,
        commodities=DEFAULT_COMMODITIES,
        money_aggregates=DEFAULT_MONEY,
        t0="2017-06-30",
    )
    result.save()

    print("\n=== Wagi QP (top 5) ===")
    print(result.weights_qp.sort_values(ascending=False).head())
    print("\n=== AUV — pierwsze i ostatnie obserwacje ===")
    print(result.auv_series.head(3))
    print("...")
    print(result.auv_series.tail(3))
    print(f"\nAUV w t_0={result.t0:%Y-%m-%d}: {result.auv_series.loc[result.t0]:.2f}")
    print(f"AUV na końcu: {result.auv_series.iloc[-1]:.2f}")
    print(f"Wzrost: {(result.auv_series.iloc[-1] / 100 - 1) * 100:.1f}%")
