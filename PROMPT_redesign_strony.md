# Prompt dla Claude Code: redesign strony głównej (panel wykresów + porządki)

*Skopiuj wszystko poniżej linii do Claude Code w katalogu repozytorium.*

---

Przebuduj stronę główną Talenta według zatwierdzonego projektu. Przeczytaj najpierw `CLAUDE.md` — obowiązuje żelazna zasada: edytujesz WYŁĄCZNIE `prototyp/src/strona_szablon.html` i `prototyp/src/build_strona.py`, nigdy wygenerowane HTML; po każdej zmianie `cd prototyp && python src/build_strona.py`. Pracuj etapami, po każdym pokaż efekt.

## Etap 1 — hak liczbowy nad sekcją wartości

Pod nagłówkiem strony dodaj jedno zdanie-hak z liczbą **liczoną przez builder** (nie wpisaną na sztywno). Builder (build_strona.py) liczy z `talent_anchors.csv`: `pct = I_c(średnia 2020) / I_c(ostatnia) × 100` i wstawia w szablon przez marker `__HOOK_PCT__` (zaokrąglone do pełnych %; dziś ≈ 67). Treść:

> „Pożyczyłeś komuś 1000 zł w 2020 roku? Oddane dziś, kupują już tylko **{pct}%** tego, co wtedy. W Talentach oddaje się dokładnie tyle wartości, ile się pożyczyło."

Stylistycznie wyraźne (większy font niż body, ale nie krzykliwe). Bez rozwijania przykładu — jedno zdanie i kropka; słowo „Talentach" linkuje do `wprowadzenie.html`.

## Etap 2 — sekcja rynkowa: kafle + panel wykresów obok siebie

Zastąp obecne trzy sekcje wykresów (Indeks Talenta / Ile waluty kosztuje / Noga płacowa) JEDNĄ sekcją rynkową:

**Układ:** na szerokim ekranie (>820px) dwie kolumny: lewa (~38%) — kafle walutowe, prawa (~62%) — panel wykresu. Na wąskim: kafle nad panelem. Kafle mają być WYRAŹNE — obecny styl kart (duża złota liczba) zostaje, siatka 2×3.

**Kafle (lewa kolumna):** obecne karty „1 TLN w PLN/USD/EUR/CHF/GBP/JPY" + na górze karta główna „Wartość dziś (TLN-PLN)" z wartością dzienną pre-commitment. Każdy kafel jest **klikalny**: klik przełącza panel wykresu na tę serię (kafel aktywny dostaje złotą ramkę). Data przy kaflach walutowych: bierz z ostatniego wiersza `talent_w_walutach.csv` (nie hardkoduj „XII 2025").

**Panel wykresu (prawa kolumna), wzorzec bankier.pl:**
- nagłówek: nazwa serii + ostatnia wartość + zmiana % w wybranym okresie (zielona/czerwona);
- zakładki serii (te same co kafle): Indeks TLN-PLN · w PLN · w USD · w EUR · w CHF · w GBP · w JPY; plus dwie nieaktywne zakładki „TLN-USD — wkrótce", „TLN-EUR — wkrótce" (opacity, bez akcji);
- przyciski okresu: 1R · 5L · 10L · Max;
- jeden wykres liniowy z wypełnieniem (istniejący Chart.js), przełączany JS-em bez przeładowania; dane z istniejących markerów `__DATA__` (kotwice, indeks) i `__FX__` (wyceny walutowe);
- pod wykresem dotychczasowa linijka harmonogramu publikacji (`__ANCHORFOR__`/`__UPDATED__`) zostaje.

**USUŃ całkowicie:** sekcję „Noga płacowa: dwie metody pomiaru" (wykres + podpis) i marker `__WAGE__` z szablonu oraz jego obsługę w builderze (dane `wage_leg_v2.json` zostają w repo — używa ich dokumentacja).

## Etap 3 — odchudzenie sekcji „Przeczytaj więcej"

Zostają tylko (w tej kolejności): **Wprowadzenie** (wprowadzenie.html, opis: „zacznij tutaj — czym jest Talent i do czego służy"), **Whitepaper** (whitepaper.html), **Reguła publikacyjna** (regula_publikacyjna.html), **TIP — proces zmian** (tip.html, patrz etap 4), **Repozytorium** (GitHub). Usuń z listy: wyścig kandydatów, test stulecia, kruche gospodarki, talent dwustronny, archiwum. NIE usuwaj samych stron HTML tych raportów — są linkowane z whitepapera; usuń tylko pozycje z listy na stronie głównej. Sekcja „Dla wnikliwych i niedowiarków" (specyfikacja + dla_agenta) zostaje bez zmian.

## Etap 4 — TIP jako strona HTML

Do słownika `DOCS` w builderze dodaj `TIP/README.md → tip.html`. W konwersji podmień linki względne `TIP-0001-...md` / `TIP-0002-...md` na linki do GitHuba (`https://github.com/kurek0010/globalny-wskaznik-wartosci/blob/main/TIP/...`) — najprościej: przed konwersją markdown zrób replace na treści tego jednego pliku. Tytuł strony: „TIP — Talent Improvement Proposals".

## Etap 5 — weryfikacja

1. `python src/build_strona.py` bez błędów; `index.html` == `talent_strona.html`.
2. Otwórz index.html: hak pokazuje ~67%, kafle klikalne przełączają wykres, zakładki i okresy działają, sekcja płacowa zniknęła, lista „Przeczytaj więcej" ma 5 pozycji, tip.html istnieje i linkuje poprawnie.
3. Sprawdź responsywność (zwęź okno: kafle nad wykresem, nic nie wystaje).
4. Commit z opisem zmian + push.

## Wymogi twarde

- Wszystko przez szablon i builder (CLAUDE.md) — zero ręcznych edycji generowanych plików.
- Żadnych nowych zależności ani frameworków; zostajemy przy Chart.js z cdnjs i czystym JS.
- Nie zmieniaj niczego w obliczeniach (`talent_update.py`, `fetch_gus.py`, workflow) — to zadanie czysto frontowe.
- Liczby na stronie wyłącznie z plików danych, nigdy wpisane na sztywno w szablonie.
