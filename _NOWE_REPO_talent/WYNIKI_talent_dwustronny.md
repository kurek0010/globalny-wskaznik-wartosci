# Talent umowy międzynarodowej — wyniki PL-US (2002–2024)

**Data:** 2026-07-04 · **Kod:** `prototyp/src/regret_bilateral.py`

## Konstrukcja

Talent dwustronny (TLN-2) dla umowy polsko-amerykańskiej: **środek geometryczny obu Talentów krajowych z kursem rozłożonym po połowie**:

$$V_{PLN}(t) = \sqrt{TLN_{PL}(t) \cdot TLN_{US}(t) \cdot \frac{S(t)}{S(0)}} \qquad V_{USD}(t) = \frac{V_{PLN}(t)}{S(t)/S(0)}$$

gdzie S to kurs PLN/USD; po stronie USD wzór jest symetryczny.

Żal liczony w obu krajach naraz: jednostka oceniana w PLN względem korytarza [CPI-PL, płaca-PL] i w USD względem [CPI-US, płaca-US]; żal okna = największe przekroczenie któregokolwiek z 4 brzegów (każda strona może być dłużnikiem lub wierzycielem). Horyzonty 3–20 lat, wszystkie okna.

## Wyniki

| Jednostka umowy | % okien zero-żalu | Mediana | p95 | Najgorszy przypadek |
|---|---|---|---|---|
| **TLN-2 dwustronny** | 20% | 5,7% | **23,0%** | **34,3%** (dłużnik US, 2003→2008) |
| TLN-US | 43% | 3,4% | 33,6% | 60,7% (wierzyciel PL, 2003→2008) |
| TLN-PL | 13% | 13,4% | 48,9% | 77,2% (dłużnik US, 2003→2008) |
| USD nominal | 0% | 19,1% | 77,0% | 84,6% |
| 50/50 PLN+USD nominal | 0% | 23,4% | 70,1% | 85,0% |
| PLN nominal | 0% | 30,6% | 77,9% | **93,0%** |

Kontekst próby: płace PL ×3,84 vs płace US ×1,82 (konwergencja), CPI PL ×2,01 vs US ×1,74, kurs bez zmian (×0,98) — realny rozjazd gospodarek ~2×.

## Odczyt

1. **TLN-2 tnie najgorszy przypadek o połowę względem najlepszej jednostki jednostronnej** (34% vs 61–77%) i niemal trzykrotnie względem walut nominalnych (85–93%). Minimaksowa własność środka geometrycznego przenosi się na przypadek międzynarodowy.
2. **Uczciwa granica:** w umowie międzynarodowej istnieje ryzyko, którego żadna formuła nie usunie — realny rozjazd dwóch gospodarek (tu: konwergencja płacowa Polski, ×2 w 22 lata). To ryzyko musi gdzieś wylądować; jednostki jednostronne i waluty zrzucają je w całości na jedną stronę, TLN-2 dzieli po połowie w logarytmach. 34% na 20 lat to cena uczestniczenia w parze z gospodarką doganiającą — nie wada formuły.
3. Para PL-US jest blisko najtrudniejszego przypadku (transatlantycki + konwergencja). Dla par o zbieżnych trajektoriach (US-EU, US-UK) korytarze niemal się pokrywają i TLN-2 powinien mieć pasmo jednocyfrowe — do policzenia, gdy dodamy płace strefy euro.
4. Uogólnienie na N stron: średnia geometryczna Talentów uczestników (równe wagi lub wagi udziałów w kontrakcie) — kandydat na jednostkę rozliczeń konsorcjów i handlu wielostronnego.

## Zastrzeżenia

Dane roczne; płace PL z tablic GUS/ZUS (do weryfikacji, jak w `WYNIKI_kruche_gospodarki.md`); płace US = produkcyjni w przemyśle; kurs = średnia roczna NBP. Wyniki wrażliwe na dobór próby 2002–2024 (jedna wielka konwergencja) — wskazany test na dłuższej parze (np. US-UK od 1939).
