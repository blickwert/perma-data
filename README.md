# PERMA Mind Academy – Landingpage-Template (WordPress / Elementor Atomic)

Template-Projekt für die Landingpage der **PERMA Mind Academy** („We create wellbeing“).
Ziel: ein wiederverwendbares Elementor-Template, gebaut mit den **Atomic Elements** (Elementor Editor V4:
`e-flexbox`, `e-div-block`, `e-heading`, `e-paragraph`, `e-button`, `e-image`).

> **Status:** Entwurf. Die JSON-Templates werden aus Design-Tokens + Inhalt generiert und sind
> **noch nicht in einer echten Elementor-Installation getestet** (siehe „Offene Punkte“).

## Struktur

| Pfad | Inhalt |
|---|---|
| `design/reference/` | Original-Mockup (Export aus dem Design-Tool, nur Referenz). Ansehen: `cd design/reference && python3 -m http.server`, dann `Main.dc.html` öffnen |
| `tokens/tokens.json` | Farben, Fonts, Radien, Schatten, Layout, Breakpoints |
| `content/content.json` | Alle Texte inkl. `[Platzhalter]` – hier pflegen, nicht in den JSONs |
| `assets/` | `logo.svg`, Icons (`icons/*.svg`, Lucide-Stil) |
| `scripts/build_elementor.py` | Generator: Tokens + Inhalt → Elementor-JSON |
| `templates/elementor/` | Ergebnis: je Sektion eine Datei + `full-page.json` |
| `docs/` | Seitenbriefing, Import-Anleitung, Design-Hinweise |

## Build

```bash
python3 scripts/build_elementor.py   # keine Abhängigkeiten, Python 3.8+
```

## Import in WordPress

Siehe [`docs/IMPORT.md`](docs/IMPORT.md). Kurz: Elementor-Atomic-Editor aktivieren →
Templates → Importieren → `templates/elementor/full-page.json` (oder einzelne Sektionen).

## Seitenaufbau

1. Header (sticky) · 2. Hero · 3. Intro · 4. Unser Angebot (4 Kacheln) · 5. Ausbildungen & Module (4 Zeilen + Zertifikat-Banner)
6. Vorteile (6 Icons) · 7. „Sorgfalt vor großen Versprechen“ · 8. Team (2 Karten) · 9. Kontakt & Vormerkung (Formular) · 10. Footer

Der Mockup enthält zusätzlich zum Briefing die Sektionen **Intro** (mit Kennzahlen 4 / 5), **Sorgfalt**, den
**Zertifikat-Banner** und einen **schwebenden Kontakt-Button**; sie sind übernommen, aber leicht entfernbar
(Sektionsdatei weglassen bzw. aus `SECTIONS` im Generator streichen).

## Offene Inhalte (aus dem Briefing)

1. Modulnamen, Reihenfolge und **Dauer** der vier Module bestätigen.
2. Welche **Anerkennung/Zertifizierung** besteht tatsächlich? Bis dahin stehen `[Anerkennung bestätigen]`-Platzhalter – keine Aussage erfinden.
3. **Team**: Namen, Titel, Werdegang; Zitate sind Entwürfe.
4. Adresse, Telefon, E-Mail, Social-Links, Impressum/Datenschutz-URLs.
