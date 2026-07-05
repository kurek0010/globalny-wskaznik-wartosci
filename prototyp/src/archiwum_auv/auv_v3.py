"""AUV v0.3 — implementacja formuły 'koszt utrzymania cywilizacji'.

Formuła podstawowa dla każdego zasobu i:

    realna_wartość_i(t) = p_i(t) × R_i_baseline × N(t) / q_i(t)

gdzie:
    p_i — cena (USD/jednostka)
    R_i_baseline — potrzeba na osobę na rok ustalona w dniu bazowym (stała)
    N(t) — populacja świata
    q_i(t) — roczna produkcja globalna

Ponieważ R_i_baseline jest stałą, formułę można uprościć do
    realna_wartość_i(t) ∝ p_i(t) × N(t) / q_i(t)

co interpretujemy jako "cena × populacja / produkcja" — wskaźnik
*względnej rzadkości na osobę* przy danej cenie. Im wyższa, tym
zasób jest bardziej "drogi w sensie cywilizacyjnym".

W obecnej wersji (v0.3.0) implementujemy formułę tylko dla zasobów,
dla których mamy publiczną produkcję światową. To znaczy:
- Żywność (zbóż) — cereal_production_world z World Bank.
Pozostałe zasoby (metale, energia, materiały) wymagają adapterów do
USGS/EIA/FAO i zostaną dodane w v0.3.1.

Notebook walidacyjny: notebooks/04_auv_v3.ipynb.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


PROTOTYP_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROTOTYP_ROOT / "data" / "processed"
OUTPUTS_DIR = PROTOTYP_ROOT / "outputs"


# ---------------------------------------------------------------------
# Defensywne oczyszczanie danych
# ---------------------------------------------------------------------

def detect_anomalies(
    series: pd.Series,
    threshold_pct: float = 0.25,
) -> pd.Series:
    """Wykryj wartości, które różnią się o > threshold od poprzedniej.

    Anomalia: rok-do-roku zmiana większa niż threshold_pct (np. 25%).
    Takie zmiany w rocznych szeregach produkcyjnych są praktycznie
    zawsze błędami danych (niekompletny raport, zmiana metodologii).

    Zwraca: bool Series, True dla wartości anomalii.
    """
    pct_change = series.pct_change().abs()
    return pct_change > threshold_pct


def fix_anomalies(
    series: pd.Series,
    threshold_pct: float = 0.25,
    log_notes: Optional[List[str]] = None,
) -> pd.Series:
    """Zastąp anomalie wartością poprzednią (carry forward).

    Reguła deterministyczna: każda obserwacja, która zmieniła się o
    więcej niż threshold_pct rok-do-roku, jest *zastępowana ostatnią
    rozsądną wartością*. To jest jawny mechanizm; rok zastąpiony
    raportujemy w log_notes, żeby było wiadomo.
    """
    s = series.copy()
    anomalies = detect_anomalies(s, threshold_pct)
    fixed_count = 0
    for idx in s.index[anomalies]:
        if log_notes is not None:
            log_notes.append(
                f"{s.name} @ {idx:%Y-%m-%d}: anomalia "
                f"({s.loc[idx]:,.0f} vs poprzednia "
                f"{s.shift(1).loc[idx]:,.0f}) — zastąpiono carry-forward."
            )
        s.loc[idx] = s.shift(1).loc[idx]
        fixed_count += 1
    if fixed_count > 0:
        logger.info(
            f"Oczyszczono {fixed_count} anomalii w serii {s.name}"
        )
    return s


def fill_missing_with_last(
    series: pd.Series,
    log_notes: Optional[List[str]] = None,
) -> pd.Series:
    """Uzupełnij brakujące końcowe obserwacje ostatnią znaną wartością.

    Dla serii, które się "kończą" w pewnym roku (np. food index 2020),
    rozszerzamy ostatnią wartość do końca okresu. Jawnie raportujemy.
    """
    s = series.copy()
    if s.notna().any():
        last_valid_idx = s.last_valid_index()
        if last_valid_idx is not None and last_valid_idx < s.index[-1]:
            if log_notes is not None:
                log_notes.append(
                    f"{s.name}: ostatnia obserwacja {last_valid_idx:%Y-%m-%d}, "
                    f"dalej carry-forward wartości {s.loc[last_valid_idx]:.2f}"
                )
            s = s.ffill()
    return s


# ---------------------------------------------------------------------
# Formuła AUV v0.3
# ---------------------------------------------------------------------

@dataclass
class AUVv3Result:
    """Wyniki obliczenia AUV v0.3."""

    realne_wartosci: pd.DataFrame
    weights: pd.Series
    population: pd.Series
    cleaned_production: pd.DataFrame
    auv_series: pd.Series
    cleaning_notes: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


def compute_food_realna_wartosc(
    monthly: pd.DataFrame,
    population_col: str = "world_population",
    cereal_production_col: str = "cereal_production_world",
    cleaning_notes: Optional[List[str]] = None,
) -> pd.Series:
    """Realna wartość żywności (kategoria zbóż).

    Liczone jako: średnia cena głównych zbóż × populacja / produkcja zbóż.

    Średnia ważona ceny: wheat (40%), corn (30%), soy (20%), rice (10%).
    Wagi przybliżają wkład w globalnej dietykalorycznej.
    """
    if cleaning_notes is None:
        cleaning_notes = []

    # Ceny: ważona średnia głównych zbóż
    grain_weights = {"wheat": 0.40, "corn": 0.30, "soy": 0.20, "rice": 0.10}
    grain_prices = pd.DataFrame()
    for grain, w in grain_weights.items():
        if grain in monthly.columns:
            grain_prices[grain] = monthly[grain]
    # Normalizacja wag do tych, które rzeczywiście mamy
    available_weights = {g: w for g, w in grain_weights.items() if g in grain_prices.columns}
    total = sum(available_weights.values())
    normalized = {g: w / total for g, w in available_weights.items()}
    weighted_price = sum(grain_prices[g] * w for g, w in normalized.items())

    # Populacja i produkcja
    population = monthly[population_col]
    production_raw = monthly[cereal_production_col]
    production_clean = fix_anomalies(production_raw, threshold_pct=0.25, log_notes=cleaning_notes)
    production_clean = fill_missing_with_last(production_clean, log_notes=cleaning_notes)

    # Formuła: p × N / q
    realna = weighted_price * population / production_clean
    realna.name = "food_realna_wartosc"
    return realna


def compute_energy_realna_wartosc(
    monthly: pd.DataFrame,
    population_col: str = "world_population",
    energy_per_capita_col: str = "energy_use_per_capita",
    cleaning_notes: Optional[List[str]] = None,
) -> pd.Series:
    """Realna wartość energii — kompromis przy braku danych produkcyjnych.

    Brakujące dane: globalna produkcja energii w jednostkach kompatybilnych
    z cenami ropy/gazu/węgla. Tymczasowo używamy:

        q_energy(t) ≈ energy_use_per_capita(t) × N(t)

    Bo w długim okresie produkcja ≈ konsumpcja na poziomie świata.

    Średnia cena energii: brent (40%), natgas_us (30%), coal_aus (30%),
    znormalizowane do jednolitej skali przed uśrednieniem.
    """
    if cleaning_notes is None:
        cleaning_notes = []

    # Średnia cena energii, znormalizowana do baseline 2017
    energy_weights = {"brent": 0.40, "natgas_us": 0.30, "coal_aus": 0.30}
    baseline_year = pd.Timestamp("2017-06-30")

    weighted_price = pd.Series(0.0, index=monthly.index)
    for source, w in energy_weights.items():
        if source in monthly.columns:
            price = monthly[source]
            # Znajdź najbliższą datę bazową
            try:
                base_val = price.loc[
                    price.index[price.index.get_indexer([baseline_year], method="nearest")[0]]
                ]
                weighted_price = weighted_price + (price / base_val) * w
            except (KeyError, IndexError):
                logger.warning(f"Nie można znaleźć wartości bazowej dla {source}")

    population = monthly[population_col]
    energy_per_capita = fill_missing_with_last(
        monthly[energy_per_capita_col],
        log_notes=cleaning_notes,
    )
    production_proxy = energy_per_capita * population

    realna = weighted_price * population / production_proxy
    realna.name = "energy_realna_wartosc"
    return realna


def construct_auv_v3(
    monthly: pd.DataFrame,
    weights: Dict[str, float] = None,
    t0: str = "2017-06-30",
) -> AUVv3Result:
    """Buduje AUV v0.3 jako ważoną sumę realnych wartości kategorii."""
    if weights is None:
        weights = {"food": 0.50, "energy": 0.50}

    cleaning_notes: List[str] = []
    realne = pd.DataFrame(index=monthly.index)

    if "food" in weights:
        realne["food"] = compute_food_realna_wartosc(
            monthly, cleaning_notes=cleaning_notes
        )

    if "energy" in weights:
        realne["energy"] = compute_energy_realna_wartosc(
            monthly, cleaning_notes=cleaning_notes
        )

    # Normalizacja każdej kategorii do t_0 = 1, żeby wagi miały sens
    t0_ts = pd.Timestamp(t0)
    t0_idx = realne.index[realne.index.get_indexer([t0_ts], method="nearest")[0]]
    realne_normalized = realne / realne.loc[t0_idx]

    # Ważona suma
    weights_series = pd.Series(weights)
    auv_unnormalized = realne_normalized.mul(weights_series, axis=1).sum(axis=1)
    auv_series = auv_unnormalized / auv_unnormalized.loc[t0_idx] * 100
    auv_series.name = "AUV_v3"

    return AUVv3Result(
        realne_wartosci=realne,
        weights=weights_series,
        population=monthly.get("world_population", pd.Series()),
        cleaned_production=pd.DataFrame({
            "cereal": monthly.get("cereal_production_world", pd.Series()),
            "energy_per_capita": monthly.get("energy_use_per_capita", pd.Series()),
        }),
        auv_series=auv_series,
        cleaning_notes=cleaning_notes,
        metadata={
            "t0": t0,
            "weights": weights,
            "version": "0.3.0",
            "scope": "food + energy (proxy)",
            "limitations": (
                "Brak produkcji metali (potrzebny USGS), brak produkcji ropy/gazu "
                "(potrzebny EIA z kluczem), brak materiałów budowlanych. "
                "Wersja demonstracyjna do walidacji koncepcji."
            ),
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
    result = construct_auv_v3(monthly)

    print("\n=== AUV v0.3 — wyniki podstawowe ===")
    print(f"Okres: {result.auv_series.first_valid_index()} → "
          f"{result.auv_series.last_valid_index()}")
    print(f"\nAUV v3 w 2000-01: {result.auv_series.loc['2000-01-31']:.1f}")
    print(f"AUV v3 w 2008-09: {result.auv_series.loc['2008-09-30']:.1f}")
    print(f"AUV v3 w 2017-06 (t_0): {result.auv_series.loc['2017-06-30']:.1f}")
    print(f"AUV v3 w 2020-03 (COVID): {result.auv_series.loc['2020-03-31']:.1f}")
    print(f"AUV v3 w 2022-02 (Ukraine): {result.auv_series.loc['2022-02-28']:.1f}")
    print(f"AUV v3 w 2025-12: {result.auv_series.iloc[-1]:.1f}")

    print(f"\n=== Notatki z oczyszczania ({len(result.cleaning_notes)}) ===")
    for note in result.cleaning_notes:
        print(f"  - {note}")
