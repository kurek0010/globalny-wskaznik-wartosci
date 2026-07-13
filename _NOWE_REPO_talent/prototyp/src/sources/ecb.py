"""Adapter do ECB Statistical Data Warehouse.

Bez uwierzytelnienia. Dokumentacja: https://data.ecb.europa.eu/help/api/data

Zachowanie zaktualizowane w v0.2 prototypu:
    - Domyślny timeout zwiększony z 30 do 90 sekund (ECB SDW bywa wolne
      dla długich szeregów).
    - Zapytania domyślnie chunkowane na okna 5-letnie, co radykalnie
      zmniejsza ryzyko timeoutu (każde okno = mniejszy ładunek odpowiedzi).
"""

from __future__ import annotations

import io
import logging
import time
from pathlib import Path
from typing import List, Optional

import pandas as pd
import requests

logger = logging.getLogger(__name__)

ECB_BASE = "https://data-api.ecb.europa.eu/service/data"


class ECBSource:
    """Pobieranie szeregów czasowych z ECB SDW z chunkowaniem i retry."""

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        retry_count: int = 3,
        retry_delay: float = 2.0,
        timeout: float = 90.0,
        chunk_years: int = 5,
    ):
        self.cache_dir = cache_dir
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.chunk_years = chunk_years

    def get_series(
        self,
        series_id: str,
        start: str,
        end: str,
        use_cache: bool = True,
    ) -> pd.Series:
        """Pobierz serię ECB.

        Argumentem `series_id` jest pełny klucz w formacie
        ``DATASET.DIM1.DIM2...``, np. ``EXR.D.CZK.EUR.SP00.A`` dla
        kursu dziennego CZK/EUR.
        """
        cache_key = series_id.replace(".", "_")
        if use_cache and self.cache_dir is not None:
            cache_path = self.cache_dir / f"ecb_{cache_key}_{start}_{end}.csv"
            if cache_path.exists():
                logger.debug(f"ECB: cache hit dla {series_id}")
                df = pd.read_csv(cache_path, parse_dates=["date"], index_col="date")
                return df["value"]

        # Chunkowanie po latach
        start_ts = pd.Timestamp(start)
        end_ts = pd.Timestamp(end)

        chunks: List[pd.Series] = []
        chunk_start = start_ts
        while chunk_start <= end_ts:
            chunk_end = min(
                chunk_start + pd.DateOffset(years=self.chunk_years) - pd.DateOffset(days=1),
                end_ts,
            )
            try:
                part = self._fetch_chunk(series_id, chunk_start, chunk_end)
                if part is not None and not part.empty:
                    chunks.append(part)
            except RuntimeError as e:
                logger.warning(
                    f"ECB: pomijam okno {chunk_start:%Y-%m-%d}..{chunk_end:%Y-%m-%d} "
                    f"dla {series_id}: {e}"
                )
            chunk_start = chunk_end + pd.DateOffset(days=1)

        if not chunks:
            raise RuntimeError(
                f"ECB: nie udało się pobrać żadnego okna dla {series_id}"
            )

        series = pd.concat(chunks).sort_index()
        # Usuń duplikaty (na granicy okien może się zdarzyć)
        series = series[~series.index.duplicated(keep="first")]
        series.name = series_id

        if use_cache and self.cache_dir is not None:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            cache_path = self.cache_dir / f"ecb_{cache_key}_{start}_{end}.csv"
            series.rename_axis("date").rename("value").to_csv(cache_path)

        return series

    def _fetch_chunk(
        self,
        series_id: str,
        start: pd.Timestamp,
        end: pd.Timestamp,
    ) -> Optional[pd.Series]:
        """Pobierz jedno okno czasowe (z retry)."""
        dataset, *key_parts = series_id.split(".")
        key = ".".join(key_parts)
        url = f"{ECB_BASE}/{dataset}/{key}"
        params = {
            "format": "csvdata",
            "startPeriod": start.strftime("%Y-%m-%d"),
            "endPeriod": end.strftime("%Y-%m-%d"),
        }

        last_err: Optional[Exception] = None
        for attempt in range(self.retry_count):
            try:
                logger.info(
                    f"ECB: pobieranie {series_id} "
                    f"{start:%Y-%m-%d}..{end:%Y-%m-%d} (próba {attempt + 1})"
                )
                response = requests.get(url, params=params, timeout=self.timeout)
                if response.status_code == 404:
                    logger.warning(
                        f"ECB: 404 dla {series_id} "
                        f"{start:%Y-%m-%d}..{end:%Y-%m-%d} — brak danych w tym oknie"
                    )
                    return None
                response.raise_for_status()
                df = pd.read_csv(io.StringIO(response.text))
                if "TIME_PERIOD" not in df.columns:
                    logger.warning(
                        f"ECB: odpowiedź dla {series_id} bez kolumny TIME_PERIOD "
                        f"(prawdopodobnie pusta)"
                    )
                    return None
                df["date"] = pd.to_datetime(df["TIME_PERIOD"])
                df = df.set_index("date").sort_index()
                return df["OBS_VALUE"]
            except Exception as e:  # noqa: BLE001
                last_err = e
                logger.warning(
                    f"ECB: błąd dla {series_id} "
                    f"{start:%Y-%m-%d}..{end:%Y-%m-%d}: {e}"
                )
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay * (attempt + 1))

        assert last_err is not None
        raise RuntimeError(
            f"ECB: nie udało się pobrać okna "
            f"{start:%Y-%m-%d}..{end:%Y-%m-%d} po {self.retry_count} próbach"
        ) from last_err
