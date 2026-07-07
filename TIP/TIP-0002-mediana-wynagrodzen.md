# TIP-0002: Noga płacowa — mediana wynagrodzeń z rejestrów administracyjnych (ZUS+MF)

**Autor:** Mariusz Kurowski · **Data:** 2026-07-07 · **Status:** Szkic

## Problem

Obecna noga płacowa (TIP-0001: fundusz płac sektora przedsiębiorstw / wygładzone zatrudnienie) dziedziczy dwie słabości źródła: (1) pomija firmy <9 pracowników i umowy cywilnoprawne; (2) opiera się na **średniej**, którą zawyża górny ogon rozkładu — średnia rośnie systematycznie szybciej niż płaca typowego pracownika, więc Talent na średniej lekko sprzyja wierzycielowi względem „typowego żalu".

## Proponowana zmiana

Drugie (docelowo główne) źródło nogi płacowej: **mediana wynagrodzeń brutto z badania GUS „Rozkład wynagrodzeń w gospodarce narodowej"** — miesięcznego, opartego na rejestrach administracyjnych ZUS i MF (nie na ankietach), z szeregiem od stycznia 2010. Dane rejestrowe obejmują całą gospodarkę narodową i są z natury odporne na manipulację ankietową (powstają jako produkt uboczny płacenia składek). Publikacja z opóźnieniem ~2 miesięcy — zgodna z kaskadą awaryjną §4 polityki danych (carry-forward jednej dynamiki).

## Test wymagany przed akceptacją (do wykonania)

1. Pobrać pełny szereg mediany (I 2010 → dziś) i porównać z obecną nogą: dynamiki roczne, rozjazd skumulowany, zachowanie w epizodach 2020 i 2022–23.
2. Sprawdzić stabilność publikacji: częstotliwość rewizji, opóźnienie faktyczne vs deklarowane, zmiany metodologiczne serii.
3. Przeliczyć test polski (regret 1989–2024 nie obejmie mediany — szereg od 2010; test na oknach 2010–2025) w wariantach: średnia, mediana, mediana z korektą składu.
4. Kryterium akceptacji: mediana nie pogarsza żadnej statystyki żalu, a zmniejsza systematyczny dryf na korzyść wierzyciela.

## Uwagi

- Efekt składu (TIP-0001) dotyczy mediany słabiej niż średniej, ale nie zerowo — do zbadania w teście 1, czy korekta MA12 zatrudnienia pozostaje potrzebna.
- Do czasu akceptacji mediana pełni rolę **drugiego źródła** w tripwire nogi płacowej (rozjazd dynamik > 3 p.p. → alert).
- Źródła: [GUS — Rozkład wynagrodzeń w gospodarce narodowej](https://stat.gov.pl/obszary-tematyczne/rynek-pracy/pracujacy-zatrudnieni-wynagrodzenia-koszty-pracy/) (komunikaty miesięczne); zapowiedź zmiany częstotliwości: [Bankier.pl](https://bankier.pl/amp/wiadomosc/Mediana-wynagrodzen-bedzie-publikowana-co-miesiac-Rewolucja-w-statystykach-GUS-8714108); przykład odczytu: [prawo.pl — mediana X 2025 = 7414 zł](https://www.prawo.pl/kadry/mediana-wynagrodzen-pazdziernik-2025-r-gus,1542164.html).
