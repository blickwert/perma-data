---
name: html-css-richtlinien
description: Regeln für sauberes, klassenbasiertes HTML und CSS mit einheitlichen Design-Tokens (Farben, Schriften, Spacing, Rahmen, Buttons), kompatibel mit dem Elementor Design System. Verwenden, wenn HTML/CSS für Webseiten, Landingpages, Templates oder Elementor-Projekte geschrieben oder überarbeitet wird.
---

# HTML & CSS schreiben – Richtlinien

Oberstes Ziel: **Konsistenz.** Jede Definition (Farbe, Schrift, Abstand, Rahmen, Button) existiert genau einmal und ist auf allen Seiten identisch. Der Code muss später ohne Umbau in das Elementor Design System (Global Colors / Global Fonts) übernommen werden können.

## 1. Keine Inline-Styles

- Im HTML **kein** `style="..."`. Styling läuft ausschließlich über Klassen.
- Ausnahme nur, wenn technisch unvermeidbar (z. B. dynamisch berechnete Werte wie ein Fortschrittsbalken `--progress: 70%` als Custom Property). Dann nur die Variable setzen, nie fertige Eigenschaften.
- Keine `<style>`-Blöcke im Body verstreuen. CSS gehört gesammelt in ein Stylesheet (oder einen einzelnen Block im Head).
- Kein `!important`, außer zum bewussten Überschreiben von Elementor-/Plugin-Defaults, und dann kommentiert.

## 2. Wiederholung = eigene Klasse

- Sobald ein Stil an mehr als einer Stelle vorkommt, wird er als Klasse definiert, nicht am Element wiederholt.
- Zwei Ebenen verwenden:
  - **Komponenten-Klassen** für wiederkehrende Bausteine: `.bw-card`, `.bw-button`, `.bw-section`, `.bw-hero`
  - **Modifier/Utilities** für Varianten: `.bw-button--secondary`, `.bw-section--dark`, `.bw-mt-m`
- Mehrere Klassen pro Element sind ok und erwünscht (`class="bw-card bw-card--highlight"`), statt Sonderfälle neu zu stylen.
- Benennung: Präfix `bw-`, Kleinbuchstaben, Bindestriche, BEM-nah (`.bw-card__title`, `.bw-card--highlight`). Namen beschreiben **Funktion**, nicht Aussehen (`.bw-button--primary`, nicht `.bw-blue-button`).
- Selektoren flach halten: maximal 2 Ebenen, keine ID-Selektoren, keine Selektoren, die an der DOM-Struktur hängen (`div > div > p`).

## 3. Design-Tokens als CSS Custom Properties

Alle Werte kommen aus Variablen im `:root`. Im restlichen CSS stehen **keine** Hex-Codes, Pixelwerte für Abstände oder Schriftnamen direkt.

Farben und Schriften werden auf die Elementor Global Variablen gemappt, damit Änderungen im Design System überall wirken:

```css
:root {
  /* Farben → Elementor Global Colors */
  --bw-color-primary:   var(--e-global-color-primary);
  --bw-color-secondary: var(--e-global-color-secondary);
  --bw-color-text:      var(--e-global-color-text);
  --bw-color-accent:    var(--e-global-color-accent);

  /* Schriften → Elementor Global Fonts */
  --bw-font-heading: var(--e-global-typography-primary-font-family), sans-serif;
  --bw-font-body:    var(--e-global-typography-text-font-family), sans-serif;

  /* Spacing-Skala (nur diese Werte verwenden) */
  --bw-space-xs: 0.5rem;
  --bw-space-s:  1rem;
  --bw-space-m:  1.5rem;
  --bw-space-l:  2.5rem;
  --bw-space-xl: 4rem;

  /* Rahmen, Radius, Schatten */
  --bw-radius:        8px;
  --bw-border:        1px solid var(--bw-color-secondary);
  --bw-shadow:        0 2px 8px rgb(0 0 0 / 0.08);
}
```

Regeln:
- Es gibt nur die definierten Spacing-Stufen. Keine Zwischenwerte wie `13px` oder `2.2rem`.
- Pro Projekt eine feste Anzahl Farben und Schriften (aus dem Design System). Neue Werte erst ins Design System aufnehmen, dann verwenden.
- Schriftgrößen ebenfalls als Skala (`--bw-text-s/m/l`, Überschriftenstufen), idealerweise fluid mit `clamp()`.

