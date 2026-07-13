# TALENT-GBP — karta walutowa

**Poziom: A** · bardzo dobra · brytyjska specjalność: administracyjne dane płacowe w czasie niemal rzeczywistym

## Noga cen
- **C1:** CPI (ONS), miesięcznie, publikacja ~połowa m+1; spójny szereg od 1988, szacunki wstecz do 1950 ✻.
- **C2:** CPIH (CPI + koszty mieszkania właścicieli) — preferowana miara ONS, ta sama publikacja; częściowo odpowiada na zarzut „CPI ślepy na mieszkania".
- Uwaga: RPI istnieje historycznie (indeksuje stare obligacje), ale ONS uznał go za wadliwy — nie używać.

## Noga płac
- **W1/W2:** Average Weekly Earnings (ONS, miesięcznie, od 2000; wcześniej AEI od 1963 ✻ — łączenie łańcuchowe do backtestu).
- **W3:** **HMRC PAYE RTI** — mediana płac z systemu podatkowego, miesięcznie, publikowana z opóźnieniem ~2–6 tygodni ✻. Administracyjny odpowiednik naszego ZUS: drugie źródło odporne na ankiety i efekt składu.

## Ryzyka specyficzne
Historia zmian miar inflacji (RPI→CPI→CPIH) — dobra ilustracja, czemu reguła Talenta pracuje na dynamikach i łańcuchowaniu; problemy ONS z response rate badań ankietowych po 2020 ✻ — kolejny argument za nogą PAYE.

## Werdykt
Wdrożenie mechaniczne po weryfikacji ✻; para nóg CPIH + PAYE-mediana może być metodologicznie najciekawszą implementacją w projekcie.
