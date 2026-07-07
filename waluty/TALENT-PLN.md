# TALENT-PLN — karta walutowa

**Poziom: A** · waluta bazowa projektu · prototyp działa (`../talent_strona.html`)

## Noga cen
- **C1:** GUS, komunikat „Wskaźniki cen towarów i usług konsumpcyjnych", dynamika m/m, publikacja ~15. dnia m+1; miesięczny szereg użyteczny od 1989 (wcześniej gospodarka niedoborów — ceny urzędowe bez treści informacyjnej).
- **C2:** Eurostat HICP-PL (`prc_hicp_midx`), ~17.–19. dnia m+1, od 1996. Liczony z danych GUS inną metodą — częściowo niezależny.
- **C3 (do zbudowania):** indeks cen online; do tego czasu tripwire na parze C1/C2.

## Noga płac
- **W1/W2:** GUS „Przeciętne zatrudnienie i wynagrodzenie w sektorze przedsiębiorstw" (~21. dnia m+1) → fundusz/MA12 wg TIP-0001. Ograniczenie: firmy ≥9 osób, bez umów cywilnoprawnych.
- **W3 (kierunek docelowy, TIP-0002):** mediana z „Rozkładu wynagrodzeń w gospodarce narodowej" — rejestry ZUS+MF, miesięcznie, od I 2010, opóźnienie ~2 mies. Dane administracyjne, praktycznie niemanipulowalne ankietowo — unikatowa przewaga Polski w tym gronie.
- Historia do backtestów: przeciętne wynagrodzenie roczne od 1950 (ZUS/GUS), z przełomami: denominacja 1995, ubruttowienie 1999.

## Ryzyka specyficzne
Przełomy metodologiczne (1995, 1999) — obsłużone łańcuchowaniem; polityczna presja na GUS niska (członkostwo w UE = nadzór Eurostatu nad HICP); szara strefa poza pomiarem płac.

## Werdykt
Pełna jakość od zaraz; po wdrożeniu TIP-0002 (mediana) — prawdopodobnie najlepsza noga płacowa w całym projekcie. Zmierzone pasmo żalu 1989–2024: maks. 10,4% (przez transformację ustrojową).
