#!/usr/bin/env python3
"""Erzeugt tokens.css aus der Token-Datei.

    python3 scripts/build_tokens.py       # tokens/tokens.json    -> design/reference/tokens.css
    python3 scripts/build_tokens.py v2    # tokens/tokens.v2.json -> design/v2/tokens.css

Ebene 1 (Palette):  --<praefix>-navy, --<praefix>-mint, ...
Ebene 2 (Rollen):   --<praefix>-color-text, --<praefix>-color-border, ... (zeigen auf die Palette)
In Markup und Stylesheets nach Moeglichkeit Rollen verwenden, Palette fuer Verlaeufe.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V2 = len(sys.argv) > 1 and sys.argv[1] == "v2"
T = json.loads((ROOT / ("tokens/tokens.v2.json" if V2 else "tokens/tokens.json")).read_text("utf-8"))
k = lambda s: s.replace("_", "-")
P = "bw" if V2 else "pma"  # CSS-Praefix: v2 = bw-, v1 (Vergleich) = pma-

lines = [f"/* AUTO-GENERIERT aus tokens/{'tokens.v2.json' if V2 else 'tokens.json'} (scripts/build_tokens.py). Nicht von Hand aendern. */", ":root{",
         "  /* Palette */"]
lines += [f"  --{P}-{k(n)}:{v};" for n, v in T["color"].items()]
lines += [f"  /* RGB-Tripel fuer Transparenzen: rgba(var(--{P}-navy-rgb),.3) */"]
lines += [f"  --{P}-{k(n)}-rgb:{v};" for n, v in T["color_rgb"].items()]
lines += ["  /* Rollen */"]
lines += [f"  --{P}-color-{k(n)}:var(--{P}-{k(v)});" for n, v in T["role"].items()]
lines += ["  /* Schriften */"]
lines += [f"  --{P}-font-{k(n.replace('_stack', ''))}:{v};" for n, v in T["font"].items() if n.endswith("_stack")]
lines += ["  /* Typografie: Groessen (Desktop), Gewichte, Zeilenhoehen, Zeichenabstand */"]
lines += [f"  --{P}-fs-{k(n)}:{v}px;" for n, v in T["font_size"].items()]
lines += [f"  --{P}-fw-{k(n)}:{v};" for n, v in T["font_weight"].items()]
lines += [f"  --{P}-lh-{k(n)}:{v};" for n, v in T["line_height"].items()]
lines += [f"  --{P}-ls-{k(n)}:{v};" for n, v in T["letter_spacing"].items()]
lines += ["  /* Radien, Schatten */"]
lines += [f"  --{P}-radius-{k(n)}:{v}px;" for n, v in T["radius"].items()]
lines += [f"  --{P}-shadow-{k(n)}:{v};" for n, v in T["shadow"].items()]
if "space" in T:
    lines += [f"  /* Abstandsskala: --{P}-space-N = N x 0.25rem (erweiterbar nach Bedarf) */"]
    lines += [f"  --{P}-space-{k(n)}:{v / 16:g}rem;" for n, v in T["space"].items()]
    lines += ["  /* Linienstaerken */"]
    lines += [f"  --{P}-border-width-{k(n)}:{v}px;" for n, v in T["border_width"].items()]
lines += ["  /* Layout */"]
lines += [f"  --{P}-{k(n)}:{v}px;" for n, v in T["layout"].items()]
lines += ["}", "",
          f"/* Mobil (bis {T['breakpoints']['stack']}px): grosse Ueberschriften werden kleiner */",
          f"@media (max-width:{T['breakpoints']['stack']}px){{", "  :root{"]
lines += [f"    --{P}-fs-{k(n)}:{v}px;" for n, v in T["font_size_mobile"].items()]
lines += ["  }", "}", ""]
out = ROOT / ("design/v2/tokens.css" if V2 else "design/reference/tokens.css")
out.write_text("\n".join(lines), "utf-8")
print("->", out.relative_to(ROOT))
