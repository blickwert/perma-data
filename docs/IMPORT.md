# Import & Einrichtung (WordPress / Elementor)

## Voraussetzungen
- WordPress mit **Elementor** in einer Version, die den **Atomic Editor (V4)** enthält; unter *Elementor → Einstellungen → Features* die Atomic-Elemente aktivieren.
- Fonts: **Gotham** (Lizenz nötig, sonst Fallback **Montserrat**), **Roboto**, **Bickham Script Pro** (Lizenz, sonst Fallback **Great Vibes**). Fallbacks per Google Fonts oder lokal hosten (DSGVO!).

## Import
0. Templates erzeugen: `python3 scripts/build_elementor.py` (die JSON-Dateien liegen nicht im Repo).
1. *Elementor → Templates → Saved Templates → Template importieren* → `templates/elementor/full-page.json`.
2. Neue Seite mit „Elementor Canvas“/„Full Width“ anlegen, Template einfügen.
3. Alternativ Sektionen einzeln aus `01-header.json … 10-footer.json` importieren (z. B. Header/Footer ins Theme-Builder-Template).

## Nach dem Import ersetzen
- **Logo** (`assets/logo.svg`), **Hero-Hintergrundbild** (derzeit Verlauf), **Banner-Foto**, **Team-Fotos**: die `e-image`-Platzhalter sind leer.
- Platzhaltertexte in `[eckigen Klammern]` – am besten vorher in `content/content.json` pflegen und neu bauen.
- **Formular**: liegt als HTML-Widget vor (ohne Backend). Produktiv durch Elementor-Pro-Formular, WPForms, Contact Form 7 o. Ä. ersetzen; Felder/Dropdown siehe `content.kontakt`. Datenschutz-Link anpassen.
- Social-Icons im Footer, Impressum/Datenschutz-URLs.

## Bekannte Einschränkungen
- Icons und Formular sind `html`-Widgets, weil Atomic derzeit keine Icon-/Formular-Elemente bietet.
- Styles sind lokale Klassen pro Element. Später sinnvoll: Farben/Typo als **Variablen** und wiederkehrende Muster (Tag, Button-Link, Karte) als **Global Classes** anlegen (Werte: `tokens/tokens.json`).
- Das Prop-Schema der Atomic-Elemente (v. a. Hintergrund-Verlauf, Dimensions, `_cssid`) ist aus dem Elementor-Format nachgebaut und **ungetestet**; schlägt der Import fehl oder fehlen Styles, bitte Fehlermeldung/Version melden, dann wird der Generator angepasst.
