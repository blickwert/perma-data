# Übergabenotiz: Export nach WordPress / Elementor

Stand: Design v2 ist fertig klassenbasiert (Präfix `bw-`). Der Export wurde noch nicht gebaut.
Diese Notiz ist für die Session, in der Zugriff auf WordPress (Bridge-Plugin) besteht. Alles mit **[prüfen]** ist eine Annahme und wird dort an der echten Installation verifiziert, nicht aus dem Gedächtnis übernommen.

## 1. Ausgangslage im Repo

| Was | Wo |
|---|---|
| Startseite (Quelle der Struktur) | `design/v2/Main.dc.html` (nur `bw-`-Klassen, 0 Inline-Styles) |
| Komponenten-CSS | `design/v2/styles.css` (mobile-first, Breakpoints 561 / 821 / 1001 px) |
| Design-Tokens (Quelle) | `tokens/tokens.v2.json` → `design/v2/tokens.css` (`scripts/build_tokens.py v2`) |
| Unterseiten | `scripts/build_design_pages_v2.py` → Kontakt, Impressum, Datenschutz |
| Regeln fürs CSS | `.claude/skills/html-css-richtlinien/SKILL.md` |
| Corporate Design | `docs/CORPORATE-DESIGN-V2.md` |
| Altes Export-Skript | `scripts/build_elementor.py` (nur v1, nicht weiterpflegen; Export direkt gegen WordPress aufbauen) |

## 2. Entscheidungen, die schon gefallen sind

- Präfix überall `bw-`.
- Farben und Schriften bleiben in der Vorschau konkrete Werte in `:root`. Das Mapping auf Elementor-Globals (`--e-global-color-*`, `--e-global-typography-*`) passiert erst beim Export.
- Die Schriften steuert später das Elementor Design System. Gotham und Roboto kommen dann von dort, nicht aus `styles.css`.
- Die Abstandsskala `--bw-space-N` (N × 0,25 rem) darf bei Bedarf erweitert werden.
- Optik zählt: Elementor-Standardwerte sollen die Gestaltung nicht überschreiben.

## 3. Elementor-Basis-CSS: was kommt mit, was kann weg?

Ziel: Elementor und das Theme sollen möglichst kein eigenes Aussehen mitbringen, das wir dann überschreiben müssen (Beispiel: die blaue Standard-Button-Farbe, die immer geladen wird). Zuerst messen, dann abschalten.

**Erst analysieren [prüfen]**
1. Welche Elementor-Version, welches Theme (Hello Elementor oder anderes), welche Experimente sind aktiv (atomare Elemente, "Optimized Markup", "Improved CSS Loading", "Inline Font Icons")?
2. Welche CSS-Dateien lädt die Startseite tatsächlich (Elementor-Frontend, `widget-*.css`, Kit-CSS, Seiten-CSS, Theme-CSS, Plugins)? Größe, Reihenfolge, was davon ungenutzt ist.
3. Woher kommt die Standard-Buttonfarbe? Kandidaten: die Standard-Globals des Elementor-Kits (Primär, Sekundär, Text, Akzent), die Button-Einstellungen im Kit, die Theme-Stile (z. B. Reset/Theme-CSS von Hello). Mit dem Inspektor am echten Button nachweisen, nicht raten.

**Mögliche Hebel [prüfen, ob in dieser Version vorhanden]**
- Elementor-Kit anpassen: Globale Farben auf unsere Palette setzen, Button- und Typografie-Standards im Kit auf unsere Werte stellen. Das ist der saubere Weg, statt zu überschreiben.
- Standardfarben und -schriften von Elementor abschalten (Einstellung in Elementor, je nach Version unter Einstellungen oder Website-Einstellungen).
- Theme-Stile abschalten (bei Hello Elementor per Filter oder Einstellung, Reset und Theme-CSS getrennt).
- CSS-Optimierungen von Elementor: Laden nur der benutzten Widget-CSS, optimiertes Markup (weniger Wrapper), Inline-CSS statt Einzeldateien.
- Nicht genutzte Widgets und Funktionen deaktivieren, wenn nichts davon gebraucht wird.
- Nur im Notfall überschreiben, dann in einem eigenen, kommentierten Block "Elementor-Overrides" am Ende von `styles.css` (Regel aus dem Skill: `!important` nur dort und nur kommentiert).

**Entscheidungsregel:** Erst Kit/Globals auf unsere Tokens umstellen, dann Standardstile abschalten, erst zuletzt überschreiben. Jede Abschaltung einzeln testen und dokumentieren (Was wurde abgeschaltet, warum, welche Seite blieb unverändert?).

## 4. Mapping Tokens → Elementor

