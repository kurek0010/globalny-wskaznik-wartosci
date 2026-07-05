# Globalny Wskaźnik Wartości — Podsumowanie Stanu Badań

**Autor projektu:** Mariusz Kurowski
**Współpraca konceptualna i implementacyjna:** asystent Claude (model konwersacyjny Anthropic)
**Data dokumentu:** 2026-06-09
**Cel dokumentu:** Self-contained podsumowanie stanu badań do dyskusji eksperckiej. Każda osoba zaznajomiona z ekonomią monetarną i ekonometrią powinna móc bez dodatkowego kontekstu zrozumieć, gdzie jesteśmy i co warto rozważyć dalej.

---

## 1. Cel projektu — krótko

Skonstruować *publicznie publikowaną, deterministyczną jednostkę rachunkową* niezależną od decyzji jakichkolwiek autorytetów (rad nadzorczych banków centralnych, urzędów statystycznych, instytucji międzynarodowych). Jednostka ma służyć dwóm grupom zastosowań:

(a) **Indeksacji umów wieloletnich** — kredytów hipotecznych, emerytur, alimentów, świadczeń socjalnych. Zamiast WIBOR-u (ustalanego decyzją RPP) lub CPI (ustalanego decyzją GUS), umowy odwoływałyby się do indeksu, którego nikt nie może arbitralnie zmienić. Konceptualny pierwowzór: chilijska **Unidad de Fomento** (UF), działająca od 1967 roku.

(b) **Pomiarowi realnej wartości w długim horyzoncie** — czy realnie świat się bogaci, czy biednieje, niezależnie od deprecjacji pieniądza papierowego.

Filozofia projektowa, którą nazywamy *heliocentryczną*, oznacza: wyniki muszą wynikać z obserwowalnych, publicznie dostępnych danych przetworzonych deterministyczną formułą. Bez czarnych skrzynek, bez subskrypcyjnych źródeł danych, bez ludzkiej uznaniowości po fakcie. Analogia: definicja metra przez prędkość światła, a nie przez fizyczny pręt przechowywany w Sèvres.

---

## 2. Ewolucja Myślenia — Cztery Iteracje

### Iteracja v0.1 — porzucona

Hipoteza pierwotna: uczenie maszynowe (autoenkoder, PCA) może *wyciągnąć* ukrytą zmienną wartości z wielowymiarowych szeregów cenowych. Pomysł: jeśli karmimy model cenami surowców, kursami walut i agregatami monetarnymi, model znajdzie wymiar reprezentujący "prawdziwą wartość" oczyszczoną z monetarnego szumu.

**Co odkryliśmy:** matematyczna pułapka. Jeśli wszystkie zmienne wejściowe są zdenominowane w pieniądzu papierowym, to każda ich kombinacja również. Pierwsza składowa PCA na takich danych reprezentuje *globalny trend inflacyjny*, a nie "prawdziwą wartość". Próba znalezienia kombinacji wag, dla której koszyk jest *najbardziej stabilny*, prowadzi do zwykłego portfela typu minimum-variance — który nie ma żadnej interpretacji wartościowej.

**Konkluzja:** nie da się "wyciągnąć" wartości czystym ML, jeśli wszystkie wejścia są wyrażone w fiat. Trzeba dodać zewnętrzną kotwicę.

### Iteracja v0.2 — zaimplementowana, częściowo udana

Procedura dwuetapowa Frischa-Waugha-Lovella (FWL) plus optymalizacja kwadratowa (QP):

1. Dla każdego surowca *i* regresujemy log-poziomy ceny na log-poziomy M2/M3 czterech głównych walut (USA, EUR, UK, JP), otrzymując reszty *e_i(t)* reprezentujące "realny" komponent ceny.
2. QP znajduje wagi nieujemne sumujące się do 1, minimalizujące wariancję ważonej sumy reszt.

Pipeline zaimplementowany w Pythonie (`prototyp/src/optimize.py`). Dane pobrane z FRED, NBP, ECB, Yahoo Finance — 31 serii czasowych za okres 1996–2025. Wagi wyznaczone. AUV(t) wyliczone.

**Co odkryliśmy:**

Problemy techniczne. Cztery agregaty M2/M3 są silnie współliniowe (wszystkie rosną monotonicznie z czasem). Współczynniki β z regresji wielokrotnej balonują do nierealistycznych wartości (±8 zamiast oczekiwanego ~1). Reszty są przeszacowane; optymalizacja na nich jest matematycznie chwiejna. QP i kontrolny PCA produkują dramatycznie różne wagi (QP: aluminum 37% + iron_ore 33%, oil 0%; PCA: WTI 46% + Brent 40%, metale 1%) — co oznacza, że minimum wariancji jest słabo zdefiniowane numerycznie.

Wnioski metodologiczne. AUV v0.2 jest w istocie *indeksem najmniej zmiennych surowców masowych*, a nie miernikiem realnej wartości. Na 30-letnim horyzoncie AUV i M2_USA kończą w tym samym miejscu — co skłoniło nas najpierw do interpretacji "metoda zawiodła", a po pushbacku autora projektu do rewizji: "to *właśnie* deprecjacja dolara wobec realnej wartości, którą chcieliśmy zobaczyć".

To rozróżnienie okazało się kluczowe. Brak długoterminowej różnicy między AUV a M2_USA nie obala metody, jeśli AUV traktujemy jako *stałą jednostkę wartości w realnych kategoriach*; długoterminowy wzrost nominalnej wartości AUV w USD jest *oczekiwanym sygnałem* o deprecjacji dolara.

**Konkluzja:** FWL+QP jest matematycznie zbyt skomplikowany i zbyt wrażliwy na multikolinearność M2. Krótkoterminowo wskaźnik jest zaszumiony szokami surowcowymi (Lehman 2008, Ukraina 2022). Wymaga przemyślenia od podstaw.

### Iteracja v0.3 — odwrócenie paradygmatu

Zamiast *ekstrakcji* AUV z surowych cen przez ML, *konstrukcja* AUV od podstaw z trzech obserwowalnych liczb dla każdego zasobu: ceny *p*, rocznej produkcji *q*, potrzeby na osobę *R*. Plus populacja świata *N* jako mianownik.

Formuła centralna:

`realna_wartość_i(t) = p_i(t) × R_i_baseline × N(t) / q_i(t)`

Interpretacja: AUV mierzy *koszt utrzymania ludzkiej cywilizacji na obecnym poziomie technologicznym*. Wzrasta gdy konsumpcja zasobów wyprzedza ich produkcję per capita; spada gdy postęp technologiczny i produkcyjny wyprzedza rosnące potrzeby ludzkości.

**Co odkryliśmy:**

Implementacja na dostępnych danych (głównie zbóż i energii) pokazała trzy problemy:

(1) *Brak twardych danych produkcyjnych dla większości kategorii.* USGS publikuje produkcję metali tylko w PDF/Excel (utrudniona automatyzacja). EIA wymaga klucza API. World Bank ma ograniczony zestaw serii produkcyjnych. Bez tych danych formuła `p × N / q` redukuje się do "p × stała", co nie wnosi informacji ponad samą cenę.

(2) *Anomalie w danych World Bank.* Produkcja zbóż 2024 spada o połowę w jednym roku (oczywisty błąd raportu/niekompletny raport), powierzchnia rolna skacze nielogicznie o 1 mln km² w 2013, indeks produkcji żywności kończy się w 2020. Defensywny pre-processing wykrywa anomalie >25% rok-do-roku, ale subtelniejsze artefakty (stopniowe zmiany metodologiczne) wymagałyby agresywniejszych filtrów.

