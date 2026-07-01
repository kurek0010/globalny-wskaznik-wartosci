"""AUV-T v0.4 — eksperymenty badawcze (kroki 1-2).

Krok 1: dekompozycja AUV-T na trend (rdzeń kontraktowy) i cykl
        (wskaźnik napięcia zasobowego).
Krok 2: koszyk ważony ZAPOTRZEBOWANIEM per capita — koszt zaspokojenia
        potrzeb jednego człowieka, w jednostkach czasu pracy. Dwa warianty:
          * "przetrwanie" (R sta" = ilość zamrożona w roku bazowym),
          * "standard"   (R(t) = rzeczywista konsumpcja per capita).
        Różnica między nimi izoluje wpływ rosnącej konsumpcji na osobę.

Liczone na danych już zebranych. Pełna wersja kroku 2 (metale,
budownictwo) wymaga ilości konsumpcji per capita, których jeszcze nie
mamy — patrz uwagi w kodzie.

Uruchamianie:
    python -m src.auv_research
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .auv_t import (
    BASE_YEAR, CATEGORIES, INCOME_NUM, INCOME_DEN,
    PROCESSED_DIR, FIGURES_DIR,
    _annual, _index_to_base, _geom_mean, compute,
)


# =====================================================================
# KROK 1 — dekompozycja trend / cykl
# =====================================================================

TREND_WINDOW = 7  # lat; krocząca (przyczynowa) — nadaje się do kontraktów


def decompose(auv: pd.Series) -> pd.DataFrame:
    """Rozłóż AUV-T (log-addytywnie) na trend kroczący i cykl.

    trend(t)  = exp(śr. krocząca ln AUV po TREND_WINDOW latach)   [rdzeń]
    cykl(t)   = AUV(t) / trend(t) * 100                            [odchylenie]
    """
    log = np.log(auv)
    trend = np.exp(log.rolling(TREND_WINDOW, min_periods=1).mean())
    cycle = auv / trend * 100.0
    return pd.DataFrame({"AUV_T": auv, "trend": trend, "cykl": cycle})


# =====================================================================
# KROK 2 — koszyk ważony zapotrzebowaniem per capita
# =====================================================================

# Mapowanie kategorii -> lista serii ILOŚCI (proxy R_i). Każda kategoria
# może mieć kilka serii (uśrednianych geometrycznie po per-capita). Serie
# nieobecne w danych są pomijane; jeśli kategoria nie ma ŻADNEJ -> R stałe.
# Metale i budownictwo zasilają się z data/manual/manual_production.csv —
# dopóki pusty, te kategorie działają na stałym R.
NEED_PROXY: dict[str, list[str]] = {
    "energia": ["energy_use_per_capita"],
    "zywnosc": ["food_production_index"],
    "metale": ["copper_production_world", "aluminum_production_world",
               "iron_ore_production_world", "nickel_production_world",
               "zinc_production_world"],
    "budownictwo": ["steel_production_world", "cement_production_world"],
}
# Serie już wyrażone per capita (nie dzielimy ich przez populację):
PER_CAPITA_ALREADY = {"energy_use_per_capita", "electric_power_consumption_per_capita"}


def _category_price(a: pd.DataFrame, cat: str) -> pd.Series:
    cols = CATEGORIES[cat]
    return _geom_mean(pd.concat([_index_to_base(a[c]) for c in cols], axis=1))


def needs_weighted(monthly: pd.DataFrame) -> pd.DataFrame:
    """Koszt zaspokojenia potrzeb 1 osoby w jednostkach czasu pracy.

    Dla kategorii c z dostępnym proxy ilości:
        koszt_pc_c(t) = cena_c(t) * ilosc_pc_c(t)          [wariant standard]
        koszt_pc_c(t) = cena_c(t) * ilosc_pc_c(t0)         [wariant przetrwanie]
    Następnie AUV_potrzeby = koszt_pc / dochod_pc * 100.
    """
    a = _annual(monthly)
    income_pc = _index_to_base(a[INCOME_NUM] / a[INCOME_DEN])
    pop = a[INCOME_DEN]

    out = pd.DataFrame(index=a.index)
    out["dochod_pc"] = income_pc

    std_cost = {}
    srv_cost = {}
    for cat, qty_cols in NEED_PROXY.items():
        price = _category_price(a, cat)
        avail = [c for c in qty_cols if c in a.columns and a[c].notna().any()]
        if not avail:
            # Brak danych ilości -> R stałe = 100 (kategoria wchodzi ceną)
            qty_pc_idx = pd.Series(100.0, index=a.index)
            out[f"R_dynamiczne_{cat}"] = False
        else:
            parts = []
            for c in avail:
                q = a[c] if c in PER_CAPITA_ALREADY else a[c] / pop
                parts.append(_index_to_base(q.ffill()))
            qty_pc_idx = _geom_mean(pd.concat(parts, axis=1))
            out[f"R_dynamiczne_{cat}"] = True
        std_cost[cat] = price * qty_pc_idx / 100.0          # standard: R(t)
        srv_cost[cat] = price * qty_pc_idx.loc[BASE_YEAR] / 100.0  # przetrwanie: R(t0)
        out[f"cena_{cat}"] = price
        out[f"ilosc_pc_{cat}"] = qty_pc_idx

    # Koszyk = średnia geometryczna kosztów kategorii (równe wagi kategorii)
    std = _geom_mean(pd.concat(std_cost.values(), axis=1))
    srv = _geom_mean(pd.concat(srv_cost.values(), axis=1))
    out["AUV_potrzeby_standard"] = _index_to_base(std / income_pc)
    out["AUV_potrzeby_przetrwanie"] = _index_to_base(srv / income_pc)
    return out


# =====================================================================
# Wykresy
# =====================================================================

def plot_decompose(dec: pd.DataFrame) -> Path:
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.plot(dec.index, dec["AUV_T"], color="#bdc3c7", lw=1.5, label="AUV-T (surowe)")
    ax1.plot(dec.index, dec["trend"], color="#16a085", lw=3,
             label=f"Trend = rdzeń ({TREND_WINDOW}-letni, przyczynowy)")
    ax1.axhline(100, color="black", lw=0.6, alpha=0.4)
    ax1.set_title("Krok 1: rozkład AUV-T na trend (rdzeń kontraktowy) i cykl", fontweight="bold")
    ax1.set_ylabel(f"indeks ({BASE_YEAR} = 100)")
    ax1.legend(fontsize=9, loc="upper left"); ax1.grid(True, alpha=0.25)

    ax2.axhline(100, color="black", lw=0.8)
    ax2.fill_between(dec.index, 100, dec["cykl"], where=dec["cykl"] >= 100,
                     color="#c0392b", alpha=0.35, label="napięcie (drogo)")
    ax2.fill_between(dec.index, 100, dec["cykl"], where=dec["cykl"] < 100,
                     color="#2980b9", alpha=0.35, label="obfitość (tanio)")
    ax2.plot(dec.index, dec["cykl"], color="#2c3e50", lw=1.5)
    ax2.set_title("Cykl = wskaźnik napięcia zasobowego (AUV-T / trend)", fontweight="bold")
    ax2.set_ylabel("odchylenie (100 = neutralnie)")
    ax2.set_xlabel("rok"); ax2.legend(fontsize=8, loc="upper left"); ax2.grid(True, alpha=0.25)
    fig.tight_layout()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / "32_auv_t_trend_cykl.png"
    fig.savefig(path, dpi=130); plt.close(fig)
    return path


def plot_needs(nw: pd.DataFrame, auv_equal: pd.Series) -> Path:
    import matplotlib.pyplot as plt
    dyn = [c.replace("R_dynamiczne_", "") for c in nw.columns
           if c.startswith("R_dynamiczne_") and bool(nw[c].iloc[-1])]
    stat = [c.replace("R_dynamiczne_", "") for c in nw.columns
            if c.startswith("R_dynamiczne_") and not bool(nw[c].iloc[-1])]
    subtitle = f"R dynamiczne: {', '.join(dyn) or '—'}; R stałe: {', '.join(stat) or '—'}"
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(nw.index, auv_equal, color="#7f8c8d", lw=1.8, ls=":",
            label="AUV-T (wagi równe, bez potrzeb)")
    ax.plot(nw.index, nw["AUV_potrzeby_przetrwanie"], color="#2980b9", lw=2.5,
            label="AUV potrzeby — przetrwanie (R sta" + "e)")
    ax.plot(nw.index, nw["AUV_potrzeby_standard"], color="#c0392b", lw=2.5,
            label="AUV potrzeby — standard (R rośnie z konsumpcją)")
    ax.axhline(100, color="black", lw=0.6, alpha=0.4)
    ax.set_title("Krok 2: koszt zaspokojenia potrzeb 1 osoby w czasie pracy\n"
                 f"({len(dyn)+len(stat)} kategorie; {subtitle})", fontweight="bold")
    ax.set_ylabel(f"indeks ({BASE_YEAR} = 100)")
    ax.set_xlabel("rok")
    ax.legend(fontsize=9, loc="upper left"); ax.grid(True, alpha=0.25)
    ax.text(0.99, 0.02,
            "Odstęp standard - przetrwanie = wpływ rosnącej konsumpcji na osobę.",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5,
            bbox=dict(boxstyle="round", fc="#f7f7f7", ec="#cccccc"))
    fig.tight_layout()
    path = FIGURES_DIR / "33_auv_potrzeby.png"
    fig.savefig(path, dpi=130); plt.close(fig)
    return path


def main() -> None:
    monthly = pd.read_parquet(PROCESSED_DIR / "monthly.parquet")
    base = compute(monthly)
    auv = base["AUV_T"]

    dec = decompose(auv)
    nw = needs_weighted(monthly)

    dec.round(3).to_csv(PROCESSED_DIR / "auv_t_trend_cykl.csv")
    nw.round(3).to_csv(PROCESSED_DIR / "auv_potrzeby.csv")
    f1 = plot_decompose(dec)
    f2 = plot_needs(nw, auv)

    print("=== KROK 1: trend / cykl ===")
    print("  zmienność surowa (std log d):", round(np.log(dec['AUV_T']).diff().std(), 3))
    print("  zmienność trendu (std log d):", round(np.log(dec['trend']).diff().std(), 3))
    print("  amplituda cyklu: min=%.0f max=%.0f" % (dec['cykl'].min(), dec['cykl'].max()))
    print("  wykres:", f1)
    print("=== KROK 2: potrzeby ===")
    for c in ["AUV_potrzeby_przetrwanie", "AUV_potrzeby_standard"]:
        print("  %-28s 2025=%.1f  (zmiana %+.1f%%)" % (c, nw[c].iloc[-1], nw[c].iloc[-1] - 100))
    print("  wykres:", f2)


if __name__ == "__main__":
    main()
