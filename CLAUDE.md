# Instrukcje dla agentów pracujących w tym repozytorium

## Architektura strony — ZASADA NADRZĘDNA

Wszystkie pliki HTML w korzeniu generuje **builder**: `prototyp/src/build_strona.py`.

**NIGDY nie edytuj bezpośrednio:** `index.html`, `talent_strona.html`, `whitepaper.html`, `wprowadzenie.html`, `regula_publikacyjna.html`, `wyscig_kandydatow.html`, `wyniki_*.html` — builder nadpisze te zmiany bez ostrzeżenia.

Zamiast tego edytuj źródła i uruchom builder:

| Chcesz zmienić | Edytuj | Potem |
|---|---|---|
| układ/treść strony głównej | `prototyp/src/strona_szablon.html` | `cd prototyp && python src/build_strona.py` |
| treść dokumentów (whitepaper itd.) | odpowiedni plik `.md` w korzeniu (markdown jest kanoniczny) | j.w. |
| listę dokumentów konwertowanych na HTML | słownik `DOCS` w `build_strona.py` | j.w. |
| wykresy/dane na stronie | skrypty w `prototyp/src/` (aktualizują `data/processed/`) | j.w. |

Ręcznie utrzymywane strony HTML (wolno edytować): `specyfikacja.html`, `dla_agenta.html`.
W szablonie markery `__DATA__`, `__FX__`, `__WAGE__`, `__CURCARDS__` wypełnia builder — nie usuwaj ich.

## Zasady merytoryczne projektu (obowiązują też agentów)

1. **Kod jest metodologią.** Zmiany formuły Talenta wyłącznie przez proces TIP (`TIP/README.md`): nazwij problem → zaproponuj → przetestuj na danych → dopiero zmień regułę. Nigdy nie zmieniaj formuły „przy okazji".
2. **Nigdy wstecz.** Opublikowane wartości i wyniki raportów nie są przeliczane po cichu; poprawki wchodzą jako nowe wersje z uzasadnieniem.
3. **Dane wejściowe:** rejestr źródeł i kaskady awaryjne w `POLITYKA_danych_v0.1.md`. Migawki danych w `prototyp/data/raw/` mają charakter dokumentacyjny — nie nadpisuj ich bez odnotowania daty pobrania.
4. **Liczby w dokumentach** pochodzą z konkretnych skryptów (`regret_*.py`, `talent_daily.py` itd.) — zmieniając skrypt, sprawdź, które dokumenty cytują jego wyniki.
5. `prototyp/.env` zawiera klucz API — nigdy nie commitować (jest w .gitignore).

## Podział ról (umowa projektu)

Utrzymanie strony i kodu: Claude Code (to repo). Treści, metodologia, decyzje: praca z autorem w Cowork. Wspólny styk to builder i pliki `.md` — dlatego zasada „wszystko przez builder" jest nienegocjowalna.
