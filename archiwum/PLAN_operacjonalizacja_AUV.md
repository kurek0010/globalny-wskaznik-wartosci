# Plan operacjonalizacji AUV — do zrobienia później

**Status:** odłożone do realizacji; analityka i dowód gotowe (v0.4), brakuje warstwy operacyjnej.
**Data:** 2026-06-22

Różnica między „prototypem" a „działającą jednostką". Trzy rzeczy do domknięcia, zanim AUV będzie można pewnie używać w umowach:

## 1. Kod publikujący (narzędzie)
Funkcja wyznaczająca wartość AUV na dany dzień w kilku walutach wg modelu dwuwarstwowego:
- miesięczna kotwica (pełne dane) + żywe ceny dzienne (surowce, FX),
- wolny mianownik (dochód) zamrożony między rocznymi odczytami,
- publikacja z wyprzedzeniem, bez rewizji wstecznej (styl UF).
Wyjście: „kalendarz AUV" (CSV) — dzienne wartości w PLN/EUR/USD/… na nadchodzący okres.

## 2. Zweryfikowane dane produkcji
Podmienić przybliżone (z pamięci) wartości produkcji metali i budownictwa na oficjalne:
- USGS Mineral Commodity Summaries (metale),
- World Steel (stal), CEMBUREAU (cement),
- uzupełnić rudę żelaza, nikiel, cynk (dziś puste).
Wpisać do `data/manual/manual_production.csv`.

## 3. Spisany regulamin AUV (zaufanie / heliocentryczność)
Dokument definiujący jednoznacznie i na stałe:
- dokładny skład koszyka i identyfikatory serii,
- wagi kategorii i regułę roku bazowego (np. średnia N pierwszych lat),
- częstotliwość i sposób publikacji (model dwuwarstwowy),
- **procedurę rewizji reguł** (jawną, ogłaszaną z wyprzedzeniem, nie uznaniową),
- ewentualny mechanizm instytucjonalny obrony wartości (patrz niżej).

## 4. (Nowy wątek) Mechanizm obrony wartości typu ETF (NAV vs cena rynkowa)
Do przeanalizowania i ewentualnego wpisania do regulaminu: mechanizm kreacji/umorzenia
(à la ETF Authorized Participants), który utrzymuje cenę rynkową instrumentu AUV przy
wartości formuły, broniąc przed spekulacją i owczym pędem. Szczegóły w osobnej notatce.

## 5. Pomysły badawcze na kolejne wersje (v0.5+)

Rozszerzenia dokładności, nie fundamentu — rdzeń (brak dryfu, powrót do wartości) jest już udowodniony i odporny.

- **Ważenie regionalne / rodzina AUV.** Dziś mianownik to globalny dochód na osobę, a ceny są światowe. Kraje rozwinięte, rozwijające się i najbiedniejsze inaczej wyceniają te same dobra (inne koszyki konsumpcji, inne poziomy cen — PPP). Możliwe kierunki: (a) ważyć dochód/koszyk udziałem regionów w światowym PKB; (b) zbudować *rodzinę* regionalnych AUV (AUV-rozwinięte, AUV-rozwijające się) obok globalnego; (c) korekta PPP. Zysk: większa dokładność i lokalna trafność. Koszt: więcej danych i decyzji o wagach — trzeba zamrozić regułą. **Temat na osobną wersję.**
- **Materiały krytyczne jako piąta kategoria.** Lit, kobalt, metale ziem rzadkich — gdy powstaną otwarte, długie serie produkcji.
- **Globalny mianownik z godzin pracy** (Penn World Table / Conference Board) zamiast PKB/os. — usuwa amerykocentryczność, wzmacnia interpretację „numéraire pracy".
- **Formalne rozplątanie endogeniczności** dochodu (PKB zawiera wartość dodaną surowców z licznika).

---
*Wracamy do tych punktów, gdy projekt przejdzie z fazy badawczej do wdrożeniowej. Rdzeń koncepcyjny jest domknięty; to są usprawnienia, nie warunki działania.*
