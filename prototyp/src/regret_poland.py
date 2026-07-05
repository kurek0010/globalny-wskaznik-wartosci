"""Test kruchej gospodarki: Talent (sqrt(CPI*placa)) na danych PL 1989-2024.

CPI: FRED POLCPIALLMINMEI (OECD MEI, srednie roczne, 2015=100), pobrane 2026-07-04.
Place: przecietne miesieczne wynagrodzenie GUS/ZUS (tablice kwoty bazowej).
  UWAGA (1): 1989-1998 netto, od 1999 brutto (ubruttowienie) - laczone
  lancuchowo wzrostem na bazie porownywalnej ~+11.1% w 1999 (przyblizenie
  GUS, do weryfikacji; wplyw na wyniki <1 p.p. na jednym roku).
  UWAGA (2): wartosci sprzed 1995 przeliczone denominacja 10000:1.
  UWAGA (3): tablica plac wpisana z wiedzy - DO WERYFIKACJI u zrodla GUS.
Metryka: regret dwustronny (patrz regret_century.py). Horyzonty 3-30 lat.
"""
import math

CPI = {1989:0.9671,1990:6.4588,1991:11.4172,1992:16.6804,1993:22.8462,1994:30.3834,
1995:38.8760,1996:46.5714,1997:53.5167,1998:59.7235,1999:63.9962,2000:70.3319,
2001:74.1357,2002:75.5482,2003:76.0640,2004:78.6369,2005:80.3542,2006:81.3865,
2007:83.3876,2008:86.8607,2009:90.1574,2010:92.4841,2011:96.4048,2012:99.8372,
2013:100.8276,2014:100.8818,2015:100.0,2016:99.3352,2017:101.3974,2018:103.2357,
2019:105.5352,2020:109.0965,2021:114.6113,2022:131.1491,2023:146.2691,2024:151.8044}

W_NETTO = {1989:20.6758,1990:102.9637,1991:177.0,1992:293.5,1993:399.5,1994:532.8,
1995:702.62,1996:873.00,1997:1061.93,1998:1239.49}
W_BRUTTO = {1999:1706.74,2000:1923.81,2001:2061.85,2002:2133.21,2003:2201.47,
2004:2289.57,2005:2380.29,2006:2477.23,2007:2691.03,2008:2943.88,2009:3102.96,
2010:3224.98,2011:3399.52,2012:3521.67,2013:3650.06,2014:3783.46,2015:3899.78,
2016:4047.21,2017:4271.51,2018:4585.03,2019:4918.17,2020:5167.47,2021:5662.53,
2022:6346.15,2023:7155.48,2024:8181.72}
CHAIN_1999 = 1.111  # wzrost plac 1998->1999 na bazie porownywalnej (przybl.)

HORIZONS = [3, 5, 10, 20, 30]
ZERO = 0.02


def build_wage():
    w = dict(W_NETTO)
    w[1999] = w[1998] * CHAIN_1999
    for y in range(2000, 2025):
        w[y] = w[y-1] * (W_BRUTTO[y] / W_BRUTTO[y-1])
    return w


def main():
    years = range(1989, 2025)
    wage = build_wage()
    c = {y: CPI[y]/CPI[1989]*100 for y in years}
    w = {y: wage[y]/wage[1989]*100 for y in years}
    tal = {y: math.sqrt(c[y]*w[y]) for y in years}
    cands = {"nominal": {y: 100.0 for y in years}, "CPI": c, "placa": w,
             "Talent": tal}
    pct = lambda x: (math.exp(x)-1)*100
    for name, I in cands.items():
        regs, zero, n, worst = [], 0, 0, (0.0, None, None, "")
        for h in HORIZONS:
            for t in years:
                if t+h > 2024:
                    continue
                R = math.log(I[t+h]/I[t])
                b = R - math.log(w[t+h]/w[t])
                l = R - math.log(c[t+h]/c[t])
                reg = max(max(b, 0), max(-l, 0))
                n += 1; zero += reg < ZERO; regs.append(reg)
                if reg > worst[0]:
                    worst = (reg, t, t+h, "dluznik" if b >= -l else "wierzyciel")
        regs.sort()
        print(f"{name:8} | zero {zero/n*100:3.0f}% | med {pct(regs[n//2]):6.1f}% | "
              f"p95 {pct(regs[int(n*.95)]):7.1f}% | max {pct(worst[0]):8.1f}% | "
              f"{worst[3]} {worst[1]}->{worst[2]}")


if __name__ == "__main__":
    main()
