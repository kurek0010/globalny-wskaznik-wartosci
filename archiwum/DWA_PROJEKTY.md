# Dwa Równoległe Projekty — Mapa Kierunków

**Data:** 2026-06-09
**Status:** Dokument koncepcyjny do dalszego namysłu i samodzielnych eksperymentów autora.
**Cel:** Po wielomiesięcznych rozmowach i empirycznych próbach (v0.1, v0.2, v0.3, v0.3.1) rozdzielić dwa naturalnie odrębne projekty, które dotąd były pomieszane pod jednym dachem. Każdy z nich ma inną ambicję, inny stopień osiągalności i inne zastosowanie.

---

## Streszczenie

Po długim okresie eksperymentowania doszliśmy do wniosku, że to, co próbowaliśmy zbudować jako jeden wskaźnik, w rzeczywistości łączy dwa różne pomysły o różnej dojrzałości i przeznaczeniu. Lepiej rozdzielić je na dwa równoległe projekty.

**Projekt 1 — FDI (Fiat Depreciation Index)**: kompozytowy wskaźnik mierzący *deprecjację pieniądza papierowego* z czterech komplementarnych źródeł sygnału. Praktyczny, osiągalny w obecnym stanie danych, gotowy do zastosowania *zamiast WIBOR-u w umowach kredytowych*. To jest projekt *do zrobienia teraz*.

**Projekt 2 — AUV (Absolute Unit of Value)**: aspiracyjny wskaźnik mierzący *realną wartość cywilizacji*, oparty na cenach surowców, ich produkcji i populacji. Wymaga jeszcze pracy nad danymi i metodologią. To jest projekt *do rozwijania w dłuższym horyzoncie*, jako badanie.

Oba projekty mogą wykorzystywać tę samą infrastrukturę danych (FRED, World Bank, ECB, NBP) i kod (`prototyp/src/sources/*.py`). Różnią się formułą i interpretacją, ale dzielą fundament techniczny.

---

## Projekt 1 — FDI (Fiat Depreciation Index)

### Cel

Stworzenie obiektywnego, deterministycznego wskaźnika *deprecjacji walut papierowych*, który mógłby służyć jako podstawa umów kredytowych zamiast WIBOR-u, SOFR-u czy podobnych benchmarków ustalanych decyzjami rad bankowych.

FDI odpowiada na pytanie: **"Jak bardzo główne waluty światowe straciły wartość względem konsensusu?"**

Nie odpowiada na pytanie *"czy świat realnie się bogaci"* — to jest zadanie AUV. Nie próbuje też wyciągać "ukrytej wartości" — to się okazało ślepą uliczką w v0.1 i v0.2.

### Cztery komponenty FDI

FDI składa się z czterech sygnałów, każdy uchwytuje inną fazę procesu deprecjacji fiat-u:

**1. SDR (lub syntetyczny SDR)** — wskaźnik *relatywny*. Pokazuje, jak waluty zachowują się *wobec siebie*. Jeśli złoty traci 30% wobec średniej, a frank szwajcarski zyskuje 5% — to realna informacja o względnej sile walut. SDR nie pokazuje absolutnej utraty wartości, tylko *kto traci szybciej, kto wolniej*. Waga proponowana: **15%**.

*Skąd dane:* MFW publikuje SDR codziennie. Alternatywnie można zbudować "syntetyczny SDR" z transparentnymi wagami opartymi na udziale w światowym PKB, automatycznie rewidowanymi formułą zamiast decyzją Zarządu MFW.

**2. CPI głównych walut** — wskaźnik *konsumencki*. Pokazuje, ile *więcej fiat-u* trzeba dziś, żeby kupić ten sam koszyk dóbr konsumenckich, co rok temu. Mierzony osobno dla każdej z głównych walut (USD, EUR, JPY, GBP, CHF), uśredniony z wagami opartymi na udziale w światowym PKB. Waga proponowana: **35%** — to najbardziej bezpośrednia miara deprecjacji.

