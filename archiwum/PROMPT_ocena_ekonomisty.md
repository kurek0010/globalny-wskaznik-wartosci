## Prompt do krytycznej oceny AUV przez inny model (rola: praktyczny ekonomista)

Skopiuj wszystko poniżej linii do modelu oceniającego. Dołącz też pliki projektu, jeśli możesz (PODSUMOWANIE_DLA_EKSPERTA.md, AUV_niezmienniczosc_i_rewizja.md, AUV_instrument_i_waluta.md, kod w prototyp/src/) — ale prompt jest napisany tak, by działać nawet bez nich.

---

Wciel się w rolę **doświadczonego ekonomisty praktyka** — kogoś, kto projektował lub oceniał realne instrumenty finansowe i indeksy (banki centralne, urzędy statystyczne, izby rozliczeniowe, zespoły produktowe funduszy). Twoim zadaniem nie jest pochwała ani teoretyczne dłubanie, lecz **znalezienie luk, które podważają praktyczną użyteczność** poniższego pomysłu. Podchodź życzliwie, ale bezlitośnie wobec słabości: zakładaj, że autor woli usłyszeć twardą prawdę teraz niż po wdrożeniu.

### Zasady oceny (przestrzegaj ściśle)
1. **Zero pochlebstw i zero rytualnej krytyki.** Nie chwal, żeby złagodzić. Nie krytykuj, żeby zabrzmieć surowo. Każde zdanie ma nieść informację.
2. **Steelman, potem atak.** Zanim wskażesz słabość, przedstaw najmocniejszą wersję pomysłu, żeby nie bić w chochoła.
3. **Powołuj się na rzeczywiste dane i epizody.** Każdą lukę poprzyj konkretem: prawdziwe szeregi (ceny surowców, płace, kursy, CPI, PKB), realne instrumenty (chilijska UF, TIPS, SDR), realne wydarzenia (szok naftowy 2008/2022, deflacja Japonii, rewizje PKB). Jeśli masz dostęp do danych/narzędzi — zweryfikuj liczbowo. Jeśli nie — podaj konkretne liczby z wiedzy i wyraźnie zaznacz, co wymaga sprawdzenia.
4. **Kwantyfikuj skutek.** Nie „to może być zmienne", lecz „w 2022 ta pozycja skoczyłaby o X%, co dla kredytu Y oznacza Z".
5. **Oddziel luki FATALNE (podważają sens) od NAPRAWIALNYCH (wymagają pracy).** Uszereguj wg wagi.
6. **Myśl scenariuszami użycia.** Prześledź, co realnie stanie się, gdy: kredytobiorca weźmie 25-letni kredyt w tej jednostce; firma zacznie płacić w niej pensje; instytucja zechce ją zmanipulować; źródło danych zniknie; jednostka zyska masową adopcję.

### Kontekst — pomysł do oceny (AUV: Absolute Unit of Value)

**Cel.** Deterministyczna jednostka wartości niezależna od decyzji jakiegokolwiek autorytetu (banków centralnych, urzędów statystycznych), liczona jawną formułą z otwartych danych. Dwa zastosowania: (a) indeksacja umów wieloletnich (zamiast WIBOR/CPI), (b) pomiar realnej wartości oszczędności.

**Formuła.** Dla koszyka 19 surowców w 4 kategoriach (energia, żywność, metale, budownictwo) liczy się indeks cen jako średnią geometryczną (znormalizowaną do roku bazowego), a następnie dzieli przez światowy dochód na osobę (PKB/populacja, też znormalizowany):

  AUV(t) = [koszyk_cen(t) / koszyk_cen(t0)] / [dochód_pc(t) / dochód_pc(t0)] × 100

Kluczowa idea: dzielenie ceny (w USD) przez dochód (w USD) kasuje walutę — wynik jest w „godzinach pracy" (pracochłonności nabycia koszyka), a nie w pieniądzu.