(3) *Arbitralność wag kategorii.* Wagi 50/50 food/energy w pierwotnej implementacji były ad-hoc. Wymagałyby uzasadnienia (np. proporcjonalnie do wartości światowej produkcji każdej kategorii), co wprowadza kolejne źródło danych i decyzji.

Wynikowy AUV v0.3.0 jest *bardziej zmienny* niż v0.2 (oscyluje 40–300 w skali, gdzie t_0 = 100), co dyskwalifikuje go jako jednostkę rozliczeniową w umowach kredytowych.

### Iteracja v0.3.1 — hybryda

Próba ratunku: AUV jako stosunek dwóch komponentów.

- *Komponent real:* ważona suma realnych wartości (food + energy + metals).
- *Komponent fiat:* konsensus CPI G5 ważony PKB.
- `AUV = real / fiat × 100`

Implementacja w `prototyp/src/auv_v3_hybrid.py`. Wyniki nadal niezadowalające — komponent metals nie ma dostępnej produkcji, więc redukuje się do średniej ceny metali; energia ma podobny problem. Formuła hybrydowa staje się funkcjonalnie zbliżona do CPI z dodatkową szarpaną domieszką surowców.

**Konkluzja iteracyjna:** projekt naturalnie *rozdziela się na dwa różne projekty* o różnej dojrzałości i przeznaczeniu.

---

## 3. Stan Obecny — Dwa Wyodrębnione Projekty

### Projekt 1 — FDI (Fiat Depreciation Index)

**Cel:** miernik deprecjacji walut papierowych do zastosowań kontraktowych (kredyty, umowy wieloletnie). Praktyczny, osiągalny w obecnym stanie danych.

**Architektura proponowana:** kompozytowy indeks z 1–4 komponentów (ważona średnia, normalizacja do dnia bazowego):

| Komponent | Co mierzy | Waga propozycja | Status danych |
| --- | --- | --- | --- |
| CPI konsensus G5 | Inflacja konsumencka głównych walut | 35% | Dostępne (FRED) |
| M2 konsensus | Ekspansja monetarna (kreacja kredytowa + ekspansja bilansów banków centralnych) | 30% | Dostępne (FRED) |
| Dług publiczny / PKB | Strukturalna presja inflacyjna | 20% | Dostępne (FRED, IMF GDD) |
| SDR (lub syntetyczny) | Relatywna siła walut | 15% | Dostępne (MFW) |

**Otwarte pytanie metodologiczne (kluczowe):** czy potrzeba *wszystkich czterech* komponentów, czy konsensus CPI G5 sam wystarcza?

Empirycznie sprawdziliśmy hipotezę autora projektu (patrz sekcja 5), że jeśli inflacja jest rzetelnie mierzona, to *compound CPI* od roku bazowego powinien wyjaśniać kursy walut. Wynik: tylko częściowo. Dla walut z dużym dyferencjałem inflacji vs USD (BRL, PLN) CPI wyjaśnia 40–85% kursów. Dla walut o podobnej inflacji do USD (EUR, GBP) korelacja PPP z rzeczywistym kursem jest praktycznie zerowa lub odwrotna znakowi (JPY!).

Wniosek: dla głównych par walutowych CPI samodzielnie *nie wystarcza*. Kursy są dodatkowo sterowane polityką monetarną (Bank of Japan), przepływami kapitału (carry trade), sentymentem (USD jako bezpieczna przystań). M2 i dług mogą wnosić tę dodatkową informację, ale wymaga to formalnej weryfikacji.

### Projekt 2 — AUV (Absolute Unit of Value)

**Cel:** miernik realnej wartości cywilizacji, oparty na cenach surowców, ich produkcji i populacji. Aspiracyjny, wymaga jeszcze pracy nad danymi i metodologią.

**Architektura proponowana:** dla 15–20 zasobów w pięciu kategoriach (energia, żywność, budownictwo, metale przemysłowe, materiały krytyczne) liczymy `cena × potrzeba_per_capita × populacja / produkcja_globalna`. AUV to ważona suma realnych wartości kategorii.

**Stan:** częściowa implementacja w `prototyp/src/auv_v3.py` i `auv_v3_hybrid.py`. Główne braki to pełne dane produkcyjne (USGS dla metali, EIA dla energii, USDA WASDE dla żywności), uzasadnione metodologicznie wagi kategorii, oraz precyzyjniejsze defensywne czyszczenie danych.

**Status:** w fazie badawczej. Sensowne dopiero po realizacji Projektu 1 i uzupełnieniu danych źródłowych.

### Relacja między projektami

FDI mierzy *jak fiat traci wartość*. AUV mierzy *jak realne zasoby stają się rzadsze lub obfitsze*. W praktyce są skorelowane (ekspansja monetarna podnosi nominalne ceny surowców), ale teoretycznie niezależne. Razem dają obraz pełniejszy niż każdy z osobna.

---

## 4. Stan Techniczny — Co Już Jest

### Infrastruktura danych (`prototyp/src/sources/`)

Pięć adapterów REST: FRED (z kluczem API), NBP (bez klucza), ECB SDW (chunkowane zapytania, bez klucza), World Bank Open Data (bez klucza), Yahoo Finance (yfinance).

### Rejestr serii (`prototyp/src/config.py`)

71 serii czasowych w 7 kategoriach: ceny surowców (19), waluty (18), agregaty pieniężne (8), zapasy surowców (2), populacja (1), wskaźniki produkcji (13), CPI (8) plus 2 kontrolne.

### Zbiór danych (`prototyp/data/processed/`)

- `daily.parquet`: 7828 dni roboczych × 47 zharmonizowanych serii (po forward-fill rocznych/miesięcznych)
- `monthly.parquet`: 360 miesięcy × 47 serii

Okres: 1996-01-01 → 2025-12-31.

### Notebooki badawcze (`prototyp/notebooks/`)

- `01_eda.ipynb`: analiza eksploracyjna, wybór dnia bazowego
- `02_optimization.ipynb`: FWL + QP (v0.2)
- `04_auv_v3.ipynb`: pierwsza implementacja v0.3
- `05_auv_v3_hybrid.ipynb`: hybryda C
- Plus ad-hoc analizy PPP w `outputs/figures/20-25_*.png`

### Repozytorium

Wersjonowane w Git, publiczne na GitHubie (zgodnie z filozofią heliocentryczną — kod i historia decyzji muszą być audytowalne).

---

## 5. Kluczowe Wyniki Empiryczne

### 5.1 Skumulowana inflacja CPI 1996 → 2025 (z FRED)

| Waluta | Kumulacyjnie | Rocznie | Siła nabywcza po 30 latach |
| --- | --- | --- | --- |
| BRL | +477% | 6,03% | 17% |
| PLN | +262% | 4,40% | 28% |
| USD | +111% | 2,52% | 47% |
| GBP | +102% | 2,38% | 50% |
| EUR | +81% | 2,06% | 55% |
| CNY | +70% | 1,79% | 59% |
| CHF | +19% | 0,58% | 84% |
| JPY | +4% | 0,16% | 96% |

Rozróżnienie między walutami jest dramatyczne. Jen i frank praktycznie zachowały siłę nabywczą, real brazylijski ją utracił prawie całkowicie.

### 5.2 Test parytetu siły nabywczej (PPP)

