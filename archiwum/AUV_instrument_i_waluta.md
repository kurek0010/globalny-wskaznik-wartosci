# AUV jako instrument i jako podstawa waluty — nota projektowa

**Autor:** Mariusz Kurowski
**Data:** 2026-06-22
**Status:** projektowe; do przemyślenia przed powstaniem instytucji dbającej o AUV.

## 0. Rozróżnienie wyjściowe: indeks, instrument, waluta

- **AUV-indeks** — liczba z formuły (jak CPI/UF). Nie ma ceny rynkowej, więc jest odporny na spekulację z definicji. Nie wymaga żadnego mechanizmu obrony.
- **AUV-instrument** — coś, co da się TRZYMAĆ i handlować (token/funduszu jednostka „1 = wartość AUV"). Ma cenę rynkową → może odjechać od wartości formuły → potrzebny mechanizm kreacji/umorzenia (à la ETF).
- **AUV-waluta** — pieniądz, którego jednostka ma trzymać wartość AUV. Najdalej idący wariant; to instrument redeemowalny podniesiony do rangi środka płatniczego.

Ta nota dotyczy warstwy 2 i 3.

## 1. Mechanizm kreacji/umorzenia (à la ETF Authorized Participants)

Instytucja stoi gotowa, by **mechanicznie** kreować i umarzać jednostki po wartości formuły AUV (± mała opłata), w walucie rozliczeniowej, z rezerwy:

- cena rynkowa > wartość AUV (premia): instytucja emituje nowe jednostki po wartości formuły → podaż rośnie → premia znika;
- cena rynkowa < wartość AUV (dyskonto): instytucja umarza jednostki po wartości formuły → podaż spada → dyskonto znika.

**Własność zgodna z heliocentryzmem:** czynności są mechaniczne, nie uznaniowe — instytucja honoruje kreację/umorzenie po deterministycznej wartości, nie ocenia i nie interweniuje z osądu. Regułą i arbitrażem, nie decyzją rady.

## 2. Rezerwa i ryzyko bazowe (kluczowy problem inżynierski)

ETF ma łatwo: trzyma dokładnie ten koszyk, który wycenia, więc NAV = to, co posiada. AUV ma trudniej, bo jego formuła to `koszyk / dochód` — a **dochodu (pracy) nie da się trzymać w rezerwie**.

Konsekwencja, którą trzeba zobaczyć jasno:

- Waluta **kryta i redeemowalna za fizyczny koszyk surowców** ma wartość = **licznika** (ceny koszyka), czyli tę zmienną, cykliczną „sinusoidę" (szoki 2008, 2022). To działa i jest w pełni kryte, ale daje zmienną wartość, nie stabilne AUV.
- Stabilne AUV (`koszyk/dochód`) bierze swoją stabilność właśnie z **nogi dochodowej**, której nie można skolateralizować. To nie jest przypadek — to strukturalne: część, która daje AUV stabilność, jest zarazem częścią, której nie da się „mieć".

Wniosek: idealne, w pełni kryte odwzorowanie AUV jest niemożliwe. Do wyboru:

(a) **Kryte koszykiem** — pełne pokrycie, ale wartość = zmienny licznik (nie AUV).
(b) **Currency board z buforem** — obiecujesz umorzenie po wartości AUV, trzymasz rezerwę przybliżającą formułę, a różnicę (ryzyko bazowe) pokrywa bufor kapitałowy. Analogia: emitent obligacji indeksowanych inflacją obiecuje wypłatę wg CPI, nie „trzymając CPI", lecz opierając się na własnym bilansie.
(c) **Algorytmiczne, bez pokrycia** — odradzam. Terra/Luna pokazała, że peg bez realnej rezerwy trzyma się tylko zaufaniem i pęka gwałtownie.

## 3. Wymóg kapitału i ryzyko runu

Instytucja musi mieć bufor kapitałowy na ryzyko bazowe (2b) oraz płynność na wypadek masowego umorzenia (run). Reguły do zamrożenia w regulaminie:

- minimalny współczynnik pokrycia (np. rezerwa ≥ 100% zobowiązań w wartości AUV + bufor X%),
- skład rezerwy i reguła rebalansu (jawna, nie uznaniowa),
- opłata za kreację/umorzenie (pokrywa koszty, hamuje mikroarbitraż),
- procedura na wypadek niedoboru pokrycia (transparentna, ogłoszona z góry).

## 4. AUV jako podstawa waluty

To logiczny szczyt: zamiast wiązać pieniądz z innym fiat-em (który dryfuje) czy złotem (zmienne), wiążesz go z AUV — stabilną realną wartością w jednostkach pracy. Taka waluta z założenia trzymałaby stałą realną siłę nabywczą.

**Mechanizm** = currency board na AUV (jak dolar Hongkongu na USD, ale kotwicą jest AUV): emisja jednostek redeemowalnych po wartości AUV, obrona parytetu arbitrażem kreacji/umorzenia.

**Obietnica:** „sound money", które nie traci wartości przez ekspansję monetarną — bo jego jednostka jest przywiązana do realnej wartości, nie do decyzji banku centralnego.

**Uczciwe granice (te same co w 2, spotęgowane skalą):**

- Noga dochodowa nadal niekryta → albo waluta faktycznie śledzi *koszyk* (zmienny), albo currency board bierze na siebie ryzyko bazowe i potrzebuje mocnego bilansu.
- Zaufanie i run: waluta jest tak wiarygodna, jak wiarygodne jest umorzenie po parytecie. To wymaga instytucji z realnym kapitałem i przejrzystością, inaczej peg pęka.
- Governance: kto zarządza rezerwą, jak zapobiec przechwyceniu instytucji — to samo pytanie, które projekt zadaje bankom centralnym, wraca tu do nas.

## 5. Rekomendacja

- **AUV błyszczy jako jednostka rachunkowa** (miara, indeks do umów) — tu jest bezkonkurencyjny i nie wymaga rezerw ani instytucji.
- **Jako instrument/waluta** najczystszy realnie wykonalny wariant to **kryty koszykiem** (redeemowalny za realne zasoby) LUB **currency board na AUV z buforem kapitałowym** — z pełną świadomością ryzyka bazowego nogi dochodowej.
- **Odradzam** warianty algorytmiczne bez pokrycia.
- Kolejność wdrożenia: najpierw AUV-indeks (publikacja), potem umowy denominowane w AUV rozliczane w istniejących walutach (model UF), a dopiero na końcu — jeśli w ogóle — AUV-instrument/waluta z pełną instytucją i kapitałem.
