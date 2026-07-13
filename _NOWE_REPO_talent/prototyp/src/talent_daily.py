"""Talent (TLN) - dzienna jednostka wartosci. Prototyp liczacy wg reguly
publikacyjnej v0.1 (patrz REGULA_publikacyjna_Talent_v0.1.md).

Formula:
  noga cen  I_c(m): indeks CPI PL (docelowo mediana zrodel), lancuch m/m
  noga plac I_w(m): indeks przecietnego wynagrodzenia, srednia kroczaca 12m
                    (usuwa sezonowosc premii/13. pensji)
  kotwica   A(m)  = sqrt(I_c(m) * I_w(m)), baza: pierwszy miesiac = 100
  dziennie  T(d)  = A(m) * g^(k/K)   dla d w oknie po publikacji kotwicy,
            gdzie g = A(m)/A(m-1), k = nr dnia w oknie, K = dlugosc okna.
  Kazda wartosc dzienna jest znana z wyprzedzeniem (pre-commitment jak UF).

Prototyp: CPI PL miesieczny z monthly.parquet; place - roczne GUS/ZUS
(tabela z regret_poland.py) interpolowane log-liniowo do miesiecy.
PROWIZORIUM do czasu adaptera GUS BDL (placa miesieczna sektora
przedsiebiorstw). Zadnych rewizji wstecz: raz policzona kotwica jest stala.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

from regret_poland import CPI as _CPI_ANNUAL_UNUSED  # noqa: F401 (dok.)
from regret_poland import W_BRUTTO, W_NETTO, CHAIN_1999, build_wage

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

WAGE_SMOOTH_MONTHS = 12
CAP_MONTHLY = 0.15  # bezpiecznik: |wzrost kotwicy m/m| > 15% -> tryb awaryjny


def monthly_cpi() -> pd.Series:
    m = pd.read_parquet(ROOT / "data" / "processed" / "monthly.parquet")
    s = m["CPI_PL"].dropna()
    s.index = s.index.to_period("M")
    return s


def monthly_wage(index: pd.PeriodIndex) -> pd.Series:
    """Roczne srednie place -> log-liniowa interpolacja miesieczna.

    Prowizorium: docelowo miesieczna placa GUS (sektor przedsiebiorstw),
    lancuchowana z placa w gospodarce narodowej (kwartalna).
    """
    annual = build_wage()
    pts = {pd.Period(f"{y}-07", "M"): math.log(v) for y, v in annual.items()}
    s = pd.Series(pts).reindex(
        pd.period_range(min(pts), max(pts), freq="M")
    ).interpolate()
    return s.reindex(index).ffill().bfill().pipe(lambda x: x.apply(math.exp))


def anchors() -> pd.DataFrame:
    cpi = monthly_cpi()
    wage = monthly_wage(cpi.index)
    i_c = cpi / cpi.iloc[0] * 100.0
    i_w = wage / wage.iloc[0] * 100.0
    i_w = i_w.rolling(WAGE_SMOOTH_MONTHS, min_periods=1).mean()
    a = (i_c * i_w) ** 0.5
    a = a / a.iloc[0] * 100.0
    g = a / a.shift(1)
    alarm = (g - 1).abs() > CAP_MONTHLY
    return pd.DataFrame({"I_c": i_c, "I_w": i_w, "A": a, "g": g,
                         "tryb_awaryjny": alarm})


def daily_path(a: pd.DataFrame, months: int = 13) -> pd.DataFrame:
    """Sciezka dzienna dla ostatnich `months` kotwic (demonstracja)."""
    rows = []
    tail = a.dropna(subset=["g"]).iloc[-months:]
    for per, row in tail.iterrows():
        start = per.to_timestamp() + pd.offsets.MonthBegin(1)  # okno: m+1
        days = pd.date_range(start, start + pd.offsets.MonthEnd(0), freq="D")
        K = len(days)
        for k, d in enumerate(days, 1):
            rows.append({"data": d.date(), "TLN": row["A"] * row["g"] ** (k / K)})
    return pd.DataFrame(rows)


def main() -> None:
    a = anchors()
    a.to_csv(OUT / "talent_anchors.csv")
    d = daily_path(a)
    d.to_csv(OUT / "talent_daily.csv", index=False)

    last = a.dropna(subset=["g"]).iloc[-1]
    per = a.dropna(subset=["g"]).index[-1]
    print(f"Kotwica {per}: A={last['A']:.3f}  (I_c={last['I_c']:.1f}, "
          f"I_w={last['I_w']:.1f}, g={last['g']:.5f})")
    print(f"Dzisiejsza wartosc TLN (sciezka pre-commitment): "
          f"{d.iloc[-1]['TLN']:.3f}  ({d.iloc[-1]['data']})")
    print(f"Trybow awaryjnych w historii: {int(a['tryb_awaryjny'].sum())}")

    # eksport kotwic do strony www (JSON: okres -> wartosc)
    export = {str(p): round(v, 3) for p, v in a["A"].dropna().items()}
    (OUT / "talent_anchors.json").write_text(json.dumps(export))
    print(f"Zapisano: talent_anchors.csv, talent_daily.csv, "
          f"talent_anchors.json ({len(export)} kotwic)")


if __name__ == "__main__":
    main()