**Główne wyniki empiryczne (dane 1996–2025).**
- AUV zmienił się o **+0,4%** w 30 lat, przy wzroście M2 USA o **+489%**, CPI USA o +105%, nominalnego koszyka o +149%, dochodu/os. o +148%.
- AUV jest cykliczny (zakres ~77–148), a wychylenia pokrywają się z cyklem surowcowym (szczyty 2008, 2022; dołki 2001, 2015–2020).
- Odporność: przy 1000 losowych zestawów wag koszyka AUV 2025 mieści się w 75–127 (nigdy blisko M2). Korelacja przyrostów z M2: 0,1–0,3.
- Wątek monetarny: *kierunek* inflacji zależy od rodzaju kolateralu (dług państwa → CPI +0,41; hipoteka → ceny domów +0,58, nie CPI), ale po kontroli na M2 kolateral nie wnosi istotnie ponad ilość pieniądza (Granger). Bilans BoJ ×9, inflacja Japonii +1,3%.
- Wariant kontraktowy (wygładzony 5-letnio): maks. zmiana roczna spada z 52% do 12% (CPI: 8%, i CPI prawie nie spada).
- Przelicznik walutowy: by utrzymać stałą realną wartość, trzeba do 2025 +95% więcej CHF, ale +238% więcej JPY.

**Deklarowane własności teoretyczne.**
- *Niezmienniczość względem numéraire:* AUV to iloraz bezwymiarowy, więc daje ten sam wynik w każdej walucie, a nawet bez walut (z ilości fizycznych i cen względnych).
- *Niezmienniczość reprezentacji:* kategorie są szkieletem, serie w nich wymienne; rewizja koszyka przez łączenie łańcuchowe (chain-linking) + reguła (obiektywne kryteria, ogłaszanie z wyprzedzeniem, brak rewizji wstecz).

**Model publikacji.** Miesięczna kotwica (pełne dane) + żywe ceny dzienne (surowce, FX) + wolny mianownik (dochód) zamrożony między rocznymi odczytami; publikacja z wyprzedzeniem, bez rewizji wstecznej (jak UF).

### Ograniczenia, które autor JUŻ zna (nie powtarzaj ich — idź głębiej i oceń, czy jego mitygacje realnie działają)
- Endogeniczność mianownika: PKB zawiera wartość dodaną surowców z licznika.
- Produkcja użyta jako proxy konsumpcji per capita; część danych produkcji przybliżona.
- Wątek jakości pieniądza tylko dla USA; wagi jakości normatywne.
- Poziom AUV w danym roku zależy od wyboru roku bazowego (dryf jest niezmienniczy, poziom nie).
- Refleksywność przy masowej adopcji.
- Kompromis: surowy AUV jest cykliczny, wygładzony — mniej niż CPI.

### Czego od Ciebie oczekuję
Znajdź luki **poza** powyższą listą — zwłaszcza takie, które **podważają praktyczność**. Kandydaci do rozważenia (nie ograniczaj się do nich): rewizje danych PKB przez urzędy vs deklaracja „nigdy nie rewidujemy" i „niezależność od autorytetu"; ryzyko bazowe nogi dochodowej dla jakiegokolwiek instrumentu; przeniesienie ryzyka cyklu surowcowego na kredytobiorcę o nominalnym dochodzie; problem adopcji i efektu sieci (jednostka rachunkowa bez mandatu); akceptacja prawna/podatkowa/księgowa; governance rewizji (kto i jak, odporność na przechwycenie); podatność koszyka na gaming; czy „realna wartość" jest w ogóle dobrze zdefiniowana; opóźnienia i kompletność danych w czasie rzeczywistym; wrażliwość na dobór kategorii i brak usług/mieszkań w koszyku.

**Dla każdej znalezionej luki podaj:** (1) mechanizm — dlaczego to problem; (2) dowód/ilustracja na rzeczywistych danych lub epizodzie, z liczbami; (3) konkretny scenariusz, w którym to boli; (4) czy luka jest fatalna czy naprawialna; (5) jeśli naprawialna — najtańsza sensowna naprawa i jej koszt/kompromis.

### Format odpowiedzi
1. **Werdykt w 3 zdaniach:** czy pomysł jest praktycznie wdrażalny, w jakim wariancie, a w jakim nie.
2. **Luki uszeregowane od najcięższej:** dla każdej pełny rozbiór wg pięciu punktów wyżej.
3. **Test kontraktowy:** prześledź jeden realny 25-letni kredyt hipoteczny indeksowany do AUV, rok po roku na danych 1996–2025 — co realnie działoby się z ratą kredytobiorcy o nominalnej pensji? Podaj liczby.
4. **Trzy pytania**, na które autor musi odpowiedzieć, zanim pomysł da się traktować poważnie w praktyce.
5. Wyraźnie oddziel **fakty/dane** od **swoich opinii**.

Bądź konkretny. Ogólniki są tu bezużyteczne.
