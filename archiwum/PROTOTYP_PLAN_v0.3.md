# AUV — Plan Prototypu v0.3

**Projekt:** Bezwzględna Jednostka Wartości (Absolute Unit of Value, AUV)
**Wersja:** 0.3
**Status:** Zatwierdzona koncepcja, plan implementacji
**Kontekst:** Trzecia iteracja podejścia do projektu, oparta na wnioskach z empirycznej weryfikacji wersji v0.2. Dokument self-contained — można go przekazać dowolnej osobie lub asystentowi AI bez utraty kontekstu i kontynuować pracę.

---

## Streszczenie Wykonawcze

AUV (Absolute Unit of Value, Bezwzględna Jednostka Wartości) to publicznie publikowana jednostka rachunkowa wyliczana algorytmicznie z otwartych danych rynkowych i fizycznych. Nie jest walutą w sensie środka wymiany — jest **miarą wartości**, służącą do oceny realnej, oczyszczonej z inflacji monetarnej wartości innych walut, surowców i aktywów.

W wersji v0.3 koncepcja przyjmuje nową, znacznie czystszą formę. AUV jest definiowane jako **koszt utrzymania ludzkiej cywilizacji na obecnym poziomie technologicznym, mierzony w realnych zasobach fizycznych**. Wskaźnik wzrasta wtedy, kiedy konsumpcja zasobów wyprzedza ich produkcję per capita. Spada wtedy, kiedy postęp technologiczny lub rozwój produkcji wyprzedza zwiększające się potrzeby ludzkości. Stoi w miejscu wtedy, kiedy oba procesy się równoważą.

Formuła podstawowa, dla każdego z 15–20 kluczowych zasobów:

> **Realna wartość zasobu = cena × (potrzeba na osobę × populacja świata) / roczna produkcja**

AUV jest ważoną sumą tych realnych wartości w pięciu kategoriach: energia, żywność, budownictwo, metale przemysłowe, materiały krytyczne dla nowoczesnych technologii.

W przeciwieństwie do koszyków walutowych typu SDR (które są średnią z psujących się pieniędzy papierowych), AUV jest zakotwiczone w *fizycznej rzeczywistości*. W przeciwieństwie do oficjalnych wskaźników CPI (które zależą od arbitralnych decyzji urzędników statystycznych), AUV jest *deterministycznie wyliczalne z otwartych danych*.

---

## 1. Definicja AUV

### 1.1 Co to jest AUV

AUV to **jednostka rachunkowa** — narzędzie pomiaru i wyceny, nie środek wymiany. Funkcjonalnie zbliżone do chilijskiej Unidad de Fomento (która od 1967 roku służy w Chile do indeksowania kredytów hipotecznych), z dwiema kluczowymi różnicami:

- AUV jest *deterministycznie wyliczalne* z publicznych danych. Każdy dysponujący tymi samymi danymi otrzyma tę samą wartość AUV. Nie zależy od oficjalnych dekretów, decyzji rad nadzorczych, ani urzędów statystycznych.
- AUV jest *globalne i fizyczne* w swojej podstawie. Nie indeksuje koszyka konsumenckiego konkretnej gospodarki, tylko zasoby cywilizacyjne istotne dla całej ludzkości.

### 1.2 Co AUV NIE jest

AUV nie jest:
- Walutą w sensie środka wymiany. Nie da się nim płacić w sklepie (chociaż docelowo można zawierać umowy denominowane w AUV).
- Średnią ważoną kursów walut. To byłby SDR — koszyk pieniędzy papierowych, które wszystkie się rozcieńczają.
- Indeksem cen konsumenckich. CPI mierzy koszyk konsumencki danego kraju, AUV mierzy zasoby cywilizacyjne.
- Indeksem surowcowym jak GSCI czy CRB. Te są ważone wolumenem handlu, AUV jest ważone rzeczywistymi potrzebami ludzkości.
- Wynikiem ML "wyciągającego ukrytą wartość". Ta koncepcja została opuszczona po empirycznej weryfikacji v0.2.

### 1.3 Filozofia heliocentryczna

AUV jest projektowany zgodnie z **filozofią heliocentryczną** — termin, który w tym kontekście oznacza systemy, których wyniki zależą od obserwowalnych, weryfikowalnych danych, a nie od decyzji jakichkolwiek autorytetów (rad nadzorczych, banków centralnych, urzędów statystycznych).

Analogia: definicja metra przez prędkość światła w próżni jest heliocentryczna — każdy laborant z odpowiednim sprzętem potwierdzi tę samą długość metra. Definicja metra jako "długości pręta przechowywanego w Sèvres" była antropocentryczna — zależała od fizycznego obiektu pod kontrolą francuskiej instytucji.

W ekonomii dzisiejszy świat opiera się prawie wyłącznie na antropocentrycznych miernikach: WIBOR jest ustalany decyzją kilku banków, CPI metodologią urzędu statystycznego, stopy procentowe głosowaniem rady polityki pieniężnej. AUV proponuje alternatywę — miernik, którego nikt nie kontroluje, bo wynika z matematyki i obserwowalnych faktów.

