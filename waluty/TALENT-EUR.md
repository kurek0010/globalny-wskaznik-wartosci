# TALENT-EUR — karta walutowa

**Poziom: B+** · najlepiej zabezpieczona noga cen świata · noga płac tylko kwartalna

## Noga cen
- **C1:** HICP strefy euro (Eurostat), miesięcznie od 1996; **flash estimate na koniec miesiąca m** (!), finał ~17. dnia m+1.
- Struktura nie do podrobienia: agregat z 20 niezależnych krajowych urzędów statystycznych liczących wspólną, prawnie uregulowaną metodologią — mediana źródeł wbudowana w samą konstrukcję. Zmanipulowanie HICP wymagałoby zmowy 20 instytucji w 20 państwach.

## Noga płac
Brak miesięcznej serii — trzy kandydatury kwartalne:
- **Labour Cost Index** (Eurostat, kwartalny, ~75 dni po kwartale ✻) — koszt godziny pracy, stały skład branż;
- **płace negocjowane** (EBC, kwartalne) — z układów zbiorowych, wolnozmienne;
- **compensation per employee** (rachunki narodowe, kwartalne) — najszersza, rewidowana.
Rozwiązanie: kotwica płacowa aktualizowana kwartalnie, między aktualizacjami noga płac interpolowana ostatnią znaną dynamiką (dokładnie mechanizm ścieżki dziennej, piętro wyżej). Do formalizacji jako TIP przy wdrożeniu.

## Ryzyka specyficzne
Strefa euro to 20 gospodarek o rozjeżdżających się płacach (Niemcy vs Grecja) — Talent-EUR mierzy średnią ważoną, więc dla umowy czysto niemieckiej lepszy byłby Talent-DE z danych krajowych (dane DE są poziomu A ✻; opcja na później). Kwartalna noga płac = wolniejsza reakcja na szok typu 2022 (do oszacowania w teście przed wdrożeniem).

## Werdykt
Wykonalny z jednym kompromisem; ze względu na wagę gospodarczą — drugi po USD w kolejce, z TIP-em o kwartalnej nodze płac jako warunkiem wejścia.
