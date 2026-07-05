# AUV — ocena praktyczna (rola: ekonomista praktyk, projektowanie instrumentów i indeksów)

**Data oceny:** 2026-07-01
**Podstawa:** PODSUMOWANIE_DLA_EKSPERTA.md, AUV_niezmienniczosc_i_rewizja.md, AUV_instrument_i_waluta.md, kod `prototyp/src/`, dane `prototyp/data/` (własne przeliczenia na plikach projektu).

---

## 1. Werdykt (3 zdania)

AUV jest wdrażalny wyłącznie jako **publikowany indeks analityczny** (miara realnej wartości, komparator do M2/CPI) — w tej roli jest solidny i wart publikacji. Jako **jednostka indeksacji umów detalicznych** (kredyty, emerytury, alimenty) w obecnym kształcie jest niewdrażalny z trzech niezależnych powodów: brak dryfu 1996–2025 to najprawdopodobniej artefakt jednego supercyklu surowcowego, a nie własność strukturalna; prawo benchmarków UE wymusza istnienie dokładnie tego autorytetu, którego projekt się wyrzeka; noga dochodowa jest opóźniona, rewidowana i zależna od kursu dolara — czego nie da się „zamrozić regułą". Droga naprawialna istnieje (indeks B2B/analityczny, potem nisza kontraktowa z administratorem), ale wymaga porzucenia dwóch flagowych haseł: „bez autorytetu" i „stała realna wartość".

## 2. Steelman — najmocniejsza wersja pomysłu

Zanim atak, wersja, której bronię: CPI systematycznie nie widzi inflacji aktywów (własny wynik projektu: hipoteki → ceny domów +0,58, nie CPI), a WIBOR/CPI są ustalane przez instytucje, którym strona umowy musi ufać. Iloraz `koszyk surowców / dochód na osobę` faktycznie kasuje walutę i mierzy pracochłonność nabycia dóbr pierwotnych — to poprawna, osadzona w literaturze wielkość (time price, Smith, commodity terms of labour). Walidacja jest ponadprzeciętna jak na projekt jednoosobowy: Monte Carlo wag, leave-one-out, rozkład trend/cykl, komparatory M2/CPI/SDR, testy Grangera. Triada japońska (bilans ×9 → inflacja +1,3% → giełda realnie −26%) to elegancki wynik. Problem nie leży w arytmetyce — leży w tym, co ta liczba znaczy i kto może na niej oprzeć 25-letnie zobowiązanie.

---

## 3. Luki (od najcięższej)

### LUKA 1 — „Brak dryfu" jest najpewniej artefaktem próby, nie własnością jednostki

**Mechanizm.** AUV = realne ceny surowców deflowane dochodem = *commodity terms of labour*. To wielkość o znanych własnościach: w literaturze (Prebisch–Singer; Grilli–Yang 1988; Jacks 2013) realne ceny surowców w XX wieku **trendowo spadały** ~0,5–1% rocznie względem cen dóbr przetworzonych, a względem płac szybciej (płace rosną szybciej niż CPI). Na to nakładają się supercykle o amplitudzie ±50% i długości 30–40 lat. Wynik „+0,4% w 30 lat" wziął się stąd, że 1996 i 2025 leżą w podobnej fazie tego samego supercyklu (1996 — środek; 2025 — zejście ze szczytu 2022). To nie jest odkrycie stałości — to wybór końcówek.

**Dowód na danych projektu.** Z `auv_t.csv`: AUV_T 2001 = 77,1; 2022 = 140,8. Ten sam wskaźnik „bez dryfu" dał **+83% w 21 lat** (2001→2022) albo **−42% w 4 lata** (2011: 147,3 → 2015: 85,7). Deklarowany dryf zależy wyłącznie od pary (start, koniec). Z literatury: indeks Grilli–Yang deflowany płacami, startujący w 1950 i zamknięty w 1998, pokazałby spadek rzędu 40–60% (do weryfikacji liczbowej na danych G-Y — ale znak i rząd wielkości są w literaturze bezsporne). Pszenica: pracochłonność nabycia w USA spadła w XX w. wielokrotnie (rząd 5–10×, Tupy & Pooley). AUV uruchomiony w 1900 nie oscylowałby wokół 100 — schodziłby schodami w dół.