---

## 2. Geneza Koncepcji — Ewolucja Myślenia

### 2.1 Wersja v0.1 (porzucona)

Pierwsze podejście zakładało, że uczenie maszynowe (autoenkodery, PCA) może "wyciągnąć" ukrytą zmienną wartości z wielowymiarowych danych rynkowych. Hipoteza: jeśli karmimy model cenami surowców, kursami walut i agregatami pieniężnymi, model znajdzie wymiar reprezentujący "prawdziwą wartość" oczyszczoną z monetarnego szumu.

Wczesna analiza pokazała fundamentalny problem matematyczny. Jeśli wszystkie zmienne wejściowe są zdenominowane w pieniądzu papierowym, to każda ich kombinacja również. Pierwsza składowa PCA na takich danych jest *globalnym trendem inflacyjnym*, a nie "prawdziwą wartością". Próba minimalizacji wariancji w przestrzeni cen nie produkuje miernika niezależnego od ekspansji monetarnej — daje co najwyżej *najmniej zmienny koszyk*, ale ten koszyk wciąż jest skażony inflacją.

### 2.2 Wersja v0.2 (zaimplementowana, częściowo udana)

Drugie podejście, oparte na procedurze Frischa-Waugha-Lovella (FWL) plus optymalizacji kwadratowej (QP). Logika: dla każdego surowca regresujemy log-poziomy ceny na log-poziomy M2/M3 głównych walut, otrzymując reszty reprezentujące "realny" komponent ceny. Następnie QP znajduje wagi minimalizujące wariancję ważonej sumy tych reszt.

Wersja v0.2 została zaimplementowana w Pythonie. Pipeline pobierający 31 serii czasowych z czterech publicznych źródeł (FRED, NBP, ECB, Yahoo) działa. Wagi zostały wyznaczone. AUV(t) został wyliczony za okres 1996–2025.

Wyniki empiryczne ujawniły dwie kluczowe rzeczy. Pierwsza — techniczna: cztery agregaty M2/M3 są silnie współliniowe, więc współczynniki β z regresji wielokrotnej balonują do nierealistycznych wartości (±8 zamiast oczekiwanego ~1). Druga — koncepcyjna: na 30-letnim horyzoncie AUV i M2_USA kończą w tym samym miejscu. Linia AUV oscyluje wokół M2, ale długoterminowy trend jest ten sam.

Z autorem projektu nastąpiła kluczowa wymiana zdań. Pierwsza interpretacja (Claude): "AUV nie uciekł od M2, metoda zawiodła". Druga interpretacja (autor): "AUV ma rosnąć tyle, ile dolar się rozcieńcza — to jest dokładnie to, co chcieliśmy zobaczyć". Druga interpretacja jest poprawna. AUV jako jednostka *stała* w terminach realnych musi rosnąć w wartości nominalnej dokładnie wtedy, kiedy waluty papierowe tracą wartość. Brak takiej zgodności oznaczałby właśnie błąd.

To rozróżnienie otworzyło drogę do v0.3, ale jednocześnie pokazało słabość metody FWL+QP — jest zbyt skomplikowana, niewytłumaczalna laikowi, i nie daje istotnie więcej niż prosta konstrukcja oparta na fundamentach.

### 2.3 Wersja v0.3 (obecna) — odwrócenie paradygmatu

Zamiast *wyciągać* AUV z surowych cen przez ML, *konstruujemy* AUV od podstaw z trzech obserwowalnych liczb dla każdego zasobu: ceny, rocznej produkcji, potrzeby na osobę. Plus populacja świata jako mianownik dla rzeczy, których nie da się skalować z populacją (przede wszystkim ziemi).

To przejście od "ekstrakcji ukrytej wartości" do "konstrukcji wartości z fundamentów" jest rewolucją koncepcyjną. Rezygnuje z aspiracji "znalezienia czegoś, czego dotąd nie widzieliśmy" na rzecz "zorganizowania tego, co już widać". Zyskuje na wytłumaczalności, prostocie, audytowalności i odporności na podważanie.

### 2.4 Kluczowe wnioski z całej drogi

Wnioski zebrane w trakcie iteracji od v0.1 do v0.3, które przeniesione do v0.3 stanowią jej fundament:

- **Waluty są w 60–70% jednym sygnałem.** Empiryczna analiza pokazała, że ~60% zmienności wszystkich walut da się wyjaśnić jednym wspólnym czynnikiem ("siła dolara"). Mając 18 walut, mamy realnie 3–4 niezależne informacje. Wystarczy USD jako roboczy pieniądz.
- **Nie da się uciec od fiat, mając tylko fiat.** Dowolna kombinacja walut papierowych jest też walutą papierową. Anchor musi być fizyczny.
- **Surowce mają indywidualną historię (szoki podażowe), ale długoterminowo śledzą M2.** Ten ostatni efekt to nie wada — to *właśnie* deprecjacja pieniądza wobec realnej wartości, którą chcemy mierzyć.
- **Wytłumaczalność jest twardym wymogiem.** Każda osoba z średnim wykształceniem powinna zrozumieć formułę w pięć minut. To wyklucza sieci neuronowe, skomplikowane regresje wielokrotne, czarne skrzynki.
- **Model musi móc ewoluować deterministycznie.** Świat się zmienia (AI, nowe technologie), ale zasady zmiany muszą być z góry znane i mechanicznie stosowane.

