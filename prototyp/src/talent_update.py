"""Miesieczna aktualizacja kotwic TLN-PLN wg REGULA + POLITYKA_danych.

PIERWSZA PUBLIKACJA: 2026-07-08. Wartosci sprzed tej daty byly robocze
(prototyp; ogon 2025 zawieral artefakt ffill) i zostaly jednorazowo
przeliczone z danych first-print GUS. OD TEJ PUBLIKACJI obowiazuje zakaz
rewizji wstecz: kolejne uruchomienia moga TYLKO dopisywac nowe miesiace
(skrypt odmowi nadpisania istniejacych wartosci).

Zrodla first-print (do rozszerzania przy kazdej aktualizacji):
- CPI m/m: GUS, tabela "Miesieczne wskazniki cen towarow i uslug
  konsumpcyjnych od 1982 roku" (odczyt 2026-07-08)
- place roczne (gospodarka narodowa): komunikaty Prezesa GUS
  (2025: 8903,56 zl, komunikat z 2026-02-09, M.P. 2026 poz. 192)
- ALERT: punkt plac 2026 = proxy (8903,56 x 1,058 wg dynamiki r/r sektora
  przedsiebiorstw, V 2026, GUS) - zastapic komunikatem GN za 2026 w II 2027.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

# --- dane first-print (GUS) ------------------------------------------------
CPI_MM = {  # dynamika m/m, poprzedni miesiac = 100
    "2025-04": 100.4, "2025-05": 99.8, "2025-06": 100.1, "2025-07": 100.3,
    "2025-08": 100.0, "2025-09": 100.0, "2025-10": 100.1, "2025-11": 100.1,
    "2025-12": 100.0,
    "2026-01": 100.7, "2026-02": 100.3, "2026-03": 101.1, "2026-04": 100.6,
}
WAGE_ANNUAL = {  # przecietne wynagrodzenie GN, zl/mies. (punkt = lipiec roku)
    2024: 8181.72,           # komunikat GUS II 2025
    2025: 8903.56,           # komunikat GUS 2026-02-09 (first print)
    2026: 8903.56 * 1.058,   # PROXY (alert) - dynamika sektora przeds. V 2026
}
FIRST_PUBLICATION = "2025-04"  # od tego miesiaca ta sciezka jest kanoniczna


def main() -> None:
    a = pd.read_csv(OUT / "talent_anchors.csv", index_col=0)
    a.index = pd.PeriodIndex(a.index, freq="M")

    # znajdz poczatek przeliczenia: FIRST_PUBLICATION
    start = pd.Period(FIRST_PUBLICATION, "M")
    if str(start) not in CPI_MM:
        raise SystemExit("Brak danych CPI dla miesiaca startowego")

    # zakaz rewizji: jesli kotwica za miesiac z CPI_MM juz opublikowana
    # w poprzednim uruchomieniu (plik talent_published.json), nie ruszaj
    pub_file = OUT / "talent_published.json"
    published = set(json.load(open(pub_file))) if pub_file.exists() else set()
    do_months = [m for m in CPI_MM if m not in published]
    if not do_months:
        print("Brak nowych miesiecy do publikacji.")
        return

    # noga plac: interpolacja log-liniowa punktow lipcowych, baza = I_w(2024-07)
    base_p = pd.Period("2024-07", "M")
    base_iw = float(a.loc[base_p, "I_w"])
    pts = {pd.Period(f"{y}-07", "M"): math.log(v) for y, v in WAGE_ANNUAL.items()}
    rng = pd.period_range(min(pts), max(pts), freq="M")
    wage = pd.Series(pts).reindex(rng).interpolate().apply(math.exp)
    wage = wage / wage[base_p]  # wzgledem bazy

    last = start - 1
    ic, iw = float(a.loc[last, "I_c"]), float(a.loc[last, "I_w"])
    rows = []
    for m in sorted(pd.Period(x, "M") for x in do_months):
        ic *= CPI_MM[str(m)] / 100.0
        iw = base_iw * float(wage[m]) if m in wage.index else iw  # carry-fwd
        A = math.sqrt(ic * iw)
        g = A / (rows[-1][3] if rows else float(a.loc[m - 1, "A"]))
        rows.append((m, ic, iw, A, g))
        a.loc[m] = {"I_c": round(ic, 3), "I_w": round(iw, 3),
                    "A": round(A, 3), "g": round(g, 5),
                    "tryb_awaryjny": abs(g - 1) > 0.15}

    a = a.sort_index()
    a.to_csv(OUT / "talent_anchors.csv")
    json.dump({str(p): round(v, 3) for p, v in a["A"].items()},
              open(OUT / "talent_anchors.json", "w"))
    json.dump(sorted(published | set(CPI_MM)), open(pub_file, "w"), indent=1)

    lastm, _, _, lastA, lastg = rows[-1]
    print(f"Opublikowano {len(rows)} kotwic: {rows[0][0]} .. {lastm}")
    print(f"Kotwica {lastm}: A = {lastA:.3f} (m/m {100*(lastg-1):+.2f}%)")
    print("ALERT: punkt plac 2026 = proxy z dynamiki sektora przeds. "
          "(+5,8% r/r) - do zastapienia komunikatem GN w II 2027.")
    print("Nastepnie uruchom: python src/build_strona.py")


if __name__ == "__main__":
    main()
