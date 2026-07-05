# Working paper — szkielet

**Tytuł roboczy (PL):** *Miara realnego kosztu zasobów cywilizacji: jednostka wartości niezależna od waluty i dekompozycja inflacji na kierunek i skalę*
**Tytuł roboczy (EN):** *Measuring the real resource cost of civilization: a currency-invariant value unit and a direction-vs-scale decomposition of inflation*

**Uwaga o pozycjonowaniu (po ocenie zewnętrznej 2026-07):** artykuł prezentuje AUV jako **miarę** realnej wartości/kosztu zasobów (i realnego postępu), NIE jako stałą jednostkę indeksacyjną. Backtest stuletni wskazuje wieloletni *spadek* AUV (zasoby tanieją względem dochodu — sygnał postępu), więc obietnica „stałej wartości" zostaje świadomie porzucona. Zastosowanie kontraktowe — jeśli w ogóle — to odległa nisza (patrz `ODPOWIEDZ_na_ocene.md`).

**Autor:** Mariusz Kurowski
**Wersja:** szkielet 0.1 (2026-06-22)
**Repozytorium / dane / kod:** publiczne, w pełni odtwarzalne (heliocentryczność).

---

## Uwaga o strukturze (do decyzji przed pisaniem)

Materiał dzieli się na dwa wkłady, które można złożyć w **jeden** artykuł albo rozdzielić na **dwa**:

- **Wkład A — jednostka wartości (AUV-T).** Pomiarowy: jak mierzyć realną wartość bez numéraire pieniężnego.
- **Wkład B — kierunek vs skala inflacji.** Empiryczny monetarny: rodzaj kolateralu steruje *kierunkiem* inflacji, ilość pieniądza — *skalą*.

Rekomendacja: **jeden artykuł**, gdzie B jest *motywacją i dowodem potrzeby* A (skoro CPI jest ślepy na inflację aktywów, potrzebna jest jednostka niezależna od kanału). Poniższy szkielet zakłada wariant jednoartykułowy; sekcja 5 może zostać wydzielona jako companion paper, jeśli recenzent uzna całość za zbyt obszerną.

---

## Abstrakt (szkic do dopracowania)

Konstruujemy deterministyczną miarę realnej wartości (AUV), w której numéraire nie jest waluta, lecz dochód: zagregowana cena koszyka surowców dzielona przez dochód na osobę. Dzielenie dwóch wielkości w tej samej walucie eliminuje wymiar monetarny; wynik interpretujemy jako realny koszt zasobów w jednostkach dochodu. Miara jest niezmiennicza względem waluty (Cz. teoretyczna) i odporna na wybór koszyka, wag i agregacji (Monte Carlo). Na danych 1996–2024 AUV zmienia się realnie o ~+5% mimo wzrostu M2 o 489% i jest odsprzężony od podaży pieniądza — co czyni go użytecznym komparatorem demaskującym iluzję monetarną. Zarazem backtest w skali stulecia wskazuje wieloletni *spadek* AUV (zasoby tanieją względem dochodu), co identyfikujemy jako sygnał realnego postępu, nie jako własność stałej jednostki. Głównym wkładem empirycznym monetarnym jest wykazanie, że *rodzaj* kreacji pieniądza steruje *kierunkiem* inflacji (dług państwowy → ceny konsumenckie; kredyt hipoteczny → ceny aktywów), podczas gdy *skalę* wyznacza ilość szerokiego pieniądza, a nie baza monetarna (naturalny eksperyment: bilans BoJ ×9 przy ~zerowej inflacji). Ponieważ CPI z konstrukcji nie obejmuje inflacji aktywów, AUV dostarcza pomiaru realnej wartości niezależnego od kanału kreacji pieniądza — jego wartość leży w pomiarze i demaskowaniu iluzji monetarnej, nie w obietnicy stałości.

---

## 1. Wprowadzenie