## 4. Konsistenz über alle Seiten

Diese Elemente sind projektweit **einmal** definiert und überall gleich:

- **Spacing:** Section-Padding, Container-Breite, Abstände zwischen Elementen (Skala oben)
- **Typografie:** h1–h6, Fließtext, Links, Listen
- **Buttons:** Primär, Sekundär, Outline; Padding, Radius, Hover/Focus-Zustand
- **Rahmen & Radien, Schatten**
- **Formularfelder:** Höhe, Rahmen, Focus-Zustand
- **Karten, Icons, Bilder** (Seitenverhältnisse, Radius)

Beim Erstellen einer neuen Seite zuerst vorhandene Klassen wiederverwenden. Neue Klasse nur, wenn es den Baustein noch nicht gibt, und dann so, dass andere Seiten sie ebenfalls nutzen können.

## 5. Elementor-Kompatibilität

- Elementor gibt Überschriften als `.elementor-heading-title` mit Größenklassen wie `.elementor-size-default` aus. Typografie-Stile deshalb **über die Elementor Global Fonts** steuern und im Custom-CSS nur dort ergänzen, wo nötig, z. B.:
  ```css
  .bw-section .elementor-heading-title { font-family: var(--bw-font-heading); }
  ```
- Mehrere Schriften: Primär-/Sekundär-Font als eigene Global Fonts anlegen und über die Variablen oben ansprechen, nie per Schriftname im CSS.
- Buttons über `.elementor-button` bzw. unsere `.bw-button`-Klassen vereinheitlichen, nicht pro Widget einzeln stylen.
- Eigene Klassen im Elementor-Feld „CSS-Klassen" eintragen, nicht per Widget-Einzelstyling im Editor duplizieren.
- Farben, Schriften und Abstände im Elementor-Editor möglichst aus den Globals wählen, nicht manuell überschreiben.

## 6. HTML-Struktur

- Semantisch: `header`, `nav`, `main`, `section`, `article`, `footer`; genau ein `h1` pro Seite, Überschriften-Hierarchie nicht überspringen.
- Optik **nie** über die Tag-Wahl steuern: Ein `h3` wird nicht verwendet, weil es kleiner aussieht. Dafür gibt es Klassen (`.bw-heading-s`).
- Keine leeren Elemente oder `<br>` für Abstände; dafür Spacing-Klassen.
- Bilder mit `alt`, Links mit sprechendem Text, Buttons als `<a>` oder `<button>` korrekt.
- Barrierefreiheit: ausreichender Kontrast, sichtbarer `:focus-visible`-Zustand.

## 7. Responsive

- Mobile-first, zentrale Breakpoints einmal definieren und überall gleich verwenden.
- Layout mit Flexbox/Grid, Größen mit `rem`/`clamp()` statt fester Pixelwerte.
- Anpassungen für Breakpoints innerhalb der jeweiligen Komponentenklasse, nicht als verstreute Einzelregeln.

## 8. CSS-Organisation

Reihenfolge im Stylesheet:
1. Tokens (`:root`)
2. Base (Reset, Typografie, Links)
3. Layout (Container, Sections, Grid)
4. Komponenten (Button, Card, Formular …)
5. Utilities/Modifier
6. Elementor-Overrides (kommentiert und gebündelt)

Kommentare als Abschnittsüberschriften, keine toten oder doppelten Regeln.

## Checkliste vor der Ausgabe

- [ ] Kein `style=""` im HTML
- [ ] Wiederholte Stile sind Klassen
- [ ] Keine Hex-Werte, Schriftnamen oder freien Pixelabstände außerhalb von `:root`
- [ ] Farben und Schriften hängen an `--e-global-*`
- [ ] Spacing, Radius, Rahmen, Buttons entsprechen den bestehenden Definitionen
- [ ] Klassennamen mit `bw-` Präfix und funktional benannt
- [ ] Semantische Tags, Überschriftenhierarchie korrekt
- [ ] Mobile geprüft
