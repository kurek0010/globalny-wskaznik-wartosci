"""Talent umowy dwustronnej PL-US: test zalu obu stron, 2002-2024.

Problem: umowa miedzy strona polska (zyje w PLN, placach i cenach PL)
a amerykanska (USD, place i ceny US). Kandydaci na jednostke umowy:
  - PLN nominal / USD nominal (dzisiejsza praktyka),
  - TLN-PL, TLN-US (Talent jednego kraju - druga strona bierze cale ryzyko),
  - TLN-2 (dwustronny): srodek geometryczny obu Talentow po przeliczeniu
    kursem; ryzyko realnego kursu dzielone po polowie w logarytmach:
      V_PLN(t) = sqrt( TLN_PL(t) * TLN_US(t) * S(t)/S(0) ),  S = PLN/USD
      V_USD(t) = V_PLN(t) / (S(t)/S(0))
               = sqrt( TLN_US(t) * TLN_PL(t) / (S(t)/S(0)) )   (symetria)

Zal (regret) okna: jednostka oceniana w OBU krajach naraz -
w PLN wzgledem korytarza [CPI_PL, placa_PL], w USD wzgledem [CPI_US, placa_US];
zal = najwieksze przekroczenie ktoregokolwiek z 4 brzegow (dowolny kierunek
umowy: kazda strona moze byc dluznikiem lub wierzycielem).

Dane roczne: CPI PL (FRED/OECD), place PL (GUS/ZUS via regret_poland),
CPI US i place US (FRED, via pliki raw), kurs PLN/USD (NBP, srednia roczna).
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import pandas as pd

from regret_poland import CPI as CPI_PL
from regret_poland import build_wage

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

HORIZONS = [3, 5, 10, 20]
ZERO = 0.02


def load_fred(name: str) -> dict[int, float]:
    with open(RAW / name) as f:
        return {int(r["year"]): float(r["value"]) for r in csv.DictReader(f)}


def pln_usd_annual() -> dict[int, float]:
    d = pd.read_csv(RAW / "nbp_USD_1996-01-01_2025-12-31.csv",
                    parse_dates=["date"])
    return d.groupby(d["date"].dt.year)["value"].mean().to_dict()


def main() -> None:
    cpi_us = load_fred("fred_CPIAUCNS_annual_1913_2025.csv")
    wage_us = load_fred("fred_CES3000000008_annual_1939_2025.csv")
    wage_pl = build_wage()
    fx = pln_usd_annual()

    Y0, Y1 = 2002, 2024
    years = range(Y0, Y1 + 1)
    nrm = lambda s: {y: s[y] / s[Y0] for y in years}
    c_pl, w_pl = nrm(CPI_PL), nrm(wage_pl)
    c_us, w_us = nrm(cpi_us), nrm(wage_us)
    s = nrm(fx)  # PLN za USD, wzgledem roku bazowego

    tln_pl = {y: math.sqrt(c_pl[y] * w_pl[y]) for y in years}
    tln_us = {y: math.sqrt(c_us[y] * w_us[y]) for y in years}
    tln2_pln = {y: math.sqrt(tln_pl[y] * tln_us[y] * s[y]) for y in years}

    # kandydaci: wartosc jednostki W PLN (wartosc w USD = /s)
    cands = {
        "PLN nominal": {y: 1.0 for y in years},
        "USD nominal": s,
        "TLN-PL": tln_pl,
        "TLN-US (w PLN)": {y: tln_us[y] * s[y] for y in years},
        "TLN-2 dwustronny": tln2_pln,
        "50/50 PLN+USD nominal": {y: math.sqrt(s[y]) for y in years},
    }

    pct = lambda x: (math.exp(x) - 1) * 100
    print(f"{'jednostka umowy':22} | {'%zero':>5} | {'med':>6} | {'p95':>6} | "
          f"{'max':>6} | najgorszy przypadek")
    for name, V in cands.items():
        regs, zero, n, worst = [], 0, 0, (0.0, "", 0, 0)
        for h in HORIZONS:
            for t in years:
                if t + h > Y1:
                    continue
                v_pln = math.log(V[t + h] / V[t])
                v_usd = v_pln - math.log(s[t + h] / s[t])
                edges = {
                    "dluznik PL": v_pln - math.log(w_pl[t + h] / w_pl[t]),
                    "wierzyciel PL": -(v_pln - math.log(c_pl[t + h] / c_pl[t])),
                    "dluznik US": v_usd - math.log(w_us[t + h] / w_us[t]),
                    "wierzyciel US": -(v_usd - math.log(c_us[t + h] / c_us[t])),
                }
                side, reg = max(edges.items(), key=lambda kv: kv[1])
                reg = max(reg, 0.0)
                n += 1
                zero += reg < ZERO
                regs.append(reg)
                if reg > worst[0]:
                    worst = (reg, side, t, t + h)
        regs.sort()
        print(f"{name:22} | {zero/n*100:4.0f}% | {pct(regs[n//2]):5.1f}% | "
              f"{pct(regs[int(n*.95)]):5.1f}% | {pct(worst[0]):5.1f}% | "
              f"{worst[1]} {worst[2]}->{worst[3]}")

    # ilustracja: rozjazd realny PL vs US w probie
    print(f"\nKontekst 2002->2024: place PL x{w_pl[2024]:.2f}, "
          f"place US x{w_us[2024]:.2f}, CPI PL x{c_pl[2024]:.2f}, "
          f"CPI US x{c_us[2024]:.2f}, kurs PLN/USD x{s[2024]:.2f}")
    print(f"TLN-PL x{tln_pl[2024]:.2f}, TLN-US x{tln_us[2024]:.2f}, "
          f"TLN-2 (w PLN) x{tln2_pln[2024]:.2f}")


if __name__ == "__main__":
    main()
