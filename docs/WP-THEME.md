# Theme `perma-mind` (Block-Theme, Design v2b)

Stand: Phase 1 der WordPress-Umsetzung (siehe `docs/WP-UMSETZUNG.md`). Das Theme bildet die Vorschau v2b (`design/v2b/`) mit Core-Blöcken nach.

## Erzeugen und prüfen

```bash
python3 scripts/build_theme.py
```

Der Generator schreibt alles, was aus Tokens und Texten folgt. Diese Dateien nicht von Hand ändern:

| Erzeugt | Quelle |
|---|---|
| `theme.json` (Palette, Verläufe, Schriften, Größen, Abstände, Schatten, Elemente) | `tokens/tokens.v2.json` |
| `assets/css/tokens.css` (`--bw-*` zeigt auf die theme.json-Presets) | `tokens/tokens.v2.json` |
| `patterns/*.php` (Abschnitte, ganze Seiten, Header, Footer, 404) | `scripts/v2b_content.py`, Rechtstexte aus `design/v2/impressum.html`, `datenschutz.html` |
| `assets/icons/*.svg` | `assets/icons/icons.json` + `ICONS` in `scripts/build_design_pages_v2b.py` |
| `assets/images/logo*.svg` | `design/v2b/assets/` |
| `wordpress/content/*.html`, `pages.json` (Seiteninhalte für die Übertragung, Phase 3) | wie Patterns |

Von Hand gepflegt: `style.css`, `functions.php`, `src/`, `templates/`, `parts/`, `blocks/icon/`, `assets/css/components.css`, `assets/fonts/`.

Lokale Prüfung (WordPress Playground, PHP 8.3, WordPress aktuell): Theme und `wordpress/content` einbinden, Seiten aus `pages.json` anlegen, dann Screenshots bei 1440 px und 390 px gegen `design/v2b/` vergleichen und im Editor die Gültigkeit der Blöcke prüfen. Ergebnis Phase 1: alle 25 Patterns und alle Seiten ohne ungültige Blöcke; fehlend ist nur `bw/perma-form` (kommt mit dem Plugin).

## Aufbau

- **Vorlagen:** `front-page`, `page`, `page-angebot` (Header im Akzent-Verlauf), `page-rechtliches` (Seitenkopf mit Titel, Fließtext), `index`, `404`.
- **Vorlagenteile:** `header`, `header-akzent`, `footer`. Sie enthalten je ein Pattern, damit Adressen (`home_url()`) und Logos (`get_theme_file_uri()`) auf jeder Installation stimmen.
- **Patterns (Kategorie „PERMA Mind: Abschnitte“):** Hero, Profilmerkmale, Einleitung, Warum PERMA Mind Academy, Angebotskarten, Verstehen + PERMA-Modell + Vom Verstehen zum Anwenden, Über uns + Trainer, ECQA-Zertifizierung, Interessentenliste, Häufige Fragen, Newsletter, Kontakt, Angebotskopf, Angebot (Module, Umfang, Eckdaten, Weiterführend), Interessentenliste für ein Angebot.
- **Seiten-Patterns (Kategorie „PERMA Mind: Seiten“):** Startseite, Basic, Advanced, Clinical Expert, Impressum, Datenschutz. Sie erscheinen beim Anlegen einer neuen Seite zur Auswahl.
- **Eigener Block `bw/icon`:** Symbol aus `assets/icons/`, serverseitig gerendert, Farbe aus der Akzentfarbe. Editor ohne Build-Schritt (`blocks/icon/editor.js`).
- **Formulare:** Platzhalter-Block `bw/perma-form` (`form`: `interest` | `newsletter` | `contact`, `preselect`: `basic` | `advanced` | `clinical`). Ihn registriert das Plugin `bw-perma-forms` (siehe `docs/WP-PLUGIN.md`); ohne Plugin bleibt die Stelle leer.

## Blockstile (Auswahl im Editor statt Einstellungen)

| Block | Stile |
|---|---|
| Gruppe | Abschnitt Mint, Abschnitt Neutral, Abschnitt Navy, Hero-Verlauf, Seitenkopf-Verlauf, Akzent Blau/Lila/Orange/Grün/Rot |
| Button | Standard (Navy), Sekundär (Kontur), Hell, Akzent (Verlauf), Link mit Pfeil |
| Liste | Fakten (Punkt in Akzentfarbe), Schritte (nummeriert 01, 02 …), PERMA-Liste (Buchstabe fett vorne) |
| Details | immer als Akkordeon mit Plus-Symbol |
| Zitat | immer im Stil der Trainerprofile |

Der Akzent-Stil setzt `--bw-accent`, `--bw-on-accent` und `--bw-accent-deep`. Auf Angebotsseiten übernimmt der Header den Akzent des Angebotskopfs (`body:has(.bw-page-hero--offer.is-style-accent-…)`).

Im Editor sind freie Farben, Verläufe, Schriftgrößen, Abstände und Rahmen abgeschaltet.

## Abweichungen von v2b (bewusst)

| Stelle | v2b | Theme | Grund |
|---|---|---|---|
| Akkordeon-Titel | `h3` im `summary` | Text im `summary` (core/details) | core/details erlaubt keine Überschrift im Titel |
| Profilmerkmale, Kontaktliste, Eckdaten | `ul`/`dl` | Gruppen mit Absätzen | Symbol pro Eintrag; `dl` gibt es als Block nicht |
| Schritte | `h3` je Schritt | Listenpunkte, Nummer per CSS | als Liste bearbeitbar |
| Mobile Navigation | Aufklappfeld unter dem Header | Vollbild-Menü von core/navigation (bis 1000 px) | Core-Block, per Tastatur bedienbar |
| Rechtstexte | Brotkrumen „Startseite / Impressum“ | ohne Brotkrumen; Einleitung (Datenschutz) steht über dem Text | Seitenkopf kommt aus der Vorlage |
| Komponenten-CSS | eine Datei | eine Datei (`components.css`, ca. 25 KB) statt CSS pro Block | einfacher zu pflegen; bei Bedarf später aufteilen |
| Breakpoints | 561/821/1001 px | gleich (Media Queries statt Container Queries) | Übereinstimmung mit v2b |

## Offen für Phase 2/3

- Formulare (`bw/perma-form`) im Plugin `bw-perma-forms`.
- Seiten auf der Dev-Installation aus `wordpress/content/` anlegen (Adressen `{{home:/…}}` werden dabei ersetzt), Startseite setzen, SEO-Titel und Beschreibungen (`pages.json`, Plugin oder Theme-Funktion klären).
- Platzhalter (Trainerfotos, ECQA-Logo) bleiben markiert, bis die Academy liefert.

## Hero-Bild

Seit Theme 0.2.0 liegt im Hero ein Hintergrundbild (`assets/images/hero-sonnenaufgang.webp`, Steinturm im Sonnenaufgang, 2000 × 750 px, vom Auftraggeber geliefert). Es ist ein normaler Bild-Block (`bw-hero__image`) und lässt sich im Editor austauschen; dekorativ, daher ohne Alt-Text. Der Hero-Verlauf bleibt als Hintergrund, falls kein Bild gesetzt ist. Ausschnitt: Desktop mittig, mobil nach links verschoben (Steinturm). Neues Bild: mindestens 2000 px breit, WebP, Motiv links und rechts, Mitte ruhig (dort liegt der Textkasten).
