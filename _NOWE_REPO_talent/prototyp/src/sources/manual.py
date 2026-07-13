"""Adapter danych RĘCZNYCH — dla serii dostępnych tylko w PDF/Excel
(USGS Mineral Commodity Summaries, World Steel, CEMBUREAU).

Użytkownik wpisuje dane do jednego pliku:
    data/manual/manual_production.csv
w formacie szerokim: kolumna `year` (1996..2025) + po jednej kolumnie na
serię (identyfikator = nazwa kolumny). Puste komórki są dozwolone —
brakujące lata zostaną pominięte, a serie całkowicie puste są traktowane
jak niedostępne (pipeline je pomija, a koszyk wraca do stałego R).

Wartości to PRODUKCJA GLOBALNA w jednostkach fizycznych (dowolnych, byle
spójnych w obrębie serii) — używamy ich jako proxy konsumpcji per capita
(globalnie produkcja ≈ konsumpcja), więc liczy się tylko DYNAMIKA.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class ManualSource:
    """Czyta serie roczne z jednego pliku CSV w formacie szerokim."""

    def __init__(self, manual_dir: Optional[Path] = None, filename: str = "manual_production.csv"):
        self.path = (manual_dir or Path("data/manual")) / filename

    def get_series(self, series_id: str, start: str, end: str) -> pd.Series:
        if not self.path.exists():
            raise FileNotFoundError(
                f"Brak pliku danych ręcznych: {self.path}. "
                f"Wypełnij szablon, by włączyć serię '{series_id}'."
            )
        df = pd.read_csv(self.path, comment="#")
        if "year" not in df.columns:
            raise ValueError(f"{self.path}: brak kolumny 'year'.")
        if series_id not in df.columns:
            raise KeyError(f"{self.path}: brak kolumny '{series_id}'.")

        s = pd.Series(
            df[series_id].values,
            index=pd.to_datetime(df["year"].astype(int).astype(str) + "-12-31"),
            name=series_id,
        ).dropna()
        if s.empty:
            raise ValueError(f"Seria '{series_id}' w {self.path} jest pusta — pomijam.")
        s = s[(s.index >= pd.Timestamp(start)) & (s.index <= pd.Timestamp(end))]
        logger.info(f"MANUAL: {series_id} → {len(s)} obserwacji z {self.path.name}")
        return s
