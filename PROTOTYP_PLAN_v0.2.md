# Plan Techniczny Prototypu Obliczeniowego AUV — v0.2

**Status:** Plan zatwierdzony przez autora; podstawa do implementacji.
**Zmiana względem v0.1:** rozszerzenie zakresu w trzech wymiarach na podstawie merytorycznych pushbacków autora — więcej walut, dane o podaży pieniądza dla każdej waluty, ilości i zapasy surowców jako dane wspomagające.

---

## 1. Cel i Zakres

Prototyp ma odpowiedzieć na trzy pytania:

1. Czy istnieje stabilna kombinacja wag $w_i$, dla której koszyk surowców i walut wykazuje minimalną korelację z agregatami M2/M3 *każdej* waluty bazowej?
2. Czy wynikowy szereg AUV(t) zachowuje się sensownie w okresach kryzysowych (1998, 2008, 2011, 2014, 2020, 2022)?
3. Czy wagi z QP są zbliżone do wag z analizy PCA (walidacja krzyżowa)?

**Świadomie wykluczone z prototypu v0.2** (do późniejszych iteracji): komponent pracy ludzkiej (kwartalna częstotliwość), warstwa PRO, integracja z Bitcoinem jako sygnał płynności, dashboard publiczny, automatyczna codzienna publikacja, anomaly detection.

## 2. Dane Wejściowe — Pełna Lista

### 2.1. Surowce — 10 pozycji cenowych

| Pozycja | Źródło | Symbol | Częstotliwość |
| --- | --- | --- | --- |
| Ropa Brent | FRED | `DCOILBRENTEU` | dzienna |
| Ropa WTI | FRED | `DCOILWTICO` | dzienna |
| Gaz ziemny Henry Hub | FRED | `DHHNGSP` | dzienna |
| Pszenica | FRED | `PWHEAMTUSDM` | miesięczna |
| Kukurydza | FRED | `PMAIZMTUSDM` | miesięczna |
| Miedź | FRED | `PCOPPUSDM` | miesięczna |
| Aluminium | FRED | `PALUMUSDM` | miesięczna |
| Ruda żelaza | FRED | `PIORECRUSDM` | miesięczna |
| Złoto (kontrola, nie do CORE) | FRED | `GOLDAMGBD228NLBM` | dzienna |
| Indeks BDI (Baltic Dry) | Yahoo | `^BDI` | dzienna |

### 2.2. Waluty — 18 walut (wszystkie wyrażone vs. USD jako jednostka odniesienia)

| Waluta | Źródło | Symbol / endpoint |
| --- | --- | --- |
| EUR | FRED | `DEXUSEU` |
| JPY | FRED | `DEXJPUS` |
| GBP | FRED | `DEXUSUK` |
| CHF | FRED | `DEXSZUS` |
| CNY | FRED | `DEXCHUS` |
| INR | FRED | `DEXINUS` |
| BRL | FRED | `DEXBZUS` |
| MXN | FRED | `DEXMXUS` |
| KRW | FRED | `DEXKOUS` |
| AUD | FRED | `DEXUSAL` |
| CAD | FRED | `DEXCAUS` |
| SGD | FRED | `DEXSIUS` |
| ZAR | FRED | `DEXSFUS` |
| TRY | FRED | `DEXTUUS` |
| PLN | NBP | `/api/exchangerates/rates/A/USD/{start}/{end}/` |
| CZK | ECB SDW | `EXR.D.CZK.EUR.SP00.A` + cross-rate via EURUSD |
| HUF | ECB SDW | `EXR.D.HUF.EUR.SP00.A` + cross-rate via EURUSD |
| SEK | FRED | `DEXSDUS` |

### 2.3. Podaż Pieniądza — M2/M3 per Kraj (NOWE w v0.2)

Logika: każda waluta otrzymuje swój własny "rodowód monetarny". To pozwoli modelowi rozróżnić, czy spadek wartości waluty wynika z ekspansji monetarnej (wewnętrzny dodruk), czy z zewnętrznych czynników gospodarczych (handel, kapitał).

| Kraj/blok | Wskaźnik | Źródło | Symbol | Częstotliwość |
| --- | --- | --- | --- | --- |
| USA | M2 | FRED | `M2SL` | miesięczna |
| Strefa euro | M3 | FRED | `MYAGM3EZM196N` | miesięczna |
| Wielka Brytania | M3 | FRED | `MABMM301GBM189S` | miesięczna |
| Japonia | M2 | FRED | `MABMM301JPM189S` | miesięczna |
| Chiny | M2 | FRED | `MYAGM2CNM189N` (lub PBOC) | miesięczna |
| Brazylia | M2 | FRED | `MYAGM2BRM189N` | miesięczna |
| Indie | M2/M3 | FRED / RBI | `MYAGM2INM189N` | miesięczna |
| Polska | M3 | NBP | statystyki monetarne | miesięczna |
| Czechy | M3 | ECB/CNB | dedykowana seria | miesięczna |
| Węgry | M3 | ECB/MNB | dedykowana seria | miesięczna |
| Pozostałe (KRW, AUD, CAD, CHF, MXN, ZAR, TRY, SEK, SGD) | M2 | FRED IFS series | różne | miesięczna |

