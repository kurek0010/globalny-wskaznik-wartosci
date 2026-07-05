# Filozofia Projektowania — Mariusz

Dokument przeznaczony do wiki autora. Stanowi opis fundamentalnych zasad, którymi kieruje się przy projektowaniu systemów. Może być również wykorzystywany jako kontekst dla asystentów AI współpracujących nad kolejnymi projektami.

---

## Zasada Heliocentryczna

Buduję systemy, które ze swej natury nie zależą od arbitralnych decyzji rad, komitetów, banków centralnych, ekspertów ani innych autorytetów. Wyniki takich systemów wynikają z obserwowalnych, weryfikowalnych danych przetworzonych przez deterministyczne reguły.

Nazwa pochodzi z analogii do rewolucji kopernikańskiej. Zamiast modelu antropocentrycznego — w którym centrum układu jest człowiek lub instytucja decyzyjna — przyjmuję model, w którym centrum jest obiektywna rzeczywistość, mierzona niezależnie od tego, co o niej myślą jej uczestnicy.

## Precyzja Terminologii

Wymagam ścisłej terminologii w sprawach pieniężnych. Termin **"dodruk pieniędzy" jest dla mnie nieakceptowalny** w jakimkolwiek kontekście roboczym. Pieniądz we współczesnym systemie powstaje przede wszystkim przez:

- **Kreację kredytową w bankach komercyjnych** — gdy bank udziela kredytu, tworzy nowy pieniądz depozytowy w księgach. To dominujący kanał kreacji pieniądza w nowoczesnej gospodarce.
- **Ekspansję bilansu banku centralnego** — luzowanie ilościowe, skup aktywów, kreacja rezerw bankowych. To procesy księgowe, nie fizyczne drukowanie.
- **Kreację długu** — pożyczki publiczne tworzą instrumenty finansowe, które w szerszym systemie finansowym pełnią funkcję pieniądza.

Akceptowalne terminy: *kreacja pieniądza*, *ekspansja monetarna*, *wzrost agregatów monetarnych*, *kreacja kredytowa*, *luzowanie ilościowe*, *skup aktywów przez bank centralny*, *powiększanie bilansu banku centralnego*.

Wyklucza: *dodruk*, *drukowanie pieniędzy*, *money printing*. Te są nieprecyzyjne i utrwalają błędną intuicję, że pieniądz jest papierowy. W rzeczywistości w nowoczesnym systemie >95% pieniądza istnieje wyłącznie elektronicznie.

## Praktyczne Kryteria

Dane wejściowe muszą być otwarte i powszechnie dostępne. Odrzucam zależność od subskrypcyjnych źródeł typu Bloomberg, S&P Global czy IHS Markit — nie ze względu na koszt, lecz dlatego że wprowadzają gatekeepera. Preferuję FRED, ECB, IMF, BIS, publiczne API giełd oraz otwarte rejestry rządowe.

Formuły muszą być deterministyczne. Każdy, kto dysponuje tymi samymi danymi, musi uzyskać ten sam wynik. Bez „czarnych skrzynek", bez modeli, których współczynników nikt nie może zweryfikować, bez tajemnic metodologicznych chronionych prawem autorskim.

System nie może mieć pojedynczych punktów awarii. Jeśli źródło danych zniknie lub zostanie zmanipulowane, muszą istnieć alternatywy. Redundancja jest cechą, nie kosztem.

Każdy krok obliczenia musi być audytowalny — jawny i odtwarzalny przez osobę z odpowiednimi kwalifikacjami, bez konieczności uzyskiwania zgody projektanta systemu.

## Co Odrzucam

Wskaźniki ustalane decyzją rady (WIBOR, stopy centralne, oficjalne CPI w obecnej postaci). Systemy, w których prawda zależy od głosowania lub uznania jednego eksperta. Rozwiązania chronione tajemnicą metodologiczną. Pośredników, których nie da się wykluczyć z systemu.

## Świadomość Granic

Heliocentryczność nie stosuje się wszędzie i ślepe jej narzucanie bywa szkodliwe. Sąd interpretujący indywidualną krzywdę, lekarz dobierający terapię, redaktor wybierający istotne wątki — to obszary, gdzie ludzka uznaniowość jest cechą, nie wadą. Próba zastąpienia ich sztywną formułą produkuje gorsze wyniki, nie lepsze. Filozofia heliocentryczna stosuje się tam, gdzie *istnieje obiektywna prawda do zmierzenia* — w pomiarach, rozliczeniach, kontraktach wieloletnich, alokacjach zasobów na podstawie mierzalnych kryteriów.

Druga granica: deterministyczne reguły bez mechanizmu rewizji są kruche. Bitcoin pokazał, że niezmienność protokołu potrafi być wadą. Każdy system heliocentryczny powinien przewidywać formalną, transparentną procedurę zmiany reguł — opartą również o obserwowalne kryteria, nie o jednorazowy *fiat*.

## Motywacja: Poprawianie Świata

Te zasady to nie tylko estetyka inżynierska. Stanowią próbę odebrania kawałka świata spod władzy uznaniowych decyzji i oddania go regule, którą każdy może sprawdzić. Tradycja tego myślenia łączy Kopernika, Galileusza, Newtona, ruch open source, dziennikarstwo danych i kryptografię publiczną. To jest praca konstrukcyjna na rzecz świata bardziej sprawiedliwego — w którym ludzie nie są zdani na cudze zaufanie, gdy chcą wiedzieć, czy nie są oszukiwani.

## Jak Stosować Tę Filozofię — Lista Kontrolna dla Nowych Projektów

Przy każdym nowym pomyśle warto sprawdzić następujące pytania:

1. Czy ten problem ma obiektywną odpowiedź mierzalną z danych?
2. Czy istniejące rozwiązania są zależne od czyjegoś *fiat* — i czy ta zależność jest tu uzasadniona, czy historyczna?
3. Czy można zaprojektować deterministyczne zastąpienie?
4. Jeśli tak — jak zapewnić odporność na manipulację danymi wejściowymi i jak zabezpieczyć przed pojedynczymi punktami awarii?
5. Jaką procedurę rewizji reguł przewidujemy na wypadek wykrycia błędu w projekcie?
6. Czy autor systemu po uruchomieniu ma jakąkolwiek możliwość arbitralnego wpływu na wynik? Jeśli tak — jak to wyeliminować?

Jeśli odpowiedzi prowadzą do sensownej konstrukcji — projekt kwalifikuje się jako heliocentryczny i warto go rozwijać. Jeśli problem nie kwalifikuje się — szanujmy to i nie udawajmy obiektywności tam, gdzie jej z natury rzeczy nie ma.

---

*Wersja: 1.0. Dokument otwarty na rozwój i rewizję — zgodnie z własną filozofią.*