---

## 3. Matematyka AUV v0.3

### 3.1 Formuła podstawowa

Dla każdego zasobu *i* w koszyku, w czasie *t*:

```
realna_wartość_i(t) = p_i(t) × R_i(t) × N(t) / q_i(t)
```

gdzie:
- `p_i(t)` — cena zasobu *i* w dolarach amerykańskich (jednostka zależna od zasobu: USD/baryłka, USD/tona, USD/MWh itp.)
- `R_i(t)` — potrzeba na osobę na rok (np. kg żelaza na osobę rocznie, kalorie na osobę dziennie razy 365)
- `N(t)` — populacja świata
- `q_i(t)` — globalna roczna produkcja zasobu *i* (w jednostkach kompatybilnych z R_i)

Jednostki: `p × R × N / q = (USD/jednostka) × (jednostka/osoba/rok) × (osoba) / (jednostka/rok) = USD` — czyli wynik jest w dolarach.

Następnie:

```
AUV(t) = Σ w_i × realna_wartość_i(t)  ÷  AUV_baseline_at_t_0  × 100
```

Wagi `w_i` są nieujemne, sumują się do 1, są ustalone według reguły jawnej z góry (sekcja 4.2). Dzień bazowy `t_0` ustalany jest jednorazowo dla normalizacji do AUV = 100.

### 3.2 Interpretacja każdego składnika

**Cena (p)** odzwierciedla wszystko, co rynek wie o zasobie w danym momencie: monetarną inflację, lokalne szoki podażowe, sentyment, spekulację. To "widoczna" cena giełdowa, której nie próbujemy przefiltrować.

**Potrzeba na osobę (R)** to fizyczne lub funkcjonalne zużycie zasobu przeciętnym mieszkańcem Ziemi na rok. Dla żywności jest fizjologiczna (kalorie, białko). Dla materiałów budowlanych funkcjonalna (cement na infrastrukturę). Dla materiałów technologicznych pochodna stylu życia (krzem na elektronikę, lit na baterie). Wartość R zmienia się powoli, ale *zmienia się* — gdy ludzkość przechodzi do AI, R dla GPU rośnie; gdy odkrywamy lepsze materiały, R dla starych spada.

**Populacja świata (N)** to ile osób potrzebuje danego zasobu. Rosnąca populacja oznacza większe zagregowane zapotrzebowanie. Jest też mianownikiem dla rzeczy nieskalowalnych (ziemia, wybrzeże, woda słodka).

**Produkcja roczna (q)** to ile zasobu globalna gospodarka faktycznie wyprodukowała w danym roku. Obejmuje wydobycie pierwotne, recykling, syntezę, w zależności od zasobu.

Iloczyn `R × N` to *zagregowana potrzeba świata* na rok. Stosunek `R × N / q` to *współczynnik niedoboru* — jeśli mniejszy od 1, produkujemy więcej, niż potrzebujemy (nadwyżka, ceny pod presją); jeśli większy od 1, produkujemy mniej, niż potrzebujemy (niedobór, ceny w górę). Mnożenie przez cenę przekłada to na wymiar pieniężny dla agregacji.

### 3.3 Przykład liczbowy

Załóżmy miedź w roku 2025 z fikcyjnymi (przykładowymi) liczbami:

- p = 9000 USD/tona
- R = 3 kg miedzi na osobę rocznie (typowo: 2,5–3,5)
- N = 8,1 miliarda osób
- q = 22 miliony ton globalnej produkcji

Wtedy:
```
R × N = 3 kg/osoba × 8 100 000 000 osób = 24 300 000 000 kg = 24,3 miliona ton (potrzeba świata)
R × N / q = 24,3 / 22 = 1,10 (potrzebujemy 10% więcej, niż produkujemy)
realna_wartość_miedzi = 9000 × 1,10 = 9900 USD/tona
```

Dla porównania 1996 z fikcyjnymi liczbami:
- p = 2500 USD/tona
- R = 2,5 kg/osoba (mniej elektroniki, mniej OZE, mniej elektroniki konsumenckiej)
- N = 5,8 miliarda
- q = 11 milionów ton

```
R × N = 2,5 × 5 800 000 000 = 14,5 miliona ton
R × N / q = 14,5 / 11 = 1,32
realna_wartość = 2500 × 1,32 = 3300
```

