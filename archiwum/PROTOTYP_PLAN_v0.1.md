# Plan Techniczny Prototypu Obliczeniowego AUV — v0.1

**Status:** Plan do zatwierdzenia przed kodowaniem.
**Cel:** Empiryczna weryfikacja, czy metodologia z `AUV_zalozenia_v0.2.md` produkuje sensowny wskaźnik na realnych danych historycznych.

---

## 1. Cel i Zakres

Prototyp ma odpowiedzieć na trzy pytania:

1. Czy istnieje stabilna kombinacja wag $w_i$, dla której koszyk surowców i walut wykazuje minimalną korelację z agregatami M2?
2. Czy wynikowy szereg AUV(t) zachowuje się sensownie w okresach kryzysowych (1973–75, 1979–82, 2008, 2020, 2022)? "Sensownie" oznacza: AUV powinien być bardziej stabilny niż pojedyncze waluty, ale reagować na rzeczywiste szoki podażowe.
3. Czy wagi z QP są zbliżone do wag z analizy PCA (walidacja krzyżowa)?

**Świadomie wykluczone z prototypu v0.1** (do następnych iteracji): komponent pracy ludzkiej (kwartalna częstotliwość komplikuje pipeline), pełna warstwa PRO, integracja z Bitcoinem, anomaly detection, dashboard publiczny, automatyczna codzienna publikacja.

## 2. Dane Wejściowe — Konkretne Szeregi

Strategia: maksymalnie polegać na **FRED** (jedna API, jedne uwierzytelnienie, jakość gwarantowana). Yahoo Finance jako fallback dla tego, czego FRED nie ma.

### Surowce — 10 pozycji

| Pozycja | Źródło | Symbol | Częstotliwość |
| --- | --- | --- | --- |
| Ropa Brent | FRED | `DCOILBRENTEU` | dzienna |
| Ropa WTI | FRED | `DCOILWTICO` | dzienna |
| Gaz ziemny Henry Hub | FRED | `DHHNGSP` | dzienna |
| Pszenica (miesięcznie) | FRED | `PWHEAMTUSDM` | miesięczna |
| Kukurydza (miesięcznie) | FRED | `PMAIZMTUSDM` | miesięczna |
| Miedź | FRED | `PCOPPUSDM` | miesięczna |
| Aluminium | FRED | `PALUMUSDM` | miesięczna |
| Ruda żelaza | FRED | `PIORECRUSDM` | miesięczna |
| Złoto (kontrola, nie do CORE) | FRED | `GOLDAMGBD228NLBM` | dzienna |
| Indeks BDI (Baltic Dry) | Yahoo | `^BDI` | dzienna |

### Waluty — 8 par przeciwko USD

Wszystkie z FRED:

| Para | Symbol FRED |
| --- | --- |
| EUR/USD | `DEXUSEU` |
| USD/JPY | `DEXJPUS` |
| GBP/USD | `DEXUSUK` |
| USD/CHF | `DEXSZUS` |
| USD/CNY | `DEXCHUS` |
| USD/INR | `DEXINUS` |
| USD/BRL | `DEXBZUS` |
| USD/MXN | `DEXMXUS` |

PLN i inne waluty CEE pojawią się w wersji v0.2 (ECB lub NBP API).

### Agregaty M2 (funkcja celu, nie składnik)

- M2 USA: FRED `M2SL` (miesięczna)
- M2 strefa euro: FRED `MYAGM2EZM196N` (miesięczna)
- M2 Chiny: pominięte w prototypie v0.1 (brak czystego API; w v0.2 ECB lub PBOC bezpośrednio)

### Okres: 1996-01-01 → 2025-12-31

Dlaczego od 1996: pełne pokrycie wszystkich serii FX, post-Mexican-crisis stabilizacja, dane dostępne dla wszystkich wymienionych źródeł.

## 3. Pipeline Danych

```
[FRED API] ──┐
             ├── [download.py] ── data/raw/*.csv
[Yahoo] ─────┘                          │
                                        │
                                        v
                              [harmonize.py]
                                        │
                                        ├── częstotliwość miesięczna (lowest common)
                                        ├── forward-fill dni wolnych
                                        ├── obcięcie do wspólnego okresu (1996–2025)
                                        │
                                        v
                              data/processed/aligned.parquet
                                        │
                                        v
                              [eda.ipynb] ── wykresy, statystyki, identyfikacja reżimów
                                        │
                                        v
                              [optimize.py] ── QP + PCA
                                        │
                                        v
                              outputs/weights.json
                              outputs/auv_series.csv
                              outputs/figures/*.png
```

## 4. Analiza Eksploracyjna (EDA)

Cel: wybrać $t_0$ i zidentyfikować ewentualne strukturalne załamania w danych.

Zakres wizualizacji i statystyk:

- Wykresy szeregowe wszystkich składników (skala log, znormalizowane do 1996 = 1)
- Macierz korelacji między składnikami (rolling 5-letnia, dla widoczności zmiany reżimu)
- Test Bai-Perron dla wykrywania momentów strukturalnych załamań
- Wykres M2 nakładający się z wybranymi surowcami — sprawdzenie wizualne, czy hipoteza o "kotwicy anty-M2" jest realistyczna
- Wybór trzech kandydatów na $t_0$: środkowe daty w okresach 1996–1999, 2003–2006, 2015–2019 (test wrażliwości w sekcji 7)

## 5. Optymalizacja — Implementacja QP

