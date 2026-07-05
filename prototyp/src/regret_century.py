"""Test stulecia: jednostka minimalnego regretu na danych USA 1929-2025.

Jednostka JW(t) = sqrt(CPI(t) * Dochod(t)) - srodek geometryczny kosztow zycia
i dochodu. Metryka: regret dwustronny pozyczki "oddajesz tyle samo jednostek":
  - regret dluznika  = wzrost splaty wzgledem dochodu (benchmark dochodowy),
  - regret wierzyciela = utrata sily nabywczej splaty (benchmark CPI).
Regret okna = max z obu. Liczymy po wszystkich oknach i horyzontach.

Dane: FRED CPIAUCNS (srednie roczne), A939RC0A052NBEA (PKB/os. nominalnie),
CES3000000008 (placa godz. przemysl, srednie roczne). Pobrane 2026-07-04.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT = Path(__file__).resolve().parents[1] / "data" / "processed"

HORIZONS = [3, 5, 10, 20, 30]
ZERO = 0.02  # prog "zero regretu": 2%


def load(name: str) -> dict[int, float]:
    with open(RAW / name) as f:
        return {int(r["year"]): float(r["value"]) for r in csv.DictReader(f)}


def race(candidates: dict[str, dict[int, float]], bench_inc: dict[int, float],
         bench_cpi: dict[int, float], years: range) -> list[dict]:
    rows = []
    for name, I in candidates.items():
        regs, zero, n = [], 0, 0
        worst = (0.0, None, None, "")
        for h in HORIZONS:
            for t in years:
                if t + h > years[-1]:
                    continue
                R = math.log(I[t + h] / I[t])
                b = R - math.log(bench_inc[t + h] / bench_inc[t])
                l = R - math.log(bench_cpi[t + h] / bench_cpi[t])
                reg = max(max(b, 0.0), max(-l, 0.0))
                n += 1
                zero += reg < ZERO
                regs.append(reg)
                if reg > worst[0]:
                    worst = (reg, t, t + h,
                             "dluznik" if b >= -l else "wierzyciel")
        regs.sort()
        pct = lambda x: (math.exp(x) - 1) * 100
        rows.append({
            "kandydat": name,
            "pct_okien_zero": round(zero / n * 100),
            "mediana_pct": round(pct(regs[len(regs) // 2]), 1),
            "p95_pct": round(pct(regs[int(len(regs) * 0.95)]), 1),
            "najgorszy_pct": round(pct(worst[0]), 1),
            "najgorszy_kto": f"{worst[3]} {worst[1]}->{worst[2]}",
        })
    return rows


def main() -> None:
    cpi = load("fred_CPIAUCNS_annual_1913_2025.csv")
    gdp = load("fred_A939RC0A052NBEA_1929_2025.csv")
    wage = load("fred_CES3000000008_annual_1939_2025.csv")

    def norm(s, y0):
        return {y: v / s[y0] * 100 for y, v in s.items() if y >= y0}

    def geo(a, b, wa=0.5):
        return {y: math.exp(wa * math.log(a[y]) + (1 - wa) * math.log(b[y]))
                for y in a if y in b}

    # --- Bieg 1: 1929-2025, dochod = PKB/os. (Wielki Kryzys w probie) ---
    c, g = norm(cpi, 1929), norm(gdp, 1929)
    jw = geo(c, g)
    cands = {"nominal": {y: 100.0 for y in c}, "CPI": c, "dochod (PKB/os.)": g,
             "JW = sqrt(CPI*dochod)": jw}
    r1 = race(cands, g, c, range(1929, 2026))

    # --- Bieg 2: 1939-2025, benchmark dluznika = PLACA (realizm KKOP) ---
    c2, g2, w2 = norm(cpi, 1939), norm(gdp, 1939), norm(wage, 1939)
    jw_g, jw_w = geo(c2, g2), geo(c2, w2)
    cands2 = {"nominal": {y: 100.0 for y in c2}, "CPI": c2, "placa": w2,
              "PKB/os.": g2, "JW(CPI,PKB/os.)": jw_g, "JW(CPI,placa)": jw_w}
    r2 = race(cands2, w2, c2, range(1939, 2026))

    for tag, rows in [("1929-2025 (benchmark: PKB/os.)", r1),
                      ("1939-2025 (benchmark: placa)", r2)]:
        print("\n===", tag, "===")
        print(f"{'kandydat':24} | {'%zero':>5} | {'med':>6} | {'p95':>6} | "
              f"{'max':>6} | kto/kiedy")
        for r in rows:
            print(f"{r['kandydat']:24} | {r['pct_okien_zero']:4}% | "
                  f"{r['mediana_pct']:5}% | {r['p95_pct']:5}% | "
                  f"{r['najgorszy_pct']:5}% | {r['najgorszy_kto']}")

    with open(OUT / "regret_century.csv", "w", newline="") as f:
        wcsv = csv.DictWriter(f, fieldnames=list(r1[0]) + ["bieg"])
        wcsv.writeheader()
        for r in r1:
            wcsv.writerow(r | {"bieg": "1929_gdp"})
        for r in r2:
            wcsv.writerow(r | {"bieg": "1939_wage"})

    # --- Korytarz CPI-dochod: najwieksze rozjazdy (epizody) ---
    print("\n=== Szerokosc korytarza CPI vs dochod (okna 10-letnie) ===")
    eps = []
    for t in range(1929, 2016):
        d = abs(math.log(g[t + 10] / g[t]) - math.log(c[t + 10] / c[t]))
        eps.append((d, t))
    eps.sort(reverse=True)
    for d, t in eps[:5]:
        print(f"{t}->{t+10}: rozjazd {round((math.exp(d)-1)*100)}% "
              f"(CPI {round((c[t+10]/c[t]-1)*100)}%, "
              f"dochod {round((g[t+10]/g[t]-1)*100)}%)")

    # --- Zachowanie jednostki w stuleciu ---
    print("\n=== JW przez stulecie (1929=100) ===")
    for y in [1929, 1933, 1945, 1970, 1980, 2000, 2025]:
        print(f"{y}: CPI={round(c[y])}, dochod={round(g[y])}, JW={round(jw[y])}")


if __name__ == "__main__":
    main()