*Skąd dane:* FRED publikuje CPI dla wszystkich głównych walut z miesięczną granulacją. Już mamy te serie pobrane (8 CPI w `prototyp/data/processed/monthly.parquet`).

**3. M2 (szeroka podaż pieniądza)** — wskaźnik *kreacji pieniądza*. Pokazuje, ile pieniądza zostało wykreowane *przez kredyt komercyjny* (banki udzielające pożyczek) i *przez ekspansję bilansów banków centralnych* (luzowanie ilościowe, skup aktywów). M2 jest *przyczyną* inflacji konsumenckiej i aktywowej, więc często wyprzedza CPI. Jeśli M2 rośnie szybciej niż CPI — coś się dzieje na rynkach finansowych (inflacja aktywów zamiast konsumenckiej). Waga proponowana: **30%**.

*Skąd dane:* FRED publikuje M2 dla USA (M2SL), strefy euro, Wielkiej Brytanii i innych krajów z miesięczną granulacją. Już mamy podstawowe serie.

**4. Dług publiczny do PKB** — wskaźnik *strukturalnej presji inflacyjnej*. Pokazuje, ile *przyszłej* deprecjacji już zostało zaprogramowane. Wysokie zadłużenie publiczne prędzej czy później musi być albo spłacone (przez podatki), albo zmonetyzowane (przez kreację pieniądza). To wyprzedzający, wolno-poruszający się sygnał. Waga proponowana: **20%**.

*Skąd dane:* FRED publikuje stosunek długu publicznego do PKB dla USA (GFDEGDQ188S), MFW dla całego świata. Pełne dane są kwartalne, ale to wystarcza dla strukturalnego komponentu.

### Formuła FDI

Każdy z czterech komponentów normalizujemy do dnia bazowego (np. 2017-06-30 = 100), potem bierzemy ważoną średnią geometryczną lub arytmetyczną.

```
FDI(t) = 0.35 × CPI_konsensus(t) + 0.30 × M2_konsensus(t)
       + 0.20 × Dług_PKB_konsensus(t) + 0.15 × SDR(t)
```

Wynik: liczba wokół 100 w punkcie bazowym, rosnąca w miarę postępu deprecjacji. W 2025 FDI byłby prawdopodobnie w okolicach 140–160 (czyli średnia waluta straciła 30–40% wartości od 2017).

### Zastosowanie kredytowe

Umowa: kredyt indeksowany do FDI plus marża.

Przykład: pożyczam 30 000 jednostek FDI (na koniec 2025: 30 000 × 1,50 = 45 000 USD), oddaję 30 000 jednostek FDI plus 2% rocznie marży. Co miesiąc do raty doliczana jest *aktualna wartość 1 jednostki FDI w walucie kontraktu*. Marża jest czystym zwrotem za czas i ryzyko — nie zawiera ryzyka inflacyjnego, bo to jest już *odjęte* w samym mechanizmie indeksacji.

### Eksperymenty, które warto przemyśleć/przeprowadzić samodzielnie

Zanim ruszymy z pełną implementacją, warto popatrzeć na każdy z czterech komponentów osobno. Sugerowane proste analizy:

1. **CPI G5 vs poszczególne CPI.** Czy CPI Szwajcarii faktycznie był stabilniejszy niż CPI USA przez 30 lat? Jaki jest dystans między najstabilniejszą a najmniej stabilną walutą? Wykres pokazałby od razu, czy konsensus G5 niesie sensowną informację.

2. **M2 USA vs CPI USA.** Klasyczne pytanie ekonomistów — czy M2 wyprzedza CPI? Jeśli tak, o ile miesięcy? Jeśli CPI w 2022 wystrzeliło, czy M2 to zapowiadało już w 2020? To analiza opóźnień.

