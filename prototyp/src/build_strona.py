"""Buduje talent_strona.html z danych processed/. Uruchom po kazdej aktualizacji."""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_HTML = ROOT.parent / "talent_strona.html"

anchors = json.load(open(ROOT / "data/processed/talent_anchors.json"))
fx = pd.read_csv(ROOT / "data/processed/talent_w_walutach.csv", index_col=0, parse_dates=True)
fx.index = fx.index.to_period("M").astype(str)
wage = json.load(open(ROOT / "data/processed/wage_leg_v2.json"))

fxd = {c.replace("TLN_", ""): [round(v, 3) for v in fx[c]] for c in fx.columns}
fx_js = json.dumps({"labels": list(fx.index), "series": fxd}, separators=(",", ":"))
data_js = json.dumps(anchors, separators=(",", ":"))
wage_js = json.dumps(wage, separators=(",", ":"))
last = fx.iloc[-1]
cur_cards = "".join(
    f'<div class="card"><div class="l">1 TLN w {c}</div><div class="v">{last["TLN_"+c]:.2f}</div>'
    f'<div class="d">{c}, XII 2025</div></div>'
    for c in ["PLN", "USD", "EUR", "CHF", "GBP", "JPY"])

HTML = """<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talent (TLN) — jednostka wartości</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{--bg:#0f1419;--card:#1a2129;--tx:#e8e6e3;--mut:#8b949e;--ac:#d4a017}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font:16px/1.6 Georgia,serif;padding:24px;max-width:900px;margin:0 auto}
h1{font-size:1.9em;letter-spacing:.02em}
h1 span{color:var(--ac)}
h2{font-size:1.15em;margin:26px 0 10px;color:var(--tx)}
.sub{color:var(--mut);margin:4px 0 24px}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:24px}
.card{background:var(--card);border-radius:10px;padding:16px 18px}
.card .l{color:var(--mut);font-size:.78em;text-transform:uppercase;letter-spacing:.08em}
.card .v{font-size:1.7em;color:var(--ac);font-variant-numeric:tabular-nums}
.card .d{color:var(--mut);font-size:.8em}
.wrap{background:var(--card);border-radius:10px;padding:18px;margin-bottom:8px}
.cap{color:var(--mut);font-size:.8em;margin:0 4px 20px}
.foot{color:var(--mut);font-size:.85em;border-top:1px solid #2a323c;padding-top:14px;margin-top:16px}
.foot b{color:var(--tx)}
a{color:var(--ac)}
@media(max-width:600px){.grid{grid-template-columns:1fr 1fr}}
</style>
</head>
<body>
<h1>Talent <span>TLN</span></h1>
<p class="sub">Jednostka wartości minimalnego żalu (regret) &middot; √(ceny &times; płace) &middot; prototyp badawczy, Polska, baza I&nbsp;1996&nbsp;=&nbsp;100</p>
<div class="grid">
<div class="card"><div class="l">Wartość dziś</div><div class="v" id="today">—</div><div class="d" id="todaydate"></div></div>
<div class="card"><div class="l">Kotwica miesięczna</div><div class="v" id="anchor">—</div><div class="d" id="anchordate"></div></div>
<div class="card"><div class="l">Zmiana 12 mies.</div><div class="v" id="yoy">—</div><div class="d">ścieżka znana z wyprzedzeniem</div></div>
</div>

<h2>Indeks Talenta</h2>
<div class="wrap"><canvas id="ch" height="110"></canvas></div>
<p class="cap">Kotwice miesięczne 1996–2025. Środek geometryczny indeksu cen (CPI) i indeksu płac (średnia 12-mies.).</p>

<h2>Ile waluty kosztuje 1 Talent?</h2>
<div class="grid">__CURCARDS__</div>
<div class="wrap"><canvas id="chfx" height="130"></canvas></div>
<p class="cap">1 TLN = 1 PLN w bazie (I 1996); wycena w walutach po kursach rynkowych (NBP/FRED). JPY podzielone przez 100. Im szybciej rośnie linia, tym szybciej dana waluta traci wartość względem Talenta: 2002–2025 CHF ×1,5 &middot; EUR ×2,4 &middot; PLN ×2,9 &middot; USD ×3,3 &middot; JPY ×3,9.</p>

<h2>Noga płacowa: dwie metody pomiaru (USA, 2000–2026)</h2>
<div class="wrap"><canvas id="chw" height="130"></canvas></div>
<p class="cap">Porównanie na danych USA (FRED): <b>przeciętna płaca</b> ma zdradliwy efekt składu — w kwietniu 2020 skoczyła o +4,2% w miesiąc, bo pracę stracili najpierw najsłabiej zarabiający. <b>Fundusz płac / wygładzone zatrudnienie</b> (definicja Talenta v0.2) pokazał wtedy −8,9%: prawdziwy ubytek dochodów społeczeństwa. Długookresowo obie metody dają to samo (+136% za 26 lat) — różnią się dokładnie tam, gdzie uczciwość ma znaczenie: w kryzysie.</p>

<p class="foot"><b>Czym jest Talent?</b> Pożyczasz 1000 TLN — oddajesz 1000 TLN i obie strony odzyskują w przybliżeniu tę samą wartość: spłata nie rośnie względem płac szybciej, niż spadałaby względem cen. Środek geometryczny indeksu cen i indeksu płac minimalizuje maksymalny żal obu stron umowy — pasmo zweryfikowane na danych USA 1929–2025 (maks. 6,1%), Polski 1989–2024 (maks. 10,4%). Formuła jest deterministyczna i open source: <b>kod jest metodologią</b>, wartości nigdy nie są rewidowane wstecz, każdą można odtworzyć z danych publicznych. Szczegóły: REGULA_publikacyjna_Talent_v0.1.md.</p>

<script>
const A=__DATA__;
const per=Object.keys(A),val=Object.values(A);
const n=per.length,last=val[n-1],prev=val[n-2],g=last/prev;
const now=new Date(),base=new Date(per[n-1]+"-01T00:00:00");
const win=new Date(base.getFullYear(),base.getMonth()+1,1);
const K=new Date(win.getFullYear(),win.getMonth()+1,0).getDate();
const k=Math.min(Math.max(now>=win?now.getDate():K,1),K);
const today=last*Math.pow(g,k/K);
const yoy=(last/val[n-13]-1)*100;
document.getElementById('today').textContent=today.toFixed(2);
document.getElementById('todaydate').textContent=now.toISOString().slice(0,10)+" (pre-commitment)";
document.getElementById('anchor').textContent=last.toFixed(2);
document.getElementById('anchordate').textContent="za "+per[n-1];
document.getElementById('yoy').textContent=(yoy>=0?"+":"")+yoy.toFixed(1)+"%";

const axis={ticks:{color:'#8b949e'},grid:{color:'#232b34'}};
new Chart(document.getElementById('ch'),{type:'line',
 data:{labels:per,datasets:[{data:val,borderColor:'#d4a017',backgroundColor:'rgba(212,160,23,.08)',fill:true,pointRadius:0,borderWidth:2,tension:.25}]},
 options:{plugins:{legend:{display:false}},interaction:{intersect:false,mode:'index'},
 scales:{x:{...axis,ticks:{...axis.ticks,maxTicksLimit:10,callback:(v,i)=>per[i].endsWith('-01')&&+per[i].slice(0,4)%5===1?per[i].slice(0,4):null}},y:axis}}});

const FX=__FX__;
const cols={PLN:'#d4a017',USD:'#4c9f70',EUR:'#5b8dbe',CHF:'#c0504d',GBP:'#8064a2',CNY:'#e08e45',JPY:'#9aa2ab'};
const ds=Object.entries(FX.series).map(([c,v])=>({label:c==='JPY'?'JPY (÷100)':c,
 data:c==='JPY'?v.map(x=>x/100):v,borderColor:cols[c],pointRadius:0,borderWidth:1.8,tension:.25}));
new Chart(document.getElementById('chfx'),{type:'line',
 data:{labels:FX.labels,datasets:ds},
 options:{plugins:{legend:{labels:{color:'#e8e6e3',boxWidth:18,font:{size:11}}}},
 interaction:{intersect:false,mode:'index'},
 scales:{x:{...axis,ticks:{...axis.ticks,maxTicksLimit:12,callback:(v,i)=>FX.labels[i].endsWith('-01')&&+FX.labels[i].slice(0,4)%4===2?FX.labels[i].slice(0,4):null}},y:axis}}});

const WG=__WAGE__;
new Chart(document.getElementById('chw'),{type:'line',
 data:{labels:WG.labels,datasets:[
  {label:'przeciętna płaca (klasyczna)',data:WG.W1,borderColor:'#c0504d',pointRadius:0,borderWidth:1.8,tension:.2},
  {label:'fundusz płac / wygładzone zatrudnienie (Talent v0.2)',data:WG.W2,borderColor:'#4c9f70',pointRadius:0,borderWidth:1.8,tension:.2}]},
 options:{plugins:{legend:{labels:{color:'#e8e6e3',boxWidth:18,font:{size:11}}}},
 interaction:{intersect:false,mode:'index'},
 scales:{x:{...axis,ticks:{...axis.ticks,maxTicksLimit:14,callback:(v,i)=>WG.labels[i].endsWith('-01')&&+WG.labels[i].slice(0,4)%4===0?WG.labels[i].slice(0,4):null}},y:axis}}});
</script>
</body>
</html>"""

html = (HTML.replace("__DATA__", data_js).replace("__FX__", fx_js)
            .replace("__WAGE__", wage_js).replace("__CURCARDS__", cur_cards))
OUT_HTML.write_text(html)
print("zapisano", OUT_HTML, len(html)//1024, "KB")
