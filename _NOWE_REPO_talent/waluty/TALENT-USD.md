# TALENT-USD — karta walutowa

**Poziom: A** · najlepsza infrastruktura danych na świecie · wdrożenie: natychmiastowe (wszystko w FRED)

## Noga cen
- **C1:** CPI-U (BLS), miesięcznie od 1913, publikacja ~10.–13. dnia m+1 (FRED: `CPIAUCNS`/`CPIAUCSL`).
- **C2:** deflator PCE (BEA), miesięcznie, koniec m+1 (`PCEPI`) — inna metodologia i wagi, realnie niezależna miara.
- **C3:** chained CPI (`SUUR0000SA0`) ✻. Trzy źródła od ręki → pełny tripwire z mediany od pierwszego dnia.

## Noga płac
- **W1/W2:** CES — average hourly earnings + zatrudnienie (`AHETPI`/`CES0500000003`, `PAYEMS`), miesięcznie; płace produkcyjnych od 1939. Publikacja: **pierwszy piątek m+1** (raport z rynku pracy) — najszybsze dane płacowe świata, kotwica może być liczona już ~10. dnia.
- **W3:** mediana Atlanta Fed Wage Growth Tracker (te same osoby rok do roku — wzorzec odporności na efekt składu) ✻; ECI kwartalnie (stały skład zatrudnienia); QCEW kwartalnie (administracyjne, spis pełny).

## Ryzyka specyficzne
Rewizje CES bywają duże (benchmark roczny do QCEW) — polityka first-print + raport pojednawczy obsługują to wprost. Płace produkcyjne stagnowały dekadami: Talent-US ≈ CPI + ~0,2 p.p. (zmierzone 1996–2025: ×2,16 vs CPI ×2,05) — jednostka uczciwie pokaże gospodarkę, w której wzrost omija płace.

## Werdykt
Kandydat na pierwszy Talent zagraniczny i pierwszy kurs krzyżowy (TLN-PL/TLN-US). Zmierzone pasmo żalu 1939–2025: maks. 6,1%.
