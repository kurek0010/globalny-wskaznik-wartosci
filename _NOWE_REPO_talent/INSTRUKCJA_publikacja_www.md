# Instrukcja: publikacja strony (GitHub Pages + własna domena)

*Notatka na później — do wykonania, gdy strona będzie gotowa do szerszej publikacji.*

## 1. GitHub Pages (darmowy hosting — być może już włączone)

1. Wejdź: https://github.com/kurek0010/talent/settings/pages (Settings **repozytorium**, nie konta → Pages).
2. Build and deployment → Source: **Deploy from a branch** → Branch: **main**, folder **/ (root)** → Save.
3. Po 1–2 min strona działa pod: https://kurek0010.github.io/talent/
4. Każdy `git push` automatycznie aktualizuje stronę. Po przeliczeniu danych: `python prototyp/src/build_strona.py` → commit → push.

## 2. Własna domena (koszt: tylko domena, ~50–100 zł/rok)

**Zakup:** rejestrator np. OVH, home.pl, nazwa.pl lub Cloudflare Registrar (ceny hurtowe). Strategia: **jedna domena, projekty na subdomenach** — np. `talent.twojadomena.pl`, `demokracja.twojadomena.pl` — jedna opłata, wiele stron.

**Konfiguracja DNS (u rejestratora):**
- subdomena: rekord **CNAME** → `talent` wskazuje na `kurek0010.github.io`
- domena główna (bez subdomeny): 4 rekordy **A** na adresy IP GitHub Pages: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (sprawdź aktualność w docs.github.com/pages)

**Konfiguracja GitHub (w repozytorium):**
1. Settings → Pages → **Custom domain**: wpisz np. `talent.twojadomena.pl` → Save.
2. Gdy pojawi się opcja, zaznacz **Enforce HTTPS** (darmowy certyfikat, wystawia się do ~24 h).
3. GitHub utworzy w repo plik `CNAME` — ma tam zostać (builder strony go nie nadpisuje).

**Weryfikacja domeny (zabezpieczenie):** Settings **konta** → Pages → Verified domains → Add a domain → dodaj rekord TXT wg instrukcji. Blokuje innym użytkownikom GitHuba podpięcie Twojej domeny pod ich strony.

**Propagacja DNS:** od kilku minut do 24 h. Sprawdzenie: `dig talent.twojadomena.pl +short` powinno zwrócić `kurek0010.github.io` (CNAME) lub IP GitHuba.

## 3. Gdy projektów będzie więcej

- Każdy projekt = osobne repozytorium + osobna subdomena.
- Opcjonalny „hub" pod adresem głównym: repozytorium o nazwie `kurek0010.github.io` (strona wizytówka linkująca projekty).
- Strony z dużą ilością tekstu (np. Demokracja Świadoma): generator statyczny **MkDocs Material** (zbiory dokumentów md) lub **Hugo** (eseje/blog) — piszesz w Markdownie, jak dotąd.
- Alternatywy hostingu, gdyby Pages nie wystarczył: Cloudflare Pages, Netlify (ten sam model repo→strona).
