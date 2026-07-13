# Szkic: „Kredyt w Talentach" — tezy do przyszłego artykułu

**Status:** notatka robocza (2026-07-10), NIE do publikacji. Obliczenia jednorazowe z sesji — do powtórzenia rygorystycznie przed pisaniem.

## Przypadek policzony

Kredyt 300 000 zł, 20 lat, raty roczne, rocznik 2006. Trzy warianty: WIBOR 12M + 2% (annuitet przeliczany co roku), rata równa w TLN bez marży, rata równa w TLN + marża 2% (annuitet w TLN). Kapitał = 138 317 TLN (kotwica 2006 ≈ 2,17 zł/TLN).

| Wariant | Suma nominalna (zł) | Koszt realny (w TLN) | Rata min–max (zł) | Obciążenie: start → koniec (% rocznej płacy GN) |
|---|---|---|---|---|
| WIBOR+2% | 511 tys. | **+19%** | 22,7–31,1 tys. | **90% → 24%** (frontloaded) |
| TLN 0% | 464 tys. | **0%** (z definicji) | 15,0–38,6 tys. | 50% → 36% |
| TLN+2% | 567 tys. | +22% | 18,3–47,3 tys. | 62% → 44% |

## Tezy (uzgodnione z autorem 2026-07-10)

1. **TLN bez marży jest sumarycznie najtańszy** i oddaje dokładnie pożyczoną wartość (model kasy/pożyczki prywatnej).
2. **TLN+2% ≈ WIBOR+2% kosztem realnym** (22% vs 19%), ale bez loterii stóp: rata znana w TLN na 20 lat, idzie równo z gospodarką, brak skoków z decyzji RPP.
3. **TLN+1% ≈ WIBOR+2% nominalnie** (~514 vs ~511 tys. zł) przy **niższym koszcie realnym** (+11% vs +19%) — raty przesunięte w tańsze złotówki i lżejsze lata. Marża ~1–2 p.p. w TLN to rynkowy ekwiwalent WIBOR+2%.
4. **Profil obciążenia to główna przewaga:** WIBOR bije najmocniej na starcie (rata 2006 = 90% rocznej pensji), TLN rozkłada ciężar płasko w kategoriach realnych (50%→36%).
5. **Odporność polityczna:** w TLN nie istnieje stopa referencyjna, którą można podnieść uchwałą (kontrast: kredyty 1989–91, „przypadek Balcerowicza" — oprocentowanie podniesione decyzją do kilkudziesięciu procent zrujnowało kredytobiorców). TLN reaguje tylko na zmierzone ceny i płace, z połowicznym tłumieniem. Uczciwie: w hiperinflacji rata w zł też rośnie kilkukrotnie — ale o połowę rozjazdu mniej niż ceny i bez odsetek składanych (por. żal 10,4% w teście polskim).

## Zastrzeżenia — obowiązkowe do domknięcia przed artykułem

- **Jedna próba, korzystny rocznik dla WIBOR** (dekada niskich stóp 2013–21; mały kapitał przy szoku 2022). Rocznik 2021 dostał +100% raty — trzeba policzyć **wszystkie roczniki** (metodą okien jak w teście żalu) i pokazać rozkład, nie jeden przykład.
- WIBOR 12M = średnie roczne z pamięci (±0,3 p.p.) — **zweryfikować u źródła** (stooq/GPW Benchmark).
- Raty roczne = uproszczenie; wersja artykułowa: miesięczne.
- Kotwice TLN sprzed IV 2025 = rekonstrukcja historyczna, nie publikacje (oznaczyć).
- Rozważyć wariant „po podatku" i prowizje bankowe, jeśli artykuł ma być kompletny.

## Dane

Skrypt sesyjny (do sformalizowania jako `prototyp/src/kredyt_porownanie.py` przy pisaniu artykułu); kotwice z `talent_anchors.csv`, płace GN z `first_prints_pln.json`.
