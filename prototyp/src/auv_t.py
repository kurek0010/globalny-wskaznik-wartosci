"""AUV-T — Absolute Unit of Value w numéraire czasu pracy (v0.4).

Idea (patrz PODSUMOWANIE_DLA_EKSPERTA.md, sekcja 10):

    AUV_T(t) = KoszykCen(t) / DochódGlobalnyNaOsobę(t)   [indeks, t0 = 100]

Licznik to fizyczny koszyk surowców (5 kategorii), mianownik to cena
ludzkiej pracy/czasu (światowy dochód na osobę). Dzielenie ceny w USD
przez dochód w USD KASUJE jednostkę walutową — wynik jest wyrażony w
ludzkim czasie, wielkości niemonetarnej, której nie da się wykreować
księgowo. To wychodzi z pułapki fiat, w którą wpadły iteracje v0.1–v0.3.1.

Zasady heliocentryczne wymuszone w kodzie:
  * formuła deterministyczna — te same dane => ta sama liczba,
  * koszyk, wagi i rok bazowy ZAMROŻONE jako stałe poniżej (bez rewizji
    po fakcie — jakakolwiek zmiana to świadoma, jawna decyzja w repo),
  * średnia geometryczna (odporna na pojedyncze szoki, symetryczna),
  * brak ML, brak czarnych skrzynek, brak danych subskrypcyjnych.

Uruchamianie:
    python -m src.auv_t
Wytwarza:
    data/processed/auv_t.csv
    outputs/figures/30_auv_t_vs_m2_cpi.png
    outputs/figures/31_auv_t_vs_currencies.png
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROTOTYP_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROTOTYP_ROOT / "data" / "processed"
FIGURES_DIR = PROTOTYP_ROOT / "outputs" / "figures"

# --- PARAMETRY ZAMROŻONE (heliocentryczność: bez uznaniowej rewizji) -----
BASE_YEAR = 1996

# Koszyk fizyczny: 5 kategorii, równe wagi między kategoriami,
# równe wagi w obrębie kategorii. Najmniej uznaniowy wybór startowy.
CATEGORIES: dict[str, list[str]] = {
    "energia": ["brent", "natgas_us", "coal_aus", "uranium"],
    "zywnosc": ["wheat", "corn", "rice", "soy", "palm_oil"],
    "metale": ["copper", "aluminum", "iron_ore", "nickel", "zinc", "lead", "tin"],
    "budownictwo": ["steel", "cement"],
}

# Mianownik — cena pracy cywilizacji. Wariant minimalny, liczalny dziś:
# światowy dochód nominalny na osobę = PKB_świata / populacja.
INCOME_NUM = "gdp_world_current_usd"
INCOME_DEN = "world_population"

# SDR jako komparator "neutralnej jednostki". SDR to koszyk pięciu walut;
# jego skumulowaną inflację składamy z CPI składowych, ważąc oficjalnymi
# wagami SDR (rewizja MFW 2022). Wagi zamrożone i jawne — świadomie
# stosujemy stałą formułę zamiast zmiennych w czasie decyzji Zarządu MFW
# (zgodnie z filozofią: syntetyczny SDR z transparentnymi wagami).
# Uproszczenie: stałe wagi dla całego okresu (CNY wszedł do koszyka
# dopiero w 2016) — to komparator poglądowy, nie produkcyjny.
SDR_WEIGHTS: dict[str, float] = {
    "CPI_USA": 0.4338,  # USD
    "CPI_EU": 0.2931,   # EUR
    "CPI_CN": 0.1228,   # CNY
    "CPI_JP": 0.0759,   # JPY
    "CPI_UK": 0.0744,   # GBP
}
# -------------------------------------------------------------------------


def _annual(df: pd.DataFrame) -> pd.DataFrame:
    a = df.resample("YE").mean()
    a.index = a.index.year
    return a


def _index_to_base(s: pd.Series) -> pd.Series:
    """Normalizuj serię do roku bazowego = 100."""
    return s / s.loc[BASE_YEAR] * 100.0


def _geom_mean(frame: pd.DataFrame) -> pd.Series:
    """Średnia geometryczna po kolumnach (każda już znormalizowana)."""
    return np.exp(np.log(frame).mean(axis=1))


def _sdr_cpi(a: pd.DataFrame) -> pd.Series | None:
    """Syntetyczna skumulowana inflacja SDR z CPI walut składowych.

    Ważona geometryczna (wagi SDR) znormalizowanych CPI; wagi
    renormalizowane do dostępnych składowych. Zwraca None, jeśli brak
    którejkolwiek serii CPI koszyka.
    """
    cols = [c for c in SDR_WEIGHTS if c in a.columns]
    if len(cols) < len(SDR_WEIGHTS):
        return None
    logn = pd.concat([np.log(_index_to_base(a[c])).rename(c) for c in cols], axis=1)
    w = pd.Series({c: SDR_WEIGHTS[c] for c in cols})
    # Ważona średnia logarytmów po DOSTĘPNYCH składowych (renormalizacja
    # wag per wiersz — odporne na luki w pojedynczej serii CPI).
    num = (logn * w).sum(axis=1, min_count=1)
    den = (logn.notna() * w).sum(axis=1)
    return np.exp(num / den)


def compute(monthly: pd.DataFrame) -> pd.DataFrame:
    """Policz AUV-T i komponenty. Zwraca roczną ramkę (rok = indeks)."""
    a = _annual(monthly)

    # Indeksy kategorii (geometryczna średnia znormalizowanych cen)
    cat_idx: dict[str, pd.Series] = {}
    for name, cols in CATEGORIES.items():
        missing = [c for c in cols if c not in a.columns]
        if missing:
            raise KeyError(f"Brak kolumn dla kategorii {name}: {missing}")
        cat_idx[name] = _geom_mean(pd.concat([_index_to_base(a[c]) for c in cols], axis=1))

    # Mianownik: dochód globalny na osobę, znormalizowany
    income = _index_to_base(a[INCOME_NUM] / a[INCOME_DEN])

    # Licznik: koszyk = geometryczna średnia indeksów kategorii (równe wagi)
    basket = _geom_mean(pd.concat(cat_idx.values(), axis=1))

    # AUV-T
    auv_t = basket / income * 100.0

    out = pd.DataFrame({f"kat_{k}": v for k, v in cat_idx.items()})
    out["koszyk_nominalny"] = basket
    out["dochod_glob_per_capita"] = income
    out["AUV_T"] = auv_t
    if "CPI_USA" in a.columns:
        out["CPI_USA"] = _index_to_base(a["CPI_USA"])
    if "M2_USA" in a.columns:
        out["M2_USA"] = _index_to_base(a["M2_USA"])
    return out


def plot_vs_m2_cpi(out: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel lewy: AUV-T vs CPI vs M2 (log)
    ax1.plot(out.index, out["M2_USA"], color="#c0392b", lw=2, label="M2 USA (ekspansja monetarna)")
    ax1.plot(out.index, out["koszyk_nominalny"], color="#7f8c8d", lw=1.5, ls="--", label="Koszyk nominalny (USD)")
    ax1.plot(out.index, out["CPI_USA"], color="#e67e22", lw=2, label="CPI USA (inflacja konsumencka)")
    ax1.plot(out.index, out["AUV_T"], color="#16a085", lw=3, label="AUV-T (numéraire czasu)")
    ax1.axhline(100, color="black", lw=0.6, alpha=0.5)
    ax1.set_yscale("log")
    ax1.set_title("AUV-T vs M2 i CPI (skala log, %s = 100)" % BASE_YEAR, fontweight="bold")
    ax1.set_ylabel("indeks (log)")
    ax1.legend(fontsize=9, loc="upper left")
    ax1.grid(True, which="both", alpha=0.25)

    # Panel prawy: kategorie AUV-T w czasie
    income = out["dochod_glob_per_capita"]
    colors = {"energia": "#34495e", "zywnosc": "#27ae60", "metale": "#8e44ad", "budownictwo": "#d35400"}
    for k, c in colors.items():
        col = f"kat_{k}"
        if col in out.columns:
            ax2.plot(out.index, out[col] / income * 100.0, color=c, lw=2, label=k)
    ax2.plot(out.index, out["AUV_T"], color="#16a085", lw=3, label="AUV-T (łącznie)")
    ax2.axhline(100, color="black", lw=0.6, alpha=0.5)
    ax2.set_title("Kategorie w jednostkach czasu pracy", fontweight="bold")
    ax2.set_ylabel("indeks (%s = 100)" % BASE_YEAR)
    ax2.legend(fontsize=9, loc="upper left")
    ax2.grid(True, alpha=0.25)

    fig.suptitle(
        "AUV-T: realna wartość koszyka cywilizacji mierzona ludzkim czasem pracy",
        fontsize=13, fontweight="bold",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / "30_auv_t_vs_m2_cpi.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_vs_currencies(monthly: pd.DataFrame, out: pd.DataFrame) -> Path:
    """Interpretacja: AUV jako kotwica vs skumulowana inflacja walut.

    Każdą walutę reprezentuje jej CPI znormalizowane do roku bazowego =
    100 (skumulowana utrata siły nabywczej). AUV-T (≈ płaski) jest
    kotwicą: pionowy dystans między linią waluty a AUV-T = o ile dana
    waluta zdeprecjonowała się względem jednostki absolutnej.
    """
    import matplotlib.pyplot as plt

    a = _annual(monthly)
    names = {
        "CPI_USA": "USD", "CPI_EU": "EUR", "CPI_JP": "JPY", "CPI_UK": "GBP",
        "CPI_CH": "CHF", "CPI_CN": "CNY", "CPI_PL": "PLN", "CPI_BR": "BRL",
    }
    present = [c for c in names if c in a.columns]

    fig, ax = plt.subplots(figsize=(13, 7.5))
    cmap = plt.colormaps.get_cmap("tab10")
    for i, col in enumerate(present):
        cum = _index_to_base(a[col])
        ax.plot(cum.index, cum.values, lw=1.6, color=cmap(i % 10), alpha=0.85, label=names[col])
        ax.annotate(names[col], (cum.index[-1], cum.values[-1]), fontsize=8,
                    xytext=(4, 0), textcoords="offset points", va="center", color=cmap(i % 10))

    # SDR — syntetyczna jednostka MFW (komparator "neutralnej" jednostki)
    sdr = _sdr_cpi(a)
    if sdr is not None:
        ax.plot(sdr.index, sdr.values, color="#1f3a93", lw=3.0, ls="--",
                label="SDR (koszyk MFW, syntet.)", zorder=9)
        ax.annotate("SDR", (sdr.index[-1], sdr.values[-1]), fontsize=9,
                    xytext=(4, 0), textcoords="offset points", va="center",
                    color="#1f3a93", fontweight="bold")

    # AUV-T — jednostka heliocentryczna
    ax.plot(out.index, out["AUV_T"], color="black", lw=3.5, label="AUV-T (heliocentryczna)", zorder=10)
    ax.annotate("AUV-T", (out.index[-1], out["AUV_T"].iloc[-1]), fontsize=9,
                xytext=(4, 0), textcoords="offset points", va="center", fontweight="bold")
    ax.axhline(100, color="black", lw=0.6, alpha=0.4)
    ax.set_title(
        "Dwie kandydatki na jednostkę wartości (SDR vs AUV-T) "
        "na tle inflacji %d walut (%d = 100)" % (len(present), BASE_YEAR),
        fontsize=13, fontweight="bold",
    )
    ax.set_ylabel("poziom cen / siła nabywcza (%d = 100)" % BASE_YEAR)
    ax.set_xlabel("rok")
    ax.legend(fontsize=9, loc="upper left", ncol=2)
    ax.grid(True, alpha=0.25)
    ax.text(
        0.99, 0.02,
        "Im wyżej linia, tym większa utrata siły nabywczej.\n"
        "SDR (koszyk fiat) dryfuje w górę razem z walutami — bo sam jest z fiat.\n"
        "AUV-T (czarna) płaska = wartość zakotwiczona w ludzkiej pracy, nie w pieniądzu.",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5,
        bbox=dict(boxstyle="round", fc="#f7f7f7", ec="#cccccc"),
    )
    fig.tight_layout()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / "31_auv_t_vs_currencies.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    out = compute(monthly)

    csv_path = PROCESSED_DIR / "auv_t.csv"
    out.round(3).to_csv(csv_path)

    f1 = plot_vs_m2_cpi(out)
    f2 = plot_vs_currencies(monthly, out)

    chg = lambda s: out[s].loc[out.index.max()] / 100.0 - 1.0
    print("AUV-T policzony. Rok bazowy =", BASE_YEAR)
    print("  zapis:", csv_path)
    print("  wykres 1:", f1)
    print("  wykres 2:", f2)
    print("Zmiana %d -> %d:" % (out.index.min(), out.index.max()))
    for s in ["koszyk_nominalny", "M2_USA", "CPI_USA", "dochod_glob_per_capita", "AUV_T"]:
        if s in out.columns:
            print("  %-26s %+7.1f%%" % (s, chg(s) * 100))
    print("Zmienność AUV-T (std rocznych zmian log): %.3f"
          % np.log(out["AUV_T"]).diff().std())


if __name__ == "__main__":
    main()
