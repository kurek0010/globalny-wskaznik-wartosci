# Jak uruchomić nowe repozytorium Talenta

Ten folder to gotowy, czysty zalążek repozytorium **`talent`** — zawiera wyłącznie to, co potrzebne do zrozumienia, odtworzenia i rozwoju jednostki Talent (TLN). Odwołania do repozytorium (linki GitHub, GitHub Pages, builder) są już ustawione na nazwę `talent` i konto `kurek0010`.

Ten plik (`START_TUTAJ.md`) możesz usunąć po pierwszym pushu — to tylko instrukcja.

## 1. (Opcjonalnie) inna nazwa repo niż `talent`

Jeśli chcesz nazwać repo inaczej (np. `talent-tln`), z wnętrza folderu uruchom:

```bash
grep -rl "kurek0010/talent" . --include=*.py --include=*.md --include=*.html --include=*.yml \
  | xargs sed -i '' 's#kurek0010/talent#kurek0010/NOWA_NAZWA#g'
grep -rl "kurek0010.github.io/talent" . --include=*.md --include=*.html \
  | xargs sed -i '' 's#kurek0010.github.io/talent#kurek0010.github.io/NOWA_NAZWA#g'
```

(Na macOS `sed -i ''`; na Linuksie `sed -i`.)

## 2. Przenieś folder poza stare repo

Ten folder leży na razie wewnątrz `globalny-wskaznik-wartosci`. Przenieś go, żeby stał się osobnym projektem:

```bash
mv ~/projekty/Globalny-wskaznik-wartosci/_NOWE_REPO_talent ~/projekty/talent
cd ~/projekty/talent
```

## 3. Zainicjuj repozytorium i pierwszy commit

```bash
git init
git add .
git commit -m "Talent (TLN) — wydzielenie czystego repozytorium z globalny-wskaznik-wartosci"
git branch -M main
```

## 4. Utwórz puste repo na GitHubie i wypchnij

Na github.com utwórz **nowe, puste** repozytorium `talent` (bez README, .gitignore i licencji — masz je już w folderze). Potem:

```bash
git remote add origin https://github.com/kurek0010/talent.git
git push -u origin main
```

(Jeśli masz GitHub CLI: `gh repo create kurek0010/talent --public --source=. --remote=origin --push`.)

## 5. Po pushu — trzy rzeczy do włączenia

1. **Klucz FRED do lokalnej pracy:** `cp prototyp/.env.example prototyp/.env` i wpisz swój bezpłatny `FRED_API_KEY` (plik `.env` jest w `.gitignore`, nie trafi na GitHub).
2. **GitHub Pages:** włącz wg `INSTRUKCJA_publikacja_www.md` (Settings → Pages → gałąź `main`). Strona ruszy pod `https://kurek0010.github.io/talent/`.
3. **GitHub Actions:** w zakładce Actions włącz workflow. Comiesięczna kotwica (`publikacja_kotwicy.yml`) i automatyczna przebudowa strony (`przebudowa_strony.yml`) zaczną działać — szczegóły w `INSTRUKCJA_aktualizacji.md` → „Automatyzacja". Automat kotwicy potrzebuje sekretu `FRED_API_KEY` w Settings → Secrets → Actions.

## 6. Sprawdzenie, że pipeline działa lokalnie

```bash
cd prototyp
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/talent_daily.py     # policzy kotwice z dołączonych danych
python src/build_strona.py     # przebuduje strony HTML
```

Dane wejściowe są dołączone w `prototyp/data/`, więc obliczenia i strona działają bez pobierania czegokolwiek.