| Token (v2) | Ziel in Elementor [prüfen] |
|---|---|
| Palette `navy`, `blue`, `purple`, `orange`, `green`, `red`, … | Global Colors (feste Namen, Rollen wie Primär/Text/Akzent sinnvoll belegen) |
| `--bw-font-heading` (Gotham, Fallback Montserrat), `--bw-font-body` (Roboto) | Global Fonts (Primär/Text); Gotham ist lizenzpflichtig, bis dahin Montserrat |
| Schriftgrößen `--bw-fs-*` (inkl. mobile Werte), Gewichte, Zeilenhöhen | Global Typography bzw. globale Klassen |
| `--bw-space-*`, Radien, Schatten | globale Variablen oder CSS in `styles.css` (prüfen, was Elementor in dieser Version als Variablen kennt) |

Beim Export bleiben die `bw-`-Variablen bestehen und zeigen auf die Elementor-Globals (`--bw-color-primary: var(--e-global-color-primary)` usw.), damit `styles.css` unverändert weiterläuft.

## 5. Struktur nachbauen

- Elementor setzt eigene Wrapper um jedes Widget. Die Struktur wird dort nachgebaut, die `bw-`-Klassen kommen in das Feld "CSS-Klassen" bzw. als globale Klassen. Pro Element reichen 1 bis 3 Klassen.
- Die Abschnitte der Startseite in der Reihenfolge: Header/Navigation, Hero, Intro, Angebot, Ausbildungen & Module (inkl. Zertifikat-Banner), Warum PERMA Mind Academy, Team, Kontakt-Teaser, Footer, Kontakt-Button (fix unten rechts).
- Akzentfarben laufen über die Utility-Klassen `bw-accent--blue|purple|orange|green` (setzen `--bw-accent`, `--bw-on-accent`, `--bw-accent-deep`).
- Unterseiten: Kontakt (Hero, Kontaktliste, Ansprechperson, Hinweis, Schritte, Formular), Impressum, Datenschutz (Fließtext mit Inhaltsverzeichnis).

## 6. Sonderfälle (voraussichtlich nicht 1:1)

- **Mobile Navigation:** In der Vorschau `details/summary` ohne JavaScript. In Elementor vermutlich das Nav-Menü-Widget oder ein eigenes Muster; Breakpoint der Umschaltung ist 1001 px.
- **Formular:** Elementor-Formular-Widget (oder das vorhandene Formular-Plugin). Felder: Name, E-Mail, Telefon (optional), Modul-Auswahl, Nachricht (optional), Einwilligung (Pflicht). Texte stehen in `content/content.json`.
- **Footer-Streifen:** fünffarbiger Streifen oben im Footer über `border-image` mit Verlauf; in Elementor als Custom CSS oder Trennlinie.
- **Rechtstexte:** Fließtext-Bereich `bw-prose`, formatiert über Elementtypen (h2, h3, p, ul). In Elementor als Text-Editor-Widget mit Klasse `bw-prose`.
- **Platzhalter:** `[Text in eckigen Klammern]` sind offene Inhalte; in der Vorschau gelb (`bw-placeholder`), im Export als Hinweis erhalten, bis der Kunde ergänzt hat.
- **Fester Kontakt-Button:** `bw-fab`, `position: fixed`; unabhängig von der Seitenstruktur halten.
- **Bilder:** Hero-Bild und Teamfotos sind Platzhalter. Stempel/Siegel und Logos liegen in `design/v2/assets/`.

## 7. Offene Inhaltspunkte (nicht technisch)

- Rolle und Titel von Person 1 (Mag. Michael Wohlkönig, Founder) und Daten für Person 2.
- Termine, Format, Dauer der Module, Anerkennung des Abschlusses.
- Rechtstexte (Impressum, Datenschutz) vor Veröffentlichung rechtlich prüfen lassen.
- Kontaktdaten laut Visitenkarte sind eingetragen (Plüddemanngasse 104, 8042 Graz, +43 676 511 2763, michael@perma-academy.at); bestätigen lassen.

## 8. Vorschlag für den Ablauf in der Session mit WordPress-Zugriff

1. Ist-Analyse (Abschnitt 3): Versionen, geladenes CSS, Quelle der Button-Farbe, aktive Experimente.
2. Kit/Globals auf unsere Tokens umstellen, Standardstile abschalten, wo möglich. Vorher/Nachher messen (CSS-Größe, Anzahl Dateien).
3. `styles.css` zentral einbinden (bzw. als globale Klassen), Elementor-Overrides gebündelt am Ende.
4. Abschnitt für Abschnitt anlegen und im Frontend gegen die Vorschau (https://blickwert.github.io/perma-data/v2/) prüfen, jeweils Desktop und Mobil.
5. Unterseiten, Navigation, Formular, Kontakt-Button.
6. Am Ende: Template exportieren, Doku (`docs/IMPORT.md`) aktualisieren.
