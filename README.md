# Talent (TLN) — jednostka wartości minimalnego żalu

**Talent** to otwarta, deterministyczna jednostka rozliczeniowa do umów wieloletnich: pożyczasz 1000 TLN — oddajesz 1000 TLN, a obie strony odzyskują w przybliżeniu tę samą wartość. Formuła: **środek geometryczny indeksu cen i indeksu płac**, √(C×W). Matematycznie minimalizuje największą możliwą krzywdę którejkolwiek strony (kryterium minimax regret); empirycznie: najgorszy przypadek 6,1% przez sto lat danych USA (1929–2025) i 10,4% przez polską transformację ustrojową (1989–2024) — wobec setek procent dla pożyczek nominalnych.

Zasada projektu: **kod jest metodologią**. Wszystkie wartości są odtwarzalne z publicznych danych, publikowane z wyprzedzeniem i nigdy nie rewidowane wstecz.

## Zacznij tutaj

| Dokument | Co zawiera |
|---|---|
| [ARTYKUL_Talent_popularnonaukowy.md](ARTYKUL_Talent_popularnonaukowy.md) | **Whitepaper** — pełny wywód: problem, wzór z dowodem dla licealisty, testy, granice metody |
| [REGULA_publikacyjna_Talent_v0.1.md](REGULA_publikacyjna_Talent_v0.1.md) | Specyfikacja techniczna: definicje nóg, kalendarz publikacji, bezpieczniki |
| [TIP/](TIP/) | Talent Improvement Proposals — jawny proces zmian formuły (wzorzec BIP/EIP) |
| [talent_strona.html](talent_strona.html) | Strona z wartością bieżącą i wykresami (statyczna, działa z GitHub Pages) |

## Dowody empiryczne

- [WYSCIG_kandydatow_minimalny_zal.md](WYSCIG_kandydatow_minimalny_zal.md) — porównanie kandydatów na jednostkę (CPI, złoto, surowce, płace, mieszanki), 1996–2025
- [WYNIKI_test_stulecia_USA.md](WYNIKI_test_stulecia_USA.md) — USA 1929–2025: Wielki Kryzys, wojna, stagflacja, 2022
- [WYNIKI_kruche_gospodarki.md](WYNIKI_kruche_gospodarki.md) — Polska 1989–2024, Niemcy 1923, Argentyna (granice metody)
- [WYNIKI_talent_dwustronny.md](WYNIKI_talent_dwustronny.md) — jednostka umów międzynarodowych (PL-US)
- [ZRODLA_backtest_historyczny.md](ZRODLA_backtest_historyczny.md) — źródła danych do testów wstecznych

## Odtwórz obliczenia

```bash
cd prototyp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # wpisz własny (darmowy) klucz API FRED
python src/talent_daily.py  # kotwice miesięczne + ścieżka dzienna
python src/regret_century.py  # test stulecia USA
python src/build_strona.py  # przebudowa strony
```

Dane wejściowe są w `prototyp/data/` (surowe pobrania + przetworzone wyniki), więc skrypty analiz działają bez pobierania.

## Struktura repozytorium

```
├── ARTYKUL_Talent_popularnonaukowy.md   # whitepaper
├── REGULA_publikacyjna_Talent_v0.1.md   # specyfikacja
├── TIP/                                 # proces zmian
├── WYNIKI_*.md, WYSCIG_*.md             # raporty z testów
├── talent_strona.html                   # strona publiczna
├── prototyp/
│   ├── src/                             # aktywny kod (talent_daily, regret_*, backtest_1900)
│   ├── src/archiwum_auv/                # kod wcześniejszych iteracji (AUV)
│   └── data/                            # dane surowe i przetworzone
└── archiwum/                            # droga do Talenta: iteracje AUV, recenzje, plany
```

## Historia projektu

Talent wyrósł z projektu **AUV (Absolute Unit of Value)** — próby zbudowania „absolutnej" miary wartości na koszyku surowców. Krytyczna ocena ekonomiczna i testy wykazały, że taka jednostka nie istnieje, a droga prób, błędów i wniosków — udokumentowana w [archiwum/](archiwum/) — doprowadziła do obecnej, węższej i mocniejszej konstrukcji. Zgodnie z filozofią projektu nie ukrywamy tej historii: błędy są częścią dowodu.

## Status

Prototyp badawczy. Znane prowizoria wymienione są jawnie w regule publikacyjnej (§7) i w artykule (§7 i §9). Dane płacowe GUS/ZUS dla Polski wymagają weryfikacji u źródła przed publikacją produkcyjną.
