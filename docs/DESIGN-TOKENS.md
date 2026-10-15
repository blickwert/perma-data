# Design-Tokens

Single Source of Truth: [`tokens/tokens.json`](../tokens/tokens.json). Daraus entstehen

- `design/reference/tokens.css` (CSS-Variablen für Startseite und Unterseiten): `python3 scripts/build_tokens.py`
- die Elementor-Templates: `python3 scripts/build_elementor.py`

Farbwerte nur in `tokens.json` ändern, danach beide Skripte laufen lassen (die Unterseiten mit `python3 scripts/build_design_pages.py`).

## Zwei Ebenen

**Palette** (`--pma-navy`, `--pma-mint`, …): die tatsächlichen Farbwerte, 17 Stück.

| Variable | Wert | Verwendung |
|---|---|---|
| `--pma-navy` | `#00416B` | Haupttext, Überschriften, CTA |
| `--pma-navy-dark` | `#00314F` | Footer, dunkle Flächen |
| `--pma-teal` / `--pma-teal-light` | `#1A8C8C` / `#25A0A0` | Eyebrows, Icons, Verläufe |
| `--pma-aqua` | `#57D3D3` | Tags, Links auf Dunkel, Hero-Box |
| `--pma-white` / `--pma-off-white` | `#FFFFFF` / `#FAFAFA` | Flächen |
| `--pma-mint` | `#E8F1F1` | helle Flächen, Pills |
| `--pma-mist` | `#C9DAD9` | Linien, Rahmen |
| `--pma-slate` | `#4B6269` | gedämpfter Text |
| `--pma-silver` / `--pma-graphite` | `#D6D6D6` / `#6B6B6B` | Text und Rahmen auf Dunkel |
| `--pma-sky`, `--pma-sky-light`, `--pma-sage`, `--pma-clay` | | Hero-Verlauf |

**Rollen** (`--pma-color-text`, `--pma-color-border`, …): zeigen auf die Palette und sagen, wofür eine Farbe da ist. Im Elementor-Export werden daraus Variablen.

## Zusammengelegte Farben
`#FEFEFE` → Weiß · `#E4F4F4`, `#D5ECEC` → Mint (`#E8F1F1`) · `#B7CDCD` → Mist (`#C9DAD9`) · `#587077` → Slate (`#4B6269`) · Navy-Transparenzen .25/.3 → .3.

## Accent-Prop
Die Startseite hat weiter die Prop `accent` (Editor-Farbwahl, Optionen `#00416b`, `#0B3C8A`) für den Header-Button und den schwebenden Kontakt-Button. Sie bleibt unverändert und ist die einzige Stelle mit festen Hex-Werten außerhalb von `tokens.json` (neben dem Logo).

## Typografie

Alle Werte kommen aus `tokens.json` und stehen als Variablen in `tokens.css`.

**Schriften (3 Familien):** `--pma-font-heading` (Gotham, Fallback Montserrat), `--pma-font-body` (Roboto), `--pma-font-script` (Bickham Script Pro, Fallback Great Vibes).

**Größen (8 Stufen)** – mobil (bis 820 px) werden die drei größten kleiner:

| Variable | Desktop | Mobil | Verwendung |
|---|---|---|---|
| `--pma-fs-xs` | 12 | | Eyebrows, Tags, Bildunterschriften |
| `--pma-fs-base` | 16 | | Fließtext, Navigation, Buttons, Formulare |
| `--pma-fs-lg` | 18 | | Einleitungen (Lead) |
| `--pma-fs-xl` | 22 | | Karten-Titel, Intro-Absatz |
| `--pma-fs-2xl` | 26 | | Modul-/Team-Titel, Zitate, Claim |
| `--pma-fs-3xl` | 32 | 26 | Abschnitts-Überschriften (H2) |
| `--pma-fs-4xl` | 36 | 28 | Seiten-Überschrift (H1) |
| `--pma-fs-5xl` | 48 | 38 | Ziffern, Script-Slogan |

**Gewichte:** `--pma-fw-regular` 400, `--pma-fw-medium` 500.
**Zeilenhöhen:** `--pma-lh-none` 1 (Ziffern), `--pma-lh-tight` 1.2 (große Titel), `--pma-lh-heading` 1.3, `--pma-lh-body` 1.7.
**Zeichenabstand:** `--pma-ls-label` 0.14em (Tags, Labels), `--pma-ls-eyebrow` 0.24em (Eyebrows).

### Zusammengelegt (vorher 23 Größen, 12 Zeilenhöhen, 5 Zeichenabstände)
11/12/13 → 12 · 14/15/16/17 → 16 · 18 → 18 · 20/21/22 → 22 · 24/26/28 → 26 · 30/32/34 → 32 · 36/38/40 → 36 · 44/47/48 → 48.
Zeilenhöhen 1.25/1.3/1.35/1.4 → 1.3, alle ab 1.5 → 1.7. Die kleine Eyebrow-Variante (14 px, 0.08em) ist an die übrigen Eyebrows (12 px, 0.24em) angeglichen; der Footer-Zeichenabstand (0.02em) entfällt.

Das Aussehen ändert sich dadurch leicht: Texte ab 14 px sind etwas größer, die Seiten dadurch länger.

## Noch offen
Abstände (Padding, Gaps) und Radien, danach Elementor-Export auf Basis der Variablen.
