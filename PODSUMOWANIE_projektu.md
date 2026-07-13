# Podsumowanie projektu — od „wartości bezwzględnej" do Talenta

**Data zamknięcia tego etapu:** 2026-07-13
**Status repozytorium:** zamknięte, zachowane jako archiwum drogi. Dalsze prace nad Talentem przeniesiono do osobnego repozytorium `talent`.

Ten dokument domyka pracę prowadzoną w repozytorium `globalny-wskaznik-wartosci`. Zbiera w jednym miejscu, po co ten projekt powstał, jaką drogą przeszedł, dlaczego pierwotny cel okazał się nieosiągalny i jak z tej drogi wyłoniła się jedna użyteczna rzecz — jednostka **Talent (TLN)**. Zgodnie z filozofią projektu („kod jest metodologią, błędy są częścią dowodu") niczego tu nie retuszujemy.

---

## 1. Cel wyjściowy: zmierzyć wartość bezwzględną

Projekt zaczął się od ambitnego pytania: **czy da się zbudować obiektywną, „absolutną" miarę wartości** — jednostkę, która nie zależy od decyzji żadnego banku centralnego ani urzędu, tylko od obserwowalnych, weryfikowalnych danych (zasada, którą w projekcie nazywaliśmy „heliocentrycznością"). Taka jednostka miała odpowiadać na pytanie: *czy świat realnie się bogaci, czy tylko rosną nominalne ceny?*

Roboczą nazwą tego pomysłu było **AUV (Absolute Unit of Value)** — jednostka wartości oparta na koszyku surowców, ich produkcji i populacji.

## 2. Droga prób i błędów

Kolejne iteracje pokazywały, że im bliżej danych, tym wyraźniej „absolutna wartość" wymyka się pomiarowi:

1. **AUV v0.1–v0.3.1** — próby ekstrakcji „ukrytej wartości" z cen surowców: metody ML/PCA, regresje na podaży pieniądza M2, formuła `cena × potrzeba × populacja / produkcja`, hybrydy z CPI. Wszystkie albo sprowadzały się do wariantu zwykłej inflacji, albo rozpadały się na danych.
2. **AUV-T / numéraire pracy** — koszyk surowców dzielony przez dochód. Obiecujący wynik „+0,4% w 30 lat" okazał się artefaktem jednego supercyklu surowcowego; test wsteczny na danych od 1900 r. potwierdził dryf.
3. **FDI (Fiat Depreciation Index)** — pomysł równoległy: zamiast mierzyć „realną wartość", mierzyć *deprecjację pieniądza papierowego* z czterech sygnałów (CPI, M2, dług/PKB, SDR). Praktyczny, ale to już inne pytanie niż „wartość absolutna".
4. **Krytyczna recenzja ekonomiczna** — punkt zwrotny. Wykazała luki (m.in. prawne — BMR), przenoszenie cyklu surowcowego na kredytobiorcę i słabość nogi dochodowej.
5. **Przeformułowanie celu** — od „miary absolutnej" do **jednostki minimalnego żalu dla umów**. Kluczowe odkrycie: najcenniejszy w całym AUV okazał się jego *mianownik* (dochód / praca), a nie cały koszyk surowców.

## 3. Główny wniosek

**Jednostka wartości absolutnej w praktyce nie istnieje.** Każda próba jej zbudowania albo redukowała się do inflacji, albo była zbyt wrażliwa na arbitralne wybory (wagi, źródła, okno czasowe), albo padała na jakości danych produkcyjnych. To nie jest porażka — to wynik. Droga zawęziła pytanie z niemożliwego („ile realnie wart jest świat?") do wykonalnego i użytecznego („jaką jednostką rozliczyć umowę wieloletnią, żeby żadna strona nie została skrzywdzona?").

## 4. Co z tego wyrosło: Talent (TLN)

Odpowiedzią jest **Talent** — deterministyczna jednostka rozliczeniowa do umów wieloletnich. Pożyczasz 1000 TLN, oddajesz 1000 TLN, a obie strony odzyskują w przybliżeniu tę samą wartość.

- **Formuła:** środek geometryczny indeksu cen i indeksu płac, √(C×W).
- **Kryterium:** minimalizuje największą możliwą krzywdę którejkolwiek strony umowy (minimax regret).
- **Dowód empiryczny:** najgorszy przypadek 6,1% przez sto lat danych USA (1929–2025) i 10,4% przez polską transformację (1989–2024) — wobec setek procent dla pożyczek czysto nominalnych.
- **Zasada:** wartości są odtwarzalne z danych publicznych, publikowane z wyprzedzeniem i **nigdy nie rewidowane wstecz**; każda zmiana formuły przechodzi przez jawny proces TIP (wzorzec BIP/EIP).

Talent jest węższy niż AUV, ale za to **działa, jest weryfikowalny i ma realne zastosowanie**.

## 5. Co przetrwało, a co odłożono

Przetrwało i żyje dalej (w repozytorium `talent`): formuła Talenta, reguła publikacyjna, proces TIP, testy historyczne (USA, Polska, jednostka dwustronna PL–US, wyścig kandydatów), strona, comiesięczna automatyczna kotwica, infrastruktura źródeł danych (FRED, NBP, ECB, World Bank, GUS) oraz reguła niezmienniczości/chain-linkingu.

Odłożono jako zamkniętą drogę (pozostaje w tym repozytorium): cała rodzina AUV (koszyk surowców, ML/PCA, AUV-T), koncepcja FDI, model jakości pieniądza, recenzje, plany prototypów i notebooki badawcze. Materiały te są w katalogach `archiwum/` oraz `prototyp/src/archiwum_auv/`.

## 6. Gdzie co teraz jest

- **`talent`** (nowe repozytorium) — żywy projekt: wszystko, co potrzebne, by zrozumieć, odtworzyć, rozwijać i stosować Talenta. Bez balastu drogi AUV.
- **`globalny-wskaznik-wartosci`** (to repozytorium) — zamrożone archiwum: pełny zapis drogi od „wartości bezwzględnej" do Talenta, łącznie z tym podsumowaniem. Zostaje dla porządku historycznego i uczciwości metodologicznej.

## 7. Zamknięcie

Ten etap uznajemy za zamknięty. Projekt osiągnął coś węższego niż pierwotna ambicja, ale mocniejszego: zamiast nieosiągalnej „miary wszystkiego" — jedną, prostą, weryfikowalną jednostkę, która rozwiązuje konkretny problem umów wieloletnich. Dalsza praca toczy się nad Talentem, w osobnym repozytorium.
