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


Source = Literal["fred", "nbp", "ecb", "yahoo", "worldbank"]
Frequency = Literal["daily", "weekly", "monthly", "yearly"]
Category = Literal[
    "commodity_price",
    "commodity_stock",
    "commodity_production",  # NOWE w v0.3 — roczna produkcja globalna
    "currency",
    "money_supply",
    "population",            # NOWE w v0.3 — populacja świata
    "inflation",             # NOWE w v0.3.1 — CPI głównych walut, dla hybrydy C
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
    # ---- CEE: agregaty M3 z ECB SDW (dataset BSI) -------------------
    # Identyfikatory poniżej to *najprawdopodobniejsze* serie ECB BSI dla
    # Polski/Czech/Węgier (broad money M3, miesięcznie, denominacja
    # w walucie krajowej). Wymagają weryfikacji w ECB Data Browser
    # (https://data.ecb.europa.eu/) — jeśli któraś nie istnieje, model
    # po prostu pominie ją z ostrzeżeniem, pipeline nie wywróci się.
    "M3_PL": {
        "source": "ecb", "id": "BSI.M.PL.N.A.M30.X.1.U2.2300.Z01.E",
        "freq": "monthly", "category": "money_supply", "unit": "PLN mn",
    },
    "M3_CZ": {
        "source": "ecb", "id": "BSI.M.CZ.N.A.M30.X.1.U2.2300.Z01.E",
        "freq": "monthly", "category": "money_supply", "unit": "CZK mn",
    },
    "M3_HU": {
        "source": "ecb", "id": "BSI.M.HU.N.A.M30.X.1.U2.2300.Z01.E",
        "freq": "monthly", "category": "money_supply", "unit": "HUF mn",
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


# =====================================================================
# NOWE W v0.3: populacja świata i produkcja zasobów
# =====================================================================

# ---------------------------------------------------------------------
# Populacja świata — World Bank
# Klucz formuły AUV v0.3: N(t) jako mianownik per-capita.
# ---------------------------------------------------------------------
POPULATION: Dict[str, SeriesSpec] = {
    "world_population": {
        "source": "worldbank", "id": "SP.POP.TOTL", "freq": "yearly",
        "category": "population", "unit": "people",
    },
}


# ---------------------------------------------------------------------
# Roczna produkcja globalna zasobów — World Bank gdzie dostępne
# Dla zasobów, których WB nie publikuje (większość metali), uzupełnimy
# w v0.3.1 ręcznie pobranymi CSV z USGS Mineral Commodity Summaries.
#
# Identyfikatory WB to częste agregaty na poziomie świata (country=WLD).
# Brakujące pozycje zaznaczone komentarzem TODO.
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Siła robocza — dla mianownika "dochód na pracownika" (AUV-T v0.4, krok 1).
# Dochód na pracownika jest bliższy "cenie pracy" niż dochód na osobę,
# bo wyklucza dzieci i emerytów (istotne przy starzeniu się populacji).
# ---------------------------------------------------------------------
LABOR: Dict[str, SeriesSpec] = {
    "labor_force_world": {
        "source": "worldbank", "id": "SL.TLF.TOTL.IN", "freq": "yearly",
        "category": "population", "unit": "people (labor force)",
    },
}


# ---------------------------------------------------------------------
# Jakość pieniądza — skład kolateralu (FDI v0.4, krok 3).
# Bilans Rezerwy Federalnej (H.4.1) i kredyt banków komercyjnych (H.8).
# Pozwala policzyć, PRZECIWKO czemu kreowany jest pieniądz: dług
# suwerenny (obligacje skarbowe) vs aktywa realne (hipoteki/MBS) vs
# kredyt produktywny. Na razie USA; docelowo EBC, BoJ, BoE.
# ---------------------------------------------------------------------
MONETARY_QUALITY: Dict[str, SeriesSpec] = {
    # --- Bilans Fed (strona aktywów) ---
    "fed_total_assets": {
        "source": "fred", "id": "WALCL", "freq": "weekly",
        "category": "money_supply", "unit": "USD mn (Fed total assets)",
    },
    "fed_treasuries": {
        "source": "fred", "id": "TREAST", "freq": "weekly",
        "category": "money_supply", "unit": "USD mn (Fed UST holdings)",
    },
    "fed_mbs": {
        "source": "fred", "id": "WSHOMCB", "freq": "weekly",
        "category": "money_supply", "unit": "USD mn (Fed MBS holdings)",
    },
    # --- Ceny nieruchomości (test inflacji aktywów vs CPI) ---
    "house_prices_us": {
        "source": "fred", "id": "CSUSHPISA", "freq": "monthly",
        "category": "money_supply", "unit": "Case-Shiller US HPI (SA)",
    },
    # --- Lepsza miara hipotek: CAŁY dług hipoteczny (z sekurytyzowanym) ---
    # HHMSDODNS = Households; Home Mortgages; Liability (Z.1), kwartalnie.
    # Łapie hipoteki niezależnie od tego, kto je trzyma (banki, GSE, ABS),
    # w przeciwieństwie do REALLN (tylko bilanse banków komercyjnych).
    "mortgage_debt_total": {
        "source": "fred", "id": "HHMSDODNS", "freq": "monthly",
        "category": "money_supply", "unit": "USD bn (home mortgage debt, all holders)",
    },
    # --- Podaż nowych domów (poszerza bazę dla hipotek) ---
    "housing_starts": {
        "source": "fred", "id": "HOUST", "freq": "monthly",
        "category": "money_supply", "unit": "tys. SAAR (nowe rozpoczęcia budów)",
    },
    "new_houses_for_sale": {
        "source": "fred", "id": "HNFSEPUSSA", "freq": "monthly",
        "category": "money_supply", "unit": "tys. (nowe domy na sprzedaż)",
    },
    # --- Indeksy giełdowe (analogia inwestycyjna do AUV-T) ---
    # OECD "Share Prices, All Shares", miesięczne, spójna metodologia
    # między krajami (2015=100). Do wyrażenia giełd w godzinach pracy.
    "stock_us": {
        "source": "fred", "id": "SPASTT01USM661N", "freq": "monthly",
        "category": "control", "unit": "OECD share price idx (2015=100)",
    },
    "stock_uk": {
        "source": "fred", "id": "SPASTT01GBM661N", "freq": "monthly",
        "category": "control", "unit": "OECD share price idx (2015=100)",
    },
    "stock_jp": {
        "source": "fred", "id": "SPASTT01JPM661N", "freq": "monthly",
        "category": "control", "unit": "OECD share price idx (2015=100)",
    },
    # --- Bilanse innych banków centralnych (krok d) — na razie SUMA aktywów.
    # Pełny skład kolateralu (jak UST/MBS dla Fed) nie jest dostępny w
    # porównywalnej formie dla EBC/BoJ — tu mierzymy ilość (ekspansję). ---
    "ecb_total_assets": {
        "source": "fred", "id": "ECBASSETSW", "freq": "weekly",
        "category": "money_supply", "unit": "EUR mn (ECB total assets)",
    },
    "boj_total_assets": {
        "source": "fred", "id": "JPNASSETS", "freq": "monthly",
        "category": "money_supply", "unit": "JPY 100mn (BoJ total assets)",
    },
    # --- Kredyt banków komercyjnych (H.8), skład wg typu zabezpieczenia ---
    "bank_credit_total": {
        "source": "fred", "id": "TOTBKCR", "freq": "weekly",
        "category": "money_supply", "unit": "USD bn (bank credit total)",
    },
    "bank_loans_realestate": {
        "source": "fred", "id": "REALLN", "freq": "weekly",
        "category": "money_supply", "unit": "USD bn (real estate loans)",
    },
    "bank_loans_business": {
        "source": "fred", "id": "BUSLOANS", "freq": "weekly",
        "category": "money_supply", "unit": "USD bn (C&I loans)",
    },
    "bank_loans_consumer": {
        "source": "fred", "id": "CONSUMER", "freq": "weekly",
        "category": "money_supply", "unit": "USD bn (consumer loans)",
    },
}


# ---------------------------------------------------------------------
# Produkcja metali i materiałów budowlanych — DANE RĘCZNE (AUV v0.4).
# Źródła w PDF/Excel: USGS Mineral Commodity Summaries, World Steel,
# CEMBUREAU. Wpisywane do data/manual/manual_production.csv.
# Służą jako proxy konsumpcji per capita (produkcja globalna / populacja).
# Dopóki plik jest pusty, koszyk używa stałego R dla tych kategorii.
# ---------------------------------------------------------------------
PRODUCTION_MANUAL: Dict[str, SeriesSpec] = {
    "steel_production_world": {
        "source": "manual", "id": "steel_production_world", "freq": "yearly",
        "category": "commodity_production", "unit": "Mt crude steel (World Steel)",
    },
    "cement_production_world": {
        "source": "manual", "id": "cement_production_world", "freq": "yearly",
        "category": "commodity_production", "unit": "Mt (USGS/CEMBUREAU)",
    },
    "copper_production_world": {
        "source": "manual", "id": "copper_production_world", "freq": "yearly",
        "category": "commodity_production", "unit": "kt mine (USGS)",
    },
    "aluminum_production_world": {
        "source": "manual", "id": "aluminum_production_world", "freq": "yearly",
        "category": "commodity_production", "unit": "kt primary (USGS)",
    },
    "iron_ore_production_world": {
        "source": "manual", "id": "iron_ore_production_world", "freq": "yearly",
        "category": "commodity_production", "unit": "Mt usable ore (USGS)",
    },
    "nickel_production_world": {
        "source": "manual", "id": "nickel_production_world", "freq": "yearly",
        "category": "commodity_production", "unit": "kt mine (USGS)",
    },
    "zinc_production_world": {
        "source": "manual", "id": "zinc_production_world", "freq": "yearly",
        "category": "commodity_production", "unit": "kt mine (USGS)",
    },
}


COMMODITY_PRODUCTION: Dict[str, SeriesSpec] = {
    # Żywność — World Bank ma dobre agregaty
    "cereal_production_world": {
        "source": "worldbank", "id": "AG.PRD.CREL.MT", "freq": "yearly",
        "category": "commodity_production", "unit": "metric tons",
    },
    "food_production_index": {
        "source": "worldbank", "id": "AG.PRD.FOOD.XD", "freq": "yearly",
        "category": "commodity_production", "unit": "index 2014-2016=100",
    },
    "livestock_production_index": {
        "source": "worldbank", "id": "AG.PRD.LVSK.XD", "freq": "yearly",
        "category": "commodity_production", "unit": "index 2014-2016=100",
    },
    # Energia — World Bank elektryczność (kWh) i zużycie/produkcja
    "electricity_production_world": {
        "source": "worldbank", "id": "EG.ELC.PROD.KH", "freq": "yearly",
        "category": "commodity_production", "unit": "kWh",
    },
    "energy_use_per_capita": {
        "source": "worldbank", "id": "EG.USE.PCAP.KG.OE", "freq": "yearly",
        "category": "commodity_production", "unit": "kg oil equivalent / capita",
    },
    # Ziemia i powierzchnia — przydatne jako mianownik dla nieruchomości
    "agricultural_land_world": {
        "source": "worldbank", "id": "AG.LND.AGRI.K2", "freq": "yearly",
        "category": "commodity_production", "unit": "sq km",
    },
    "arable_land_world": {
        "source": "worldbank", "id": "AG.LND.ARBL.ZS", "freq": "yearly",
        "category": "commodity_production", "unit": "% of land area",
    },
    # ---- v0.3.1: dodatkowe wskaźniki produkcji z WB ----
    "cereal_yield_kg_per_ha": {
        "source": "worldbank", "id": "AG.YLD.CREL.KG", "freq": "yearly",
        "category": "commodity_production", "unit": "kg/ha",
    },
    "electric_power_consumption_per_capita": {
        "source": "worldbank", "id": "EG.USE.ELEC.KH.PC", "freq": "yearly",
        "category": "commodity_production", "unit": "kWh/capita",
    },
    "renewable_energy_percent": {
        "source": "worldbank", "id": "EG.FEC.RNEW.ZS", "freq": "yearly",
        "category": "commodity_production", "unit": "% of total energy",
    },
    "fertilizer_consumption_per_ha": {
        "source": "worldbank", "id": "AG.CON.FERT.ZS", "freq": "yearly",
        "category": "commodity_production", "unit": "kg/ha arable",
    },
    "gdp_world_current_usd": {
        "source": "worldbank", "id": "NY.GDP.MKTP.CD", "freq": "yearly",
        "category": "commodity_production", "unit": "USD",
    },
    "gdp_per_capita_ppp": {
        "source": "worldbank", "id": "NY.GDP.PCAP.PP.CD", "freq": "yearly",
        "category": "commodity_production", "unit": "USD PPP/capita",
    },
    # TODO v0.4: pozyskać z USGS Mineral Commodity Summaries:
    #   - mine_production_copper (kt)
    #   - mine_production_aluminum (kt) — z bauksytu + huty
    #   - mine_production_iron_ore (Mt)
    #   - mine_production_lithium (kt LCE)
    #   - mine_production_cobalt (kt)
    # TODO v0.3.1: pozyskać z IEA / BP Energy Stats Review:
    #   - oil_production_world (Mb/d)
    #   - natgas_production_world (Bcm)
    #   - coal_production_world (Mt)
    #   - uranium_production_world (t)
    # TODO v0.3.1: pozyskać z USDA WASDE:
    #   - wheat_production_world (Mt)
    #   - corn_production_world (Mt)
    #   - rice_production_world (Mt)
    #   - soy_production_world (Mt)
}


# ---------------------------------------------------------------------
# Dodatkowe ceny surowców dla v0.3 — uzupełnienie z FRED
# (oprócz tych już zdefiniowanych w COMMODITY_PRICES)
# ---------------------------------------------------------------------
COMMODITY_PRICES_V3_EXTRA: Dict[str, SeriesSpec] = {
    "uranium": {
        "source": "fred", "id": "PURANUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/lb U3O8",
    },
    "coal_aus": {
        "source": "fred", "id": "PCOALAUUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "rice": {
        "source": "fred", "id": "PRICENPQUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "soy": {
        "source": "fred", "id": "PSOYBUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "palm_oil": {
        "source": "fred", "id": "PPOILUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "nickel": {
        "source": "fred", "id": "PNICKUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "zinc": {
        "source": "fred", "id": "PZINCUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "lead": {
        "source": "fred", "id": "PLEADUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
    "tin": {
        "source": "fred", "id": "PTINUSDM", "freq": "monthly",
        "category": "commodity_price", "unit": "USD/t",
    },
}


# ---------------------------------------------------------------------
# Materiały budowlane — kategoria "budownictwo" dla koszyka AUV-T (v0.4)
# ---------------------------------------------------------------------
# Uwaga metodologiczna: stal jest towarem globalnym, ale otwarta, długa
# (1996+) seria ceny globalnej w danych otwartych praktycznie nie istnieje;
# cement jest dobrem regionalnym (niski stosunek wartości do masy, słabo
# handlowany globalnie). Dlatego jako proxy używamy indeksów PPI z USA
# (FRED). Dla AUV-T to akceptowalne, bo każda seria i tak jest
# normalizowana do roku bazowego (t0 = 100) przed wejściem do koszyka —
# liczy się dynamika, nie poziom ani jednostka. Do oznaczenia jako proxy
# regionalne; docelowo do zastąpienia globalnym indeksem, jeśli powstanie.
CONSTRUCTION_MATERIALS: Dict[str, SeriesSpec] = {
    "steel": {
        "source": "fred", "id": "WPU101", "freq": "monthly",
        "category": "commodity_price", "unit": "PPI 1982=100 (US proxy)",
    },
    "cement": {
        "source": "fred", "id": "PCU327310327310", "freq": "monthly",
        "category": "commodity_price", "unit": "PPI (US proxy, cement mfg)",
    },
}


# =====================================================================
# NOWE W v0.3.1 (hybryda C): CPI głównych walut
# =====================================================================

# ---------------------------------------------------------------------
# CPI głównych walut z FRED.
# Używamy harmonizowanych OECD CPI (CPALTT01) gdzie dostępne —
# spójna metodologia między krajami.
#
# Dla hybrydy C: konsensus_CPI(t) = średnia ważona PKB z tych pięciu.
# AUV = real_component / consensus_CPI.
# ---------------------------------------------------------------------
CPI: Dict[str, SeriesSpec] = {
    "CPI_USA": {
        "source": "fred", "id": "CPIAUCSL", "freq": "monthly",
        "category": "inflation", "unit": "1982-84=100",
    },
    "CPI_EU": {
        "source": "fred", "id": "CP0000EZ19M086NEST", "freq": "monthly",
        "category": "inflation", "unit": "2015=100",
    },
    "CPI_JP": {
        "source": "fred", "id": "JPNCPIALLMINMEI", "freq": "monthly",
        "category": "inflation", "unit": "2015=100",
    },
    "CPI_UK": {
        "source": "fred", "id": "GBRCPIALLMINMEI", "freq": "monthly",
        "category": "inflation", "unit": "2015=100",
    },
    "CPI_CH": {
        "source": "fred", "id": "CHECPIALLMINMEI", "freq": "monthly",
        "category": "inflation", "unit": "2015=100",
    },
    # Dodatkowo dla porównań — wybrane rynki wschodzące
    "CPI_PL": {
        "source": "fred", "id": "POLCPIALLMINMEI", "freq": "monthly",
        "category": "inflation", "unit": "2015=100",
    },
    "CPI_BR": {
        "source": "fred", "id": "BRACPIALLMINMEI", "freq": "monthly",
        "category": "inflation", "unit": "2015=100",
    },
    "CPI_CN": {
        "source": "fred", "id": "CHNCPIALLMINMEI", "freq": "monthly",
        "category": "inflation", "unit": "2015=100",
    },
}
# Uwaga (v0.4): SDR NIE jest osobną serią do pobrania — to koszyk pięciu
# walut (USD, EUR, CNY, JPY, GBP). Jego "inflację" konstruujemy
# syntetycznie z CPI tych pięciu (już obecnych powyżej), z jawnymi,
# zamrożonymi wagami — patrz SDR_WEIGHTS w src/auv_t.py.


# ---------------------------------------------------------------------
# Agregaty — pełen rejestr serii do pobrania
# ---------------------------------------------------------------------
ALL_SERIES: Dict[str, SeriesSpec] = {
    **COMMODITY_PRICES,
    **COMMODITY_PRICES_V3_EXTRA,
    **CONSTRUCTION_MATERIALS,
    **CURRENCIES,
    **MONEY_SUPPLY,
    **COMMODITY_STOCKS,
    **POPULATION,
    **LABOR,
    **MONETARY_QUALITY,
    **PRODUCTION_MANUAL,
    **COMMODITY_PRODUCTION,
    **CPI,
}


def series_by_source(source: Source) -> Dict[str, SeriesSpec]:
    """Filtruj rejestr po źródle danych."""
    return {k: v for k, v in ALL_SERIES.items() if v["source"] == source}


def series_by_category(category: Category) -> Dict[str, SeriesSpec]:
    """Filtruj rejestr po kategorii."""
    return {k: v for k, v in ALL_SERIES.items() if v["category"] == category}