3. **Dług publiczny do PKB w USA.** Jak wyglądał trend? 60% w 1996, ok. 100% w 2008, ok. 120% w 2025. Czy korelacja z inflacją jest widoczna *w długim okresie*?

4. **SDR vs koszyk równo-ważony.** Czy oficjalny SDR (z aktualnych wag MFW) różni się znacząco od równo-ważonego koszyka 5 głównych walut? Jeśli różnice są małe, to znaczy, że MFW nie wprowadza wiele "uznaniowości".

Każda z tych analiz to godzinka pracy — nowa komórka w istniejącym notebooku lub krótki własny skrypt. Po nich można decydować, czy wagi 15/35/30/20 są rozsądne, czy trzeba je przesunąć.

### Świadome ograniczenia FDI

FDI nie pokaże:

- Czy realnie świat się bogaci czy biednieje.
- Czy postęp technologiczny przewyższa inflację.
- Czy konsumpcja jakiegoś dobra rośnie na osobę.

Te pytania nie są jego zadaniem. FDI to *miernik deprecjacji fiat-u*, nie miernik realnej wartości.

---

## Projekt 2 — AUV (Absolute Unit of Value)

### Cel

Stworzenie wskaźnika mierzącego *koszt utrzymania ludzkiej cywilizacji na obecnym poziomie technologicznym*, mierzony w realnych zasobach fizycznych. Wskaźnik powinien:

- Spadać, gdy postęp technologiczny i produkcja per capita wyprzedzają konsumpcję (realny postęp cywilizacji).
- Rosnąć, gdy konsumpcja przewyższa produkcję per capita (rzeczywista inflacja zasobowa).
- Stać w miejscu, gdy procesy się równoważą.

AUV odpowiada na pytanie: **"Czy w realnych jednostkach świat jest bogatszy niż 30 lat temu?"**

### Architektura — formuła oparta na fundamentach

Dla każdego z 15–20 kluczowych zasobów w koszyku:

```
realna_wartość_i(t) = cena_i(t) × potrzeba_na_osobę_i × populacja(t) / produkcja_globalna_i(t)
```

Wskaźnik AUV jest ważoną sumą tych realnych wartości w pięciu kategoriach: energia, żywność, budownictwo, metale przemysłowe, materiały krytyczne.

Pełna specyfikacja w `PROTOTYP_PLAN_v0.3.md`.

### Status — gdzie jesteśmy

Wersja v0.3.0 została zaimplementowana w `prototyp/src/auv_v3.py` i `notebooks/04_auv_v3.ipynb`, ale wyniki są niezadowalające z trzech powodów:

1. **Brak twardych danych produkcyjnych** dla metali, ropy, gazu, materiałów budowlanych. Bez nich formuła `cena × N / produkcja` redukuje się do "cena razy stała", co praktycznie nie wnosi informacji ponad samą cenę.
2. **Wagi kategorii** wybrane arbitralnie (50/50 food/energy w prototypie), nie z analizy realnego udziału w fizycznym przepływie cywilizacji.
3. **Anomalie w danych** World Bank (np. produkcja zbóż 2024) wymagają agresywniejszego pre-processingu, niż początkowo zakładaliśmy.

### Co trzeba zrobić, żeby AUV się sprawdziło

Trzy kierunki pracy, każdy na osobne kilka tygodni:

**A — Akwizycja danych produkcyjnych.** Adaptery do:
- USGS Mineral Commodity Summaries (produkcja metali — często PDF/Excel, wymaga ręcznego parsowania)
- EIA International Energy Statistics (produkcja ropy/gazu/węgla — wymaga klucza API)
- USDA FAS/PSD (produkcja żywności per crop)
- Dane o cementie i stali z World Steel Association i CEMBUREAU

**B — Lepsze pre-processing.** Reguły:
- Wykrywanie i obsługa anomalii (nie tylko 25% skoków, ale też skoków stopniowych nielogicznych)
- Interpolacja między rocznymi punktami z uwzględnieniem sezonowości
- Walidacja krzyżowa między źródłami (jeśli USGS i USDA mówią co innego, którego słuchać)

