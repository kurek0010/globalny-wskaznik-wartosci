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

RZYMSKIE = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

# ---------------------------------------------------------------- strona glowna

def build_index() -> None:
    tpl = (SRC / "strona_szablon.html").read_text()

    anchors = json.load(open(DATA / "talent_anchors.json"))

    a = pd.read_csv(DATA / "talent_anchors.csv", index_col=0)
    a.index = pd.PeriodIndex(a.index, freq="M")
    avg_ic_2020 = a.loc[a.index.year == 2020, "I_c"].mean()
    hook_pct = round(avg_ic_2020 / a["I_c"].iloc[-1] * 100)

    fx = pd.read_csv(DATA / "talent_w_walutach.csv", index_col=0, parse_dates=True)
    fx_last_date = fx.index[-1]
    fx.index = fx.index.to_period("M").astype(str)

    fxd = {c.replace("TLN_", ""): [round(v, 3) for v in fx[c]] for c in fx.columns}
    last = fx.iloc[-1]
    fx_date = f"{RZYMSKIE[fx_last_date.month - 1]} {fx_last_date.year}"
    cur_cards = "".join(
        f'<div class="card mtile" data-series="{c}"><div class="l">1 TLN w {c}</div>'
        f'<div class="v">{last["TLN_"+c]:.2f}</div>'
        f'<div class="d">{c}, {fx_date}</div></div>'
        for c in ["PLN", "USD", "EUR", "CHF", "GBP", "JPY"])

    html = (tpl
            .replace("__DATA__", json.dumps(anchors, separators=(",", ":")))
            .replace("__FX__", json.dumps({"labels": list(fx.index), "series": fxd},
                                          separators=(",", ":")))
            .replace("__CURCARDS__", cur_cards)
            .replace("__HOOK_PCT__", str(hook_pct))
            .replace("__ANCHORFOR__", list(anchors)[-1])
            .replace("__UPDATED__", __import__("datetime").date.today().isoformat()))
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
    "TIP/README.md": "tip.html",
}

# Podmiana wzglednych linkow markdown na linki do GitHub - potrzebne tylko dla
# plikow spoza korzenia repo (np. TIP/README.md linkuje do TIP-0001-...md w
# tym samym katalogu, ktory nie ma wlasnej strony HTML).
GITHUB_BLOB = "https://github.com/kurek0010/talent/blob/main"
LINK_REWRITES = {
    "TIP/README.md": [
        ("(TIP-0001-noga-placowa-v02.md)", f"({GITHUB_BLOB}/TIP/TIP-0001-noga-placowa-v02.md)"),
        ("(TIP-0002-mediana-wynagrodzen.md)", f"({GITHUB_BLOB}/TIP/TIP-0002-mediana-wynagrodzen.md)"),
    ],
}

# KaTeX auto-render (cdnjs). Delimitery: $$ dla wzorow blokowych; celowo BEZ
# pojedynczego $ (kolizja z kwotami typu "147 $" w tresciach finansowych) -
# wzory w linii pisz jako \( ... \). auto-render domyslnie ignoruje <pre>/<code>
# (zweryfikowane w cdnjs katex 0.16.47/contrib/auto-render.min.js), wiec bloki
# kodu z formulami (np. regula_publikacyjna.html) zostaja nietkniete.
KATEX_RENDER_JS = (
    "renderMathInElement(document.body, {"
    "delimiters: [{left: '$$', right: '$$', display: true}, "
    "{left: '\\\\(', right: '\\\\)', display: false}], "
    "throwOnError: false});"
)

# Ten sam mechanizm motywu (Ciemny/Sepia/Jasny) co na stronie glownej
# (strona_szablon.html), zeby wybor przenosil sie miedzy stronami przez
# wspolny klucz localStorage "tln-theme". Inline skrypt w <head> ustawia
# atrybut przed renderowaniem (bez blysku zlego motywu).
THEME_HEAD_SCRIPT = """<script>
(function(){
 try{
  var t=localStorage.getItem('tln-theme');
  if(t!=='dark'&&t!=='sepia'&&t!=='light') t=window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';
  document.documentElement.setAttribute('data-theme',t);
 }catch(e){document.documentElement.setAttribute('data-theme','dark');}
})();
</script>"""

THEME_SWITCH_HTML = """<div class="theme-switch" role="group" aria-label="Wybierz motyw strony">
<button class="theme-btn" data-theme-btn="dark">Ciemny</button>
<button class="theme-btn" data-theme-btn="sepia">Sepia</button>
<button class="theme-btn" data-theme-btn="light">Jasny</button>
</div>"""

