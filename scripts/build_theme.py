#!/usr/bin/env python3
"""Erzeugt die generierten Teile des Block-Themes perma-mind aus Tokens und Texten.

    python3 scripts/build_theme.py

Quellen (nur diese ändern, nicht die erzeugten Dateien):
  tokens/tokens.v2.json       -> theme.json, assets/css/tokens.css
  scripts/v2b_content.py      -> patterns/*.php (Texte der Website)
  content/rechtstexte/*.html  -> Seiten Impressum und Datenschutz (Entwurf der Rechtstexte)
  assets/icons/ + ICONS aus build_design_pages_v2b.py -> assets/icons/*.svg
  design/v2b/assets/logo*.svg -> assets/images/

Von Hand gepflegt (nicht erzeugt): style.css, functions.php, src/, templates/, parts/, blocks/,
assets/css/components.css, assets/fonts/.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2b_content as C  # noqa: E402
from build_design_pages_v2b import ICONS, OFFER_CHIP, OFFER_ICON, CONTACT as CONTACT_DATA  # noqa: E402

THEME = ROOT / "wordpress/themes/perma-mind"
SLUG = "perma-mind"
T = json.loads((ROOT / "tokens/tokens.v2.json").read_text("utf-8"))
k = lambda s: s.replace("_", "-")

GEN_NOTE = "AUTO-GENERIERT von scripts/build_theme.py – nicht von Hand ändern."

# ------------------------------------------------------------------ Schriften (Dateien liegen in assets/fonts)
LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
         "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
LATIN_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,"
             "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF")


def faces(family, file_prefix, variants):
    out = []
    for weight, style in variants:
        for subset, rng in (("latin", LATIN), ("latin-ext", LATIN_EXT)):
            out.append({"fontFamily": family, "fontWeight": str(weight), "fontStyle": style, "fontDisplay": "swap",
                        "src": [f"file:./assets/fonts/{file_prefix}-{subset}-{weight}-{style}.woff2"],
                        "unicodeRange": rng})
    return out


def shadow(v):
    """Schatten aus den Tokens: Variablen durch die RGB-Werte ersetzen (Presets stehen vor tokens.css)."""
    return (v.replace("var(--bw-shadow-rgb)", T["color_rgb"]["shadow"])
             .replace("var(--bw-navy-rgb)", T["color_rgb"]["navy"]))


# ------------------------------------------------------------------ theme.json
def build_theme_json():
    c = T["color"]
    palette = [{"slug": k(n), "name": n.replace("_", " ").title(), "color": v}
               for n, v in c.items() if n not in ("blue_glass", "placeholder")]
    grad = lambda deg, stops: f"linear-gradient({deg}," + ",".join(f"var(--wp--preset--color--{k(s)}) {p}" for s, p in stops) + ")"
    gradients = [
        {"slug": "hero", "name": "Hero", "gradient": grad("180deg", [("sky", "0%"), ("sky_light", "42%"), ("dawn_purple", "66%"), ("dawn_orange", "100%")])},
        {"slug": "page-head", "name": "Seitenkopf", "gradient": grad("180deg", [("sky", "0%"), ("sky_light", "60%"), ("mint", "100%")])},
    ] + [
        {"slug": f"accent-{a}", "name": f"Akzent {n}", "gradient": grad("135deg", [(f"{a}_deep", "0%"), ("navy_dark", "100%")])}
        for a, n in (("blue", "Blau"), ("purple", "Lila"), ("orange", "Orange"), ("green", "Grün"))
    ] + [
        {"slug": "footer-stripe", "name": "Footer-Streifen",
         "gradient": "linear-gradient(90deg," + ",".join(
             f"var(--wp--preset--color--{s}) {i * 20}% {(i + 1) * 20}%" for i, s in enumerate(("blue", "purple", "orange", "green", "red"))) + ")"},
    ]
    fs, fsm = T["font_size"], T["font_size_mobile"]
    names = {"xs": "XS", "base": "Normal", "lg": "L", "xl": "XL", "2xl": "2XL", "3xl": "3XL", "4xl": "4XL", "5xl": "5XL"}
    sizes = []
    for n, px in fs.items():
        e = {"slug": n, "name": names[n], "size": f"{px / 16:g}rem"}
        if n in fsm:
            e["fluid"] = {"min": f"{fsm[n] / 16:g}rem", "max": f"{px / 16:g}rem"}
        else:
            e["fluid"] = False
        sizes.append(e)
    spacing = [{"slug": n, "name": f"{n} ({v}px)", "size": f"{v / 16:g}rem"} for n, v in T["space"].items()]
    lay = T["layout"]
    data = {
        "$schema": "https://schemas.wp.org/wp/6.8/theme.json",
        "version": 3,
        "title": "PERMA Mind",
        "settings": {
            "appearanceTools": False,
            "useRootPaddingAwareAlignments": False,
            "color": {
                "custom": False, "customGradient": False, "customDuotone": False,
                "defaultPalette": False, "defaultGradients": False, "defaultDuotone": False,
                "palette": palette, "gradients": gradients, "link": False,
            },
            "typography": {
                "customFontSize": False, "defaultFontSizes": False, "dropCap": False,
                "fontStyle": False, "fontWeight": False, "letterSpacing": False, "lineHeight": False,
                "textDecoration": False, "textTransform": False, "writingMode": False,
                "fluid": {"minViewportWidth": "390px", "maxViewportWidth": "1200px"},
                "fontFamilies": [
                    {"slug": "heading", "name": "Montserrat (Überschriften)", "fontFamily": "Montserrat, sans-serif",
                     "fontFace": faces("Montserrat", "montserrat", [(500, "normal")])},
                    {"slug": "body", "name": "Roboto (Text)", "fontFamily": "Roboto, system-ui, sans-serif",
                     "fontFace": faces("Roboto", "roboto", [(300, "normal"), (400, "normal"), (500, "normal"), (300, "italic")])},
                ],
                "fontSizes": sizes,
            },
            "spacing": {
                "blockGap": False, "margin": False, "padding": False,
                "defaultSpacingSizes": False, "customSpacingSize": False,
                "spacingSizes": spacing, "units": ["px", "rem", "%"],
            },
            "border": {"color": False, "radius": False, "style": False, "width": False},
            "shadow": {"defaultPresets": False,
                       "presets": [{"slug": k(n), "name": n.title(), "shadow": shadow(v)} for n, v in T["shadow"].items()]},
            "dimensions": {"minHeight": False, "aspectRatio": False},
            "layout": {"contentSize": f"{lay['max_width']}px", "wideSize": f"{lay['max_width']}px"},
            "custom": {
                "radius": {k(n): f"{v}px" for n, v in T["radius"].items()},
                "border-width": {k(n): f"{v}px" for n, v in T["border_width"].items()},
                "font-weight": {k(n): v for n, v in T["font_weight"].items()},
                "line-height": {k(n): v for n, v in T["line_height"].items()},
                "letter-spacing": {k(n): v for n, v in T["letter_spacing"].items()},
                "gutter": f"{lay['gutter']}px",
                "gutter-mobile": f"{lay['gutter_mobile']}px",
                "color": {"blue-glass": c["blue_glass"], "placeholder": c["placeholder"]},
            },
            "blocks": {
                "core/button": {"color": {"background": False, "text": False}},
            },
        },
        "styles": {
            "color": {"background": "var(--wp--preset--color--white)", "text": "var(--wp--preset--color--navy)"},
            "spacing": {"blockGap": "0px", "padding": {"top": "0px", "right": "0px", "bottom": "0px", "left": "0px"}},
            "typography": {"fontFamily": "var(--wp--preset--font-family--body)", "fontSize": "var:preset|font-size|base",
                           "lineHeight": str(T["line_height"]["body"])},
            "elements": {
                "heading": {"color": {"text": "var(--wp--preset--color--navy)"},
                            "typography": {"fontFamily": "var(--wp--preset--font-family--heading)", "fontWeight": "500",
                                           "lineHeight": str(T["line_height"]["heading"])}},
                "h1": {"typography": {"fontSize": "var:preset|font-size|4xl", "lineHeight": str(T["line_height"]["tight"])}},
                "h2": {"typography": {"fontSize": "var:preset|font-size|3xl"}},
                "h3": {"typography": {"fontSize": "var:preset|font-size|xl"}},
                "h4": {"typography": {"fontSize": "var:preset|font-size|lg"}},
                "link": {"color": {"text": "currentColor"}},
                "button": {
                    "color": {"background": "var(--wp--preset--color--navy)", "text": "var(--wp--preset--color--white)"},
                    "border": {"radius": "var(--wp--custom--radius--pill)", "width": "0"},
                    "spacing": {"padding": {"top": "0", "bottom": "0", "left": "var(--wp--preset--spacing--6)", "right": "var(--wp--preset--spacing--6)"}},
                    "typography": {"fontFamily": "inherit", "fontSize": "var:preset|font-size|base", "fontWeight": "500", "lineHeight": "1.2"},
                },
            },
        },
        "templateParts": [
            {"name": "header", "title": "Header", "area": "header"},
            {"name": "header-akzent", "title": "Header Akzent (Angebotsseiten)", "area": "header"},
            {"name": "footer", "title": "Footer", "area": "footer"},
        ],
        "customTemplates": [
            {"name": "page-angebot", "title": "Angebotsseite (Header im Akzent-Verlauf)", "postTypes": ["page"]},
            {"name": "page-rechtliches", "title": "Rechtstext (Seitenkopf mit Titel)", "postTypes": ["page"]},
        ],
    }
    (THEME / "theme.json").write_text(json.dumps(data, ensure_ascii=False, indent="\t") + "\n", "utf-8")


# ------------------------------------------------------------------ tokens.css (Kurz-Variablen -> Presets)
def build_tokens_css():
    P = "bw"
    lines = [f"/* {GEN_NOTE} Quelle: tokens/tokens.v2.json */", "/* Die --bw-*-Variablen zeigen auf die theme.json-Presets, damit das Komponenten-CSS aus der Vorschau weiterläuft. */", ":root{"]
    for n, v in T["color"].items():
        if n in ("blue_glass", "placeholder"):
            lines.append(f"  --{P}-{k(n)}:var(--wp--custom--color--{k(n)});")
        else:
            lines.append(f"  --{P}-{k(n)}:var(--wp--preset--color--{k(n)});")
    lines += [f"  --{P}-{k(n)}-rgb:{v};" for n, v in T["color_rgb"].items()]
    lines += [f"  --{P}-color-{k(n)}:var(--{P}-{k(v)});" for n, v in T["role"].items()]
    lines += [f"  --{P}-font-heading:var(--wp--preset--font-family--heading);", f"  --{P}-font-body:var(--wp--preset--font-family--body);"]
    lines += [f"  --{P}-fs-{n}:var(--wp--preset--font-size--{re.sub(r'(\d)([a-z])', r'\1-\2', n)});" for n in T["font_size"]]
    lines += [f"  --{P}-fw-{k(n)}:var(--wp--custom--font-weight--{k(n)});" for n in T["font_weight"]]
    lines += [f"  --{P}-lh-{k(n)}:var(--wp--custom--line-height--{k(n)});" for n in T["line_height"]]
    lines += [f"  --{P}-ls-{k(n)}:var(--wp--custom--letter-spacing--{k(n)});" for n in T["letter_spacing"]]
    lines += [f"  --{P}-radius-{k(n)}:var(--wp--custom--radius--{k(n)});" for n in T["radius"]]
    lines += [f"  --{P}-shadow-{k(n)}:var(--wp--preset--shadow--{k(n)});" for n in T["shadow"]]
    lines += [f"  --{P}-space-{n}:var(--wp--preset--spacing--{n});" for n in T["space"]]
    lines += [f"  --{P}-border-width-{k(n)}:var(--wp--custom--border-width--{k(n)});" for n in T["border_width"]]
    lines += [f"  --{P}-max-width:{T['layout']['max_width']}px;",
              f"  --{P}-gutter:var(--wp--custom--gutter);", f"  --{P}-gutter-mobile:var(--wp--custom--gutter-mobile);", "}", ""]
    (THEME / "assets/css/tokens.css").write_text("\n".join(lines), "utf-8")


# ------------------------------------------------------------------ Icons, Logos
def build_assets():
    d = THEME / "assets/icons"
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.svg"):
        old.unlink()
    for name, body in sorted(ICONS.items()):
        (d / f"{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{body}</svg>\n', "utf-8")
    img = THEME / "assets/images"
    img.mkdir(parents=True, exist_ok=True)
    for f in ("logo.svg", "logo-white.svg"):
        shutil.copy(ROOT / "design/v2b/assets" / f, img / f)
    build_image_variants(img)
    return sorted(ICONS)


# Kleinere Fassungen der Hero-Bilder für srcset (src/HeroImage.php sucht <name>-<breite>.webp neben dem Original).
HERO_VARIANTS = {"hero-sonnenaufgang.webp": (1200, 1600), "hero-sonnenaufgang-mobil.webp": (640, 768)}


def build_image_variants(img_dir):
    try:
        from PIL import Image
    except ImportError:
        print("Hinweis: Pillow fehlt, Bildvarianten nicht erzeugt (pip install pillow)")
        return
    for name, widths in HERO_VARIANTS.items():
        src = img_dir / name
        if not src.exists():
            continue
        with Image.open(src) as im:
            for w in widths:
                out = img_dir / f"{src.stem}-{w}.webp"
                if w < im.width:
                    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out, "WEBP", quality=80, method=6)


# ------------------------------------------------------------------ Block-Markup
def j(attrs):
    """Block-Attribute wie WordPress serialisieren (ohne Leerzeichen, Sonderzeichen escaped)."""
    if not attrs:
        return ""
    s = json.dumps(attrs, ensure_ascii=False, separators=(",", ":"))
    s = s.replace("--", "\\u002d\\u002d").replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return " " + s


def cls_attr(*parts):
    c = " ".join(p for p in parts if p)
    return f' class="{c}"' if c else ""


def ph(text):
    """[Platzhalter] markieren."""
    return re.sub(r"\[([^\]]+)\]", r'<mark class="bw-placeholder">[\1]</mark>', text)


def home(path=""):
    return "{{home:" + path + "}}"


def group(inner, cls="", tag="div", style=None, anchor=None, label=None):
    a = {}
    if tag != "div":
        a["tagName"] = tag
    classes = " ".join(x for x in (cls, f"is-style-{style}" if style else "") if x)
    if anchor:
        a["anchor"] = anchor
    if classes:
        a["className"] = classes
    if label:
        a["metadata"] = {"name": label}
    idattr = f' id="{anchor}"' if anchor else ""
    return f'<!-- wp:group{j(a)} -->\n<{tag}{idattr}{cls_attr("wp-block-group", classes)}>{inner}</{tag}>\n<!-- /wp:group -->'


def heading(text, level=2, cls="", anchor=None):
    a = {}
    if level != 2:
        a["level"] = level
    if anchor:
        a["anchor"] = anchor
    if cls:
        a["className"] = cls
    idattr = f' id="{anchor}"' if anchor else ""
    return f'<!-- wp:heading{j(a)} -->\n<h{level}{idattr}{cls_attr("wp-block-heading", cls)}>{text}</h{level}>\n<!-- /wp:heading -->'


def para(text, cls=""):
    a = {"className": cls} if cls else {}
    return f'<!-- wp:paragraph{j(a)} -->\n<p{cls_attr(cls)}>{text}</p>\n<!-- /wp:paragraph -->'


def lst(items, cls="", ordered=False, item_cls=None):
    a = {}
    if ordered:
        a["ordered"] = True
    if cls:
        a["className"] = cls
    tag = "ol" if ordered else "ul"
    lis = ""
    for i, t in enumerate(items):
        ic = item_cls[i] if item_cls else ""
        ia = {"className": ic} if ic else {}
        lis += f'<!-- wp:list-item{j(ia)} -->\n<li{cls_attr(ic)}>{t}</li>\n<!-- /wp:list-item -->'
    return f'<!-- wp:list{j(a)} -->\n<{tag}{cls_attr("wp-block-list", cls)}>{lis}</{tag}>\n<!-- /wp:list -->'


def button(text, url, style=None, cls=""):
    classes = " ".join(x for x in (cls, f"is-style-{style}" if style else "") if x)
    a = {"className": classes} if classes else {}
    return (f'<!-- wp:button{j(a)} -->\n<div{cls_attr("wp-block-button", classes)}><a class="wp-block-button__link wp-element-button" '
            f'href="{url}">{text}</a></div>\n<!-- /wp:button -->')


def buttons(*btns, cls=""):
    a = {"className": cls} if cls else {}
    return f'<!-- wp:buttons{j(a)} -->\n<div{cls_attr("wp-block-buttons", cls)}>{"".join(btns)}</div>\n<!-- /wp:buttons -->'


def details(summary, inner, cls=""):
    a = {"className": cls} if cls else {}
    return f'<!-- wp:details{j(a)} -->\n<details{cls_attr("wp-block-details", cls)}><summary>{summary}</summary>{inner}</details>\n<!-- /wp:details -->'


def quote(text, cite):
    return (f'<!-- wp:quote -->\n<blockquote class="wp-block-quote">{para(text)}<cite>{cite}</cite></blockquote>\n<!-- /wp:quote -->')


def image(src, alt, cls="", href=None, caption=None):
    a = {}
    if cls:
        a["className"] = cls
    if href:
        a["linkDestination"] = "custom"
    img = f'<img src="{src}" alt="{html.escape(alt, quote=True)}"/>'
    if href:
        img = f'<a href="{href}">{img}</a>'
    if caption:
        img += f'<figcaption class="wp-element-caption">{caption}</figcaption>'
    return f'<!-- wp:image{j(a)} -->\n<figure{cls_attr("wp-block-image", cls)}>{img}</figure>\n<!-- /wp:image -->'


def icon(name, cls="", size=None):
    assert name in ICONS, name
    a = {"icon": name}
    if size:
        a["size"] = size
    if cls:
        a["className"] = cls
    return f"<!-- wp:bw/icon{j(a)} /-->"


def form(kind, preselect=None):
    a = {"form": kind}
    if preselect:
        a["preselect"] = preselect
    return f"<!-- wp:bw/perma-form{j(a)} /-->"


def paras(lst_, cls="bw-text"):
    return "".join(para(ph(p), cls) for p in lst_)


def section_head(title, eyebrow=None, lead=None, center=False):
    inner = (para(eyebrow, "bw-eyebrow") if eyebrow else "") + heading(title, 2, "bw-heading-section") + (para(lead, "bw-section-head__lead") if lead else "")
    return group(inner, "bw-section-head bw-section-head--center" if center else "bw-section-head")


def container(inner, cls=""):
    return group(inner, ("bw-container " + cls).strip())


def accordion(title, inner):
    return details(title, inner, "bw-accordion")


def accordions(items, cls=""):
    return group("".join(items), ("bw-accordion-list " + cls).strip())


# ------------------------------------------------------------------ Abschnitte Startseite
OFFER_URL = {o: C.META[o]["url"] for o in ("basic", "advanced", "clinical")}


def p_hero():
    H = C.HERO
    first_sentence = H["paras"][0].split(". ")[0] + "."
    # Mobil nur Überschrift, ein Satz (bw-hero__lead) und Buttons; der lange Text (bw-hero__text) erst ab Tablet.
    box = group(heading(H["h1"], 1, "bw-hero__title") + para(first_sentence, "bw-hero__lead") + para(H["paras"][0], "bw-hero__text")
                + buttons(button(H["button_secondary"], "#interessentenliste"), button(H["button_primary"], "#ausbildungen", "secondary"), cls="bw-hero__actions"),
                "bw-hero__box bw-hero__box--wide")
    # Hintergrundbilder als normale Bild-Blöcke (im Editor austauschbar, dekorativ). Das Theme fasst beide beim Ausgeben
    # zu einem <picture> zusammen (src/HeroImage.php), damit jedes Gerät nur sein Bild lädt.
    images = (image("{{asset:assets/images/hero-sonnenaufgang-mobil.webp}}", "", "bw-hero__image bw-hero__image--mobile")
              + image("{{asset:assets/images/hero-sonnenaufgang.webp}}", "", "bw-hero__image bw-hero__image--desktop"))
    return group(images + box, "bw-hero bw-hero--v2b", "section", style="gradient-hero", label="Hero")


def p_highlights():
    items = "".join(group(icon(i, "bw-highlight__icon", 22) + para(t), "bw-highlight", style=f"accent-{a}")
                    for (a, i), t in zip([("blue", "globe"), ("purple", "flask"), ("green", "badge")], C.HERO["features"]))
    return group(container(group(items, "bw-highlights__list")), "bw-highlights", "section", style="section-navy", label="Profilmerkmale")


def p_intro():
    return group(para(C.HERO["paras"][1], "bw-intro__lead"), "bw-intro", "section", label="Einleitung")


def p_why():
    cards = "".join(group(icon(i, "bw-feature__icon", 26) + heading(t, 3, "bw-feature__title") + para(x, "bw-feature__text"),
                          "bw-feature bw-feature--raised", "article", style=f"accent-{a}")
                    for a, i, t, x in C.WHY["items"])
    return group(container(section_head(C.WHY["title"], center=True) + group(cards, "bw-grid bw-grid--3")),
                 "bw-block", "section", style="section-neutral", label="Warum PERMA Mind Academy")


def offer_card(o):
    facts = [f.strip() for f in o["card_meta"].split("·")]
    head = group(para(OFFER_CHIP[o["key"]], "bw-chip") + icon(OFFER_ICON[o["key"]], "bw-offer-card__icon", 30), "bw-offer-card__head")
    link = para(f'<a href="{home(OFFER_URL[o["key"]])}">{o["card_button"]} →</a>', "bw-link bw-link--on-dark bw-link--strong bw-offer-card__link")
    return group(head + heading(o["name"], 3, "bw-offer-card__title") + para(o["card_text"], "bw-offer-card__text")
                 + lst(facts, "bw-offer-card__facts") + link, "bw-offer-card", "article", style=f"accent-{o['accent']}")


def p_offers():
    return group(container(section_head(C.COURSES["title"], C.COURSES["eyebrow"], center=True)
                           + group("".join(offer_card(o) for o in C.OFFERS), "bw-offer-grid")),
                 "bw-block", "section", style="section-tint", anchor="ausbildungen", label="Angebotskarten")


PERMA = [("P", "blue", "Positive Emotionen"), ("E", "purple", "Engagement"), ("R", "orange", "Beziehungen"),
         ("M", "green", "Sinn"), ("A", "red", "Persönlich bedeutsame Ziele erreichen")]
STEPS = ["Ziele klären", "Methoden auswählen", "Erfahrungen reflektieren", "Die Anwendung anpassen"]


def p_understand():
    U = C.UNDERSTAND
    split = group(group(section_head(U["left_title"]) + paras(U["left"]), "bw-split__main")
                  + group(para("Das PERMA-Modell", "bw-eyebrow")
                          + lst([f"<strong>{l}</strong>{t}" for l, a, t in PERMA], "is-style-perma",
                                item_cls=[f"bw-accent--{a}" for l, a, t in PERMA]), "bw-split__aside"), "bw-split")
    apply_ = group(section_head(U["right_title"]) + paras(U["right"]) + lst(STEPS, "is-style-steps", ordered=True), "bw-apply")
    return group(container(split + apply_), "bw-block", "section", label="Positive Psychologie verstehen und anwenden")


def trainer(t):
    body = paras(t["profile"])
    if t["quote"]:
        body += quote(t["quote"][0], t["quote"][1])
    if t.get("figure"):
        f_src, f_alt, f_cap = t["figure"]
        body += image("{{asset:assets/images/" + f_src + "}}", f_alt, "bw-person__figure", caption=f_cap)
    body += paras(t["after"])
    if t.get("image"):
        photo = group(para(t["role"], "bw-person__role") + image("{{asset:assets/images/" + t["image"] + "}}", t["alt"], "bw-person__img"),
                      "bw-person__photo bw-person__photo--img")
    else:
        photo = group(para(t["role"], "bw-person__role") + icon("user", "bw-person__photo-icon", 72) + para(t["photo"], "bw-person__photo-label"),
                      "bw-person__photo")
    return group(photo + heading(t["name"], 3, "bw-person__name") + para(t["teaser"], "bw-person__bio") + accordion("Profil lesen", body),
                 "bw-person", "article")


def research(R):
    """Fotos aus der Forschungsarbeit unter den Trainerprofilen, mit Ort/Datum und Bildunterschrift."""
    if not R:
        return ""
    figs = "".join(image("{{asset:assets/images/" + f + "}}", alt, "bw-research__figure", caption=f"<strong>{place}</strong><br>{text}")
                   for f, alt, place, text in R["figures"])
    return group(heading(R["title"], 3, "bw-research__title") + group(figs, "bw-research__grid"), "bw-research")


def p_about():
    A = C.ABOUT
    acc = accordions([accordion(t, paras(p)) for t, p in A["accordions"]], "bw-accordion-list--limit")
    return group(container(section_head(A["title"], A["eyebrow"], A["intro"]) + acc
                           + group("".join(trainer(t) for t in A["trainers"]), "bw-team__list") + research(A.get("research"))),
                 "bw-block", "section", style="section-neutral", anchor="ueber-uns", label="Über uns und Trainer")


def p_cert():
    Z = C.CERT
    main = group(section_head(Z["title"], Z["eyebrow"]) + paras(Z["paras"])
                 + buttons(button(Z["button"], "#ausbildungen", "secondary"), cls="bw-cert__button"), "bw-split__main")
    aside = group(para(ph(Z["logo_placeholder"]), "bw-cert__logo")
                  + accordions([accordion(t, paras(p)) for t, p in Z["accordions"]]), "bw-split__aside")
    return group(container(group(main + aside, "bw-split")), "bw-block", "section", anchor="zertifizierung", label="ECQA-Zertifizierung")


def fab():
    return para(f'<a href="#interessentenliste">Zur Interessentenliste</a>', "bw-fab")


def interest(title, text, pre=None, accent=None):
    side = group(para("Unverbindliche Interessentenliste", "bw-eyebrow bw-eyebrow--on-dark") + heading(title, 2, "bw-form-card__title")
                 + para(text, "bw-form-card__text")
                 + group(icon("badge-check", "bw-form-card__note-icon") + para(C.LIST["intro2"], "bw-form-card__note-text"), "bw-form-card__note"),
                 "bw-form-card__side")
    card = group(side + group(form("interest", pre), "bw-form-card__form"),
                 "bw-form-card bw-form-card--accent" if accent else "bw-form-card", style=f"accent-{accent}" if accent else None)
    return group(container(card) + fab(), "bw-block", "section", anchor="interessentenliste", label="Interessentenliste")


def p_interest():
    return interest(C.NEXT_STEP["title"], C.NEXT_STEP["text"])


def p_faq():
    F = C.FAQ
    return group(container(section_head(F["title"], F["eyebrow"], center=True)
                           + accordions([accordion(q, para(a, "bw-text")) for q, a in F["items"]], "bw-accordion-list--center")),
                 "bw-block", "section", style="section-neutral", anchor="fragen", label="Häufige Fragen")


def p_newsletter():
    N = C.NEWSLETTER
    return group(container(group(group(section_head(N["title"], N["eyebrow"], N["text"]), "bw-columns__item")
                                 + group(form("newsletter"), "bw-columns__item bw-form-slot"), "bw-columns")),
                 "bw-block", "section", style="section-tint", anchor="newsletter", label="Newsletter")


def p_contact():
    K = C.CONTACT
    items = "".join(group(icon(i, "bw-contact-list__icon") + para(t), "bw-contact-list__item")
                    for i, t in (("mail", CONTACT_DATA["mail"]), ("phone", CONTACT_DATA["phone"]), ("pin", CONTACT_DATA["address"])))
    left = group(section_head(K["title"], lead=K["text"]) + group(items, "bw-contact-list"), "bw-columns__item")
    return group(container(group(left + group(form("contact"), "bw-columns__item bw-form-slot"), "bw-columns")),
                 "bw-block", "section", anchor="kontakt", label="Kontakt")


# ------------------------------------------------------------------ Abschnitte Angebotsseiten
def offer_of(key):
    return next(x for x in C.OFFERS if x["key"] == key)


def p_offer_hero(key):
    P, o = C.PAGES[key], offer_of(key)
    crumbs = f'<a href="{home("/")}">Startseite</a> / <a href="{home("/#ausbildungen")}">Ausbildungen</a> / {o["name"]}'
    lead = P["lead"]
    texts = para(lead[0], "bw-page-hero__lead") + "".join(
        para(p.replace("abgeschlossene Basic-Ausbildung", f'abgeschlossene <a href="{home(OFFER_URL["basic"])}">Basic-Ausbildung</a>') if key == "advanced" else p,
             "bw-page-hero__text") for p in lead[1:])
    inner = (para(crumbs, "bw-crumbs") + para(P["eyebrow"], "bw-chip bw-page-hero__chip") + heading(P["h1"], 1, "bw-page-hero__title") + texts
             + buttons(button(o["list_button"], "#interessentenliste", "light"), button("Alle Ausbildungen vergleichen", home("/#ausbildungen"), "secondary"),
                       cls="bw-page-hero__actions"))
    return group(container(inner, "bw-page-hero__inner"), "bw-page-hero bw-page-hero--offer", "section",
                 style=f"accent-{o['accent']}", label="Angebotskopf")


def facts_card(key):
    P, o = C.PAGES[key], offer_of(key)
    rows = ""
    for f in P["facts"]:
        if f[0] == "Kosten":
            val = "".join(para(x.strip(), "bw-facts__price") for x in f[1].split(" / "))
        else:
            val = para(f[1], "bw-facts__value")
        note = para(f[2], "bw-facts__note") if len(f) > 2 else ""
        rows += group(para(f[0], "bw-facts__term") + val + note, "bw-facts__row")
    return group(heading("Das Angebot auf einen Blick", 2, "bw-facts-card__title") + group(rows, "bw-facts")
                 + buttons(button(o["list_button"], "#interessentenliste"), cls="bw-facts-card__actions"),
                 "bw-facts-card", style=f"accent-{o['accent']}")


def related():
    links = [("/#ausbildungen", "Zur Ausbildungsauswahl"), ("/#ueber-uns", "Trainer kennenlernen"),
             ("/#zertifizierung", "ECQA-Zertifizierung"), ("/#fragen", "Häufige Fragen")]
    return group("".join(para(f'<a href="{home(u)}">{t} →</a>', "bw-related__link") for u, t in links), "bw-related", "nav")


def module_body(text, goals=None):
    """Modultext; optional mit Lernzielen („Was du nach dem Modul kannst“, Clinical Expert)."""
    out = para(text, "bw-text")
    if goals:
        out += para("Was du nach dem Modul kannst", "bw-module__goals-title") + lst(goals, "bw-module__goals")
    return out


def p_offer_details(key):
    P = C.PAGES[key]
    scope = paras(P["scope"])
    if P.get("scope_more"):
        title, texts = P["scope_more"]
        scope += heading(title, 4, "bw-card__subtitle") + paras(texts)
    if P.get("scope_link"):
        kk, label = P["scope_link"]
        scope += para(f'<a href="{home(OFFER_URL[kk])}">{label} →</a>', "bw-text bw-link-strong")
    main = (section_head(P["content_title"]) + accordions([accordion(m[0], module_body(*m[1:])) for m in P["modules"]])
            + group(heading(P["scope_title"], 3, "bw-card__title") + scope, "bw-card bw-card--plain"))
    for title, texts in P.get("extras", []):
        main += group(heading(title, 3, "bw-card__title") + paras(texts), "bw-card")
    split = group(group(main, "bw-split__main") + group(facts_card(key) + related(), "bw-split__aside", "aside"), "bw-split")
    return group(container(split), "bw-block", "section", label="Inhalte, Eckdaten und Weiterführendes")


def p_offer_interest(key):
    P, o = C.PAGES[key], offer_of(key)
    return interest(P["list_title"], P["list_text"], pre=key, accent=o["accent"])


# ------------------------------------------------------------------ Rechtstexte (Entwurf aus v2)
def legal_blocks(fname):
    """Rechtstexte aus content/rechtstexte/ (Entwurf mit [Platzhaltern]) als Blöcke."""
    src = (ROOT / "content/rechtstexte" / fname).read_text("utf-8")
    main = re.search(r"<main>(.*?)</main>", src, re.S).group(1)
    lead = re.search(r'<p class="bw-page-hero__lead">(.*?)</p>', main, re.S)
    art = re.search(r'<article class="bw-prose">(.*?)</article>', main, re.S).group(1)
    fix = lambda s: re.sub(r'<span class="bw-placeholder">(.*?)</span>', r'<mark class="bw-placeholder">\1</mark>', s.replace('href="Main.dc.html"', f'href="{home("/")}"')).strip()
    out = [para(fix(lead.group(1)), "bw-prose__lead")] if lead else []
    for m in re.finditer(r'<(h2|h3|p|address|ul|ol|nav)([^>]*)>(.*?)</\1>', art, re.S):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        cl = re.search(r'class="([^"]*)"', attrs)
        cl = cl.group(1) if cl else ""
        anchor = re.search(r'id="([^"]*)"', attrs)
        anchor = anchor.group(1) if anchor else None
        if tag in ("h2", "h3"):
            out.append(heading(fix(inner), int(tag[1]), anchor=anchor))
        elif tag == "p":
            out.append(para(fix(inner), cl))
        elif tag == "address":
            out.append(para(fix(inner), "bw-prose__address"))
        elif tag in ("ul", "ol"):
            out.append(lst([fix(x) for x in re.findall(r"<li>(.*?)</li>", inner, re.S)], ordered=tag == "ol"))
        elif tag == "nav":
            title = re.search(r'<strong class="bw-toc__title">(.*?)</strong>', inner).group(1)
            items = [fix(x) for x in re.findall(r"<li>(.*?)</li>", inner, re.S)]
            out.append(group(para(title, "bw-toc__title") + lst(items, "bw-toc__list", ordered=True), "bw-toc", "nav"))
    return "".join(out)


# ------------------------------------------------------------------ Pattern-Dateien
def php_markup(markup):
    """{{home:/pfad}} -> PHP-Ausgabe der Adresse auf der jeweiligen Installation."""
    return re.sub(r"\{\{home:([^}]*)\}\}", lambda m: f"<?php echo esc_url( home_url( '{m.group(1)}' ) ); ?>", markup)


def write_pattern(name, title, markup, desc="", inserter=True, block_types=None, post_types=None, cats=SLUG, keywords=""):
    head = [f" * Title: {title}", f" * Slug: {SLUG}/{name}", f" * Categories: {cats}"]
    if desc:
        head.append(f" * Description: {desc}")
    if keywords:
        head.append(f" * Keywords: {keywords}")
    if block_types:
        head.append(f" * Block Types: {block_types}")
    if post_types:
        head.append(f" * Post Types: {post_types}")
    head.append(f" * Inserter: {'true' if inserter else 'false'}")
    php = "<?php\n/**\n" + "\n".join(head) + f"\n *\n * {GEN_NOTE}\n *\n * @package PermaMind\n */\n\ndeclare(strict_types=1);\n?>\n" + php_markup(markup) + "\n"
    (THEME / "patterns" / f"{name}.php").write_text(php, "utf-8")


def build_patterns():
    d = THEME / "patterns"
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.php"):
        old.unlink()
    home_sections = [
        ("hero", "Hero Startseite", p_hero()),
        ("highlights", "Profilmerkmale", p_highlights()),
        ("intro", "Einleitung", p_intro()),
        ("why", "Warum PERMA Mind Academy", p_why()),
        ("offers", "Angebotskarten (3)", p_offers()),
        ("understand", "Positive Psychologie verstehen + PERMA-Modell + Vom Verstehen zum Anwenden", p_understand()),
        ("about", "Über uns + Trainer", p_about()),
        ("certification", "ECQA-Zertifizierung", p_cert()),
        ("interest-list", "Interessentenliste (Formular)", p_interest()),
        ("faq", "Häufige Fragen", p_faq()),
        ("newsletter", "Newsletter (Formular)", p_newsletter()),
        ("contact", "Kontakt (Formular)", p_contact()),
    ]
    for name, title, m in home_sections:
        write_pattern(name, title, m)
    # Angebotsseiten: Abschnitte als Vorlage (Basic als Beispiel), komplette Seiten je Angebot
    write_pattern("offer-hero", "Angebotskopf", p_offer_hero("basic"), "Kopfbereich einer Angebotsseite. Akzent über den Stil des Abschnitts wählen.")
    write_pattern("offer-details", "Angebot: Module, Umfang, Eckdaten, Weiterführend", p_offer_details("basic"))
    write_pattern("offer-interest-list", "Interessentenliste für ein Angebot", p_offer_interest("basic"), "Lehrgang im Formular vorausgewählt.")
    pages = {"home": ("Seite: Startseite", "".join(m for _, _, m in home_sections))}
    for key in ("basic", "advanced", "clinical"):
        pages[key] = (f"Seite: {offer_of(key)['name']}", p_offer_hero(key) + p_offer_details(key) + p_offer_interest(key))
    pages["impressum"] = ("Seite: Impressum (Entwurf)", legal_blocks("impressum.html"))
    pages["datenschutz"] = ("Seite: Datenschutz (Entwurf)", legal_blocks("datenschutz.html"))
    pages["agb"] = ("Seite: AGB (Entwurf)", legal_blocks("agb.html"))
    for key, (title, m) in pages.items():
        write_pattern(f"page-{key}", title, m, "Kompletter Seiteninhalt.", inserter=True,
                      block_types="core/post-content", post_types="page", cats=f"{SLUG}-pages")
    # Header und Footer (für die Vorlagenteile)
    write_pattern("header-bar", "Header", header_bar(False), inserter=False)
    write_pattern("header-bar-accent", "Header Akzent", header_bar(True), inserter=False)
    write_pattern("footer", "Footer", footer(), inserter=False)
    write_pattern("not-found", "Seite nicht gefunden", not_found(), inserter=False)
    return [n for n, _, _ in home_sections], list(pages)


def nav():
    sub = "".join(f'<!-- wp:navigation-link{j({"label": o["name"], "url": home(OFFER_URL[o["key"]]), "kind": "custom"})} /-->' for o in C.OFFERS)
    items = [("Über uns", "ueber-uns"), ("Zertifizierung", "zertifizierung"), ("Fragen", "fragen"), ("Kontakt", "kontakt")]
    links = "".join(f'<!-- wp:navigation-link{j({"label": t, "url": home("/#" + a), "kind": "custom"})} /-->' for t, a in items)
    cta = f'<!-- wp:navigation-link{j({"label": "Zur Interessentenliste", "url": "#interessentenliste", "kind": "custom", "className": "bw-nav__cta"})} /-->'
    a = {"overlayMenu": "mobile", "className": "bw-nav", "layout": {"type": "flex", "justifyContent": "center"},
         "ariaLabel": "Hauptnavigation"}
    return (f'<!-- wp:navigation{j(a)} -->'
            f'<!-- wp:navigation-submenu{j({"label": "Ausbildungen", "url": home("/#ausbildungen"), "kind": "custom"})} -->{sub}<!-- /wp:navigation-submenu -->'
            f'{links}{cta}<!-- /wp:navigation -->')


def header_bar(accent):
    logo = "{{asset:assets/images/" + ("logo-white.svg" if accent else "logo.svg") + "}}"
    return group(image(logo, "PERMA Mind Academy – We create wellbeing", "bw-header__logo", href=home("/"))
                 + nav()
                 + buttons(button("Zur Interessentenliste", "#interessentenliste", "light" if accent else None), cls="bw-header__cta"),
                 "bw-header__bar")


def footer():
    D = CONTACT_DATA
    cols = (group(image("{{asset:assets/images/logo-white.svg}}", "PERMA Mind Academy – We create wellbeing", "bw-footer__logo"), "bw-footer__col")
            + group(para("Kontakt", "bw-footer__title") + para(D["address"]) + para(f'Tel: {D["phone"]}') + para(f'Mail: {D["mail"]}'), "bw-footer__col")
            + group(para("Social Media", "bw-footer__title")
                    + '<!-- wp:social-links {"openInNewTab":true,"className":"bw-footer__social"} -->\n<ul class="wp-block-social-links bw-footer__social">'
                    + "".join(f'<!-- wp:social-link {j({"url": u, "service": sv})} /-->' for sv, u in C.SOCIAL if u)
                    + '</ul>\n<!-- /wp:social-links -->',
                    "bw-footer__col bw-footer__col--social")
            + group("".join(para(f'<a href="{home(u)}">{t}</a>', "bw-footer__link") for u, t in
                            (("/#kontakt", "Kontakt"), ("/#newsletter", "Newsletter"), ("/impressum/", "Impressum"), ("/datenschutz/", "Datenschutz"), ("/agb/", "AGB"))),
                    "bw-footer__col bw-footer__col--legal"))
    return group(cols, "bw-container bw-footer__inner")


def not_found():
    inner = (para("Fehler 404", "bw-eyebrow") + heading("Diese Seite gibt es nicht", 1, "bw-page-hero__title")
             + para("Vielleicht hat sich die Adresse geändert. Auf der Startseite findest du alle Ausbildungen.", "bw-page-hero__lead")
             + buttons(button("Zur Startseite", home("/")), cls="bw-page-hero__actions"))
    return group(container(inner, "bw-page-hero__inner"), "bw-page-hero", "section", style="gradient-page")


def finalize_assets_in_patterns():
    for f in (THEME / "patterns").glob("*.php"):
        s = f.read_text("utf-8")
        s = re.sub(r"\{\{asset:([^}]*)\}\}", lambda m: f"<?php echo esc_url( get_theme_file_uri( '{m.group(1)}' ) ); ?>", s)
        f.write_text(s, "utf-8")


def p_newsletter_confirmed():
    inner = (para("Newsletter", "bw-eyebrow") + heading("Danke, deine Anmeldung ist bestätigt", 1, "bw-page-hero__title")
             + para("Du erhältst ab jetzt den Newsletter der PERMA Mind Academy mit Neuigkeiten zu Ausbildungen und Terminen. "
                    "Abmelden kannst du dich jederzeit über den Link am Ende jeder Ausgabe.", "bw-page-hero__lead")
             + buttons(button("Zu den Ausbildungen", home("/#ausbildungen")), cls="bw-page-hero__actions"))
    return group(container(inner, "bw-page-hero__inner"), "bw-page-hero", "section", style="gradient-page", label="Newsletter bestätigt")


# ------------------------------------------------------------------ Seiteninhalte für die Übertragung (Phase 3)
def build_content():
    """Seiteninhalte als Block-Markup mit {{home:/pfad}}-Platzhaltern; beim Übertragen durch die Website-Adresse ersetzt."""
    d = ROOT / "wordpress/content"
    d.mkdir(parents=True, exist_ok=True)
    home_m = "".join(f() for f in (p_hero, p_highlights, p_intro, p_why, p_offers, p_understand, p_about, p_cert, p_interest, p_faq, p_newsletter, p_contact))
    pages = {
        "startseite": {"title": "Startseite", "slug": "startseite", "template": "", "front": True, "markup": home_m, "meta": C.META["index"]},
    }
    for key in ("basic", "advanced", "clinical"):
        pages[key] = {"title": offer_of(key)["name"], "slug": C.META[key]["url"].strip("/"), "template": "page-angebot",
                      "markup": p_offer_hero(key) + p_offer_details(key) + p_offer_interest(key), "meta": C.META[key]}
    pages["impressum"] = {"title": "Impressum", "slug": "impressum", "template": "page-rechtliches", "markup": legal_blocks("impressum.html"),
                          "meta": {"title": "Impressum | PERMA Mind Academy", "desc": "Impressum der PERMA Mind Academy."}}
    pages["datenschutz"] = {"title": "Datenschutzerklärung", "slug": "datenschutz", "template": "page-rechtliches",
                            "markup": legal_blocks("datenschutz.html"),
                            "meta": {"title": "Datenschutz | PERMA Mind Academy", "desc": "Datenschutzerklärung der PERMA Mind Academy."}}
    pages["agb"] = {"title": "Allgemeine Geschäftsbedingungen", "slug": "agb", "template": "page-rechtliches",
                    "markup": legal_blocks("agb.html"),
                    "meta": {"title": "AGB | PERMA Mind Academy", "desc": "Allgemeine Geschäftsbedingungen der PERMA Mind Academy für Workshops, Seminare und Ausbildungen."}}
    pages["newsletter-bestaetigt"] = {"title": "Newsletter bestätigt", "slug": "newsletter-bestaetigt", "template": "",
                                      "markup": p_newsletter_confirmed(),
                                      "meta": {"title": "Newsletter bestätigt | PERMA Mind Academy", "desc": "Deine Anmeldung zum Newsletter der PERMA Mind Academy ist bestätigt."}}
    index = []
    for key, p in pages.items():
        (d / f"{key}.html").write_text(p["markup"] + "\n", "utf-8")
        index.append({"key": key, "file": f"{key}.html", "title": p["title"], "slug": p["slug"], "template": p["template"],
                      "front_page": bool(p.get("front")), "seo_title": p["meta"]["title"], "seo_description": p["meta"]["desc"]})
    (d / "pages.json").write_text(json.dumps({"$comment": GEN_NOTE, "pages": index}, ensure_ascii=False, indent=1) + "\n", "utf-8")
    return list(pages)


if __name__ == "__main__":
    (THEME / "assets/css").mkdir(parents=True, exist_ok=True)
    build_theme_json()
    build_tokens_css()
    icons = build_assets()
    sections, pages = build_patterns()
    finalize_assets_in_patterns()
    content = build_content()
    print(f"theme.json, tokens.css, {len(icons)} Icons, {len(sections)} Abschnitts-Patterns, {len(pages)} Seiten-Patterns, "
          f"{len(content)} Seiteninhalte -> {THEME.relative_to(ROOT)}")
