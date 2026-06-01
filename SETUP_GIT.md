# Instrukcja Inicjalizacji Repozytorium Git i Publikacji na GitHubie

Ten dokument zawiera jednorazową procedurę uruchomienia kontroli wersji projektu AUV. Wykonujesz ją raz, w swoim terminalu na Macu.

## Kontekst Techniczny

W sesji Cowork pełna inicjalizacja Git napotyka ograniczenia uprawnień systemu plików (FUSE mount). Mogę tworzyć i edytować pliki w katalogu projektu, ale nie mogę ich usuwać ani w pełni zarządzać `.git/` po stronie tej sesji. Dlatego cała inicjalizacja Git oraz fizyczne usunięcie obsolete plików odbywa się w Twoim terminalu lokalnym, gdzie nie ma tych ograniczeń.

W katalogu projektu pozostała próbnie utworzona, ale niepełna podkatalog `.git/` z sesji Cowork — pierwszym krokiem jest jej usunięcie.

## Wymagania Wstępne

Sprawdź, czy masz zainstalowanego Gita:

```bash
git --version
```

Jeśli nie — zainstaluj przez Homebrew (`brew install git`) lub pobierz z https://git-scm.com.

## Krok 1 — Czyszczenie katalogu i inicjalizacja Git

W terminalu, w katalogu projektu:

```bash
cd ~/projekty/Globalny-wskaznik-wartosci

# Usuń niepełny .git utworzony przez sesję Cowork
rm -rf .git

# Usuń obsolete pliki koncepcyjne (ich treść jest skonsolidowana w AUV_zalozenia_v0.2.md)
rm -f AUV_koncepcja.md \
      AUV_zalozenia_v0.1.md \
      GAVI_Szkielet_Projektu.md \
      "Globalny Wskaźnik Wartości Bezwzględnej (GAVI) - P.pdf" \
      ModelowanieBJW.md \
      miernik_wartosci_rozwazania.md \
      uniwersalna_wartosc_specyfikacja.md

# Jeśli istnieje resztkowy plik bundla z poprzedniej próby — usuń też
rm -f auv-historia.bundle

# Inicjalizuj świeże repozytorium
git init -b main
git config user.name "Mariusz"
git config user.email "kurowskimariusz@pm.me"

# Sprawdź, co pozostało w katalogu
ls -la
```

Po wykonaniu powyższego w katalogu powinny być tylko cztery pliki:

```
.gitignore
AUV_zalozenia_v0.2.md
PROFIL_AUTORA.md
SETUP_GIT.md
```

Plus ukryty `.git/` (nowy, świeży).

## Krok 2 — Pierwszy commit

```bash
git add .
git commit -m "Stan początkowy projektu AUV

Konsolidacja po wstępnej fazie dyskusyjnej:
- AUV_zalozenia_v0.2.md — formalna specyfikacja założeń projektu
- PROFIL_AUTORA.md — filozofia heliocentryczna (cross-project)
- SETUP_GIT.md — niniejsza instrukcja
- .gitignore — wykluczenia (Python, dane, sekrety)

Wcześniejsze notatki koncepcyjne zostały skonsolidowane do v0.2 i celowo
nie wchodzą do historii Git — projekt zaczynamy od czystego stanu."
```

## Krok 3 — Utworzenie repozytorium na GitHubie

W przeglądarce:

1. Wejdź na https://github.com/new
2. Nazwa repozytorium (sugestia): `auv` lub `globalny-wskaznik-wartosci`
3. Opis (sugestia): "Absolute Unit of Value — heliocentryczna jednostka rachunkowa wyliczana z otwartych danych rynkowych"
4. **Ważne**: nie zaznaczaj "Initialize this repository with a README" ani żadnych innych checkboxów — będziemy importować istniejące lokalne repo.
5. Visibility: **public** (zgodnie z filozofią heliocentryczną — projekt powinien być audytowalny). Możesz tymczasowo wybrać "private" do czasu, gdy będziesz gotowy do publikacji.

Kliknij "Create repository".

## Krok 4 — Połączenie lokalnego repo z GitHubem

GitHub po utworzeniu pokaże komendy. Użyj wariantu "push an existing repository":

```bash
git remote add origin git@github.com:TWOJA_NAZWA/auv.git
git push -u origin main
```

Zamiast `TWOJA_NAZWA` wpisz swoją nazwę użytkownika GitHub. Jeśli GitHub poprosi o uwierzytelnienie i nie masz skonfigurowanych kluczy SSH, użyj HTTPS:

```bash
git remote add origin https://github.com/TWOJA_NAZWA/auv.git
git push -u origin main
```

GitHub poprowadzi przez procedurę uwierzytelnienia (Personal Access Token).

## Krok 5 — Weryfikacja

Po wykonaniu komend powyżej, odśwież stronę swojego repozytorium na GitHubie. Powinieneś zobaczyć cztery pliki projektu z jednym commitem w historii.

## Dalsza Praca

Od tego momentu każda zmiana w plikach projektu jest śledzona standardowo:

```bash
git add NAZWA_PLIKU
git commit -m "Krótki opis zmiany"
git push
```

Jeśli kolejna sesja Cowork wprowadzi zmiany, dane będą widoczne w katalogu po stronie Twojego Maca — wystarczy wtedy `git status`, `git add`, `git commit`, `git push`, aby zapisać do GitHuba.

## Uwaga o Historii Wcześniejszych Wersji

W poprzedniej iteracji asystent próbował utworzyć repozytorium z czterema commitami pokazującymi ewolucję projektu (notatki → profil → v0.1 → v0.2) i spakował to do pliku `auv-historia.bundle`. Plik ten zniknął między sesjami (prawdopodobnie z powodu synchronizacji folderu Cowork lub mechanizmu uprawnień FUSE), dlatego procedura powyżej jest uproszczona: jeden commit z czystego stanu. Nie tracimy wiele — ewolucja decyzji jest udokumentowana w v0.2 w sekcji "Kwestie Otwarte" i komentarzach do poszczególnych decyzji.
