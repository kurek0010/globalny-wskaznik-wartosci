# Linijka, której nie da się rozciągnąć. Jak zmierzyć wartość, gdy sam pieniądz się kurczy

*Reportaż o eksperymencie, który mierzy ceny świata nie w dolarach, lecz w ludzkich godzinach pracy.*

Wyobraźmy sobie krawca, który mierzy materiał miarką wykonaną z gumy. Każdego ranka miarka jest odrobinę dłuższa niż wczoraj. Klienci skarżą się, że garnitury maleją, choć krawiec przysięga, że odmierzył „tyle samo centymetrów". Problem nie leży w materiale — leży w miarce.

Dokładnie tym jest pieniądz, gdy próbujemy nim mierzyć wartość w długim okresie. Dolar, euro czy złoty to gumowa miarka: rozciąga się rok po roku w tempie, na które wpływają decyzje banków centralnych, kreacja kredytowa w bankach komercyjnych i ekspansja bilansów. Kiedy mówimy „ropa podrożała o 150% przez trzydzieści lat", nie wiemy, czy ropa stała się rzadsza, czy po prostu miarka się wydłużyła.

Pewien polski projekt badawczy — rozwijany otwarcie, z publicznym kodem i publicznymi danymi — próbuje skonstruować miarkę, której nikt nie potrafi rozciągnąć. Nazywa się AUV-T, *Absolute Unit of Value* w jednostkach czasu pracy. Poniżej tłumaczymy, jak się ją liczy i co już pokazała.

## Pomysł: zamiast pieniędzy — ludzki czas

Punkt wyjścia jest filozoficzny, ale prowadzi do bardzo konkretnej matematyki. Skoro każda cena wyrażona w pieniądzu jest skażona kondycją tego pieniądza, trzeba znaleźć jednostkę, której podaży nie da się powiększyć księgowym zapisem. Autor projektu wskazuje na jedyny taki zasób: **ludzki czas**. Bank centralny może rozszerzyć podaż pieniądza dowolnie. Nikt nie może dodać godzin do ludzkiej doby ani lat do ludzkiego życia.

Stąd przepis. Bierzemy cenę dobra wyrażoną w dolarach i dzielimy ją przez dochód z pracy, również wyrażony w dolarach. I tu dzieje się rzecz kluczowa: **dolar w liczniku i dolar w mianowniku skracają się**, jak ułamek. To, co zostaje, nie jest już wyrażone w żadnej walucie — jest wyrażone w czystym czasie pracy. Ile godzin musi przepracować przeciętny człowiek, żeby kupić beczkę ropy, tonę pszenicy, tonę miedzi.

To rozróżnienie jest subtelne, ale rozstrzygające. Klasyczny wskaźnik inflacji (CPI) dzieli cenę przez ceny *innych dóbr* — porównuje jedną gumową miarkę do drugiej. AUV-T dzieli cenę przez *pracę*, czyli przez coś spoza świata pieniądza. To pomysł stary jak ekonomia — już Adam Smith pisał, że „praca była pierwszą ceną, pierwotnym pieniądzem nabywczym" — i odświeżony współcześnie pod hasłem *time prices*.

## Przepis krok po kroku

W praktyce AUV-T powstaje z czterech składników, a całość jest na tyle prosta, że mieści się na serwetce.

Po pierwsze, **koszyk fizyczny**. Dziś to dziewiętnaście cen surowców w pięciu kategoriach: energia (ropa, gaz, węgiel, uran), żywność (pszenica, kukurydza, ryż, soja, olej palmowy), metale przemysłowe (miedź, aluminium, ruda żelaza, nikiel, cynk, ołów, cyna) oraz — od niedawna — budownictwo (stal i cement). Każdą cenę sprowadza się do wspólnego punktu odniesienia: rok 1996 to 100.

Po drugie, **sposób łączenia cen**. Zamiast zwykłej średniej projekt używa średniej geometrycznej. To nie kosmetyka: średnia geometryczna jest odporna na sytuację, w której jeden surowiec wystrzeli dziesięciokrotnie, i traktuje wzrosty oraz spadki symetrycznie. Dzięki temu pojedynczy szok naftowy nie zawłaszcza całego wskaźnika.

Po trzecie, **mianownik — cena pracy**. W wersji liczalnej dziś jest to światowy dochód na osobę, czyli produkt krajowy brutto całego świata podzielony przez liczbę ludzi. Też sprowadzony do 1996 = 100.

Po czwarte, **iloraz**. Koszyk dzielony przez dochód, pomnożony przez sto. Wynik to liczba krążąca wokół setki — i to właśnie jest AUV-T.

Nad wszystkim czuwają dwie żelazne zasady, które odróżniają ten wskaźnik od WIBOR-u czy oficjalnego CPI. Pierwsza: **determinizm** — ktokolwiek weźmie te same dane i ten sam kod, dostanie tę samą liczbę, co do miejsca po przecinku. Druga: **zakaz poprawiania po fakcie** — skład koszyka, wagi i rok bazowy są zamrożone w kodzie; gdyby kiedyś trzeba je było zmienić, musi to nastąpić jawnie, ogłoszoną wcześniej regułą, a nie cichą decyzją.

