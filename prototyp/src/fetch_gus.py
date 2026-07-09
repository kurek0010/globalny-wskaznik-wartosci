"""Fetcher first-printow GUS zasilajacy kotwice TLN-PLN (append-only).

WYBOR ZRODLA CPI m/m (zbadane 2026-07-09, w kolejnosci preferencji z
INSTRUKCJA_aktualizacji.md):

1. API GUS DBW (api-dbw.stat.gov.pl) - odrzucone: endpoint danych zwraca 404,
   nie znaleziono publicznego "cube" z miesiecznym CPI m/m dla Polski ogolem.
2. API BDL (bdl.stat.gov.pl) - odrzucone: dzial CENY / WSKAZNIKI CEN (grupa
   G405) publikuje wylacznie czestotliwosc kwartalna i roczna (pole
   "quarterly" w /api/v1/subjects/G405 przyjmuje tylko "K"/"R") - nie ma tam
   miesiecznego "poprzedni miesiac = 100", wiec nie nadaje sie do publikacji
   25. dnia kazdego miesiaca.
3. WYBRANE: tabela GUS "Miesieczne wskazniki cen towarow i uslug
   konsumpcyjnych od 1982 roku" pod stalym adresem CSV (patrz CPI_CSV_URL).
   Format: srednik jako separator, kodowanie cp1250 (polskie znaki), kolumna
   "Sposob prezentacji" == "Poprzedni miesiac = 100" to szukany m/m,
   przecinek jako separator dziesietny. To ten sam zestaw liczb, ktory byl
   dotad recznie przepisywany do CPI_MM w talent_update.py (wartosci sie
   zgadzaja co do przecinka).

PLACE ROCZNE (gospodarka narodowa, komunikat Prezesa GUS, ok. 9 lutego):
brak stabilnego, przewidywalnego adresu URL komunikatu (numer strony w
adresie zmienia sie co publikacje) - fetcher probuje best-effort znalezc
link na liscie komunikatow GUS i sparsowac wartosc; jesli sie nie uda,
WYLACZNIE raportuje potrzebe recznego wpisu do first_prints_pln.json
(wage_annual) - nigdy nie zgaduje liczby.

Zapis: prototyp/data/first_prints_pln.json, append-only - istniejace klucze
(miesiace CPI, lata plac) nigdy nie sa nadpisywane ani usuwane, zgodnie z
zakazem rewizji wstecz (REGULA_publikacyjna_Talent_v0.1.md §3).
"""
from __future__ import annotations

import csv
import io
import json
import re
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
FIRST_PRINTS = ROOT / "data" / "first_prints_pln.json"

CPI_CSV_URL = (
    "https://stat.gov.pl/download/gfx/portalinformacyjny/pl/"
    "defaultstronaopisowa/4741/1/1/"
    "miesiecznewskaznikicentowarowiuslugkonsumpcyjnychod1982roku_6.csv"
)
CPI_SOURCE_NAME = (
    'GUS, tabela "Miesięczne wskaźniki cen towarów i usług konsumpcyjnych '
    'od 1982 roku" (Poprzedni miesiąc = 100)'
)

GUS_KOMUNIKATY_LIST = (
    "https://stat.gov.pl/sygnalne/komunikaty-i-obwieszczenia/"
    "lista-komunikatow-i-obwieszczen/"
)
WAGE_LINK_RE = re.compile(
    r'href="([^"]*przeci[ei]tny?m?-wynagrodzeniu?-w-gospodarce-narodowej[^"]*\.html)"',
    re.IGNORECASE,
)
WAGE_VALUE_RE = re.compile(
    r"wynios[lł]o[^0-9]{0,40}([0-9]{1,2}\s?[0-9]{3},[0-9]{2})\s?z[lł]",
    re.IGNORECASE,
)
WAGE_YEAR_RE = re.compile(r"w\s+(\d{4})\s+roku")


def load_first_prints() -> dict:
    if FIRST_PRINTS.exists():
        return json.loads(FIRST_PRINTS.read_text(encoding="utf-8"))
    return {"cpi_mm": {}, "wage_annual": {}}


def save_first_prints(data: dict) -> None:
    FIRST_PRINTS.write_text(
        json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )


# Tabela GUS sięga do 1982 r., ale first_prints_pln.json zasila tylko biezaca
# publikacje kotwic (od FIRST_PUBLICATION w talent_update.py) - pelna historia
# jest juz w talent_anchors.csv z innych zrodel. Ograniczamy fetch do okna
# wystarczajaco szerokiego na kazda realna przerwe w publikacjach, bez
# zasmiecania pliku danymi sprzed lat.
LOOKBACK_MONTHS = 24


