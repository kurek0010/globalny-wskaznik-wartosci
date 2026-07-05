"""Wskaźnik OBFITOŚCI na osobę — komplement do AUV.

AUV mierzy KOSZT zasobów (cena/dochód). Ten moduł mierzy ILOŚĆ: ile
zasobów przypada na osobę (produkcja globalna / populacja). Razem:
  - obfitość per capita rośnie  -> materialne bogacenie się,
  - AUV (koszt) stoi/spada      -> zasoby nie drożeją względem dochodu.
Jedno i drugie w górę (materialnie) = jednoznaczny rozwój.

Uwaga: ilości metali i budownictwa pochodzą z przybliżonych danych
produkcji (data/manual) — kierunek wiarygodny, poziom do weryfikacji.

Uruchamianie:  python -m src.abundance
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import BASE_YEAR, PROCESSED_DIR, FIGURES_DIR, compute
from .auv_research import needs_weighted, NEED_PROXY


def build(monthly: pd.DataFrame) -> pd.DataFrame:
    nw = needs_weighted(monthly)
    cats = list(NEED_PROXY)
    qty = pd.concat([nw[f"ilosc_pc_{c}"].rename(c) for c in cats], axis=1)
    # aglomerat obfitości = średnia geometryczna ilości per capita kategorii
    abundance = np.exp(np.log(qty).mean(axis=1))
    auv = compute(monthly)["AUV_T"]
    afford = 1.0 / auv * 100 * 100  # dostępność = 1/AUV (znormalizowana, 1996=100)
    out = qty.copy()
    out["OBFITOSC_per_capita"] = abundance
    out["AUV_koszt"] = auv
    out["dostepnosc(1/AUV)"] = afford
    return out


def plot(df: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5))
    colors = {"energia": "#34495e", "zywnosc": "#27ae60",
              "metale": "#8e44ad", "budownictwo": "#d35400"}

    # panel 1: konsumpcja per capita wg kategorii
    for c, col in colors.items():
        if c in df.columns:
            ax1.plot(df.index, df[c], color=col, lw=2, label=c)
    ax1.plot(df.index, df["OBFITOSC_per_capita"], color="#c0392b", lw=3.2,
             label="OBFITOŚĆ (łącznie)")
    ax1.axhline(100, color="black", lw=0.6, alpha=0.4)
    ax1.set_title("Zużycie zasobów na osobę (produkcja / ludność)", fontweight="bold")
    ax1.set_ylabel(f"indeks ({BASE_YEAR}=100)"); ax1.set_xlabel("rok")
    ax1.legend(fontsize=9, loc="upper left"); ax1.grid(True, alpha=0.25)

    # panel 2: obfitość (ilość) vs AUV (koszt)
    ax2.plot(df.index, df["OBFITOSC_per_capita"], color="#c0392b", lw=3,
             label="OBFITOŚĆ na osobę (ilość) ↑ = bogatszy")
    ax2.plot(df.index, df["AUV_koszt"], color="#16a085", lw=3,
             label="AUV (koszt w dochodzie)")
    ax2.axhline(100, color="black", lw=0.6, alpha=0.5)
    ax2.set_title("Obfitość (ile mamy) vs AUV (ile kosztuje)", fontweight="bold")
    ax2.set_ylabel(f"indeks ({BASE_YEAR}=100)"); ax2.set_xlabel("rok")
    ax2.legend(fontsize=9, loc="upper left"); ax2.grid(True, alpha=0.25)
    ax2.text(0.99, 0.03,
             "Więcej na osobę przy ~stałym koszcie pracy = materialne bogacenie się.\n"
             "Metale/budownictwo z przybliżonych danych produkcji (kierunek OK).",
             transform=ax2.transAxes, ha="right", va="bottom", fontsize=8,
             bbox=dict(boxstyle="round", fc="#f7f7f7", ec="#cccccc"))

    fig.suptitle("Dwie strony bogactwa materialnego: ilość zasobów na osobę i ich koszt",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    p = FIGURES_DIR / "49_obfitosc_vs_auv.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return p


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    df = build(monthly)
    df.round(1).to_csv(PROCESSED_DIR / "abundance.csv")
    p = plot(df)
    e = df.index.max()
    print("=== Zużycie na osobę 1996 -> %d (indeks 1996=100) ===" % e)
    for c in list(NEED_PROXY) + ["OBFITOSC_per_capita"]:
        if c in df.columns:
            print("  %-22s %6.0f  (%+.0f%%)" % (c, df[c].loc[e], df[c].loc[e]-100))
    print("  %-22s %6.0f" % ("AUV_koszt", df["AUV_koszt"].loc[e]))
    print("wykres:", p.name)


if __name__ == "__main__":
    main()
