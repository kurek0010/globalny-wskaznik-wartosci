# Prompt dla Claude Code: KaTeX + automatyczna przebudowa strony po edycji treści

*Skopiuj wszystko poniżej linii do Claude Code w katalogu repozytorium.*

---

Dwa zadania frontowo-infrastrukturalne. Przeczytaj najpierw `CLAUDE.md` (zasada „wszystko przez builder"). Pracuj etapami, po każdym pokaż efekt.

## Etap 1 — KaTeX na stronach dokumentów

W szablonie `SHELL` w `prototyp/src/build_strona.py` dodaj renderowanie wzorów LaTeX przez KaTeX (wyłącznie z cdnjs.cloudflare.com):

1. W `<head>`: arkusz `katex.min.css`.
2. Przed `</body>`: `katex.min.js`, potem `contrib/auto-render.min.js` (z atrybutem `defer`), potem wywołanie:
   `renderMathInElement(document.body, {delimiters: [{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}], throwOnError: false})` — uruchamiane po załadowaniu (np. `onload` na skrypcie auto-render).
3. Zadbaj, by KaTeX NIE dotykał bloków kodu (` ``` ` i `` ` ``) — auto-render domyślnie ignoruje `<code>/<pre>`, zweryfikuj to na `regula_publikacyjna.html`, gdzie wzory są dziś w blokach kodu i mają zostać nietknięte.
4. Uwaga na kolizję ze znakiem dolara w treści: teksty zawierają kwoty typu „147 $" — sprawdź wszystkie generowane strony, czy auto-render nie skleił przypadkiem dwóch dolarów w „wzór". Jeśli tak: usuń pojedynczy delimiter `$` z konfiguracji (zostaw tylko `$$` i dodaj `\\(` / `\\)` dla wzorów w linii) — bezpieczniejsze przy treściach finansowych.
5. Test: dopisz na końcu dowolnego pliku md (tymczasowo) wzór `$$A(m)=100\cdot\sqrt{I_c(m)\cdot I_w(m)}$$`, przebuduj, pokaż że renderuje się jak w LaTeX-u, po czym usuń testowy wpis.

## Etap 2 — automatyczna przebudowa po zmianie treści

Nowy workflow `.github/workflows/przebudowa_strony.yml`:

- **Trigger:** `push` na `main` z filtrem `paths` obejmującym WYŁĄCZNIE pliki md kompilowane na stronę — czyli dokładnie klucze słownika `DOCS` z buildera (dziś: `ARTYKUL_Talent_popularnonaukowy.md`, `ARTYKUL_wprowadzenie_i_zastosowania.md`, `REGULA_publikacyjna_Talent_v0.1.md`, `WYSCIG_kandydatow_minimalny_zal.md`, `WYNIKI_test_stulecia_USA.md`, `WYNIKI_kruche_gospodarki.md`, `WYNIKI_talent_dwustronny.md`, `TIP/README.md`) plus `prototyp/src/strona_szablon.html` i `prototyp/src/build_strona.py` (zmiana szablonu/buildera też ma przebudowywać). ŻADNYCH innych ścieżek — dokumenty robocze (SZKIC_*, PROMPT_*, OCENA_*, TALENTY_*, waluty/, archiwum/ itd.) nie mogą uruchamiać builda.
- **Kroki:** checkout → Python + `pip install -r prototyp/requirements.txt` → `python prototyp/src/build_strona.py` → commit + push wygenerowanych HTML **tylko jeśli są zmiany** (`git diff --quiet` guard), autor `github-actions[bot]`, komunikat: `Przebudowa strony po zmianie treści`.
- **Bez pętli:** workflow commituje tylko pliki `.html` — one nie są w `paths`, więc własny commit nie wyzwoli kolejnego builda. Upewnij się, że tak jest.
- `permissions: contents: write`, `concurrency` z grupą `przebudowa-strony` (bez anulowania publikacji kotwicy — osobna grupa).
- **Synchronizacja na przyszłość:** dopisz komentarz w YAML i jedną linię w `CLAUDE.md` (sekcja o builderze): „dodajesz plik do DOCS → dodaj go też do paths w przebudowa_strony.yml".

## Etap 3 — weryfikacja

1. Lokalnie: builder przechodzi, strony z KaTeX wyglądają poprawnie, bloki kodu nietknięte, kwoty z „$" nierozjechane.
2. Zrób testowy commit drobnej zmiany w jednym z plików DOCS (np. literówka w ARTYKUL_wprowadzenie...) i push — pokaż, że workflow się uruchomił i dopchnął przebudowane HTML.
3. Zrób commit zmiany w pliku spoza listy (np. dowolny SZKIC_*) — pokaż, że workflow się NIE uruchomił.
4. Zaktualizuj `INSTRUKCJA_aktualizacji.md` (krótka wzmianka w sekcji Automatyzacja: drugi workflow, co wyzwala, jak wyłączyć).

## Wymogi twarde

- Zero zmian w logice obliczeń i workflow publikacji kotwicy.
- CDN wyłącznie cdnjs.cloudflare.com; żadnych nowych zależności Pythona.
- Wygenerowane HTML nadal wyłącznie z buildera; markdown pozostaje kanoniczny.