**C — Wagowanie kategorii.** Metoda:
- Udział kategorii w światowym PKB (USDA dla rolnictwa, IEA dla energii, World Steel dla budownictwa)
- Ewentualnie ważenie *wartością produkcji* (cena × ilość) zamiast samym wolumenem
- Test wrażliwości na inne wagi

### Eksperymenty, które warto przeprowadzić samodzielnie

Zanim ruszy się z pełną v0.4, dobrze byłoby przemyśleć:

1. **Jak wyglądałby AUV dla jednej kategorii?** Np. tylko żywność, tylko energia, tylko metale. To by pokazało, która kategoria niesie najwięcej zmienności i czy jest sens je łączyć.

2. **Co się dzieje, jak zmieniamy populację na produktywną populację (15–65 lat)?** Mianownik zmienia się znacząco, bo udział populacji produktywnej spada (starzenie się społeczeństwa). Czy to zmienia wynik istotnie?

3. **Test stabilności wag.** Jeśli zmienimy wagi z 30/40/30 na 20/50/30, jak bardzo zmienia się wynikowy AUV? Jeśli niewiele — dobre, jeśli dużo — sygnalizuje, że projekt jest zbyt wrażliwy na arbitralne wybory.

### Świadome ograniczenia AUV

AUV nie pokaże:

- Czy decyzje bankowe konkretnego dnia są dobre czy złe (FDI to robi).
- Wartości aktywów finansowych (akcji, obligacji).
- Jakości życia poza zasobami materialnymi (zdrowie, edukacja, środowisko).

AUV to *miernik fizycznej wartości cywilizacji*, nie *miernik dobrobytu*.

---

## Relacja Między Projektami

### Co dzielą

- **Infrastrukturę kodu**: `prototyp/src/sources/*.py` (FRED, ECB, NBP, World Bank, Yahoo) jest wspólny.
- **Dane wejściowe**: 71 serii w `monthly.parquet` zawiera wszystko, co potrzebne dla obu projektów.
- **Filozofię**: heliocentryzm, otwarte dane, deterministyczne formuły, brak pojedynczych punktów awarii (patrz `PROFIL_AUTORA.md`).

### Czym się różnią

| Cecha | FDI | AUV |
| --- | --- | --- |
| Cel | Deprecjacja fiat-u | Realna wartość cywilizacji |
| Składniki | CPI, M2, dług, SDR | Surowce, produkcja, populacja |
| Dane | W pełni dostępne dziś | Częściowo dostępne |
| Dojrzałość | Gotowy do implementacji | Wymaga jeszcze pracy badawczej |
| Zastosowanie | Kredyty, umowy wieloletnie | Polityka publiczna, analiza długoterminowa |
| Stabilność | Wysoka (gładki wzrost) | Niska (szoki surowcowe) |
| Wytłumaczalność | Bardzo wysoka | Wymaga zrozumienia formuły |

### Jak rozumieć ich wzajemną relację

FDI mierzy *jak fiat traci wartość*. AUV mierzy *jak realne zasoby stają się rzadsze lub obfitsze*. Idealnie te dwa procesy są niezależne — FDI rośnie z ekspansją monetarną i kredytową, AUV rośnie albo spada w zależności od postępu technologicznego i demograficznego.

W praktyce są skorelowane, bo ekspansja monetarna podnosi nominalne ceny surowców, które wchodzą do AUV. Ale FDI mierzy *średnią* deprecjację fiat-u, a AUV pokazuje, gdzie *odchylenia* od tej średniej się ujawniają — np. szok energetyczny po inwazji Rosji na Ukrainę był widoczny w AUV (silny wzrost), ale słabszy w FDI (bo CPI zareagowało wolniej i częściowo).

