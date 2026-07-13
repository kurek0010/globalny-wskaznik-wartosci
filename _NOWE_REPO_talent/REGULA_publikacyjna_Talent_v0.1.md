# Reguła publikacyjna Talenta (TLN) — v0.1

**Data:** 2026-07-04 · **Status:** projekt do dyskusji · **Kod referencyjny:** `prototyp/src/talent_daily.py`
Zasada nadrzędna: **kod jest metodologią**. Ten dokument opisuje regułę słowami; w razie rozbieżności wiąże wersjonowany kod z podpisanym tagiem. Operacyjne szczegóły zasilania danymi (konkretne komunikaty, dni publikacji, kaskady awaryjne, rewizje, zmiany bazy): `POLITYKA_danych_v0.1.md`.

## 1. Definicja jednostki

Talent to jednostka wartości będąca środkiem geometrycznym kosztów życia i płac:

$$A(m) = 100 \cdot \sqrt{\frac{I_c(m)}{I_c(m_0)} \cdot \frac{I_w(m)}{I_w(m_0)}}$$

- **I_c — noga cen:** indeks cen konsumpcyjnych, łańcuch miesięczny. Docelowo **mediana ≥3 niezależnych źródeł** (GUS CPI, HICP Eurostat, niezależny indeks cen online); do czasu trzeciego źródła: średnia geometryczna GUS i HICP z tripwire (§5.3).
- **I_w — noga płac (definicja v0.2):** indeks **funduszu płac na wygładzone zatrudnienie**: `W(m) = FunduszPłac(m) / MA12(Zatrudnienie)(m)` (średnia krocząca 12-mies., przyczynowa), następnie wygładzenie 12-mies. całego indeksu (sezonowość premii). Oba składniki pochodzą z tych samych sprawozdań firm do GUS. Uzasadnienie: przeciętna płaca (fundusz/bieżące zatrudnienie) ma procykliczny artefakt składu — w kryzysie zwalniani są najpierw nisko opłacani i średnia *rośnie*, gdy dochody spadają (USA, IV 2020: przeciętna +4,2% m/m, fundusz/MA12 −8,9%; dryf długookresowy obu wariantów identyczny: +135,7% vs +136,2% za 2000–2026). Weryfikacja: `src/wage_leg_v2 — data/processed/wage_leg_v2_monthly.csv`. Źródła: sektor przedsiębiorstw (GUS, miesięczny) łańcuchowany gospodarką narodową (GUS, kwartalny); docelowo mediana wzrostu płac tych samych osób z danych ZUS jako drugie źródło.
- **m₀ — baza:** pierwszy miesiąc publikacji = 100. Baza jest stała na zawsze; nigdy nie jest przesuwana.

Uzasadnienie empiryczne wag 50/50 i wyboru nóg: `WYSCIG_kandydatow_minimalny_zal.md`, `WYNIKI_test_stulecia_USA.md`, `WYNIKI_kruche_gospodarki.md` (minimalizacja dwustronnego regretu/żalu).

## 2. Kalendarz i wartość dzienna (model UF — pełny pre-commitment)

1. GUS publikuje CPI za miesiąc *m* ok. 15. dnia *m+1*; płace przedsiębiorstw ok. 21. dnia *m+1*.
2. **Dzień kotwicy: 25. dzień miesiąca *m+1*.** Liczymy A(m) z danych opublikowanych do tego dnia i **jednocześnie publikujemy pełną ścieżkę dzienną** na okno od 26. dnia *m+1* do 25. dnia *m+2*:

$$T(d_k) = A(m) \cdot g^{k/K} \qquad g = \frac{A(m)}{A(m-1)} \qquad k = 1, \dots, K$$

(K to liczba dni okna publikacyjnego.)

3. Każda wartość dzienna jest więc znana **co najmniej dzień naprzód, a maksymalnie miesiąc naprzód** — strony umowy nigdy nie rozliczają się po wartości, której nie mogły znać wcześniej (wzór: chilijska UF).

## 3. Zakaz rewizji wstecz

Raz opublikowana wartość (kotwica lub dzienna) **nigdy nie jest zmieniana**. Rewizje danych źródłowych (GUS/Eurostat) wpływają wyłącznie na przyszłe łańcuchy m/m. Publikacja każdego odczytu zawiera **hash danych wejściowych** i wersję kodu (tag git), więc każdy może odtworzyć wynik co do grosza.

## 4. Rewizje składu i źródeł (chain-linking)

Zmiana źródła/składnika wyłącznie wg procedury niezmienniczości (chain-linking): kryteria kwalifikacji zapisane z góry, ogłoszenie ≥3 miesiące naprzód, łączenie łańcuchowe (bez skoku), test nakładania, nigdy wstecz. Konsensus społeczności (model open source) decyduje **czy kryteria zastosowano poprawnie** — nigdy o pożądanym wyniku.

## 5. Bezpieczniki (deterministyczne, ogłoszone z góry)

1. **Próg podwyższonej inflacji:** jeśli 3-miesięczna średnia |wzrostu kotwicy m/m| > 5%, okno interpolacji skraca się (publikacja dekadowa: 5., 15., 25.) — redukcja strat lagu (lekcja: Polska I 1990, −44% przy lagu miesięcznym).
2. **Próg Cagana (tryb awaryjny):** inflacja > 50% m/m przez 2 kolejne miesiące → jednostka przechodzi na z góry zadeklarowany twardy koszyk (mediana kursów 3 stabilnych walut), aż inflacja < 15% m/m przez 6 miesięcy; powrót przez chain-linking (lekcja: Niemcy 1923 — powyżej tego progu żaden indeks nie działa i nie wolno udawać, że jest inaczej).
3. **Tripwire źródeł:** rozjazd rocznych dynamik źródeł jednej nogi > 3 p.p. → automatyczne przejście na medianę pozostałych + publiczny alert (lekcja: INDEC 2007–15).
4. **Cap kontraktowy (zalecenie do umów, nie do indeksu):** wzrost zobowiązania m/m ponad X% podlega odroczeniu z kapitalizacją, nie umorzeniu (lekcja: zamrożenie UVA dekretem).

## 6. Publikacja i licencja

- Kanały: repozytorium git (dane + kod + podpisane tagi), plik JSON/CSV z kotwicami i ścieżką dzienną, strona statyczna (`talent_strona.html` — działa z GitHub Pages, bez serwera).
- Licencja: kod i dane wynikowe otwarte (np. MIT + CC-BY); warunek użycia nazwy „Talent/TLN": niemodyfikowana formuła (ochrona przed podszywaniem).
- Częstotliwość: kotwica miesięcznie, ścieżka dzienna z wyprzedzeniem, alerty bezpieczników natychmiast.

## 7. Znane prowizoria v0.1 (jawna lista)

1. Noga płac w prototypie: dane roczne GUS/ZUS interpolowane — do zastąpienia adapterem GUS BDL (płaca miesięczna sektora przedsiębiorstw).
2. Noga cen: jedno źródło (CPI PL) — do rozszerzenia o HICP i indeks online.
3. Baza prototypu: 1996-01 = 100 (dla ciągłości badań); baza produkcyjna zostanie ustalona w dniu pierwszej publikacji.
4. Wariant Qist (finanse bezodsetkowe): identyczna formuła, odrębna dokumentacja zgodności (mithl/riba) — do opracowania z ekspertem fiqh.
