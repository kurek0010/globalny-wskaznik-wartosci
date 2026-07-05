# Indeks jakości pieniądza — nota projektowa (FDI v0.4, krok 3)

**Autor projektu:** Mariusz Kurowski
**Status:** projekt, dane wpięte do rejestru, obliczenia po pobraniu.
**Powiązanie:** rozszerza Projekt 1 (FDI — Fiat Depreciation Index) o wymiar *jakości*, obok dotychczasowego wymiaru *ilości* (M2).

## 1. Idea i przeformułowanie pojęciowe

Dotychczasowy FDI mierzy *ilość* pieniądza (agregaty M2/M3). Hipoteza tego kroku: dla przewidywania deprecjacji liczy się nie tylko ile pieniądza powstało, ale **przeciwko czemu** został wykreowany — jaki jest skład kolateralu stojącego za kreacją.

Wymaga to ścisłego przeformułowania. W systemie fiat waluta *prawnie* nie jest zabezpieczona żadnym aktywem — nie ma wymienialności na złoto ani na nic innego. Jej wartość bierze się z popytu podatkowego (państwo żąda podatków w swojej walucie) i powszechnej akceptacji. Dlatego nie mówimy o „zabezpieczeniu" w sensie standardu złota, lecz o **jakości kolateralu / ryzyku bilansu**: skład aktywów, przeciwko którym kreowany jest pieniądz, jest obserwowalnym sygnałem o ryzyku przyszłej deprecjacji.

Intuicja ekonomiczna: pieniądz kreowany pod produktywny kredyt lub realne aktywa (hipoteka na istniejącym domu, kredyt obrotowy spłacany z przepływów firmy) jest „kryty" strumieniem wartości, który go umorzy. Pieniądz kreowany pod dług suwerenny jest częściowo samozwrotny — obligacja skarbowa jest „kryta" przyszłymi podatkami lub przyszłą monetyzacją, co przy wysokim zadłużeniu staje się ryzykiem dominacji fiskalnej i presji inflacyjnej.

## 2. Dwie warstwy kreacji pieniądza

Mierzymy skład kolateralu na dwóch poziomach systemu, oba z danych publicznych (USA jako pierwszy przypadek; docelowo EBC, BoJ, BoE).

**Warstwa bazowa — bilans banku centralnego (Fed, raport H.4.1).** Strona aktywów pokazuje, co Fed kupił, kreując rezerwy:
- `fed_treasuries` (FRED: TREAST) — obligacje skarbowe = kolateral suwerenny;
- `fed_mbs` (WSHOMCB) — papiery hipoteczne = kolateral oparty na realnych nieruchomościach;
- `fed_total_assets` (WALCL) — suma bilansu.

**Warstwa szeroka — kredyt banków komercyjnych (raport H.8).** To dominujący kanał kreacji pieniądza:
- `bank_loans_realestate` (REALLN) — kredyty pod nieruchomości;
- `bank_loans_business` (BUSLOANS) — kredyty komercyjne/przemysłowe (produktywne);
- `bank_loans_consumer` (CONSUMER) — kredyty konsumpcyjne;
- `bank_credit_total` (TOTBKCR) — całość kredytu bankowego.

## 3. Konstrukcja indeksu

Dla każdej warstwy liczymy udziały typów kolateralu, np. dla Fed:

```
udział_suwerenny(t)  = fed_treasuries(t) / fed_total_assets(t)
udział_realny(t)     = fed_mbs(t)        / fed_total_assets(t)
```

i analogicznie dla kredytu bankowego (nieruchomości / produktywny / konsumpcyjny).

Indeks jakości Q przypisuje typom kolateralu jawne, zamrożone wagi jakości *w_k ∈ [0,1]* i liczy średnią ważoną udziałami:

```
Q(t) = Σ_k  w_k · udział_k(t),        Σ_k udział_k = 1
```

Proponowane uporządkowanie wag (do dyskusji, nie przesądzone): kredyt produktywny/biznesowy oraz realne aktywa wysoko (kolateral generujący strumień wartości), dług suwerenny nisko (kolateral samozwrotny). Wyższe Q = pieniądz lepiej pokryty realnym/produktywnym kolateralem; niższe Q = większe oparcie na długu suwerennym, czyli wyższe utajone ryzyko deprecjacji.

Włączenie do FDI: zamiast traktować każdą jednostkę przyrostu M2 jednakowo, ważymy ją jakością kolateralu — ekspansja monetarna o niskim Q (np. luzowanie ilościowe skupujące obligacje skarbowe) sygnalizuje silniejszą przyszłą deprecjację niż równa co do wielkości ekspansja kredytu produktywnego.

## 4. Hipoteza empiryczna do przetestowania

Po pobraniu danych testujemy: **czy skład kolateralu (Q) wyprzedza późniejszą deprecjację waluty** (mierzoną CPI lub kursem realnym)? Konkretnie — czy spadki Q (przesunięcie ku długowi suwerennemu, np. 2008–2014 i 2020–2021 w USA) poprzedzają epizody podwyższonej inflacji (2021–2023)? Jeśli tak, Q jest wyprzedzającym komponentem FDI o realnej wartości informacyjnej ponad samo M2.

## 5. Uczciwe zastrzeżenia

To najbardziej teorio-zależny wątek projektu i wymaga ostrożności:

1. **Wagi jakości są normatywne.** Uznanie długu suwerennego za „niższą jakość" to teza w duchu szkoły austriackiej i doktryny realnych weksli. Stanowisko przeciwne (głównego nurtu) głosi, że obligacje skarbowe USA to *najbezpieczniejszy* aktyw świata, a ich obecność w bilansie zwiększa stabilność. Indeks musi być przedstawiony z obiema interpretacjami; wagi powinny być parametrem poddanym analizie wrażliwości, nie ukrytą tezą.

2. **Fiat nie jest prawnie kryty.** Q nie jest miarą „pokrycia" w sensie wymienialności, lecz proxy ryzyka bilansowego/fiskalnego. Należy unikać sugestii, że wysokie Q oznacza wymienialność.

3. **Na razie USA.** Bilanse EBC, BoJ, BoE mają inną strukturę i klasyfikację — porównywalność między walutami wymaga harmonizacji kategorii.

4. **Endogeniczność i kierunek przyczynowości.** QE skupujące obligacje jest *reakcją* na kryzys, a nie tylko jego przyczyną; rozplątanie wymaga ostrożnej analizy szeregów czasowych (np. opóźnienia, testy przyczynowości Grangera).

## 6. Dane — status

Serie wpięte do `src/config.py` (sekcja `MONETARY_QUALITY`), gotowe do pobrania:
`WALCL`, `TREAST`, `WSHOMCB` (bilans Fed) oraz `TOTBKCR`, `REALLN`, `BUSLOANS`, `CONSUMER` (kredyt H.8). Po `python -m src.download && python -m src.harmonize` można policzyć Q i przetestować hipotezę z sekcji 4.
