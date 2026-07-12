# Test stulecia — zachowanie jednostki na danych USA 1929–2025

**Data:** 2026-07-04
**Kod:** `prototyp/src/regret_century.py` (odtwarzalny). Dane: FRED — CPI (CPIAUCNS, średnie roczne, od 1913), dochód nominalny/os. (A939RC0A052NBEA, od 1929), płaca godzinowa produkcyjna w przemyśle (CES3000000008, od 1939); pobrane 2026-07-04, zapisane w `prototyp/data/raw/`. Wyniki: `prototyp/data/processed/regret_century.csv`.

**Terminologia:** metrykę „żal" zastępujemy terminem **regret** — to standardowe pojęcie teorii decyzji (kryterium minimax regret, Savage 1951). Mierzymy **regret dwustronny** pożyczki „oddajesz tyle samo jednostek": regret dłużnika = wzrost spłaty względem dochodów; regret wierzyciela = utrata siły nabywczej spłaty; regret okna = większy z obu. Horyzonty 3–30 lat, wszystkie lata startu.

---

## Bieg 1: 1929–2025 (w próbie Wielki Kryzys, WWII, stagflacja, 2022)

Benchmark dochodowy: PKB nominalny/os. Jednostka testowana:

$$JW(t) = \sqrt{CPI(t) \cdot \text{Dochód}(t)}$$

| Kandydat | % okien zero-regret | Mediana | p95 | Najgorszy przypadek |
|---|---|---|---|---|
| **JW = √(CPI×dochód)** | **97%** | **0,0%** | **1,4%** | **19,7%** (wierzyciel, 1929→1932) |
| CPI | 95% | 0,0% | 2,9% | 43,3% (dłużnik, 1929→1932) |
| dochód | 95% | 0,0% | 2,9% | 43,3% (wierzyciel, 1929→1932) |
| nominal | 2% | 33,0% | 283,1% | **383,6%** (wierzyciel, 1965→1995) |

## Bieg 2: 1939–2025, benchmark dłużnika = płaca (realizm kasy pożyczkowej)

Członek kasy zarabia płacę, nie PKB. To zmienia obraz zasadniczo:

| Kandydat | % okien zero-regret | Mediana | p95 | Najgorszy przypadek |
|---|---|---|---|---|
| **JW(CPI, płaca)** | **88%** | **0,0%** | **3,5%** | **6,1%** (dłużnik, 1978→2008) |
| CPI | 79% | 0,0% | 7,1% | 12,5% (dłużnik, 1978→2008) |
| płaca | 79% | 0,0% | 7,1% | 12,5% (wierzyciel, 1978→2008) |
| JW(CPI, PKB/os.) | 49% | 2,2% | 23,7% | 34,0% (dłużnik, 1977→2007) |
| PKB/os. | 20% | 8,8% | 50,7% | 63,2% (dłużnik, 1977→2007) |
| nominal | 1% | 32,5% | 301,7% | 383,6% (wierzyciel, 1965→1995) |

---

## Wnioski

**1. Jednostka działa przez stulecie — z twardym pasmem.** JW(CPI, płaca) przez 87 lat, przez WWII, stagflację lat 70., dezinflację Volckera i inflację 2022, w żadnym oknie żadnego horyzontu nie skrzywdziła żadnej strony o więcej niż **6,1%**, a w 88% okien odchylenie było poniżej 2%. To jest odpowiedź w formie, o którą chodziło: naukowe wyliczenie pasma, nie obietnica.

**2. Noga dochodowa MUSI być płacą, nie PKB na osobę.** Największe odkrycie tego testu: JW zbudowany na PKB/os. ma najgorszy przypadek 34% (era stagnacji płac 1977–2007, gdy PKB/os. urósł o 63% więcej niż płace). Ten sam środek geometryczny na płacy: 6,1%. To koryguje też wybór mianownika AUV — PKB/os. przeszacowuje dochód typowego człowieka o cały wzrost nierówności i udziału kapitału.

