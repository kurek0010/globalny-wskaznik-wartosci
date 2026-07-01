"""Adapter do World Bank Open Data API.

Bez uwierzytelnienia. Dokumentacja: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
URL format: https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json

World Bank dostarcza znacznie więcej niż populacja — wskaźniki produkcji
żywności, energii, metali, ekonomiki dla wszystkich krajów świata z
historią od 1960 (gdzie dostępna).

Konwencja: country='WLD' to świat. Inne istotne:
    EUU = Unia Europejska
    OED = OECD
    HIC = High Income Countries
    POL = Polska, USA = Stany Zjednoczone (kody ISO3)
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

logger = logging.getLogger(__name__)

WB_BASE = "https://api.worldbank.org/v2"


class WorldBankSource:
    """Pobieranie wskaźników z World Bank Open Data."""

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        retry_count: int = 3,
        retry_delay: float = 2.0,
        timeout: float = 60.0,
    ):
        self.cache_dir = cache_dir
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.timeout = timeout

    def get_indicator(
        self,
        indicator: str,
        country: str = "WLD",
        start: str = "1990",
        end: str = "2025",
        use_cache: bool = True,
    ) -> pd.Series:
        """Pobiera roczną serię wskaźnika WB dla danego kraju.

        Argumenty:
            indicator: kod wskaźnika WB, np. 'SP.POP.TOTL' (populacja),
                       'AG.PRD.CREL.MT' (produkcja zbóż, tony metryczne)
            country:   kod kraju ISO3 lub agregatu (WLD=świat)
            start:     rok startowy
            end:       rok końcowy

        Zwraca pd.Series z indeksem DatetimeIndex (rocznym, koniec roku).
        """
        cache_key = f"{country}_{indicator.replace('.', '_')}"
        if use_cache and self.cache_dir is not None:
            cache_path = self.cache_dir / f"wb_{cache_key}_{start}_{end}.csv"
            if cache_path.exists():
                logger.debug(f"WB: cache hit dla {indicator}")
                df = pd.read_csv(cache_path, parse_dates=["date"], index_col="date")
                return df["value"]

        url = f"{WB_BASE}/country/{country}/indicator/{indicator}"
        params = {
            "format": "json",
            "date": f"{start}:{end}",
            "per_page": 1000,
        }

        last_err: Optional[Exception] = None
        for attempt in range(self.retry_count):
            try:
                logger.info(
                    f"WB: pobieranie {indicator} dla {country} ({start}–{end}), próba {attempt + 1}"
                )
                response = requests.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()

                # WB zwraca [metadata, data]
                if not isinstance(data, list) or len(data) < 2 or not data[1]:
                    raise RuntimeError(f"WB: brak danych dla {indicator}/{country}")

                records = data[1]
                df = pd.DataFrame(
                    [
                        {
                            "date": pd.Timestamp(f"{r['date']}-12-31"),
                            "value": r["value"],
                        }
                        for r in records
                        if r["value"] is not None
                    ]
                )
                if df.empty:
                    raise RuntimeError(
                        f"WB: wszystkie wartości puste dla {indicator}/{country}"
                    )

                df = df.set_index("date").sort_index()
                series = df["value"].rename(f"WB_{indicator}_{country}")

                if use_cache and self.cache_dir is not None:
                    self.cache_dir.mkdir(parents=True, exist_ok=True)
                    cache_path = self.cache_dir / f"wb_{cache_key}_{start}_{end}.csv"
                    series.rename_axis("date").rename("value").to_csv(cache_path)

                return series

            except Exception as e:  # noqa: BLE001
                last_err = e
                logger.warning(f"WB: błąd dla {indicator}/{country}: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay * (attempt + 1))

        assert last_err is not None
        raise RuntimeError(
            f"WB: nie udało się pobrać {indicator}/{country} po {self.retry_count} próbach"
        ) from last_err
