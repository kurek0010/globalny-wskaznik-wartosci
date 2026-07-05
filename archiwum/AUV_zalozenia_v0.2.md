# AUV — Notatka Założeń v0.2

**Projekt:** Bezwzględna Jednostka Wartości (Absolute Unit of Value, AUV)
**Data:** 2026-05-28
**Status:** Założenia robocze, druga iteracja
**Kontekst:** Aktualizacja v0.1 po dyskusji o koszcie pracy, wyborze okresu bazowego i procedurze optymalizacji. Trzy spośród czterech "kwestii otwartych" z v0.1 zostały rozstrzygnięte.

---

## 1. Streszczenie

AUV to publicznie publikowana, codzienna jednostka rachunkowa wyliczana algorytmicznie z otwartych danych rynkowych. Nie jest walutą w sensie środka wymiany — jest *miarą*, służącą do oceny realnej (oczyszczonej z inflacji monetarnej) wartości innych walut, surowców i aktywów. Konstruowana zgodnie z filozofią heliocentryczną: bez zależności od decyzji jakiegokolwiek organu, bez subskrypcyjnych gatekeeperów danych, w pełni deterministyczna i odtwarzalna przez każdego.

Najbliższe istniejące analogie: SDR (Międzynarodowego Funduszu Walutowego) oraz chilijskie Unidad de Fomento — z tą różnicą, że AUV jest w pełni transparentne, multinarodowe w zasięgu i nie wymaga aktów politycznych do utrzymania.

## 2. Architektura Dwuwarstwowa

Projekt jest celowo podzielony na dwa równoległe poziomy o różnych celach i wymaganiach jakościowych.

**Warstwa CORE** to właściwy AUV — jednostka rachunkowa nadająca się do zastosowań kontraktowych (kredyty, umowy długoterminowe, indeksacje). Cechy nieprzekraczalne: prosta formuła weryfikowalna ręcznie, ok. 18–28 składników, w pełni transparentna, wynik jest jednoznaczną liczbą dla każdego dnia. Brak elementów uczenia maszynowego w warstwie produkcyjnej — ML służy wyłącznie do *jednorazowego* doboru wag, po czym wagi są fixowane na okres co najmniej 5 lat.

**Warstwa PRO** to rozszerzony produkt analityczny. Zawiera setki wskaźników, cechy interakcyjne, nieliniowe modele typu gradient boosting, detekcję anomalii. Służy inwestorom, badaczom i jako system wczesnego ostrzegania o szokach makroekonomicznych. **Nie pełni funkcji jednostki rozliczeniowej** — dlatego dopuszczalne jest tu większe ryzyko nadmiernego dopasowania (overfitting) w zamian za bogatszą informację analityczną.

Obie warstwy czerpią z tej samej bazy danych i pozostają w spójności metodologicznej. Rozwijane przez ten sam zespół, równolegle.

## 3. Skład Koszyka CORE

Składniki podzielone na pięć klas. Każdy składnik wymaga zasilenia z co najmniej dwóch niezależnych giełd/źródeł dla zapewnienia odporności na pojedyncze punkty awarii.

**Surowce energetyczne (częstotliwość: dzienna):** ropa Brent, ropa WTI, ropa Dubai, gaz ziemny TTF (Europa), gaz Henry Hub (USA), ceny spot energii elektrycznej z wybranych rynków (PJM, EEX, JEPX).

**Surowce żywieniowe (częstotliwość: dzienna):** pszenica (Chicago, Paryż, czarnomorska), kukurydza, ryż, soja, oleje roślinne (palmowy, sojowy), indeks cen żywności FAO jako agregat (miesięczna częstotliwość — uzupełnienie dla dziennych notowań).

**Metale przemysłowe (częstotliwość: dzienna):** miedź, aluminium, ruda żelaza, lit, nikiel. Plus kompromis dla nieruchomości jako proxy kosztu budowy nowego metra kwadratowego: cement, stal zbrojeniowa, drewno konstrukcyjne. Pominięcie cen mieszkań *per se* jest celowe — zbyt lokalne, zniekształcone przez politykę kredytową i pozwolenia na budowę.

**Logistyka i frachty (częstotliwość: dzienna):** Baltic Dry Index, Drewry Container Index (frachty kontenerowe).

