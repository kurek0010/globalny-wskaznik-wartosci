# TIP — Talent Improvement Proposals

Każda zmiana formuły, źródeł danych lub reguły publikacyjnej Talenta przechodzi przez TIP: ponumerowany dokument z uzasadnieniem, testem na danych i decyzją. Wzorzec: BIP (Bitcoin) / EIP (Ethereum).

## Proces (cztery kroki, zawsze w tej kolejności)

1. **Nazwij problem publicznie** — TIP powstaje jako szkic z opisem problemu i mechanizmu.
2. **Zaproponuj poprawkę** — konkretna zmiana definicji/kodu, bez nowych zależności, jeśli to możliwe.
3. **Przetestuj na danych, zanim cokolwiek zmienisz** — wyniki i kod testu są częścią TIP-a.
4. **Zmień regułę z pełnym uzasadnieniem, nigdy wstecz** — po akceptacji definicja wchodzi do reguły publikacyjnej z odnośnikiem do TIP-a; opublikowane wartości indeksu nie są nigdy przeliczane.

## Statusy

`Szkic` → `Testowany` → `Zaakceptowany` / `Odrzucony` → `Wdrożony`

Konsensus społeczności dotyczy wyłącznie tego, **czy kryteria i test zostały poprawnie zastosowane** — nigdy tego, jaki ma być wynik indeksu.

## Szablon

Nagłówek (numer, tytuł, autor, data, status) · Problem · Proponowana zmiana · Test na danych (kod + liczby) · Skutki uboczne i czego zmiana NIE psuje · Decyzja i data wdrożenia.

## Rejestr

| Nr | Tytuł | Status |
|---|---|---|
| [TIP-0001](TIP-0001-noga-placowa-v02.md) | Noga płacowa v0.2: fundusz płac / wygładzone zatrudnienie | Wdrożony |
| [TIP-0002](TIP-0002-mediana-wynagrodzen.md) | Noga płacowa: mediana wynagrodzeń z rejestrów ZUS+MF | Szkic |