**Scenariusz, w którym boli.** Bank udziela w 2026 kredytów indeksowanych AUV, wierząc w „powrót do 100". Technologia (np. tanie OZE + automatyzacja wydobycia) powtarza wzorzec 1980–2000: AUV dryfuje do 60 w 15 lat. Portfel kredytowy banku realnie topnieje o 40% względem jego nominalnych pasywów; symetrycznie — oszczędzający „w AUV" przegrywa z każdym aktywem. Jednostka nie jest neutralna: **wbudowuje zakład o wyścig rzadkości zasobów z technologią**, a historia XX w. ten zakład rozstrzygała przeciw surowcom.

**Klasyfikacja: FATALNA dla interpretacji „jednostka absolutna / stała realna wartość".** Nie unieważnia indeksu jako *miary* — unieważnia obietnicę stałości, na której opiera się zastosowanie kontraktowe.

**Naprawa.** Najtańsza: policzyć AUV wstecz do 1900 (Grilli–Yang, Jacks, dane płacowe BLS/Clark — wszystko publiczne) i pokazać, jak jednostka zachowuje się przez *kilka* supercykli i przez trend Prebischa–Singera. Koszt: tygodnie pracy, zero nowych koncepcji. Kompromis: wynik niemal na pewno pokaże dryf, więc narracja musi się zmienić z „stała wartość" na „miara o znanym cyklu i trendzie" — co jest uczciwe, ale odbiera głównej tezie marketingowej ostrze. Walidacja Monte Carlo (75–127) tego nie ratuje: losuje wagi **wewnątrz tego samego koszyka i okresu**, więc testuje odporność kompozycji, nie odporność koncepcji na epokę.

### LUKA 2 — Prawo benchmarków: „indeks bez autorytetu" nie może indeksować umów konsumenckich w UE

**Mechanizm.** Rozporządzenie UE 2016/1011 (BMR) wymaga, by wskaźnik referencyjny używany w umowach kredytu konsumenckiego/hipotecznego miał **autoryzowanego administratora** wpisanego do rejestru ESMA, z procedurami nadzoru, dokumentacją metodologii, planami awaryjnymi i odpowiedzialnością prawną. Deterministyczna formuła na GitHubie nie jest podmiotem prawa. Bank w Polsce nie może zgodnie z prawem uzależnić raty od indeksu bez administratora — niezależnie od jakości formuły.

**Dowód/ilustracja.** Reforma WIBOR→WIRON/POLSTR (2022–2025) — wymiana jednego administrowanego wskaźnika na inny administrowany, pod nadzorem KNF, z wieloletnią mapą drogową; nikt nawet nie rozważał wskaźnika „bezadministratorowego", bo BMR to wyklucza. Drugi konkret: polskie kredyty CHF — sądy masowo unieważniały umowy z powodu klauzul indeksacyjnych uznanych za abuzywne (art. 385¹ k.c.); rezerwy sektora bankowego na to ryzyko przekroczyły rząd **80–100 mld zł** (do sprawdzenia dokładnej kwoty na 2026). Indeksacja do egzotycznego, zmiennego, obcego ekonomicznie indeksu to podręcznikowy kandydat na klauzulę abuzywną: konsument nie jest w stanie zrozumieć ryzyka (rata zależna od ceny uranu i niklu?).

**Scenariusz.** Fintech oferuje „kredyt w AUV". Vintage 2015: rata rośnie o 64% do 2022 (patrz test kontraktowy niżej). Kredytobiorcy idą do sądu; pełnomocnik wskazuje: wskaźnik bez administratora BMR, ryzyko nieobjaśnione, asymetria informacji. Umowy padają seriami jak CHF; oferent bankrutuje od kosztów prawnych, indeks zostaje spalony reputacyjnie na dekadę.

**Klasyfikacja: FATALNA dla zastosowania (a) w UE w formule „bez autorytetu"; NAPRAWIALNA przez kapitulację z hasła.** Naprawa: powołać fundację-administratora (jak ICE Benchmark Administration po LIBOR), przejść autoryzację BMR, publikować kod jako *załącznik* do metodologii. Koszt: instytucja, nadzór, pieniądze — i przyznanie, że projekt buduje kolejny (lepiej skonstruowany) autorytet, a nie jego brak. UF — przywoływany wzorzec — działa właśnie dlatego, że jest tworem **państwowym z mandatem** (dekret 1967, dziś ustawowo publikowana przez Banco Central de Chile): to dokładne zaprzeczenie heliocentryczności.

