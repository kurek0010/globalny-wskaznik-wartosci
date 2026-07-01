"""Analiza v0.4 — komplet obliczeń i wykresów (kroki 1-3, dane pobrane).

1. AUV-T: wariant mianownika "dochód na pracownika" vs "na osobę".
2. Jakość pieniądza: skład kolateralu Fed (H.4.1) i kredytu banków (H.8),
   syntetyczny indeks jakości Q (wagi ILUSTRACYJNE — patrz uwagi).
3. Zależność poboczna: inflacja vs podaż pieniądza vs skład kolateralu.

Uruchamianie:  python -m src.analysis_v4
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import (
    BASE_YEAR, INCOME_NUM, INCOME_DEN, PROCESSED_DIR, FIGURES_DIR,
    _annual, _index_to_base, compute,
)

# Wagi jakości kolateralu — ILUSTRACYJNE, do analizy wrażliwości.
# Ujęcie: kredyt produktywny (biznes) najwyżej, realne aktywa (hipoteki/
# MBS) pośrednio, dług suwerenny i konsumpcja nisko. Stanowisko sporne —
# patrz FDI_indeks_jakosci_pieniadza.md, sekcja 5.
W_BANK = {"bank_loans_business": 1.0, "bank_loans_realestate": 0.7, "bank_loans_consumer": 0.3}
W_FED = {"fed_mbs": 0.7, "fed_treasuries": 0.2}


# ---------------------------------------------------------------------
# KROK 1 — mianownik na pracownika
# ---------------------------------------------------------------------
def auv_denominator_variants(monthly: pd.DataFrame) -> pd.DataFrame:
    a = _annual(monthly)
    base = compute(monthly)
    out = pd.DataFrame(index=base.index)
    out["AUV_T_na_osobe"] = base["AUV_T"]
    basket = base["koszyk_nominalny"]
    inc_worker = _index_to_base(a[INCOME_NUM] / a["labor_force_world"])
    out["AUV_T_na_pracownika"] = basket / inc_worker * 100.0
    out["dochod_na_osobe"] = base["dochod_glob_per_capita"]
    out["dochod_na_pracownika"] = inc_worker
    return out


# ---------------------------------------------------------------------
# KROK 3 — jakość pieniądza
# ---------------------------------------------------------------------
def money_quality(monthly: pd.DataFrame) -> pd.DataFrame:
    a = _annual(monthly)
    out = pd.DataFrame(index=a.index)

    # Skład kredytu banków komercyjnych (udziały w sumie 3 typów kredytu)
    bank_cols = list(W_BANK)
    bsum = a[bank_cols].sum(axis=1)
    for c in bank_cols:
        out[f"udzial_{c}"] = a[c] / bsum
    out["Q_banki"] = sum(W_BANK[c] * (a[c] / bsum) for c in bank_cols)

    # Skład bilansu Fed (udziały UST vs MBS w ich sumie)
    fed_cols = list(W_FED)
    fsum = a[fed_cols].sum(axis=1)
    for c in fed_cols:
        out[f"udzial_{c}"] = a[c] / fsum
    out["Q_fed"] = sum(W_FED[c] * (a[c] / fsum) for c in fed_cols)
    out["fed_total_assets"] = a["fed_total_assets"]

    # Kontekst monetarny i inflacja
    out["M2_USA"] = a["M2_USA"]
    out["CPI_USA"] = a["CPI_USA"]
    out["M2_yoy"] = a["M2_USA"].pct_change() * 100
    out["CPI_yoy"] = a["CPI_USA"].pct_change() * 100
    return out


# ---------------------------------------------------------------------
# Wykresy
# ---------------------------------------------------------------------
def plot_denominator(d: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.plot(d.index, d["AUV_T_na_osobe"], color="#16a085", lw=2.5, label="AUV-T / dochód na osobę")
    ax.plot(d.index, d["AUV_T_na_pracownika"], color="#8e44ad", lw=2.5, ls="--",
            label="AUV-T / dochód na pracownika")
    ax.axhline(100, color="black", lw=0.6, alpha=0.4)
    ax.set_title("Krok 1: AUV-T przy dwóch mianownikach (cena pracy)", fontweight="bold")
    ax.set_ylabel(f"indeks ({BASE_YEAR} = 100)"); ax.set_xlabel("rok")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.25)
    fig.tight_layout()
    p = FIGURES_DIR / "34_auv_t_mianowniki.png"; fig.savefig(p, dpi=130); plt.close(fig); return p


def plot_collateral(q: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Banki — udziały kredytu
    re = q["udzial_bank_loans_realestate"] * 100
    bu = q["udzial_bank_loans_business"] * 100
    co = q["udzial_bank_loans_consumer"] * 100
    ax1.stackplot(q.index, re, bu, co,
                  labels=["nieruchomości", "biznes (produktywny)", "konsumpcja"],
                  colors=["#e67e22", "#27ae60", "#c0392b"], alpha=0.85)
    ax1.set_title("Skład kredytu banków komercyjnych (H.8)", fontweight="bold")
    ax1.set_ylabel("% sumy trzech typów kredytu"); ax1.set_xlabel("rok")
    ax1.set_ylim(0, 100); ax1.legend(fontsize=8, loc="lower left"); ax1.margins(x=0)

    # Fed — udziały aktywów
    fq = q.dropna(subset=["udzial_fed_treasuries"])
    tr = fq["udzial_fed_treasuries"] * 100
    mb = fq["udzial_fed_mbs"] * 100
    ax2.stackplot(fq.index, tr, mb,
                  labels=["obligacje skarbowe (suwerenny)", "MBS (realny)"],
                  colors=["#2980b9", "#e67e22"], alpha=0.85)
    ax2.set_title("Skład bilansu Fed (H.4.1, od 2003)", fontweight="bold")
    ax2.set_ylabel("% sumy UST+MBS"); ax2.set_xlabel("rok")
    ax2.set_ylim(0, 100); ax2.legend(fontsize=8, loc="lower left"); ax2.margins(x=0)

    fig.suptitle("Krok 3: PRZECIWKO czemu kreowany jest pieniądz — skład kolateralu",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    p = FIGURES_DIR / "35_kolateral_sklad.png"; fig.savefig(p, dpi=130); plt.close(fig); return p


def plot_inflation_money_collateral(q: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    ax1.bar(q.index, q["M2_yoy"], color="#c0392b", alpha=0.5, label="M2 USA r/r %")
    ax1.plot(q.index, q["CPI_yoy"], color="#2c3e50", lw=2.5, label="CPI USA r/r %")
    ax1.axhline(0, color="black", lw=0.6)
    ax1.set_title("Podaż pieniądza vs inflacja", fontweight="bold")
    ax1.set_ylabel("% r/r"); ax1.legend(fontsize=9); ax1.grid(True, alpha=0.25)

    ax2.plot(q.index, q["Q_banki"], color="#16a085", lw=2.5, label="Q banki (jakość kredytu)")
    ax2.plot(q.index, q["Q_fed"], color="#2980b9", lw=2.5, ls="--", label="Q Fed (jakość aktywów)")
    ax2.set_title("Jakość kolateralu (wyżej = więcej realnego/produktywnego; wagi ilustracyjne)",
                  fontweight="bold")
    ax2.set_ylabel("indeks Q [0-1]"); ax2.legend(fontsize=9); ax2.grid(True, alpha=0.25)

    ax3.plot(q.index, q["udzial_fed_treasuries"] * 100, color="#2980b9", lw=2.5,
             label="udział obligacji skarbowych w bilansie Fed %")
    ax3.plot(q.index, q["udzial_bank_loans_business"] * 100, color="#27ae60", lw=2.5,
             label="udział kredytu produktywnego (biznes) %")
    ax3.set_title("Wybrane udziały kolateralu", fontweight="bold")
    ax3.set_ylabel("%"); ax3.set_xlabel("rok"); ax3.legend(fontsize=9); ax3.grid(True, alpha=0.25)

    fig.suptitle("Pobocznie: inflacja a podaż pieniądza względem składu zabezpieczeń",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    p = FIGURES_DIR / "36_inflacja_podaz_kolateral.png"; fig.savefig(p, dpi=130); plt.close(fig); return p


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    d = auv_denominator_variants(monthly)
    q = money_quality(monthly)
    d.round(3).to_csv(PROCESSED_DIR / "auv_t_mianowniki.csv")
    q.round(4).to_csv(PROCESSED_DIR / "money_quality.csv")
    f1 = plot_denominator(d); f2 = plot_collateral(q); f3 = plot_inflation_money_collateral(q)

    print("=== KROK 1: mianowniki ===")
    print("  AUV-T na osobe     2025=%.1f (%+.1f%%)" % (d["AUV_T_na_osobe"].iloc[-1], d["AUV_T_na_osobe"].iloc[-1]-100))
    print("  AUV-T na pracownika 2025=%.1f (%+.1f%%)" % (d["AUV_T_na_pracownika"].iloc[-1], d["AUV_T_na_pracownika"].iloc[-1]-100))
    print("=== KROK 3: jakość pieniądza (2025) ===")
    print("  kredyt: nieruchomości=%.0f%% biznes=%.0f%% konsumpcja=%.0f%%" % (
        q["udzial_bank_loans_realestate"].iloc[-1]*100, q["udzial_bank_loans_business"].iloc[-1]*100, q["udzial_bank_loans_consumer"].iloc[-1]*100))
    print("  Fed: obligacje=%.0f%% MBS=%.0f%%" % (q["udzial_fed_treasuries"].iloc[-1]*100, q["udzial_fed_mbs"].iloc[-1]*100))
    print("  Q_banki=%.2f  Q_fed=%.2f" % (q["Q_banki"].iloc[-1], q["Q_fed"].iloc[-1]))
    # prosty test wyprzedzania: korelacja Q_banki(t-k) z CPI_yoy(t)
    print("=== test: czy spadek jakości kredytu wyprzedza inflację? ===")
    for k in [0,1,2,3]:
        c = q["Q_banki"].shift(k).corr(q["CPI_yoy"])
        print(f"  corr(Q_banki[t-{k}], CPI_yoy[t]) = {c:+.2f}")
    print("wykresy:", f1.name, f2.name, f3.name)


if __name__ == "__main__":
    main()
