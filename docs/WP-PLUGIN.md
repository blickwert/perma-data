# Plugin `bw-perma-forms` (Formulare und Kontakt-Datenbank)

Stand: Phase 2 der WordPress-Umsetzung (siehe `docs/WP-UMSETZUNG.md`). Code: `wordpress/plugins/bw-perma-forms/` (Plugin-Ordner `free/`, Aufbau nach `.claude/skills/wp-plugin-architecture`).

## Was es kann

- **Drei Formulare auf Basis von Contact Form 7:** Interessentenliste, Newsletter, Kontakt. Das Plugin legt die CF7-Formulare selbst an und hält sie aktuell (Vorlage, Mails, Meldungen). Änderungen direkt in CF7 werden überschrieben, sobald sich die Definition im Plugin ändert.
- **Block „PERMA-Formular“ (`bw/perma-form`)** mit Auswahl des Formulars und der vorausgewählten Ausbildung; die Theme-Patterns nutzen ihn. Zusätzlich Shortcode `[bw_perma_form form="interest" preselect="basic"]`.
- **Kontakt-Datenbank** statt Flamingo: eine Person pro E-Mail-Adresse, mit Status (Interessent:in, Anfrage, Mitglied, Ehemaliges Mitglied), Ausbildungen, Newsletter-Stand, Beruf, Telefon, Notizen und **frei erweiterbaren Zusatzfeldern** (für spätere Mitgliedsdaten). Jeder Formulareintrag landet zusätzlich im Verlauf der Person.
- **Dashboard › PERMA Kontakte:** Liste mit Suche und Filtern, Detailseite zum Bearbeiten (Status, Zusatzfelder, Verlauf, Löschen), **CSV-Download** (gefiltert, Excel-tauglich: UTF-8, Semikolon, Zusatzfelder als eigene Spalten), Einstellungen.
- **Newsletter über Brevo** mit Double-Opt-in durch Brevo (Brevo-Vorlage). API-Schlüssel aus dem verbundenen Brevo-Plugin oder eigener Schlüssel. Optionaler Webhook von Brevo setzt „angemeldet“ bzw. „abgemeldet“.
- **Spamschutz:** Cloudflare Turnstile über die CF7-Integration, dazu Honeypot, Mindestausfüllzeit (signierter Zeitstempel), Ratenbegrenzung pro Besucher (nur Hash der IP, in Transients), Link- und Wortfilter.
- **Datenschutz:** Checkboxen nicht vorausgewählt, keine IP-Adressen gespeichert, Anbindung an die WordPress-Werkzeuge „Personenbezogene Daten exportieren/löschen“.

## Module

| ID | Aufgabe | Braucht |
|---|---|---|
| `contacts` | Tabellen, Kontakt-Service, REST, CSV, Datenschutz-Werkzeuge | – |
| `forms` | Definitionen sammeln, CF7-Formulare anlegen, Block, Weitergabe der Einträge | – |
| `spam-protection` | Honeypot, Zeit, Rate, Inhaltsfilter | forms |
| `interest-list` | Formular Interessentenliste, Mail an Empfänger, Bestätigungsmail | forms |
| `contact` | Kontaktformular, Mail an Empfänger | forms |
| `newsletter` | Newsletter-Formular, Brevo Double-Opt-in, Webhook | forms |

Module sprechen nur über Hooks miteinander:

| Hook | Art | Wer feuert | Zweck |
|---|---|---|---|
| `bw_perma_forms_definitions` | Filter | forms | Module melden ihre Formulare an |
| `bw_perma_forms_before_submit` | Filter | forms | Eintrag ablehnen (z. B. Newsletter bei Brevo fehlgeschlagen) |
| `bw_perma_forms_submitted` | Action | forms | angenommener Eintrag (normalisierte Daten) |
| `bw_perma_forms_form_key` | Filter | forms | „Ist diese CF7-ID eines unserer Formulare?“ |
| `bw_perma_forms_newsletter_state` | Action | newsletter | Newsletter-Stand einer Adresse geändert |
| `bw_perma_forms_contact_saved`, `bw_perma_forms_contact_updated` | Action | contacts | Kontakt gespeichert/geändert |
| `bw_perma_forms_settings_updated` | Action | Core | Einstellungen gespeichert (Formulare werden neu geschrieben) |
| `bw_perma_forms_admin_data`, `bw_perma_forms_settings_response` | Filter | Core | Module ergänzen Daten der Admin-App |
| `bw_perma_forms_register_modules` | Filter | Core | weitere Module (z. B. später Mitgliederbereich) |