### LUKA 3 — Noga dochodowa: opóźniona, rewidowana, kursowa — i już dziś z błędem w pipeline

**Mechanizm.** Mianownik (PKB świata w bieżących USD / populacja) ma trzy wady, których żadna reguła publikacyjna nie usuwa: (i) publikowany z opóźnieniem ~6–18 mies. i **rewidowany przez lata** przez te same „autorytety", od których AUV miał być niezależny; (ii) zależny od **kursu dolara**: aprecjacja USD mechanicznie kurczy światowe PKB w USD bez żadnej zmiany realnej; (iii) skokowo rewidowany przez rebasing krajów.

**Dowody z liczbami.**
- *Rewizje/rebasing:* Nigeria 2014: PKB **+89%** jednym komunikatem (rebasing z bazy 1990 na 2010); Ghana 2010: **+60%**; Indie 2015: zmiana metodologii przesunęła dynamikę wzrostu o ~2 p.p. UN WPP 2022/2024 rewidowały poziom i trajektorię populacji świata (w tym Chin/Indii). Zasada „nigdy nie rewidujemy wstecz" jest pusta, gdy **wejście** formuły jest rewidowane wstecz — AUV opublikowany w marcu i „ten sam" AUV policzony z danych ostatecznych to dwie różne liczby; którą honoruje kontrakt?
- *Efekt kursowy:* 2015 — światowe PKB w bieżących USD spadło o **−5,5%** (80,05→75,62 bln, plik `wb_WLD_NY_GDP_MKTP_CD` w repo), podczas gdy realny wzrost świata wyniósł ok. +2,9%. Różnica ~8 p.p. to czysta aprecjacja dolara. Mianownik „w godzinach pracy cywilizacji" zafalował o 8% od decyzji Fed — dokładnie ten rodzaj zależności, który projekt deklaratywnie eliminuje. Niezmienniczość numéraire jest prawdziwa *księgowo* (I.2), ale agregat „dochód świata w USD" nie jest wielkością fizyczną — jest sumą po kursach bieżących, z wagami zależnymi od polityki monetarnej USA.
- *Błąd w pipeline (wykryty przy tej ocenie):* w `processed/auv_t.csv` mianownik jest **opóźniony o ~1 rok** względem danych źródłowych — spadek PKB z 2015 pojawia się w `dochod_glob_per_capita` dopiero w 2016 (WB 2015: −5,5% vs processed 2015: +0,7%, processed 2016: −6,1%). To artefakt forward-fill rocznych danych stemplowanych 31.12 i rocznego uśredniania. Wszystkie flagowe liczby (+0,4%, tabele sekcji 10.4/11.2) są policzone z licznikiem bieżącym i mianownikiem zeszłorocznym — cykl AUV jest przez to sztucznie wzmocniony (licznik reaguje natychmiast, mianownik rok później). Do poprawki przed jakąkolwiek publikacją.

**Scenariusz.** Publikujesz AUV z „wolnym mianownikiem zamrożonym między odczytami". W lipcu Bank Światowy podnosi PKB świata o 2% (rutynowa rewizja + rebasing dużego kraju). Nowy odczyt mianownika skokowo obniża AUV o 2% jednego dnia. Strony kontraktów znają datę odczytu z wyprzedzeniem → rozliczenia i przedpłaty klastrują się wokół tej daty (gaming terminu). Jednocześnie ktoś odtwarza AUV z danych ostatecznych i pokazuje, że opublikowana historia odbiega od „prawdziwej" o 1–3% — kończy się spórem, czym AUV *jest*.

**Klasyfikacja: NAPRAWIALNA, ale kosztem prostoty i części filozofii.** Najtańsza naprawa: (1) naprawić lag w pipeline (dni); (2) mianownik liczyć z **PKB w PPP lub z trendu realnego PKB + własnego deflatora** zamiast bieżących USD — usuwa większość efektu kursowego; (3) do kontraktów zamrażać mianownik jako **prognozę trendu ogłaszaną z wyprzedzeniem** (jak UF zamraża ścieżkę na miesiąc naprzód), z korektą wyłącznie w przód. Kompromis: mianownik staje się modelem, nie obserwacją — kolejny krok od „czystej formuły z danych".

