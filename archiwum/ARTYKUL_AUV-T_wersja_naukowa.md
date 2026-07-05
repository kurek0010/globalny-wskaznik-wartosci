# AUV-T: jednostka wartości w numéraire czasu pracy. Nota metodologiczna i wstępne wyniki empiryczne

**Autor projektu:** Mariusz Kurowski
**Wersja:** v0.4 (robocza)
**Okres danych:** 1996–2025
**Status:** projekt badawczy we wczesnej fazie; wyniki ilustrują metodę, nie stanowią rekomendacji finansowej.

## Streszczenie

Przedstawiamy AUV-T (*Absolute Unit of Value, time-denominated*) — deterministyczny indeks realnej wartości koszyka surowców, w którym jednostką odniesienia (numéraire) nie jest waluta, lecz ludzki czas pracy aproksymowany dochodem na osobę. Konstrukcja polega na podzieleniu zagregowanej ceny koszyka surowców przez dochód globalny na osobę, co eliminuje wymiar walutowy i wyraża wynik w jednostkach względnej pracochłonności. Na danych z lat 1996–2025 AUV-T nie wykazuje istotnego dryfu długoterminowego (zmiana +0,4% przy nominalnym wzroście koszyka o ~150% i wzroście agregatu M2 USA o 489%), wykazuje natomiast wyraźną komponentę cykliczną o okresie ~10 lat, skorelowaną z cyklem surowcowym. Wskazujemy, że własność braku dryfu czyni AUV-T kandydatem na miarę realnej wartości, podczas gdy amplituda cyklu ogranicza obecnie jego zastosowanie jako jednostki indeksacyjnej w kontraktach.

## 1. Motywacja i hipoteza

Wskaźniki wartości wyrażone w pieniądzu papierowym są obciążone zmianą siły nabywczej tego pieniądza w czasie. Deflacja indeksem cen konsumpcyjnych (CPI) usuwa ten problem tylko częściowo, ponieważ CPI jest ilorazem cen dóbr względem cen innych dóbr — obie wielkości podlegają wspólnemu wpływowi ekspansji monetarnej. Formalnie, jeśli wszystkie obserwowane ceny są denominowane w jednostce monetarnej, to dowolna ich kombinacja liniowa również jest denominowana w tej jednostce; nie istnieje wewnątrz tego zbioru kombinacja niezależna od stanu pieniądza.

Hipoteza projektu głosi, że wyjście z tej zależności wymaga numéraire spoza zbioru wielkości monetarnych. Jako taki numéraire przyjmujemy ludzki czas pracy. Uzasadnienie ma dwa filary. Po pierwsze, czas pracy jest wielkością fizyczną, której podaży nie można powiększyć operacją księgową — w przeciwieństwie do agregatów monetarnych. Po drugie, iloraz dwóch wielkości wyrażonych w tej samej walucie (cena dobra oraz dochód z pracy) jest bezwymiarowy względem waluty i może być interpretowany w jednostkach czasu (liczba godzin pracy potrzebna do nabycia dobra). Koncepcja nawiązuje do klasycznej teorii wartości opartej na pracy oraz do współczesnej literatury *time prices*.

## 2. Definicja formalna

Niech *t* oznacza rok, a *t₀* = 1996 rok bazowy. Dla pojedynczej serii cenowej *p* definiujemy normalizację

```
p̃(t) = p(t) / p(t₀) × 100.
```

Koszyk dzielimy na *K* = 5 kategorii (energia, żywność, metale przemysłowe, budownictwo oraz — docelowo — materiały krytyczne). Indeks kategorii *c* złożonej z dóbr *i ∈ c* jest średnią geometryczną znormalizowanych cen:

```
C_c(t) = exp( (1/|c|) · Σ_{i∈c} ln p̃_i(t) ).
```

Wybór średniej geometrycznej jest celowy: jest ona odporna na pojedyncze ekstremalne odchylenia i symetryczna względem wzrostów oraz spadków (równe co do wartości bezwzględnej zmiany logarytmiczne znoszą się). Zagregowany indeks koszyka jest średnią geometryczną indeksów kategorii z wagami równymi:

