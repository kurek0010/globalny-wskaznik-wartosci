"""AUV codzienny — przelicznik walutowy (jednostka do życia codziennego).

Idea: jednostka AUV reprezentuje STAŁĄ realną wartość (koszyk realnych
dóbr z roku bazowego). Jej cena w danej walucie = wygładzona cena tego
koszyka w tej walucie. Pokazuje, ILE danej waluty trzeba, by utrzymać tę
samą realną wartość — analogicznie do chilijskiej Unidad de Fomento.

Wygładzanie (5-letnie) czyni jednostkę na tyle stabilną, by dało się nią
posługiwać na co dzień (odnosić do niej ceny, umowy, oszczędności).

Uwaga: to jednostka RACHUNKOWA (nominalna cena stałej realnej wartości),
odróżnić od AUV-T (miary realnej w godzinach pracy).

Uruchamianie:  python -m src.auv_converter
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import BASE_YEAR, PROCESSED_DIR, FIGURES_DIR, compute, _annual, _index_to_base

SMOOTH = 5  # lat wygładzania (zamrożone)
# Waluty: kolumna FX = jednostek waluty za 1 USD. USD dodajemy jako 1.
CURRENCIES = ["EUR", "GBP", "PLN", "JPY", "CHF", "CNY"]


def build(monthly: pd.DataFrame) -> pd.DataFrame:
    a = _annual(monthly)
    basket_usd = _index_to_base(compute(monthly)["koszyk_nominalny"])  # USD, 1996=100

    df = pd.DataFrame(index=basket_usd.index)
    # Cena koszyka w każdej walucie; każdą serię rebasujemy do jej
    # PIERWSZEGO dostępnego roku = 100 (EUR od 1999, PLN od 2002).
    raw = {"USD": basket_usd}
    for cur in CURRENCIES:
        if cur not in a.columns or a[cur].notna().sum() < 5:
            continue
        raw[cur] = basket_usd * a[cur]             # cena koszyka w walucie (surowo)

    for cur, s in raw.items():
        s = s.dropna()
        s = s / s.iloc[0] * 100                     # rebase do pierwszego roku = 100
        df[cur] = np.exp(np.log(s).rolling(SMOOTH, min_periods=1).mean())
    return df


def plot(df: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(13, 7))
    palette = {"USD": "#2c3e50", "EUR": "#2980b9", "GBP": "#8e44ad",
               "PLN": "#c0392b", "JPY": "#e67e22", "CHF": "#16a085", "CNY": "#7f8c8d"}
    for cur in df.columns:
        ax.plot(df.index, df[cur], lw=2.2, color=palette.get(cur, "gray"), label=cur)
        ax.annotate(cur, (df.index[-1], df[cur].iloc[-1]), fontsize=8.5,
                    xytext=(4, 0), textcoords="offset points", va="center",
                    color=palette.get(cur, "gray"))
    ax.axhline(100, color="black", lw=0.6, alpha=0.5)
    ax.set_title("AUV codzienny: cena 1 jednostki AUV w każdej walucie (wygładzona)\n"
                 f"ile waluty trzeba, by utrzymać stałą realną wartość ({BASE_YEAR}=100)",
                 fontweight="bold")
    ax.set_ylabel(f"indeks ceny AUV w walucie ({BASE_YEAR}=100)")
    ax.set_xlabel("rok"); ax.legend(fontsize=9, ncol=2); ax.grid(True, alpha=0.25)
    ax.text(0.99, 0.02,
            "Wyżej = waluta bardziej się zdeprecjonowała wobec realnej wartości.\n"
            "Wygładzone 5-letnio -> nadaje się do codziennego odnoszenia cen i umów.",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5,
            bbox=dict(boxstyle="round", fc="#f7f7f7", ec="#cccccc"))
    fig.tight_layout()
    p = FIGURES_DIR / "46_auv_przelicznik.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return p


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    df = build(monthly)
    df.round(1).to_csv(PROCESSED_DIR / "auv_converter.csv")
    p = plot(df)
    print("=== Cena 1 jednostki AUV w walucie (index %d=100) ===" % BASE_YEAR)
    print(df.loc[[1996, 2010, 2025]].round(0).to_string())
    print("\nWzrost 1996->2025 (ile bardziej trzeba waluty na stałą realną wartość):")
    for cur in df.columns:
        print(f"  {cur}: {df[cur].iloc[-1]-100:+.0f}%")
    print("\nInterpretacja: różnice między walutami = różne tempo ich deprecjacji")
    print("wobec realnej wartości. Wygładzone -> jednostka codzienna (jak UF).")
    print("wykres:", p.name)


if __name__ == "__main__":
    main()