```python
import cvxpy as cp

# Zmienne: wagi w_i (nieujemne, sumujące się do 1)
w = cp.Variable(N, nonneg=True)

# Wartość koszyka w czasie (log)
basket_log = cp.log(prices @ w)  # uwaga: nieliniowe, wymaga reformulacji

# Funkcja celu: minimalizuj kowariancję z log(M2)
# W praktyce — najpierw obliczamy deviacje, potem QP

objective = cp.Minimize(cp.quad_form(w, covariance_matrix_with_m2))
constraints = [cp.sum(w) == 1, w >= 0]

problem = cp.Problem(objective, constraints)
problem.solve()
```

Uwaga: formuła z logarytmem nie jest bezpośrednio kwadratowa. Reformułujemy: zamiast minimalizować korelację z log(M2), minimalizujemy *kowariancję pierwszych różnic logarytmicznych* koszyka i M2. To jest poprawne kwadratowe sformułowanie.

## 6. Walidacja Krzyżowa — PCA

Niezależna metoda: PCA na zlogarytmowanych szeregach, identyfikacja pierwszej składowej, której obciążenie na M2 jest największe (to "komponent inflacyjny"), i obliczenie wag jako rzut pozostałych składowych. Porównanie z wagami QP — jeśli zbliżone (korelacja > 0,7), mamy wzajemne potwierdzenie.

## 7. Wyniki — Co Pokazujemy

- Tabela wag CORE (15 do 18 składników) z QP i PCA obok siebie
- Wykres szeregu AUV(t) za cały okres, nakładający się z indeksem CPI-USA i z ceną złota (oba w log)
- Wykres "AUV / pojedyncza waluta" dla USD, EUR, PLN — pokazujący realną deprecjację
- Tabela "wartość 1 jednostki w 1996 vs 2025" dla wybranych aktywów (mieszkanie, hamburger, ropa, itd. — w miarę dostępności danych)
- Test wrażliwości: jak zmienia się AUV przy różnych wyborach $t_0$ z sekcji 4

## 8. Struktura Kodu w Repozytorium

```
prototyp/
├── README.md
├── requirements.txt
├── .env.example          # template dla FRED_API_KEY
├── data/
│   ├── raw/              # gitignored (cache pobranych CSV)
│   └── processed/        # gitignored (aligned.parquet)
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_optimization.ipynb
│   └── 03_results.ipynb
├── src/
│   ├── __init__.py
│   ├── download.py       # pobranie z FRED i Yahoo
│   ├── harmonize.py      # częstotliwości, FFill, alignment
│   ├── optimize.py       # QP + PCA
│   └── viz.py            # wykresy
└── outputs/
    ├── weights.json
    ├── auv_series.csv
    └── figures/
```

## 9. Zależności (requirements.txt)

```
pandas>=2.0
numpy>=1.24
fredapi>=0.5
yfinance>=0.2
cvxpy>=1.4
scikit-learn>=1.3
matplotlib>=3.7
plotly>=5.17
jupyter>=1.0
pyarrow>=14.0
python-dotenv>=1.0
```

## 10. Czego Prototyp NIE Zrobi (Świadome Ograniczenia)

- Brak komponentu pracy (do v0.2 prototypu)
- Brak komponentu energii elektrycznej (dane spot nie są w FRED w wygodnej formie)
- Brak walut wysokoinflacyjnych typu TRY, ARS (dane FRED dla nich są problematyczne; testy odporności AUV w hiperinflacjach w iteracji v0.3)
- Brak codziennej publikacji "live" (to faza produkcyjna, długo po prototypie)
- Brak warstwy PRO (anomaly detection, gradient boosting)
- Brak interaktywnego dashboardu (statyczne wykresy PNG/HTML w outputs/)

## 11. Ryzyka i Zastrzeżenia

- **FRED API key wymagany.** Bezpłatny, ale wymaga rejestracji na https://fred.stlouisfed.org/docs/api/api_key.html — Ty będziesz musiał go założyć (system heliocentryczny ≠ bez uwierzytelnienia, oznacza tylko że dane są publiczne).
- **Yahoo Finance bywa zawodne** — dla BDI mogą być luki, fallback ręcznie pobrany CSV.
- **Optymalizacja QP może dać wagi "rogowe"** (np. wszystko na jednym aktywie, reszta na zero), jeśli funkcja celu jest zbyt restrykcyjna. Wtedy dodajemy regularyzację (Ridge na wagach), żeby wymusić dywersyfikację.
- **Empirycznie może się okazać, że minimalna korelacja z M2 to wciąż istotna korelacja** (np. 0.4 zamiast oczekiwanych 0). Jeśli tak — to ważny wynik sam w sobie, oznacza że żadna kombinacja realnych surowców nie jest naprawdę "wolna" od inflacji monetarnej. Zinterpretujemy.

---

## Następne Kroki (Po Akceptacji Planu)

1. Załóż konto FRED API key i wklej go do `.env` (instrukcję dam w README prototypu).
2. Ja tworzę strukturę katalogów, requirements.txt, `download.py` i `harmonize.py`. Commit do GitHuba.
3. Pobieramy dane, robimy EDA — Ty oglądasz pierwsze wykresy.
4. Optymalizacja i wyniki.
5. Iteracja: czego nie wystarczy, co dodać do v0.2 prototypu.

**Estymowany czas pracy:** kroki 2–4 do wykonania w ramach 1–2 sesji jeśli wszystko idzie gładko, więcej jeśli pojawią się problemy z danymi.

---

*Plan v0.1, gotowy do akceptacji lub pushbacku.*
