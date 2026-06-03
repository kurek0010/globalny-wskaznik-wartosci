"""Orkiestracja pobierania danych z czterech źródeł.

Uruchamianie:
    python -m prototyp.src.download

Lub jako moduł:
    from prototyp.src.download import download_all
    download_all()

Wymagania: zmienne środowiskowe (najlepiej w pliku prototyp/.env):
    FRED_API_KEY  — klucz API do FRED
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

import pandas as pd
from dotenv import load_dotenv

from .config import (
    ALL_SERIES,
    END_DATE,
    START_DATE,
    SeriesSpec,
)
from .sources.ecb import ECBSource
from .sources.fred import FredSource
from .sources.nbp import NBPSource
from .sources.yahoo import YahooSource


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("download")


# Ścieżki — relatywne do katalogu prototyp/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = PROJECT_ROOT / "data" / "raw"


def _fetch_one(
    label: str,
    spec: SeriesSpec,
    sources: Dict[str, object],
) -> pd.Series:
    """Pobierz pojedynczą serię, używając odpowiedniego źródła."""
    source = sources[spec["source"]]

    if spec["source"] == "fred":
        return source.get_series(spec["id"], START_DATE, END_DATE)  # type: ignore[attr-defined]
    if spec["source"] == "yahoo":
        return source.get_close(spec["id"], START_DATE, END_DATE)  # type: ignore[attr-defined]
    if spec["source"] == "ecb":
        return source.get_series(spec["id"], START_DATE, END_DATE)  # type: ignore[attr-defined]
    if spec["source"] == "nbp":
        # NBP traktujemy specjalnie — bo identyfikatorem jest waluta,
        # nie symbol serii. Dla M3_PL będzie osobna ścieżka (TODO).
        if spec["category"] == "currency":
            return source.get_exchange_rate(spec["id"], START_DATE, END_DATE)  # type: ignore[attr-defined]
        raise NotImplementedError(
            f"NBP dla kategorii {spec['category']} nie jest jeszcze obsługiwane"
        )

    raise ValueError(f"Nieznane źródło: {spec['source']}")


def download_all() -> Dict[str, pd.Series]:
    """Pobierz wszystkie serie z rejestru ALL_SERIES.

    Zwraca słownik {label: pd.Series}. Serie, których nie udało się
    pobrać, są pominięte z odpowiednim logiem ostrzegającym — pipeline
    nie kończy się błędem, bo niektóre serie M2 dla mniejszych gospodarek
    bywają chwilowo niedostępne lub mają zmienione identyfikatory.
    """
    load_dotenv(PROJECT_ROOT / ".env")

    sources = {
        "fred": FredSource(cache_dir=CACHE_DIR),
        "nbp": NBPSource(cache_dir=CACHE_DIR),
        "ecb": ECBSource(cache_dir=CACHE_DIR),
        "yahoo": YahooSource(cache_dir=CACHE_DIR),
    }

    results: Dict[str, pd.Series] = {}
    failures: Dict[str, str] = {}

    for label, spec in ALL_SERIES.items():
        try:
            logger.info(f"=== {label} ({spec['source']}:{spec['id']}) ===")
            series = _fetch_one(label, spec, sources)
            results[label] = series
            logger.info(
                f"OK: {label} → {len(series)} obserwacji, "
                f"od {series.index.min()} do {series.index.max()}"
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"NIE: {label} — {e}")
            failures[label] = str(e)

    logger.info(
        f"Podsumowanie: {len(results)} pobranych, {len(failures)} nieudanych"
    )
    if failures:
        logger.warning("Nieudane serie:")
        for label, msg in failures.items():
            logger.warning(f"  {label}: {msg}")

    return results


if __name__ == "__main__":
    download_all()
