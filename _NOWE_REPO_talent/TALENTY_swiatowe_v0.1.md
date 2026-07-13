# Talenty światowe — audyt dostępności danych (v0.1)

**Data:** 2026-07-07 · **Cel:** dla których głównych walut da się liczyć Talenta (√(CPI × płace)) na poziomie jakości Talenta-PL/US — i co z tego wynika dla rozliczeń międzynarodowych.
**Metoda oceny:** noga cen (CPI/HICP: częstotliwość, historia, liczba niezależnych źródeł) + noga płac (miesięczna > kwartalna > roczna; rejestrowa > ankietowa) + wiarygodność instytucjonalna (kazus INDEC). Wpisy oznaczone ✻ pochodzą z wiedzy i wymagają potwierdzenia u źródła przed wdrożeniem.

## 1. Klasyfikacja

### Poziom A — pełna jakość (obie nogi miesięczne, długa historia)

| Waluta | Noga cen | Noga płac | Uwagi |
|---|---|---|---|
| **USD** | CPI-U (BLS, od 1913) + PCE + chained CPI — 3 miary od ręki | CES miesięcznie (od 1939), ECI kwartalnie, mediana Atlanta Fed | wzorzec; wszystko w FRED |
| **PLN** | GUS m/m (od 1989) + HICP | sektor przedsiębiorstw miesięcznie + **mediana z rejestrów ZUS+MF miesięcznie** (od 2010) | nasz rdzeń; TIP-0002 |
| **GBP** | CPI/CPIH (ONS, miesięcznie) | Average Weekly Earnings miesięcznie (od 2000; wcześniej AEI od 1963 ✻) | b. dobra |
| **JPY** | CPI (Statistics Bureau, miesięcznie, od 1946 ✻) | Monthly Labour Survey — płace miesięcznie, długa historia | uwaga: skandal metodologiczny MLS 2018 (zaniżone próbkowanie) — podręcznikowy argument za tripwire; poza tym GREEN |
| **CAD** | CPI (StatCan, miesięcznie) | SEPH — przeciętne tygodniówki miesięcznie + płace z LFS miesięcznie (2 źródła!) | b. dobra |
| **SEK** | CPI/CPIF (SCB, miesięcznie) | krótkookresowa statystyka płac miesięcznie ✻ | dobra |
| **KRW** | CPI (KOSTAT, miesięcznie) | badanie płac MOEL miesięcznie ✻ | dobra |

### Poziom B — wykonalne z kompromisem (noga płac kwartalna/roczna)

| Waluta | Noga cen | Noga płac | Kompromis |
|---|---|---|---|
| **EUR** | HICP miesięcznie (Eurostat, od 1996; + krajowe CPI 20 państw = naturalna mediana źródeł) | brak miesięcznej: Labour Cost Index i płace negocjowane (EBC) kwartalnie; compensation per employee kwartalnie | kotwica płacowa aktualizowana kwartalnie, interpolacja UF-style; za to noga cen najlepiej zabezpieczona na świecie (20 niezależnych urzędów) |
| **AUD** | **pełny miesięczny CPI od X 2025** (wcześniej kwartalny — historia miesięczna dopiero się buduje) | Wage Price Index kwartalnie | obie kotwice do niedawna kwartalne; historycznie liczyć kwartalnie, od 2025 mieszanie |
| **CHF** | CPI (FSO, miesięcznie) | szwajcarski indeks płac (SLI) **rocznie** ✻ | noga płac roczna — jak nasz prototyp PL; przy szwajcarskiej stabilności płac akceptowalne, ale to najsłabsza noga w gronie |
| **NOK** | CPI miesięcznie | indeks płac kwartalnie ✻ | jak EUR |
| **BRL** | IPCA miesięcznie (IBGE; solidny) | dochody z pracy PNAD Contínua miesięcznie (ankietowe) ✻ | wykonalne; historia inflacyjna sprzed 1994 wymaga trybu awaryjnego w backteście |
| **MXN** | INPC dwutygodniowo(!) | płaca rejestrowa IMSS miesięcznie (administracyjna — jak ZUS) ✻ | zaskakująco dobra infrastruktura danych |

### Poziom C — poważne przeszkody

| Waluta | Problem |
|---|---|
| **CNY** | CPI miesięczny jest, ale płace tylko **roczne** (urban units), brak niezależnych źródeł do tripwire, wątpliwości o odporność statystyk na presję polityczną — dokładnie ryzyko INDEC bez narzędzi obrony. Talent-CNY liczyć można, publikować z gwiazdką |
| **INR** | CPI ogólnokrajowy dopiero od 2011; brak wiarygodnej ogólnokrajowej serii płac (ogromny sektor nieformalny) |

## 2. Wniosek operacyjny

**Dziewięć walut nadaje się od zaraz** (poziom A + EUR z kwartalną nogą płac): USD, EUR, PLN, GBP, JPY, CAD, SEK, KRW, + CHF/AUD z kompromisem. To pokrywa ~2/3 światowego PKB i ~90% rozliczeń walutowych. Wspólna reguła publikacyjna, wspólny kod, per kraj tylko rejestr źródeł w polityce danych (rozdział per waluta, jak §1 dla PL).

## 3. Kursy między-talentowe — macierz rozliczeń międzynarodowych

Z K talentów krajowych i rynkowych kursów walut wynika bez żadnych nowych danych:

1. **Kurs krzyżowy talentów**: `TLN-A/TLN-B (t) = [A_A(t)/A_A(0)] / [A_B(t)/A_B(0)] × FX_AB(t)/FX_AB(0)` — mierzy czysty realny rozjazd dwóch gospodarek po odjęciu szumu walutowego i inflacyjnego. Sama w sobie ciekawa publikacja (np. TLN-PL/TLN-US ×~1,53 za 2002–2024: tyle realnie Polska dogoniła Amerykę).
2. **Talent umowy dwustronnej** (zbadany w `WYNIKI_talent_dwustronny.md`): środek geometryczny pary z kursem po połowie — dla dowolnej z K(K−1)/2 par. Przy 9 walutach: **36 gotowych jednostek umów dwustronnych**.
3. **Talent koszykowy N stron**: średnia geometryczna talentów uczestników (wagi równe lub kontraktowe) — jednostka konsorcjów i łańcuchów dostaw.

Publikacyjnie: jedna tabela dzienna K kotwic + macierz kursów krzyżowych; koszt krańcowy kolejnej waluty bliski zeru.

## 4. Następne kroki (propozycja kolejności)

1. **Talent-US produkcyjnie** (dane najlepsze, wszystko w FRED, zero pracy nad źródłami) — drugi kraj na stronie + pierwszy kurs krzyżowy TLN-PL/TLN-US.
2. **Talent-EUR** (największa waga gospodarcza; do rozstrzygnięcia szczegół kwartalnej nogi płac — kandydat na TIP).
3. GBP, JPY, CAD — mechaniczne powtórzenie.
4. Weryfikacja pozycji ✻ przed każdym wdrożeniem (jedna sesja na kraj).

Świadomie poza zakresem: CNY/INR do czasu rozwiązania problemu źródeł; kraje strefy euro osobno (mają EUR); kryptowaluty (nie mają własnych cen i płac — Talent mierzy gospodarki, nie tokeny).

**Rozwinięcie per waluta:** karty w katalogu [waluty/](waluty/) — PLN, USD, GBP, JPY, EUR, CHF oraz CNY (z zastrzeżeniem dużej aproksymacji).
