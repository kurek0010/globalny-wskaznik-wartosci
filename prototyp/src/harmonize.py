"""Harmonizacja zebranych szeregów: częstotliwość, normalizacja, alignment.

Wejście: słownik {label: pd.Series} (jak zwraca download.download_all).
Wyjście: dwa DataFrame'y zapisane jako parquet w data/processed/:
    daily.parquet    — wszystkie serie ujednolicone do dziennej siatki
    monthly.parquet  — agregacja miesięczna (średnie z końca miesiąca)

Konwencje:
    - Kursy walutowe sprowadzane do PER-USD (jednostek waluty obcej za 1 USD).
      Dla par podanych jako USD/EUR, USD/GBP, USD/AUD odwracamy: 1/x.
    - Forward-fill dla dni roboczych poza weekendami i świętami.
    - Cubic spline NIE jest stosowany w v0.2 — używamy forward-fill,
      żeby uniknąć look-ahead bias.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

import pandas as pd

from .config import ALL_SERIES, CURRENCIES, END_DATE, START_DATE


logger = logging.getLogger("harmonize")


# Plik znajduje się w prototyp/src/harmonize.py, więc parents[1] == prototyp/.
PROTOTYP_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROTOTYP_ROOT / "data" / "processed"


# Pary FX z FRED, w których konwencja to "USD za 1 jednostkę waluty obcej"
# (czyli odwrotnie niż chcemy — chcemy "waluta obca za 1 USD").
INVERTED_FX = {"EUR", "GBP", "AUD"}


def _normalize_currency(label: str, series: pd.Series) -> pd.Series:
    """Ujednolicenie kursów walutowych do konwencji 'jednostek waluty za 1 USD'."""
    if label in INVERTED_FX:
        return 1.0 / series
    return series


def _to_daily(series: pd.Series, freq_hint: str) -> pd.Series:
    """Sprowadzenie serii do siatki dziennej (dni robocze)."""
    daily_index = pd.bdate_range(start=START_DATE, end=END_DATE)
    if freq_hint == "daily":
        return series.reindex(daily_index).ffill()
    if freq_hint in {"weekly", "monthly"}:
        # Forward-fill: ostatnia znana wartość niesie się do następnego raportu
        return series.reindex(daily_index, method="ffill")
    if freq_hint == "yearly":
        return series.reindex(daily_index, method="ffill")
    raise ValueError(f"Nieznana częstotliwość: {freq_hint}")


def harmonize(series_dict: Dict[str, pd.Series]) -> Dict[str, pd.DataFrame]:
    """Ujednolicenie wszystkich serii do dwóch DataFrame'ów: daily + monthly.

    Zwraca słownik {'daily': df_daily, 'monthly': df_monthly}.
    """
    aligned_daily: Dict[str, pd.Series] = {}

    for label, series in series_dict.items():
        spec = ALL_SERIES[label]
        s = series.copy()

        # Specjalne traktowanie walut
        if spec["category"] == "currency":
            s = _normalize_currency(label, s)

        s = _to_daily(s, spec["freq"])
        aligned_daily[label] = s

    df_daily = pd.DataFrame(aligned_daily)

    # Podsumowanie kompletności
    completeness = df_daily.notna().mean()
    logger.info("Kompletność serii po alignmentcie:")
    for col, pct in completeness.sort_values(ascending=False).items():
        logger.info(f"  {col}: {pct:.1%}")

    # Wersja miesięczna — end-of-month
    df_monthly = df_daily.resample("ME").last()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_daily.to_parquet(PROCESSED_DIR / "daily.parquet")
    df_monthly.to_parquet(PROCESSED_DIR / "monthly.parquet")
    logger.info(f"Zapisano: {PROCESSED_DIR}/daily.parquet ({df_daily.shape})")
    logger.info(f"Zapisano: {PROCESSED_DIR}/monthly.parquet ({df_monthly.shape})")

    return {"daily": df_daily, "monthly": df_monthly}


if __name__ == "__main__":
    from .download import download_all

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    )
    series_dict = download_all()
    harmonize(series_dict)
