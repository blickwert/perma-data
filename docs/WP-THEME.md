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
| `patterns/*.php` (Abschnitte, ganze Seiten, Header, Footer, 404) | `scripts/v2b_content.py`, Rechtstexte aus `content/rechtstexte/impressum.html`, `datenschutz.html` |
| `assets/icons/*.svg` | `assets/icons/icons.json` + `ICONS` in `scripts/build_design_pages_v2b.py` |
| `assets/images/logo*.svg` | `design/v2b/assets/` |
| `wordpress/content/*.html`, `pages.json` (Seiteninhalte für die Übertragung, Phase 3) | wie Patterns |

Von Hand gepflegt: `style.css`, `functions.php`, `src/`, `templates/`, `parts/`, `blocks/icon/`, `assets/css/components.css`, `assets/fonts/`.

Lokale Prüfung (WordPress Playground, PHP 8.3, WordPress aktuell): Theme und `wordpress/content` einbinden, Seiten aus `pages.json` anlegen, dann Screenshots bei 1440 px und 390 px gegen `design/v2b/` vergleichen und im Editor die Gültigkeit der Blöcke prüfen. Ergebnis Phase 1: alle 25 Patterns und alle Seiten ohne ungültige Blöcke; fehlend ist nur `bw/perma-form` (kommt mit dem Plugin).

## Aufbau

- **Vorlagen:** `front-page`, `page`, `page-angebot` (Header im Akzent-Verlauf), `page-rechtliches` (wie der Abschnitt „Über uns“ der Startseite: heller Hintergrund, „Rechtliches“ und Titel links, Fließtext darunter, kein farbiger Seitenkopf), `index`, `404`.
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
| Rechtstexte | Brotkrumen, Seitenkopf mit Verlauf | ohne Brotkrumen und Seitenkopf; gestaltet wie der Abschnitt „Über uns“ der Startseite (seit 0.6.1) | Wunsch des Auftraggebers: an die Startseite angleichen |
| Komponenten-CSS | eine Datei | eine Datei (`components.css`, ca. 25 KB) statt CSS pro Block | einfacher zu pflegen; bei Bedarf später aufteilen |
| Breakpoints | 561/821/1001 px | gleich (Media Queries statt Container Queries) | Übereinstimmung mit v2b |

## Offen für Phase 2/3

- Formulare (`bw/perma-form`) im Plugin `bw-perma-forms`.
- Seiten auf der Dev-Installation aus `wordpress/content/` anlegen (Adressen `{{home:/…}}` werden dabei ersetzt), Startseite setzen, SEO-Titel und Beschreibungen (`pages.json`, Plugin oder Theme-Funktion klären).
- Platzhalter (Trainerfotos, ECQA-Logo) bleiben markiert, bis die Academy liefert.

## Hero-Bild

Seit Theme 0.3.0 hat der Hero zwei Hintergrundbilder (vom Auftraggeber geliefert): Querformat `assets/images/hero-sonnenaufgang.webp` (2000 × 750 px) ab 821 px, Hochformat `assets/images/hero-sonnenaufgang-mobil.webp` (1024 × 1536 px) darunter. Beide sind normale Bild-Blöcke (`bw-hero__image--desktop`, `bw-hero__image--mobile`) und im Editor austauschbar; das mobile Bild ist im Editor ausgeblendet und über die Listenansicht erreichbar. Beim Ausgeben fasst `src/HeroImage.php` beide zu einem `<picture>` zusammen, damit jedes Gerät nur sein Bild lädt. Dekorativ, daher ohne Alt-Text.

**Mobil (Variante B, vom Auftraggeber gewählt):** kein Textkasten; Überschrift, ein Satz (`bw-hero__lead`, erster Satz des Hero-Texts) und beide Buttons direkt auf dem Himmel, der zweite Button weiß gefüllt. Der lange Text (`bw-hero__text`) ist mobil ausgeblendet, steht aber im HTML. **Desktop:** unverändert mit blauem Textkasten.

**Schwebender Button** „Zur Interessentenliste“ (nur mobil): erscheint erst, wenn der Hero bzw. Angebotskopf aus dem Bild gescrollt ist (`assets/js/front.js`, ohne JavaScript immer sichtbar).

**Höhe mobil (seit 0.4.0):** Der Hero ist so hoch, dass der blaue Balken mit den Profilmerkmalen genau am unteren Bildschirmrand sitzt: `100svh` minus Header (`--bw-header-height`, 68 px) minus Balken (`--bw-highlights-height`, 64 px), mindestens 420 px. Auf sehr niedrigen Bildschirmen (unter 640 px Höhe) entfällt der kurze Satz.

**Profilmerkmale mobil:** Slider mit je einem Merkmal (Scroll-Snap, wischbar); blättert alle 4 Sekunden weiter, pausiert 10 Sekunden nach einer Berührung, steht still bei „Bewegung reduzieren“. Ab 821 px alle drei nebeneinander wie bisher.

Neue Bilder: Querformat mindestens 2000 px breit, Mitte ruhig (Textkasten); Hochformat mit ruhigem Himmel im oberen Drittel (Text) und Motiv unten.

## Ladezeit (Lighthouse, Startseite, Dev-Installation)

| | Handy vorher | Handy nachher | Desktop vorher | Desktop nachher |
|---|---|---|---|---|
| Leistung | 83 | 95 | 94 | 98 |
| Barrierefreiheit | 97 | 100 | 97 | 100 |
| LCP (Hero-Bild) | 4,1 s | 2,4 s | 1,2 s | 0,8 s |

Maßnahmen (Theme 0.5.0, Plugin 0.3.0):
- Hero-Bild mit `fetchpriority="high"`, `srcset` aus kleineren Fassungen (`<name>-<breite>.webp`, erzeugt von `scripts/build_theme.py`, Varianten in `HERO_VARIANTS`), `sizes`, `width`/`height` (`src/HeroImage.php`).
- Theme-Bilder (Logos) mit `width`/`height`, Footer-Logo nachgeladen (`src/ThemeImages.php`).
- `tokens.css` direkt in der Seite statt als eigene Datei.
- Das Plugin entfernt Skript und CSS des Brevo-Plugins im Frontend; damit fällt jQuery weg (Filter `bw_perma_forms_keep_brevo_frontend`).
- Etiketten (`bw-chip`) auf Kontrast ≥ 4,5:1: Schrift `navy_dark` auf Blau und Orange, Hintergrund `purple_dark` (neuer Token, Lila 9 % dunkler) bei Lila.

Offen am Server (Hoster, vor dem Livegang): Antwortzeit 0,7 s (Seiten-Cache), HTTP/2, Cache-Dauer für Bilder/CSS/JS. SEO 63 nur, weil die Dev-Seite Suchmaschinen aussperrt.
