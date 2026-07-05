"""AUV v0.3.1 — hybryda C.

Założenie projektowe (po rozczarowaniu wersją v0.3.0):

Wskaźnik AUV składa się z dwóch komponentów, które mają jasne i
osobno wytłumaczalne role:

1. **Komponent realny (real)** — ważona suma realnych wartości zasobów
   wg formuły p × N / q. Mierzy, jak rzadkie są realne zasoby per capita.

2. **Komponent fiat (fiat)** — konsensus CPI głównych walut światowych
   (USA, EUR, Japonia, Wielka Brytania, Szwajcaria), ważony PKB.
   Mierzy, jak fiat-jako-całość się rozcieńcza.

Finalne AUV:

    AUV(t) = (real(t) / real(t_0)) / (fiat(t) / fiat(t_0)) × 100

Interpretacja: AUV > 100 znaczy, że *realne zasoby* drożeją szybciej
niż *fiat się rozcieńcza*. AUV < 100 — odwrotnie, świat staje się
realnie bogatszy (postęp technologiczny i produkcyjny wyprzedza inflację).

Dlaczego hybryda zamiast czystego heliocentrycznego:
- CPI dla głównych walut jest *w rzeczywistości* solidnie mierzone
  przez profesjonalne agencje statystyczne. Pomijanie tej informacji
  to ortodoksja, nie inżynieria.
- Pełna formuła p × R × N / q wymagałaby kompletnych danych
  produkcyjnych, których jeszcze nie mamy.
- Hybryda C łączy nasze najmocniejsze obserwacje (realne wahania
  surowców) z dobrze zmierzonym konsensusem (CPI G5).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from .auv_v3 import (
    fix_anomalies,
    fill_missing_with_last,
)

logger = logging.getLogger(__name__)


PROTOTYP_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROTOTYP_ROOT / "data" / "processed"
OUTPUTS_DIR = PROTOTYP_ROOT / "outputs"


# Wagi PKB-podobne dla CPI głównych walut (~ udział w światowym PKB nominalnym)
DEFAULT_CPI_WEIGHTS = {
    "CPI_USA": 0.40,
    "CPI_EU": 0.25,
    "CPI_JP": 0.15,
    "CPI_UK": 0.10,
    "CPI_CH": 0.10,
}


# ---------------------------------------------------------------------
# Komponent fiat — konsensus CPI
# ---------------------------------------------------------------------

def compute_fiat_consensus(
    monthly: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None,
    cleaning_notes: Optional[List[str]] = None,
) -> pd.Series:
    """Ważony konsensus CPI głównych walut.

    Każda seria CPI ma inny rok bazowy (1982-84=100 dla USA,
    2015=100 dla pozostałych). Najpierw normalizujemy wszystkie do
    wspólnego punktu (najwcześniejsza wartość 1996-01 = 100), potem
    bierzemy ważoną średnią.
    """
    if weights is None:
        weights = DEFAULT_CPI_WEIGHTS

    available_cpis = [c for c in weights if c in monthly.columns]
    if not available_cpis:
        raise ValueError(
            f"Brak CPI w danych. Sprawdź download_all() dla CPI_USA, CPI_EU, ..."
        )

    if cleaning_notes is not None and len(available_cpis) < len(weights):
        missing = set(weights) - set(available_cpis)
        cleaning_notes.append(
            f"CPI niedostępne dla {missing} — pomijam z konsensusu"
        )

    # Normalizacja każdej serii do swojej pierwszej dostępnej wartości
    normalized = pd.DataFrame(index=monthly.index)
    for c in available_cpis:
        s = monthly[c].dropna()
        if s.empty:
            continue
        first_val = s.iloc[0]
        normalized[c] = monthly[c] / first_val * 100

    # Re-normalizacja wag do dostępnych serii
    total_weight = sum(weights[c] for c in available_cpis)
    norm_weights = {c: weights[c] / total_weight for c in available_cpis}

    consensus = normalized[available_cpis].mul(
        pd.Series(norm_weights), axis=1
    ).sum(axis=1)
    consensus.name = "fiat_consensus_cpi"
    return consensus


# ---------------------------------------------------------------------
# Komponent realny — uproszczona wersja v0.3
# ---------------------------------------------------------------------

def compute_real_component(
    monthly: pd.DataFrame,
    category_weights: Optional[Dict[str, float]] = None,
    cleaning_notes: Optional[List[str]] = None,
) -> pd.Series:
    """Komponent realny — ważona realna wartość zasobów.

    Używa dostępnych zasobów: zboża, energia (przez ceny + populacja),
    + metale (cena × populacja, bo nie mamy produkcji metali — przyjmujemy
    że ich produkcja rośnie liniowo z populacją, więc N/q ≈ stała).

    Wagi inspirowane udziałem w fizycznym przepływie cywilizacji.
    """
    if category_weights is None:
        category_weights = {
            "food": 0.30,
            "energy": 0.40,
            "metals": 0.30,
        }
    if cleaning_notes is None:
        cleaning_notes = []

    population = monthly["world_population"]

    # === Komponent FOOD ===
    grain_weights = {"wheat": 0.40, "corn": 0.30, "soy": 0.20, "rice": 0.10}
    avail = {g: w for g, w in grain_weights.items() if g in monthly.columns}
    total = sum(avail.values())
    norm = {g: w / total for g, w in avail.items()}
    food_price = sum(monthly[g] * w for g, w in norm.items())

    cereal_prod = fix_anomalies(
        monthly["cereal_production_world"],
        threshold_pct=0.25,
        log_notes=cleaning_notes,
    )
    cereal_prod = fill_missing_with_last(cereal_prod, log_notes=cleaning_notes)
    food_real = food_price * population / cereal_prod

    # === Komponent ENERGY ===
    # Średnia cena energii znormalizowana do baseline 2017
    baseline_year = pd.Timestamp("2017-06-30")
    energy_sources = {"brent": 0.40, "natgas_us": 0.30, "coal_aus": 0.30}
    energy_price = pd.Series(0.0, index=monthly.index)
    total_eweight = 0.0
    for s, w in energy_sources.items():
        if s in monthly.columns:
            price = monthly[s]
            try:
                base = price.loc[
                    price.index[price.index.get_indexer([baseline_year], method="nearest")[0]]
                ]
                if pd.notna(base) and base > 0:
                    energy_price = energy_price + (price / base) * w
                    total_eweight += w
            except (KeyError, IndexError):
                pass
    if total_eweight > 0:
        energy_price = energy_price / total_eweight
    # Brak twardej produkcji energii — używamy populacji jako mianownika
    # (interpretacja: ile energii na osobę w stosunku do bazowej dostępności)
    energy_real = energy_price * population / population.loc[baseline_year]

    # === Komponent METALS ===
    # Średnia ważona ceny metali, znormalizowana w bazowym czasie
    metal_sources = {"copper": 0.30, "aluminum": 0.20, "iron_ore": 0.20,
                     "nickel": 0.10, "zinc": 0.10, "lead": 0.10}
    metal_price = pd.Series(0.0, index=monthly.index)
    total_mweight = 0.0
    for s, w in metal_sources.items():
        if s in monthly.columns:
            price = monthly[s]
            try:
                base = price.loc[
                    price.index[price.index.get_indexer([baseline_year], method="nearest")[0]]
                ]
                if pd.notna(base) and base > 0:
                    metal_price = metal_price + (price / base) * w
                    total_mweight += w
            except (KeyError, IndexError):
                pass
    if total_mweight > 0:
        metal_price = metal_price / total_mweight
    # Brak twardej produkcji metali — przyjmujemy że q metali rośnie liniowo z N
    # (założenie do v0.4 — zastąpimy USGS, gdy będzie)
    metals_real = metal_price  # × N / N = stała, więc tylko cena znormalizowana

    # Normalizacja każdej kategorii do t_0
    t0 = pd.Timestamp("2017-06-30")
    realne = pd.DataFrame({
        "food": food_real,
        "energy": energy_real,
        "metals": metals_real,
    })

    for col in realne.columns:
        s = realne[col].dropna()
        if not s.empty:
            base_val = s.loc[
                s.index[s.index.get_indexer([t0], method="nearest")[0]]
            ]
            if pd.notna(base_val) and base_val > 0:
                realne[col] = realne[col] / base_val * 100

    # Ważona suma kategorii (po normalizacji każdej do t_0 = 100)
    w_series = pd.Series(category_weights)
    available_cats = [c for c in w_series.index if c in realne.columns]
    norm_cat_weights = w_series[available_cats] / w_series[available_cats].sum()

    real_component = realne[available_cats].mul(norm_cat_weights, axis=1).sum(axis=1)
    real_component.name = "real_component"
    return real_component


# ---------------------------------------------------------------------
# Główna procedura — hybryda C
# ---------------------------------------------------------------------

@dataclass
class AUVHybridResult:
    """Wyniki obliczenia AUV v0.3.1 hybryda C."""

    real_component: pd.Series
    fiat_component: pd.Series
    auv: pd.Series
    cleaning_notes: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


def construct_auv_v3_hybrid(
    monthly: pd.DataFrame,
    t0: str = "2017-06-30",
    category_weights: Optional[Dict[str, float]] = None,
    cpi_weights: Optional[Dict[str, float]] = None,
) -> AUVHybridResult:
    """Pełna procedura: AUV = real / fiat * 100.

    real: ważona suma realnych wartości zasobów (cena × populacja / produkcja).
    fiat: konsensus CPI głównych walut.
    Obie znormalizowane do t_0 = 100.
    """
    cleaning_notes: List[str] = []

    fiat = compute_fiat_consensus(
        monthly, weights=cpi_weights, cleaning_notes=cleaning_notes
    )
    real = compute_real_component(
        monthly, category_weights=category_weights, cleaning_notes=cleaning_notes
    )

    t0_ts = pd.Timestamp(t0)
    # Już są znormalizowane do t_0 = 100 (real po stronie funkcji,
    # fiat względem swojej pierwszej wartości). Re-normalizujmy fiat do t_0.
    fiat_t0 = fiat.loc[
        fiat.index[fiat.index.get_indexer([t0_ts], method="nearest")[0]]
    ]
    fiat = fiat / fiat_t0 * 100

    # AUV = real / fiat × 100, znormalizowane jeszcze raz, żeby gwarancja t_0=100
    auv_raw = real / fiat * 100
    auv_t0 = auv_raw.loc[
        auv_raw.index[auv_raw.index.get_indexer([t0_ts], method="nearest")[0]]
    ]
    auv = auv_raw / auv_t0 * 100
    auv.name = "AUV_v3_hybrid"

    return AUVHybridResult(
        real_component=real,
        fiat_component=fiat,
        auv=auv,
        cleaning_notes=cleaning_notes,
        metadata={
            "t0": t0,
            "version": "0.3.1-hybrid-C",
            "category_weights": category_weights or {"food": 0.30, "energy": 0.40, "metals": 0.30},
            "cpi_weights": cpi_weights or DEFAULT_CPI_WEIGHTS,
            "interpretation": (
                "AUV > 100: realne zasoby drożeją szybciej niż fiat się rozcieńcza. "
                "AUV < 100: świat realnie się bogaci (postęp wyprzedza inflację)."
            ),
        },
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    result = construct_auv_v3_hybrid(monthly)

    print("\n=== AUV v0.3.1 (hybrid C) ===")
    auv = result.auv.dropna()
    print(f"Okres: {auv.index.min()} → {auv.index.max()}")
    for date in ["2000-01-31", "2008-09-30", "2017-06-30",
                 "2020-03-31", "2022-02-28", "2025-12-31"]:
        try:
            v = result.auv.loc[date]
            r = result.real_component.loc[date]
            f = result.fiat_component.loc[date]
            print(f"  {date}: AUV={v:6.1f}  real={r:6.1f}  fiat={f:6.1f}")
        except KeyError:
            pass

    print(f"\nNotatki ({len(result.cleaning_notes)}):")
    for note in result.cleaning_notes:
        print(f"  • {note}")