Wzrost realnej wartości miedzi z 3300 do 9900 to 3-krotny przyrost. W tym czasie M2 USA wzrósł ~5,5×. Czyli miedź realnie *staniała* o 40% wobec dolara — co intuicyjnie odpowiada faktowi, że produkcja miedzi dwukrotnie przyspieszyła a popyt na osobę wzrósł tylko o 20%.

---

## 4. Skład Koszyka AUV

### 4.1 Pięć kategorii zasobów

Koszyk pokrywa pięć kategorii odpowiadających różnym warstwom utrzymania cywilizacji:

**Energia** (ok. 25% wagi). Energia jest fundamentalnym kosztem każdej innej produkcji. Wszystko, co robimy, wymaga energii: wydobycie surowców, transport, produkcja, ogrzewanie. Zawiera: ropę naftową (kompozyt Brent/WTI/Dubai), gaz ziemny (Henry Hub + TTF), węgiel energetyczny, uran.

**Żywność** (ok. 20% wagi). Bez kalorii nie ma cywilizacji. Zawiera: pszenicę, ryż, kukurydzę, soję, mięso (proxy: wieprzowinę i wołowinę), oleje roślinne. Mierzona w przeliczeniu na kalorie i białko per capita.

**Materiały budowlane** (ok. 20% wagi). Infrastruktura: drogi, mosty, budynki, mieszkania. Zawiera: cement, stal zbrojeniową, drewno konstrukcyjne, szkło budowlane, miedź instalacyjną.

**Metale przemysłowe** (ok. 20% wagi). Produkcja dóbr trwałych: maszyn, pojazdów, urządzeń. Zawiera: stal węglową, aluminium, miedź (przewody), nikiel, cynk.

**Materiały krytyczne dla nowoczesnej technologii** (ok. 15% wagi). Wymagania współczesnej elektroniki i transformacji energetycznej. Zawiera: lit (baterie), kobalt (baterie), ziemie rzadkie (silniki, elektronika), pallad i platyna (katalizatory), krzem czysty (półprzewodniki).

### 4.2 Wagi w koszyku

Wagi pomiędzy kategoriami są ustalane na podstawie *udziału kategorii w fizycznym przepływie cywilizacyjnym*, mierzonym w przybliżeniu wartością światowej produkcji danego sektora. Wagi *wewnątrz kategorii* są proporcjonalne do realnych wartości każdego zasobu (powyższy iloczyn p × R × N / q) uśrednionych z ostatnich pięciu lat.

To podejście jest po części arbitralne — można zaproponować inne uzasadnienia wag. Kluczowe jest, że wagi są:
- Wyliczane z otwartych danych (nie ustalane decyzją)
- Publikowane jawnie
- Rewidowane raz na pięć lat zgodnie z procedurą określoną w sekcji 7

### 4.3 Lista konkretnych zasobów w v0.3

Pierwsza iteracja (v0.3.1) pokrywa 18 zasobów:

**Energia (4):** ropa naftowa Brent, gaz ziemny TTF, węgiel energetyczny Newcastle, uran U3O8.

**Żywność (5):** pszenica HRW, ryż 5% broken, kukurydza paszowa, soja, oleje roślinne (palmowy jako benchmark).

**Budownictwo (3):** cement portlandzki, stal zbrojeniowa (rebar HRB400), drewno konstrukcyjne (lumber).

**Metale przemysłowe (3):** miedź LME, aluminium LME, ruda żelaza Tianjin.

**Materiały krytyczne (3):** węglan litu, kobalt LME, krzem metaliczny.

Druga iteracja (v0.3.2, w późniejszych miesiącach) doda jeszcze do 5 zasobów, w tym: ziemie rzadkie, palladium, krzem solarny, ewentualnie wodę słodką jako oddzielny składnik.

---

## 5. Dane Wejściowe

### 5.1 Cena (p_i)

Częstotliwość: dzienna lub miesięczna w zależności od dostępności.

Źródła:
- **FRED** (Federal Reserve Bank of St. Louis) dla większości surowców notowanych globalnie. Bezpłatny API z kluczem.
- **World Bank Pink Sheet** dla zharmonizowanych miesięcznych cen surowców.
- **IMF Primary Commodity Prices** dla rzadszych zasobów.
- **EIA** (US Energy Information Administration) dla detalicznych cen energii.
- **USGS Mineral Commodity Summaries** dla cen metali krytycznych w ujęciu rocznym.

Każdy zasób będzie miał *co najmniej dwa* niezależne źródła, by uniknąć pojedynczych punktów awarii (np. wycofania serii z FRED, jak miało miejsce z złotem LBMA w v0.2).

### 5.2 Produkcja roczna (q_i)

Częstotliwość: roczna, w niektórych przypadkach kwartalna.

Źródła:
- **USGS Mineral Commodity Summaries** (publikacja roczna, styczeń) dla wszystkich metali — historia od ~1900.
- **EIA International Energy Outlook + Annual Energy Outlook** dla energii.
- **FAO FAOSTAT** dla żywności — globalna produkcja per crop.
- **USDA WASDE** (World Agricultural Supply and Demand Estimates) — miesięczne raporty z prognozami i estymatami.
- **World Steel Association** dla stali.
- **CRU, Wood Mackenzie reports** dla metali krytycznych (część płatna, część open access).
- **United Nations Industrial Development Organization (UNIDO)** dla materiałów budowlanych.

