# Odpowiedź na ocenę ekonomisty praktyka

**Data:** 2026-07-02
**Do:** `OCENA_ekonomisty_praktyka.md`
**Stanowisko ogólne:** ocena jest rzetelna i w większości trafna. Przyjmujemy jej główny werdykt: **AUV jest solidny jako miara/indeks analityczny, a niewdrażalny jako detaliczna jednostka kontraktowa w obecnym kształcie.** Poniżej pozycja do każdej luki oraz wprowadzone korekty.

## 0. Błąd w pipeline — POTWIERDZONY i NAPRAWIONY

Zarzut z LUKI 3 o opóźnieniu mianownika zweryfikowany empirycznie i prawdziwy. Korelacja `dochod_glob_per_capita` z WB(t−1) = 0,9999 vs z WB(t) = 0,986; spadek PKB 2015 (−6,6%) pojawiał się u nas w 2016. Przyczyna: dane roczne WB stemplowane 31.12, forward-fill + roczne uśrednianie przesuwały mianownik o rok.

Naprawa (`src/auv_t.py`): mianownik liczony teraz z wartości końca roku (`.last()` = grudzień = poprawny rok), nie ze średniej rocznej. Skutki:
- zmienność AUV-T spada z **0,154 do 0,123**, cykl urealniony (szczyt 2008: 148→137; 2011: 147→134);
- **dryf 1996→2024 = +5,0%** (poprawnie zsynchronizowany), zamiast rozdmuchanego cyklu;
- liczba „2025 = +0,4%" jest **prowizoryczna** — WB nie opublikował PKB 2025, więc dzieli koszyk 2025 przez dochód 2024; przestaje być liczbą flagową.

Wszystkie moduły używające `compute()` dziedziczą poprawkę. Flagowe liczby w dokumentach do aktualizacji na 1996→2024.

## Pozycja do poszczególnych luk

**LUKA 1 — „brak dryfu" to artefakt jednego supercyklu. PRZYJMUJEMY.** To najgłębszy i najsłuszniejszy zarzut. Literatura (Prebisch–Singer, Grilli–Yang, Jacks) wskazuje na wielodekadowy spadek realnych cen surowców względem płac. Nasze +5,0% (1996–2024) leży wewnątrz jednego supercyklu i nie dowodzi stałości. *Niuans, nie obrona:* jeśli AUV dryfuje w dół w stuleciu, to jest to **poprawny sygnał realnego postępu** (teza Superabundance: zasoby tanieją w pracy) — nie błąd miary, lecz jej treść. Podważa to obietnicę „stałej wartości" dla zastosowania *kontraktowego/store-of-value*, nie wartość *pomiarową*. Działanie: **test wsteczny do 1900** (Grilli–Yang, Jacks, płace) jako warunek konieczny; zmiana narracji ze „stałej wartości" na „przejrzystą miarę cyklu i trendu zasobowego".

**LUKA 2 — prawo benchmarków (BMR). PRZYJMUJEMY w całości.** Formuła na GitHubie nie jest podmiotem prawa; rozporządzenie UE 2016/1011 wymaga autoryzowanego administratora dla wskaźników w kredytach konsumenckich. Hasło „bez autorytetu" jest niekompatybilne z detaliczną indeksacją w UE. Trafna też uwaga o UF: działa, bo jest tworem *państwowym z mandatem* — przeciwieństwo heliocentryczności. Działanie: albo AUV pozostaje indeksem analitycznym (BMR nie dotyczy), albo powstaje fundacja-administrator (BMR) — czyli „lepszy autorytet", nie jego brak. Reframing hasła obowiązkowy.

**LUKA 3 — noga dochodowa: opóźniona, rewidowana, kursowa. PRZYJMUJEMY (poza naprawionym lagiem).** Trzy realne wady mianownika: (i) PKB rewidowane przez te same instytucje, od których deklarowaliśmy niezależność (Nigeria 2014 +89% itd.) — realna sprzeczność z „heliocentrycznością"; (ii) PKB w bieżących USD zależy od kursu dolara (2015: −5,5% w USD to głównie aprecjacja USD, nie realność) — poważna wada; (iii) rebasing skoków krajowych. *Ważne przyznanie:* teza z noty o niezmienniczości (Cz. I), że dochód da się odtworzyć z wielkości fizycznych, jest prawdziwa *teoretycznie*, ale nasza *implementacja* używa nominalnego PKB w USD — ani fizycznego, ani neutralnego kursowo. To luka między teorią a kodem. Działanie: mianownik z **PKB w PPP lub realnego PKB + własny deflator** (usuwa efekt kursowy); do kontraktów mianownik jako ogłaszana z wyprzedzeniem ścieżka trendu.