- Problem: pieniądz jako ruchoma miara wartości; nie da się odróżnić realnej zmiany wartości od deprecjacji jednostki.
- Luka: deflacja CPI usuwa problem tylko częściowo (cena/cena, wewnątrz fiat) i pomija inflację aktywów.
- Wkład 1: miara realnego kosztu zasobów niezależna od waluty — wychodzi z pętli fiat (iloraz dwóch wielkości w tej samej walucie jest bezwymiarowy względem waluty). Interpretacja: realny koszt zasobów cywilizacji; jego wieloletni spadek = miara postępu, nie stałość.
- Wkład 2: dekompozycja inflacji na kierunek (kolateral) i skalę (ilość) — empiryczna motywacja dla wkładu 1.
- Wkład 3 (metodologiczny): pełna odtwarzalność (heliocentryczność) — kod, dane, zamrożone parametry, jawna reguła rewizji.
- Wkład 4 (teoretyczny): **dwie niezmienniczości** — względem numéraire (AUV działa bez żadnej waluty, nawet w granicy ich zniknięcia) i względem reprezentacji (AUV przeżywa rotację/utratę serií dzięki szkieletowi kategorii + łączeniu łańcuchowemu). To odróżnia AUV od wszystkich dotychczasowych jednostek indeksacyjnych. Pełny dowód: `AUV_niezmienniczosc_i_rewizja.md`.
- Zajawka wyników i mapa artykułu.

## 2. Powiązania z literaturą