def fetch_cpi_mm() -> dict[str, float]:
    """Zwraca {"YYYY-MM": wartość} dla miesięcy z opublikowanym m/m w oknie
    ostatnich LOOKBACK_MONTHS miesięcy (kolumna "Poprzedni miesiąc = 100",
    jednostka terytorialna Polska)."""
    resp = requests.get(CPI_CSV_URL, timeout=30)
    resp.raise_for_status()
    text = resp.content.decode("cp1250")
    reader = csv.DictReader(io.StringIO(text), delimiter=";")

    today = date.today()
    cutoff = (today.year * 12 + today.month - 1) - LOOKBACK_MONTHS  # 0-based YYYYMM

    out: dict[str, float] = {}
    for row in reader:
        if row.get("Sposób prezentacji") != "Poprzedni miesiąc = 100":
            continue
        if row.get("Jednostka terytorialna") != "Polska":
            continue
        val = (row.get("Wartość") or "").strip()
        if not val:
            continue
        year, month = int(row["Rok"]), int(row["Miesiąc"])
        if year * 12 + month - 1 < cutoff:
            continue
        out[f"{year:04d}-{month:02d}"] = float(val.replace(",", "."))
    return out


def fetch_wage_annual_guess() -> tuple[int, float] | None:
    """Best-effort: szuka na liście komunikatów GUS ogłoszenia o przeciętnym
    wynagrodzeniu w gospodarce narodowej i próbuje wyłuskać wartość. Zwraca
    (rok, wartość) albo None, gdy się nie uda (wtedy wymagany ręczny wpis)."""
    try:
        resp = requests.get(GUS_KOMUNIKATY_LIST, timeout=30)
        resp.raise_for_status()
    except requests.RequestException:
        return None
    m = WAGE_LINK_RE.search(resp.text)
    if not m:
        return None
    url = m.group(1)
    if url.startswith("/"):
        url = "https://stat.gov.pl" + url
    try:
        page = requests.get(url, timeout=30)
        page.raise_for_status()
    except requests.RequestException:
        return None
    vm = WAGE_VALUE_RE.search(page.text)
    if not vm:
        return None
    value = float(vm.group(1).replace(" ", "").replace(",", "."))
    ym = WAGE_YEAR_RE.search(page.text)
    year = int(ym.group(1)) if ym else date.today().year - 1
    return year, value


def main() -> None:
    data = load_first_prints()
    data.setdefault("cpi_mm", {})
    data.setdefault("wage_annual", {})
    today = date.today().isoformat()
    report: list[str] = []

    # --- CPI m/m ---------------------------------------------------------
    try:
        cpi_all = fetch_cpi_mm()
    except Exception as exc:  # noqa: BLE001
        report.append(f"BŁĄD pobierania CPI z GUS: {exc}")
        cpi_all = {}

    new_cpi = 0
    for month, value in sorted(cpi_all.items()):
        if month in data["cpi_mm"]:
            continue  # append-only: nigdy nie nadpisujemy istniejącego miesiąca
        data["cpi_mm"][month] = {
            "value": value,
            "source": CPI_SOURCE_NAME,
            "fetched": today,
        }
        new_cpi += 1
        report.append(f"CPI {month}: {value} (nowy odczyt)")
    if new_cpi == 0 and not any("BŁĄD" in r for r in report):
        report.append("CPI: brak nowych miesięcy ponad już zapisane w first_prints_pln.json.")

    # --- płace roczne (gospodarka narodowa) -------------------------------
    prev_year = date.today().year - 1
    is_february = date.today().month == 2
    if str(prev_year) in data["wage_annual"]:
        pass  # już mamy - nic nie robimy (append-only)
    elif is_february:
        guess = fetch_wage_annual_guess()
        if guess:
            year, value = guess
            key = str(year)
            if key not in data["wage_annual"]:
                data["wage_annual"][key] = {
                    "value": value,
                    "source": "komunikat Prezesa GUS (auto-odczyt listy ogłoszeń GUS)",
                    "fetched": today,
                }
                report.append(f"Płace {year}: {value} zł (nowy odczyt, auto)")
        else:
            report.append(
                f"ALERT: nie udało się automatycznie odczytać przeciętnego "
                f"wynagrodzenia w gospodarce narodowej za {prev_year} — "
                "WYMAGA RĘCZNEGO WPISU do first_prints_pln.json (wage_annual)."
            )
    else:
        report.append(
            f"Płace {prev_year}: brak wpisu, ale to nie luty — komunikat "
            "Prezesa GUS oczekiwany ok. 9 lutego, próba automatyczna wtedy."
        )

    save_first_prints(data)

    print("=== fetch_gus.py — raport ===")
    for line in report:
        print("-", line)
    print(f"Zapisano: {FIRST_PRINTS}")


if __name__ == "__main__":
    main()
