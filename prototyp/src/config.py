"""Centralny rejestr serii danych dla prototypu AUV v0.2.

Każda seria opisana jako:
    {
        "source": "fred" | "nbp" | "ecb" | "yahoo",
        "id":      <identyfikator w danym źródle>,
        "freq":    "daily" | "weekly" | "monthly",
        "category": "commodity_price" | "commodity_stock" |
                    "currency" | "money_supply" | "control",
        "unit":    "USD/bbl" | "PLN/USD" | ... (informacyjnie),
    }

Wszystkie kursy walutowe traktujemy jako KURS_USD_PER_X (jednostek
waluty obcej za 1 USD), niezależnie od konwencji źródła — normalizacja
robi się w `harmonize.py`. W konsekwencji wzrost wartości waluty obcej
zawsze oznacza spadek odpowiadającej serii kursowej.
"""

from typing import Dict, Literal, TypedDict


Source = Literal["fred", "nbp", "ecb", "yahoo"]
Frequency = Literal["daily", "weekly", "monthly", "yearly"]
Category = Literal[
    "commodity_price",
    "commodity_stock",
    "currency",
    "money_supply",
    "control",
]


class SeriesSpec(TypedDict):
    source: Source
    id: str
    freq: Frequency
    category: Category
    unit: str


# Okres pokrycia bazowego — patrz PROTOTYP_PLAN_v0.2.md sekcja 2.5
START_DATE = "1996-01-01"
END_DATE = "2025-12-31"


# ---------------------------------------------------------------------
# Ceny surowców (CORE i kontrolne)
# ---------------------------------------------------------------------
COMMODITY_PRICES: Dict[str, SeriesSpec] = {
    "brent": {
        "source": "fred", "id": "DCOILBRENTEU", "freq": "daily",
        "category": "commodity_price", "unit": "USD/bbl",
    },
    "wti": {
        "source": "fred", "id": "DCOILWTICO", "freq": "daily",
        "category": "commodity_price", "unit": "USD/bbl",
    },
    "natgas_us": {
        "source": "fred", "id": "DHHNGSP", "freq": "daily",
        "category": "commodity_price", "unit": "USD/MMBtu",
    },
    "wheat": {
        "source": "fred", "id": "PWHEAMTUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "corn": {
        "source": "fred", "id": "PMAIZMTUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "copper": {
        "source": "fred", "id": "PCOPPUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "aluminum": {
        "source": "fred", "id": "PALUMUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "iron_ore": {
        "source": "fred", "id": "PIORECRUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/dmtu",
    },
    "gold": {
        "source": "fred", "id": "GOLDAMGBD228NLBM", "freq": "daily",
        "category": "control", "unit": "USD/oz",
    },
    "baltic_dry": {
        "source": "yahoo", "id": "^BDI", "freq": "daily",
        "category": "commodity_price", "unit": "index",
    },
}


# ---------------------------------------------------------------------
# Waluty — 18 par
# Konwencja: każda seria mierzy "ile jednostek waluty obcej za 1 USD".
# Dla par typu EUR/USD czy GBP/USD musimy odwrócić wartości w
# harmonize.py, bo FRED publikuje je jako USD/EUR (USD za 1 EUR).
# ---------------------------------------------------------------------
CURRENCIES: Dict[str, SeriesSpec] = {
    "EUR": {
        "source": "fred", "id": "DEXUSEU", "freq": "daily",
        "category": "currency", "unit": "USD/EUR (invert)",
    },
    "JPY": {
        "source": "fred", "id": "DEXJPUS", "freq": "daily",
        "category": "currency", "unit": "JPY/USD",
    },
    "GBP": {
        "source": "fred", "id": "DEXUSUK", "freq": "daily",
        "category": "currency", "unit": "USD/GBP (invert)",
    },
    "CHF": {
        "source": "fred", "id": "DEXSZUS", "freq": "daily",
        "category": "currency", "unit": "CHF/USD",
    },
    "CNY": {
        "source": "fred", "id": "DEXCHUS", "freq": "daily",
        "category": "currency", "unit": "CNY/USD",
    },
    "INR": {
        "source": "fred", "id": "DEXINUS", "freq": "daily",
        "category": "currency", "unit": "INR/USD",
    },
    "BRL": {
        "source": "fred", "id": "DEXBZUS", "freq": "daily",
        "category": "currency", "unit": "BRL/USD",
    },
    "MXN": {
        "source": "fred", "id": "DEXMXUS", "freq": "daily",
        "category": "currency", "unit": "MXN/USD",
    },
    "KRW": {
        "source": "fred", "id": "DEXKOUS", "freq": "daily",
        "category": "currency", "unit": "KRW/USD",
    },
    "AUD": {
        "source": "fred", "id": "DEXUSAL", "freq": "daily",
        "category": "currency", "unit": "USD/AUD (invert)",
    },
    "CAD": {
        "source": "fred", "id": "DEXCAUS", "freq": "daily",
        "category": "currency", "unit": "CAD/USD",
    },
    "SGD": {
        "source": "fred", "id": "DEXSIUS", "freq": "daily",
        "category": "currency", "unit": "SGD/USD",
    },
    "ZAR": {
        "source": "fred", "id": "DEXSFUS", "freq": "daily",
        "category": "currency", "unit": "ZAR/USD",
    },
    "TRY": {
        "source": "fred", "id": "DEXTUUS", "freq": "daily",
        "category": "currency", "unit": "TRY/USD",
    },
    "SEK": {
        "source": "fred", "id": "DEXSDUS", "freq": "daily",
        "category": "currency", "unit": "SEK/USD",
    },
    "PLN": {
        "source": "nbp", "id": "USD", "freq": "daily",
        "category": "currency", "unit": "PLN/USD",
    },
    "CZK": {
        "source": "ecb", "id": "EXR.D.CZK.EUR.SP00.A", "freq": "daily",
        "category": "currency", "unit": "CZK/EUR (cross via EUR)",
    },
    "HUF": {
        "source": "ecb", "id": "EXR.D.HUF.EUR.SP00.A", "freq": "daily",
        "category": "currency", "unit": "HUF/EUR (cross via EUR)",
    },
}