### LUKA 4 — Kontrakt przenosi cykl surowcowy na kredytobiorcę dokładnie wtedy, gdy ten jest najsłabszy

**Mechanizm.** Dochód kredytobiorcy jest nominalny i lepki; AUV szczytuje w szokach podażowych (2008, 2022), które są zarazem kryzysami kosztów życia i recesji. Indeksacja do AUV podnosi ratę **procyklicznie względem stresu gospodarstwa domowego** — silniej niż CPI, bo koszyk to surowce bez tłumiących usług. Wygładzenie 5-letnie zmniejsza amplitudę, ale wprowadza nowy problem: raty potrafią *spadać* nominalnie przez 5 lat z rzędu (2015–2020), czego nominalnie finansujący się bank nie przeżyje bez rynku hedgingowego — a rynku instrumentów na „koszyk surowców / dochód świata" nie ma i długo nie będzie.

**Dowód.** Pełny test kontraktowy w sekcji 4. Skróty: raw — obciążenie dochodu rośnie z 30% do **42,3%** (2007); vintage 2015 — rata **+64%** do 2022 przy wzroście płac +27%. Wariant kontraktowy — rata spada z ~25 tys. (2011) do ~16,9 tys. (2020): **−32%** przychodu odsetkowego banku w 9 lat, nie do zabezpieczenia żadnym istniejącym instrumentem (TIPS hedżują CPI; futures surowcowe hedżują licznik, ale nie iloraz i nie 5-letnią średnią).

**Klasyfikacja: FATALNA dla detalicznych hipotek; NAPRAWIALNA dla nisz.** Nisze, gdzie dochód dłużnika *jest* skorelowany z AUV: producenci surowców, firmy energetyczne, kraje eksporterzy (analogia: obligacje indeksowane ceną ropy — Meksyk, Wenezuela; obligacje katastroficzne). Tam AUV-indeksacja redukuje ryzyko zamiast je tworzyć. Naprawa = zmiana grupy docelowej, nie formuły. Koszt: rezygnacja z opowieści o „kredycie hipotecznym w AUV".

### LUKA 5 — Do indeksacji emerytur i alimentów AUV nie nadaje się wprost z konstrukcji

**Mechanizm.** Emerytura/alimenty mają utrzymać **koszyk konsumpcji** beneficjenta, który w gospodarkach rozwiniętych to w ~70–80% usługi i mieszkanie — składniki nieobecne w AUV. AUV mierzy pracochłonność surowców, która z Engelowskiej natury *spada* relatywnie do kosztów życia.

**Dowód z danych projektu.** Emeryt ze świadczeniem indeksowanym AUV-kontrakt od 2011: indeks 145,4 (2011) → 98,3 (2020) = świadczenie nominalnie **−32%**, podczas gdy CPI wzrósł +15%. Realna siła nabywcza świadczenia względem kosztów życia: **−41%** w 9 lat. W wariancie surowym −42% nominalnie już do 2015. Świadczeniobiorca nie ma żadnego mechanizmu kompensaty — to nie jest „zmienność", to strukturalne niedopasowanie miary do celu. Dla porównania: absurd symetryczny — indeksacja do samego CPI energii też nikomu nie przyszłaby do głowy jako „ochrona emeryta".

**Klasyfikacja: FATALNA dla świadczeń socjalnych/alimentów.** Nie naprawiaj — wykreśl ten use case z materiałów. Najtańsza „naprawa" to uczciwość: AUV chroni przed deprecjacją *pieniądza*, nie przed wzrostem *kosztów życia*; to różne ryzyka i różne produkty.

### LUKA 6 — Determinizm formuły pęka na awariach i manipulacjach rynków źródłowych

