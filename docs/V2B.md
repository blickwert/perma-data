# Version v2b: Kundenwünsche (Homepagetexte V5, Stand 16. November 2026)

v2b setzt die Inhalte und die Struktur aus dem Kundendokument um, damit sie mit v2 verglichen werden können. Corporate Design, Tokens und CSS-Regeln (Präfix `bw-`, keine Inline-Styles) sind dieselben wie in v2.

Vorschau: https://blickwert.github.io/perma-data/v2b/ (v2 zum Vergleich: https://blickwert.github.io/perma-data/v2/)

## Dateien

| Was | Wo |
|---|---|
| Texte (aus dem Dokument, nur öffentliche Website-Texte) | `scripts/v2b_content.py` |
| Generator | `scripts/build_design_pages_v2b.py` |
| Seiten | `design/v2b/index.html`, `positive-psychologie-basic.html`, `positive-psychologie-advanced.html`, `klinische-positive-psychologie.html`, `impressum.html`, `datenschutz.html` |
| Stile | `design/v2b/styles.css` (Basis aus v2, ungenutzte v2-Bausteine entfernt, v2b-Erweiterungen am Ende) |
| Tokens | `design/v2b/tokens.css` aus `tokens/tokens.v2.json` |
| Formular-Vorschau | `design/v2b/preview.js` (sendet nichts, zeigt nur die Bestätigung) |

Neu erzeugen:

```
python3 scripts/build_tokens.py v2b
python3 scripts/build_design_pages_v2b.py
```

## Was sich gegenüber v2 ändert

- **Ansprache:** „du“ statt „Sie“ (außer Impressum und Datenschutz, die aus v2 übernommen sind; deren Texte liefert die Academy).
- **Angebot:** drei Ausbildungen statt vier allgemeiner Angebotskarten: Positive Psychology Basic, Positive Psychology Advanced, PERMA Clinical Expert. Workshops, Coaching-Tools und die alte Modulliste entfallen.
- **Navigation:** Ausbildungen (mit Untermenü zu den drei Seiten) · Über uns · Zertifizierung · Fragen · Kontakt. Hauptschaltfläche „Zur Interessentenliste“. Footer: Kontakt · Newsletter · Impressum · Datenschutz.
- **Startseite** (Sprungziele `#ausbildungen`, `#ueber-uns`, `#zertifizierung`, `#interessentenliste`, `#fragen`, `#newsletter`, `#kontakt`):
  Hero mit H1 und Hauptschaltfläche → drei Profilmerkmale → Einleitung → Warum PERMA Mind Academy? (3 Karten) → Ausbildungen (3 Karten) → Positive Psychologie verstehen (mit PERMA-Modell) und Vom Verstehen zum Anwenden (4 Schritte) → Über uns mit Trainerprofilen (aufklappbar) → ECQA-Zertifizierung (aufklappbar) → Interessentenliste (Formular) → Häufige Fragen (8, aufklappbar) → Newsletter → Kontakt.
- **Angebotsseiten:** Farbschema wie die jeweilige Angebotskarte (Kopfbereich und Interessentenliste im Verlauf Akzent-Tiefe → Navy), H1, Einleitung, „Das Angebot auf einen Blick“ (Eckdaten mit Preis), Module aufklappbar, Umfang und Abschluss, Querverweise (Basic → Advanced, Advanced → Basic), Interessentenliste mit vorausgewähltem Lehrgang.
- **Formulare:** Interessentenliste (Vorname, Nachname, E-Mail, Mehrfachauswahl, Beruf und Nachricht optional, freiwillige Newsletter-Checkbox), separater Newsletter (E-Mail, Vorname optional, Einwilligung), Kontaktformular (Name, E-Mail, Nachricht). Checkboxen sind nicht vorausgewählt (außer dem Lehrgang der jeweiligen Angebotsseite).
- **Kontaktseite:** entfällt; Kontakt und Interessentenliste sind Abschnitte auf den Seiten.
- **Neue Bausteine:** Akkordeon (`bw-accordion`, natives `details`/`summary`, Inhalte als HTML und per Tastatur bedienbar), Untermenü (`bw-nav-menu`), Profilmerkmale (`bw-highlights`), Eckdaten-Karte (`bw-facts-card`, auf dem Desktop mitlaufend), PERMA-Liste (`bw-perma`, fünf CD-Farben), Zitat (`bw-quote`), Abschnittskopf (`bw-section-head`), sekundärer Button, Mehrfachauswahl im Formular, Akzent Rot.
- **Mobil:** Hauptschaltfläche steht im Hero direkt unter der H1; der schwebende Button „Zur Interessentenliste“ erscheint nur, solange der Header keine Schaltfläche zeigt (unter 561 px).
- **SEO:** Seitentitel und Meta-Beschreibungen aus Abschnitt 10; je Seite genau eine H1, Abschnitte H2, Module H3. Die URLs im Dokument (`/positive-psychologie-basic/` usw.) gelten für WordPress; in der Vorschau heißen die Dateien entsprechend `.html`.

## Bewusst nicht übernommen

- Kursive Umsetzungshinweise, „Button:“-Markierungen und die Abschnitte 8 bis 10 (nur für die Umsetzung).
- Noch nicht ausgeschriebene Reihen (Advanced Plus, Neurodivergenz, Clinical Expert Advanced).

## Platzhalter und offene Punkte

- Hero-Bild, Trainerporträts und ECQA-Logo sind Platzhalter (Logo erst in der freigegebenen Version).
- Termine, Orte, Frühbucherfristen und Zertifizierungsgebühren folgen laut Dokument.
- Impressum und Datenschutz: Texte liefert die Academy; derzeit Entwurf aus v2 in „Sie“-Form.
- Csíkszentmihályi ist 2021 verstorben; laut Dokument rückblickend beschreiben. Der Kundentext („Dazu zählen Begegnungen …“) ist unverändert übernommen und sollte das bei der Freigabe berücksichtigen.
- Akzentfarben je Angebot (Basic blau, Advanced lila, Clinical Expert orange) sind ein Gestaltungsvorschlag.
