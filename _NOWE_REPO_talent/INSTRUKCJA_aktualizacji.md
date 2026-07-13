# Instrukcja miesięcznej aktualizacji Talenta (dla Claude Code / administratora)

**Kadencja — ścisła, z `REGULA_publikacyjna_Talent_v0.1.md` §2 i `POLITYKA_danych_v0.1.md` §2:**

| Kiedy | Co się dzieje |
|---|---|
| ~15. dzień miesiąca | GUS publikuje CPI za miesiąc poprzedni |
| ~21. dzień | GUS publikuje płace/zatrudnienie sektora przedsiębiorstw |
| **24. dzień, 12:00** | **odcięcie danych** — do obliczeń wchodzi tylko to, co już opublikowane |
| **25. dzień** | **obliczenie i publikacja kotwicy** + ścieżki dziennej na okno 26. bm. – 25. następnego miesiąca |

Zasada żelazna: raz opublikowana wartość nigdy nie jest zmieniana (`talent_published.json` pilnuje tego w kodzie — skrypt dopisuje tylko nowe miesiące). Pierwsza publikacja: 2026-07-08 (kotwice do IV 2026).

## Procedura (25. dnia miesiąca)

1. **Zbierz first-printy GUS** (linki w `POLITYKA_danych_v0.1.md` §1):
   - CPI m/m za nowy miesiąc — komunikat GUS lub tabela „Miesięczne wskaźniki cen…od 1982 roku";
   - raz w roku (po ~9 lutego): przeciętne wynagrodzenie w gospodarce narodowej za rok ubiegły (komunikat Prezesa GUS) — zastępuje proxy.
2. **Dopisz wartości** do słowników `CPI_MM` / `WAGE_ANNUAL` w `prototyp/src/talent_update.py`, z komentarzem źródłowym (nazwa komunikatu + data odczytu).
3. **Uruchom:** `cd prototyp && python src/talent_update.py` — wypisze nowe kotwice i alerty; potem `python src/build_strona.py`.
4. **Commit + push** (Pages zaktualizuje stronę automatycznie). Komunikat commita: `Kotwica TLN-PLN za YYYY-MM: <wartość>`.
5. **Sprawdź alerty** ze skryptu (np. proxy płac, tryb awaryjny |g−1|>15%) — alert nie blokuje publikacji, ale musi trafić do komunikatu commita.

## Znane prowizoria (stan 2026-07)

- Noga płac = roczne komunikaty GN interpolowane; punkt 2026 to **proxy** (+5,8% r/r z sektora przedsiębiorstw, V 2026) — zastąpić komunikatem GN w lutym 2027. Docelowo: płace miesięczne sektora przedsiębiorstw (fundusz/MA12, TIP-0001) i mediana ZUS (TIP-0002) — wymaga adaptera GUS BDL.
- Noga cen = jedno źródło (GUS m/m). HICP-PL: Eurostat przeszedł na COICOP-2018 (zbiór `prc_hicp_minr`), stary `prc_hicp_midx` zamknięty na XII 2025 — adapter do nowego zbioru przed włączeniem drugiego źródła.
- FRED/OECD (`POLCPIALLMINMEI`) opóźniony o ~15 miesięcy — NIE nadaje się do aktualizacji bieżących (tylko do historii).

## Automatyzacja

**Działa od 2026-07-09.** GitHub Action `.github/workflows/publikacja_kotwicy.yml`,
cron `0 9 25 * *` (25. dnia miesiąca, 09:00 UTC — po odcięciu danych 24. 12:00 CET):

1. `prototyp/src/fetch_gus.py` — pobiera first-printy CPI m/m z tabeli GUS
   „Miesięczne wskaźniki cen… od 1982 roku" (CSV, jedyne sprawdzone źródło
   maszynowe — API DBW i BDL nie dają miesięcznego CPI m/m dla Polski),
   append-only do `prototyp/data/first_prints_pln.json`. Płace roczne (komunikat
   Prezesa GUS) — próba automatyczna tylko w lutym, inaczej zgłasza potrzebę
   ręcznego wpisu.
2. `prototyp/src/talent_update.py` — czyta z `first_prints_pln.json`, liczy nowe
   kotwice (zakaz rewizji wstecz przez `talent_published.json` bez zmian).
   Kaskada awaryjna: 1 brakujący miesiąc CPI = carry-forward ostatniej dynamiki
   + alert; 2 kolejne braki = przerwanie **bez** publikacji (Issue w repo).
3. `prototyp/src/build_strona.py` — przebudowuje stronę.
4. Commit (`github-actions[bot]`) i push — **tylko gdy są nowe kotwice**;
   komunikat: `Kotwica TLN-PLN za YYYY-MM: <wartość>` + alerty.

**Ręczne uruchomienie:** zakładka Actions → „Publikacja kotwicy TLN-PLN" →
Run workflow (opcjonalnie zaznacz `dry_run`, żeby zobaczyć podgląd zmian bez
commita/pusha).

**Wyłączenie:** zakładka Actions → „Publikacja kotwicy TLN-PLN" → „…" →
Disable workflow. Albo usuń/zakomentuj blok `schedule:` w pliku workflow
(zostanie tylko ręczne uruchamianie przez `workflow_dispatch`).

**Błąd/alert automatu** → automat tworzy Issue w repozytorium z logiem i
instrukcją, co ma zrobić człowiek (zwykle: ręczny wpis do
`first_prints_pln.json`, potem ponowne ręczne uruchomienie).

**Drugi automat — przebudowa strony po zmianie treści.** GitHub Action
`.github/workflows/przebudowa_strony.yml` (działa od 2026-07-12): trigger to
push na `main`, który zmienia jeden z plików `.md` kompilowanych na stronę
(dokładnie klucze słownika `DOCS` w `build_strona.py`) albo
`prototyp/src/strona_szablon.html`/`prototyp/src/build_strona.py`. Uruchamia
wyłącznie `build_strona.py` i commituje wygenerowane HTML (autor
`github-actions[bot]`, komunikat `Przebudowa strony po zmianie treści`) —
tylko jeśli builder faktycznie coś zmienił. Dokumenty spoza słownika `DOCS`
(`SZKIC_`, `TALENTY_`, `waluty/`, `PODSUMOWANIE_` itd.) nie są na liście
`paths` i push do nich nie uruchamia builda. **Dodajesz plik do `DOCS`** →
dopisz go też do `paths` w tym workflow, inaczej treść się zmieni, ale strona
nie. Wyłączenie: zakładka Actions → „Przebudowa strony po zmianie treści" →
„…" → Disable workflow.

## Inne waluty (gdy powstaną TLN-USD, TLN-EUR…)

Ta sama kadencja per kraj wg kalendarza z karty walutowej (`waluty/TALENT-XXX.md`): kotwica 25. dnia z danych opublikowanych do 24., osobny plik `talent_published_XXX.json`, osobny alert-log. Kursy krzyżowe (TLN-PLN-USD itd.) liczą się automatycznie z kotwic i kursów NBP — bez dodatkowych publikacji.
