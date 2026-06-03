# Prototyp Obliczeniowy AUV — v0.2

Implementacja pierwszej iteracji empirycznej weryfikacji koncepcji *Absolute Unit of Value*. Pełny opis metodologii: `../PROTOTYP_PLAN_v0.2.md`.

## Cel

Sprawdzić na 30-letnich danych historycznych (1996–2025), czy istnieje stabilna kombinacja wag $w_i$ dla koszyka surowców i walut, która produkuje wskaźnik AUV najmniej skorelowany z agregatami pieniężnymi M2 najważniejszych gospodarek.

## Wymagania

- Python 3.10 lub nowszy
- FRED API key (bezpłatny) — założenie: https://fred.stlouisfed.org/docs/api/api_key.html

## Setup

```bash
# w katalogu prototyp/
python3 -m venv .venv
source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt

# skonfiguruj klucz FRED
cp .env.example .env
# wyedytuj .env i wklej swój FRED_API_KEY
```

## Pierwsze Uruchomienie

Pobranie wszystkich serii i ujednolicenie do siatki dziennej + miesięcznej:

```bash
python -m src.harmonize
```

To pobierze ok. 40 serii czasowych (cache do `data/raw/`), wyrówna do dziennej siatki dni roboczych (cache do `data/processed/`) i wyświetli raport kompletności każdej serii.

Pierwsze uruchomienie zajmie kilka minut (pobieranie). Kolejne uruchomienia są błyskawiczne dzięki cache CSV.

## Struktura

```
prototyp/
├── PROTOTYP_PLAN_v0.2.md  ← (w katalogu nadrzędnym)
├── README.md              ← ten plik
├── requirements.txt
├── .env.example
├── .env                   ← gitignored, Twój klucz FRED
│
├── src/
│   ├── config.py          centralny rejestr ~40 serii danych
│   ├── sources/
│   │   ├── fred.py        adapter FRED (z retry + cache)
│   │   ├── nbp.py         adapter NBP (PLN, M3)
│   │   ├── ecb.py         adapter ECB SDW (CZK, HUF)
│   │   └── yahoo.py       adapter Yahoo (BDI)
│   ├── download.py        orkiestracja pobierania
│   ├── harmonize.py       alignment częstotliwości i okresów
│   ├── optimize.py        TODO — QP + FWL + PCA
│   └── viz.py             TODO — wizualizacje
│
├── notebooks/
│   ├── 01_eda.ipynb       TODO — analiza eksploracyjna, wybór t_0
│   ├── 02_optimization.ipynb  TODO — uruchomienie optymalizacji
│   └── 03_results.ipynb       TODO — wykresy końcowe
│
├── data/
│   ├── raw/               gitignored — pobrane CSV
│   └── processed/         gitignored — daily.parquet, monthly.parquet
│
└── outputs/               gitignored — wyniki uruchomień
    ├── weights.json
    ├── auv_series.csv
    └── figures/
```

## Dane

Prototyp pobiera ok. 40 serii z czterech publicznych źródeł — wszystkie wymienione szczegółowo w `src/config.py`. Brak żadnych źródeł subskrypcyjnych (zgodnie z filozofią heliocentryczną, patrz `../PROFIL_AUTORA.md`).

W razie chwilowych niedostępności któregoś źródła, pipeline pomija problematyczne serie z ostrzeżeniem i kontynuuje pracę. Nie przerywamy całego pobierania z powodu jednej brakującej waluty.

## Następne Kroki Implementacyjne

Po sukcesie kroku pobierania + harmonizacji:

1. Notebook `01_eda.ipynb` — wykresy szeregów, identyfikacja reżimów, wybór $t_0$.
2. Implementacja `src/optimize.py` — dwuetapowe Frisch-Waugh-Lovell + QP w CVXPY.
3. Notebook `02_optimization.ipynb` — uruchomienie i walidacja krzyżowa PCA.
4. Notebook `03_results.ipynb` — wykresy końcowe, AUV(t), porównania.

## Co Świadomie NIE Robimy w v0.2

- Komponentu kosztu pracy ludzkiej (kwartalna częstotliwość, do v0.3).
- Energii elektrycznej spot (dane regionalne skomplikowane, do v0.3).
- Walut z hiperinflacją (ARS, VES — dane FRED problematyczne).
- Kryptowalut (rezerwowane dla warstwy PRO).
- Codziennej publikacji live (faza produkcyjna).

Pełna lista i uzasadnienia: `../PROTOTYP_PLAN_v0.2.md` sekcja 10.