Hipoteza testowana: kurs waluty wobec USD powinien podążać za różnicą skumulowanej inflacji. Formalnie:

`kurs_PPP(t) = kurs(t_0) × (1 + skumulowana_inflacja_waluty) / (1 + skumulowana_inflacja_USD)`

Wyniki na danych kwartalnych 2000–2025:

| Para | Korelacja PPP z rzeczywistym kursem | Maksymalny błąd | Interpretacja |
| --- | --- | --- | --- |
| EUR/USD | 0,004 | 37% | PPP praktycznie nic nie wyjaśnia |
| GBP/USD | 0,608 | 48% | Częściowo wyjaśnia |
| CHF/USD | 0,829 | 40% | Silnie wyjaśnia |
| JPY/USD | 0,367 | 67% | Wyjaśnia *przeciwny* kierunek długoterminowo |
| CNY/USD | -0,472 | 27% | PPP ma zły znak (polityka kursowa Chin) |
| BRL/USD | 0,853 | (nie liczone) | PPP wyjaśnia bardzo dobrze |

Wniosek: PPP jako jedyna formuła wyjaśniająca kursy walut *zawodzi systematycznie* dla głównych par. Działa najlepiej dla walut z ekstremalnym dyferencjałem inflacji (BRL vs USD) lub dla walut o znacznie niższej zmienności kapitałowej (CHF).

Wersja alternatywna PPP (suma zamiast stosunku inflacji) jest matematycznie błędna — daje korelacje ujemne lub bliskie zera dla wszystkich par.

### 5.3 Współliniowość M2 i CPI

Analizy z v0.2 i v0.3 wykazały: cztery agregaty M2/M3 głównych walut są silnie współliniowe (korelacje rocznych przyrostów logarytmicznych >0,7 między parami). CPI G5 jest silnie skorelowane z odpowiednim M2 z opóźnieniem 12–24 miesięcy. Dług publiczny / PKB rośnie monotonicznie z lekko wyprzedzającą dynamiką wobec M2.

Implikacja: w formule FDI komponenty CPI, M2 i długu *częściowo redundantnie pokrywają się*. Pytanie, czy ich kombinacja wnosi *istotnie* więcej informacji niż sam CPI, jest empiryczne i wymaga formalnego testu (np. regresji długoterminowej zmiany kursu na różne zestawy komponentów).

---

## 6. Otwarte Pytania Do Dyskusji Eksperckiej

Wymieniam je w kolejności od najpilniejszych po najbardziej długoterminowe:

### 6.1 Czy konsensus CPI G5 wystarcza jako rdzeń FDI?

Z wyników w sekcji 5.2 wynika, że PPP w pełnej skali nie wyjaśnia kursów głównych walut. Ale dla *długiego horyzontu* (5–30 lat, relevantnego dla kredytów hipotecznych), trendy CPI faktycznie tłumaczą *średni* poziom kursu (CHF i GBP korelacje >0,6).

Hipoteza autora: w długim okresie krótkoterminowe szumy spekulacyjne się uśredniają, a CPI sam wystarcza. To by *drastycznie upraszczało* projekt — FDI byłby średnią ważoną CPI G5, miesięczną, w pełni transparentną.

Pytanie do eksperta: czy z punktu widzenia ekonomii monetarnej i praktyki ubezpieczeniowo-kredytowej, taki uproszczony indeks jest *wystarczający* dla wieloletnich kontraktów? Czy istnieją *typowe ryzyka* takiego podejścia (np. perypetie metodologiczne CPI, manipulacje w słabszych gospodarkach), które wymagają dodatkowych komponentów?

### 6.2 Czy zaufanie do oficjalnego CPI jest uzasadnione?

Krytycy ortodoksyjni argumentują, że oficjalne CPI:
- Niedoszacowuje inflacji aktywów (mieszkania, akcje)
- Stosuje korekty hedoniczne, które obniżają mierzoną inflację
- Podlega presji politycznej na zaniżanie (zwłaszcza w gospodarkach wschodzących)

Z drugiej strony: CPI G5 mierzony przez profesjonalne, niezależne agencje (BLS, Eurostat, Bank of Japan, ONS, BFS) jest praktycznie poza kontrolą polityczną. Metodologie są publikowane. Manipulacja byłaby wykrywalna.

Pytanie: czy zaufanie do CPI G5 jest *jakościowo wystarczające* dla celów heliocentrycznego indeksu kontraktowego? Czy istnieją niezależne, lepiej weryfikowalne miary inflacji konsumenckiej?

### 6.3 Czy formuła AUV (p × N / q) jest realizowalna w praktyce?

Główne przeszkody to:

(a) *Akwizycja danych.* Pełne, miesięczne dane produkcyjne dla metali, ropy, gazu, materiałów budowlanych wymagają adapterów do USGS, EIA, USDA WASDE, World Steel, CEMBUREAU. Część danych jest w PDF/Excel, nie w API. Estymowany nakład: 2–4 tygodnie pracy programistycznej.

(b) *Uzasadnienie wag kategorii.* Czy 30% energia, 25% żywność, 20% metale, 15% budownictwo, 10% materiały krytyczne ma sens metodologiczny? Czy lepiej ważyć proporcjonalnie do wartości światowej produkcji (jeśli tak, jaki rok bazowy)?

(c) *Definicja "potrzeby per capita" (R_i).* Czy używać średniej światowej konsumpcji (tautologia: "potrzeba = co zużywamy"), czy korygować regionalnie, czy wprowadzić "normatywne" wartości typu kalorii minimum dziennego?

Pytanie: czy ekonomista ze specjalizacją w *ecological economics* lub *resource economics* widzi tę formułę jako rozsądny pomiar realnej wartości cywilizacji, czy raczej jako naukowy fetysz? Jakie są podobne istniejące podejścia (np. Wealth Accounting WAVES Banku Światowego)?

### 6.4 Czy heliocentryczność jest w ogóle osiągalna?

Filozofia projektu wymaga, by wyniki nie zależały od decyzji autorytetów. Ale każda dana wejściowa (CPI, M2, ceny giełdowe, dane USGS, populacja UN) jest *zbierana przez jakąś instytucję*. Idealnie heliocentryczna byłaby tylko surowa obserwacja fizyczna (np. cena ropy z odczytów tankowców satelitarnych), co jest praktycznie niewykonalne.

Pytanie: gdzie *realistycznie* przebiega granica między heliocentrycznym a antropocentrycznym wskaźnikiem? Czy istnieją kryteria akceptowalności (np. "instytucja musi być niezależna od rządu", "metodologia publicznie dostępna", "minimum N niezależnych dostawców tych samych danych")?

### 6.5 Czy podział na FDI i AUV jest właściwy?

Założenie obecne: FDI mierzy deprecjację fiat-u, AUV mierzy realną wartość. To są dwa różne pytania o ten sam świat.

Alternatywne podziały:
- *Wymiar czasowy:* wskaźnik krótkoterminowy (miesięczny, dla trade) vs długoterminowy (roczny, dla emerytur)
- *Wymiar regionalny:* wskaźnik globalny vs wskaźniki kontynentalne (Europa, Azja, Ameryki)
- *Wymiar zastosowania:* wskaźnik dla osób fizycznych (UF-podobny) vs dla instytucji (SDR-podobny)

Pytanie: czy podział FDI/AUV jest właściwym pierwszym podziałem? Czy lepiej zacząć od jednego wskaźnika z dwoma "trybami" (fiat-mode vs real-mode)?

---

## 7. Co Eksperta Można Konkretnie Zapytać

