"""Builder strony Talenta — JEDYNE źródło plików HTML w korzeniu repo.

Zasada: NIE edytuj recznie index.html, talent_strona.html ani stron
dokumentow (whitepaper.html itd.) — kazde uruchomienie buildera je nadpisze.
- uklad strony glownej: prototyp/src/strona_szablon.html (edytuj TO)
- tresc dokumentow: pliki .md w korzeniu repo (edytuj TE)
Po zmianach uruchom: python src/build_strona.py
"""
from __future__ import annotations

import json
from pathlib import Path

import markdown
import pandas as pd

SRC = Path(__file__).resolve().parent
ROOT = SRC.parents[1]          # korzen repo
DATA = SRC.parent / "data" / "processed"

# ---------------------------------------------------------------- strona glowna

def build_index() -> None:
    tpl = (SRC / "strona_szablon.html").read_text()

    anchors = json.load(open(DATA / "talent_anchors.json"))
    fx = pd.read_csv(DATA / "talent_w_walutach.csv", index_col=0, parse_dates=True)
    fx.index = fx.index.to_period("M").astype(str)
    wage = json.load(open(DATA / "wage_leg_v2.json"))

    fxd = {c.replace("TLN_", ""): [round(v, 3) for v in fx[c]] for c in fx.columns}
    last = fx.iloc[-1]
    cur_cards = "".join(
        f'<div class="card"><div class="l">1 TLN w {c}</div>'
        f'<div class="v">{last["TLN_"+c]:.2f}</div>'
        f'<div class="d">{c}, XII 2025</div></div>'
        for c in ["PLN", "USD", "EUR", "CHF", "GBP", "JPY"])

    html = (tpl
            .replace("__DATA__", json.dumps(anchors, separators=(",", ":")))
            .replace("__FX__", json.dumps({"labels": list(fx.index), "series": fxd},
                                          separators=(",", ":")))
            .replace("__WAGE__", json.dumps(wage, separators=(",", ":")))
            .replace("__CURCARDS__", cur_cards))
    (ROOT / "index.html").write_text(html)
    (ROOT / "talent_strona.html").write_text(html)
    print(f"index.html + talent_strona.html: {len(html)//1024} KB")

# ------------------------------------------------------------- dokumenty md->html

DOCS = {  # plik md w korzeniu -> strona html
    "ARTYKUL_Talent_popularnonaukowy.md": "whitepaper.html",
    "ARTYKUL_wprowadzenie_i_zastosowania.md": "wprowadzenie.html",
    "REGULA_publikacyjna_Talent_v0.1.md": "regula_publikacyjna.html",
    "WYSCIG_kandydatow_minimalny_zal.md": "wyscig_kandydatow.html",
    "WYNIKI_test_stulecia_USA.md": "wyniki_test_stulecia_usa.html",
    "WYNIKI_kruche_gospodarki.md": "wyniki_kruche_gospodarki.html",
    "WYNIKI_talent_dwustronny.md": "wyniki_talent_dwustronny.html",
}

SHELL = """<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Talent (TLN)</title>
<style>
:root{{--bg:#0f1419;--card:#1a2129;--tx:#e8e6e3;--mut:#8b949e;--ac:#d4a017}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--tx);font:16px/1.65 Georgia,serif;padding:24px;max-width:900px;margin:0 auto}}
h1{{font-size:1.6em;margin:0 0 14px}}
h2{{font-size:1.2em;margin:28px 0 10px;color:var(--ac)}}
h3{{font-size:1.05em;margin:18px 0 8px}}
p,li{{margin:0 0 10px}}
ul,ol{{padding-left:22px;margin:0 0 12px}}
code{{font:.88em ui-monospace,Menlo,Consolas,monospace;background:var(--card);border-radius:6px;padding:1px 6px}}
pre{{background:var(--card);border-radius:8px;border-left:3px solid var(--ac);padding:14px 16px;overflow-x:auto;margin:0 0 14px}}
pre code{{background:none;padding:0}}
table{{border-collapse:collapse;width:100%;margin:0 0 16px;font-size:.92em}}
th,td{{border:1px solid #2a323c;padding:6px 10px;text-align:left;vertical-align:top}}
th{{color:var(--mut);font-weight:normal}}
a{{color:var(--ac)}}
hr{{border:0;border-top:1px solid #2a323c;margin:22px 0}}
em{{color:var(--mut)}}
blockquote{{border-left:3px solid #2a323c;padding-left:14px;color:var(--mut);margin:0 0 12px}}
.top{{margin-bottom:22px;font-size:.9em}}
.gen{{color:var(--mut);font-size:.78em;border-top:1px solid #2a323c;margin-top:30px;padding-top:12px}}
</style>
</head>
<body>
<p class="top"><a href="index.html">← strona główna Talenta</a></p>
{body}
<p class="gen">Strona wygenerowana automatycznie z pliku <code>{src}</code> w
<a href="https://github.com/kurek0010/globalny-wskaznik-wartosci">repozytorium</a> —
wersja markdown jest kanoniczna.</p>
</body>
</html>
"""


def build_docs() -> None:
    md = markdown.Markdown(extensions=["tables", "fenced_code"])
    for src_name, out_name in DOCS.items():
        src_path = ROOT / src_name
        if not src_path.exists():
            print(f"POMINIETO (brak pliku): {src_name}")
            continue
        text = src_path.read_text()
        title = next((l.lstrip("# ").strip() for l in text.splitlines()
                      if l.startswith("# ")), out_name)
        body = md.reset().convert(text)
        (ROOT / out_name).write_text(
            SHELL.format(title=title, body=body, src=src_name))
        print(f"{out_name} <- {src_name}")


if __name__ == "__main__":
    build_index()
    build_docs()
