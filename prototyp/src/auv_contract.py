"""Krok (c): wariant KONTRAKTOWY AUV — do indeksacji umów wieloletnich.

Jednostka kontraktowa musi być GŁADKA (niskie zmiany rok-do-roku) i
ustalona jawną regułą (bez uznaniowości po fakcie). Bierzemy szeroki
koszyk AUV-T (19 surowców, 4 kategorie) i nakładamy dwie zamrożone reguły:

  1. Rok bazowy: średnia z pierwszych BASE_WINDOW lat (nie pojedynczy rok
     — rekomendacja z walidacji wrażliwości, by uniknąć ekstremum cyklu).
  2. Wygładzanie: krocząca średnia geometryczna SMOOTH_WINDOW lat
     (przyczynowa — bez podglądania przyszłości).

Metryki kontraktowe: maks. zmiana roczna, zmienność, obsunięcie.
Porównanie z indeksacją CPI.

Uruchamianie:  python -m src.auv_contract
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import PROCESSED_DIR, FIGURES_DIR, compute

BASE_WINDOW = 3    # lat do ustalenia poziomu bazowego (zamrożone)
SMOOTH_WINDOW = 5  # lat wygładzania kroczącego (zamrożone)


def contract_series(monthly: pd.DataFrame) -> pd.DataFrame:
    out = compute(monthly)
    raw = out["AUV_T"]
    cpi = out["CPI_USA"]

    # Reguła roku bazowego: średnia pierwszych BASE_WINDOW lat = 100
    def rebase(s):
        return s / s.iloc[:BASE_WINDOW].mean() * 100.0

    raw_r = rebase(raw)
    cpi_r = rebase(cpi)
    contract = np.exp(np.log(raw_r).rolling(SMOOTH_WINDOW, min_periods=1).mean())

    df = pd.DataFrame({"AUV_raw": raw_r, "AUV_kontrakt": contract, "CPI": cpi_r})
    return df


def metrics(df: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for col in ["AUV_raw", "AUV_kontrakt", "CPI"]:
        s = df[col]
        chg = s.pct_change() * 100
        rows[col] = {
            "maks_zmiana_roczna_%": chg.abs().max(),
            "śr_|zmiana|_%": chg.abs().mean(),
            "std_zmian_%": chg.std(),
            "maks_spadek_%": chg.min(),
        }
    return pd.DataFrame(rows).T


def plot(df: pd.DataFrame, met: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), gridspec_kw={"height_ratios": [2, 1]})

    ax1.plot(df.index, df["AUV_raw"], color="#bdc3c7", lw=1.5, label="AUV-T surowe")
    ax1.plot(df.index, df["AUV_kontrakt"], color="#16a085", lw=3,
             label=f"AUV kontraktowy ({SMOOTH_WINDOW}-letni)")
    ax1.plot(df.index, df["CPI"], color="#e67e22", lw=2, ls="--", label="CPI (dla porównania)")
    ax1.axhline(100, color="black", lw=0.6, alpha=0.4)
    ax1.set_title(f"Krok (c): AUV kontraktowy — baza = śr. {BASE_WINDOW} pierwszych lat, "
                  f"wygładzanie {SMOOTH_WINDOW}-letnie", fontweight="bold")
    ax1.set_ylabel("indeks (baza = 100)"); ax1.legend(fontsize=9); ax1.grid(True, alpha=0.25)

    chg = df.pct_change() * 100
    ax2.plot(chg.index, chg["AUV_raw"], color="#bdc3c7", lw=1.2, label="surowe")
    ax2.plot(chg.index, chg["AUV_kontrakt"], color="#16a085", lw=2.5, label="kontraktowy")
    ax2.plot(chg.index, chg["CPI"], color="#e67e22", lw=1.5, ls="--", label="CPI")
    ax2.axhline(0, color="black", lw=0.6)
    ax2.set_title("Zmiany rok-do-roku (kluczowe dla rat kredytowych)", fontweight="bold")
    ax2.set_ylabel("% r/r"); ax2.set_xlabel("rok"); ax2.legend(fontsize=8); ax2.grid(True, alpha=0.25)

    fig.tight_layout()
    p = FIGURES_DIR / "42_auv_kontraktowy.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return p


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    df = contract_series(monthly)
    met = metrics(df)
    df.round(2).to_csv(PROCESSED_DIR / "auv_contract.csv")
    p = plot(df, met)
    print("=== Metryki kontraktowe (gładkość) ===")
    print(met.round(2).to_string())
    print(f"\nWygładzanie {SMOOTH_WINDOW}-letnie obniża maks. roczną zmianę z "
          f"{met.loc['AUV_raw','maks_zmiana_roczna_%']:.0f}% do "
          f"{met.loc['AUV_kontrakt','maks_zmiana_roczna_%']:.0f}% "
          f"(CPI: {met.loc['CPI','maks_zmiana_roczna_%']:.0f}%).")
    print("wykres:", p.name)


if __name__ == "__main__":
    main()