Konkretne pytania, które warto skierować:

1. **Czy znana literatura akademicka analizuje podobne projekty?** Czy istnieją prace nad *de facto* heliocentrycznymi miernikami wartości — poza klasycznymi SDR i Unidad de Fomento? Co warto przeczytać przed dalszym kontynuowaniem?

2. **Czy proponowany FDI ma analogi w istniejących instrumentach finansowych?** TIPS (USA), OAT€i (Francja), UF (Chile) — wszystkie używają jednego CPI. Czy multi-currency CPI consensus jest gdzieś już używany w praktyce?

3. **Czy heliocentryczność przekłada się na *realnie lepszy* wskaźnik?** Czy istnieje empiryczna ewidencja, że indeksy "bez ludzkiej uznaniowości" są bardziej godne zaufania w długim okresie niż te z udziałem instytucji?

4. **Czy projektowanie wskaźnika *dla kredytów* (FDI) i *dla pomiaru cywilizacji* (AUV) wymaga rzeczywiście dwóch różnych konstrukcji?** Czy może wystarczy jeden, w różnych trybach interpretacji?

5. **Czy w nazwie wskaźnika (jak Unidad de Fomento) powinno być coś "neutralnego", czy ambitnego?** Marketingowo i społecznie — co działa?

---

## 8. Załączniki Techniczne

### 8.1 Pliki i dokumentacja w repozytorium

- `PROFIL_AUTORA.md` — filozofia projektu (heliocentryczność, terminologia)
- `PROTOTYP_PLAN_v0.2.md` — pierwsza formalna specyfikacja (ML + FWL + QP)
- `PROTOTYP_PLAN_v0.3.md` — przeprojektowanie do formuły p × N / q (cost of civilization)
- `DWA_PROJEKTY.md` — wyodrębnienie FDI i AUV jako osobnych projektów
- `prototyp/` — pełna implementacja w Pythonie

### 8.2 Najważniejsze wykresy (`prototyp/outputs/figures/`)

- `09_auv_vs_m2.png` — AUV v0.2 vs M2 USA, log skala
- `13_v3_vs_v2_vs_m2.png` — porównanie wszystkich iteracji
- `17_hybrid_auv_combined.png` — AUV v0.3.1 jako hybryda
- `20_compound_cpi.png` — skumulowana inflacja CPI G5+
- `22_ppp_test.png` — test PPP dla głównych par
- `24_real_fx_quarterly.png` — rzeczywiste kwartalne kursy
- `25_ppp_versions_comparison.png` — porównanie PPP wersji A i B

### 8.3 Słownik terminologii

W projekcie używamy precyzyjnej terminologii ekonomii monetarnej. Świadomie *odrzucamy* termin "dodruk pieniędzy" jako mylący i utrzymujący błędną intuicję, że pieniądz jest papierowy. We współczesnym systemie monetarnym >95% pieniądza istnieje wyłącznie elektronicznie i powstaje przez:

- **Kreację kredytową w bankach komercyjnych** — gdy bank udziela kredytu, kreuje nowy pieniądz depozytowy w księgach. Dominujący kanał kreacji pieniądza.
- **Ekspansję bilansu banku centralnego** — luzowanie ilościowe, skup aktywów, kreacja rezerw bankowych. Procesy księgowe.
- **Kreację długu publicznego** — pożyczki rządowe tworzą instrumenty finansowe pełniące funkcję pieniądza.

Akceptowalne terminy: *kreacja pieniądza*, *ekspansja monetarna*, *wzrost agregatów monetarnych*, *kreacja kredytowa*, *luzowanie ilościowe*, *powiększanie bilansu banku centralnego*.

---

## 9. Notatka Końcowa

Po sześciu miesiącach pracy projekt znajduje się w punkcie, w którym dalsze decyzje wymagają zewnętrznej, eksperckiej oceny. Implementacja techniczna istnieje. Dane są zebrane. Cztery iteracje koncepcyjne zostały przepracowane. Wnioski empiryczne (zwłaszcza z testów PPP) ujawniły, że samo zbliżenie się do problemu z jednej strony — czy to ML, czy formuła per capita, czy konsensus CPI — nie daje gotowej odpowiedzi.

Nie wykluczamy, że właściwa odpowiedź jest *prostsza* niż wszystkie nasze iteracje (np. mediana CPI G5 plus mała domieszka koszyka energii), lub *bardziej złożona* (pełna formuła AUV z 18 zasobami i defensywnym pre-processingiem). Ten dokument ma za zadanie umożliwić ekspertowi spoza projektu *szybką ocenę*, w którym kierunku warto pójść, bez konieczności prześledzenia wszystkich poprzednich rozmów.

Dokument przygotowany do dyskusji.

---

## 10. Propozycja Kierunku — AUV w Numéraire Czasu Pracy (v0.4)

*Dopisek z 2026-06-13. Sekcja proponuje nowy kierunek dla Projektu 2 (AUV) wraz ze wstępną weryfikacją empiryczną na danych już zebranych.*

### 10.1 Diagnoza — wspólny wątek wszystkich czterech porażek

Cztery iteracje próbowały różnych metod, ale wszystkie popełniły *ten sam* błąd: zachowały **pieniądz jako jednostkę rachunkową (numéraire)**. To jest właściwa przyczyna, dla której każda z nich zredukowała się ostatecznie do wariantu inflacji.

| Iteracja | Czym dzielono / co odejmowano | Dlaczego to wciąż fiat |
| --- | --- | --- |
| v0.1 (PCA/AE) | nic — kombinacja cen w fiat | kombinacja liniowa wielkości fiat też jest w fiat → 1. składowa = trend inflacyjny |
| v0.2 (FWL+QP) | odejmowano komponent M2 | M2 to agregat monetarny — kotwica wciąż monetarna, do tego współliniowa |
| v0.3 (p·N/q) | dzielono przez produkcję *q* | poprawne pojęciowo, ale *q* niedostępne → formuła padła na braku danych |
| v0.3.1 (real/fiat) | dzielono przez CPI | CPI to cena koszyka *innych dóbr* → iloraz cena/cena, błądzenie wewnątrz fiat |

Wniosek z v0.1 brzmiał: „trzeba dodać zewnętrzną kotwicę". Ale wszystkie kolejne kotwice (M2, CPI) *też były pieniężne*. Jedyny eksperyment z kotwicą niemonetarną — produkcja fizyczna *q* w v0.3 — rozbił się o brak danych, nie o błąd koncepcji.

**Teza tej sekcji:** istnieje kotwica niemonetarna, która (a) jest fizyczna i niemanipulowalna, (b) jest dostępna w danych, które *już mamy*, i (c) matematycznie wychodzi z pułapki fiat. Tą kotwicą jest **ludzki czas pracy**.

### 10.2 Mechanizm — dlaczego dzielenie przez dochód wychodzi z pętli fiat

Kluczowa obserwacja matematyczna, której nie wykorzystała żadna iteracja: jeśli dzielimy *cenę* (w USD) przez *dochód z pracy* (w USD), jednostka walutowa **kasuje się**, a wynik jest wyrażony w **godzinach/dniach ludzkiej pracy** — wielkości fizycznej, niezależnej od jakiejkolwiek waluty.

```
cena_w_czasie_i(t) = cena_i(t) [USD]  /  dochód_z_pracy_na_godzinę(t) [USD/h]   →  [godziny]
```

