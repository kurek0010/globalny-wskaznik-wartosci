# Źródła danych do backtestu AUV 1900–1995

**Cel:** zastąpić rekonstrukcję ilustracyjną (wykres 47) prawdziwym obliczeniem na twardych, cytowalnych danych historycznych. Format wpisywania: `prototyp/data/manual/backtest_historyczny.csv` (kolumny opisane niżej). Skrypt liczący: `src/backtest_1900.py`.

Potrzebujemy trzech serii rocznych za okres 1900–1995. Wszystkie są publiczne i darmowe.

## 1. Realny indeks cen surowców → kolumna `commodity_index_real`

**Podstawowe: indeks Grilli–Yang, aktualizacja Pfaffenzellera.**
- Grilli, E., Yang, M.C. (1988), „Primary Commodity Prices, Manufactured Goods Prices…", World Bank Economic Review.
- Aktualizacja: Pfaffenzeller, Newbold, Rayner (2007) — dane do ~2010, udostępniane publicznie (Stephan Pfaffenzeller, arkusz „GYCPI"). Użyj indeksu **realnego** (deflowanego MUV — manufactures unit value), non-fuel lub all, konsekwentnie.
- Pokrycie: 1900–2010, roczne. Idealne.

**Alternatywa/kontrola: David Jacks (2013), „From Boom to Bust: A Typology of Real Commodity Prices".**
- Realne ceny surowców 1850–2015, indeks zbiorczy i pojedyncze surowce. Strona autora (SFU) — pliki Excel publiczne.
- Dobre do testu wrażliwości (czy wynik zależy od wyboru indeksu).

## 2. Realne światowe PKB na osobę → kolumna `world_gdppc_real`

**Maddison Project Database (2020), Bolt & van Zanden.**
- Realne PKB/os. w dolarach międzynarodowych 1990/2011, świat i kraje, od roku 1 do 2018.
- Groningen Growth and Development Centre — plik publiczny (Excel/Stata).
- Weź agregat światowy (lub zważ regiony, jeśli brak gotowego agregatu — patrz uwaga niżej).

## 3. (Opcjonalnie) Realna płaca historyczna → kolumna `us_real_wage`

Dla wariantu „w godzinach pracy" (nie PKB), odpowiadającego na LUKĘ 7 recenzji.
- **Officer & Williamson, MeasuringWorth.com** — realne płace USA 1774–dziś, roczne, publiczne.
- Alternatywnie Gregory Clark dla Anglii (bardzo długie szeregi).
- Pozwoli policzyć AUV deflowany *płacą* obok wariantu deflowanego PKB i pokazać wachlarz.

## Uwagi metodyczne (do zapisania w artykule)

- **Deflator.** Grilli–Yang jest deflowany MUV, nasze AUV 1996+ efektywnie CPI. To różne deflatory — do odnotowania; dla kształtu wieloletniego nieistotne, dla precyzji tak.
- **Zszycie (chain-linking).** Skrypt zszywa część historyczną z naszym policzonym 1996+ we wspólnym punkcie (1995/1996), zachowując ciągłość — zgodnie z regułą niezmienniczości (chain-linking, patrz REGULA_publikacyjna_Talent_v0.1.md §4).
- **Agregat światowy vs USA.** Jeśli łatwiej dostępne są dane USA (płace, CPI), można policzyć wariant „AUV-USA" 1900+ i osobno pilnować, że wniosek (wieloletni spadek) nie zależy od geografii.
- **Cel testu, nie liczba.** Rozstrzygamy pytanie jakościowe: czy AUV ma wieloletni trend (a jeśli tak, jaki znak i rząd), czy oscyluje wokół stałej. Rekonstrukcja ilustracyjna wskazuje silny spadek (~−2%/rok); ten test ma to potwierdzić lub obalić na twardych danych.

## Jak policzyć po wypełnieniu
```
# wpisz dane do prototyp/data/manual/backtest_historyczny.csv (choćby co 5 lat — reszta się zinterpoluje)
cd prototyp
python -m src.backtest_1900
# -> outputs/figures/48_auv_backtest_1900_dane.png + wydruk trendu
```
