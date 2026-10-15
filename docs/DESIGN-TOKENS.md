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

## Noch offen
Schriftstufen, Gewichte, Zeilenhöhen und Abstände (nächster Schritt).
