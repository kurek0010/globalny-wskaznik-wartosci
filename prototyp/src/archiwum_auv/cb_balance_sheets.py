"""Krok (d): ekspansja bilansów banków centralnych vs inflacja —
USA / strefa euro / Japonia.

Zakres: porównujemy ILOŚĆ (sumę aktywów banku centralnego) z inflacją
CPI danej gospodarki. Pełny SKŁAD kolateralu jak dla Fed (UST/MBS) nie
jest dostępny w porównywalnej formie dla EBC/BoJ — stąd ten krok dotyczy
ekspansji, nie jakości kolateralu cross-country.

Pytanie: Japonia od dekad ma gigantyczną ekspansję bilansu BoJ, a niemal
zerową inflację. Jeśli sama ekspansja bilansu nie tłumaczy inflacji w JP,
to wzmacnia wniosek z kroku (b), że liczy się szerszy agregat (M2/kredyt),
a nie sam bilans banku centralnego.

Uruchamianie:  python -m src.cb_balance_sheets
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import PROCESSED_DIR, FIGURES_DIR

CB = {
    "USA": ("fed_total_assets", "CPI_USA"),
    "Strefa euro": ("ecb_total_assets", "CPI_EU"),
    "Japonia": ("boj_total_assets", "CPI_JP"),
}


def _annual(monthly: pd.DataFrame) -> pd.DataFrame:
    a = monthly.resample("YE").mean(); a.index = a.index.year
    return a


def analyse(monthly: pd.DataFrame):
    a = _annual(monthly)
    rows = {}
    series = {}
    for name, (bs_col, cpi_col) in CB.items():
        if bs_col not in a.columns:
            rows[name] = {"dostępne": False}; continue
        bs = a[bs_col].dropna()
        cpi = a[cpi_col]
        bs_growth = bs.iloc[-1] / bs.iloc[0] - 1
        years = bs.index[-1] - bs.index[0]
        cpi_growth = cpi.loc[bs.index[-1]] / cpi.loc[bs.index[0]] - 1
        corr = (bs.pct_change() * 100).corr(cpi.pct_change() * 100)
        rows[name] = {
            "okres": f"{bs.index[0]}-{bs.index[-1]}",
            "wzrost_bilansu_%": bs_growth * 100,
            "inflacja_okresu_%": cpi_growth * 100,
            "korelacja_dynamik": corr,
        }
        series[name] = (bs / bs.iloc[0] * 100, cpi / cpi.loc[bs.index[0]] * 100)
    return pd.DataFrame(rows).T, series


def plot(series: dict) -> Path:
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, len(series), figsize=(5 * len(series), 5.5), sharey=False)
    if len(series) == 1:
        axs = [axs]
    for ax, (name, (bs, cpi)) in zip(axs, series.items()):
        ax.plot(bs.index, bs, color="#c0392b", lw=2.5, label="bilans banku centr.")
        ax.plot(cpi.index, cpi, color="#2c3e50", lw=2.5, label="CPI")
        ax.set_yscale("log")
        ax.axhline(100, color="black", lw=0.6, alpha=0.4)
        ax.set_title(name, fontweight="bold")
        ax.set_xlabel("rok"); ax.legend(fontsize=8); ax.grid(True, which="both", alpha=0.25)
    axs[0].set_ylabel("indeks (początek = 100, log)")
    fig.suptitle("Krok (d): ekspansja bilansu banku centralnego vs inflacja CPI",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    p = FIGURES_DIR / "43_bilanse_cb_vs_inflacja.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return p


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    table, series = analyse(monthly)
    print("=== Bilanse banków centralnych vs inflacja ===")
    print(table.to_string())
    if series:
        p = plot(series)
        print("\nwykres:", p.name)
    else:
        print("\n[!] Brak serii bilansów EBC/BoJ — uruchom download + harmonize.")


if __name__ == "__main__":
    main()
