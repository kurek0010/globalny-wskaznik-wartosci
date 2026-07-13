# TIP-0001: Noga płacowa v0.2 — fundusz płac / wygładzone zatrudnienie

**Autor:** Mariusz Kurowski · **Data:** 2026-07-05 · **Status:** Wdrożony
*(TIP udokumentowany retroaktywnie — zmiana przeszła pełny proces przed formalizacją systemu TIP.)*

## Problem

Przeciętne wynagrodzenie = fundusz płac / bieżąca liczba pracujących. W kryzysie pracę tracą najpierw najsłabiej zarabiający, więc średnia płaca pozostałych **rośnie dokładnie wtedy, gdy dochody społeczeństwa spadają** (efekt składu). Noga płacowa oparta na przeciętnej zawyżałaby ciężar zobowiązań w najgorszym momencie — dokładnie tam, gdzie własność minimaksowa Talenta ma znaczenie.

## Proponowana zmiana

```
W(m) = FunduszPłac(m) / MA12(Zatrudnienie)(m)     (średnia krocząca, przyczynowa)
```

Mianownik wygładzony 12-miesięcznie „pamięta" pełne zatrudnienie: w kryzysie miara uczciwie opada, przy odbiciu symetrycznie tłumi fałszywy spadek. Zero nowych źródeł danych — oba składniki pochodzą z tych samych sprawozdań firm (GUS; w teście: BLS/FRED).

## Test na danych (przed zmianą reguły)

Dane: USA, miesięczne 2000-01–2026-06 (FRED: AHETPI, PAYEMS; `data/raw/fred_*_monthly_2000_2026.csv`). Wyniki (`data/processed/wage_leg_v2_monthly.csv`):

| Epizod | Przeciętna (stara) | Fundusz/MA12 (nowa) |
|---|---|---|
| IV 2020 (szok COVID), m/m | **+4,2%** (artefakt) | **−8,9%** (realny ubytek) |
| Wielka recesja IX 2008→XII 2009 | +3,5% | +3,2% |
| Dryf 2000→2026 (26,5 roku) | +135,7% | +136,2% |

## Czego zmiana NIE psuje

Dryf długookresowy identyczny (różnica 0,5 p.p. na ćwierć wieku — opóźnienie mianownika znosi się w dynamikach przy stabilnym wzroście zatrudnienia). Powolne recesje: obie metody zbieżne. Zmiana działa wyłącznie przy gwałtownych szokach zatrudnienia — zgodnie z intencją.

## Decyzja

Wdrożono do `REGULA_publikacyjna_Talent_v0.1.md` (definicja I_w v0.2) dnia 2026-07-05. Wykres porównawczy obu metod: `talent_strona.html`. Docelowym rozszerzeniem pozostaje mediana wzrostu płac tych samych osób z danych ZUS (osobny TIP, gdy dostępność danych zostanie zbadana).