### 5.3 Potrzeba na osobę (R_i)

Częstotliwość: rewizja co 5 lat lub po istotnym wydarzeniu technologicznym/cywilizacyjnym.

Sposób wyznaczenia: *średnia światowa konsumpcja per capita* w ostatnich 5 latach (zużycie krajowe = produkcja + import − eksport, sumowane globalnie).

Źródła:
- **USGS Mineral Yearbook** publikuje "apparent consumption" per kraj dla każdego metalu.
- **IEA World Energy Balances** dla energii (kWh per capita per kraj).
- **FAOSTAT Food Balance Sheets** dla żywności (kalorie i białko per capita per kraj).
- **UN Population Division** dla bazy populacyjnej.

Dla zasobów, dla których nie ma czystych danych o konsumpcji (np. krzem do półprzewodników), używa się produkcji jako proxy konsumpcji (w długim okresie te dwie wartości są równe w skali globalnej).

### 5.4 Populacja świata (N)

Częstotliwość: dzienna interpolacja na bazie rocznych estymatów.

Źródło: **UN Population Division — World Population Prospects** (publikacja co dwa lata, dane roczne historyczne i prognozy do 2100).

Alternatywne źródło: **World Bank Population Data**.

### 5.5 Częstotliwości i opóźnienia — implikacje dla publikacji AUV

Z uwagi na to, że dane produkcyjne są roczne z opóźnieniem 6–18 miesięcy, AUV nie może być w pełni "live". Konstrukcja:

- **Komponent cenowy aktualizuje się dziennie** (z głównych giełd).
- **Komponent produkcyjny aktualizuje się raz w roku** w styczniu, kiedy USGS publikuje Mineral Commodity Summaries. Pomiędzy aktualizacjami stosujemy ostatnią znaną produkcję plus linearną ekstrapolację z trendu.
- **Komponent potrzeby per capita rewidowany co 5 lat**, w cyklu raportowym ONZ Sustainable Development Goals.
- **Populacja interpolowana liniowo** między rocznymi punktami UN.

To znaczy, że AUV ma codzienną granulację dla użytkowników finansowych (umowy mogą odwoływać się do dnia roboczego), ale fundamentalne zmiany są kwartalne lub roczne.

---

## 6. Konsekwencje Interpretacyjne AUV

### 6.1 AUV rośnie — co to oznacza

Trzy możliwe przyczyny, każda znacząca:

1. **Pieniądz papierowy się rozcieńcza** — komponent cenowy `p` rośnie, podczas gdy fizyczna podaż `q` nie nadąża. To klasyczna inflacja monetarna.
2. **Zapotrzebowanie cywilizacji rośnie szybciej niż produkcja** — komponent `R × N / q` rośnie. To może być wzrost populacji bez wzrostu wydajności (presja demograficzna), lub nowa technologia wymagająca nowych materiałów (AI → GPU → krzem, lit).
3. **Wystąpił szok podażowy** — wojna, embargo, kataklizm naturalny. `q` spada gwałtownie, `p` rośnie, AUV podskakuje.

Te trzy przyczyny mają różne implikacje polityczne i społeczne. Same w sobie AUV ich nie rozróżnia — ale w połączeniu z osobnymi seriami (M2, populacja, produkcja) można zinterpretować, *która* z tych przyczyn dominuje.

### 6.2 AUV spada — co to oznacza

Również trzy możliwe przyczyny:

1. **Postęp technologiczny przewyższa wzrost potrzeb** — produkcja rośnie szybciej niż R × N. To jest *rzeczywista deflacja produktywności* — najbardziej pożądany scenariusz cywilizacyjny.
2. **Odkrycie nowych zasobów** — geologiczne lub geograficzne. Nowe złoże litu, nowa technologia ekstrakcji rzadkich pierwiastków.
3. **Recesja popytowa** — gospodarka konsumuje mniej z powodu kryzysu finansowego, demograficznego lub zdrowotnego. Ten przypadek bywa mylący w krótkim okresie, ale długoterminowo trend AUV powinien być pozytywny dla cywilizacji.

### 6.3 AUV stoi w miejscu — co to oznacza

Postęp technologiczny dokładnie równoważy wzrost zapotrzebowania. Cywilizacja "trzyma się" na obecnym poziomie. Pieniądz papierowy traci wartość proporcjonalnie do produkcji. Wszystkie procesy są w równowadze.

Jest to ciekawa, ale rzadka sytuacja. Historycznie AUV wahałby się — przyspieszały okresy szybkiego wzrostu (1900–1960, 1990–2010), spowalniały podczas wojen, kryzysów i pandemii.

---

## 7. Reguły Ewolucji Modelu

