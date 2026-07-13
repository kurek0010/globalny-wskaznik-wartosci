"""Adapter do FRED (Federal Reserve Economic Data).

Wymaga klucza API (bezpłatny): https://fred.stlouisfed.org/docs/api/api_key.html
Klucz oczekiwany w zmiennej środowiskowej FRED_API_KEY (lub w pliku .env).
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Optional

import pandas as pd
from fredapi import Fred

logger = logging.getLogger(__name__)


class FredSource:
    """Cienka warstwa nad biblioteką fredapi z cachem CSV i retry."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        cache_dir: Optional[Path] = None,
        retry_count: int = 3,
        retry_delay: float = 2.0,
    ):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "Brak klucza FRED API. Załóż go na "
                "https://fred.stlouisfed.org/docs/api/api_key.html "
                "i wpisz do prototyp/.env jako FRED_API_KEY=..."
            )
        self.fred = Fred(api_key=self.api_key)
        self.cache_dir = cache_dir
        self.retry_count = retry_count
        self.retry_delay = retry_delay

    def get_series(
        self,
        series_id: str,
        start: str,
        end: str,
        use_cache: bool = True,
    ) -> pd.Series:
        """Pobierz pojedynczą serię z FRED-a.

        Cache jest oparty na pliku CSV z nazwą {series_id}_{start}_{end}.csv.
        """
        if use_cache and self.cache_dir is not None:
            cache_path = self.cache_dir / f"fred_{series_id}_{start}_{end}.csv"
            if cache_path.exists():
                logger.debug(f"FRED: cache hit dla {series_id}")
                df = pd.read_csv(cache_path, parse_dates=["date"], index_col="date")
                return df["value"]

        last_err: Optional[Exception] = None
        for attempt in range(self.retry_count):
            try:
                logger.info(
                    f"FRED: pobieranie {series_id} ({start} → {end}), próba {attempt + 1}"
                )
                series = self.fred.get_series(
                    series_id,
                    observation_start=start,
                    observation_end=end,
                )
                series.name = series_id
                if use_cache and self.cache_dir is not None:
                    self.cache_dir.mkdir(parents=True, exist_ok=True)
                    cache_path = (
                        self.cache_dir / f"fred_{series_id}_{start}_{end}.csv"
                    )
                    series.rename_axis("date").rename("value").to_csv(cache_path)
                return series
            except Exception as e:  # noqa: BLE001 — chcemy łapać wszystko, retry
                last_err = e
                logger.warning(f"FRED: błąd dla {series_id}: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay * (attempt + 1))

        assert last_err is not None
        raise RuntimeError(
            f"FRED: nie udało się pobrać {series_id} po {self.retry_count} próbach"
        ) from last_err
