# Prompt dla Claude Code: automat miesięcznej publikacji TLN-PLN

*Skopiuj wszystko poniżej linii do Claude Code uruchomionego w katalogu repozytorium.*

---

Zbuduj automat GitHub Actions, który każdego miesiąca publikuje nową kotwicę TLN-PLN zgodnie z procedurą z `INSTRUKCJA_aktualizacji.md`. Przeczytaj najpierw: `CLAUDE.md` (zasady repo), `INSTRUKCJA_aktualizacji.md`, `POLITYKA_danych_v0.1.md` (§2 kalendarz, §4 kaskada awaryjna, §5 first-print), `REGULA_publikacyjna_Talent_v0.1.md` oraz kod `prototyp/src/talent_update.py` i `prototyp/src/build_strona.py`. Pracuj etapami i po każdym etapie pokaż, co zrobiłeś.

## Etap 1 — adapter danych GUS (fetcher)

Stwórz `prototyp/src/fetch_gus.py`, który pobiera first-printy potrzebne do kotwicy:

1. **CPI m/m** za najnowszy miesiąc. Zbadaj i wybierz najstabilniejsze źródło maszynowe, w tej kolejności preferencji: oficjalne API GUS (DBW / SDMX / API BDL), a jeśli żadne nie daje miesięcznego m/m wprost — parsowanie tabeli GUS „Miesięczne wskaźniki cen towarów i usług konsumpcyjnych od 1982 roku" (uwaga: format polski, przecinki dziesiętne, „Poprzedni miesiąc = 100"). Udokumentuj wybór w docstringu.
2. **Raz w roku (uruchomienia w lutym):** przeciętne wynagrodzenie w gospodarce narodowej za rok ubiegły z komunikatu Prezesa GUS — jeśli dostępne maszynowo, pobierz; jeśli nie, tylko zgłoś w raporcie „wymaga ręcznego wpisu do WAGE_ANNUAL".

Fetcher zapisuje pobrane wartości do pliku danych `prototyp/data/first_prints_pln.json` (append-only: nigdy nie nadpisuje istniejących miesięcy — to jest wymóg twardy, spójny z `talent_published.json`). Każdy wpis z metadanymi: wartość, źródło (nazwa komunikatu/endpoint), data pobrania.

## Etap 2 — refaktoryzacja talent_update.py

Zmień `talent_update.py` tak, by słowniki `CPI_MM` / `WAGE_ANNUAL` czytał z `first_prints_pln.json` (istniejące wartości w kodzie przenieś do tego pliku jako migrację, z zachowaniem komentarzy źródłowych w polach metadanych). NIE ZMIENIAJ logiki obliczeń ani mechanizmu `talent_published.json` — zakaz rewizji wstecz musi działać dokładnie jak teraz. Kaskada awaryjna: jeśli fetcher nie dostarczył CPI za oczekiwany miesiąc, zastosuj carry-forward ostatniej dynamiki (jest w polityce §4.1) i ustaw flagę alertu; jeśli braki trwają ≥2 miesiące — przerwij z błędem zamiast publikować (eskalacja do człowieka).

## Etap 3 — workflow GitHub Actions

`.github/workflows/publikacja_kotwicy.yml`:
- cron: `0 9 25 * *` (25. dzień, 09:00 UTC — po odcięciu danych 24. 12:00 CET) + `workflow_dispatch` do ręcznych uruchomień z opcją dry-run;
- kroki: checkout → Python 3.11 → `pip install -r prototyp/requirements.txt` → `python prototyp/src/fetch_gus.py` → `python prototyp/src/talent_update.py` → `python prototyp/src/build_strona.py` → commit + push;
- commit tylko gdy są nowe kotwice (skrypt update wypisuje ile opublikował; przy zerze — zakończ bez commita); komunikat commita: `Kotwica TLN-PLN za YYYY-MM: <wartość>` + linia z alertami, jeśli były;
- `permissions: contents: write`; commit jako `github-actions[bot]`;
- przy alercie kaskady awaryjnej lub błędzie: utwórz Issue w repo (gh CLI jest na runnerach) z opisem, co się stało i co ma zrobić człowiek;
- żadnych sekretów nie potrzebujesz (dane GUS są publiczne bez klucza; NIE używaj `prototyp/.env`).

## Etap 4 — test przed włączeniem

1. Uruchom lokalnie pełny łańcuch (fetch → update → build) i pokaż wynik. Ma zgłosić „brak nowych miesięcy" albo opublikować wyłącznie miesiące, których nie ma w `talent_published.json` (na dziś opublikowane są kotwice do 2026-04; jeśli GUS wydał już CPI za maj/czerwiec 2026, automat powinien je dodać — pokaż wartości przed commitem).
2. Uruchom workflow ręcznie (`workflow_dispatch`, dry-run) i pokaż log.
3. Dopiero po obu testach: włącz cron i zaktualizuj `INSTRUKCJA_aktualizacji.md` (sekcja „Automatyzacja" → opisz, że działa, jak wyłączyć i jak uruchomić ręcznie) oraz dopisz jedną linię do `CLAUDE.md` w sekcji „Aktualizacja miesięczna".

## Wymogi twarde (nie negocjuj z nimi)

- Nigdy nie modyfikuj wstecz `talent_published.json`, `first_prints_pln.json` ani opublikowanych kotwic — tylko dopisywanie.
- Nie edytuj ręcznie generowanych HTML (lista w `CLAUDE.md`) — wszystko przez builder.
- Nie zmieniaj formuły Talenta ani definicji nóg — to wymaga procesu TIP.
- Wartości liczbowe w raporcie końcowym: pokaż ostatnią kotwicę przed i po, żeby człowiek mógł ocenić sensowność (sanity check: |m/m| > 2% = podejrzane przy obecnej inflacji).
