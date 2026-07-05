"""Analogia inwestycyjna: giełdy widziane przez AUV-T.

Dwa ujęcia:
  1. Giełdy w GODZINACH PRACY (indeks / dochód) — realna wartość rynku,
     oczyszczona z iluzji monetarnej. Różnice USA/UK/JP „coś mówią".
  2. Hipoteza czasowa autora: czy niskie AUV-T (tanie realne dobra, mocny
     pieniądz) poprzedza wyższe późniejsze stopy zwrotu z akcji?
     Test: korelacja AUV-T[t] z przyszłą stopą zwrotu (k lat do przodu).

UWAGA: analiza historyczna, NIE porada inwestycyjna.

Uruchamianie:  python -m src.auv_markets
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import BASE_YEAR, PROCESSED_DIR, FIGURES_DIR, compute, _annual, _index_to_base

MARKETS = {"USA": "stock_us", "Wielka Brytania": "stock_uk", "Japonia": "stock_jp"}


def build(monthly: pd.DataFrame):
    out = compute(monthly)
    a = _annual(monthly)
    auv = out["AUV_T"]
    income = out["dochod_glob_per_capita"]
    df = pd.DataFrame({"AUV_T": auv, "income": income})
    for name, col in MARKETS.items():
        if col not in a.columns or a[col].notna().sum() < 5:
            continue
        nom = _index_to_base(a[col])
        df[f"{name}_nominal"] = nom
        df[f"{name}_w_pracy"] = nom / income * 100          # giełda w godzinach pracy
        df[f"{name}_w_AUV"] = nom / auv * 100                # giełda w jednostkach AUV
    return df


def timing_test(df: pd.DataFrame, horizons=(1, 3, 5)) -> pd.DataFrame:
    """Korelacja AUV-T[t] z przyszłą stopą zwrotu giełdy (k lat)."""
    rows = {}
    for name in MARKETS:
        col = f"{name}_nominal"
        if col not in df.columns:
            continue
        r = {}
        for k in horizons:
            fwd = df[col].shift(-k) / df[col] - 1          # zwrot t -> t+k
            r[f"{k}L"] = df["AUV_T"].corr(fwd)
        rows[name] = r
    return pd.DataFrame(rows).T


def plot(df: pd.DataFrame, timing: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    colors = {"USA": "#2980b9", "Wielka Brytania": "#c0392b", "Japonia": "#e67e22"}

    # (a) giełdy nominalnie
    ax = axs[0, 0]
    for name in MARKETS:
        c = f"{name}_nominal"
        if c in df.columns:
            ax.plot(df.index, df[c], color=colors[name], lw=2, label=name)
    ax.set_yscale("log"); ax.axhline(100, color="black", lw=0.6, alpha=0.4)
    ax.set_title("Giełdy nominalnie (indeks, 1996=100, log)", fontweight="bold")
    ax.legend(fontsize=9); ax.grid(True, which="both", alpha=0.25)

    # (b) giełdy w godzinach pracy
    ax = axs[0, 1]
    for name in MARKETS:
        c = f"{name}_w_pracy"
        if c in df.columns:
            ax.plot(df.index, df[c], color=colors[name], lw=2.5, label=name)
    ax.axhline(100, color="black", lw=0.8, alpha=0.6)
    ax.set_title("Giełdy w GODZINACH PRACY (realna wartość rynku)", fontweight="bold")
    ax.set_ylabel(f"indeks ({BASE_YEAR}=100)"); ax.legend(fontsize=9); ax.grid(True, alpha=0.25)

    # (c) AUV-T + odwrócone (siła nabywcza) jako sygnał
    ax = axs[1, 0]
    ax.plot(df.index, df["AUV_T"], color="#16a085", lw=2.5, label="AUV-T")
    ax.fill_between(df.index, 100, df["AUV_T"], where=df["AUV_T"] >= 100,
                    color="#c0392b", alpha=0.2, label="drogo (słaby pieniądz)")
    ax.fill_between(df.index, 100, df["AUV_T"], where=df["AUV_T"] < 100,
                    color="#2980b9", alpha=0.2, label="tanio (mocny pieniądz)")
    ax.axhline(100, color="black", lw=0.6)
    ax.set_title("AUV-T: faza tanio/drogo realnych dóbr", fontweight="bold")
    ax.set_xlabel("rok"); ax.legend(fontsize=8); ax.grid(True, alpha=0.25)

    # (d) test czasowy: korelacja AUV-T z przyszłym zwrotem
    ax = axs[1, 1]; ax.axis("off")
    if not timing.empty:
        t = timing.round(2)
        tab = ax.table(cellText=t.values, rowLabels=t.index, colLabels=t.columns,
                       loc="center", cellLoc="center")
        tab.auto_set_font_size(False); tab.set_fontsize(10); tab.scale(1, 1.8)
    ax.set_title("Korelacja AUV-T[t] z przyszłym zwrotem giełdy\n"
                 "(ujemna = niskie AUV-T → wyższe późniejsze zwroty)", fontweight="bold")

    fig.suptitle("AUV-T a giełdy: realna wartość rynków i sygnał czasowy",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p = FIGURES_DIR / "44_auv_gieldy.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return p


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    df = build(monthly)
    have = [n for n in MARKETS if f"{n}_nominal" in df.columns]
    if not have:
        print("[!] Brak serii giełdowych — uruchom: python -m src.download && python -m src.harmonize")
        return
    timing = timing_test(df)
    df.round(2).to_csv(PROCESSED_DIR / "auv_markets.csv")
    p = plot(df, timing)
    print("=== Giełdy 1996 -> 2025 ===")
    for name in have:
        print(f"  {name:16} nominalnie {df[f'{name}_nominal'].iloc[-1]:7.0f}   "
              f"w pracy {df[f'{name}_w_pracy'].iloc[-1]:7.0f}   "
              f"w AUV {df[f'{name}_w_AUV'].iloc[-1]:7.0f}")
    print("\n=== Test czasowy: korelacja AUV-T[t] z przyszłym zwrotem (k lat) ===")
    print(timing.round(2).to_string())
    print("\nwykres:", p.name)


if __name__ == "__main__":
    main()