**Komponent monetarny — waluty (częstotliwość: dzienna, intraday):** 15–25 walut dobranych nie po wolumenie obrotu, lecz po reprezentacji różnych reżimów monetarnych. Rezerwowe i safe haven: USD, EUR, JPY, GBP, CHF. Rynki wschodzące: CNY, INR, BRL, MXN. Region środkowoeuropejski: PLN, CZK, HUF. Wysokoinflacyjne (jako test odporności AUV w kryzysach walutowych): ZAR, TRY, ARS.

**Komponent czasowy — koszt pracy ludzkiej (częstotliwość: kwartalna):** mediana wynagrodzenia godzinowego skorygowana o parytet siły nabywczej (PPP) dla państw G20, agregowana z dwóch niezależnych źródeł: ILOSTAT (Międzynarodowa Organizacja Pracy) oraz OECD Labour Compensation per Hour Worked. Wprowadzenie tego komponentu zostało zdecydowane w v0.2 z uzasadnieniem: dane są systematycznie mierzone od dekad (Penn World Table sięga 1950 roku, BLS od 1947), metodologia jest dokumentowana i porównywalna międzynarodowo, a "czas pracy" stanowi fundamentalną kotwicę wartości niezależną od polityki monetarnej.

**Konsekwencja architektoniczna:** AUV staje się indeksem o *mieszanej częstotliwości*. Komponent surowcowy i walutowy aktualizuje się codziennie; komponent kosztu pracy raz na kwartał. Codzienna wartość AUV używa ostatniego znanego odczytu komponentu pracy (forward fill), z formalnym oznaczeniem dnia, w którym następuje rewizja. Technika łączenia danych o różnych częstotliwościach jest standardowa w ekonometrii makro (modele MIDAS).

## 4. Skład Warstwy PRO (Rozszerzenie)

Wszystkie składniki CORE plus dodatkowo:
- **Złoto i srebro** jako wskaźniki "anty-fiat" (silnie skorelowane z M2, używane do detekcji szoków zaufania do walut, nie do CORE).
- **Bitcoin i wybrane duże kryptowaluty** jako rezerwuar wartości skali bilionowej. Pomimo spekulacyjnego charakteru, skala wyklucza ich pominięcie w analizie — ujęte jednak wyłącznie w PRO, nie w CORE.
- **Główne indeksy giełdowe**: S&P 500, STOXX 600, Nikkei, MSCI Emerging Markets.
- **Agregaty pieniężne**: M2 USA, EUR, CNY (jednocześnie używane jako *funkcja celu* dla optymalizacji CORE — patrz sekcja 6).
- **Rentowności obligacji 10-letnich** (US10Y, Bund, JGB, oraz wybrane EM).
- **Spready CDS suwerennych** dla państw G20.
- **Cechy interakcyjne**: iloczyny i ratio (np. S&P × M2, miedź/złoto, ropa/pszenica).
- **Wskaźniki produktywności**: Total Factor Productivity (TFP) z Penn World Table.

Te zmienne służą detekcji anomalii i analizie strukturalnej, ale **nie wchodzą do formuły CORE**.

## 5. Formuła Matematyczna AUV (CORE)

Codziennie o godzinie odniesienia (kandydat: 17:00 czasu londyńskiego, po zamknięciu LME):

$$\text{AUV}(t) = \frac{\sum_{i=1}^{N} w_i \cdot p_i(t)}{\sum_{i=1}^{N} w_i \cdot p_i(t_0)} \cdot 100$$

gdzie $p_i(t)$ to cena $i$-tego składnika w wybranej walucie referencyjnej w dniu $t$, a $w_i$ to stałe wagi dobrane procedurą optymalizacji (sekcja 6).

**Dzień bazowy $t_0$ — procedura wyboru (zmiana względem v0.1):**

Zamiast arbitralnego ustalenia $t_0$ (poprzednio kandydatem był 1 stycznia 2026), $t_0$ wybierany jest po przeprowadzeniu analizy eksploracyjnej danych (Exploratory Data Analysis). Procedura:

