"""Adapter do ECB Statistical Data Warehouse.

Bez uwierzytelnienia. Dokumentacja: https://data.ecb.europa.eu/help/api/data
"""

from __future__ import annotations

import io
import logging
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

logger = logging.getLogger(__name__)

ECB_BASE = "https://data-api.ecb.europa.eu/service/data"


class ECBSource:
    """Pobieranie szeregów czasowych z ECB SDW."""

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        retry_count: int = 3,
        retry_delay: float = 2.0,
    ):
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
        """Pobierz serię ECB w formacie CSV.

        `series_id` ma format dataset.frequency.dim1.dim2.dim3.dim4,
        np. EXR.D.CZK.EUR.SP00.A dla kursu dziennego CZK/EUR.
        """
        if use_cache and self.cache_dir is not None:
            cache_path = self.cache_dir / f"ecb_{series_id.replace('.', '_')}_{start}_{end}.csv"
            if cache_path.exists():
                logger.debug(f"ECB: cache hit dla {series_id}")
                df = pd.read_csv(cache_path, parse_dates=["date"], index_col="date")
                return df["value"]

        dataset, *key_parts = series_id.split(".")
        key = ".".join(key_parts)
        url = f"{ECB_BASE}/{dataset}/{key}"

        params = {
            "format": "csvdata",
            "startPeriod": start,
            "endPeriod": end,
        }

        last_err: Optional[Exception] = None
        for attempt in range(self.retry_count):
            try:
                logger.info(
                    f"ECB: pobieranie {series_id} ({start} → {end}), próba {attempt + 1}"
                )
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                df = pd.read_csv(io.StringIO(response.text))
                # Format ECB: kolumny TIME_PERIOD i OBS_VALUE
                df["date"] = pd.to_datetime(df["TIME_PERIOD"])
                df = df.set_index("date").sort_index()
                series = df["OBS_VALUE"].rename(series_id)

                if use_cache and self.cache_dir is not None:
                    self.cache_dir.mkdir(parents=True, exist_ok=True)
                    cache_path = self.cache_dir / f"ecb_{series_id.replace('.', '_')}_{start}_{end}.csv"
                    series.rename_axis("date").rename("value").to_csv(cache_path)
                return series
            except Exception as e:  # noqa: BLE001
                last_err = e
                logger.warning(f"ECB: błąd dla {series_id}: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay * (attempt + 1))

        assert last_err is not None
        raise RuntimeError(
            f"ECB: nie udało się pobrać {series_id} po {self.retry_count} próbach"
        ) from last_err
