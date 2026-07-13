"""Miesieczna aktualizacja kotwic TLN-PLN wg REGULA + POLITYKA_danych.

PIERWSZA PUBLIKACJA: 2026-07-08. Wartosci sprzed tej daty byly robocze
(prototyp; ogon 2025 zawieral artefakt ffill) i zostaly jednorazowo
przeliczone z danych first-print GUS. OD TEJ PUBLIKACJI obowiazuje zakaz
rewizji wstecz: kolejne uruchomienia moga TYLKO dopisywac nowe miesiace
(skrypt odmowi nadpisania istniejacych wartosci) - to pilnuje
talent_published.json.

Od automatyzacji (fetch_gus.py): CPI_MM i WAGE_ANNUAL nie sa juz wpisywane
recznie w tym pliku - skrypt czyta je z prototyp/data/first_prints_pln.json
(ktory dopisuje fetch_gus.py, append-only). Logika obliczen (srodek
geometryczny, interpolacja log-liniowa nogi placowej, format
talent_anchors.csv/json, mechanizm talent_published.json) jest DOKLADNIE
taka sama jak przed refaktoryzacja - zmienilo sie tylko zrodlo slownikow.

Kaskada awaryjna (POLITYKA_danych_v0.1.md §4.1-2): miesiac, dla ktorego wg
kalendarza (REGULA §2 / POLITYKA §2: kotwica 25. dnia m+1 dla miesiaca m)
powinna juz istniec kotwica, ale fetcher nie dostarczyl CPI - dostaje
dynamike z ostatniej dostepnej publikacji (carry-forward) + alert. Jesli
brakuje danych dla >=2 kolejnych oczekiwanych miesiecy, skrypt PRZERYWA bez
zadnej publikacji w tym uruchomieniu (transakcyjnie) - eskalacja do
czlowieka, zgodnie z POLITYKA §4.2.
"""
from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"
FIRST_PRINTS = ROOT / "data" / "first_prints_pln.json"

FIRST_PUBLICATION = "2025-04"  # od tego miesiaca ta sciezka jest kanoniczna


def load_first_prints() -> tuple[dict[str, float], dict[int, float], set[int]]:
    raw = json.loads(FIRST_PRINTS.read_text(encoding="utf-8"))
    cpi_mm = {m: float(v["value"]) for m, v in raw.get("cpi_mm", {}).items()}
    wage_raw = raw.get("wage_annual", {})
    wage_annual = {int(y): float(v["value"]) for y, v in wage_raw.items()}
    proxy_years = {int(y) for y, v in wage_raw.items() if v.get("proxy")}
    return cpi_mm, wage_annual, proxy_years


def expected_anchor_month(today: date | None = None) -> pd.Period:
    """Miesiac m, dla ktorego kotwica A(m) powinna juz byc obliczona wg
    kadencji REGULA §2 / POLITYKA §2: 25. dnia miesiaca m+1 publikujemy A(m).
    Uzywane WYLACZNIE do wykrywania brakow (kaskada) - samo przetwarzanie
    idzie po danych faktycznie dostepnych w first_prints_pln.json."""
    today = today or date.today()
    cur = pd.Period(f"{today.year}-{today.month:02d}", "M")
    return cur - 1 if today.day >= 25 else cur - 2