**3. Asymetria regretu — własność, którą łatwo komunikować.** Regret pojawia się tylko wtedy, gdy płace realnie spadają (społeczeństwo biednieje). Gdy płace rosną szybciej niż ceny (normalność), indeks leżący między nimi daje **zero regretu obu stronom naraz**: wierzyciel odzyskuje więcej niż siłę nabywczą, dłużnik oddaje mniej niż udział dochodu. W złych czasach JW dzieli stratę po połowie — nie da się lepiej bez przerzucenia całości na jedną stronę. Stąd wyniki: dobre epoki = 88–97% okien zero; złe epoki (1929–32: dochody −45% przy cenach −24%; 1978–2008: realny spadek płac produkcyjnych) = strata dzielona.

**4. Nominal — dzisiejsza praktyka kas — jest katastrofą stulecia.** Pożyczkodawca z 1965 odzyskał w 1995 równowartość ~21% siły nabywczej (regret 384%). Nawet w „spokojnych" oknach mediana 33%. Każdy argument za projektem zaczyna się od tej liczby.

**5. Zachowanie jednostki w długim trwaniu (1929=100):** CPI 1876, dochód 10 485, **JW 4435**. Posiadacz JW przez stulecie zachował siłę nabywczą ×2,4 (uczestniczy w połowie realnego wzrostu w logarytmach) i utrzymał ~42% relacji do dochodów. Dokładnie pośrodku — to jest treść „trzymania wartości" w wersji uczciwej: nie „stałość absolutna" (niemożliwa), lecz symetria między dwiema jedynymi miarami, które mają znaczenie dla stron umowy.

## Zastrzeżenia

1. Płaca CES3000000008 = pracownicy produkcyjni przemysłu (proxy; od lat 60. istnieją szersze serie — docelowo mediana kilku serii płacowych).
2. CPI sprzed ~1980 liczone starszą metodologią (bez korekt hedonicznych itd.) — poziom nieporównywalny idealnie, dynamika wystarczająca do testu.
3. USA nie miały hiperinflacji ani załamania państwa — pasmo 6,1% jest warunkowe na „kraj o ciągłości instytucjonalnej". Test na Polsce (transformacja, inflacja 1989–90: 250–580%) i Niemczech/Argentynie to następny krok i prawdopodobnie poszerzy pasmo dla gospodarek kruchych.
4. Serie FRED są rewidowane; do publikacji produkcyjnej — reguła pre-commitment i mediana źródeł, jak w nocie koncepcyjnej.

## Nazewnictwo — propozycje

Metryka: **regret** (Savage, minimax regret) — po polsku można zostawić „regret" lub „ryzyko indeksacyjne"; „żal" jako nieformalny skrót jest zaskakująco bliski terminowi źródłowemu.

Nazwa jednostki (√(ceny × płace)) — kandydaci:

| Nazwa | Ticker | Uzasadnienie |
|---|---|---|
| **PAR** | PAR | „at par" = po równi, spłata po parytecie; krótkie, międzynarodowe, bez konfliktów |
| **Aequo** | AEQ | łac. *ex aequo* — po równo; brzmi jak jednostka, łatwe w PL i EN |
| **Concordia** | CRD | łac. zgoda; „jednostka zgody" — dokładnie opisuje funkcję (obie strony się zgadzają) |
| **Qist** | QST | arab. قسط — sprawiedliwa miara (pojęcie koraniczne o uczciwych miarach i wagach); naturalny dla finansów bezodsetkowych |
| **Talent** | TLN | historyczna jednostka wartości; czytelna metafora, identyczna w PL/EN |

Rekomendacja robocza: **PAR** jako nazwa główna (uniwersalna, opisowa), **Qist** jako nazwa wariantu dla rynku finansów islamskich. Decyzja niepilna.

## Następne kroki

1. Test kruchych gospodarek: Polska 1950–2025 (GUS/MFW), opcjonalnie Niemcy 1920–23, Argentyna — ile wynosi pasmo, gdy państwo przechodzi transformację/hiperinflację.
2. Mediana źródeł dla obu nóg (CPI: BLS+alternatywy; płace: 2–3 serie) i reguła publikacyjna (pre-commitment, chain-linking, hash).
3. Symulacja pełnej kasy pożyczkowej (wpłaty/wypłaty członków w JW przez dekady) zamiast pojedynczych okien.