## Co pokazała miarka

Tu zaczyna się część, dla której warto było liczyć. Na danych z lat 1996–2025:

Mierzony nominalnie, w dolarach, koszyk surowców podrożał o około **150%**. Szeroka podaż pieniądza w USA (agregat M2) wzrosła w tym czasie o **489%**. Inflacja konsumencka w USA wyniosła **105%**.

A AUV-T? Zmienił się o **0,4%** w ciągu trzydziestu lat. Mierzony w ludzkiej pracy, koszyk dóbr podstawowych kosztuje dziś niemal dokładnie tyle, ile kosztował w 1996 roku. Gumowa miarka rozciągnęła się prawie pięciokrotnie; rzecz, którą mierzyła, ani drgnęła.

Co więcej, gdy ten sam test zastosować do SDR — koszyka walut Międzynarodowego Funduszu Walutowego, uchodzącego za „neutralną" jednostkę rozrachunkową — okazuje się, że i on dryfuje w górę o około **90%**. Neutralny w sensie nieprzywiązania do jednego kraju, ale wciąż zlepiony z walut papierowych, więc tracący wartość razem z nimi. Dopiero zakotwiczenie w pracy daje linijkę, która stoi w miejscu.

Pod powierzchnią dzieją się rzeczy jeszcze ciekawsze. Rozbity na kategorie, AUV-T pokazuje, że żywność w przeliczeniu na czas pracy **staniała o niemal połowę** — to konkretny, mierzalny dowód, że wyżywienie człowieka kosztuje dziś dramatycznie mniej wysiłku niż pokolenie temu. Energia i metale realnie nieco podrożały, budownictwo praktycznie się nie zmieniło.

## Falowanie, które nie jest błędem

Wykres AUV-T nie jest płaską kreską. Faluje: szczyt w 2008 roku (około 148), dolina w latach 2015–2020 (poniżej 90), potem powrót do setki. Na pierwszy rzut oka wygląda to na wadę. W rzeczywistości to sygnał.

Te fale to cykl surowcowy: boom napędzany chińskim popytem przed 2008 rokiem, krach po upadku Lehman Brothers, załamanie cen ropy w 2014–2015, szok energetyczny po inwazji na Ukrainę. AUV-T mówi nam coś, czego sam CPI nie powie: **realna siła nabywcza pieniądza nad zasobami nie jest stała — oddycha razem z kryzysami**. Gdy wskaźnik jest nisko (kryzys deflacyjny, „gotówka jest królem"), za te same pieniądze kupisz więcej realnych dóbr. Gdy jest wysoko (kryzys podażowy, inflacja), kupisz mniej. Jeden wskaźnik rozróżnia więc dwa zupełnie różne rodzaje kryzysu.

To prowadzi do uczciwego rozgraniczenia, które autorzy projektu podkreślają. AUV-T w obecnej postaci jest **znakomitym termometrem, ale jeszcze nie linijką**. Jako miara realnej wartości — tego, czy świat się bogaci — działa, bo jego powrót do setki bez długoterminowego dryfu jest właśnie odpowiedzią: w ujęciu zasobowym ludzkość ani nie zubożała, ani nie wzbogaciła się dramatycznie, tylko falowała wokół równowagi. Ale jako jednostka do indeksacji kredytów hipotecznych czy emerytur — gdzie potrzebna jest gładkość — wahania rzędu kilkudziesięciu procent na razie ją dyskwalifikują. Wygładzanie kroczącą średnią tłumi drgania, lecz nie kasuje samej dekadowej fali, bo ta jest prawdziwą cechą świata, nie szumem.

## Czego jeszcze brakuje

Projekt nie udaje gotowego. Ceny stali i cementu pochodzą na razie z amerykańskich indeksów producenckich użytych jako przybliżenie globalnych — bo otwartej, długiej serii cen światowych dla tych dóbr po prostu nie ma. Mianownik liczony jest jako dochód na osobę, a nie jako precyzyjny dochód na godzinę pracy, co jest świadomym uproszczeniem do czasu wpięcia danych o godzinach przepracowanych. Otwarte pozostaje pytanie, jak najlepiej oddzielić trwały trend od cyklicznej fali.

Wszystko to jednak dzieje się na widoku. Kod, dane i historia decyzji są publiczne, a każdy krok obliczenia daje się odtworzyć bez pytania kogokolwiek o zgodę. W świecie, w którym najważniejsze wskaźniki finansowe ustala się za zamkniętymi drzwiami, sama ta przejrzystość jest już eksperymentem wartym obserwowania — niezależnie od tego, czy gumową miarkę uda się ostatecznie zastąpić stalową.

---

*AUV-T jest projektem badawczym we wczesnej fazie. Przedstawione liczby pochodzą z roboczych obliczeń na danych 1996–2025 i służą ilustracji metody, nie stanowią rekomendacji finansowej.*
