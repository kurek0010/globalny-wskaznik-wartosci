"""Test tezy: czy inflacja koreluje bliżej ze wzrostem pieniądza INNEGO
niż hipoteczny?

Teza autora: pieniądz kreowany pod hipotekę nie napędza inflacji
konsumenckiej; napędza ją głównie monetyzacja długu państwowego i inne
składniki. Test (świadomie prosty): korelacja 12-mies. dynamiki każdego
składnika [t-lag] z inflacją CPI [t], przy różnych opóźnieniach.

Uruchamianie:  python -m src.collateral_inflation
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import PROCESSED_DIR, FIGURES_DIR

LAGS = list(range(0, 37, 3))  # miesiące


def _yoy(s: pd.Series) -> pd.Series:
    return s.pct_change(12, fill_method=None) * 100


def analyse(monthly: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    m = monthly
    cpi = _yoy(m["CPI_USA"])
    components = {
        "M2 (cały)": m["M2_USA"],
        "hipoteki banki (REALLN)": m["bank_loans_realestate"],
        "biznes": m["bank_loans_business"],
        "konsumpcja": m["bank_loans_consumer"],
        "dług państwa (Fed UST)": m["fed_treasuries"],
        "NIE-hipoteki (biznes+konsum)": m["bank_loans_business"] + m["bank_loans_consumer"],
    }
    if "mortgage_debt_total" in m.columns:
        components["hipoteki CAŁE (z sekuryt.)"] = m["mortgage_debt_total"]
    rows = {}
    best = {}
    for name, ser in components.items():
        g = _yoy(ser)
        cors = {lag: g.shift(lag).corr(cpi) for lag in LAGS}
        rows[name] = cors
        bl = max(cors, key=lambda l: abs(cors[l]))
        best[name] = (bl, cors[bl])
    table = pd.DataFrame(rows).T
    table.columns = [f"lag{l}" for l in LAGS]
    best_s = pd.Series({k: v[1] for k, v in best.items()})
    best_lag = pd.Series({k: v[0] for k, v in best.items()})
    table["best_corr"] = best_s
    table["best_lag_m"] = best_lag
    return table, best_s


def plot(monthly: pd.DataFrame, table: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    m = monthly
    cpi = _yoy(m["CPI_USA"])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9.5))

    # Panel 1: najlepsza korelacja każdego składnika z inflacją
    order = table.sort_values("best_corr")
    colors = ["#27ae60" if "hipotek" in n else "#c0392b" for n in order.index]
    ax1.barh(order.index, order["best_corr"], color=colors, alpha=0.85)
    for i, (n, r) in enumerate(zip(order.index, order["best_corr"])):
        ax1.text(r + (0.01 if r >= 0 else -0.01), i,
                 f"{r:+.2f} (lag {int(order['best_lag_m'][n])}m)",
                 va="center", ha="left" if r >= 0 else "right", fontsize=8.5)
    ax1.axvline(0, color="black", lw=0.8)
    ax1.set_xlim(-0.4, 0.65)
    ax1.set_title("Najsilniejsza korelacja dynamiki składnika z inflacją CPI\n"
                  "(zielony = hipoteki; czerwony = pozostałe)", fontweight="bold")
    ax1.set_xlabel("korelacja przy najlepszym opóźnieniu")

    # Panel 2: szeregi — inflacja vs M2 vs hipoteki vs dług państwa
    ax2.plot(cpi.index, cpi, color="#2c3e50", lw=2.5, label="CPI USA r/r %")
    ax2.plot(cpi.index, _yoy(m["M2_USA"]).shift(18), color="#8e44ad", lw=1.8,
             label="M2 r/r % (przesunięte +18 m)")
    ax2.plot(cpi.index, _yoy(m["bank_loans_realestate"]), color="#27ae60", lw=1.8,
             label="hipoteki r/r %")
    ax2.plot(cpi.index, _yoy(m["fed_treasuries"]).shift(18), color="#2980b9", lw=1.8, ls="--",
             label="dług państwa / Fed UST r/r % (+18 m)")
    ax2.axhline(0, color="black", lw=0.6)
    ax2.set_ylim(-15, 35)
    ax2.set_title("Dynamika składników vs inflacja (wyprzedzające przesunięte o 18 m)",
                  fontweight="bold")
    ax2.set_ylabel("% r/r"); ax2.set_xlabel("rok")
    ax2.legend(fontsize=8.5, loc="upper left"); ax2.grid(True, alpha=0.25)

    fig.suptitle("Czy inflacja trzyma się pieniądza INNEGO niż hipoteczny?",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p = FIGURES_DIR / "37_inflacja_vs_skladniki.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return p


def asset_vs_consumer(monthly: pd.DataFrame) -> tuple[pd.DataFrame, Path]:
    """Test docelowy: kredyt hipoteczny napędza CENY DOMÓW czy CPI?

    Wymaga kolumny 'house_prices_us' (Case-Shiller). Zwraca tabelę
    korelacji i ścieżkę wykresu.
    """
    import matplotlib.pyplot as plt
    m = monthly
    if "house_prices_us" not in m.columns:
        raise KeyError("Brak 'house_prices_us' — uruchom download + harmonize.")

    cpi = _yoy(m["CPI_USA"])
    hpi = _yoy(m["house_prices_us"])
    # Lepsza miara hipotek, jeśli dostępna
    mort_col = "mortgage_debt_total" if "mortgage_debt_total" in m.columns else "bank_loans_realestate"
    # Współbieżnie (lag 0) — najmniej naciągana statystyka
    rows = {}
    for name, col in [("hipoteki (cały dług)", mort_col),
                      ("M2 (cały)", "M2_USA"),
                      ("dług państwa (Fed UST)", "fed_treasuries")]:
        g = _yoy(m[col])
        rows[name] = {"z_CPI": g.corr(cpi), "z_cenami_domów": g.corr(hpi)}
    table = pd.DataFrame(rows).T

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9.5))
    # Panel 1: funkcja korelacji krzyżowej dla hipotek (lag<0: hipoteki za,
    # lag>0: hipoteki wyprzedzają)
    sym = list(range(-24, 25, 2))
    mort = _yoy(m[mort_col])
    cc_cpi = [mort.shift(l).corr(cpi) for l in sym]
    cc_hpi = [mort.shift(l).corr(hpi) for l in sym]
    ax1.plot(sym, cc_hpi, color="#e67e22", lw=2.5, marker="o", ms=3, label="hipoteki ↔ ceny domów")
    ax1.plot(sym, cc_cpi, color="#2c3e50", lw=2.5, marker="o", ms=3, label="hipoteki ↔ CPI")
    ax1.axhline(0, color="black", lw=0.8); ax1.axvline(0, color="gray", lw=0.8, ls=":")
    ax1.set_title("Funkcja korelacji krzyżowej dynamiki kredytu hipotecznego\n"
                  "(lag>0: hipoteki wyprzedzają)", fontweight="bold")
    ax1.set_xlabel("opóźnienie [miesiące]"); ax1.set_ylabel("korelacja")
    ax1.legend(fontsize=9); ax1.grid(True, alpha=0.25)

    ax2.plot(cpi.index, cpi, color="#2c3e50", lw=2.5, label="CPI USA r/r %")
    ax2.plot(hpi.index, hpi, color="#e67e22", lw=2.5, label="ceny domów r/r %")
    ax2.plot(cpi.index, _yoy(m["bank_loans_realestate"]), color="#27ae60", lw=1.8, label="hipoteki r/r %")
    ax2.axhline(0, color="black", lw=0.6)
    ax2.set_title("Kredyt hipoteczny vs ceny domów vs CPI", fontweight="bold")
    ax2.set_ylabel("% r/r"); ax2.set_xlabel("rok")
    ax2.legend(fontsize=9, loc="upper left"); ax2.grid(True, alpha=0.25)

    fig.suptitle("Hipoteka: inflacja aktywów (domy) czy inflacja konsumencka (CPI)?",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p = FIGURES_DIR / "38_hipoteka_domy_vs_cpi.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    return table, p


def housing_supply(monthly: pd.DataFrame) -> tuple[pd.DataFrame, Path]:
    """Wpływ podaży nowych domów na hipoteki i ceny domów.

    Logika autora: więcej nowych domów -> szersza baza dla hipotek ->
    większa kreacja pieniądza hipotecznego. Sprawdzamy łańcuch:
    podaż nowych domów -> dług hipoteczny -> ceny domów.
    """
    import matplotlib.pyplot as plt
    m = monthly
    need = ["housing_starts", "mortgage_debt_total", "house_prices_us"]
    miss = [c for c in need if c not in m.columns]
    if miss:
        raise KeyError(f"Brak kolumn: {miss} — uruchom download + harmonize.")

    starts = _yoy(m["housing_starts"])
    mort = _yoy(m["mortgage_debt_total"])
    hpi = _yoy(m["house_prices_us"])

    # korelacje łańcucha przy najlepszym (dodatnim) wyprzedzeniu
    def best_pos(a, b):
        cands = {l: a.shift(l).corr(b) for l in range(0, 37, 3)}
        bl = max(cands, key=lambda l: cands[l]); return bl, cands[bl]
    l1, c1 = best_pos(starts, mort)      # podaż -> hipoteki
    l2, c2 = best_pos(mort, hpi)         # hipoteki -> ceny
    l3, c3 = best_pos(starts, hpi)       # podaż -> ceny (oczek. ujemne/słabe)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9.5))
    ax1.plot(starts.index, starts, color="#16a085", lw=1.8, label="nowe domy (starts) r/r %")
    ax1.plot(mort.index, mort, color="#8e44ad", lw=2.2, label="dług hipoteczny r/r %")
    ax1.plot(hpi.index, hpi, color="#e67e22", lw=2.2, label="ceny domów r/r %")
    ax1.axhline(0, color="black", lw=0.6)
    ax1.set_title("Łańcuch: podaż nowych domów → dług hipoteczny → ceny domów",
                  fontweight="bold")
    ax1.set_ylabel("% r/r"); ax1.legend(fontsize=8.5, loc="upper left"); ax1.grid(True, alpha=0.25)

    # poziom podaży nowych domów (kontekst cyklu budowlanego)
    ax2.plot(m.index, m["housing_starts"], color="#16a085", lw=1.8, label="rozpoczęcia budów (tys.)")
    if "new_houses_for_sale" in m.columns:
        ax2b = ax2.twinx()
        ax2b.plot(m.index, m["new_houses_for_sale"], color="#c0392b", lw=1.5, ls="--",
                  label="nowe domy na sprzedaż (tys.)")
        ax2b.set_ylabel("na sprzedaż (tys.)", color="#c0392b")
    ax2.set_title("Poziom podaży nowych domów", fontweight="bold")
    ax2.set_ylabel("rozpoczęcia (tys. SAAR)"); ax2.set_xlabel("rok"); ax2.grid(True, alpha=0.25)
    ax2.legend(fontsize=8.5, loc="upper left")

    txt = (f"podaż→hipoteki: {c1:+.2f} (lag {l1}m)\n"
           f"hipoteki→ceny: {c2:+.2f} (lag {l2}m)\n"
           f"podaż→ceny:    {c3:+.2f} (lag {l3}m)")
    ax1.text(0.99, 0.97, txt, transform=ax1.transAxes, ha="right", va="top", fontsize=9,
             bbox=dict(boxstyle="round", fc="#f7f7f7", ec="#cccccc"))

    fig.suptitle("Podaż nowych domów a kanał hipoteczny", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p = FIGURES_DIR / "39_podaz_domow_hipoteki.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    res = pd.DataFrame({"para": ["podaż→hipoteki", "hipoteki→ceny", "podaż→ceny"],
                        "korelacja": [c1, c2, c3], "lag_m": [l1, l2, l3]})
    return res, p


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    table, best = analyse(monthly)
    table.round(3).to_csv(PROCESSED_DIR / "inflacja_vs_skladniki.csv")
    p = plot(monthly, table)
    print("Najlepsza korelacja z inflacją (|max|):")
    for n in table.sort_values("best_corr", ascending=False).index:
        print(f"  {n:32} {table.loc[n,'best_corr']:+.2f} @ {int(table.loc[n,'best_lag_m'])}m")
    print("wykres:", p.name)

    if "house_prices_us" in monthly.columns:
        t2, p2 = asset_vs_consumer(monthly)
        print("\nHipoteka/M2/dług — korelacja WSPÓŁBIEŻNA z CPI vs z cenami domów:")
        print(t2.round(2).to_string())
        print("wykres:", p2.name)
    else:
        print("\n[!] Brak 'house_prices_us' — uruchom: python -m src.download && python -m src.harmonize")

    if "housing_starts" in monthly.columns and "mortgage_debt_total" in monthly.columns:
        t3, p3 = housing_supply(monthly)
        print("\nŁańcuch podaż domów → hipoteki → ceny:")
        print(t3.round(2).to_string(index=False))
        print("wykres:", p3.name)
    else:
        print("\n[!] Brak serii podaży/długu hipotecznego — pobierz nowe serie.")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
