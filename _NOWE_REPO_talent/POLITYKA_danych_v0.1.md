# Polityka wprowadzania danych — v0.1

**Data:** 2026-07-07 · **Status:** projekt · **Uzupełnia:** `REGULA_publikacyjna_Talent_v0.1.md`
Reguła publikacyjna mówi *co* i *dlaczego*; ten dokument mówi *którędy dokładnie* — co do serii, tabeli urzędu i dnia. Zasada nadrzędna bez zmian: kod jest metodologią; ta polityka jest jego opisem słownym.

## 1. Rejestr serii produkcyjnych (Talent-PL)

| # | Seria | Źródło i publikacja | Dzień publikacji | Rola |
|---|---|---|---|---|
| C1 | Wskaźnik cen towarów i usług konsumpcyjnych (m/m) | GUS, komunikat „Wskaźniki cen towarów i usług konsumpcyjnych" | ~15. dzień m+1 | noga cen |
| C2 | HICP Polska (m/m) | Eurostat, tabela `prc_hicp_midx`, geo=PL | ~17.–19. dzień m+1 | noga cen |
| C3 *(docelowo)* | Indeks cen online | do zbudowania/wyboru (scraping koszyka) | dziennie | noga cen, 3. źródło |
| W1 | Przeciętne wynagrodzenie w sektorze przedsiębiorstw | GUS, komunikat „Przeciętne zatrudnienie i wynagrodzenie w sektorze przedsiębiorstw" | ~21. dzień m+1 | noga płac (fundusz) |
| W2 | Przeciętne zatrudnienie w sektorze przedsiębiorstw | ten sam komunikat co W1 | ~21. dzień m+1 | noga płac (mianownik MA12) |
| W3 *(kandydat, TIP-0002)* | Mediana wynagrodzeń w gospodarce narodowej | GUS, „Rozkład wynagrodzeń w gospodarce narodowej" (rejestry ZUS+MF, miesięcznie, szereg od I 2010) | ~2 miesiące po m | noga płac, 2. źródło |
| F1 | Kursy średnie walut | NBP, tabela A | każdy dzień roboczy | tryb awaryjny; przeliczenia |

Serie testów historycznych (FRED: CPIAUCNS, CES3000000008, A939RC0A052NBEA, AHETPI, PAYEMS; POLCPIALLMINMEI) są **zamrożonymi migawkami** w `prototyp/data/raw/` z datą pobrania w nagłówku raportów — nie podlegają tej polityce, bo nie zasilają publikacji.

## 2. Kalendarz jednego cyklu (miesiąc m)

| Dzień | Zdarzenie |
|---|---|
| ~15. m+1 | GUS publikuje C1 za m |
| ~17.–19. m+1 | Eurostat publikuje C2 za m |
| ~21. m+1 | GUS publikuje W1, W2 za m |
| **24. m+1, 12:00 CET** | **odcięcie danych** — do obliczeń wchodzi wyłącznie to, co opublikowano do tej chwili |
| **25. m+1** | obliczenie kotwicy A(m); publikacja A(m) + pełnej ścieżki dziennej na okno 26. m+1 → 25. m+2; publikacja hasha danych wejściowych i tagu wersji kodu |

## 3. Co dokładnie wchodzi do wzoru

1. **Dynamiki, nie poziomy.** Z każdego źródła bierzemy **oficjalnie opublikowaną dynamikę m/m z pierwszego odczytu** (first print). Indeksy nóg budujemy łańcuchowo z tych dynamik. Dzięki temu późniejsze rewizje poziomów niczego nie psują — patrz §5.
2. **Noga cen:** dynamika = mediana dynamik dostępnych źródeł C (przy dwóch źródłach: średnia geometryczna).
3. **Noga płac:** `W(m) = W1(m)×W2(m) / MA12(W2)(m)` (fundusz / wygładzone zatrudnienie, TIP-0001), potem MA12 całego indeksu.

## 4. Kaskada awaryjna opóźnień (fallback)

Zapisana z góry, uruchamiana mechanicznie:

1. **Źródło spóźnione w dniu odcięcia** → jego dynamika za m = dynamika z ostatniej dostępnej publikacji tego źródła (carry-forward); gdy publikacja nadejdzie, różnica wchodzi wyłącznie w dynamikę kolejnego cyklu. Publiczny alert w metadanych odczytu.
2. **Źródło spóźnione ≥2 cykle** → nogę liczy mediana pozostałych źródeł; alert eskalowany.
3. **Źródło ogłasza zaprzestanie publikacji** → wypada z rejestru przy najbliższej rewizji wg procedury TIP (chain-linking, test nakładania); do tego czasu pkt 2.
4. **Wszystkie źródła nogi niedostępne** (stan nadzwyczajny) → kotwica za m = kotwica за m−1 przedłużona ostatnią znaną dynamiką; jeśli stan trwa >3 cykle — procedura trybu awaryjnego z reguły §5.2.

## 5. Rewizje danych źródłowych

- Wiąże **pierwszy oficjalny odczyt** dynamiki m/m. Opublikowane wartości Talenta są ostateczne — rozliczona umowa nigdy nie jest „przeliczana po rewizji" (odpowiedź na pytanie: *nie*, umowa nie była rozliczona krzywdząco — była rozliczona po jedynej wartości, którą obie strony mogły znać; symetrycznie działa to w obie strony).
- Rewizje wpływają na przyszłość wyłącznie pośrednio: kolejne dynamiki first-print urzędy liczą już od zrewidowanych poziomów — łańcuch sam się koryguje bez naszej ingerencji.
- Rozjazd skumulowany: raz w roku publikujemy **raport pojednawczy** (indeks z first-printów vs indeks z danych ostatecznych) — jawna miara kosztu zasady nierewidowania; sama publikacja, zero korekt.

## 6. Zmiany bazy, wag i metodologii urzędów

- Pracujemy na dynamikach m/m, więc **zmiana roku bazowego urzędu (np. 2015=100 → 2020=100) jest neutralna** — dynamika nie zależy od bazy.
- Zmiana koszyka/wag CPI (coroczna, styczniowa u GUS): przyjmujemy dynamikę publikowaną przez urząd (już łańcuchowaną przez GUS/Eurostat wg standardu HICP); w metadanych odczytu odnotowujemy miesiąc zmiany wag.
- Zmiana **definicji** serii (np. rozszerzenie próby W1): traktowana jak wymiana źródła → procedura TIP z oknem nakładania i testem zgodności dynamik (korelacja > próg), zszycie łańcuchowe, nigdy wstecz.

## 7. Świadome kompromisy (jawna lista decyzji)

1. **Średnia zamiast mediany (na dziś).** Przeciętne wynagrodzenie sektora przedsiębiorstw pomija firmy <9 osób i rośnie szybciej niż płaca typowego pracownika (górny ogon rozkładu) — noga płac na średniej lekko sprzyja wierzycielowi. To decyzja świadoma, wymuszona historyczną dostępnością danych, częściowo złagodzona przez TIP-0001 (fundusz/zatrudnienie — usuwa artefakt kryzysowy). **Kierunek docelowy: mediana z rejestrów ZUS+MF** — GUS publikuje ją już miesięcznie („Rozkład wynagrodzeń w gospodarce narodowej", od I 2010) — przejście wg szkicu TIP-0002 po zbadaniu opóźnienia i stabilności serii.
2. **Dwa źródła cen zamiast trzech.** C3 (indeks online) pozostaje do zbudowania; do tego czasu tripwire działa na parze C1/C2, które nie są w pełni niezależne (HICP liczony z danych GUS inną metodą). Odnotowane jako słabość.
3. **First print zamiast prawdy ostatecznej.** Koszt mierzony raportem pojednawczym (§5); wybór podyktowany rozstrzygalnością umów.

## 8. Integralność publikacji

Każdy odczyt zawiera: wartości, listę użytych publikacji źródłowych (nazwa komunikatu + data), hash SHA-256 plików wejściowych, tag wersji kodu, flagi alertów (§4). Odtworzenie: `python src/talent_daily.py` na tych samych wejściach musi dać identyczny wynik co do grosza.