## Datenbank

| Tabelle | Inhalt |
|---|---|
| `{prefix}bw_perma_contacts` | eine Zeile pro Person (E-Mail eindeutig) |
| `{prefix}bw_perma_contactmeta` | Zusatzfelder (WordPress-Metadaten-API, Typ `bw_perma_contact`) |
| `{prefix}bw_perma_submissions` | Verlauf: jeder Formulareintrag mit Ausbildungen und Nachricht |

Regeln beim Zusammenführen: Namen und Beruf werden nur mit nicht leeren Werten überschrieben, Ausbildungen addieren sich, der Status geht nie zurück (ein Mitglied bleibt Mitglied; aus „Anfrage“ wird bei einem Eintrag in die Interessentenliste „Interessent:in“).

## Einrichtung auf einer Installation

1. Contact Form 7 aktivieren, dann das Plugin. Die drei CF7-Formulare entstehen beim ersten Aufruf des Dashboards.
2. **PERMA Kontakte › Einstellungen:** Empfänger (Standard `bw-cms@blickwert.at`, später `info@perma-academy.at`), Pfad der Datenschutzerklärung.
3. **Brevo:** In den Einstellungen „Brevo einrichten“ klicken: Das Plugin legt die Liste „Newsletter PERMA Mind Academy“, eine Double-Opt-in-Vorlage im PERMA-Stil (Absender: erste aktive Absenderadresse in Brevo) und den Webhook für Bestätigungen und Abmeldungen an und wählt sie aus. Wiederholen erzeugt keine Doppelten. Alternativ Liste und Vorlage in Brevo selbst anlegen und auswählen. Weiterleitung nach der Bestätigung: Seite `/newsletter-bestaetigt/`. Optional die angezeigte Webhook-Adresse in Brevo eintragen. Hat das Brevo-Konto „Autorisierte IP-Adressen“ eingeschaltet, muss die IP des Webservers dort freigegeben sein (sonst Fehler „unrecognised IP address“).
4. **Turnstile:** Schlüssel in Contact Form 7 › Integration eintragen.

## Übertragung

```bash
python3 scripts/wp_deploy.py --site perma all   # ZIPs bauen, per BW WP Bridge installieren, Seiten anlegen, SEO-Felder (Yoast) setzen
```

Zugangsdaten kommen aus `WP_PERMA_*` (Umgebung), nie aus dem Repo. Die ZIPs landen in `dist/` (nicht im Git).

## Entwicklung

```bash
cd wordpress/plugins/bw-perma-forms
composer install && composer test        # PHPUnit + Brain Monkey (27 Tests)
npm install && npm run build             # Admin-App (TypeScript) nach free/build/
npx tsc -p tsconfig.json                 # Typprüfung
python3 scripts/build-i18n.py            # deutsche Übersetzung (.po -> .mo + JSON)
```

`free/build/`, `vendor/` und `node_modules/` sind nicht im Git; vor dem Einspielen `npm run build` ausführen und den Ordner `free/` als `bw-perma-forms` zippen.

Formulartexte stehen in den Modulen (`InterestListModule`, `ContactModule`, `NewsletterModule`) und folgen `scripts/v2b_content.py`; bei Textänderungen beide anpassen.

## Geprüft (Playground, PHP 8.3, WordPress aktuell, CF7 6.2.5)

- Formulare erscheinen auf Startseite und Angebotsseiten; auf der Basic-Seite ist Basic vorausgewählt.
- Interessentenliste und Kontakt: Bestätigung erscheint, Kontakt und Verlauf werden gespeichert, Mails gehen raus (lokal abgefangen).
- Newsletter ohne Brevo-Einrichtung: verständliche Fehlermeldung, kein Eintrag „Bestätigung offen“.
- Honeypot greift (Eintrag als Spam abgelehnt).
- Dashboard: Liste, Detail, Status „Mitglied“ setzen, Zusatzfeld anlegen, CSV-Download mit Zusatzfeld-Spalte.
- 390 px: kein seitlicher Überlauf.

## Offen

- Brevo-Liste, Double-Opt-in-Vorlage und Bestätigungsseite anlegen (Auftraggeber bzw. beim Einrichten), Webhook in Brevo eintragen.
- Turnstile-Schlüssel eintragen.
- Datenschutztext: Turnstile, Brevo und die Kontakt-Datenbank (Speicherdauer) erwähnen.