**Mechanizm.** Formuła jest deterministyczna tylko wtedy, gdy wejścia są jednoznaczne. Rynki z koszyka bywają cienkie (uran — rynek spot rzędu paru mld USD/rok, ceny raportowane przez prywatne agencje UxC/TradeTech; ruda żelaza i węgiel — benchmarki Platts/Fastmarkets, **licencjonowane i płatne**, co już łamie deklarację „otwarte dane"; ryż — płytki rynek referencyjny). Cienki rynek + indeks o dużej adopcji = zaproszenie do manipulacji (lekcja LIBOR: manipulowano nawet *ankietą banków*; lekcja Platts 2013: śledztwo KE ws. manipulacji oknem cenowym ropy).

**Dowód-epizod.** Nikiel, LME, 8 marca 2022: cena z ~30 do >100 tys. USD/t intraday (short squeeze Tsingshan); LME **zawiesiła handel i anulowała transakcje** za ~4–12 mld USD (kwota sporna, do sprawdzenia) decyzją zarządu. Pytanie bez dobrej odpowiedzi: co robi „deterministyczny, nieuznaniowy" AUV tego dnia? (a) bierze cenę ×4 — kontrakty na AUV dostają fałszywy szok od jednego squeeze'u; (b) czeka na decyzję LME — czyli autorytetu; (c) stosuje własną regułę odcięcia — czyli *sam jest* autorytetem, tylko zapisanym w kodzie z góry. Nikiel ma w koszyku 1/7 wagi kategorii metali ≈ 3,6% całości: dzień ×4 to impuls ~+5% w AUV dziennym — przy indeksie reklamowanym jako „stabilna jednostka".

**Klasyfikacja: NAPRAWIALNA, ale naprawa = governance.** Mediana z ≥3 niezależnych źródeł na składnik, winsoryzacja ruchów dziennych (np. obcięcie do ±3σ), reguły zawieszenia składnika — wszystko do zapisania z góry (projekt zresztą kierunkowo to przewiduje w II.4). Koszt: każda taka reguła to parametr wybrany przez człowieka; „test nakładania" z II.4.6 wprost przywraca uznaniowość („wstrzymanie do przeglądu" — czyj przegląd?). Determinizm okazuje się stopniowalny, nie binarny — i trzeba to powiedzieć otwarcie, zamiast obiecywać jednostkę „której nikt nie może zmienić".

### LUKA 7 — „Godziny pracy" to metafora: mianownik nie jest płacą, a kredytobiorca nie zarabia światowego PKB

**Mechanizm.** PKB/os. ≠ dochód z pracy: zawiera zyski kapitałowe, amortyzację, podatki; udział pracy w PKB **spada** (globalnie z ok. 54% do ok. 50–52% w 30 lat — rząd wielkości do weryfikacji, kierunek bezsporny), a mediana płac rośnie wolniej niż PKB/os. (USA 1996–2025: realna mediana tygodniówki +~10–15% vs realny PKB/os. +~55%; dokładne liczby do sprawdzenia w FRED LES1252881600Q). AUV liczony **medianową płacą** — czyli tym, co retoryka „godzin pracy zwykłego człowieka" obiecuje — miałby wyraźny dryf w górę. Wybór mianownika (PKB/os. vs płaca) zmienia znak głównego wyniku; test odporności w 11.2 (na osobę vs na pracownika, różnica 3 p.p.) nie dotyka tej osi, bo oba warianty to nadal PKB.

Do tego basis risk geograficzny: mianownik jest światowy, kredytobiorca lokalny. Polski dochód nominalny w USD potrafi rozjechać się ze światowym o kilkanaście procent w rok (2015: PLN −20% do USD). Kontrakt „w godzinach pracy cywilizacji" indeksuje polską ratę do chińsko-amerykańskiego wzrostu ważonego kursem dolara.

**Klasyfikacja: NAPRAWIALNA analitycznie, groźna komunikacyjnie.** Naprawa: policzyć warianty mianownika (PKB/os., płaca mediana G5, compensation of employees z rachunków narodowych) i pokazać wachlarz wyników zamiast jednej liczby; nazywać jednostkę „w jednostkach dochodu", nie „w godzinach pracy", dopóki mianownik nie jest płacą × godziny. Koszt: kolejny cios w prostotę przekazu.

### LUKA 8 — Adopcja: jednostka rachunkowa bez mandatu i bez rynku nie ma strony podażowej

**Mechanizm.** Każdy udany przypadek jednostki indeksacyjnej miał przymus lub quasi-przymus: UF — dekret państwowy i cały system (podatki, czynsze, sądy) rozliczający się w UF; TIPS — emitent suwerenny; SDR — traktat. AUV nie ma nikogo, kto *musi* go używać, i nikogo, kto *może* zabezpieczyć drugą stronę ryzyka (brak instrumentów pochodnych na iloraz koszyk/dochód). Bez emitenta naturalnego i bez hedgingu spread, jaki bank doliczy za nieznane ryzyko, zje całą korzyść kredytobiorcy.