W razie braków danych dla konkretnego kraju w prototypie pominiemy ten komponent — model zaadaptuje się, korzystając z dostępnych M2 jako reprezentantów regionalnych.

### 2.4. Ilości i Zapasy Surowców — Dane Wspomagające (NOWE w v0.2)

Wykorzystanie: w analizie eksploracyjnej do rozróżniania szoków podażowych od monetarnych. W przyszłej wersji formuły (v0.3 prototypu) mogą posłużyć do ważenia surowców według ich realnej wartości produkcji (cena × ilość) zamiast wag optymalizatora.

| Wskaźnik | Źródło | Symbol | Częstotliwość |
| --- | --- | --- | --- |
| Zapasy ropy USA | FRED | `WCESTUS1` | tygodniowa |
| Zapasy gazu USA | FRED | `WNGSUS1` | tygodniowa |
| Produkcja miedzi (świat) | USGS MCS | – | roczna |
| Zapasy miedzi LME | LME (free CSV) | – | dzienna |
| Globalna produkcja stali | World Steel Association | – | miesięczna |
| Globalna produkcja pszenicy | USDA WASDE | – | miesięczna (raport) |
| Globalna produkcja kukurydzy | USDA WASDE | – | miesięczna (raport) |
| Zapasy aluminium LME | LME | – | dzienna |

Dla części z tych wskaźników dane są dostępne bezpośrednio z FRED (np. krzywe rezerw USA, niektóre serie WASDE są mirrorowane), dla pozostałych konieczne będzie ręczne pobranie CSV-i (jeden raz, bez automatyzacji w v0.2 prototypu).

### 2.5. Okres

**1996-01-01 → 2025-12-31** (29 lat). Powód: pełne pokrycie danych FX dla wszystkich par, post-Mexican-crisis stabilizacja, brakujące hiperinflacje w gospodarkach G20.

## 3. Pipeline Danych

```
[FRED API] ──┐
[NBP API]  ──┤
[ECB SDW]  ──┼─→ [src/sources/*] ─→ data/raw/*.csv (cache)
[Yahoo]    ──┤
[USGS/USDA CSV] ┘
                                        │
                                        v
                              [src/harmonize.py]
                                        │
                                        ├── ujednolicenie częstotliwości (dziennej dla daily, miesięcznej dla mixed)
                                        ├── forward-fill dla weekendów i świąt
                                        ├── obcięcie do wspólnego okresu (1996–2025)
                                        ├── interpolacja kwartalnych zapasów do miesięcznych (cubic spline)
                                        │
                                        v
                              data/processed/{daily.parquet, monthly.parquet}
                                        │
                                        v
                              [notebooks/01_eda.ipynb] — wybór t_0, wizualizacja reżimów
                                        │
                                        v
                              [src/optimize.py] — QP z partial regression + PCA
                                        │
                                        v
                              outputs/{weights.json, auv_series.csv, figures/*.png}
```

## 4. Analiza Eksploracyjna (EDA)

Cel: wybrać $t_0$ i zidentyfikować strukturalne załamania reżimu.

Plan: log-skalowane wykresy szeregów, znormalizowane do 1996 = 1; macierze korelacji rollingowe (5-letnie okna); test Bai-Perron dla wykrywania momentów strukturalnych załamań; wizualne porównanie M2 z najbliższymi mu surowcami (czy hipoteza "anty-M2" wytrzymuje wstępną kontrolę); test wrażliwości na trzech kandydatach $t_0$ (1996–1999, 2003–2006, 2015–2019).

## 5. Optymalizacja — Zmieniona Matematyka (NOWE w v0.2)

Z dodaniem M2 jako *features* (a nie tylko targetu), formuła z v0.1 — "minimalizuj korelację koszyka z M2" — jest niewystarczająca. Stosujemy dwuetapowe podejście Frisch-Waugh-Lovell:

**Etap 1 (ortogonalizacja):** dla każdego składnika $p_i(t)$ obliczamy jego komponent ortogonalny do agregatu M2:
$$\tilde{p}_i(t) = p_i(t) - \beta_i \cdot M2(t)$$
gdzie $\beta_i$ to współczynnik z regresji $\log p_i$ na $\log M2$. Składnik $\tilde{p}_i$ to "realna" część ceny — to, co pozostaje po odjęciu wkładu monetarnego.