THEME_JS = """function setTheme(t){
 document.documentElement.setAttribute('data-theme',t);
 try{localStorage.setItem('tln-theme',t);}catch(e){}
 document.querySelectorAll('.theme-btn').forEach(b=>b.classList.toggle('active',b.dataset.themeBtn===t));
}
document.querySelectorAll('.theme-btn').forEach(b=>{
 b.addEventListener('click',()=>setTheme(b.dataset.themeBtn));
});
setTheme(document.documentElement.getAttribute('data-theme')||'dark');"""

SHELL = """<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{theme_head}
<title>{title} — Talent (TLN)</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.47/katex.min.css">
<style>
:root[data-theme="dark"]{{--bg:#0f1419;--card:#1a2129;--tx:#e8e6e3;--mut:#8b949e;--ac:#d4a017;--border:#2a323c}}
:root[data-theme="sepia"]{{--bg:#f2e8d5;--card:#fbf3e3;--tx:#3a2f1e;--mut:#7a6a52;--ac:#9c6b1f;--border:#ded0b0}}
:root[data-theme="light"]{{--bg:#faf9f6;--card:#ffffff;--tx:#1c1c1c;--mut:#6b6b6b;--ac:#a8720b;--border:#e2ded4}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--tx);font:16px/1.65 Georgia,serif;padding:24px;max-width:900px;margin:0 auto;transition:background-color .2s,color .2s}}
h1{{font-size:1.6em;margin:0 0 14px}}
h2{{font-size:1.2em;margin:28px 0 10px;color:var(--ac)}}
h3{{font-size:1.05em;margin:18px 0 8px}}
p,li{{margin:0 0 10px}}
ul,ol{{padding-left:22px;margin:0 0 12px}}
code{{font:.88em ui-monospace,Menlo,Consolas,monospace;background:var(--card);border-radius:6px;padding:1px 6px}}
pre{{background:var(--card);border-radius:8px;border-left:3px solid var(--ac);padding:14px 16px;overflow-x:auto;margin:0 0 14px}}
pre code{{background:none;padding:0}}
table{{border-collapse:collapse;width:100%;margin:0 0 16px;font-size:.92em}}
th,td{{border:1px solid var(--border);padding:6px 10px;text-align:left;vertical-align:top}}
th{{color:var(--mut);font-weight:normal}}
a{{color:var(--ac)}}
hr{{border:0;border-top:1px solid var(--border);margin:22px 0}}
em{{color:var(--mut)}}
blockquote{{border-left:3px solid var(--border);padding-left:14px;color:var(--mut);margin:0 0 12px}}
.topbar{{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:22px}}
.top{{font-size:.9em;margin:0}}
.theme-switch{{display:flex;gap:6px;flex-shrink:0}}
.theme-btn{{background:var(--border);color:var(--mut);border:1px solid transparent;border-radius:6px;padding:5px 11px;font:.8em/1.2 Georgia,serif;cursor:pointer;white-space:nowrap}}
.theme-btn:hover{{color:var(--tx)}}
.theme-btn.active{{border-color:var(--ac);color:var(--ac)}}
.gen{{color:var(--mut);font-size:.78em;border-top:1px solid var(--border);margin-top:30px;padding-top:12px}}
</style>
</head>
<body>
<div class="topbar">
<p class="top"><a href="index.html">← strona główna Talenta</a></p>
{theme_switch}
</div>
{body}
<p class="gen">Strona wygenerowana automatycznie z pliku <code>{src}</code> w
<a href="https://github.com/kurek0010/talent">repozytorium</a> —
wersja markdown jest kanoniczna.</p>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.47/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.47/contrib/auto-render.min.js" onload="{katex_js}"></script>
<script>{theme_js}</script>
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
        for old, new in LINK_REWRITES.get(src_name, []):
            text = text.replace(old, new)
        title = next((l.lstrip("# ").strip() for l in text.splitlines()
                      if l.startswith("# ")), out_name)
        body = md.reset().convert(text)
        (ROOT / out_name).write_text(
            SHELL.format(title=title, body=body, src=src_name, katex_js=KATEX_RENDER_JS,
                         theme_head=THEME_HEAD_SCRIPT, theme_switch=THEME_SWITCH_HTML,
                         theme_js=THEME_JS))
        print(f"{out_name} <- {src_name}")


if __name__ == "__main__":
    build_index()
    build_docs()
