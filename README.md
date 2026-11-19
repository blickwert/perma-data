# PERMA Mind Academy – Website (Design-Vorschau und WordPress-Block-Theme)

Website der **PERMA Mind Academy** („We create wellbeing“). Das Design wird hier als statische Vorschau entwickelt und anschließend als eigenes **WordPress-Block-Theme** mit einem **Formular-Plugin** (auf Basis von Contact Form 7) umgesetzt. Elementor wird nicht mehr verwendet.

**Nächster Schritt:** WordPress-Umsetzung. Arbeitsanweisung: [`docs/WP-UMSETZUNG.md`](docs/WP-UMSETZUNG.md) (Einstieg für neue Sessions: [`CLAUDE.md`](CLAUDE.md)).

## Live-Vorschau (GitHub Pages)

| Version | Link | Ordner | Doku |
|---|---|---|---|
| v2b – Kundenwünsche (Homepagetexte V5), **Basis für WordPress** | <https://blickwert.github.io/perma-data/v2b/> | `design/v2b/` | `docs/V2B.md` |
| v2 – Corporate Design v2 | <https://blickwert.github.io/perma-data/v2/> | `design/v2/` | `docs/CORPORATE-DESIGN-V2.md` |
| v1 – ursprüngliches Mockup (nur Vergleich) | <https://blickwert.github.io/perma-data/> | `design/reference/` | – |

Die Seiten aktualisieren sich bei jedem Push auf `main` (Workflow `.github/workflows/pages.yml`).

## Struktur

| Pfad | Inhalt |
|---|---|
| `tokens/tokens.v2.json` | Single Source für das Designsystem (Farben, Schriften, Größen, Abstände, Radien, Schatten) |
| `scripts/build_tokens.py` | Tokens → `tokens.css` (`v1`, `v2`, `v2b`) |
| `scripts/v2b_content.py` | Alle Website-Texte der Version v2b (Quelle für die WordPress-Inhalte) |
| `scripts/build_design_pages_v2b.py` | Erzeugt die v2b-Vorschau |
| `scripts/build_design_pages_v2.py`, `build_design_pages.py` | Unterseiten v2 bzw. v1 |
| `design/` | Statische Vorschauen v1, v2, v2b |
| `assets/` | Logo, Icons (`icons/icons.json`, Lucide-Stil) |
| `docs/` | Briefing, Corporate Design, Tokens, v2b, WordPress-Umsetzung, Änderungslisten (Word) |
| `.claude/skills/` | Regeln für CSS, Block-Theme und Plugins |
| `wordpress/themes/perma-mind/` | Block-Theme (Aufbau: `docs/WP-THEME.md`, erzeugt mit `scripts/build_theme.py`) |
| `wordpress/content/` | Seiteninhalte als Block-Markup für die Übertragung (erzeugt) |
| `wordpress/plugins/bw-perma-forms/` | Formular-Plugin (folgt in Phase 2) |

## Vorschau neu erzeugen

```bash
python3 scripts/build_tokens.py v2b
python3 scripts/build_design_pages_v2b.py
cd design/v2b && python3 -m http.server   # dann index.html öffnen
```
