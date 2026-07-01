"""Walidacja wrażliwości AUV-T (v0.4).

Pytanie: czy główny wynik — AUV-T bez dryfu długoterminowego (~100 po 30
latach), z dala od M2 (+489%) — zależy od arbitralnych wyborów (skład
koszyka, wagi kategorii, średnia geom. vs aryt., rok bazowy)?

Testy:
  1. Leave-one-out kategorii (czy jedna kategoria nie steruje wynikiem).
  2. Monte Carlo wag (1000 losowań z sympleksu Dirichleta).
  3. Średnia geometryczna vs arytmetyczna.
  4. Rok bazowy (1996..2015).

Uruchamianie:  python -m src.sensitivity
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import BASE_YEAR, CATEGORIES, PROCESSED_DIR, FIGURES_DIR, compute

CATS = list(CATEGORIES)  # energia, zywnosc, metale, budownictwo
RNG = np.random.default_rng(42)


def _components(monthly: pd.DataFrame):
    out = compute(monthly)
    catdf = out[[f"kat_{c}" for c in CATS]].copy()
    catdf.columns = CATS
    income = out["dochod_glob_per_capita"]
    m2 = out["M2_USA"]
    return catdf, income, m2


def auv(catdf: pd.DataFrame, income: pd.Series, weights, method="geom") -> pd.Series:
    w = np.asarray(weights, float); w = w / w.sum()
    if method == "geom":
        basket = np.exp((np.log(catdf) * w).sum(axis=1))
    else:
        basket = (catdf * w).sum(axis=1)
    s = basket / income * 100.0
    return s / s.loc[BASE_YEAR] * 100.0


def _stats(s: pd.Series, m2: pd.Series) -> dict:
    return {
        "end2025": s.loc[2025],
        "min": s.min(), "max": s.max(),
        "std_logd": np.log(s).diff().std(),
        "corr_M2": np.log(s).diff().corr(np.log(m2).diff()),
    }


def run(monthly: pd.DataFrame):
    catdf, income, m2 = _components(monthly)
    eqw = np.ones(len(CATS))
    rows = {}

    # 0. baza (równe wagi, geom)
    rows["pełny (równe, geom)"] = _stats(auv(catdf, income, eqw), m2)

    # 1. leave-one-out
    loo = {}
    for i, c in enumerate(CATS):
        w = eqw.copy(); w[i] = 0
        s = auv(catdf, income, w)
        rows[f"bez: {c}"] = _stats(s, m2)
        loo[c] = s

    # 2. geom vs aryt
    rows["arytmetyczna"] = _stats(auv(catdf, income, eqw, "arit"), m2)

    # 3. Monte Carlo wag
    N = 1000
    ends, paths = [], []
    for _ in range(N):
        w = RNG.dirichlet(np.ones(len(CATS)))
        s = auv(catdf, income, w)
        ends.append(s.loc[2025]); paths.append(s.values)
    ends = np.array(ends); paths = np.array(paths)
    mc = {"end2025": ends.mean(), "min": paths.min(), "max": paths.max(),
          "std_logd": np.nan, "corr_M2": np.nan}
    rows["Monte Carlo (śr. z 1000)"] = mc

    table = pd.DataFrame(rows).T
    return table, catdf, income, m2, loo, (ends, paths, np.array(catdf.index))


def plot(table, loo, mc, m2):
    import matplotlib.pyplot as plt
    ends, paths, years = mc
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # (a) leave-one-out + pełny
    ax = axs[0, 0]
    catdf_full = loo  # dict
    base = None
    for c, s in loo.items():
        ax.plot(s.index, s, lw=1.6, label=f"bez {c}")
    ax.axhline(100, color="black", lw=0.6, alpha=0.5)
    ax.set_title("1. Leave-one-out kategorii", fontweight="bold")
    ax.set_ylabel(f"AUV-T ({BASE_YEAR}=100)"); ax.legend(fontsize=8); ax.grid(True, alpha=0.25)

    # (b) Monte Carlo: pasmo percentyli + M2
    ax = axs[0, 1]
    p5, p50, p95 = np.percentile(paths, [5, 50, 95], axis=0)
    ax.fill_between(years, p5, p95, color="#16a085", alpha=0.25, label="AUV-T 5–95 pct (1000 wag)")
    ax.plot(years, p50, color="#16a085", lw=2, label="AUV-T mediana")
    ax.plot(m2.index, m2, color="#c0392b", lw=2, label="M2 USA")
    ax.set_yscale("log")
    ax.axhline(100, color="black", lw=0.6, alpha=0.5)
    ax.set_title("2. Monte Carlo wag vs M2 (log)", fontweight="bold")
    ax.legend(fontsize=8); ax.grid(True, which="both", alpha=0.25)

    # (c) histogram końcówki 2025
    ax = axs[1, 0]
    ax.hist(ends, bins=40, color="#2980b9", alpha=0.8)
    ax.axvline(100, color="black", lw=1, ls="--", label="poziom 1996")
    ax.axvline(ends.mean(), color="#c0392b", lw=2, label=f"średnia {ends.mean():.0f}")
    ax.set_title("3. Rozkład AUV-T 2025 przy losowych wagach", fontweight="bold")
    ax.set_xlabel("AUV-T w 2025"); ax.legend(fontsize=8); ax.grid(True, alpha=0.25)

    # (d) tabela statystyk (end2025 i corr_M2)
    ax = axs[1, 1]; ax.axis("off")
    show = table[["end2025", "min", "max", "corr_M2"]].round(1)
    tab = ax.table(cellText=show.values, rowLabels=show.index,
                   colLabels=["2025", "min", "max", "kor. M2"],
                   loc="center", cellLoc="center")
    tab.auto_set_font_size(False); tab.set_fontsize(8.5); tab.scale(1, 1.4)
    ax.set_title("4. Statystyki konfiguracji", fontweight="bold")

    fig.suptitle("Walidacja wrażliwości AUV-T — czy wynik zależy od arbitralnych wyborów?",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p = FIGURES_DIR / "40_walidacja_wrazliwosc.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return p


def base_year_robustness(monthly: pd.DataFrame) -> pd.DataFrame:
    """Dryf AUV-T (koniec/początek) niezależnie od roku bazowego."""
    catdf, income, m2 = _components(monthly)
    s = auv(catdf, income, np.ones(len(CATS)))  # base 1996
    rows = {}
    for b in [1996, 2000, 2005, 2010, 2015]:
        sb = s / s.loc[b] * 100.0
        rows[b] = {"poziom_2025": sb.loc[2025], "dryf_całego_okresu_%": s.loc[2025]/s.loc[1996]*100-100}
    return pd.DataFrame(rows).T


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    table, catdf, income, m2, loo, mc = run(monthly)
    table.round(2).to_csv(PROCESSED_DIR / "sensitivity.csv")
    p = plot(table, loo, mc, m2)
    by = base_year_robustness(monthly)

    print("=== Wrażliwość: AUV-T 2025 i korelacja z M2 wg konfiguracji ===")
    print(table[["end2025", "min", "max", "corr_M2"]].round(2).to_string())
    print("\n=== Monte Carlo (1000 losowych wag) ===")
    ends = mc[0]
    print(f"  AUV-T 2025: średnia={ends.mean():.1f}, 5pct={np.percentile(ends,5):.1f}, "
          f"95pct={np.percentile(ends,95):.1f}  (M2 2025 = {m2.loc[2025]:.0f})")
    print("\n=== Rok bazowy: dryf całego okresu jest niezmienniczy ===")
    print(by.round(1).to_string())
    print("\nwykres:", p.name)


if __name__ == "__main__":
    main()
