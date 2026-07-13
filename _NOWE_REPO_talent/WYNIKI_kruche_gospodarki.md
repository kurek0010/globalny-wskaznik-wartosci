# Talent w kruchych gospodarkach — Polska (ilościowo), Niemcy i Argentyna (epizody)

**Data:** 2026-07-04
**Kod:** `prototyp/src/regret_poland.py`. Nazewnictwo przyjęte: jednostka **Talent (TLN)** = √(CPI × płaca); wariant dla finansów bezodsetkowych: **Qist**. Metryka: **żal / regret** (dwustronny, jak w `WYNIKI_test_stulecia_USA.md`).

---

## 1. Polska 1989–2024 (transformacja, dezinflacja, deflacja 2015, szok 2022)

Dane: CPI — FRED/OECD (POLCPIALLMINMEI, od 1989); płace — przeciętne wynagrodzenie GUS/ZUS (tablice wpisane z wiedzy, **do weryfikacji u źródła**; przełom netto→brutto 1999 połączony łańcuchowo wzrostem ~+11,1% na bazie porównywalnej — wpływ na wyniki <1 p.p.).

| Kandydat | % okien zero-żalu | Mediana | p95 | Najgorszy przypadek |
|---|---|---|---|---|
| **Talent** | **98%** | **0,0%** | **0,0%** | **10,4%** (wierzyciel, 1989→1994) |
| CPI | 98% | 0,0% | 0,0% | 21,9% (dłużnik, 1989→1994) |
| płaca | 98% | 0,0% | 0,0% | 21,9% (wierzyciel, 1989→1994) |
| nominal | 4% | 32,6% | 1 589% | **10 813%** (wierzyciel, 1989→2019) |

Odczyt:

- **Talent przeszedł transformację ustrojową z maksymalnym żalem 10,4%** — połowa 18-procentowego realnego spadku płac 1989–1994. Indeksacja samym CPI zdusiłaby dłużnika o 22% względem pensji; sama płaca — okradła wierzyciela o 22% siły nabywczej. Talent rozłożył szok po połowie.
- **Nominal w Polsce to nie strata, to unicestwienie:** pożyczka z 1989 oddana w 2019 nominalnie = żal 10 813% (wierzyciel odzyskał <1% wartości). Nawet pożyczka 2019→2024: wierzyciel −40% względem płac, −30% względem cen. Każda kasa koleżeńska w Polsce działająca nominalnie przez ostatnie 35 lat systematycznie transferowała majątek od pożyczających do pożyczkobiorców.
- Epizod 2022 (pożyczka 2019→2024): Talent ×1,55 → dłużnik −7% względem płac, wierzyciel +8% względem cen. **Obie strony wygrały jednocześnie** (płace nominalnie wyprzedziły inflację w pełnym oknie).

**Lekcja operacyjna z 1990 r. (poza tabelą):** inflacja m/m w styczniu 1990 wyniosła ~79,6%. Jednostka publikowana z miesięcznym opóźnieniem traci w takim miesiącu do ~44% realnie. Wniosek projektowy w §3.

## 2. Niemcy 1913–1923 — granica stosowalności (epizod, liczby z literatury)

Indeks cen hurtowych (1913=1): styczeń 1920 ≈ 12,6; styczeń 1923 ≈ 2 785; listopad 1923 ≈ 725 miliardów. Inflacja października 1923: ~29 500% **miesięcznie** (~20–25% dziennie).

- **Matematycznie Talent przeżywa** (obie nogi eksplodują razem, iloraz i średnia geometryczna pozostają skończone; płace w 1923 renegocjowano co tydzień, potem codziennie — realnie ~50–70% poziomu 1913 dla wykwalifikowanych).
- **Operacyjnie umiera każdy indeks:** przy 20% dziennie publikacja opóźniona o jeden dzień oddaje wierzycielowi o 1/6 mniej. Niemcy rozwiązali to dopiero kotwicą realną (Roggenmark — marka żytnia, potem Rentenmark), nie lepszym indeksem.
- To wyznacza **uczciwą granicę produktu**: Talent jest jednostką dla inflacji do rzędu kilkudziesięciu % rocznie. Powyżej progu Cagana (50% m/m) żadna jednostka indeksowa nie działa — działa tylko natychmiastowa wymiana na dobra/waluty obce.

## 3. Argentyna — trzy lekcje, każda projektowa (epizod, liczby przybliżone)