**Ilustracja.** Nawet CPI-linked hipoteki — z doskonale znanym, administrowanym indeksem — są rynkową egzotyką poza Chile/Izraelem (Izrael: znów mandat historyczny wysokiej inflacji; Islandia: kredyty indeksowane CPI istnieją i są politycznie znienawidzone po 2008 — dobry benchmark tego, jak kończy indeksacja, którą kredytobiorcy rozumieją dopiero w kryzysie).

**Klasyfikacja: NAPRAWIALNA tylko sekwencją.** Realistyczna drabina: (1) publikacja indeksu + seria analityczna (za darmo, buduje historię i cytowalność); (2) użycie w umowach B2B między stronami o dochodach skorelowanych z surowcami (nie wymaga BMR przy kwalifikowanych kontrahentach — do weryfikacji prawnej); (3) dopiero po dekadzie historii — rozmowa o detalicznych produktach. Koszt: horyzont 10+ lat i pokora wobec efektu sieci.

---

## 4. Test kontraktowy: 25-letni kredyt hipoteczny indeksowany AUV, 2000–2024

Założenia (jawne): kapitał 300 000 j.p., annuitet 25 lat, stopa realna 2,5% ponad indeksację (model UF), rata = stała w jednostkach indeksu × indeks(t)/indeks(2000); dochód kredytobiorcy nominalny, start 54 276 j.p. (rata początkowa = 30% dochodu), wzrost płac 3,5%/rok (≈ średnia USA 1996–2025). Indeksy z pliku projektu `auv_contract.csv` (AUV_raw, AUV_kontrakt = wygładzony 5-letnio, CPI). Obciążenie = rata/dochód.

| Rok | Rata AUV_raw | Obc. | Rata AUV_kontrakt | Obc. | Rata CPI | Obc. |
|---|---|---|---|---|---|---|
| 2000 | 16 283 | 30,0% | 16 283 | 30,0% | 16 283 | 30,0% |
| 2004 | 20 691 | 33,2% | 15 989 | 25,7% | 17 864 | 28,7% |
| 2007 | 29 185 | **42,3%** | 20 538 | 29,7% | 19 607 | 28,4% |
| 2008 | 29 407 | 41,1% | 22 792 | **31,9%** | 20 355 | 28,5% |
| 2009 | 20 809 | 28,1% | 22 818 | 30,8% | 20 289 | 27,4% |
| 2011 | 29 352 | 37,0% | 24 963 | 31,5% | 21 269 | 26,8% |
| 2015 | 17 088 | 18,8% | 21 015 | 23,1% | 22 412 | 24,6% |
| 2020 | 16 907 | 15,7% | 16 866 | 15,6% | 24 478 | 22,7% |
| 2021 | 25 722 | 23,0% | 18 236 | 16,3% | 25 624 | 22,9% |
| 2022 | 28 057 | 24,3% | 19 697 | 17,0% | 27 671 | 23,9% |
| 2024 | 21 492 | 17,3% | 21 214 | 17,1% | 29 664 | 23,9% |

Statystyki pełnej ścieżki 2000–2024:

| Wariant | Maks. skok raty r/r | Maks. spadek r/r | Maks. obciążenie | Suma rat |
|---|---|---|---|---|
| AUV_raw | **+52,1%** (2021) | **−29,2%** (2009) | 42,3% | 540 134 |
| AUV_kontrakt | +12,2% | −9,9% | 31,9% | 486 798 |
| CPI | +8,0% | −0,3% | 30,0% | 543 549 |

Odczyt praktyczny. (1) Surowy AUV jest kontraktowo dyskwalifikowany własnymi liczbami: rata +52% w rok, obciążenie 42% dochodu w 2007 — dla vintage 2000 i tak „łagodnie", bo start trafił w dołek cyklu. (2) **Vintage 2015** (start w dołku): rata raw +64% do 2022 przy płacach +27% — obciążenie z 30% na 38,7%; to jest scenariusz pozwu zbiorowego. (3) Wariant kontraktowy chroni kredytobiorcę (maks. 31,9%), ale spójrz na to okiem banku: raty **spadają nominalnie w 8 z 24 lat**, suma rat jest o ~10% niższa niż przy CPI, a szczyt przychodu wypada w 2011 i potem maleje przez 9 lat — przy pasywach banku rosnących nominalnie. Bez instrumentu hedgingowego na AUV żaden komitet ALCO tego nie zaakceptuje, a instrumentu nie ma. (4) Los kredytobiorcy zależy od **vintage'u** (fazy cyklu na starcie) bardziej niż od czegokolwiek innego — loteria, której CPI-indeksacja nie ma.