1. Pozyskanie pełnych szeregów czasowych wszystkich składników CORE za ostatnie 30 lat (lub maksymalnie dostępne).
2. Identyfikacja momentów strukturalnych załamań reżimu — kandydaci do zaznaczenia: 1971 (koniec Bretton Woods), 1979–82 (dezinflacja Volckera), 1997 (kryzys azjatycki), 2008 (GFC), 2020 (COVID), 2022 (post-COVID inflation surge).
3. Wybór okresu bazowego w "spokojnym środku" — między załamaniami, w okresie niskiej zmienności wszystkich składników.
4. Kandydaci wstępni: 1996–1999, 2003–2006, 2015–2019.
5. Test wrażliwości: powtórzenie konstrukcji AUV dla kilku różnych $t_0$ i sprawdzenie, czy wyniki są podobne (oznaka stabilności wskaźnika).

Decyzja co do konkretnego $t_0$ zapada *po* obejrzeniu danych, nie z góry.

## 6. Funkcja Celu i Rola ML w Doborze Wag

Wagi $w_i$ są dobrane jednorazowo (z możliwością formalnej rewizji) jako rozwiązanie zadania optymalizacyjnego.

**Wybrana metoda: programowanie kwadratowe (Quadratic Programming, QP)** — rekomendacja sformalizowana w v0.2.

Sformułowanie problemu:

$$\min_{w} \; \text{Cov}\Big( \log \sum_i w_i p_i(t), \; \log M2(t) \Big)$$

przy ograniczeniach: $w_i \geq 0$ (niedopuszczanie wag ujemnych dla interpretowalności), $\sum w_i = 1$ (normalizacja).

W praktyce minimalizujemy kowariancję z agregatem obejmującym M2 USA, M2 strefy euro i M2 Chin — uśrednione lub jako zestaw ograniczeń typu "korelacja z każdym z osobna ≤ próg".

**Uzasadnienie wyboru QP:** Po pierwsze — transparentność. Każdy dysponujący tymi samymi danymi i tą samą funkcją celu otrzyma te same wagi; nie ma efektu losowej inicjalizacji jak w sieciach neuronowych. Po drugie — interpretowalność: ograniczenia są jawne i zrozumiałe ekonomicznie. Po trzecie — wykonalność: standardowa biblioteka Pythona (CVXPY) rozwiązuje problem w sekundach na 30-letnich danych historycznych.

**Walidacja krzyżowa metodą alternatywną:** Niezależnie przeprowadzamy konstrukcję wag metodą *analizy głównych składowych* (PCA) — wyciągamy komponenty wariancji niezależne od M2 i konstruujemy wagi proporcjonalne do ich obciążeń. Jeśli wagi QP i PCA są zbliżone, mamy wzajemne potwierdzenie metodologiczne. Jeśli rozbiegają się znacząco, sygnalizuje to problem strukturalny do dyskusji.

**Procedura rewizji wag:** Wagi są fixowane na **5 lat**. Rewizja wymaga formalnej procedury i publicznego ogłoszenia z wyprzedzeniem ≥ 6 miesięcy, na podstawie matematycznego kryterium (zmiana strukturalna w danych wykryta testem CUSUM lub podobnym), nie politycznego.

## 7. Wymogi Heliocentryczne (Wymagane Cechy Systemu)

- **Tylko otwarte dane**: FRED, ECB, IMF, BIS, publiczne API giełd (CME, ICE, LME, SHFE, COMEX, JPX), portale rządowe, ILOSTAT, OECD iLibrary, Penn World Table. Wykluczone: Bloomberg Terminal, S&P Global Market Intelligence, IHS Markit i podobne źródła subskrypcyjne.
- **Deterministyczna formuła**: każdy dysponujący tymi samymi danymi musi uzyskać tę samą wartość AUV.
- **Brak pojedynczych punktów awarii**: każdy surowiec powinien mieć cenę z co najmniej dwóch niezależnych giełd; awaria/manipulacja jednej nie psuje wskaźnika.
- **Audytowalność źródeł**: dla każdego punktu danych ma być jednoznacznie zdefiniowane, z jakiej giełdy, o której godzinie i z jakiego instrumentu pochodzi.
- **Publikacja open-source**: kod obliczeniowy, dane historyczne i pełna dokumentacja muszą być publicznie dostępne na repozytorium typu GitHub.
- **Procedura rewizji jawna**: warunki, w których zmieniają się wagi lub skład koszyka, są zapisane formalnie i nie pozostawiają miejsca na uznaniowość po fakcie.

