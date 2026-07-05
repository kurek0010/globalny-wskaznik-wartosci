# Jak zbudować jednostkę wartości zdatną do umów finansowych — nota koncepcyjna

**Kontekst:** odpowiedź na pytanie „jak zbudować wskaźnik będący miernikiem wszelkich wartości, na którym można oprzeć wszelkie umowy finansowe", po krytycznej ocenie AUV (`OCENA_ekonomisty_praktyka.md`).
**Data:** 2026-07-02
**Status:** koncepcja do dyskusji.

---

## 1. Twierdzenie o niemożliwości — najpierw uczciwość

„Miernik wszelkich wartości" nie istnieje i nie może istnieć. Cztery niezależne powody:

**(1) Problem indeksowy (Fisher).** Każdy indeks wartości wymaga koszyka i wag. Różne koszyki dają różne odpowiedzi na pytanie „ile to jest warte" i nie ma matematycznego kryterium wyboru „tego właściwego" — Fisher skatalogował ponad sto formuł indeksowych i żadna nie spełnia wszystkich aksjomatów naraz. To nie brak pomysłowości, to twierdzenie.

**(2) Heterogeniczność.** Wartość dla emeryta (koszyk konsumpcji: leki, mieszkanie, usługi) ≠ wartość dla oszczędzającego (dostęp do aktywów) ≠ wartość dla huty (surowce i energia). Jedna liczba nie może chronić wszystkich naraz — ochrona jednego profilu jest ekspozycją innego. AUV udowodnił to na sobie: chronił przed deprecjacją pieniądza, rujnując emeryta (−41% względem kosztów życia 2011–2020).

**(3) Numéraire to decyzja dystrybucyjna.** W każdej umowie jednostka rozliczeniowa decyduje, **kto niesie które ryzyko**. Nominalna złotówka: ryzyko inflacji niesie wierzyciel. CPI: ryzyko realnych płac niesie dłużnik. AUV: ryzyko cyklu surowcowego niesie dłużnik. Nie ma jednostki „bez ryzyka" — jest tylko jawny albo ukryty podział ryzyka. Właściwe pytanie brzmi więc nie „jaka jednostka jest prawdziwa", lecz **„jaki podział ryzyka jest sprawiedliwy i utrzymywalny przez 25 lat"**.

