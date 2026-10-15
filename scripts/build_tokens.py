#!/usr/bin/env python3
"""Erzeugt design/reference/tokens.css aus tokens/tokens.json.

    python3 scripts/build_tokens.py

Ebene 1 (Palette):  --pma-navy, --pma-mint, ...
Ebene 2 (Rollen):   --pma-color-text, --pma-color-border, ... (zeigen auf die Palette)
In Markup und Stylesheets nach Moeglichkeit Rollen verwenden, Palette fuer Verlaeufe.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "tokens/tokens.json").read_text("utf-8"))
k = lambda s: s.replace("_", "-")

lines = ["/* AUTO-GENERIERT aus tokens/tokens.json (scripts/build_tokens.py). Nicht von Hand aendern. */", ":root{",
         "  /* Palette */"]
lines += [f"  --pma-{k(n)}:{v};" for n, v in T["color"].items()]
lines += ["  /* RGB-Tripel fuer Transparenzen: rgba(var(--pma-navy-rgb),.3) */"]
lines += [f"  --pma-{k(n)}-rgb:{v};" for n, v in T["color_rgb"].items()]
lines += ["  /* Rollen */"]
lines += [f"  --pma-color-{k(n)}:var(--pma-{k(v)});" for n, v in T["role"].items()]
lines += ["  /* Schriften */"]
lines += [f"  --pma-font-{k(n.replace('_stack', ''))}:{v};" for n, v in T["font"].items() if n.endswith("_stack")]
lines += ["  /* Typografie: Groessen (Desktop), Gewichte, Zeilenhoehen, Zeichenabstand */"]
lines += [f"  --pma-fs-{k(n)}:{v}px;" for n, v in T["font_size"].items()]
lines += [f"  --pma-fw-{k(n)}:{v};" for n, v in T["font_weight"].items()]
lines += [f"  --pma-lh-{k(n)}:{v};" for n, v in T["line_height"].items()]
lines += [f"  --pma-ls-{k(n)}:{v};" for n, v in T["letter_spacing"].items()]
lines += ["  /* Radien, Schatten */"]
lines += [f"  --pma-radius-{k(n)}:{v}px;" for n, v in T["radius"].items()]
lines += [f"  --pma-shadow-{k(n)}:{v};" for n, v in T["shadow"].items()]
lines += ["  /* Layout */"]
lines += [f"  --pma-{k(n)}:{v}px;" for n, v in T["layout"].items()]
lines += ["}", "",
          f"/* Mobil (bis {T['breakpoints']['stack']}px): grosse Ueberschriften werden kleiner */",
          f"@media (max-width:{T['breakpoints']['stack']}px){{", "  :root{"]
lines += [f"    --pma-fs-{k(n)}:{v}px;" for n, v in T["font_size_mobile"].items()]
lines += ["  }", "}", ""]
out = ROOT / "design/reference/tokens.css"
out.write_text("\n".join(lines), "utf-8")
print("->", out.relative_to(ROOT))