## 8. Co Świadomie Wykluczamy

**Z CORE:** kryptowaluty (skala uzasadnia analizę w PRO, ale zmienność wyklucza je z jednostki rachunkowej); złoto i srebro (silnie skorelowane z M2 jako aktywa anty-fiat, czyli z funkcji celu wynika ich wykluczenie); ceny nieruchomości *per se* (zastąpione kosztem budowy); indeksy giełdowe (silnie skorelowane z polityką monetarną).

**Z całego projektu:** wskaźniki ustalane przez ciała decyzyjne (oficjalne CPI, stopy banków centralnych, WIBOR, SOFR); dane subskrypcyjne; modele "czarnej skrzynki" bez jawnych współczynników; jakakolwiek uznaniowość pohistoryczna w interpretacji wyników.

## 9. Kwestie Otwarte (Aktualizacja względem v0.1)

**Rozstrzygnięte w v0.2 (zamknięte):**
- ~~Czy włączyć koszt pracy ludzkiej do CORE?~~ TAK — jako kwartalny komponent agregowany z ILOSTAT i OECD.
- ~~Wybór dnia bazowego $t_0$?~~ Zamiast arbitralnego ustalenia, wprowadzona procedura wyboru po EDA (sekcja 5).
- ~~Wybór procedury optymalizacji?~~ Programowanie kwadratowe (QP) z walidacją PCA (sekcja 6).
- ~~Zespół autorski?~~ Mały zespół (autor + asystenci AI). Konsultacje akademickie i recenzje merytoryczne na etapie publikacji.

**Pozostałe otwarte (do późniejszej decyzji):**
- Konkretna parametryzacja QP: długość okna historycznego treningu (proponowane 25 lat — do walidacji), ewentualna regularyzacja, czy uśrednianie M2 z państw vs. zestaw ograniczeń per kraj.
- Waluta referencyjna do publikacji bieżącej wartości AUV — USD (najwyższa płynność danych), koszyk SDR-podobny (mniej polityczny), czy publikacja w kilku walutach równolegle z jasnym wskazaniem, że to ta sama wartość.
- Procedura testu strukturalnego załamania uruchamiającego rewizję wag — wybór konkretnego testu (CUSUM, Chow, Bai-Perron) i poziomu istotności.
- Polityka traktowania dni wolnych i przesunięć czasowych między giełdami — szczególnie dla komponentu walutowego, gdzie rynek działa 24/5.

## 10. Następne Kroki

1. **Repozytorium Git (lokalne) + GitHub** — utworzenie repozytorium z dotychczasowymi notatkami, profilem autora i obecną wersją założeń. Cel: śledzenie ewolucji decyzji i przygotowanie do publicznej publikacji.
2. **Prototyp obliczeniowy** — implementacja CORE w Pythonie na danych z FRED, Yahoo Finance, ECB i Quandl/Nasdaq Data Link za ostatnie 25–30 lat. Cel: empiryczne sprawdzenie, czy wagi optymalizujące korelację z M2 dają wynikową serię AUV o sensownej dynamice (np. czy lata 1973–75, 2008, 2020 wyglądają jak należy).
3. **Analiza eksploracyjna danych (EDA)** — przeprowadzenie procedury wyboru $t_0$ z sekcji 5 na realnych szeregach.
4. **Walidacja porównawcza** — porównanie AUV z istniejącymi miarami (globalny CPI, indeksy złota, indeksy surowcowe) w okresach kryzysowych. Cel: pokazać, że AUV zachowuje się odmiennie i lepiej oddaje "prawdziwą wartość".
5. **Dokument metodologiczny v1.0** — po wynikach prototypu, doprecyzowanie pozostałych kwestii otwartych i przekształcenie obecnej notatki w formalną specyfikację (15–25 stron).
6. **Publikacja** — preprint na arXiv/SSRN, dashboard publiczny, otwarte repozytorium kodu, ogłoszenie społeczne i zaproszenie do zewnętrznej recenzji.

---

*Wersja v0.2, otwarta do iteracji. Dokument operacyjny, nie ostateczny.*
*Kolejne wersje śledzone przez Git.*