```
B(t) = exp( (1/K) · Σ_{c} ln C_c(t) ).
```

Mianownik — cena pracy cywilizacji — w wersji liczalnej na dostępnych danych jest światowym dochodem nominalnym na osobę, znormalizowanym do roku bazowego:

```
Y(t) = [ PKB_świat(t) / Populacja(t) ] / [ PKB_świat(t₀) / Populacja(t₀) ] × 100.
```

Indeks AUV-T definiujemy jako

```
AUV-T(t) = B(t) / Y(t) × 100.
```

Ponieważ B i Y są w tej samej walucie (USD bieżące), wymiar walutowy znosi się; AUV-T jest wielkością względną interpretowaną jako pracochłonność nabycia koszyka, odniesioną do roku bazowego.

## 3. Dane

Zbiór obejmuje 19 serii cenowych w czterech zaimplementowanych kategoriach: energia (ropa Brent, gaz ziemny, węgiel, uran), żywność (pszenica, kukurydza, ryż, soja, olej palmowy), metale przemysłowe (miedź, aluminium, ruda żelaza, nikiel, cynk, ołów, cyna), budownictwo (stal, cement). Źródła to publiczne API: FRED (w tym serie cen globalnych MFW oraz indeksy PPI), World Bank Open Data, ECB SDW, NBP. Mianownik korzysta ze światowego PKB w cenach bieżących oraz populacji świata (World Bank). Wszystkie serie sprowadzono do częstotliwości miesięcznej, a następnie zagregowano do rocznych średnich. Przyjęta filozofia danych wyklucza źródła subskrypcyjne oraz wielkości ustalane uznaniowo, na rzecz danych otwartych i odtwarzalnych.

Ograniczenie jakości danych: ceny stali i cementu pochodzą z amerykańskich indeksów producenckich (PPI) użytych jako przybliżenie cen globalnych, ponieważ otwarta, długookresowa seria cen światowych dla tych dóbr nie jest dostępna. Indeksy PPI charakteryzuje większa „lepkość" niż ceny spot, co może zaniżać mierzoną zmienność tej kategorii. Wpływ na poziom indeksu jest neutralizowany przez normalizację do roku bazowego.

## 4. Wyniki empiryczne

W okresie 1996–2025 zmiany skumulowane wynoszą: koszyk nominalny **+149,3%**, agregat M2 USA **+489,0%**, CPI USA **+105,3%**, dochód globalny na osobę **+148,3%**. Wynikowy AUV-T zmienia się o **+0,4%**. Brak istotnego dryfu długoterminowego oznacza, że realna pracochłonność koszyka dóbr podstawowych na koniec okresu jest zbliżona do wartości z roku bazowego. Bliska równość dynamiki koszyka nominalnego (+149,3%) i dochodu na osobę (+148,3%) wskazuje, że nominalne ceny surowców i nominalne dochody rosły niemal proporcjonalnie, a ich iloraz neutralizuje wspólną komponentę monetarną.

AUV-T wykazuje wyraźną komponentę cykliczną: lokalne maksimum w 2008 r. (~148) oraz minimum w latach 2015–2020 (~85–90), z rozpiętością min–max rzędu 91% i odchyleniem standardowym rocznych zmian logarytmicznych równym 0,152. Fazy te pokrywają się z cyklem surowcowym (boom popytowy do 2008 r., korekta po kryzysie finansowym, załamanie cen energii 2014–2015, szok podażowy 2022). Wygładzenie kroczącą średnią geometryczną 7-letnią obniża odchylenie standardowe do 0,046 (redukcja ~70%), lecz rozpiętość min–max pozostaje rzędu 56%, co potwierdza, że dominująca zmienność ma charakter niskoczęstotliwościowego cyklu, a nie szumu wysokoczęstotliwościowego.

