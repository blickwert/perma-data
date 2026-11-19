# Arbeitsanweisung: WordPress-Umsetzung (Block-Theme + Formular-Plugin)

Diese Datei ist die Aufgabe für die nächste Session. Sie enthält alle Entscheidungen, die mit dem Auftraggeber (David, Blickwert) bereits geklärt sind. Nicht neu verhandeln, sondern umsetzen; nur echte Lücken nachfragen.

## 1. Ziel

Die Website der PERMA Mind Academy aus der Vorschau **v2b** (`design/v2b/`, live: https://blickwert.github.io/perma-data/v2b/) wird als eigenes **WordPress-Block-Theme** plus eigenes **Formular-Plugin** umgesetzt und auf die Entwicklungsinstallation übertragen. Elementor wird nicht verwendet.

Ergebnis:
- Theme `perma-mind` und Plugin `bw-perma-forms` liegen im Repo unter `wordpress/` und sind auf der Dev-Installation aktiv.
- Startseite, drei Angebotsseiten, Impressum und Datenschutz sind als WordPress-Seiten angelegt und sehen aus wie v2b (Desktop und Handy).
- Formulare (Interessentenliste, Newsletter, Kontakt) funktionieren mit Spamschutz.
- Im Block-Editor müssen fast keine Designeinstellungen mehr vorgenommen werden.

## 2. Getroffene Entscheidungen

| Thema | Entscheidung |
|---|---|
| Theme-Typ | Block-Theme (FSE), Designsystem vollständig in `theme.json` + Blockstilen |
| Inhaltsbasis | v2b (Texte: `scripts/v2b_content.py`, Struktur/Optik: `design/v2b/`) |
| Ablage | Beides in diesem Repo: `wordpress/themes/perma-mind/`, `wordpress/plugins/bw-perma-forms/` |
| Präfix | `bw-` (CSS-Klassen/Variablen), `bw_` für PHP-Hooks/Optionen, Blöcke `bw/…` |
| Theme | Slug `perma-mind`, Namespace `BW\PermaMind`, Hook-Präfix `bw_perma_mind_` |
| Plugin | Slug `bw-perma-forms`, Namespace `BW\PermaForms`, Hook-/Options-Präfix `bw_perma_forms_`, Konstanten `BW_PERMA_FORMS_*`; nur Free-Teil, kein Pro |
| Server | PHP 8.3, WordPress 7.x |
| Formulare | Eigenes Plugin, aufbauend auf **Contact Form 7** |
| Spamschutz | **Cloudflare Turnstile** plus Honeypot, Mindestausfüllzeit, Ratenbegrenzung, Inhaltsfilter |
| Newsletter | **Brevo** über das **Brevo-Plugin** (Double-Opt-in über Brevo) |
| Empfänger | vorerst **bw-cms@blickwert.at**, später **info@perma-academy.at** (als Einstellung, nicht fest im Code) |
| Schriften | **Montserrat** (Überschriften, statt Gotham) und **Roboto**, lokal im Theme, keine Google Fonts |
| Icons | SVG-Dateien direkt im Theme |
| Elementor | gestrichen |
| Dev-Installation | `WP_PERMA_URL=https://dev.blickwert.at/wp/2604-perma` |

## 3. Regeln (zuerst lesen)

- `.claude/skills/wp-theme-architecture/SKILL.md` – Theme-Aufbau, theme.json als Designsystem
- `.claude/skills/wp-plugin-architecture/SKILL.md` – Plugin-Aufbau (OOP, Module, Schichten, Sicherheit)
- `.claude/skills/html-css-richtlinien/SKILL.md` – CSS-Regeln (keine Inline-Styles, Tokens, Präfix)
- `docs/V2B.md` – Aufbau und Inhalte von v2b
- `docs/CORPORATE-DESIGN-V2.md`, `docs/DESIGN-TOKENS.md` – Farben, Schriften, Kontraste

## 4. Zugang zur WordPress-Installation

- In dieser Session ist die Dev-Installation über das **Bridge-Plugin** verbunden. Zuerst prüfen, welche Werkzeuge das Bridge-Plugin bereitstellt (MCP-Tools; Liste der verfügbaren Tools ansehen) und was sie können: Dateien hochladen, Plugins/Themes installieren und aktivieren, Seiten anlegen, Optionen setzen, WP-CLI o. Ä.
- Die URL steht als `WP_PERMA_URL` zur Verfügung (siehe oben). Zugangsdaten und API-Schlüssel (Turnstile, Brevo) **nie** ins Repo schreiben; sie werden in WordPress eingetragen. Fehlt ein Schlüssel, den Auftraggeber fragen.
- Es ist eine Entwicklungsinstallation. Trotzdem: vor dem Löschen oder Überschreiben vorhandener Inhalte nachsehen, was es ist, und im Zweifel fragen.

## 5. Ablauf

### Phase 0 – Bestandsaufnahme (nichts ändern)
1. Repo-Stand lesen (Abschnitt 3), v2b lokal ansehen (`cd design/v2b && python3 -m http.server`).
2. Über das Bridge-Plugin erfassen: WordPress-Version, aktives Theme, installierte/aktive Plugins (Contact Form 7? Version; Brevo-Plugin? Flamingo? SEO-Plugin?), Permalink-Struktur, vorhandene Seiten/Menüs, Mail-Versand (SMTP-Plugin?).
3. Prüfen, ob die verwendete CF7-Version Cloudflare Turnstile selbst unterstützt (Integration in CF7) und ob das Brevo-Plugin eine CF7-Anbindung oder eine eigene Formular-/Listen-Funktion mitbringt. Danach entscheiden, was das Plugin selbst bauen muss (Abschnitt 7).
4. Ergebnis kurz dem Auftraggeber melden, mit dem konkreten Umsetzungsplan.

**Ergebnis Phase 0 (19. November 2026):**
- Dev-Installation: WordPress 7.1.5, PHP auf 8.3 umgestellt, Sprache Deutsch, Permalinks `/%postname%/`, Suchmaschinen ausgesperrt.
- Aufgeräumt: alte Elementor-Plugins und Hello-Themes gelöscht. Behalten: ACF Pro und CookieYes (inaktiv), UpdraftPlus (aktiv).
- Installiert: Contact Form 7 6.2.5, Brevo-Plugin 3.3.6 (für An- und Abmeldung zum Newsletter; mit dem Brevo-Konto verbunden). Kein SMTP- und kein SEO-Plugin.
- CF7 bringt Cloudflare Turnstile selbst mit → das Plugin nutzt die CF7-Integration und ergänzt Honeypot, Mindestzeit, Ratenbegrenzung, Inhaltsfilter.
- CF7 kann Kontakte in Brevo-Listen eintragen, die Bestätigung (Double-Opt-in) liefe aber über WordPress-Mails. Das Brevo-Plugin hat keine CF7-Anbindung. → Das Newsletter-Modul ruft die Brevo-API selbst auf (`/contacts/doubleOptinConfirmation`, Bestätigung mit Brevo-Vorlage).
- GitHub Pages ist seit dem Umstellen des Repos auf privat nicht mehr erreichbar; Vergleich lokal mit `design/v2b/`.

### Phase 1 – Theme im Repo bauen (`wordpress/themes/perma-mind/`)
Siehe Abschnitt 6. Lokal prüfen, z. B. mit WordPress Playground (`npx @wp-playground/cli server --mount=...`), falls im Container verfügbar; sonst direkt auf der Dev-Installation.

**Stand:** Theme gebaut und lokal in Playground geprüft. Aufbau, Generator (`scripts/build_theme.py`), Blockstile und Abweichungen von v2b: [`docs/WP-THEME.md`](WP-THEME.md).

### Phase 2 – Plugin im Repo bauen (`wordpress/plugins/bw-perma-forms/`)
Siehe Abschnitt 7. Unit-Tests für die Services (PHPUnit + Brain Monkey laut Plugin-Skill).

### Phase 3 – Übertragung auf die Dev-Installation
1. Theme und Plugin installieren und aktivieren (über das Bridge-Plugin, z. B. als ZIP).
2. Seiten anlegen (Slugs aus Abschnitt 8), Startseite als statische Startseite setzen, Navigation (mit Untermenü „Ausbildungen“) und Footer-Links einrichten.
3. Inhalte aus den Patterns einsetzen (Texte aus `scripts/v2b_content.py`), Seitentitel und Meta-Beschreibungen setzen (SEO-Plugin, falls vorhanden; sonst Auftraggeber fragen).
4. CF7-Formulare anlegen (vom Plugin bereitgestellt), Empfänger `bw-cms@blickwert.at`, Turnstile- und Brevo-Schlüssel eintragen lassen bzw. eintragen.
5. Testeinträge für alle drei Formulare absenden, Mails und Brevo-Eingang prüfen, Testdaten danach löschen.

### Phase 4 – Abnahme
- Screenshot-Vergleich je Seite gegen v2b bei 1440 px und 390 px (Startseite, drei Angebotsseiten, Impressum, Datenschutz).
- Editor-Test: Neue Seite aus Patterns zusammensetzen, ohne Designeinstellungen; Texte ändern; Stile wechseln.
- Checkliste Abschnitt 9 abhaken, Ergebnis und offene Punkte melden.

## 6. Theme `perma-mind` – Inhalt

**Designsystem (`theme.json`, erzeugt):** neues Skript `scripts/build_theme_json.py` liest `tokens/tokens.v2.json` und schreibt `wordpress/themes/perma-mind/theme.json`.
- Palette: alle Farben aus `color` (navy, navy-dark, blue, blue-dark, purple, orange, green, red, white, off-white, mint, mist, slate, silver, graphite, sky, sky-light, dawn-purple, dawn-orange, blue-deep, purple-deep, orange-deep, green-deep). `blue_glass` und `placeholder` nur als `custom`.
- Verläufe: Hero (sky → sky-light → dawn-purple → dawn-orange, 180°), Seitenkopf (sky → sky-light → mint), vier Akzent-Verläufe (`<akzent>-deep` → navy-dark, 135°), Footer-Streifen (fünf CD-Farben).
- Schriften: Montserrat 500 (Überschriften), Roboto 300/400/500 + 300 kursiv (Text), lokal als woff2 mit Lizenz (z. B. aus den npm-Paketen `@fontsource/montserrat`, `@fontsource/roboto`, OFL/Apache 2.0).
- Schriftgrößen: `xs 12, base 16, lg 18, xl 22, 2xl 26, 3xl 32, 4xl 36, 5xl 48` (mobil kleiner: 3xl 26, 4xl 28, 5xl 38 → als `fluid` bzw. `clamp()`).
- Abstände: Skala `--bw-space-N = N × 0,25 rem` (1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24).
- Radien (card 12, pill 999, sm 6, md 8), Schatten (card, pop, menu), Inhaltsbreite 1200 px, Seitenrand 32/20 px.
- Freie Farben, freie Schriftgrößen und Standard-Paletten von WordPress abschalten.
- `styles`: Grundtypografie (Roboto, Navy, Zeilenhöhe 1.7), H1–H4 (Montserrat 500), Links, Buttons (Primär navy, Pillenform), `core/details` als Akkordeon (Plus-Symbol), `core/quote`, `core/navigation`, `core/list`, `core/separator`, Fokus sichtbar.

**Blockstil-Varianten** (Auswahl im Editor statt Einstellungen):
- Abschnitte (`core/group`): Mint, Neutral, Navy, Hero-Verlauf, Seitenkopf-Verlauf, Akzent-Verlauf blau/lila/orange/grün.
- Karten (`core/group`/`core/column`): Karte hell mit Schatten, Karte mit farbiger Linie oben, Angebotskarte dunkel im Akzent.
- Buttons: Primär, Sekundär (Kontur), Hell, Akzent (Verlauf blau), Link mit Pfeil.
- Listen: Fakten mit Punkt in Akzentfarbe, Kontaktliste mit Icons.
- Akzent als eigene Variante (`is-style-accent-blue|purple|orange|green|red`), die `--bw-accent`, `--bw-on-accent`, `--bw-accent-deep` setzt.

**Vorlagen und Teile:** `front-page.html`, `page.html`, `page-angebot.html` (Header im Akzent-Verlauf, Akzent pro Seite wählbar), `index.html`, `404.html`; Teile `header.html` (weiß, Logo, Navigation mit Untermenü „Ausbildungen“, Button „Zur Interessentenliste“), `header-akzent.html` (Verlauf, weißes Logo, helle Navigation), `footer.html` (navy-dark, Farbstreifen, Logo weiß, Kontakt, Social, Links Kontakt · Newsletter · Impressum · Datenschutz).

**Patterns** (je ein Abschnitt aus v2b, Kategorie `perma-mind`): Hero, Profilmerkmale, Einleitung, Warum PERMA Mind Academy, Angebotskarten (3), Positive Psychologie verstehen + PERMA-Modell, Vom Verstehen zum Anwenden (4 Schritte), Über uns + Trainer (Profil aufklappbar, Zitat), ECQA-Zertifizierung, Interessentenliste (Platz für das Plugin-Formular), FAQ, Newsletter, Kontakt, Angebotskopf, Eckdaten-Karte, Module (aufklappbar), Umfang und Abschluss, Weiterführende Links, schwebender Button (nur mobil).

**Eigene Blöcke:** `bw/icon` (Symbol aus `assets/icons/`, Größe, Akzent; serverseitig gerendert). Weitere nur, wenn Core-Blöcke + Stile nicht reichen (z. B. Eckdaten-Karte, falls `core/group` + Liste nicht genügt).

**Icons:** aus `assets/icons/` dieses Repos plus die in `scripts/build_design_pages_v2b.py` (`ICONS.update`) definierten (mail, phone, pin, globe, badge, chevron, arrow, heart, user, check) als SVG nach `wordpress/themes/perma-mind/assets/icons/`.

**Logos:** `design/v2b/assets/logo.svg`, `logo-white.svg`.

## 7. Plugin `bw-perma-forms` – Inhalt

Aufbau nach `wp-plugin-architecture` (nur `free/`-Teil, Module, Schichten, Tests). Abhängigkeit: Contact Form 7 (bei fehlendem CF7 Hinweis im Admin, nichts kaputt machen).

**Module:**
- `interest-list` (Interessentenliste): CF7-Formular mit Vorname, Nachname, E-Mail (Pflicht), Mehrfachauswahl „Ich interessiere mich für“ (Positive Psychology Basic / Positive Psychology Advanced / PERMA Clinical Expert, mindestens eine Pflicht), Beruf oder bisherige Ausbildung (optional), Nachricht (optional), freiwillige Newsletter-Checkbox (nicht vorausgewählt). Auf Angebotsseiten ist der jeweilige Lehrgang vorausgewählt (z. B. über Shortcode-/Block-Attribut oder Seitenkontext). Hinweistext, Button „Unverbindlich eintragen“, Bestätigungstext und Bestätigungsmail laut `scripts/v2b_content.py` (`LIST`) bzw. Kundendokument Abschnitt 7. Einträge nach Ausbildung zuordnen. Bei angehakter Newsletter-Checkbox an das Newsletter-Modul übergeben (eigener Hook, kein direkter Modulaufruf).
- `newsletter`: E-Mail (Pflicht), Vorname (optional), Einwilligung (Pflicht), Button „Newsletter abonnieren“; Anmeldung an **Brevo** über das Brevo-Plugin bzw. dessen API, **Double-Opt-in über Brevo** (Liste und DOI-Vorlage in Brevo). Texte laut `NEWSLETTER` in `scripts/v2b_content.py`.
- `contact`: Name, E-Mail, Nachricht, Datenschutz-Hinweis mit Link, Button „Nachricht senden“, Erfolgsmeldung laut `CONTACT`.
- `spam-protection`: Cloudflare Turnstile (CF7-Integration nutzen, falls vorhanden, sonst eigene Prüfung), Honeypot-Feld, Mindestausfüllzeit, Ratenbegrenzung pro IP (Transients), Inhaltsfilter (Anzahl Links, Sperrwörter). Für alle drei Formulare.
- `settings`: Empfängeradresse (Standard `bw-cms@blickwert.at`, später `info@perma-academy.at`), Brevo-Liste, Spam-Schwellen. Keine Schlüssel im Code.
- Optional `entries`: Speichern der Einträge (eigener Beitragstyp) mit Löschfrist, falls der Auftraggeber das will (nachfragen; sonst Flamingo prüfen).

**Ausgabe:** Formular-Markup und CSS passend zum Theme (`bw-form*`-Klassen aus `design/v2b/styles.css`, Farben über CSS-Variablen des Themes). Ein Block oder Shortcode pro Formular, damit es in den Theme-Patterns platziert werden kann. Erfolgsmeldung erst nach erfolgreicher Übermittlung.

**Datenschutz:** Checkboxen nicht vorausgewählt, Newsletter nur mit Double-Opt-in, Turnstile im Datenschutztext erwähnen (Hinweis an Auftraggeber), keine Daten in Logs.

## 8. Seiten

| Seite | Slug | Vorlage | Titel (SEO) | Meta-Beschreibung |
|---|---|---|---|---|
| Startseite | `/` | front-page | Positive Psychologie Ausbildung \| PERMA Mind Academy | siehe `META["index"]` in `scripts/v2b_content.py` |
| Basic | `/positive-psychologie-basic/` | page-angebot (Akzent blau) | `META["basic"]` | `META["basic"]` |
| Advanced | `/positive-psychologie-advanced/` | page-angebot (Akzent lila) | `META["advanced"]` | `META["advanced"]` |
| Clinical Expert | `/klinische-positive-psychologie/` | page-angebot (Akzent orange) | `META["clinical"]` | `META["clinical"]` |
| Impressum | `/impressum/` | page | Impressum \| PERMA Mind Academy | – |
| Datenschutz | `/datenschutz/` | page | Datenschutz \| PERMA Mind Academy | – |

Sprungziele auf der Startseite: `#ausbildungen`, `#ueber-uns`, `#zertifizierung`, `#interessentenliste`, `#fragen`, `#newsletter`, `#kontakt`. Impressum- und Datenschutztext vorerst aus v2b (Entwurf, „Sie“-Form); die endgültigen Texte liefert die Academy.

## 9. Abnahme-Checkliste

- [ ] Alle Seiten sehen bei 1440 px und 390 px aus wie v2b (Abweichungen dokumentiert und begründet)
- [ ] Keine Inline-Styles mit Rohwerten in Patterns/Vorlagen, keine freien Farben im Editor
- [ ] Neue Seite nur aus Patterns und Stilen baubar, ohne Designeinstellungen
- [ ] Schriften lokal, keine Anfragen an Google oder andere fremde Server (außer Turnstile/Brevo bei Formularen)
- [ ] Je Seite eine H1, Überschriften-Hierarchie korrekt, Akkordeons per Tastatur bedienbar
- [ ] Alle drei Formulare senden, Mails an bw-cms@blickwert.at, Newsletter landet in Brevo (DOI), Spamschutz greift
- [ ] `php -l` grün, Plugin-Tests grün, keine PHP-Warnungen im Debug-Log
- [ ] `CLAUDE.md` und diese Datei auf den neuen Stand gebracht (erledigt / offen)

## 10. Offene Inhalte (nicht blockierend)

Hero-Bild, Trainerfotos, ECQA-Logo (freigegebene Version), Termine/Orte/Fristen/Zertifizierungsgebühren, endgültige Rechtstexte, Status der Fortbildungsanerkennung für Clinical Expert. Platzhalter bleiben sichtbar markiert, bis die Academy liefert.