**LUKA 4 — kontrakt przenosi cykl surowcowy na kredytobiorcę. PRZYJMUJEMY.** Test kontraktowy recenzenta (vintage 2015: rata +64% do 2022 przy płacach +27%; wariant wygładzony spada nominalnie w 8/24 lat, niehedżowalny) jest przekonujący. Surowy AUV kontraktowo zdyskwalifikowany; wygładzony chroni dłużnika, ale zabija wierzyciela bez rynku hedgingowego, którego nie ma. Działanie: zawęzić do **nisz o dochodzie skorelowanym z AUV** (producenci surowców, eksporterzy energii), gdzie indeksacja *redukuje* ryzyko.

**LUKA 5 — emerytury/alimenty. PRZYJMUJEMY, wykreślamy use case.** AUV mierzy pracochłonność surowców; koszt życia emeryta to w ~70–80% usługi i mieszkanie, nieobecne w koszyku. Indeksacja świadczeń do AUV jest strukturalnie błędna (emeryt 2011→2020: −32% nominalnie przy CPI +15%). AUV chroni przed deprecjacją *pieniądza*, nie przed wzrostem *kosztu życia* — to różne ryzyka. Usuwamy emerytury/alimenty z zastosowań.

**LUKA 6 — determinizm pęka na manipulacji/awariach rynków. PRZYJMUJEMY.** Nikiel LME 8.03.2022 (cena ×4, giełda anuluje transakcje) obnaża: „nieuznaniowy" AUV tego dnia i tak wymaga reguły wybranej przez człowieka. Determinizm jest **stopniowalny, nie binarny**. Trafna też uwaga, że część benchmarków (ruda żelaza, węgiel — Platts/Fastmarkets) jest licencjonowana — więc „w pełni otwarte dane" to idealizacja (choć nasze ceny idą przez FRED/IMF, które są darmowe, źródło pierwotne bywa płatne). Działanie: mediana z ≥3 źródeł, winsoryzacja, reguły zawieszenia — zapisane z góry, ale otwarcie nazwane „ograniczoną uznaniowością", nie „brakiem autorytetu".

**LUKA 7 — „godziny pracy" to metafora; mianownik to PKB, nie płaca. PRZYJMUJEMY.** PKB/os. ≠ dochód z pracy (udział pracy spada; mediana płac rośnie wolniej niż PKB/os.). Wybór mianownika (PKB vs płaca mediana) może zmienić znak wyniku; test „na osobę vs na pracownika" tego nie dotyka, bo oba to PKB. Działanie: nazywać jednostkę **„w jednostkach dochodu"**, nie „w godzinach pracy", dopóki mianownik nie jest płacą; policzyć wariant z medianą płac G5 i pokazać wachlarz.

**LUKA 8 — adopcja bez mandatu i rynku. PRZYJMUJEMY.** Każdy udany przypadek miał przymus (UF dekret, TIPS suweren, SDR traktat). Realistyczna drabina: (1) indeks analityczny publiczny; (2) umowy B2B między stronami o dochodach skorelowanych z surowcami; (3) detal dopiero po dekadzie historii. Przyjmujemy tę sekwencję.

## Synteza — co się zmienia w projekcie

1. **Rdzeń wartości przesuwa się jednoznacznie na POMIAR.** AUV to linijka demaskująca iluzję monetarną (triada japońska, kierunek vs skala inflacji) — i to jest publikowalny wkład. Zastosowanie kontraktowe: nisza B2B, po backteście i z administratorem, w dalekim horyzoncie.
2. **Korekty haseł (uczciwość):** „stała wartość" → „miara o znanym cyklu/trendzie (trend historyczny do zbadania)"; „bez autorytetu" → „minimalizacja i przejrzystość uznaniowości; determinizm stopniowalny"; „w godzinach pracy" → „w jednostkach dochodu"; „w pełni otwarte dane" → „przeważnie otwarte".
3. **Nowa lista zadań (priorytet):** (a) backtest 1900–1995; (b) mianownik PPP/realny zamiast bieżących USD; (c) wariant z medianą płac; (d) reguły odporności na manipulację (mediana źródeł, winsoryzacja) zapisane wprost; (e) reszta jak w `PLAN_operacjonalizacja_AUV.md`.
4. **Use case wykreślone:** emerytury, alimenty, detaliczne hipoteki „w AUV" (do czasu spełnienia a–d i rozwiązania BMR).

Ocena nie obala projektu — **urealnia go**. Najmocniejszy wynik (AUV jako miara realnej wartości ponad iluzją monetarną) pozostaje nietknięty; upada część marketingowa („absolutna, stała, bez autorytetu"), która i tak była najsłabszym ogniwem.