W dekompozycji kategorialnej (w jednostkach czasu pracy) żywność wykazuje spadek o ~46% w okresie, energia i metale wzrost rzędu +35% każda, budownictwo zmianę o ~+4%. Dodanie kategorii budownictwa do koszyka obniża odchylenie standardowe rocznych zmian indeksu (z 0,179 do 0,152), co jest spójne z efektem dywersyfikacji.

Jako komparator zewnętrzny konstruujemy syntetyczny indeks inflacji SDR jako ważoną (wagami koszyka MFW z rewizji 2022, zamrożonymi) średnią geometryczną CPI pięciu walut składowych. SDR rośnie w okresie o **+90,5%**, co potwierdza, że koszyk walutowy — mimo statusu „neutralnej" jednostki rozrachunkowej — podlega wspólnej deprecjacji składników i nie pełni funkcji kotwicy realnej.

## 5. Interpretacja

Wyniki sugerują rozdzielenie dwóch funkcji wskaźnika. Po pierwsze, jako **miara realnej wartości**, AUV-T jest informatywny: brak dryfu długoterminowego stanowi empiryczną odpowiedź na pytanie o realną zmianę zasobochłonności cywilizacji (w ujęciu na jednostkę pracy zbliżona do stałej), a komponenta cykliczna niesie informację o naprzemiennych fazach względnej obfitości i niedoboru zasobów. Znak indeksu rozróżnia typy szoków: niskie wartości odpowiadają fazom deflacyjnym (wzrost realnej siły nabywczej dochodu wobec zasobów), wysokie — fazom podażowo-inflacyjnym (spadek tej siły).

Po drugie, jako **jednostka indeksacyjna** w kontraktach wieloletnich, AUV-T w obecnej postaci jest ograniczony amplitudą cyklu. Wygładzanie redukuje zmienność rok-do-roku, lecz kosztem opóźnienia i bez eliminacji cyklu dekadowego. Osiągnięcie gładkości wymaganej dla indeksacji wymagałoby albo formalnej dekompozycji na trend (jednostka kontraktowa) i cykl (wskaźnik napięcia zasobowego), albo modyfikacji licznika w kierunku szerszego, mniej zdominowanego cenami spot koszyka.

## 6. Ograniczenia i kierunki dalszych prac

Główne ograniczenia metodologiczne są następujące. Mianownik aproksymuje cenę pracy dochodem na osobę, a nie dochodem na godzinę przepracowaną; wpięcie danych o nakładzie pracy (np. produktywność z baz OECD/Conference Board/Penn World Table) pozwoli uściślić interpretację. Występuje potencjalna endogeniczność: PKB w mianowniku zawiera wartość dodaną tych samych surowców, które tworzą licznik, co wymaga formalnego zbadania. Wagi koszyka i kategorii są równe i zamrożone; alternatywą jest ważenie wartością produkcji, wymagające danych o wolumenach. Komparator SDR przyjmuje stałe wagi dla całego okresu, mimo że skład koszyka MFW zmieniał się (włączenie CNY w 2016 r.). Pokrycie CPI obejmuje obecnie osiem walut.

Dalsze prace obejmą: (i) formalną separację trendu i cyklu, (ii) test wariantów mianownika (dochód na godzinę, PPP vs ceny bieżące), (iii) rozszerzenie koszyka o materiały krytyczne oraz weryfikację wrażliwości na skład i wagi, (iv) konfrontację z literaturą dotyczącą realnych cen surowców deflowanych płacą.

## 7. Odtwarzalność

Indeks jest w pełni deterministyczny: dane wejściowe, kod obliczeniowy i parametry (skład koszyka, wagi, rok bazowy) są jawne i zamrożone w repozytorium. Każdy posiadający te same dane uzyskuje identyczny wynik bez konieczności uzyskiwania zgody autora. Ewentualne zmiany reguł podlegają jawnej, ogłoszonej procedurze rewizji, a nie uznaniowej decyzji po obserwacji wyników.
