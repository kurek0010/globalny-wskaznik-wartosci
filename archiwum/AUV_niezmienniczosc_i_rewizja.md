# AUV — niezmienniczość jednostki i reguła rewizji koszyka

**Autor:** Mariusz Kurowski
**Data:** 2026-06-22
**Przeznaczenie:** sekcja teoretyczna working papera; uzasadnienie poprawności i trwałości AUV.

AUV opiera się na dwóch filarach niezmienniczości, które razem oznaczają: *prawdziwość wskaźnika nie zależy ani od żadnej waluty, ani od żadnego pojedynczego źródła danych.*

- **Część I — niezmienniczość względem numéraire:** AUV daje ten sam wynik niezależnie od tego, w jakiej jednostce wyrażone są ceny; działa nawet, gdy znikną wszystkie waluty.
- **Część II — niezmienniczość względem składu koszyka:** AUV pozostaje prawdą, gdy poszczególne serie wypadają lub są dodawane — pod warunkiem stosowania jawnej reguły rewizji.

---

## Część I — Niezmienniczość względem numéraire

### I.1 Twierdzenie

AUV jest ilorazem stosunków wzrostu:

```
AUV(t) = [ koszyk(t)/koszyk(t0) ] / [ dochód(t)/dochód(t0) ]
```

Każdy nawias jest wielkością **bezwymiarową** (stosunek dwóch wartości w tej samej jednostce). Stosunek nie zależy od jednostki miary. Zatem AUV jest niezmienniczy względem wyboru numéraire.

### I.2 Dowód (kasowanie numéraire)

Niech ceny będą wyrażone w dowolnej walucie X. Wyraźmy je w AUV: `p^AUV = p^X / AUV^X`. Wtedy dla koszyka i dochodu:

```
koszyk^AUV / dochód^AUV = (koszyk^X / AUV^X) / (dochód^X / AUV^X) = koszyk^X / dochód^X
```

Czynnik AUV^X skraca się. Wynik jest identyczny niezależnie od tego, czy liczymy w dolarach, złocie, muszlach czy w samym AUV. Dolar w dotychczasowej implementacji był jedynie **wygodnym rusztowaniem**, nigdy istotą wskaźnika.

### I.3 Przypadek graniczny — świat bez walut

Gdyby zniknęły wszystkie waluty, AUV nadal da się policzyć, bo zależy wyłącznie od wielkości niezależnych od pieniądza:

1. **względne ceny surowców** (stosunki wymiany: ile ropy za pszenicę) — z natury bez numéraire;
2. **realny wzrost produkcji/dochodu** — mierzalny metodą łańcuchową z ilości fizycznych i cen względnych, tak jak dziś liczy się realne PKB niezależnie od poziomu cen.

Z fizycznych ilości (tony, baryłki, populacja) i cen względnych rekonstruujemy realny koszyk i realny dochód, bierzemy iloraz — otrzymujemy AUV. W granicy AUV staje się **naturalnym numéraire**, bo jako jedyny jest zakotwiczony w rzeczywistości fizycznej, a nie w decyzji autorytetu. To realizacja zasady heliocentrycznej: jednostka, której prawda nie zależy od nikogo.

### I.4 Zastrzeżenie — refleksywność

Gdy AUV stanie się powszechną kotwicą, uczestnicy zaczną ustawiać ceny z oglądaniem się na AUV (jak dziś na CPI). Powstaje sprzężenie zwrotne miara↔mierzone. Nie unieważnia to wzoru, ale wymaga: (a) procedury rewizji reguł (Część II), (b) **zakotwiczenia w wielkościach fizycznych** (wersja ważona produkcją/zapotrzebowaniem). Dopóki AUV jest przywiązany do ton i baryłek, a nie tylko do własnych notowań, sprzężenie nie oderwie go od realu — inaczej niż walutę opartą wyłącznie na cenach.

---

## Część II — Niezmienniczość względem składu koszyka i reguła rewizji

### II.1 Problem

W horyzoncie dekad: część serií zniknie (źródło przestanie publikować), pojawią się nowe istotne zasoby (lit, metale ziem rzadkich), a instytucja może chcieć dodać/usunąć składnik uchwałą. Trzeba to robić tak, by (a) nie powstał skok/nieciągłość indeksu, (b) nie otworzyć drzwi do manipulacji (dobierania składników pod pożądany wynik).

### II.2 Idea kluczowa: kategorie są szkieletem, składniki są wymienne

