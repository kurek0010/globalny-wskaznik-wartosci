"""Krok (b): czy skład/jakość kolateralu przewiduje inflację PONAD M2?

Metoda (dane roczne, by uniknąć autokorelacji nakładających się YoY):
  1. Granger parami: X -> inflacja CPI (statsmodels), min p po lagach 1-2.
  2. Regresja przyrostowa z błędami Newey-West (HAC):
        baza:  CPI[t] ~ CPI[t-1] + M2_growth[t-1]
        +X:    dodaj kolateral[t-1]; raportuj ΔR²_adj i p-wartość X.
     Jeśli X istotne PONAD M2 -> kolateral wnosi informację. Jeśli nie ->
     dominuje sama ilość pieniądza.

Ostrzeżenie: próba mała (roczna, ~22-29 obs; bilans Fed od 2003).
Wyniki sugestywne, nie rozstrzygające.

Uruchamianie:  python -m src.money_quality_model
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import PROCESSED_DIR, FIGURES_DIR

warnings.filterwarnings("ignore")


def _annual(monthly: pd.DataFrame) -> pd.DataFrame:
    a = monthly.resample("YE").mean()
    a.index = a.index.year
    return a


def build(monthly: pd.DataFrame) -> pd.DataFrame:
    a = _annual(monthly)
    df = pd.DataFrame(index=a.index)
    df["CPI"] = a["CPI_USA"].pct_change() * 100
    df["M2"] = a["M2_USA"].pct_change() * 100
    df["mortgage_growth"] = a["mortgage_debt_total"].pct_change() * 100
    df["govdebt_growth"] = a["fed_treasuries"].pct_change() * 100
    bank = a[["bank_loans_business", "bank_loans_realestate", "bank_loans_consumer"]]
    bsum = bank.sum(axis=1)
    df["Q_banki"] = (1.0 * a["bank_loans_business"] + 0.7 * a["bank_loans_realestate"]
                     + 0.3 * a["bank_loans_consumer"]) / bsum
    df["mortgage_share"] = a["bank_loans_realestate"] / bsum
    return df


def granger_pairwise(df: pd.DataFrame, target="CPI", maxlag=2) -> dict:
    from statsmodels.tsa.stattools import grangercausalitytests
    res = {}
    for x in ["M2", "mortgage_growth", "govdebt_growth", "Q_banki", "mortgage_share"]:
        d = df[[target, x]].dropna()
        if len(d) < maxlag + 5:
            res[x] = np.nan; continue
        try:
            out = grangercausalitytests(d[[target, x]], maxlag=maxlag, verbose=False)
            pmin = min(out[l][0]["ssr_ftest"][1] for l in out)
            res[x] = pmin
        except Exception:
            res[x] = np.nan
    return res


def incremental(df: pd.DataFrame) -> pd.DataFrame:
    import statsmodels.api as sm
    rows = {}
    for x in ["mortgage_growth", "govdebt_growth", "Q_banki", "mortgage_share"]:
        d = pd.DataFrame({
            "CPI": df["CPI"],
            "CPI_l1": df["CPI"].shift(1),
            "M2_l1": df["M2"].shift(1),
            "X_l1": df[x].shift(1),
        }).dropna()
        if len(d) < 8:
            rows[x] = {"n": len(d), "dR2_adj": np.nan, "p_X (HAC)": np.nan}
            continue
        y = d["CPI"]
        base = sm.OLS(y, sm.add_constant(d[["CPI_l1", "M2_l1"]])).fit()
        full = sm.OLS(y, sm.add_constant(d[["CPI_l1", "M2_l1", "X_l1"]])).fit(
            cov_type="HAC", cov_kwds={"maxlags": 2})
        rows[x] = {
            "n": len(d),
            "dR2_adj": full.rsquared_adj - base.rsquared_adj,
            "p_X (HAC)": full.pvalues["X_l1"],
        }
    return pd.DataFrame(rows).T


def plot(granger: dict, inc: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    g = pd.Series(granger).dropna().sort_values()
    colors = ["#27ae60" if p < 0.05 else "#c0392b" for p in g.values]
    ax1.barh(g.index, g.values, color=colors, alpha=0.85)
    ax1.axvline(0.05, color="black", ls="--", lw=1, label="p = 0,05")
    ax1.set_title("Granger parami: X → inflacja CPI\n(zielony: istotne p<0,05)", fontweight="bold")
    ax1.set_xlabel("min p-wartość (lagi 1-2)"); ax1.legend(fontsize=8)

    inc2 = inc.dropna(subset=["p_X (HAC)"])
    colors2 = ["#27ae60" if p < 0.05 else "#c0392b" for p in inc2["p_X (HAC)"]]
    ax2.barh(inc2.index, inc2["dR2_adj"], color=colors2, alpha=0.85)
    for i, (n, r) in enumerate(zip(inc2.index, inc2["dR2_adj"])):
        ax2.text(r, i, f"  p={inc2['p_X (HAC)'][n]:.2f}", va="center", fontsize=8.5)
    ax2.axvline(0, color="black", lw=0.8)
    ax2.set_title("Przyrost R²_adj PONAD (CPI[t-1] + M2[t-1])\n(zielony: X istotne p<0,05)",
                  fontweight="bold")
    ax2.set_xlabel("ΔR²_adj po dodaniu kolateralu")

    fig.suptitle("Krok (b): czy kolateral przewiduje inflację ponad ilość pieniądza (M2)?",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    p = FIGURES_DIR / "41_kolateral_ponad_M2.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return p


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    df = build(monthly)
    g = granger_pairwise(df)
    inc = incremental(df)
    inc.round(3).to_csv(PROCESSED_DIR / "money_quality_model.csv")
    p = plot(g, inc)

    print("=== Granger parami (min p, lagi 1-2; p<0,05 = wyprzedza CPI) ===")
    for k, v in sorted(g.items(), key=lambda kv: (np.isnan(kv[1]), kv[1])):
        flag = "  <-- istotne" if (v == v and v < 0.05) else ""
        print(f"  {k:18} p = {v:.3f}{flag}")
    print("\n=== Przyrost ponad M2 (CPI[t-1]+M2[t-1] -> +kolateral) ===")
    print(inc.round(3).to_string())
    print("\nInterpretacja: dodatni ΔR²_adj i p_X<0,05 => kolateral wnosi PONAD M2.")
    print("wykres:", p.name)


if __name__ == "__main__":
    main()