# ---------------------------------------------------------------------
# Podaż pieniądza per kraj / blok
# Każdy region monetarny dostaje swój własny agregat.
# Dla niektórych krajów dane mogą mieć luki — to akceptujemy
# i obsłużymy fallbackami w harmonize.py.
# ---------------------------------------------------------------------
MONEY_SUPPLY: Dict[str, SeriesSpec] = {
    "M2_USA": {
        "source": "fred", "id": "M2SL", "freq": "monthly",
        "category": "money_supply", "unit": "USD bn",
    },
    "M3_EU": {
        "source": "fred", "id": "MYAGM3EZM196N", "freq": "monthly",
        "category": "money_supply", "unit": "EUR bn",
    },
    "M3_UK": {
        "source": "fred", "id": "MABMM301GBM189S", "freq": "monthly",
        "category": "money_supply", "unit": "GBP bn",
    },
    "M2_JP": {
        "source": "fred", "id": "MABMM301JPM189S", "freq": "monthly",
        "category": "money_supply", "unit": "JPY bn",
    },
    "M2_CN": {
        "source": "fred", "id": "MYAGM2CNM189N", "freq": "monthly",
        "category": "money_supply", "unit": "CNY bn",
    },
    "M2_BR": {
        "source": "fred", "id": "MYAGM2BRM189N", "freq": "monthly",
        "category": "money_supply", "unit": "BRL bn",
    },
    "M2_IN": {
        "source": "fred", "id": "MYAGM2INM189N", "freq": "monthly",
        "category": "money_supply", "unit": "INR bn",
    },
    "M3_PL": {
        "source": "nbp", "id": "M3", "freq": "monthly",
        "category": "money_supply", "unit": "PLN bn",
    },
}


# ---------------------------------------------------------------------
# Ilości i zapasy surowców — dane wspomagające (sekcja 2.4 planu)
# ---------------------------------------------------------------------
COMMODITY_STOCKS: Dict[str, SeriesSpec] = {
    "oil_stocks_us": {
        "source": "fred", "id": "WCESTUS1", "freq": "weekly",
        "category": "commodity_stock", "unit": "thousand bbl",
    },
    "natgas_stocks_us": {
        "source": "fred", "id": "WNGSUS1", "freq": "weekly",
        "category": "commodity_stock", "unit": "Bcf",
    },
}


# ---------------------------------------------------------------------
# Agregaty — pełen rejestr serii do pobrania
# ---------------------------------------------------------------------
ALL_SERIES: Dict[str, SeriesSpec] = {
    **COMMODITY_PRICES,
    **CURRENCIES,
    **MONEY_SUPPLY,
    **COMMODITY_STOCKS,
}


def series_by_source(source: Source) -> Dict[str, SeriesSpec]:
    """Filtruj rejestr po źródle danych."""
    return {k: v for k, v in ALL_SERIES.items() if v["source"] == source}


def series_by_category(category: Category) -> Dict[str, SeriesSpec]:
    """Filtruj rejestr po kategorii."""
    return {k: v for k, v in ALL_SERIES.items() if v["category"] == category}