### 7.1 Dodawanie nowych zasobów

Nowy zasób trafia do koszyka, jeśli spełnia *jednocześnie* trzy warunki:

1. **Globalna produkcja wartościowo przekracza 5 mld USD rocznie** — czyli zasób ma realną wagę w gospodarce.
2. **Konsumpcja per capita wzrosła co najmniej dwukrotnie w ciągu poprzedzających 10 lat** — czyli zasób stał się "potrzebą cywilizacyjną" w ostatniej epoce.
3. **Istnieje publicznie dostępne, ciągłe źródło danych o produkcji i cenie** — przynajmniej miesięczne, z co najmniej 5-letnią historią.

Reguła jest jawna z góry. Każdy może sprawdzić, czy nowy zasób kwalifikuje się.

Przykład: w 2026 trzeba rozważyć dodanie *mocy obliczeniowej GPU* jako zasobu cywilizacyjnego. Produkcja chipów AI przekroczyła 100 mld USD rocznie (warunek 1 spełniony), zapotrzebowanie na osobę wzrosło co najmniej dziesięciokrotnie od 2018 (warunek 2 spełniony), dane o produkcji są dostępne przez raporty branżowe (warunek 3 do zweryfikowania). Decyzja: prawdopodobnie tak, w v0.4.

### 7.2 Usuwanie obsolete zasobów

Zasób wypada z koszyka, jeśli spełnia *jednocześnie* dwa warunki:

1. **Globalna produkcja wartościowo spadła poniżej 1 mld USD rocznie** — zasób stał się ekonomicznie marginalny.
2. **Konsumpcja per capita spada przez co najmniej 10 lat z rzędu** — zasób przestaje być "cywilizacyjnie potrzebny".

Albo jeśli:

3. **Źródło danych przestaje publikować przez ponad 24 miesiące** — utracona obserwowalność uniemożliwia uczciwe wycenianie.

### 7.3 Rewizja wag

Wagi pomiędzy kategoriami są rewidowane raz na 5 lat na podstawie tej samej procedury, według której zostały pierwotnie wyznaczone. Wagi *wewnątrz kategorii* są przeliczane automatycznie co roku, gdy aktualizują się dane o produkcji.

### 7.4 Procedura audytu

Każda zmiana składu koszyka lub wag jest:
- Ogłaszana publicznie z minimum 6-miesięcznym wyprzedzeniem.
- Uzasadniana w pełni z odwołaniem do konkretnych liczb i konkretnych reguł.
- Archiwizowana w repozytorium projektu z timestampem.

Stary skład pozostaje równolegle publikowany przez minimum 12 miesięcy po wprowadzeniu nowego, żeby umożliwić użytkownikom AUV adaptację umów i kontraktów.

---

## 8. Zastosowania AUV

### 8.1 Indeks rachunkowy

Najbardziej oczywiste zastosowanie: AUV jako waluta rachunkowa dla wielomilionowych aktywów i umów wieloletnich. Cena nieruchomości, wartość kapitału firmy, wartość portfela emerytalnego — wszystko można wyrazić w AUV i porównywać przez dziesięciolecia bez zniekształceń inflacyjnych.

### 8.2 Pożyczki bez ryzyka inflacyjnego

Najbardziej rewolucyjne zastosowanie. Klasyczny kredyt:

> Pożyczam 100 000 PLN, oddaję 100 000 PLN plus odsetki według WIBOR + 2,5%.

Jest grą o przyszłą inflację. Bank zarabia, jeśli inflacja okaże się niższa od WIBOR-u (kredytobiorca przepłaca). Kredytobiorca zarabia, jeśli inflacja przekroczy WIBOR (bank traci realną wartość). Obie strony grają przeciwko sobie.

Kredyt w AUV:

> Pożyczam 30 000 AUV, oddaję 30 000 AUV plus 2% rocznie marży.

Nie jest grą o nic. Obie strony wiedzą, że AUV trzyma realną wartość — kredytobiorca oddaje dokładnie tę samą siłę nabywczą, jaką pożyczył, plus uczciwą prowizję za czas i ryzyko. Bank nie traci na inflacji. Kredytobiorca nie przepłaca z powodu inflacyjnych panik. To czysty, uczciwy kredyt.

Wzorzec ten od 1967 roku działa w Chile (Unidad de Fomento). AUV byłby UF globalnym, niezależnym od oficjalnej statystyki państwowej, opartym na realnych zasobach cywilizacyjnych.

### 8.3 Wycena aktywów wieloletnich

Plany emerytalne, polisy na życie, długoletnie kontrakty wynajmu — wszystko, co dzisiaj jest "wartością mglistą" za 20–30 lat, można uściślić, denominując w AUV. Klient widzi, na co realnie może liczyć w roku 2050, niezależnie od tego, co się stanie z dolarem czy złotym.

### 8.4 Wskaźnik wyprzedzający rynki finansowe

