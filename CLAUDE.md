# PERMA Mind Academy – Projektkontext für Claude

Sprache mit dem Auftraggeber: Deutsch. Auftraggeber: David (Blickwert, Graz).

## Aktuelle Aufgabe

**WordPress-Umsetzung als Block-Theme + Formular-Plugin.** Vollständige Arbeitsanweisung mit allen bereits getroffenen Entscheidungen: [`docs/WP-UMSETZUNG.md`](docs/WP-UMSETZUNG.md). Phase 0 bis 2 sind erledigt (Theme: [`docs/WP-THEME.md`](docs/WP-THEME.md), Plugin: [`docs/WP-PLUGIN.md`](docs/WP-PLUGIN.md)); weiter mit Phase 3 (Übertragung auf die Dev-Installation).

Kurz: Basis ist die Vorschau **v2b** (`design/v2b/`, Texte in `scripts/v2b_content.py`). Theme `wordpress/themes/perma-mind/`, Plugin `wordpress/plugins/bw-perma-forms/` (Contact Form 7, Turnstile, Brevo). Dev-Installation: `WP_PERMA_URL=https://dev.blickwert.at/wp/2604-perma`. Elementor wird nicht mehr verwendet.

## Regeln

- Skills in `.claude/skills/`: `wp-theme-architecture`, `wp-plugin-architecture`, `html-css-richtlinien`. Immer anwenden.
- Präfix `bw-` (CSS), `bw_` (PHP-Hooks), PHP 8.3, WordPress 7.x.
- Designwerte nur aus `tokens/tokens.v2.json` (Generatoren anpassen, nicht die erzeugten Dateien von Hand).
- Keine Schriften oder Skripte von fremden Servern (Ausnahme: Turnstile/Brevo in Formularen).
- Keine Schlüssel oder Passwörter ins Repo.

## Arbeitsweise im Repo

- Pro Änderung: Branch, Commit, Pull Request. Der Auftraggeber hat erlaubt, eigene PRs selbst zu mergen („merge meine PRs künftig selbst“). Danach Branch auf `origin/main` zurücksetzen.
- Sichtbare Änderungen vorher lokal prüfen (Chromium/Playwright, 1440 px und 390 px).
- Vorschauen werden über GitHub Pages veröffentlicht (`.github/workflows/pages.yml`): v1 `/`, v2 `/v2/`, v2b `/v2b/`. Das geht nur, solange das Repo öffentlich ist (kostenloser GitHub-Tarif); wird es privat, schaltet GitHub Pages ab und es muss danach unter Settings › Pages (Source: GitHub Actions) wieder eingeschaltet werden.
- Dokumentation in `docs/` aktuell halten (v. a. `V2B.md`, `WP-UMSETZUNG.md`).

## Wichtige Dateien

| Pfad | Zweck |
|---|---|
| `design/v2b/` | Referenz-Optik (statisch, `styles.css` mit allen `bw-`-Komponenten) |
| `scripts/v2b_content.py` | Alle Website-Texte, Seitentitel, Meta-Beschreibungen |
| `scripts/build_design_pages_v2b.py` | Seitengenerator v2b (Struktur der Abschnitte, Icons) |
| `tokens/tokens.v2.json` | Designsystem (Farben, Schriften, Größen, Abstände, Radien, Schatten) |
| `scripts/build_tokens.py` | Tokens → `tokens.css` (v2, v2b) |
| `docs/V2B.md` | Aufbau v2b, Entscheidungen, offene Punkte |
| `scripts/build_theme.py` | Tokens + Texte → theme.json, tokens.css, Patterns, Icons, Seiteninhalte des Themes |
| `docs/WP-THEME.md` | Aufbau des Block-Themes, Blockstile, Abweichungen von v2b |
| `docs/WP-PLUGIN.md` | Plugin bw-perma-forms: Module, Hooks, Kontakt-Datenbank, Einrichtung |
| `docs/PERMA-v2b-Aenderungen.docx`, `docs/PERMA-v2-Aenderungen.docx` | Änderungslisten für den Kunden |
