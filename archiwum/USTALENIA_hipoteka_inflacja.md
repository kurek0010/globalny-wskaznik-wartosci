# Ustalenia: zabezpieczenie pieniądza a rodzaj inflacji

**Autor projektu:** Mariusz Kurowski
**Data:** 2026-06-21
**Status:** wyniki robocze (USA, 1996–2025), materiał do przyszłego artykułu.
**Kod:** `prototyp/src/collateral_inflation.py`, `analysis_v4.py`
**Wykresy:** `outputs/figures/36–39_*.png`
**Dane:** FRED — M2 (M2SL), bilans Fed (WALCL/TREAST/WSHOMCB), kredyt banków H.8 (REALLN/BUSLOANS/CONSUMER), cały dług hipoteczny gospodarstw (HHMSDODNS), ceny domów (CSUSHPISA), podaż nowych domów (HOUST/HNFSEPUSSA).

## Teza wyjściowa (autora)

Pieniądz kreowany pod różne zabezpieczenia ma różną „jakość". Hipoteka jest najlepszym zastawem; dług państwowy oparty o przyszłe dochody obywateli — najgorszym. Hipoteza mocna: gdyby podaż pieniądza opierała się wyłącznie na kredycie hipotecznym, inflacja konsumencka byłaby nieznaczna.

## Co pokazują dane

### 1. Inflacja CPI trzyma się ilości pieniądza i monetyzacji długu państwa

Korelacja 12-mies. dynamiki składnika (z wyprzedzeniem) z inflacją CPI:

| Składnik | Najlepsza korelacja z CPI | Wyprzedzenie |
| --- | --- | --- |
| M2 (cały) | +0,52 | 18 mies. |
| dług państwa (Fed UST) | +0,41 | 18 mies. |
| hipoteki — cały dług (HHMSDODNS) | +0,38 | 6 mies. |
| hipoteki — banki (REALLN) | +0,18 | 0 mies. |
| konsumpcja | −0,18 | (endogeniczne) |
| biznes | −0,24 | (endogeniczne) |

Ujemne znaki dla kredytu biznesowego i konsumpcyjnego to endogeniczność (kredyt kurczy się po podwyżkach stóp i szczycie inflacji), nie dowód „antyinflacyjności".

### 2. Rodzaj zabezpieczenia steruje TYM, GDZIE ląduje inflacja

Korelacja współbieżna dynamiki z dwoma rodzajami inflacji:

| Źródło pieniądza | z CPI (konsumencka) | z cenami domów (aktywa) |
| --- | --- | --- |
| hipoteki (cały dług) | +0,35 | **+0,58** |
| dług państwa (Fed UST) | **+0,41** (18 m) | +0,04 |
| M2 (cały) | +0,52 (18 m) | +0,15 |

To jest najważniejszy wynik. Asymetria jest wyraźna:
- **Dług państwa → inflacja konsumencka** (CPI +0,41), a praktycznie **zero** wpływu na ceny domów (+0,04).
- **Hipoteka → inflacja aktywów** (ceny domów +0,58), z częściowym przeciekiem do CPI (+0,35).

Rodzaj kolateralu rzeczywiście decyduje, czy pieniądz ujawnia się w koszyku konsumenta, czy w cenach aktywów.

### 3. Korekta tezy wyjściowej

Pierwotny pomiar (wąski, bankowy REALLN) sugerował, że hipoteki w ogóle nie dają inflacji CPI (korelacja +0,18, zero na leadach). Po zamianie na **cały** dług hipoteczny (z sekurytyzowanym i niebankowym) korelacja z CPI urosła do +0,38. Wniosek: hipoteki **nie są obojętne** dla inflacji konsumenckiej — przeciekają do niej, najpewniej przez wypłatę kapitału z domów (cash-out refinancing finansujący konsumpcję).

Teza autora wymaga więc doprecyzowania: nie „pod hipotekę nie ma inflacji", lecz **„pieniądz hipoteczny napędza głównie inflację aktywów (mieszkań), a dla CPI jest dużo czystszy niż dług państwowy"**. Hierarchia jakości kolateralu się broni; absolutna wersja („zero inflacji") — nie.

### 4. Podaż nowych domów

Łańcuch podaż nowych domów → dług hipoteczny → ceny:
- podaż → hipoteki: +0,25 (24 mies.) — słaby, opóźniony związek; nowe budownictwo nieznacznie poszerza bazę długu hipotecznego.
- hipoteki → ceny: +0,58 (współbieżnie) — silny.
- podaż → ceny: +0,58 — **uwaga, to procykliczność**, nie dowód, że podaż winduje ceny. Deweloperzy budują w czasie boomu, więc rozpoczęcia budów i ceny rosną razem, oba napędzane tym samym popytem kredytowym. Efekt tłumienia cen przez podaż jest wolniejszy i przykryty przez wspólny cykl.

Cykl budowlany: rozpoczęcia budów spadły z ~2250 tys. (2006) do ~500 tys. (2009) i odbudowywały się kilkanaście lat — ta sama dziura, którą widać w skoku MBS w bilansie Fed i w cenach domów.

## Wniosek dla projektu

Kreacja pieniądza rozkłada się na dwa rodzaje inflacji: konsumencką (CPI łapie) i aktywów (CPI nie łapie). Indeksacja oparta na samym CPI jest systematycznie ślepa na połowę zjawiska — co jest bezpośrednim argumentem za jednostką opartą na pracy (AUV), mierzącą realną wartość niezależnie od tego, w którą stronę ucieka pieniądz.

## Zastrzeżenia metodologiczne

Korelacja to nie przyczynowość; związki są często dwustronne (ceny domów ↔ hipoteki to sprzężenie zwrotne). Dane wyłącznie USA — uogólnienie wymaga EBC/BoJ/BoE. Wagi jakości kolateralu (w indeksie Q) są normatywne i sporne (ujęcie austriackie vs główny nurt). Pełne rozplątanie wymaga modelu z opóźnieniami i kontrolą na M2 (np. testy Grangera), nie samych korelacji.
