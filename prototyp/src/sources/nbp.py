"""Adapter do API Narodowego Banku Polskiego.

Bez uwierzytelnienia. Dokumentacja: http://api.nbp.pl/
Ograniczenie: jeden request może obejmować maksymalnie 367 dni.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

logger = logging.getLogger(__name__)

NBP_BASE = "https://api.nbp.pl/api"
MAX_DAYS_PER_CALL = 367


class NBPSource:
    """Pobieranie kursów walut i wybranych statystyk monetarnych z NBP."""

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        retry_count: int = 3,
        retry_delay: float = 2.0,
    ):
        self.cache_dir = cache_dir
        self.retry_count = retry_count
        self.retry_delay = retry_delay

    def get_exchange_rate(
        self,
        currency: str,
        start: str,
        end: str,
        use_cache: bool = True,
    ) -> pd.Series:
        """Kurs danej waluty wyrażony w PLN za 1 jednostkę.

        Tabela A — kursy średnie NBP, codzienne dni robocze.

        Argumentem `currency` jest kod ISO (USD, EUR, GBP, ...). Zwracana
        seria nazywa się "PLN/{currency}".
        """
        if use_cache and self.cache_dir is not None:
            cache_path = self.cache_dir / f"nbp_{currency}_{start}_{end}.csv"
            if cache_path.exists():
                logger.debug(f"NBP: cache hit dla {currency}")
                df = pd.read_csv(cache_path, parse_dates=["date"], index_col="date")
                return df["value"]

        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)

        all_records = []
        chunk_start = start_dt
        while chunk_start <= end_dt:
            chunk_end = min(chunk_start + timedelta(days=MAX_DAYS_PER_CALL - 1), end_dt)
            chunk = self._fetch_chunk(currency, chunk_start, chunk_end)
            all_records.extend(chunk)
            chunk_start = chunk_end + timedelta(days=1)

        if not all_records:
            raise RuntimeError(f"NBP: brak danych dla {currency} ({start} → {end})")

        df = pd.DataFrame(all_records)
        df["date"] = pd.to_datetime(df["effectiveDate"])
        df = df.set_index("date").sort_index()
        series = df["mid"].rename(f"PLN/{currency}")

        if use_cache and self.cache_dir is not None:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            cache_path = self.cache_dir / f"nbp_{currency}_{start}_{end}.csv"
            series.rename_axis("date").rename("value").to_csv(cache_path)

        return series

    def _fetch_chunk(
        self, currency: str, start: datetime, end: datetime
    ) -> list[dict]:
        url = (
            f"{NBP_BASE}/exchangerates/rates/A/{currency}/"
            f"{start.strftime('%Y-%m-%d')}/{end.strftime('%Y-%m-%d')}/"
        )
        last_err: Optional[Exception] = None
        for attempt in range(self.retry_count):
            try:
                logger.info(
                    f"NBP: pobieranie {currency} "
                    f"{start:%Y-%m-%d}..{end:%Y-%m-%d} (próba {attempt + 1})"
                )
                response = requests.get(
                    url,
                    headers={"Accept": "application/json"},
                    timeout=30,
                )
                if response.status_code == 404:
                    logger.warning(
                        f"NBP: brak danych dla {currency} {start:%Y-%m-%d}..{end:%Y-%m-%d}"
                    )
                    return []
                response.raise_for_status()
                return response.json().get("rates", [])
            except Exception as e:  # noqa: BLE001
                last_err = e
                logger.warning(f"NBP: błąd dla {currency}: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay * (attempt + 1))

        assert last_err is not None
        raise RuntimeError(
            f"NBP: nie udało się pobrać {currency} po {self.retry_count} próbach"
        ) from last_err