- Klasyczna teoria wartości opartej na pracy (Smith — „praca pierwotnym pieniądzem nabywczym"; Ricardo).
- *Time prices* / Superabundance (Tupy & Pooley 2022) — pomiar w godzinach pracy.
- Realne ceny surowców: indeks Grilli-Yang; Jacks (real commodity prices over three centuries); deflacja płacą.
- Teoria ilościowa pieniądza; szeroki vs bazowy pieniądz; pułapka płynności (Japonia).
- Teoria „pokrycia" pieniądza / jakości kolateralu; dominacja fiskalna; inflacja aktywów (pominięcie w CPI).
- *Pozycjonowanie:* czym nasza jednostka różni się od time prices (koszyk + numéraire dochodu, nie pojedyncze dobra) i od indeksów realnych cen surowców (interpretacja jako jednostka wartości, nie deflator).

### 2.1 Rzeczywiste próby rozwiązania podobnego problemu (przegląd i porównanie)

Kluczowe dla wykazania wkładu: pokazać, że problem „jednostki wartości niezależnej od deprecjacji pieniądza" był podejmowany wielokrotnie, a AUV łączy zalety, których poprzednicy nie mieli razem.

- **Unidad de Fomento (Chile, 1967–)** — jednostka indeksowana krajowym CPI, publikowana dziennie, szeroko używana (kredyty, umowy, oszczędności). *Zaleta:* dojrzała, gładka, sprawdzona 55+ lat. *Ograniczenie:* zależy od urzędu statystycznego (CPI = decyzje metodologiczne, korekty hedoniczne, presja polityczna), krajowa (peso), ślepa na inflację aktywów, wciąż w pętli fiat (cena/cena).
- **TIPS / OAT€i / linkers** — obligacje indeksowane krajowym CPI. Te same ograniczenia CPI-zależności co UF.
- **SDR (MFW)** — koszyk pięciu walut. *Ograniczenie:* to nadal fiat (empirycznie dryfuje +90% w naszych danych), wagi ustala Zarząd MFW (uznaniowość).
- **Standard złota / pieniądz towarowy** — kotwica obiektywna, ale jednosurowcowa, zmienna, z tendencją deflacyjną.
- **„Bancor" Keynesa (1944)** — proponowana międzynarodowa jednostka wiązana z koszykiem surowców; nigdy nie wdrożona. AUV jest nowoczesną, policzalną realizacją podobnej ambicji.
- **Stablecoiny** — pegowane do fiat (USD) lub algorytmiczne (Terra/Luna — spektakularna porażka pegu bez pokrycia).
- **Indeksy cen surowców (CRB, GSCI, Grilli-Yang)** — mierzą ceny surowców, ale nie są jednostką wartości; nie dzielą przez dochód/pracę.

**Tabela pozycjonująca** (do artykułu): oceny wg czterech własności, których pełen komplet ma tylko AUV.

| Rozwiązanie | Niezależne od autorytetu | Globalne / bez-numéraire | Łapie realną wartość (nie tylko CPI) | Zakotwiczone w wielkościach fizycznych |
| --- | --- | --- | --- | --- |
| UF / TIPS (CPI) | nie | nie | nie | nie |
| SDR | nie | częściowo | nie | nie |
| Standard złota | tak | częściowo | częściowo | tak (1 dobro) |
| Indeksy surowców | tak | częściowo | częściowo | tak |
| Stablecoin (fiat/algo) | nie | nie | nie | nie |
| **AUV** | **tak** | **tak** | **tak** | **tak** |

## 3. Dane i metoda

- Źródła (wyłącznie otwarte): FRED, World Bank, ECB SDW, NBP; dane ręczne USGS/World Steel dla produkcji.
- Koszyk: 19 cen w 4 kategoriach (energia, żywność, metale, budownictwo); tabela serii i jednostek.
- Formuła AUV-T: normalizacja do bazy, średnia geometryczna w kategoriach i między nimi, mianownik = dochód na jednostkę pracy. Równania.
- Zasady heliocentryczne wymuszone w kodzie: determinizm, zamrożone parametry, jawna reguła roku bazowego.
- Uwaga o aproksymacji danych produkcji (do zastąpienia zweryfikowanymi — patrz limitacje).

## 3a. Teoria: dwie niezmienniczości (Wkład 4)

Sekcja podbudowująca poprawność i trwałość metody. Pełne wyprowadzenie: `AUV_niezmienniczosc_i_rewizja.md`.

- **Niezmienniczość względem numéraire.** AUV to iloraz stosunków wzrostu (bezwymiarowy), więc daje ten sam wynik niezależnie od waluty; w granicy zniknięcia walut liczy się z ilości fizycznych i cen względnych — staje się *naturalnym* numéraire. Dowód przez kasowanie czynnika przeliczeniowego. Zastrzeżenie: refleksywność → wymóg zakotwiczenia w wielkościach fizycznych.
- **Niezmienniczość reprezentacji.** Kategorie (energia, żywność, metale, budownictwo, materiały krytyczne) są niezmiennym szkieletem; serie w ich obrębie są wymiennymi proxy. Rewizja koszyka przez łączenie łańcuchowe (chain-linking) zachowuje ciągłość; reguła rewizji (obiektywne kryteria, ogłoszenie z wyprzedzeniem, automatyczne wypadanie, redundancja, brak rewizji wstecz, test nakładania) czyni zmiany odpornymi na manipulację.
- **Znaczenie:** AUV nie zależy ani od żadnej waluty, ani od żadnego pojedynczego dostawcy danych — co odróżnia go od UF/TIPS/SDR i odpowiada na dwie główne obiekcje (co, gdy waluta odniesienia traci sens? co, gdy źródło danych znika?).

## 4. AUV-T: wyniki (Wkład A)

- 4.1 Główny wynik: AUV-T +0,4% vs M2 +489%, CPI +105%, dochód +148% (rok 1996→2025). [Fig. 30, 31; Tab. wyników]
- 4.2 SDR jako komparator: +90% — „neutralna" jednostka MFW też dryfuje (jest z fiat). [Fig. 31]
- 4.3 Odporność na mianownik: na osobę vs na pracownika (różnica nieistotna). [Fig. 34]
- 4.4 Dekompozycja trend/cykl: gładki rdzeń + cykl jako wskaźnik napięcia zasobowego. [Fig. 32]
- 4.5 Walidacja wrażliwości: leave-one-out, Monte Carlo wag (1000), geom vs aryt, rok bazowy — wynik niezależny od arbitralnych wyborów. [Fig. 40; Tab.]
- 4.6 Interpretacja potrzeb: koszt utrzymania człowieka — przetrwanie (+0,4%) vs standard (+59%); rozplątanie tautologii „potrzeba = konsumpcja". [Fig. 33]

## 5. Kierunek vs skala inflacji (Wkład B)

- 5.1 Kierunek: korelacje i funkcje korelacji krzyżowej — hipoteka → ceny domów (+0,58), dług państwa → CPI (+0,41), nie odwrotnie. [Fig. 36–39; Tab.]
- 5.2 Skala ponad ilość: Granger + regresja przyrostowa z kontrolą na M2 (Newey-West) — kolateral nie wnosi istotnie ponad M2; rządzi ilość. [Fig. 41]
- 5.3 Naturalny eksperyment: bilanse banków centralnych USA/EBC/BoJ — ×9 baza, inflacja +79/+73/+1,3%. Baza monetarna nie napędza CPI; liczy się transmisja przez M2/kredyt. [Fig. 43]
- 5.4 Wniosek: CPI pomija inflację aktywów → indeksacja na CPI niepełna → potrzeba jednostki niezależnej od kanału (powrót do Wkładu A).

## 6. Zastosowanie kontraktowe

- Wariant kontraktowy AUV: szeroki koszyk + zamrożone reguły (baza, wygładzanie). Maks. zmiana roczna 52%→12%. [Fig. 42]
- Kompromis: realna wartość bez dryfu fiat vs gładkość CPI; dla jakich kontraktów (emerytury, kredyty wieloletnie) który wariant.
- Mechanizm umowy indeksowanej do AUV + marża (przykład liczbowy).

## 7. Ograniczenia

- Dane produkcji metali/budownictwa przybliżone (do zastąpienia USGS/World Steel); produkcja jako proxy konsumpcji per capita.
- Mianownik amerykocentryczny (PKB/os.) — do zglobalizowania (godziny pracy, Penn World Table).
- Wątek monetarny wyłącznie USA + porównanie ilościowe EBC/BoJ; brak porównywalnego składu kolateralu cross-country; wagi jakości Q normatywne.
- Korelacja ≠ przyczynowość; małe próby roczne w testach Grangera (niska moc).
- Endogeniczność dochodu (PKB zawiera wartość dodaną surowców z licznika).

## 8. Wnioski i dalsze prace

- Synteza: jednostka pracy daje stabilną, odporną miarę realnej wartości; rozróżnienie kierunek/skala inflacji ma implikacje dla projektowania indeksacji i polityki.
- Dalej: globalny mianownik, pełne dane produkcji, formalny model jakości pieniądza z kontrolą na M2, rozszerzenie cross-country.

## Załączniki

- A. Słownik terminologii monetarnej (kreacja kredytowa, ekspansja monetarna — bez „dodruku").
- B. Pełna lista serii i identyfikatorów; reguły zamrożone (koszyk, wagi, baza).
- C. Reprodukcja: jak odtworzyć każdą liczbę i wykres z repozytorium.

---

## Mapa: wynik → rysunek/plik (do kontroli kompletności)

| Sekcja | Wynik | Rysunek | Kod |
| --- | --- | --- | --- |
| 4.1 | AUV-T vs M2/CPI | 30 | `auv_t.py` |
| 4.2 | SDR komparator | 31 | `auv_t.py` |
| 4.3 | mianowniki | 34 | `analysis_v4.py` |
| 4.4 | trend/cykl | 32 | `auv_research.py` |
| 4.5 | walidacja | 40 | `sensitivity.py` |
| 4.6 | potrzeby | 33 | `auv_research.py` |
| 5.1 | kierunek inflacji | 36–39 | `collateral_inflation.py` |
| 5.2 | ponad M2 | 41 | `money_quality_model.py` |
| 5.3 | bilanse CB | 43 | `cb_balance_sheets.py` |
| 6 | wariant kontraktowy | 42 | `auv_contract.py` |

## Docelowe miejsce publikacji (do rozważenia)

Preprint (SSRN / arXiv econ.GN / MPRA) jako pierwszy krok — datuje i upublicznia, zgodnie z filozofią otwartości. Potem ewentualnie czasopismo (np. z obszaru ecological/resource economics lub monetary economics, zależnie od tego, czy akcent pada na Wkład A czy B).