def main() -> None:
    cpi_mm, wage_annual, proxy_years = load_first_prints()

    a = pd.read_csv(OUT / "talent_anchors.csv", index_col=0)
    a.index = pd.PeriodIndex(a.index, freq="M")

    start = pd.Period(FIRST_PUBLICATION, "M")
    if str(start) not in cpi_mm:
        raise SystemExit("Brak danych CPI dla miesiaca startowego w first_prints_pln.json")

    pub_file = OUT / "talent_published.json"
    published = set(json.load(open(pub_file))) if pub_file.exists() else set()

    last_published = max((pd.Period(m, "M") for m in published), default=start - 1)
    target = expected_anchor_month()

    if target <= last_published:
        print(f"Brak nowych miesiecy do publikacji (ostatnia kotwica: {last_published}, "
              f"oczekiwana wg kalendarza: {target}).")
        return

    # noga plac: interpolacja log-liniowa punktow lipcowych, baza = I_w(2024-07)
    base_p = pd.Period("2024-07", "M")
    base_iw = float(a.loc[base_p, "I_w"])
    pts = {pd.Period(f"{y}-07", "M"): math.log(v) for y, v in wage_annual.items()}
    rng = pd.period_range(min(pts), max(pts), freq="M")
    wage = pd.Series(pts).reindex(rng).interpolate().apply(math.exp)
    wage = wage / wage[base_p]  # wzgledem bazy

    ic, iw = float(a.loc[last_published, "I_c"]), float(a.loc[last_published, "I_w"])
    last_A = float(a.loc[last_published, "A"])
    last_dynamic = cpi_mm.get(str(last_published), 100.0) / 100.0  # fallback: brak zmiany

    rows: list[tuple] = []
    alerts: list[str] = []
    consecutive_missing = 0
    m = last_published + 1
    while m <= target:
        key = str(m)
        if key in cpi_mm:
            dyn = cpi_mm[key] / 100.0
            consecutive_missing = 0
            last_dynamic = dyn
        else:
            consecutive_missing += 1
            if consecutive_missing >= 2:
                raise SystemExit(
                    f"BLAD: brak danych CPI za {consecutive_missing} kolejne "
                    f"oczekiwane miesiace (do {m} wlacznie) - kaskada awaryjna "
                    "wyczerpana (POLITYKA_danych_v0.1.md §4.2). Przerywam BEZ "
                    "publikacji zadnego miesiaca w tym uruchomieniu - eskalacja "
                    "do czlowieka."
                )
            dyn = last_dynamic
            alerts.append(
                f"ALERT: brak CPI za {m} w first_prints_pln.json - zastosowano "
                f"carry-forward ostatniej znanej dynamiki ({100*dyn:.2f} = "
                "poprzedni miesiac, POLITYKA §4.1)."
            )

        ic *= dyn
        iw = base_iw * float(wage[m]) if m in wage.index else iw  # carry-fwd
        A = math.sqrt(ic * iw)
        g = A / (rows[-1][3] if rows else last_A)
        rows.append((m, ic, iw, A, g))
        a.loc[m] = {"I_c": round(ic, 3), "I_w": round(iw, 3),
                    "A": round(A, 3), "g": round(g, 5),
                    "tryb_awaryjny": abs(g - 1) > 0.15}
        m += 1

    a = a.sort_index()
    a.to_csv(OUT / "talent_anchors.csv")
    json.dump({str(p): round(v, 3) for p, v in a["A"].items()},
              open(OUT / "talent_anchors.json", "w"))
    json.dump(sorted(published | {str(r[0]) for r in rows}), open(pub_file, "w"), indent=1)

    lastm, _, _, lastA, lastg = rows[-1]
    print(f"Opublikowano {len(rows)} kotwic: {rows[0][0]} .. {lastm}")
    print(f"Kotwica przed: {last_published} = {last_A:.3f}")
    print(f"Kotwica po:    {lastm} = {lastA:.3f} (m/m {100*(lastg-1):+.2f}%)")
    for al in alerts:
        print(al)
    if abs(lastg - 1) > 0.02:
        print(f"SANITY: |m/m| = {100*abs(lastg-1):.2f}% > 2% przy obecnej inflacji - sprawdz recznie sensownosc.")
    processed_years = {r[0].year for r in rows}
    for y in sorted(proxy_years & processed_years):
        print(f"ALERT: placa roczna {y} w first_prints_pln.json to PROXY - "
              "do zastapienia komunikatem GN, gdy sie ukaze.")
    print("Nastepnie uruchom: python src/build_strona.py")


if __name__ == "__main__":
    main()