Razem dają obraz pełniejszy niż każdy z osobna: FDI pokazuje "ile zostało zdeprecjonowane", AUV pokazuje "jaka jest realna sytuacja zasobowa".

---

## Słownik Pojęć (z poprawioną terminologią)

**Kreacja pieniądza** — proces, w którym powstaje nowy pieniądz. We współczesnym systemie odbywa się przede wszystkim przez:
- *Kredyt komercyjny*: gdy bank udziela pożyczki, tworzy nowy pieniądz depozytowy w księgach. Dominujący kanał kreacji pieniądza w gospodarce.
- *Operacje banku centralnego*: luzowanie ilościowe (QE), skup obligacji, kreacja rezerw bankowych. To procesy księgowe, nie fizyczne drukowanie.
- *Kreacja długu publicznego*: pożyczki państwowe tworzą instrumenty finansowe, które funkcjonują w systemie jako pieniądz.

**Ekspansja monetarna** — wzrost agregatów monetarnych (M2, M3) w czasie. Suma efektu kreacji kredytowej i operacji banku centralnego.

**Inflacja konsumencka (CPI)** — wzrost cen koszyka dóbr konsumenckich. Skutek ekspansji monetarnej *po stronie konsumentów*. Mierzona przez urzędy statystyczne.

**Inflacja aktywów** — wzrost cen aktywów finansowych (akcji, obligacji, nieruchomości). Skutek ekspansji monetarnej *po stronie kapitału*. Nie wchodzi do oficjalnego CPI.

**Deprecjacja fiat-u** — utrata siły nabywczej pieniądza papierowego w czasie. Skutek netto kreacji pieniądza minus realnego wzrostu produkcji.

**M2 / M3** — agregaty pieniężne. M2 obejmuje gotówkę, depozyty na żądanie i depozyty terminowe. M3 dodaje większe instrumenty pieniężne (np. fundusze rynku pieniężnego).

**Dług publiczny do PKB** — stosunek całkowitego zadłużenia rządu do rocznego PKB. Wskaźnik strukturalnej presji inflacyjnej w przyszłości.

**SDR (Special Drawing Rights)** — jednostka rachunkowa MFW, koszyk pięciu walut (USD, EUR, CNY, JPY, GBP) z wagami rewidowanymi co pięć lat.

**Heliocentryczność** — w kontekście tego projektu: właściwość systemu, którego wyniki zależą wyłącznie od obserwowalnych, weryfikowalnych danych, a nie od decyzji jakichkolwiek autorytetów (rad nadzorczych, banków centralnych, urzędów statystycznych).

**Konsensus G5** — średnia ważona PKB pięciu największych walut światowych (USA, strefa euro, Japonia, Wielka Brytania, Szwajcaria). Używana w FDI jako odniesienie "typowej" deprecjacji fiat-u.

---

## Co Dalej

Niniejszy dokument zostaje jako kotwica koncepcyjna. Następne kroki:

1. **Autor przeprowadza samodzielnie eksperymenty wskazane w sekcjach "Eksperymenty"** — żeby zbudować intuicję, jak każdy komponent się zachowuje. Dane są już pobrane, narzędzia są gotowe, wystarczy uruchamiać nowe komórki Jupyter w istniejących notebookach lub pisać własne skrypty.

2. **Po zakończeniu eksperymentów** — decyzja, czy ruszamy z implementacją FDI w pełnej formie. Wymagałoby to napisania `src/fdi.py` (analogicznie do `src/auv_v3_hybrid.py`) i nowego notebooka walidacyjnego.

3. **AUV pozostaje w fazie badawczej.** Bez nowych źródeł danych produkcyjnych (USGS, EIA, USDA) projekt nie jest gotowy do pełnej implementacji. Sensowne jest odłożenie go do v0.4, po ustabilizowaniu FDI.

Dokument otwarty na rewizję. Wszystkie liczby (wagi, identyfikatory, źródła) są propozycjami do dyskusji, nie ostatecznymi decyzjami.
