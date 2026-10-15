# Corporate Design v2

**v2 ist die Arbeitsgrundlage** für alle weiteren Änderungen und für den späteren Elementor-Export. Version 1 bleibt nur zum Vergleich im Repo.

Das neue Corporate Design liegt parallel zur ersten Version in **`design/v2/`** (Vorschau: `/v2/`). Die erste Version (`design/reference/`) bleibt unverändert zum Vergleich.

Quellen: `Font_and_color_info.pdf`, Logo (Variante auf Weiß), Siegel (Stamp 3), Visitenkarte und Logo auf Navy.

## Was gilt in v2

**Schriften:** Gotham Medium (Überschriften), Roboto Light, Regular und Medium (Text), Bickham Script Pro Semibold (Slogan, Zitate). Fallbacks wie bisher: Montserrat und Great Vibes.

**Farben aus dem PDF (7):** Navy `#00416B`, Blau `#16A5D2`, Lila `#B464A7`, Orange `#F09133`, Grün `#18946B`, Rot `#D83662`, Weiß `#FFFFFF`. Alle weiteren Töne (helle Flächen, Linien, gedämpfter Text, Hero-Verlauf, dunkles Navy) sind daraus durch Mischung mit Weiß oder Schwarz abgeleitet, siehe `tokens/tokens.v2.json`.

**Der türkise Akzent entfällt.** An seiner Stelle steht Blau, Grün ersetzt das dunkle Türkis.

## Was sich gegenüber v1 sichtbar ändert
- Neues Logo (fünf farbige Bögen), in der Fußzeile die weiße Variante.
- Hero: Verlauf von Himmelblau über Lila zu Orange (Morgenröte) statt Blau-Türkis-Braun, Textbox in Blau.
- Angebots-Kacheln: dunkel getönt mit je einem Hauch der Markenfarben (Blau, Lila, Orange, Grün), weißer Text. Das Feld „Angebot 0X“ trägt die volle Kachelfarbe. Weißer Text auf den hellen Markenfarben selbst wäre schlecht lesbar. Die Töne heißen `--pma-blue-deep`, `--pma-purple-deep` usw. in `tokens.v2.json`.
- Akzentfarben der Reihe nach von oben (Blau, Lila, Orange, Grün): bei „Warum PERMA Mind Academy?“ Oberkante und Icon der vier Karten, in der Modul-Liste ein Balken unter der Ziffer und das Niveau-Feld.
- **Startseite gestrafft:** „Ihre Vorteile“ und „Sorgfalt vor großen Versprechen“ sind zu einem Abschnitt „Warum PERMA Mind Academy?“ mit vier Karten verschmolzen (Wissenschaftlich fundiert, Praxisnah, Persönlich begleitet, Nachvollziehbarer Abschluss). „Erfahrene Trainer:innen“ steht jetzt in der Einleitung des Team-Bereichs, „Termine und Format“ in der Einleitung der Module. Die Kennzahlen „4“ und „5“ im Intro-Block sind entfallen.
- **Team:** zwei Personen nebeneinander in einem Block mit höchstens 70 % Breite (mobil untereinander in voller Breite). Pro Person oben ein Porträt (Rollen-Feld oben links im Bild), darunter Name, Titel, Kurzprofil, Social-Icons, Trenner, „Werdegang“ mit drei Haken-Punkten (Ausbildung, Berufserfahrung, Schwerpunkt) und das Zitat in Schreibschrift. Der Bereich hat weißen Grund, die Bildfläche ist hellblau.
- **„Warum PERMA Mind Academy?“**: Beschriftung, Überschrift und Absatz stehen in Navy, wie bei „Ausbildungen & Module“. Die Akzentlinien der Karten liegen innen am oberen Rand.
- Der schwebende Button „Kontakt aufnehmen“ ist orange mit Navy-Schrift (Weiß auf Orange hätte nur 2,4:1 Kontrast, Navy auf Orange 4,5:1). Der Button in der Kopfzeile bleibt Navy.
- Zertifikat-Bereich: das Siegel statt des Foto-Platzhalters.
- Fünffarbiger Streifen über der Fußzeile (wie auf der Visitenkarte).
- Roboto Light für die Einleitungen der Unterseiten.
- Kontaktdaten laut Visitenkarte: Plüddemanngasse 104, 8042 Graz, +43 676 511 2763, michael@perma-academy.at, www.perma-academy.at. Mag. Michael Wohlkönig (Founder) steht als Ansprechperson und als erste Teamkarte. Beides bitte bestätigen.

## Erzeugen
```bash
python3 scripts/build_tokens.py v2          # tokens/tokens.v2.json -> design/v2/tokens.css
python3 scripts/build_design_pages.py v2    # Kontakt, Impressum, Datenschutz -> design/v2/
```
Die Startseite (`design/v2/Main.dc.html`) und `site.css` werden von Hand gepflegt und nutzen nur Variablen aus `tokens.css`.

## Offen
- Bickham Script Pro Semibold und Gotham Medium sind lizenzpflichtig und derzeit nur über Fallbacks sichtbar.
- Kontrast: Weißer Text auf Blau und Orange ist knapp. Deshalb Navy-Text auf der blauen Hero-Box und Navy als Grund der Kacheln.