To jest wnikliwa obserwacja z naszej dyskusji, którą warto zachować. Po wybudowaniu wskaźnika AUV, samo *monitorowanie odchyłów poszczególnych składowych* dostarcza informacji predykcyjnej.

Jeśli realna wartość miedzi w naszym wzorze nagle rośnie szybciej niż średnia AUV, to znaczy, że albo produkcja zwalnia, albo potrzeba rośnie, albo cena reaguje na coś, czego inne surowce jeszcze nie widzą. W każdym z tych przypadków jest to *sygnał wyprzedzający* o nadchodzących ruchach na rynkach związanych — bo gdy miedź drożeje, zaraz drożeją kable elektryczne, instalacje fotowoltaiczne, infrastruktura.

Mechanizm jest taki sam jak w klasycznym "Doctor Copper" (miedź jako wyprzedzający wskaźnik koniunktury), ale rozszerzony na cały koszyk AUV i unormowany przez fundamentalne wielkości popytu/podaży. Inwestorzy używający AUV jako pulpitu monitorującego mieliby przewagę informacyjną nad rynkiem.

### 8.5 Polityka monetarna i fiskalna (długoterminowa wizja)

Docelowo, jeśli AUV się sprawdzi, mógłby pełnić rolę punktu odniesienia dla decyzji o:
- Realnej stopie procentowej (kredyt w AUV daje *prawdziwą* stopę naturalną).
- Wycenie świadczeń socjalnych w długim okresie.
- Ocenie skuteczności polityki monetarnej (czy bank centralny realnie utrzymuje siłę nabywczą).
- Indeksacji umów międzynarodowych, alimentów, opłat publicznych.

Adopcja wymagałaby społecznego zaufania i kilku lat udokumentowanej stabilności AUV. To jest aspiracja na 10–20 lat, nie na rok.

---

## 9. Wymogi Heliocentryczne

System musi spełniać następujące cechy w celu zachowania filozofii heliocentrycznej (patrz PROFIL_AUTORA.md):

1. **Wyłącznie otwarte dane.** Wszystkie źródła publiczne (FRED, USGS, EIA, FAO, USDA, UN, World Bank, IMF, BIS, ECB SDW). Wykluczone: Bloomberg, S&P Global Market Intelligence, IHS Markit, Refinitiv. Powód: gatekeeper psuje audytowalność.

2. **Determinizm formuły.** Każdy z tymi samymi danymi otrzyma tę samą wartość AUV.

3. **Brak pojedynczych punktów awarii.** Każdy zasób w koszyku ma co najmniej dwa niezależne źródła ceny i dwa źródła produkcji.

4. **Audytowalność.** Każdy krok obliczeniowy musi być jawny, opisany i odtwarzalny. Kod open-source na GitHubie.

5. **Procedura rewizji jawna z góry.** Warunki dodawania, usuwania składników i zmiany wag są zapisane w niniejszym dokumencie. Nie zmieniają się retrospektywnie.

6. **Brak ludzkiej uznaniowości w obliczeniach.** Żaden krok między danymi wejściowymi a wynikową liczbą AUV nie wymaga decyzji człowieka.

---

## 10. Co Świadomie Wykluczamy

Z koszyka AUV: kryptowaluty (zbyt spekulacyjne, brak historii), złoto i srebro (silnie skorelowane z M2 jako aktywa anty-fiat, niezgodne z funkcją celu), indeksy giełdowe (zawierają silnie monetarny komponent), nieruchomości jako aktywo (zastąpione kosztem budowy nowego metra), waluty papierowe (skorelowane z USD, dodawały szum bez informacji).

Z całego projektu: wskaźniki ustalane przez ciała decyzyjne (oficjalne CPI, WIBOR, SOFR, stopy banków centralnych), dane subskrypcyjne, modele "czarnej skrzynki" bez jawnych współczynników, jakakolwiek uznaniowość po fakcie.

---

## 11. Świadome Ograniczenia v0.3

1. **Brak komponentu pracy ludzkiej** (godzina pracy w PPP). Pomysłowo interesujący, technicznie trudny do harmonizacji między krajami. Do v0.4.

2. **Brak regionalnej dyferencjacji "potrzeby na osobę"**. Używamy globalnej średniej (zużycie świata / populacja świata). Amerykanin zużywa wielokrotnie więcej, niż Bangladeszczyk, ale w pierwszej iteracji nie modelujemy regionów. Do v0.5.

3. **Brak modelowania substytucji.** Gdy miedź drożeje, aluminium ją zastępuje w przewodnictwie. Formuła traktuje je niezależnie. Akceptowalne, do v0.4–0.5.

4. **Brak modelowania recyklingu.** Stal jest w 80% recyklowana, miedź w 30%, lit prawie wcale. Używamy tylko produkcji pierwotnej (mining), co przeszacowuje rzeczywistą "produkcję" niektórych metali. Do v0.4.

