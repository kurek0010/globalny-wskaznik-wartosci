# Prototyp obliczeniowy Talenta

Kod referencyjny liczący jednostkę **Talent (TLN)** — środek geometryczny indeksu cen i indeksu płac, √(C×W) — oraz przeprowadzający testy historyczne (minimax regret) i budujący stronę.

Zasada projektu: **kod jest metodologią**. Wszystkie liczby cytowane w dokumentach dają się odtworzyć z tych skryptów i publicznych danych.

## Wymagania

- Python 3.10 lub nowszy
- FRED API key (bezpłatny): https://fred.stlouisfed.org/docs/api/api_key.html

## Setup

```bash
# w katalogu prototyp/
python3 -m venv .venv
source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt

cp .env.example .env          # wklej swój FRED_API_KEY
```

Dane wejściowe są dołączone w `data/` (surowe pobrania + przetworzone wyniki), więc skrypty analiz i builder działają bez ponownego pobierania.

## Najczęstsze polecenia

```bash
python src/talent_daily.py     # kotwice miesięczne + ścieżka dzienna Talenta
python src/regret_century.py   # test stulecia USA (1929–2025)
python src/regret_poland.py    # Polska 1989–2024
python src/regret_bilateral.py # jednostka dwustronna PL–US
python src/build_strona.py     # przebudowa wszystkich plików HTML w korzeniu repo
```

Aktualizacja miesięczna (kotwica): `python src/fetch_gus.py` → `python src/talent_update.py` → `python src/build_strona.py`. Szczegóły i kalendarz: `../INSTRUKCJA_aktualizacji.md`.

## Struktura

```
prototyp/
├── README.md              ← ten plik
├── requirements.txt
├── .env.example           (skopiuj do .env — Twój klucz FRED, gitignored)
│
├── src/
│   ├── talent_daily.py    kotwice miesięczne + ścieżka dzienna
│   ├── talent_update.py   dołożenie nowej kotwicy (aktualizacja miesięczna)
│   ├── fetch_gus.py       pobranie first-printów GUS (płace, zatrudnienie)
│   ├── regret_century.py  test USA 1929–2025 (minimax regret)
│   ├── regret_poland.py   test Polska 1989–2024
│   ├── regret_bilateral.py jednostka dwustronna (PL–US)
│   ├── backtest_1900.py   test wsteczny na długiej serii
│   ├── build_strona.py    JEDYNE źródło plików HTML w korzeniu repo
│   ├── strona_szablon.html szablon strony głównej
│   ├── config.py          rejestr publicznych serii danych
│   ├── download.py        orkiestracja pobierania
│   ├── harmonize.py       ujednolicenie częstotliwości i okresów
│   └── sources/           adaptery: FRED, NBP, ECB, World Bank, Yahoo, manual
│
└── data/
    ├── raw/               surowe pobrania (dokumentacyjne — patrz POLITYKA_danych)
    ├── manual/            ręcznie wprowadzone serie (backtest historyczny)
    └── processed/         daily.parquet, monthly.parquet, talent_* , regret_*
```

## Dane

Wszystkie serie pochodzą z publicznych, weryfikowalnych źródeł (FRED, NBP, ECB, World Bank, GUS) — zgodnie z zasadą heliocentryczną (patrz `../PROFIL_AUTORA.md`). Rejestr źródeł, dni publikacji i kaskady awaryjne: `../POLITYKA_danych_v0.1.md`. Jeśli któreś źródło jest chwilowo niedostępne, pipeline pomija problematyczną serię z ostrzeżeniem i kontynuuje.

## Zmiany metodologii

Każda zmiana formuły, źródeł lub reguły publikacyjnej przechodzi przez proces **TIP** (`../TIP/README.md`): nazwij problem → zaproponuj → przetestuj na danych → dopiero zmień regułę, nigdy wstecz.
