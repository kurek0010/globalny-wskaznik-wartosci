# Wyścig kandydatów na jednostkę minimalnego żalu — wyniki

**Data:** 2026-07-04
**Dane:** 1996–2025, pliki projektu (`auv_contract.csv`, `auv_t.csv`); złoto: średnie roczne LBMA z wiedzy (1996–2024 pewne, 2025 ≈3250 USD/oz przybliżone). Wyniki także w `prototyp/data/processed/regret_race.csv`.

## Metoda

Pożyczka „oddajesz tyle samo jednostek": dla każdego okna czasowego (horyzonty 3–20 lat, wszystkie lata startu) liczymy, ile nominalnie oddaje dłużnik przy indeksacji kandydatem, i mierzymy **żal obu stron**:

- żal dłużnika = o ile spłata urosła względem dochodów (benchmark: dochód/os.),
- żal wierzyciela = o ile spłata straciła siłę nabywczą (benchmark: CPI).

Żal okna = większy z dwóch. „Zero żalu" = odchylenie < 2%. To operacjonalizacja wymogu: *obie strony po latach uznają, że oddano w przybliżeniu tę samą wartość*.

## Wyniki (wszystkie okna łącznie)

| Kandydat | % okien zero-żalu | Mediana żalu | p95 | Najgorszy przypadek |
|---|---|---|---|---|
| **MIX A: 50% dochód + 50% CPI (geom.)** | **82%** | **0,0%** | **4,5%** | **7,2%** |
| MIX D: 45/45/10 (dochód/CPI/AUV-kon) | 69% | 0,0% | 7,5% | 9,7% |
| CPI USA | 75% | 0,0% | 9,3% | 14,9% |
| dochód/os. (świat) | 75% | 0,0% | 9,3% | 14,9% |
| dochód wygładzony 3l | 43% | 3,1% | 11,6% | 14,9% |
| MIX B: 60% dochód + 40% AUV-kontrakt | 57% | 1,3% | 23,1% | 25,9% |
| MIX C: 1/3 CPI + 1/3 dochód + 1/3 złoto | 12% | 11,8% | 28,4% | 44,3% |
| **nominal (dzisiejsza praktyka KKOP)** | 0% | 17,7% | 54,0% | 66,1% |
| AUV kontraktowy (wygładzony 5l) | 19% | 15,1% | 58,2% | 68,8% |
| koszyk surowcowy (nominalny) | 13% | 20,0% | 64,8% | 87,6% |
| AUV surowy | 18% | 20,0% | 78,8% | 93,9% |
| złoto | 2% | 47,7% | 189,0% | **264,9%** |

## Odczyt

**1. Zwycięzca jest analityczny, nie przypadkowy.** Żal dłużnika mierzony jest dochodem, żal wierzyciela — kosztami życia. Między tymi dwiema trajektoriami rozciąga się „korytarz zero-żalu": indeks, który w nim siedzi, nie krzywdzi nikogo. Geometryczna średnia 50/50 obu benchmarków **z konstrukcji** siedzi w środku korytarza — jej najgorszy żal to zawsze połowa maksymalnej rozbieżności dochody↔ceny. Empiryczna treść wyniku: w latach 1996–2025 ta rozbieżność nie przekroczyła ~14%, więc najgorszy żal MIX A = 7,2% na dwie dekady. To jest pasmo, o które pytałeś.

**2. To rozwiązanie ma 40 lat praktyki, tylko nikt go nie używa do pożyczek.** Szwajcarski *Mischindex* waloryzuje emerytury dokładnie formułą 50% płace / 50% ceny od lat 80. Polska waloryzacja emerytur: inflacja + ≥20% realnego wzrostu płac — ten sam duch, inne wagi. Fińskie indeksy emerytalne — analogicznie. Czyli: formuła minimalnego żalu między „siłą nabywczą" a „udziałem w dochodzie" została niezależnie odkryta przez systemy emerytalne, które mają identyczny problem (zobowiązanie wieloletnie, dwie strony, spór o miarę). Nowość Twojego projektu to zastosowanie jej jako **jednostki pożyczkowej open source**, nie wynalezienie wag.

**3. Dzisiejsza praktyka KKOP (nominalnie, bez indeksacji) jest gorsza od wszystkiego poza złotem i surowym AUV:** mediana żalu 17,7%, najgorzej 66% (wierzyciel, 2004→2024). To jest liczbowy argument założycielski projektu: kasy wzajemne *systematycznie* karzą pożyczających kolegom.

**4. Złoto i surowce nie nadają się wprost.** Złoto: pożyczka z 2005 oddana w 2025 kosztuje dłużnika 265% więcej względem dochodów. AUV/koszyk: cykl surowcowy generuje żal 60–94%. Domieszka AUV do miksu (MIX D, 10%) tylko pogarsza wynik względem czystego MIX A — surowce nie wnoszą tu informacji, wnoszą wariancję. **Rola AUV w projekcie powinna być diagnostyczna** (miara napięcia zasobowego, demaskowanie iluzji monetarnej), nie kontraktowa.

## Zastrzeżenia (uczciwie)

1. **Benchmarki są endogeniczne:** CPI i dochód oceniają same siebie (stąd ich mediana 0,0%). Wynik MIX A nie jest jednak tautologią — mówi: *jeśli* zgadzamy się, że żal stron mierzy się kosztami życia i dochodami, *to* środek geometryczny minimalizuje maksimum żalu. Spór może dotyczyć tylko definicji żalu, nie arytmetyki.
2. **Uniwersum USD/świat.** Dla polskiej kasy właściwy jest wariant lokalny: 50% CPI-PL (mediana z GUS/Eurostat/HICP) + 50% mediana płac PL (GUS/ZUS). Do policzenia analogicznie.
3. **Korytarz może się rozszerzyć.** W stagflacji z realnym spadkiem płac (PL lata 80., Argentyna) rozbieżność dochody↔ceny sięga dziesiątek procent — wtedy żaden indeks nie da zero-żalu i MIX dzieli ból po połowie (co nadal jest własnością minimaksową, ale trzeba to komunikować). Test wsteczny na długiej historii (docelowo do ~1900) pozostaje kluczowym następnym dowodem.
4. **Powrót autorytetów:** CPI i płace liczą urzędy. Mitygacja zgodna z filozofią projektu: mediana z ≥2–3 niezależnych źródeł na nogę, formuła i dane opublikowane, hash odczytu, zakaz rewizji wstecz — „instytucja skuta regułą", jak w nocie koncepcyjnej.
5. Złoto 2025 przybliżone; nie zmienia rzędu wielkości wyniku (żal złota jest katastrofalny niezależnie od końcówki).

## Następne kroki

1. Wariant lokalny PL (CPI-PL + płace PL) — ten sam wyścig.
2. Rozszerzenie historii wstecz (USA: CPI + płace od ~1900, dane BLS/MeasuringWorth) — pasmo żalu przez wojny, stagflację lat 70., deflację lat 30.
3. Reguła publikacyjna jednostki (nazwa robocza: **JW — jednostka wartości**): JW(t) = √(CPI(t) × Dochód(t)), mediana źródeł, pre-commitment miesięczny, chain-linking przy zmianie źródeł — szkielet z Części II dokumentu o niezmienniczości przenosi się wprost.