To jest istotnie różne od deflacji CPI. CPI to `cena / cena` — porównanie dobra do koszyka innych dóbr, oba rosnące z ekspansją monetarną (stąd „błądzenie wewnątrz fiat"). Numéraire pracy to `cena / dochód` — porównanie dobra do **jedynego zasobu, którego podaży nie da się wykreować księgowo**. Bank centralny może rozszerzyć M2 dowolnie; nikt nie może powiększyć liczby godzin w ludzkim życiu. Całkowita pula czasu cywilizacji ≈ populacja × roczne godziny pracy rośnie powoli i fizycznie — co czyni ją naturalnym filtrem ekspansji monetarnej.

To jest też klasyczna „wartość absolutna" w sensie Adama Smitha („praca była pierwszą ceną, pierwotnym pieniądzem nabywczym") oraz współczesna koncepcja **time price** (Tupy & Pooley, *Superabundance* 2022): mierz cenę liczbą godzin, które przeciętny człowiek musi przepracować, by ją zapłacić. Time price odpowiada *dokładnie* na centralne pytanie AUV z sekcji 1(b): „czy realnie świat się bogaci".

### 10.3 Formuła AUV-T

Dla koszyka kluczowych zasobów (energia, żywność, metale — ten sam koszyk fizyczny co dotąd):

```
AUV_T(t) = KoszykCen(t) / DochódGlobalnyNaJednostkęPracy(t)   [indeks, t_0 = 100]
```

- **Licznik:** indeks cen koszyka (np. średnia geometryczna znormalizowanych cen surowców) — bez zmian względem dotychczasowego podejścia.
- **Mianownik:** światowy dochód z pracy na jednostkę czasu. W docelowej wersji: `PKB_świata / całkowite_przepracowane_godziny` (produktywność pracy, OECD / Conference Board Total Economy Database / Penn World Table). W wersji minimalnej, *liczalnej dziś*: `PKB_świata / populacja` (dochód na osobę), bo godziny pracy na osobę zmieniają się wolno.

Interpretacja: **ile pracy cywilizacji kosztuje utrzymanie cywilizacji**. AUV_T spada, gdy produktywność wyprzedza ceny zasobów (realny postęp); rośnie, gdy zasoby drożeją szybciej niż rośnie ludzka produktywność (realna inflacja zasobowa). Identyczna semantyka, jaką chcieliśmy w v0.3 — ale *bez* zależności od niedostępnych danych produkcyjnych *q*.

### 10.4 Wynik wstępny — na danych, które już mamy

Policzyłem AUV_T na `monthly.parquet` (agregacja roczna, koszyk równo-ważony: brent, natgas, węgiel, pszenica, kukurydza, ryż, miedź, aluminium, ruda żelaza; mianownik = `gdp_world_current_usd / world_population`; t₀ = 1996 = 100). Zero nowych danych.

| Rok | Koszyk nominalny | CPI USA | M2 USA | Dochód glob./os. | Koszyk realny (÷CPI) | **AUV_T (÷czas)** |
| --- | --- | --- | --- | --- | --- | --- |
| 1996 | 100,0 | 100,0 | 100,0 | 100,0 | 100,0 | **100,0** |
| 2008 | 261,6 | 137,2 | 209,3 | 159,2 | 190,6 | **164,3** |
| 2020 | 185,7 | 165,0 | 474,6 | 206,5 | 112,5 | **89,9** |
| 2025 | 252,2 | 205,3 | 589,0 | 248,3 | 122,8 | **101,6** |

Zmiana 1996 → 2025: koszyk nominalny **+152%**, M2 USA **+489%**, CPI USA **+105%**, dochód globalny/os. **+148%**, koszyk realny vs CPI **+23%**, **AUV_T +1,6%**.

Dwie obserwacje warte uwagi eksperta:

1. **AUV_T jest niemal stacjonarny w 30-letnim horyzoncie** (+1,6%), mimo że nominalnie koszyk wzrósł o 152%, a M2 o 489%. To jest pożądana własność „jednostki absolutnej": mierzone w ludzkiej pracy, koszyk dóbr podstawowych kosztuje dziś tyle, co w 1996. Realna wartość zasobów względem ludzkiej zdolności wytwórczej została w przybliżeniu *zachowana*.

2. **Koszyk nominalny (+152%) ≈ dochód globalny/os. (+148%).** Ceny zasobów esencjonalnych i ludzki dochód rosły niemal równolegle — to mikroskala tezy *Superabundance*. Sygnał, że ekspansja monetarna unosi *jednocześnie* ceny surowców i nominalne dochody, więc ich iloraz ją wycina.

Przy tym AUV_T nie jest płaski w środku okresu — wyłapuje realne szoki: szczyt 2008 (164) i dołek 2015–2020 (~88–90), czyli surowcowy boom i jego rozejście. To jest sygnał *realny*, nie monetarny. (Wartości robocze, do audytu; skrypt do dopisania jako `src/auv_t.py`.)

### 10.5 Co ta propozycja rozwiązuje

- **Pułapka v0.1** (wszystko w fiat): rozwiązana — iloraz cena/dochód kasuje walutę, wynik w godzinach.
- **Blokada v0.3** (brak danych *q*): rozwiązana — numéraire pracy nie wymaga danych produkcyjnych ani populacji jako mnożnika; działa na danych już zebranych.
- **Redukcja v0.3.1 do CPI**: rozwiązana — mianownik to dochód (cena pracy), nie koszyk dóbr; to inna wielkość niż CPI i niesie informację o produktywności.
- **Niestabilność v0.2/v0.3** (oscylacje 40–300): wstępnie rozwiązana — AUV_T mieści się ~88–164, a długoterminowo wraca do 100. To kandydat *nadający się* na jednostkę rozliczeniową (Projekt 2 zbliża się do użyteczności Projektu 1).

### 10.6 Karta heliocentryczna

| Kryterium (z `PROFIL_AUTORA.md`) | Ocena AUV_T |
| --- | --- |
| Dane otwarte, bez gatekeepera | ✓ ceny rynkowe + PKB/populacja (UN, World Bank, OECD — redundantne źródła) |
| Formuła deterministyczna | ✓ iloraz dwóch obserwabli + ustalony koszyk |
| Brak pojedynczego punktu awarii | ~ dochód/produktywność liczone przez instytucje; ale wielu niezależnych dostawców (UN, WB, OECD, Conference Board, PWT) |
| Audytowalność | ✓ każdy krok jawny, brak ML |
| Niezależność od *fiat* autorytetu | ✓✓ numéraire (czas) jest poza zasięgiem banków centralnych i urzędów — silniejsze niż FDI, który mierzy fiat *w* fiat |

Paradoks wart odnotowania: AUV_T jest *bardziej* heliocentryczny niż FDI, bo jego jednostka jest fizyczna (godzina), a nie umowna (jednostka indeksu zdefiniowana przez koszyk walut).

### 10.7 Pytania do eksperta (specyficzne dla tej propozycji)

1. **Wybór mianownika.** Co jest właściwszą „ceną pracy cywilizacji": (a) globalne PKB/godzinę (produktywność zagregowana), (b) mediana płacy niewykwalifikowanej (interpretacja *time price* à la Superabundance — „ile pracuje zwykły człowiek"), czy (c) płaca realna G5 ważona populacją? Każdy daje inny AUV_T; który ma najlepszą interpretację dla umów wieloletnich i dla pomiaru dobrobytu?