**Etap 2 (QP na komponentach realnych):**
$$\min_{w} \; \mathrm{Var}\!\left( \sum_i w_i \tilde{p}_i \right)$$
przy ograniczeniach $w_i \geq 0$ i $\sum w_i = 1$.

Intuicja: szukamy koszyka *najbardziej stabilnego po oczyszczeniu z M2*. Dla każdej waluty osobno odejmujemy lokalny M2 (innymi słowy — różne β_i dla różnych regionów monetarnych).

**Walidacja krzyżowa PCA:** niezależnie obliczamy PCA na samych komponentach realnych $\tilde{p}_i$, pierwsza składowa powinna odpowiadać "wspólnemu cyklowi gospodarczemu" (a nie inflacji, którą już odjęliśmy). Wagi proporcjonalne do drugiej i dalszych składowych — porównanie z wagami QP.

## 6. Wyniki — Co Pokazujemy

- Tabela wag CORE (15–18 składników) z QP i PCA obok siebie
- Wykres AUV(t) za 1996–2025, nakładający się z indeksami CPI-USA, CPI-EU, ceną złota (wszystkie w log)
- Wykres "AUV / pojedyncza waluta" dla USD, EUR, PLN, JPY, BRL, TRY — pokazujący realną deprecjację dla różnych reżimów monetarnych
- Tabela β_i dla każdego surowca względem każdego z dziewięciu agregatów M2 — *sama w sobie* ciekawa informacja o tym, do której waluty który surowiec jest najbliższy
- Tabela "wartość 1 jednostki w 1996 vs 2025" dla USD, EUR, PLN, BRL, mieszkania (proxy: stal+cement+drewno), ropy, pszenicy
- Test wrażliwości: jak zmienia się AUV przy różnych wyborach $t_0$

## 7. Struktura Kodu w Repozytorium

```
prototyp/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   ├── raw/              # gitignored — cache pobranych CSV
│   └── processed/        # gitignored — aligned.parquet
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_optimization.ipynb
│   └── 03_results.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py         # centralny rejestr serii danych
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── fred.py
│   │   ├── nbp.py
│   │   ├── ecb.py
│   │   └── yahoo.py
│   ├── download.py       # orkiestracja pobierania
│   ├── harmonize.py      # alignment częstotliwości
│   ├── optimize.py       # QP + FWL + PCA
│   └── viz.py            # wykresy
└── outputs/
    ├── weights.json
    ├── auv_series.csv
    └── figures/
```

## 8. Zależności (requirements.txt)

```
pandas>=2.0,<3.0
numpy>=1.24,<2.0
fredapi>=0.5
yfinance>=0.2.40
requests>=2.31
cvxpy>=1.4
scikit-learn>=1.3
ruptures>=1.1            # Bai-Perron
statsmodels>=0.14        # FWL, regresja
matplotlib>=3.7
plotly>=5.17
jupyter>=1.0
pyarrow>=14.0
python-dotenv>=1.0
```

## 9. Wymagania od Autora (Setup po Stronie Macu)

1. **FRED API key** — bezpłatne konto na https://fred.stlouisfed.org/docs/api/api_key.html, klucz wstawić do `prototyp/.env`.
2. **Python 3.10+** — zalecane virtualenv (`python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`).
3. **Klucz NBP i ECB** — *nie są wymagane* (oba API są publiczne bez uwierzytelniania).

## 10. Świadome Ograniczenia v0.2 Prototypu

- Bez komponentu pracy ludzkiej (kwartalny, do v0.3).
- Bez energii elektrycznej spot (skomplikowane dane regionalne, do v0.3).
- Bez wysokoinflacyjnych "ekstremów" jak ARS (dane FRED są tutaj problematyczne — duże luki).
- Bez Bitcoina (rezerwowane dla warstwy PRO).
- Bez codziennej publikacji "live" — wyniki to statyczne pliki w `outputs/`.

## 11. Ryzyka

- **Niektóre serie M2 z FRED mogą mieć luki** dla mniejszych krajów. W takim wypadku model zaadaptuje się, używając regionalnego agregatu zamiast krajowego (np. M3 strefy euro jako proxy dla wszystkich walut UE).
- **Ortogonalizacja FWL może być niestabilna** dla par, gdzie $p_i$ i $M2$ są silnie kointegrowane (np. ropa i M2 USA z lat 70.). Wtedy współczynnik $\beta_i$ staje się wrażliwy na okres estymacji. Mitygacja: estymacja w oknach kroczących i uśrednianie.
- **Empirycznie może się okazać, że minimum wariancji koszyka po FWL to wciąż istotna zmienność** (np. 30% rocznie). To byłby też ważny wynik — oznaczałby, że "realna" wartość gospodarki jest sama w sobie zmienna i pojęcie absolutnego miernika ma niesuwerenny charakter. Zinterpretujemy uczciwie.

---

*Plan v0.2 — gotowy do implementacji.*
