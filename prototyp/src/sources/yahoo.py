"""Adapter do Yahoo Finance przez bibliotekę yfinance.

Bez uwierzytelnienia. Yahoo jest mniej stabilne niż FRED — używamy
tylko dla danych, których FRED nie udostępnia (np. Baltic Dry Index).
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


class YahooSource:
    """Pobieranie tickerów Yahoo z cachem CSV."""

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        retry_count: int = 3,
        retry_delay: float = 2.0,
    ):
        self.cache_dir = cache_dir
        self.retry_count = retry_count
        self.retry_delay = retry_delay

    def get_close(
        self,
        symbol: str,
        start: str,
        end: str,
        use_cache: bool = True,
    ) -> pd.Series:
        """Zwraca dzienną cenę zamknięcia jako pd.Series indeksowaną datą."""
        cache_key = symbol.replace("^", "idx_")
        if use_cache and self.cache_dir is not None:
            cache_path = self.cache_dir / f"yahoo_{cache_key}_{start}_{end}.csv"
            if cache_path.exists():
                logger.debug(f"Yahoo: cache hit dla {symbol}")
                df = pd.read_csv(cache_path, parse_dates=["date"], index_col="date")
                return df["value"]

        last_err: Optional[Exception] = None
        for attempt in range(self.retry_count):
            try:
                logger.info(
                    f"Yahoo: pobieranie {symbol} ({start} → {end}), próba {attempt + 1}"
                )
                df = yf.download(
                    symbol,
                    start=start,
                    end=end,
                    progress=False,
                    auto_adjust=True,
                )
                if df.empty:
                    raise RuntimeError(f"Yahoo: brak danych dla {symbol}")

                series = df["Close"]
                if isinstance(series, pd.DataFrame):
                    # yfinance czasem zwraca multiindex column
                    series = series.iloc[:, 0]
                series = series.rename(symbol)
                series.index.name = "date"

                if use_cache and self.cache_dir is not None:
                    self.cache_dir.mkdir(parents=True, exist_ok=True)
                    cache_path = self.cache_dir / f"yahoo_{cache_key}_{start}_{end}.csv"
                    series.rename("value").to_csv(cache_path)
                return series
            except Exception as e:  # noqa: BLE001
                last_err = e
                logger.warning(f"Yahoo: błąd dla {symbol}: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay * (attempt + 1))

        assert last_err is not None
        raise RuntimeError(
            f"Yahoo: nie udało się pobrać {symbol} po {self.retry_count} próbach"
        ) from last_err