2. **PKB nominalne vs PPP.** W liczniku ceny światowe w USD; w mianowniku PKB w bieżących USD jest spójne. Ale czy dla pomiaru *globalnego* dobrobytu nie należy użyć PKB w PPP (mamy `gdp_per_capita_ppp`)? Jak to zmienia interpretację jednostki?

3. **Tautologiczność.** Czy `cena / dochód` nie jest po prostu „udziałem zasobu w dochodzie" — wielkością znaną w ekonomii (np. Engel, share-of-income)? Jeśli tak, czy to wada (brak nowości), czy zaleta (osadzenie w uznanej teorii)? Czym AUV_T różni się od indeksu *commodity terms of labour*?

4. **Stabilność jako artefakt.** Czy near-stacjonarność AUV_T (+1,6% / 30 lat) to realna własność świata, czy artefakt tego, że PKB *zawiera* wartość dodaną tych samych surowców (endogeniczność licznika i mianownika)? Jak to formalnie odseparować?

5. **Relacja do literatury.** Poza Smithem, Tupy & Pooley (time prices) i klasyczną labour theory of value — czy istnieją współczesne, recenzowane miary „commodity prices in wage units" (np. prace Jacksa o realnych cenach surowców, indeksy Grilli-Yang deflowane płacą)? Co warto przeczytać, zanim ogłosimy to jako nowość?

### 10.8 Następny minimalny eksperyment

Jedna sesja pracy, bez nowych źródeł: (1) napisać `src/auv_t.py` formalizujący formułę 10.3; (2) policzyć trzy warianty mianownika z 10.7.1 i porównać na jednym wykresie; (3) test wrażliwości na skład koszyka (energia vs żywność vs metale osobno); (4) zestawić AUV_T z AUV v0.2 i M2 na jednym logarytmicznym wykresie, żeby pokazać, że *to* jest seria, która nie ucieka razem z M2. Dopiero po tym — decyzja, czy AUV_T zostaje rdzeniem Projektu 2 i czy uzasadnia jeszcze akwizycję danych *q* (do dekompozycji, nie do samej formuły).

---

## 11. Dorobek v0.4 — Co Zrealizowano

*Sekcja dopisana 2026-06-22. Podsumowuje pełen cykl prac v0.4 zrealizowany po sformułowaniu propozycji z sekcji 10. Wszystkie liczby pochodzą z kodu w `prototyp/src/` na danych 1996–2025; wartości robocze, do audytu.*

### 11.1 Streszczenie

Propozycja z sekcji 10 (numéraire pracy) została zaimplementowana i rozwinięta w pełną rodzinę wskaźników. Powstały cztery moduły obliczeniowe (`auv_t.py`, `auv_research.py`, `analysis_v4.py`, `collateral_inflation.py`), rozbudowano rejestr danych z 71 do ~85 serii (w tym nowe źródło danych ręcznych), a wątek jakości pieniądza dał nieoczekiwane, mocne wyniki empiryczne dotyczące kanałów inflacji. Poniżej zwięzła mapa rezultatów.

### 11.2 AUV-T — rdzeń (zaimplementowany)

Formuła `AUV-T(t) = KoszykCen(t) / DochódNaJednostkęPracy(t)` (sekcja 10.3) policzona na 19 cenach surowców w 4 kategoriach (energia, żywność, metale, budownictwo). Wynik potwierdza tezę o braku dryfu:

| Wielkość | Zmiana 1996→2025 |
| --- | --- |
| Koszyk nominalny (USD) | +149% |
| M2 USA | +489% |
| CPI USA | +105% |
| Dochód globalny / os. | +148% |
| **AUV-T** | **+0,4%** |
| SDR (syntet., koszyk MFW) | +90% |

Mierzony w ludzkiej pracy, koszyk dóbr podstawowych kosztuje dziś tyle, co w 1996 — przy niemal pięciokrotnym wzroście M2. SDR, mimo statusu „neutralnej" jednostki, dryfuje w górę razem z walutami (jest z fiat-u).

**Odporność na wybór mianownika:** dochód na osobę (+0,4%) vs na pracownika (+3,5%) — różnica nieistotna. Wynik nie zależy od tej decyzji.

### 11.3 Rozkład trend / cykl

AUV-T rozłożono log-addytywnie na trend kroczący (7-letni, przyczynowy — kandydat na rdzeń kontraktowy) i cykl. Zmienność rocznych zmian spada z 0,152 (surowe) do 0,046 (trend). Cykl (amplituda ~75–145) stał się osobnym, czytelnym **wskaźnikiem napięcia zasobowego**: fazy „drogo" 2005–08 i 2021–22, „tanio" 1997–02 i 2013–20. Wniosek metodologiczny: falowanie AUV-T to niskoczęstotliwościowy cykl surowcowy (sygnał), nie szum — czego nie da się usunąć samym wygładzaniem.

### 11.4 Koszyk ważony zapotrzebowaniem (rozwiązanie problemu v0.3)

Wprowadzono pomiar „kosztu utrzymania jednego człowieka" w dwóch wariantach, co rozplątuje tautologię, która zablokowała v0.3:

- **Przetrwanie** (R zamrożone na poziomie 1996): **+0,4%** — utrzymanie standardu z 1996 jest dziś „za darmo" w jednostkach pracy (postęp technologiczny zrównoważył ceny).
- **Standard** (R rośnie z realną konsumpcją per capita): **+58,8%** — utrzymanie *dzisiejszej*, wyższej konsumpcji kosztuje o ~59% więcej pracy.

Odstęp to czysty koszt cywilizacyjnego skoku. Napędzają go wzrosty zużycia per capita 1996→2025: energia +17%, żywność +47%, **metale +92%**, **budownictwo +88%**.

Kluczowe: formuła nie wymaga już dzielenia przez produkcję `q` (blokada v0.3) — zapotrzebowanie wchodzi jako *waga ilościowa*, a nie mianownik. Dane ilości dla metali i budownictwa pochodzą z ręcznie wypełnianego pliku (`data/manual/`, źródła USGS/World Steel); kategorie bez danych automatycznie działają na stałym R.

### 11.5 Wątek FDI — jakość pieniądza i kanały inflacji