**(4) Goodhart/refleksywność.** Każda miara, na której wiszą duże pieniądze, przestaje być neutralnym pomiarem (LIBOR, manipulacje benchmarków Platts, WIBOR-owe spory). Skala adopcji, o którą pytasz („wszelkie umowy"), gwarantuje presję na miarę.

Wniosek: cel trzeba przeformułować. Nie „jednostka absolutna", lecz **jednostka minimalnego żalu** — taka, przy której obie strony umowy po 25 latach najmniej żałują podpisu, plus **rodzina** jednostek zamiast jednej.

---

## 2. Kluczowa obserwacja: najlepszą jednostką dla umów jest dochód, nie koszyk dóbr

To jest serce propozycji i zarazem miejsce, gdzie AUV był o krok od celu — mianownik AUV jest lepszym kandydatem na jednostkę niż cały AUV.

**Argument.** Rozważ ratę kredytu indeksowaną do **mediany dochodu z pracy** w gospodarce kredytobiorcy. Wtedy z konstrukcji: rata = stały ułamek typowego dochodu, zawsze. Kredytobiorca nigdy nie doświadcza wzrostu obciążenia względem społeczeństwa, w którym żyje (jego osobiste ryzyko względem mediany zostaje — i powinno zostać, to jego ryzyko idiosynkratyczne). Wierzyciel dostaje w zamian udział we wzroście nominalnych dochodów — czyli ochronę i przed inflacją, i przed stagnacją realną. Żadna jednostka koszykowa (CPI, złoto, surowce, AUV) nie ma tej własności; wszystkie mogą rozjechać się z dochodami i wtedy któraś strona krwawi.

**To nie jest nowy pomysł — i to jest jego zaleta.** Marshall (1887) postulował „tabular standard" dla kontraktów; Fisher (1913) „compensated dollar"; współcześnie Shiller (*Macro Markets* 1993, *The New Financial Order* 2003) zaprojektował dokładnie to: jednostki rozliczeniowe indeksowane dochodem oraz „trille" — papiery wypłacające jedną bilionową PKB. Literatura obligacji indeksowanych PKB (Borensztein–Mauro, MFW) istnieje od dekad. Twój projekt niezależnie doszedł do mianownika dochodowego — to dobra wiadomość: koncepcja ma teoretyczne plecy.

**Dlaczego dochód rozwiązuje problem hedgingu, który zabił AUV-kontrakt.** Instrument indeksowany dochodem ma **naturalnego nabywcę drugiej strony**: fundusze emerytalne i ubezpieczyciele rent mają zobowiązania z natury indeksowane płacami (przyszłe emerytury rosną z płacami). Dziś nie mają czym ich hedżować — kupują obligacje nominalne i modlą się. Aktywa płacowo-indeksowane to dla nich brakujący instrument, na który czekają od lat (Shiller o tym pisał wprost). AUV nie miał kontrahenta; jednostka dochodowa ma go systemowo. To jest różnica między pomysłem a rynkiem.

---

## 3. Architektura: rodzina jednostek zamiast jednego wskaźnika

Zamiast jednej liczby — **standard rodziny jednostek** (jak ISO walut), z jawną konwersją między nimi. Cztery jednostki bazowe, każda odpowiada innemu pojęciu „wartości":

| Jednostka | Definicja (szkic) | Chroni | Naturalne zastosowanie |
|---|---|---|---|
| **UD — dochodowa** | mediana dochodu z pracy na godzinę w obszarze walutowym umowy (PL: GUS+ZUS+Eurostat, mediana z ≥2 źródeł) | stały udział zobowiązania w typowym dochodzie | kredyty hipoteczne, długi wieloletnie, czynsze |
| **UK — konsumpcyjna** | koszyk kosztów życia z mieszkaniem (CPI + imputowany koszt mieszkania, mediana z niezależnych pomiarów) | siłę nabywczą konsumenta | emerytury, alimenty, renty, płaca minimalna |
| **UM — majątkowa** | szeroki koszyk aktywów (akcje świat + obligacje + nieruchomości), wolno rebalansowany jawną regułą | dostęp do zakumulowanego bogactwa | oszczędności długoterminowe, wyceny międzypokoleniowe |
| **UZ — zasobowa (≈AUV)** | koszyk surowców / UD — czyli obecny AUV z poprawionym mianownikiem | pracochłonność dóbr pierwotnych | kontrakty B2B surowcowo skorelowane; **miernik analityczny** |

Zasady rodziny:

1. **Umowa deklaruje jednostkę albo miks** (np. emerytura: 70% UK + 30% UD — chroni koszty życia i partycypuje we wzroście). Standaryzujemy *menu*, nie odpowiedź. To rozbraja problem heterogeniczności z §1(2).
2. **Kursy wymiany między jednostkami publikowane codziennie** — dzięki temu zobowiązanie w UD można wycenić w UK itd.; rodzina zachowuje spójność księgową.
3. **Każda jednostka regionalna tam, gdzie trzeba.** Lekcja z oceny AUV: mianownik światowy indeksuje polską ratę do kursu dolara i wzrostu Chin. UD jest per obszar walutowy; UZ może zostać globalna (to jej sens).

„Miernik wszelkich wartości" w jedynym osiągalnym sensie to **wektor (UD, UK, UM, UZ)** plus reguły konwersji — nie skalar.

---

## 4. Warstwa zaufania: determinizm jako kajdany instytucji, nie jej brak

Ocena AUV pokazała, że „bez autorytetu" jest prawnie (BMR) i operacyjnie (nikiel 2022) niewykonalne. Ale ideał heliocentryczny da się uratować w mocniejszej formie: **instytucja istnieje, lecz jest skuta regułą** — każdy może zweryfikować, że nie miała pola manewru.

Komponenty (wszystkie mają precedensy):

- **Administrator-fundacja non-profit** z autoryzacją BMR; statut zakazuje zmian formuły bez procedury (wzór: ICE Benchmark Administration po LIBOR, ale z open source).
- **Kod = metodologia.** Formuła opublikowana jako wykonywalny, wersjonowany kod; publikacja dnia = hash danych wejściowych + wynik; każdy odtwarza wynik lokalnie. (Tu Twój projekt już jest — to jego realna przewaga.)
- **Dane z medianny ≥3 niezależnych źródeł** na każdą serię; winsoryzacja ruchów ekstremalnych zapisana z góry (odpowiedź na nikiel-2022 *w kodzie*, nie w komitecie).
- **Reguły awaryjne à la ISDA fallbacks:** z góry zdefiniowana kaskada — źródło znika → substytut → zamrożenie → procedura rewizji z chain-linkingiem i testem nakładania (Twoja Część II jest tu dobra i zostaje).
- **Pre-commitment publikacyjny jak UF:** wartości jednostek na miesiąc naprzód, nigdy rewidowane wstecz; rewizje danych źródłowych wchodzą wyłącznie w przyszłe odczyty (to rozcina problem „która liczba wiąże kontrakt").
- **Rada rewizyjna wieloośrodkowa** (akademia + strony rynku + audytor), której jedyna kompetencja to stwierdzanie, czy kryteria zapisane z góry zostały spełnione — nigdy jaki ma być wynik.

To jest „authority-lite": zaufanie nie do osądu instytucji, lecz do niemożności jej odchylenia się od reguły. Różnica względem GUS/RPP nie polega na braku instytucji, tylko na **weryfikowalności każdego kroku**.

---

## 5. Co pozostaje nierozwiązywalne (i musi być jawnie w umowach)

- **Rewizje danych źródłowych** — minimalizowane medianą źródeł i pre-commitmentem, ale nieusuwalne. Umowa musi wskazywać: wiąże wartość opublikowana, nie „prawdziwa".
- **Refleksywność przy masowej adopcji** — UD ma tu najlepszą pozycję (trudno „manipulować medianą dochodów" inaczej niż realną polityką), UM najgorszą (aktywa same reagują na indeksację).
- **Ryzyko polityczne** — państwo może zdelegalizować indeksację (Argentyna zakazywała indeksacji wielokrotnie; USA zakazały klauzul złota 1933–1977). Żadna konstrukcja indeksu tego nie obchodzi; dywersyfikacja jurysdykcyjna administratora łagodzi, nie usuwa.
- **Ryzyko idiosynkratyczne stron** — jednostka wyrównuje względem agregatu; osobisty los (utrata pracy, choroba) pozostaje po stronie ubezpieczeń, nie indeksacji. To feature, nie bug — ale trzeba to komunikować.

---

## 6. Ścieżka wdrożenia (od najtańszego kroku)

1. **Przebuduj projekt wokół UD** (mediana dochodu godzinowego PL / strefa euro; źródła: GUS struktura wynagrodzeń, ZUS dane administracyjne, Eurostat SES). AUV → UZ: satelita analityczny z poprawionym mianownikiem (= UD zamiast PKB/os. w USD — usuwa efekt kursowy i częściowo endogeniczność).
2. **Publikuj rodzinę jako indeksy analityczne** (bez umów): buduje historię, cytowalność, zaufanie. Minimum 3–5 lat nieprzerwanej publikacji zanim ktokolwiek podpisze kontrakt — tak budowały wiarygodność UF i TIPS.
3. **Pierwsze kontrakty B2B** między stronami kwalifikowanymi (poza pełnym rygorem BMR — do weryfikacji prawnej): czynsze komercyjne w UD, kontrakty surowcowe w UZ.
4. **Pilotaż z funduszem emerytalnym**: obligacja korporacyjna lub list zastawny indeksowany UD — test tezy o naturalnym nabywcy.
5. **Autoryzacja BMR i produkty detaliczne** — dopiero na końcu, z historią i kontrahentami.

---

## 7. Podsumowanie w trzech zdaniach

Jednostka „wszelkich wartości" jest niemożliwa z powodów twierdzeniowych, nie inżynierskich — osiągalny jest **standard rodziny jednostek** (dochodowa, konsumpcyjna, majątkowa, zasobowa) z jawną konwersją i wspólną warstwą zaufania. Rdzeniem kontraktowym powinna być **jednostka dochodowa** (mediana dochodu z pracy), bo jako jedyna utrzymuje zobowiązania w stałej proporcji do zdolności ich obsługi i ma naturalnego kontrahenta hedgingowego w funduszach emerytalnych. Heliocentryczność przeżywa w formie „instytucji skutej regułą": nie brak autorytetu, lecz autorytet, którego każdy krok jest odtwarzalny z opublikowanego kodu i danych.