5. **Brak ujęcia kosztu zewnętrznego (środowiskowego).** Wydobycie litu w Bolivii vs. czysta energetyka w Norwegii są wyceniane tak samo, mimo że ich wpływ ekologiczny jest dramatycznie różny. To jest świadomy wybór — AUV mierzy *ekonomiczną wartość*, nie *moralną*. Inny wskaźnik (np. ESG-AUV) mógłby to robić oddzielnie.

---

## 12. Kwestie Otwarte do Rozstrzygnięcia w v0.3.1

1. **Konkretne wagi pomiędzy pięcioma kategoriami.** Wstępna propozycja 25/20/20/20/15, ale uzasadnienie ekonometryczne wymaga doprecyzowania.

2. **Dzień bazowy `t_0`.** Kandydat: 2017-06-30 (z analizy z v0.2 jako najspokojniejszy okres). Do potwierdzenia po sprawdzeniu nowej formuły na danych.

3. **Procedura interpolacji rocznych danych produkcji na granulację miesięczną/dzienną.** Forward fill (ostatnia znana wartość) czy linearna ekstrapolacja z trendu? Trade-off między prostotą a aktualnością.

4. **Sposób uwzględnienia wielu źródeł ceny dla tego samego zasobu.** Średnia ważona wolumenem? Mediana? Najwyższa płynność?

5. **Definicja "potrzeby na osobę" dla rzeczy, dla których brak danych konsumpcyjnych.** Krzem do półprzewodników, ziemie rzadkie — używamy produkcji jako proxy, ale to nie jest idealne.

---

## 13. Plan Implementacji

### Faza 1 — Adaptery danych (3–4 dni roboty)
- Adapter UN Population API
- Adapter USGS Mineral Commodity Summaries (web scraping XLS lub PDF)
- Adapter FAO FAOSTAT (REST API)
- Adapter USDA WASDE (CSV downloads)
- Rozszerzenie istniejących adapterów FRED i ECB o nowe serie cenowe

### Faza 2 — Nowy moduł obliczeniowy (2 dni)
- `src/civilization_basket.py` — definicja zasobów, ich kategorii, jednostek i baseline'ów R_i
- `src/auv_v3.py` — implementacja formuły p × R × N / q i agregacji koszyka

### Faza 3 — Notebook walidacyjny (1 dzień)
- `notebooks/04_auv_v3_validation.ipynb` — porównanie nowego AUV z poprzednim z v0.2, z M2_USA, z głównymi walutami
- Wizualizacje pokazujące zachowanie AUV w kryzysach 2008, 2020, 2022

### Faza 4 — Wnioski empiryczne i ewentualne korekty
- Po obejrzeniu nowych wyników, decyzja o ewentualnych korektach wag, składu, formuły
- Konsolidacja wniosków do v0.3.2 lub przejście do v0.4

---

## 14. Słownik Pojęć

**AUV** — Absolute Unit of Value, Bezwzględna Jednostka Wartości. Jednostka rachunkowa definiowana jako koszt utrzymania ludzkiej cywilizacji na obecnym poziomie technologicznym, mierzony w realnych zasobach.

**Heliocentryczność** — w kontekście tego projektu: właściwość systemu, którego wyniki zależą wyłącznie od obserwowalnych, weryfikowalnych danych, a nie od decyzji jakichkolwiek autorytetów.

**Frisch-Waugh-Lovell (FWL)** — twierdzenie ekonometryczne, według którego współczynnik regresji na konkretną zmienną można uzyskać przez dwuetapową procedurę "ortogonalizacji". Używane w v0.2, porzucone w v0.3.

**M2/M3** — agregaty pieniężne. M2 to gotówka, depozyty bieżące i depozyty terminowe. M3 dodaje większe instrumenty pieniężne.

**SDR** — Special Drawing Rights MFW, koszyk pięciu walut (USD, EUR, CNY, JPY, GBP).

**UF** — Unidad de Fomento, chilijska jednostka rachunkowa indeksowana inflacją CPI, funkcjonująca od 1967 roku.

**Doctor Copper** — finansowy termin oznaczający, że cena miedzi historycznie wyprzedza zmiany w koniunkturze gospodarczej (bo miedź jest używana wszędzie, od elektroniki po budownictwo).

**Per capita** — na osobę. Dzielimy przez populację, by uzyskać wskaźnik niezależny od skali demograficznej.

---

## 15. Następne Kroki Bezpośrednio Po Zatwierdzeniu

1. Commit niniejszego dokumentu do repozytorium Git i push na GitHub.
2. Rozszerzenie `prototyp/src/config.py` o nowe serie danych (ceny + produkcja + nowe źródła).
3. Implementacja Faz 1–4 z sekcji 13.
4. Pierwsze uruchomienie AUV v0.3 na realnych danych.
5. Porównanie wyników z v0.2 — zobaczenie, czy nowa koncepcja daje wyraźnie inny (i lepszy) obraz.

---

*Wersja v0.3. Zatwierdzona po dyskusji ze współautorem. Dokument self-contained — może być przeniesiony do dowolnej innej dyskusji bez utraty kontekstu projektu.*