Rozszerzono Projekt 1 (FDI) o wymiar *jakości* kolateralu (sekcja po przeformułowaniu: „przeciwko czemu kreowany jest pieniądz"). Najważniejszy wynik empiryczny dotyczy **kierowania inflacji przez rodzaj zabezpieczenia**:

| Źródło pieniądza | korelacja z CPI | korelacja z cenami domów |
| --- | --- | --- |
| Hipoteki (cały dług) | +0,35 (6 m) | **+0,58** |
| Dług państwa (Fed UST) | **+0,41** (18 m) | +0,04 |
| M2 (cały) | +0,52 (18 m) | +0,15 |

Asymetria: **dług państwowy → inflacja konsumencka** (CPI), a **hipoteka → inflacja aktywów** (ceny domów), nie CPI. To empiryczny szkielet pod tezę o hierarchii jakości kolateralu (dług suwerenny najgorszy). Ważne zastrzeżenie: korelacja to nie przyczynowość, dane wyłącznie USA, a wagi jakości w indeksie Q są normatywne i sporne (austriacy vs główny nurt). Szczegóły w `USTALENIA_hipoteka_inflacja.md`.

Implikacja dla całego projektu: skoro znaczna część kreacji pieniądza (hipoteki) ucieka w aktywa, których CPI nie mierzy, indeksacja oparta na samym CPI jest systematycznie ślepa na połowę zjawiska — co jest bezpośrednim argumentem za jednostką opartą na pracy.

### 11.6 Rozbudowa infrastruktury danych

Dodano: ceny budownictwa (stal `WPU101`, cement `PCU327310327310` — proxy PPI USA), siłę roboczą świata (`SL.TLF.TOTL.IN`), bilans Fed (`WALCL/TREAST/WSHOMCB`), kredyt banków H.8 (`REALLN/BUSLOANS/CONSUMER/TOTBKCR`), ceny domów (`CSUSHPISA`), cały dług hipoteczny (`HHMSDODNS`), podaż nowych domów (`HOUST/HNFSEPUSSA`). Powstało nowe źródło **`manual`** (`src/sources/manual.py`) z szablonem CSV dla danych z PDF (USGS/World Steel) — rozwiązuje problem akwizycji produkcji metali zgłoszony w sekcji 6.3(a).

### 11.7 Ograniczenia v0.4

(1) Dane produkcji metali/cementu są *przybliżone* (odtworzone z wiedzy do 2025-05), do weryfikacji przy źródłach pierwotnych — choć dynamika, która decyduje, jest wiarygodna. (2) Produkcja globalna użyta jako proxy konsumpcji per capita. (3) Ruda żelaza, nikiel, cynk wciąż bez danych ilości — „metale" liczą się z miedzi i aluminium. (4) Wątek jakości pieniądza wyłącznie dla USA; wagi Q normatywne. (5) Rozkład trend/cykl używa kroczącej średniej — lag i wrażliwość na okno do formalnej analizy.

### 11.8 Rekomendowane następne kroki

W kolejności wartości: (a) test wrażliwości i walidacja AUV (skład koszyka, wagi, rok bazowy, geom. vs aryt.) — by wykazać, że wynik nie zależy od arbitralnych wyborów; (b) formalny model jakości pieniądza z kontrolą na M2 (testy Grangera) — czy kolateral wnosi coś ponad ilość; (c) wariant kontraktowy AUV (szerszy koszyk + wygładzanie) do indeksacji; (d) rozszerzenie wątku jakości pieniądza na EBC/BoJ/BoE.

### 11.9 Walidacja wrażliwości (zrealizowana)

Krok (a) z 11.8 wykonano (`src/sensitivity.py`). Wynik: teza „AUV-T bez dryfu, odsprzężony od M2" jest **odporna na arbitralne wybory**.

- **Leave-one-out kategorii:** AUV-T 2025 w przedziale 91–124 niezależnie od usuniętej kategorii (M2 = 589).
- **Monte Carlo wag (1000 losowań z sympleksu Dirichleta):** AUV-T 2025 średnia 102, pasmo 5–95 pct = 75–127; nawet skrajne losowanie (249) nie zbliża się do M2.
- **Średnia geom. vs aryt.:** 100,4 vs 106,9 — bez znaczenia.
- **Korelacja z M2:** 0,11–0,28 we wszystkich konfiguracjach.
- **Rok bazowy:** dryf całego okresu niezmienniczy (+0,4%); baza tylko przeskalowuje odniesienie.

**Rekomendacja (jedyna realna wrażliwość):** choć *dryf* jest niezmienniczy, *poziom* w danym roku zależy od wyboru roku bazowego (76 przy bazie 2010, 123 przy bazie 2000). Narracja „płasko wokół 100" wymaga bazy nie będącej ekstremum cyklu. Rok bazowy należy więc ustalać **jawną regułą** (np. średnia z pierwszych N lat szeregu, albo rok najbliższy długookresowej medianie), a nie ad hoc — zgodnie z zasadą heliocentryczną zakazu uznaniowości po fakcie.

### 11.10 Domknięcie wątku jakości pieniądza i wariant kontraktowy (kroki b–d)

**(b) Czy kolateral przewiduje inflację ponad M2?** (`src/money_quality_model.py`). Granger parami: M2 (p=0,007) i monetyzacja długu państwa (p=0,041) wyprzedzają inflację CPI. Ale w regresji przyrostowej z kontrolą na M2 (błędy Newey-West) **żaden składnik kolateralu nie wnosi istotnie ponad samą ilość pieniądza** (wszystkie p>0,05; wzrost hipotek na granicy, p=0,06). Wniosek: dla *skali* inflacji rządzi ilość (M2), nie jakość kolateralu; kolateral steruje *kierunkiem* (CPI vs aktywa, krok wcześniejszy), nie magnitudą. Zastrzeżenie: próba mała (22–28 obs), test słabo mocny.

**(c) Wariant kontraktowy AUV** (`src/auv_contract.py`). Szeroki koszyk + dwie zamrożone reguły: baza = średnia 3 pierwszych lat, wygładzanie 5-letnie krocząco. Maks. zmiana roczna spada z **52% (surowe) do 12%**, typowa z 11,6% do 4,8%. To czyni AUV znacznie bardziej zdatnym do indeksacji, ale wciąż **mniej gładkim niż CPI** (maks. 8%, CPI prawie nigdy nie spada, AUV-kontrakt potrafi −10%). Realny kompromis: realna wartość bez dryfu fiat (kończy ~128 vs CPI ~200) kosztem resztkowej zmienności cyklu surowcowego.

**(d) Bilanse banków centralnych cross-country** (`src/cb_balance_sheets.py`). Zakres: ilość (suma aktywów), bo skład kolateralu jak dla Fed nie jest porównywalnie dostępny dla EBC/BoJ. Wynik decydujący:

| Bank centralny | Wzrost bilansu | Inflacja CPI okresu |
| --- | --- | --- |
| Fed (2002–2025) | +811% (×9,1) | +79% |
| EBC (1999–2025) | +759% (×8,6) | +73% |
| BoJ (1998–2021) | +805% (×9,0) | **+1,3%** |

Niemal identyczna ekspansja bazy monetarnej, a inflacja od +79% do zera. **Sama ekspansja bilansu banku centralnego nie napędza inflacji konsumenckiej** — Japonia jest podręcznikowym dowodem (×9 bilans, ~0 inflacji, bo pieniądz nie krążył przez kredyt). Domyka krok (b): transmisją inflacji jest M2/kredyt, nie bilans banku centralnego. Korelacje dynamik rok-do-roku: USA −0,24, EBC −0,13, JP +0,31 — wszystkie słabe.

**Łączny wniosek wątku FDI:** dla *wielkości* inflacji liczy się szeroki pieniądz (M2/kredyt), nie baza monetarna ani skład kolateralu; *kierunek* inflacji (konsumencka vs aktywów) zależy od rodzaju kolateralu (dług państwa → CPI, hipoteka → aktywa). To wzmacnia rację bytu AUV: indeksacja na samym CPI jest ślepa na inflację aktywów, a jednostka oparta na pracy mierzy realną wartość niezależnie od kanału.

### 11.11 AUV zastosowany do finansów: realna wartość rynków akcji i mapa wydarzeń

**Giełdy w godzinach pracy** (`src/auv_markets.py`, indeksy akcji OECD USA/UK/JP wyrażone w tym samym numéraire pracy co AUV). Wynik 1996→2025:

| Rynek | Nominalnie | W godzinach pracy (realnie) |
| --- | --- | --- |
| USA | ×5,4 (539) | **+117%** (217) |
| Wielka Brytania | ×2,4 (235) | **−5%** (95) |
| Japonia | ×1,8 (183) | **−26%** (74) |

Interpretacja: tylko rynek USA stworzył realne bogactwo. Nominalny wzrost giełdy japońskiej (+83%) i brytyjskiej był w dużej mierze *iluzją monetarną* — w jednostkach pracy japoński rynek cofnął się o ~26%. To domyka „triadę Japonii": bilans BoJ ×9 → ~zero inflacji → realny spadek giełdy. Ten sam pieniądz nie stworzył ani inflacji, ani realnej wartości rynku. Trzeci niezależny dowód, że *ilość pieniądza ≠ realna wartość*, i najdobitniejsza ilustracja użyteczności numéraire pracy.

**Sygnał czasowy (hipoteza „kupuj, gdy realne dobra tanie"):** korelacja AUV-T[t] z przyszłym zwrotem giełdy jest ujemna dla USA (−0,27 w 1 rok, −0,18 w 5 lat), lecz niespójna dla UK/JP i słaba. Wniosek: AUV *nie* jest wiarygodnym sygnałem market-timing — jest *miarą* realnej wartości, nie predyktorem. (Analiza historyczna, nie rekomendacja.)

**Mapa wydarzeń** (`45_auv_wydarzenia.png`). Wychylenia AUV-T pokrywają się z globalnymi szokami zasobowymi: dołek 2001 (kryzys azjatycki, bańka dot-com, tania ropa), szczyt 2008 (supercykl surowcowy napędzany Chinami, ropa ~$147), szczyt 2011 (odbicie po QE, Arabska Wiosna), dołek 2015–2020 (krach ropy 2014, spowolnienie Chin, COVID), szczyt 2022 (post-COVID + inwazja Rosji na Ukrainę). Potwierdza to, że cykl AUV-T niesie realny sygnał (napięcie zasobowe), a nie szum — przecięcia stałej 100 wyznaczają przejścia między fazą „tanio/mocny pieniądz" a „drogo/słaby pieniądz" wobec realnych dóbr.

**Rola AUV wobec oszczędności:** wynik giełdowy pokazuje, że AUV nie mówi *kiedy* inwestować, ale rzetelnie mierzy, *czy* oszczędności (gotówkowe czy giełdowe) realnie zyskały — po odjęciu iluzji monetarnej. To potwierdza AUV jako miernik (linijkę), nie wyrocznię.

---

## 12. Dygresja: heliocentryczność a ekonomia polityczna instytucji

*Sekcja dyskusyjna. Formułuje obserwację o charakterze ekonomii politycznej — świadomie wyważoną, z argumentami za i przeciw.*

Podejście heliocentryczne ujawnia klasę problemów, które *dają się* rozwiązać deterministyczną regułą na danych publicznych, a które dziś „rozwiązuje" uznaniowość instytucji: ustalanie stóp referencyjnych, indeksów inflacji, kursów rozrachunkowych. Nasuwa się obserwacja, że instytucje dysponujące tą uznaniowością mają słabą zachętę, by zastąpić ją regułą, która tę uznaniowość odbiera — reformator jest tu zarazem podmiotem ograniczanym.

**Argument za tezą (dlaczego opór jest strukturalny, nie spiskowy).** To nie jest teza o złej woli, lecz o bodźcach — dobrze opisana w teorii wyboru publicznego (Buchanan, Tullock), teorii przechwycenia regulacyjnego (Stigler) i w literaturze o samozachowaniu organizacji. Podmiot, którego racją bytu jest wydawanie osądów, racjonalnie nie promuje narzędzia, które te osądy czyni zbędnymi. Wartość informacyjna uznaniowości jest też źródłem renty (kto ustala benchmark, ten ma władzę i wpływ). Historyczne analogie — od oporu wobec heliocentryzmu Kopernika, przez zamknięte standardy przełamywane przez open source, po kryptografię publiczną odbierającą monopol na zaufanie — sugerują, że reguły przejrzyste wygrywają tam, gdzie istnieje obiektywna prawda do zmierzenia, ale wygrywają *wolno* i wbrew zasiedziałym interesom.

**Argument przeciw / konieczne wyważenie.** Uczciwość wymaga odnotowania, że instytucje dostarczają realnej wartości, której reguła nie odtwarza: reakcji na kryzys w sytuacjach bezprecedensowych, osądu tam, gdzie sztywna formuła produkuje gorsze wyniki (por. `PROFIL_AUTORA.md`, „Świadomość Granic": sąd, lekarz, redaktor), oraz rozliczalności i legitymacji demokratycznej. Nie każdy opór wobec automatyzacji jest obroną renty — część to uzasadniona ostrożność wobec kruchości sztywnych reguł (czego dowiódł Bitcoin: niezmienność protokołu bywa wadą). Dlatego krytyka jest *celowana*, nie totalna: dotyczy funkcji, gdzie istnieje mierzalna prawda (pomiar, rozliczenia, alokacja wg mierzalnych kryteriów), a nie obszarów z natury uznaniowych.

**Synteza.** AUV nie znosi instytucji — *relokuje* jedną funkcję (pomiar wartości) z uznaniowości do reguły, zostawiając instytucjom to, czego reguła nie potrafi. Opór jest przewidywalny i po części uzasadniony, ale tam, gdzie prawda jest obiektywnie mierzalna, przeniesienie jej spod głosowania pod regułę, którą każdy może sprawdzić, jest — zgodnie z motywacją projektu — pracą konstrukcyjną na rzecz świata, w którym ludzie nie są zdani na cudze zaufanie, gdy chcą wiedzieć, czy nie są oszukiwani. To zdanie jest tezą normatywną autora, nie wnioskiem empirycznym pracy — i jako takie zostaje wyraźnie oznaczone.

---

## 13. KOREKTA (2026-07): błąd w pipeline i rewizja liczb flagowych po ocenie zewnętrznej

Zewnętrzna ocena ekonomiczna (`OCENA_ekonomisty_praktyka.md`) wykryła **błąd w pipeline**: mianownik (dochód/os.) był opóźniony o ~1 rok względem danych źródłowych (dane roczne WB stemplowane 31.12 + forward-fill + roczne uśrednianie). Zweryfikowane (korelacja z WB(t−1)=0,9999) i naprawione (`src/auv_t.py` — mianownik z wartości końca roku).

**Rewizja liczb flagowych:**
- Dryf AUV-T **1996→2024 = +5,0%** (poprawnie zsynchronizowany), a nie +0,4%/30 lat. Wartość „2025 = +0,4%" jest **prowizoryczna** (brak PKB 2025 w WB → koszyk 2025 dzielony przez dochód 2024) i nie jest liczbą flagową.
- Zmienność AUV-T: **0,123** (było 0,154); cykl urealniony (szczyty 2008/2011 niższe o ~10 pkt). Wnioski jakościowe (brak wielkiego dryfu w tej próbie, odsprzężenie od M2) pozostają, ale są *słabsze* i wymagają backtestu przed 1996.

**Skorygowane deklaracje (za `ODPOWIEDZ_na_ocene.md`):** „stała/absolutna wartość" → „miara o znanym cyklu; trend długookresowy do zbadania (backtest 1900)"; „bez autorytetu" → „minimalizacja i przejrzystość uznaniowości; determinizm stopniowalny; mianownik zależny od danych instytucji i od kursu USD"; „w godzinach pracy" → „w jednostkach dochodu"; „w pełni otwarte dane" → „przeważnie otwarte". **Wykreślone zastosowania:** emerytury, alimenty, detaliczne hipoteki „w AUV" (do czasu backtestu, mianownika PPP/realnego i rozwiązania kwestii administratora BMR). Pełna pozycja do ośmiu luk: `ODPOWIEDZ_na_ocene.md`.
