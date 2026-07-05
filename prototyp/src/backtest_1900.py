"""Backtest AUV 1900-1995 na TWARDYCH danych historycznych.

Zastępuje rekonstrukcję ilustracyjną (wykres 47) obliczeniem z danych
wpisanych do data/manual/backtest_historyczny.csv (źródła: Grilli-Yang/
Pfaffenzeller, Maddison, Officer-Williamson — patrz ZRODLA_backtest_
historyczny.md). Zszywa część historyczną z policzonym szeregiem 1996+.

Rozstrzyga pytanie z LUKI 1 oceny: czy AUV ma wieloletni trend, czy
oscyluje wokół stałej.

Uruchamianie:  python -m src.backtest_1900
Dopóki plik jest pusty, skrypt wypisuje instrukcję i nic nie liczy.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import PROCESSED_DIR, FIGURES_DIR, compute

MANUAL = Path("data/manual/backtest_historyczny.csv")


def _load_hist() -> pd.DataFrame | None:
    if not MANUAL.exists():
        return None
    df = pd.read_csv(MANUAL, comment="#")
    df = df.set_index("year")
    have = df.dropna(how="all")
    if have.empty:
        return None
    return df.interpolate("linear").dropna(how="all")


def compute_historical(monthly: pd.DataFrame):
    hist = _load_hist()
    if hist is None or hist["commodity_index_real"].notna().sum() < 3 \
            or hist["world_gdppc_real"].notna().sum() < 3:
        return None

    b = hist.index.min()
    ci = hist["commodity_index_real"]; ci = ci / ci.loc[b] * 100
    gd = hist["world_gdppc_real"]; gd = gd / gd.loc[b] * 100
    auv_pkb = ci / gd * 100                       # AUV deflowany PKB, b=100

    out = {"AUV_PKB": auv_pkb}
    if hist["us_real_wage"].notna().sum() >= 3:
        wg = hist["us_real_wage"]; wg = wg / wg.loc[b] * 100
        out["AUV_placa"] = ci / wg * 100          # wariant deflowany płacą
    return pd.DataFrame(out)


def plot(histdf: pd.DataFrame, monthly: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    auv_mod = compute(monthly)["AUV_T"]
    link_year = histdf.index.max()               # np. 1995
    # zszycie: nasz 1996 = poziom historyczny w link_year (ciągłość)
    splice = histdf["AUV_PKB"].loc[link_year]
    recent = auv_mod / auv_mod.loc[auv_mod.index.min()] * splice

    fig, ax = plt.subplots(figsize=(13, 7))
    ax.plot(histdf.index, histdf["AUV_PKB"], color="#c0392b", lw=2,
            label="AUV 1900-1995 (dane hist., deflowane PKB)")
    if "AUV_placa" in histdf.columns:
        ax.plot(histdf.index, histdf["AUV_placa"], color="#8e44ad", lw=1.8, ls="--",
                label="wariant deflowany płacą")
    ax.plot(recent.index, recent, color="#16a085", lw=2.5,
            label="AUV 1996-2024 (nasze dane, zszyte)")
    ax.axhline(100, color="black", lw=0.6, alpha=0.4)
    ax.set_yscale("log")
    # adnotacja: część historyczna to dane robocze do weryfikacji
    ax.axvspan(histdf.index.min(), link_year, color="#c0392b", alpha=0.05)
    ax.annotate("DANE ROBOCZE DO WERYFIKACJI\n(kotwice z wiedzy, nie źródła pierwotne)",
                xy=(0.30, 0.90), xycoords="axes fraction", ha="center", fontsize=9,
                color="#c0392b", fontweight="bold",
                bbox=dict(boxstyle="round", fc="#fff3f3", ec="#c0392b", alpha=0.9))
    ax.annotate("dane policzone (1996+)", xy=(0.86, 0.20), xycoords="axes fraction",
                ha="center", fontsize=8.5, color="#16a085")
    ax.set_title("Backtest AUV w skali stulecia — część przed 1996 do weryfikacji źródłowej",
                 fontweight="bold")
    ax.set_ylabel(f"AUV ({histdf.index.min()}=100, log)"); ax.set_xlabel("rok")
    ax.legend(fontsize=9); ax.grid(True, which="both", alpha=0.25)
    fig.tight_layout()
    p = FIGURES_DIR / "48_auv_backtest_1900_dane.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return p


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    histdf = compute_historical(monthly)
    if histdf is None:
        print("[!] Brak danych w data/manual/backtest_historyczny.csv.")
        print("    Wypełnij wg ZRODLA_backtest_historyczny.md, potem uruchom ponownie.")
        return
    b = histdf.index.min(); e = histdf.index.max()
    drift = histdf["AUV_PKB"].loc[e] / 100 - 1
    cagr = (histdf["AUV_PKB"].loc[e] / 100) ** (1 / (e - b)) - 1
    print(f"AUV historyczny {b}->{e}: {drift*100:+.0f}%  ({cagr*100:+.1f}%/rok)")
    if "AUV_placa" in histdf.columns:
        dp = histdf["AUV_placa"].loc[e] / 100 - 1
        print(f"  wariant deflowany płacą: {dp*100:+.0f}%")
    p = plot(histdf, monthly)
    print("wykres:", p.name)
    print("\nWniosek: jeśli |trend| duży -> AUV ma zdefiniowany trend (miara postępu),")
    print("nie jest stałą jednostką. Jeśli ~0 -> teza o stałości się broni.")


if __name__ == "__main__":
    main()