AUV mierzy **koszt kategorii potrzeb** (energia, żywność, metale, budownictwo, materiały krytyczne) — pojęcia stabilne — a nie „cenę serii X". Poszczególne surowce w obrębie kategorii są *wymiennymi proxy*. Zamiana jednej serii ropy na inną, czy jednego metalu na inny, nie zmienia *co* mierzymy, tylko *czym* to przybliżamy. To jest sedno „wszystko pozostaje prawdą": obiekt pojęciowy (realny koszt potrzeb cywilizacji) jest niezmienny, przyrządy pomiarowe są wymienne.

### II.3 Ciągłość: łączenie łańcuchowe (chain-linking)

Standard teorii indeksów (stosowany w CPI, indeksach giełdowych). W momencie rewizji L liczymy indeks starym i nowym koszykiem dla tego samego okresu i zszywamy je współczynnikiem:

```
s = Indeks_stary(L) / Indeks_nowy_surowy(L)
Indeks_zszyty(t) = Indeks_nowy_surowy(t) × s     dla t ≥ L
```

Poziom indeksu jest **ciągły** w L (bez skoku); zmienia się tylko koszyk napędzający przyrosty *po* L. Wartości sprzed L nigdy nie są rewidowane.

### II.4 Reguła rewizji odporna na manipulację

Sześć zasad, które zamrażamy w regulaminie:

1. **Obiektywne kryteria włączenia, ustalone z góry.** Składnik kwalifikuje się, jeśli spełnia mierzalne warunki (np. udział w wartości światowej produkcji zasobów > próg; publiczne, niezależne źródło o częstotliwości ≥ miesięcznej i historii ≥ N lat). Włączenie/wyłączenie jest wtedy mechaniczne, nie głosowaniem nad wynikiem.
2. **Ogłoszenie przed zastosowaniem (pre-commitment).** Każda zmiana ogłaszana K okresów naprzód, na danych do ustalonego odcięcia — nikt nie może zsynchronizować zmiany, by poruszyć indeks w pożądaną stronę.
3. **Automatyczne wypadnięcie przy utracie danych.** Gdy seria przestaje być publikowana, wypada przy najbliższej rewizji; jej wagę przejmuje reguła wagowa (np. proporcjonalnie w kategorii). Chain-linking gwarantuje brak skoku.
4. **Redundancja / minimalne pokrycie.** Wymóg ≥ N niezależnych źródeł na kategorię, by utrata jednego nie łamała kategorii.
5. **Nigdy wstecz.** Zmiany nie rewidują opublikowanych wartości (jak UF).
6. **Test nakładania (ciągłości znaczenia).** W oknie nakładania stary i nowy koszyk muszą podążać blisko (np. korelacja przyrostów > próg); zbyt duża rozbieżność = sygnał, że rewizja po cichu zmienia sens indeksu → wstrzymanie do przeglądu.

### II.5 Ograniczona uznaniowość (uchwała)

Dodanie składnika uchwałą jest dopuszczalne **wyłącznie** gdy: spełnia kryteria z II.4.1, jest ogłoszone z wyprzedzeniem (II.4.2), udokumentowane i przechodzi test nakładania (II.4.6). To uznaniowość *związana regułą* — instytucja decyduje *kiedy* zastosować kryterium, nie *jaki ma być wynik*.

### II.6 Wniosek

Utrata danych nie łamie AUV. Wskaźnik pozostaje prawdą, bo to, co mierzy — realny koszt potrzeb cywilizacji — jest pojęciowo stałe, a jego przyrządy (konkretne serie) rotują wg jawnej reguły z ciągłością łańcuchową. To jest druga niezmienniczość obok numéraire: **niezmienniczość reprezentacji**.

---

## Podsumowanie: dwie niezmienniczości

| Filar | Co znaczy | Dzięki czemu |
| --- | --- | --- |
| Numéraire (Cz. I) | wynik niezależny od waluty; działa bez fiat | AUV to iloraz stosunków bezwymiarowych |
| Reprezentacja (Cz. II) | wynik trwały mimo rotacji serii | kategorie-szkielet + chain-linking + reguła rewizji |

Razem: AUV nie zależy ani od żadnej „prymitywnej" waluty, ani od żadnego pojedynczego dostawcy danych. Jego prawdziwość opiera się na wielkościach fizycznych i stosunkach względnych — najtrwalszym możliwym fundamencie.