---

## 5. Trzy pytania, na które autor musi odpowiedzieć przed traktowaniem pomysłu poważnie

1. **Jak AUV zachowuje się poza próbą 1996–2025?** Policz go na danych 1900–1995 (Grilli–Yang, Jacks, płace BLS). Jeśli — jak wskazuje literatura — pokaże wielodekadowy dryf, czy jesteś gotów zmienić obietnicę produktu ze „stałej realnej wartości" na „przejrzystą miarę cyklu zasobowego"? To pytanie rozstrzyga, czy istnieje w ogóle zastosowanie kontraktowe.
2. **Kto jest administratorem i kto trzyma drugą stronę ryzyka?** Konkretnie: jaki podmiot przejdzie autoryzację BMR (albo jaka jurysdykcja/segment jej nie wymaga), i jaki bilans absorbuje spadki rat −10% r/r w fazie „tanio" oraz czym się hedżuje? Bez tych dwóch nazwisk (instytucja, kontrahent) AUV pozostaje publikacją, nie instrumentem.
3. **Co dokładnie jest opublikowaną, kontraktowo wiążącą liczbą w czasie rzeczywistym**, skoro mianownik jest roczny, opóźniony ~1,5 roku, rewidowany wstecz i zależny od kursu USD (a w obecnym pipeline dodatkowo przesunięty o rok)? Podaj pełny algorytm dnia publikacji — z regułą na rewizję PKB, rebasing kraju i anulowanie transakcji przez giełdę (przypadek nikiel-2022) — i sprawdź, ile decyzji ludzkich ten algorytm jednak zawiera.

---

## 6. Fakty vs opinie

**Fakty (dane projektu, przeliczone przy tej ocenie):** wartości AUV_T/AUV_raw/AUV_kontrakt/CPI cytowane wyżej pochodzą z `auv_t.csv` i `auv_contract.csv`; symulacja kredytu — obliczenia własne na tych plikach przy jawnych założeniach (2,5% real, 3,5% wzrost płac, 30% startowe obciążenie); opóźnienie mianownika o ~1 rok — zweryfikowane porównaniem `wb_WLD_NY_GDP_MKTP_CD` (2015: −5,5%) z `dochod_glob_per_capita` (2015: +0,7%; 2016: −6,1%); spadek światowego PKB w USD w 2015 przy dodatnim wzroście realnym — plik w repo + dane WB.

**Fakty (wiedza dziedzinowa, wysoka pewność):** Nigeria 2014 rebasing +89%; Ghana 2010 ~+60%; UF utworzona w 1967 i publikowana przez instytucje państwowe Chile; BMR 2016/1011 wymaga administratora dla wskaźników w umowach konsumenckich UE; LME zawiesiła i anulowała transakcje niklem 8.03.2022; śledztwo KE ws. Platts 2013; trend Prebischa–Singera i indeks Grilli–Yang (realny spadek cen surowców w XX w.); Islandia/Izrael/Chile jako rynki kredytów indeksowanych.

**Do weryfikacji liczbowej (podałem rzędy wielkości):** dokładna kwota rezerw CHF polskich banków (rząd 80–100 mld zł); wartość anulowanych transakcji niklowych (4–12 mld USD); dokładny spadek udziału pracy w PKB i rozjazd mediany płac vs PKB/os. w USA; wielkość dryfu hipotetycznego AUV 1950–2000.

**Opinie (moje osądy zawodowe):** że brak dryfu 1996–2025 jest artefaktem próby (mechanizm i literatura mocno to wspierają, ale rozstrzygnie dopiero przeliczenie wstecz); że żaden bank nie przyjmie ryzyka AUV bez rynku hedgingowego; że sekwencja „indeks analityczny → B2B → detal" jest jedyną realistyczną; że wartość projektu jest realna, ale leży w **pomiarze** (linijka do demaskowania iluzji monetarnej — triada japońska to najlepszy materiał na publikację), a nie w indeksacji detalicznych zobowiązań.
