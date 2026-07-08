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

## Automatyzacja (zadanie dla Claude Code)

Docelowo: GitHub Action (cron `0 10 25 * *`), która pobiera first-printy (adapter GUS: komunikaty lub API DBW), dopisuje do słowników lub czyta z pliku danych, uruchamia oba skrypty, commituje z raportem i alertami. Do czasu automatu — procedura ręczna powyżej (~10 minut).

## Inne waluty (gdy powstaną TLN-USD, TLN-EUR…)

Ta sama kadencja per kraj wg kalendarza z karty walutowej (`waluty/TALENT-XXX.md`): kotwica 25. dnia z danych opublikowanych do 24., osobny plik `talent_published_XXX.json`, osobny alert-log. Kursy krzyżowe (TLN-PLN-USD itd.) liczą się automatycznie z kotwic i kursów NBP — bez dodatkowych publikacji.