**(a) 2002 — korytarz rozdarty w jeden rok.** CPI +41%, płace nominalne +7% → realny spadek płac ~24% w 12 miesięcy. Talent = √(1,41×1,07) → +22,8%: dłużnik +14,8% względem płac, wierzyciel −12,9% względem cen. Bolesne, ale symetryczne — i wciąż o połowę lepsze dla każdej strony niż czysta indeksacja drugą nogą.

**(b) 2007–2015 — INDEC, czyli zmanipulowane źródło.** Rząd Kirchnerów fałszował oficjalny CPI: ~10%/rok oficjalnie vs ~25%/rok według niezależnych pomiarów (PriceStats/MIT Billion Prices, indeksy prowincji, „CPI Kongresu"). Po 9 latach: oficjalnie ×2,2, realnie ×~7. **Talent liczony z jednego oficjalnego źródła okradłby wierzycieli z ~70% wartości.** To jest rozstrzygający argument za regułą, którą przyjęliśmy w warstwie zaufania: **każda noga = mediana ≥3 niezależnych źródeł + tripwire** (rozjazd źródeł powyżej progu → automatyczne wykluczenie odstającego, zapisane z góry w kodzie). Manipulacja INDEC była wykrywalna natychmiast — PriceStats pokazywał rozjazd od pierwszego roku.

**(c) 2016–2021 — UVA, czyli naturalny eksperyment jednonożnej indeksacji.** Argentyńskie kredyty hipoteczne UVA (indeksowane samym CPI, model chilijski) po skoku inflacji 2018–19 (CPI ~×2,3 w dwa lata przy płacach ~×1,8) podniosły obciążenie kredytobiorców o ~25% względem pensji → protesty → rząd **zamroził raty dekretem** (2019–2021). Talent z nogą płacową dałby w tym samym epizodzie wzrost obciążenia o ~11% zamiast ~25% — być może poniżej progu wybuchu politycznego. Lekcja podwójna: (1) noga płacowa to nie ozdoba, to polityczny bezpiecznik produktu; (2) umowa musi z góry zawierać regułę kryzysową (odroczenie/wydłużenie zamiast zamrożenia dekretem), bo inaczej państwo napisze ją za nas.

## 4. Wnioski projektowe — trzy reguły do wpisania w kod jednostki

1. **Reguła częstotliwości (z Polski 1990 i Niemiec 1923):** publikacja dzienna interpolowana (jak UF); gdy 3-miesięczna średnia inflacji m/m przekroczy próg (np. 15%), automatyczne skrócenie okna wygładzania i interpolacja kursowa; powyżej progu Cagana (50% m/m) — jednostka przechodzi w tryb awaryjny na z góry zadeklarowany twardy koszyk (mediana 3 stabilnych walut), aż inflacja wróci poniżej progu przez 6 miesięcy. Wszystko deterministyczne, ogłoszone z góry.
2. **Reguła mediany źródeł (z Argentyny b):** minimum 3 niezależne źródła na nogę; mediana; tripwire rozjazdu. Bez tego jednostka jest zakładnikiem najsłabszego urzędu statystycznego.
3. **Reguła kryzysowa w umowie (z Argentyny c):** kontrakt w Talentach zawiera z góry mechanizm ulgi (wydłużenie zamiast redukcji, cap rocznego wzrostu raty z kapitalizacją reszty), żeby polityka nie musiała łamać jednostki dekretem.

## 5. Stan wiedzy po trzech testach

| Test | Najgorszy żal Talenta | Warunki |
|---|---|---|
| USA 1929–2025 | 19,7% (CPI×PKB/os.; Wielki Kryzys) / **6,1%** (CPI×płaca, od 1939) | kraj stabilny instytucjonalnie |
| Polska 1989–2024 | **10,4%** (transformacja ustrojowa) | zmiana ustroju, inflacja 586%/rok |
| Niemcy 1923 | jednostka indeksowa nie działa | hiperinflacja > próg Cagana |
| Argentyna | ~13–15%/rok szoku (2002); manipulacja źródła = do −70% bez mediany źródeł | kryzys walutowy; wrogie państwo |

Pasmo „w przybliżeniu ta sama wartość po latach" jest więc policzalne i zaskakująco wąskie wszędzie tam, gdzie istnieje wiarygodny pomiar cen i płac — a tam, gdzie nie istnieje, żadna formuła go nie zastąpi i trzeba to wpisać w granice produktu.

**Do weryfikacji u źródeł:** tablica płac GUS/ZUS 1989–2024; liczby niemieckie (Bresciani-Turroni/Cagan); argentyńskie (INDEC vs PriceStats, dynamika RIPTE 2018–19, dekrety UVA). Rzędy wielkości pewne, dokładne wartości do audytu przed publikacją.
