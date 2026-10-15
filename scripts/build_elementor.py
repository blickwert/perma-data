#!/usr/bin/env python3
"""Erzeugt Elementor-Templates (Atomic Editor / Elementor 4) aus Tokens + Inhalt.

    python3 scripts/build_elementor.py

Quellen : tokens/tokens.json, content/content.json, assets/icons/icons.json
Ausgabe : templates/elementor/*.json   (je Sektion) + full-page.json (ganze Seite)

Es werden ausschliesslich Atomic-Elemente verwendet:
e-flexbox, e-div-block, e-heading, e-paragraph, e-button, e-image
Ausnahmen (noch kein Atomic-Aequivalent): Inline-SVG-Icons und Formular
-> Widget "html".  Alle Styles sind lokale Klassen-Styles pro Element.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOK = json.loads((ROOT / "tokens/tokens.json").read_text("utf-8"))
CONTENT = json.loads((ROOT / "content/content.json").read_text("utf-8"))
ICONS = json.loads((ROOT / "assets/icons/icons.json").read_text("utf-8"))
C = TOK["color"]
F = TOK["font"]

_seen = {}


def rid(seed):
    """Deterministische, eindeutige 7-stellige Element-ID."""
    n = _seen.get(seed, 0)
    _seen[seed] = n + 1
    return hashlib.sha1(f"{seed}#{n}".encode()).hexdigest()[:7]


# --------------------------------------------------------------- Prop-Typen
def T(t, v):
    return {"$$type": t, "value": v}


def size(n, unit="px"):
    return T("size", {"size": n, "unit": unit})


def color(c):
    return T("color", c)


def dims(top, right=None, bottom=None, left=None):
    if right is None:
        right = bottom = left = top
    d = lambda v: size("", "auto") if v == "auto" else size(v)
    return T("dimensions", {"block-start": d(top), "inline-end": d(right),
                            "block-end": d(bottom), "inline-start": d(left)})


def gradient(angle, stops):
    return T("background", {"background-overlay": T("background-overlay", [
        T("background-gradient-overlay", {
            "type": T("string", "linear"),
            "angle": T("number", angle),
            "stops": T("gradient-color-stop", [
                T("color-stop", {"color": color(c), "offset": T("number", off)}) for c, off in stops]),
        })])})


SIZE_KEYS = {"font-size", "gap", "row-gap", "column-gap", "min-height", "min-width", "max-width",
             "width", "height", "letter-spacing", "border-radius", "top", "right", "bottom", "left",
             "flex-basis"}
NUMBER_KEYS = {"z-index", "flex-grow", "flex-shrink"}
COLOR_KEYS = {"color", "border-color"}


def props(p):
    """Wandelt kompakte CSS-artige Angaben in Atomic-Props."""
    out = {}
    for k, v in p.items():
        if k in ("padding", "margin"):
            out[k] = dims(*v) if isinstance(v, (list, tuple)) else dims(v)
        elif k == "border-width":
            out[k] = dims(*v) if isinstance(v, (list, tuple)) else dims(v)
        elif k == "line-height":
            out[k] = size(v, "em")
        elif k == "bg":
            out["background"] = (T("background", {"color": color(v)}) if isinstance(v, str)
                                 else gradient(*v))
        elif k in ("background-color",):
            out["background"] = T("background", {"color": color(v)})
        elif k in SIZE_KEYS and v == "auto":
            out[k] = size("", "auto")
        elif k in SIZE_KEYS:
            out[k] = size(*v) if isinstance(v, (list, tuple)) else size(v)
        elif k in NUMBER_KEYS:
            out[k] = T("number", v)
        elif k in COLOR_KEYS:
            out[k] = color(v)
        elif k == "box-shadow":
            out[k] = T("box-shadow", [T("shadow", {
                "hOffset": size(0), "vOffset": size(10), "blur": size(30), "spread": size(-8),
                "color": color("rgba(15,23,42,0.18)"), "position": None})])
        else:
            out[k] = T("string", v)
    return out


def style(seed, base, tablet=None, mobile=None):
    cid = "e-" + rid("c" + seed)
    variants = [{"meta": {"breakpoint": "desktop", "state": None}, "props": props(base)}]
    for bp, p in (("tablet", tablet), ("mobile", mobile)):
        if p:
            variants.append({"meta": {"breakpoint": bp, "state": None}, "props": props(p)})
    return cid, {cid: {"id": cid, "label": "local", "type": "class", "variants": variants}}


def el(kind, seed, base, settings=None, children=None, tablet=None, mobile=None, anchor=None,
       widget=False):
    cid, styles = style(seed, base, tablet, mobile)
    s = {"classes": T("classes", [cid])}
    if anchor:
        s["_cssid"] = T("string", anchor)
    s.update(settings or {})
    node = {"id": rid("n" + seed), "elType": "widget" if widget else kind,
            "settings": s, "elements": children or [], "styles": styles}
    if widget:
        node["widgetType"] = kind
    return node


# ------------------------------------------------------------------ Bausteine
def flex(seed, children, base=None, **kw):
    return el("e-flexbox", seed, {"display": "flex", **(base or {})}, children=children, **kw)


def block(seed, children, base=None, **kw):
    return el("e-div-block", seed, base or {}, children=children, **kw)


def heading(seed, text, tag="h2", base=None, link=None, **kw):
    s = {"title": T("html", text), "tag": T("string", tag)}
    b = {"margin": 0, "font-weight": "500", "line-height": 1.25, "color": C["navy"],
         "font-family": F["heading"], **(base or {})}
    return el("e-heading", seed, b, s, widget=True, **kw)


def para(seed, text, base=None, **kw):
    b = {"margin": 0, "font-size": 16, "color": C["navy"], **(base or {})}
    return el("e-paragraph", seed, b, {"paragraph": T("html", text)}, widget=True, **kw)


def link_prop(href):
    return T("link", {"destination": T("url", href), "isTargetBlank": None})


def button(seed, text, href, base=None, **kw):
    b = {"text-decoration": "none", **(base or {})}
    return el("e-button", seed, b, {"text": T("string", text), "link": link_prop(href)},
              widget=True, **kw)


def image(seed, alt, base=None, **kw):
    # Platzhalter-Bild: in Elementor per Medienbibliothek ersetzen
    return el("e-image", seed, {"width": (100, "%"), "object-fit": "cover", **(base or {})},
              {"image": T("image", {"src": T("image-src", {"id": None, "url": None}),
                                    "size": T("string", "full")}),
               "alt": T("string", alt)}, widget=True, **kw)


def html(seed, markup):
    """Fallback-Widget fuer Inline-SVG / Formular."""
    cid, styles = style("h" + seed, {"display": "block"})
    return {"id": rid("h" + seed), "elType": "widget", "widgetType": "html",
            "settings": {"html": markup}, "elements": [], "styles": {}}


def svg(name, px=26, stroke_w=None, cls=""):
    sw = f' stroke-width="{stroke_w}"' if stroke_w else ""
    return (f'<span style="display:inline-flex;{cls}"><svg width="{px}" height="{px}" '
            f'viewBox="0 0 24 24" fill="none" stroke="currentColor"{sw} stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg></span>')


def tag(seed, text):
    return para(seed, text, {"background-color": C["aqua"], "color": C["navy"], "font-size": 11,
                             "font-weight": "500", "letter-spacing": (0.14, "em"),
                             "text-transform": "uppercase", "padding": (3, 8, 3, 8),
                             "align-self": "flex-start"})


def eyebrow(seed, text, col=None):
    return para(seed, text, {"font-size": 12, "font-weight": "500", "letter-spacing": (0.24, "em"),
                             "text-transform": "uppercase", "color": col or C["navy"]})


def section_head(seed, eyebrow_text, title, intro=None, center=False):
    kids = []
    if eyebrow_text:
        kids.append(para(seed + "e", eyebrow_text, {"font-size": 14, "font-weight": "500",
                                                    "letter-spacing": (0.08, "em"),
                                                    "text-transform": "uppercase"}))
    kids.append(heading(seed + "h", title, "h2", {"font-size": 30},
                        mobile={"font-size": 24}))
    if intro:
        kids.append(para(seed + "p", intro, {"margin": (12, 0, 0, 0), "max-width": 640,
                                             **({"text-align": "center"} if center else {})}))
    return flex(seed + "hd", kids, {"flex-direction": "column", "gap": 6,
                                    **({"align-items": "center", "text-align": "center"} if center else {})})


def wrap(seed, children, bg=None, pad=(88, 32, 96, 32), mpad=(56, 20, 64, 20), gap=48, anchor=None,
         inner=None):
    """Vollbreite Sektion + zentrierter 1200px-Container."""
    cont = flex(seed + "i", children, {"max-width": 1200, "width": (100, "%"), "margin": (0, "auto", 0, "auto"),
                                       "flex-direction": "column", "gap": gap, "padding": pad,
                                       "box-sizing": "border-box", **(inner or {})},
                mobile={"padding": mpad})
    return flex(seed, [cont], {"flex-direction": "column", "width": (100, "%"),
                               **({"bg": bg} if bg else {})}, anchor=anchor)


# ------------------------------------------------------------------ Sektionen
def s_header():
    d = CONTENT["nav"]
    links = [button(f"nav{i}", t, h, {"font-size": 14, "color": C["navy"], "min-height": 44,
                                      "display": "inline-flex", "align-items": "center",
                                      "background-color": "transparent", "padding": (0, 0, 0, 0)})
             for i, (t, h) in enumerate(d["links"])]
    logo = image("logo", "PERMA Mind Academy – We create wellbeing", {"height": 56, "width": "auto",
                                                                      "object-fit": "contain"})
    logo["settings"]["link"] = link_prop("#oben")
    nav = flex("nav", links, {"flex-wrap": "wrap", "gap": (4, ), "column-gap": 32, "justify-content": "center",
                              "flex-grow": 1, "flex-basis": 440}, mobile={"display": "none"})
    cta = button("navcta", d["cta"], "#kontakt",
                 {"background-color": C["navy"], "color": "#FFFFFF", "font-size": 15, "font-weight": "500",
                  "padding": (0, 24, 0, 24), "min-height": 44, "border-radius": 999,
                  "display": "inline-flex", "align-items": "center"}, mobile={"display": "none"})
    burger = html("burger", MOBILE_NAV)
    row = flex("hdrow", [logo, nav, cta, burger],
               {"flex-wrap": "wrap", "gap": 12, "column-gap": 32, "align-items": "center",
                "justify-content": "space-between", "padding": (16, 40, 16, 40), "box-sizing": "border-box"},
               mobile={"padding": (12, 20, 12, 20), "flex-wrap": "nowrap"})
    return flex("header", [row], {"position": "sticky", "top": 0, "z-index": 20, "bg": "#FFFFFF",
                                  "flex-direction": "column", "width": (100, "%"),
                                  "border-width": (0, 0, 1, 0), "border-style": "solid",
                                  "border-color": C["mint"]})


MOBILE_NAV = """<style>
.pma-mnav{display:none;position:relative}
.pma-mnav summary{list-style:none;cursor:pointer;width:44px;height:44px;display:flex;align-items:center;justify-content:center;border-radius:50%;border:1px solid #C9DAD9;color:#00416B}
.pma-mnav summary::-webkit-details-marker{display:none}
.pma-mnav-panel{position:absolute;right:-20px;width:100vw;top:calc(100% + 12px);background:#fff;padding:4px 20px 20px;box-shadow:0 14px 24px -12px rgba(0,65,107,.3);display:flex;flex-direction:column}
.pma-mnav-panel a{min-height:52px;display:flex;align-items:center;text-decoration:none;border-bottom:1px solid #E4F4F4;font-size:17px;color:#00416B}
.pma-mnav-panel a.cta{margin-top:16px;border:0;justify-content:center;background:#00416B;color:#fff;border-radius:999px;font-weight:500}
@media (max-width:767px){.pma-mnav{display:block;margin-left:auto}}
</style>
<details class="pma-mnav"><summary aria-label="Menü öffnen"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></summary>
<div class="pma-mnav-panel"><a href="#ueber-uns">Über uns</a><a href="#angebot">Angebot</a><a href="#ausbildungen">Ausbildungen</a><a href="#team">Team</a><a href="#kontakt">Kontakt</a><a class="cta" href="#kontakt">Unverbindlich anfragen</a></div></details>"""


def s_hero():
    d = CONTENT["hero"]
    links = flex("herolinks", [
        button("hero1", d["cta"], "#kontakt", {"color": C["navy"], "font-size": 16, "font-weight": "500",
                                              "background-color": "transparent", "padding": (0, 0, 4, 0),
                                              "border-width": (0, 0, 1, 0), "border-style": "solid",
                                              "border-color": C["navy"]}),
        button("hero2", d["cta2"], "#ausbildungen", {"color": C["navy"], "font-size": 16,
                                                    "background-color": "transparent", "padding": (0, 0, 4, 0),
                                                    "border-width": (0, 0, 1, 0), "border-style": "solid",
                                                    "border-color": C["navy"]}),
    ], {"flex-wrap": "wrap", "gap": 12, "column-gap": 28, "align-items": "center", "margin": (8, 0, 0, 0)})
    box = flex("herobox", [
        heading("herot", d["title"], "h1", {"font-size": 36, "line-height": 1.2}, mobile={"font-size": 28}),
        para("heroslogan", d["slogan"], {"font-family": F["script"], "font-size": 47, "line-height": 1.1,
                                          "font-weight": "400"}, mobile={"font-size": 38}),
        links,
    ], {"flex-direction": "column", "gap": 20, "bg": C["aqua_glass"], "padding": (40, 40, 40, 40),
        "width": 520, "max-width": (100, "%"), "box-sizing": "border-box", "position": "absolute",
        "right": (10, "%"), "top": (50, "%")},
        mobile={"position": "relative", "right": "auto", "top": "auto", "padding": (28, 28, 28, 28),
                "margin": (0, 20, 48, 20), "width": "auto"})
    # Hero-Bild liegt als Hintergrund-Platzhalter (Verlauf); Foto in Elementor als Hintergrund ergaenzen
    return flex("hero", [box], {"position": "relative", "min-height": 560, "overflow": "hidden",
                                "bg": (180, [("#8FCBE6", 0), ("#C9E6EE", 42), ("#86B0B0", 66), ("#8A5F59", 100)]),
                                "width": (100, "%")},
                mobile={"min-height": 0, "padding": (260, 0, 0, 0)})


def s_intro():
    d = CONTENT["intro"]
    stats = flex("stats", [
        flex(f"stat{i}", [heading(f"statn{i}", n, "div", {"font-size": 44, "line-height": 1}),
                          para(f"statl{i}", l, {"font-size": 14, "margin": (6, 0, 0, 0)})],
             {"flex-direction": "column", "align-items": "center"})
        for i, (n, l) in enumerate(d["stats"])
    ], {"margin": (12, 0, 0, 0), "flex-wrap": "wrap", "gap": 16, "column-gap": 64, "justify-content": "center"})
    inner = flex("introc", [
        para("introp", d["text"], {"font-family": F["heading"], "font-size": 22, "line-height": 1.6,
                                    "font-weight": "500", "text-align": "center"}, mobile={"font-size": 18}),
        block("introline", [], {"width": 64, "height": 1, "bg": C["navy"]}),
        flex("introsub", [
            heading("introh", d["eyebrow"], "h2", {"font-size": 15}),
            para("introq", d["claim"], {"font-family": F["heading"], "font-size": 24, "line-height": 1.35,
                                         "font-weight": "500", "text-align": "center"}),
            stats], {"flex-direction": "column", "align-items": "center", "gap": 16}),
    ], {"max-width": 760, "width": (100, "%"), "margin": (0, "auto", 0, "auto"), "flex-direction": "column",
        "align-items": "center", "gap": 40, "padding": (88, 32, 80, 32), "box-sizing": "border-box"},
        mobile={"padding": (56, 20, 56, 20), "gap": 28})
    return flex("intro", [inner], {"flex-direction": "column", "width": (100, "%")}, anchor="ueber-uns")


def s_angebot():
    d = CONTENT["angebot"]
    cards = []
    for i, c in enumerate(d["cards"]):
        link_col = "#FFFFFF" if i == 0 else C["aqua"]
        cards.append(flex(f"ang{i}", [
            flex(f"angtop{i}", [tag(f"angtag{i}", f"Angebot {i + 1:02d}"),
                                html(f"angi{i}", svg(c["icon"], 30, "1.6", f"color:{C['aqua']}"))],
                 {"align-items": "center", "justify-content": "space-between"}),
            heading(f"angt{i}", c["title"], "h3", {"font-size": 34, "line-height": 1.25, "color": "#FFFFFF"},
                    mobile={"font-size": 26}),
            para(f"angp{i}", c["text"], {"color": "#FFFFFF", "max-width": 420}),
            button(f"angl{i}", "Mehr erfahren →", c["href"],
                   {"margin": ("auto", 0, 0, 0), "align-self": "flex-start", "color": link_col, "font-size": 15,
                    "background-color": "transparent", "padding": (0, 0, 4, 0), "border-width": (0, 0, 1, 0),
                    "border-style": "solid", "border-color": link_col}),
        ], {"flex-grow": 1, "flex-shrink": 1, "flex-basis": 440, "min-width": 0, "min-height": 340,
            "box-sizing": "border-box", "padding": (40, 40, 40, 40), "flex-direction": "column", "gap": 18,
            "bg": (135, [(c["from"], 0), (c["to"], 100)]), "color": "#FFFFFF"},
            mobile={"padding": (24, 24, 24, 24), "min-height": 0}))
    head = section_head("angh", None, d["title"], d["intro"], center=True)
    grid = flex("anggrid", cards, {"flex-wrap": "wrap", "gap": 12, "margin": (32, 0, 0, 0)})
    return wrap("angebot", [head, grid], bg=C["mint"], pad=(72, 32, 80, 32), mpad=(48, 20, 56, 20), gap=24,
                anchor="angebot")


def s_ausbildungen():
    d = CONTENT["ausbildungen"]
    head_inner = flex("ausbheadi", [section_head("ausbh", d["eyebrow"], d["title"], d["intro"])],
                      {"max-width": 1200, "width": (100, "%"), "margin": (0, "auto", 0, "auto"),
                       "padding": (56, 32, 48, 32), "box-sizing": "border-box", "flex-direction": "column"},
                      mobile={"padding": (48, 20, 32, 20)})
    head_wrap = flex("ausbheadw", [head_inner], {"flex-direction": "column", "width": (100, "%"),
                                                  "bg": C["off_white"]})
    rows = []
    for i, m in enumerate(d["modules"]):
        rows.append(flex(f"mod{i}", [
            heading(f"modn{i}", f"{i + 1:02d}", "div", {"font-size": 48, "line-height": 1, "flex-basis": 72,
                                                         "flex-shrink": 0}, mobile={"flex-basis": (100, "%")}),
            flex(f"modb{i}", [
                heading(f"modt{i}", m["title"], "h3", {"font-size": 26, "line-height": 1.3}),
                para(f"modp{i}", m["text"], {"max-width": 560}),
                button(f"modl{i}", "→ Mehr erfahren", m.get("href", "#kontakt"),
                       {"align-self": "flex-start", "margin": (4, 0, 0, 0), "font-size": 16, "font-weight": "500",
                        "min-height": 44, "color": C["navy"], "background-color": "transparent",
                        "text-decoration": "underline", "padding": (0, 0, 0, 0)}),
            ], {"flex-direction": "column", "gap": 8, "flex-grow": 1, "flex-shrink": 1, "flex-basis": 360,
                "min-width": 0}),
            flex(f"modm{i}", [tag(f"modtag{i}", m["level"]),
                              para(f"moddur{i}", f"Dauer: {m['duration']}", {"font-size": 15})],
                 {"flex-direction": "column", "gap": 8, "align-items": "flex-start", "flex-basis": 240,
                  "flex-shrink": 1, "min-width": 180}, mobile={"flex-basis": (100, "%")}),
        ], {"flex-wrap": "wrap", "gap": 20, "column-gap": 32, "align-items": "flex-start",
            "padding": (32, 0, 32, 0), "border-width": (0, 0, 1, 0), "border-style": "solid",
            "border-color": C["line"]}))
    list_wrap = flex("modlist", rows, {"max-width": 1200, "width": (100, "%"), "margin": (0, "auto", 0, "auto"),
                                       "flex-direction": "column", "padding": (24, 32, 0, 32),
                                       "box-sizing": "border-box"}, mobile={"padding": (24, 20, 0, 20)})
    b = d["banner"]
    banner = flex("banner", [
        image("bannerimg", b["image_alt"], {"flex-grow": 1.2, "flex-basis": 420, "min-height": 300,
                                            "bg": C["line"]}),
        flex("bannerbox", [
            tag("bannertag", b["tag"]),
            heading("bannert", b["title"], "h3", {"font-size": 32, "line-height": 1.2, "color": "#FFFFFF"},
                    mobile={"font-size": 26}),
            flex("bannerrow", [html("bannerico", svg("badge-check", 26, "1.8", f"color:{C['aqua']}")),
                               para("bannerp", b["text"], {"font-size": 15, "line-height": 1.6, "color": "#D5ECEC"})],
                 {"gap": 14, "align-items": "flex-start"}),
        ], {"flex-grow": 1, "flex-basis": 360, "min-width": 0, "box-sizing": "border-box", "padding": (40, 40, 40, 40),
            "bg": C["navy_dark"], "flex-direction": "column", "gap": 20, "justify-content": "center"},
            mobile={"padding": (24, 24, 24, 24)}),
    ], {"flex-wrap": "wrap", "max-width": 1200, "width": (100, "%"), "margin": (64, "auto", 96, "auto"),
        "padding": (0, 32, 0, 32), "box-sizing": "border-box"}, mobile={"padding": (0, 20, 0, 20)})
    return flex("ausbildungen", [head_wrap, list_wrap, banner], {"flex-direction": "column", "width": (100, "%")},
                anchor="ausbildungen")


def s_vorteile():
    d = CONTENT["vorteile"]
    items = [flex(f"vt{i}", [
        html(f"vti{i}", svg(it["icon"], 28, "1.6", f"color:{C['navy']}")),
        heading(f"vtt{i}", it["title"], "h3", {"font-size": 22, "line-height": 1.3}),
        para(f"vtp{i}", it["text"]),
    ], {"flex-grow": 1, "flex-shrink": 1, "flex-basis": 300, "min-width": 0, "flex-direction": "column",
        "gap": 12, "border-width": (3, 0, 0, 0), "border-style": "solid", "border-color": C["navy"],
        "padding": (20, 0, 0, 0)}) for i, it in enumerate(d["items"])]
    grid = flex("vtgrid", items, {"flex-wrap": "wrap", "gap": 40, "column-gap": 32})
    return wrap("vorteile", [section_head("vth", d["eyebrow"], d["title"], d["intro"]), grid], bg=C["off_white"])


def s_sorgfalt():
    d = CONTENT["sorgfalt"]
    pills = [para(f"pill{i}", t, {"border-width": (1, 1, 1, 1), "border-style": "solid", "border-color": C["line"],
                                  "background-color": C["soft"], "border-radius": 999, "padding": (8, 16, 8, 16),
                                  "font-size": 12, "font-weight": "500"}) for i, t in enumerate(d["pills"])]
    left = flex("sgl", [
        eyebrow("sge", d["eyebrow"], C["teal"]),
        heading("sgh", d["title"], "h2", {"font-size": 34, "line-height": 1.2, "margin": (16, 0, 0, 0)},
                mobile={"font-size": 26}),
        para("sgp", d["text"], {"margin": (20, 0, 0, 0), "line-height": 1.75, "color": C["slate"]}),
        flex("sgpills", pills, {"margin": (32, 0, 0, 0), "flex-wrap": "wrap", "gap": 12}),
    ], {"flex-direction": "column", "flex-grow": 1, "flex-basis": 360, "min-width": 0, "max-width": 480})
    cards = []
    for i, it in enumerate(d["cards"]):
        hi = i in (1, 2)
        cards.append(flex(f"sgc{i}", [
            html(f"sgci{i}", svg(it["icon"], 26, "1.8", f"color:{C['teal']}")),
            heading(f"sgct{i}", it["title"], "h3", {"font-size": 21, "line-height": 1.3, "margin": (28, 0, 0, 0)}),
            para(f"sgcp{i}", it["text"], {"font-size": 15, "line-height": 1.7, "color": C["slate"],
                                          "margin": (8, 0, 0, 0)}),
        ], {"flex-grow": 1, "flex-basis": 240, "box-sizing": "border-box", "flex-direction": "column",
            "padding": (24, 24, 24, 24), "border-width": (2, 0, 0, 0), "border-style": "solid",
            "border-color": C["navy"] if hi else C["teal"], "bg": "#FFFFFF" if hi else C["soft"],
            **({"box-shadow": "soft"} if hi else {})}))
    right = flex("sgr", cards, {"flex-wrap": "wrap", "gap": 16, "flex-grow": 2, "flex-basis": 520, "min-width": 0})
    return wrap("sorgfalt", [flex("sgrow", [left, right], {"flex-wrap": "wrap", "gap": 48})], bg="#FEFEFE",
                pad=(96, 32, 96, 32), mpad=(56, 20, 56, 20))


def s_team():
    d = CONTENT["team"]
    head = flex("tmh", [
        flex("tmhl", [eyebrow("tme", d["eyebrow"]),
                      heading("tmt", d["title"], "h2", {"font-size": 34, "line-height": 1.2, "margin": (12, 0, 0, 0)},
                              mobile={"font-size": 26})],
             {"flex-direction": "column", "flex-grow": 1, "flex-basis": 400}),
        para("tmp", d["intro"], {"flex-grow": 1, "flex-basis": 320, "max-width": 450, "line-height": 1.75,
                                 "color": C["slate"]}),
    ], {"flex-wrap": "wrap", "gap": 20, "column-gap": 48, "align-items": "flex-start",
        "justify-content": "space-between"})
    cards = []
    for i, p in enumerate(d["people"]):
        cards.append(flex(f"tmc{i}", [
            image(f"tmi{i}", p["photo_alt"], {"flex-grow": 2, "flex-basis": 200, "min-height": 290,
                                              "bg": C["line"]}, mobile={"min-height": 220}),
            flex(f"tmb{i}", [
                para(f"tmr{i}", p["role"], {"font-size": 12, "font-weight": "500", "letter-spacing": (0.16, "em"),
                                            "text-transform": "uppercase", "color": C["teal"]}),
                heading(f"tmn{i}", p["name"], "h3", {"font-size": 26, "line-height": 1.25, "margin": (8, 0, 0, 0)}),
                para(f"tmq{i}", p["title"], {"font-size": 14, "color": C["muted"], "margin": (4, 0, 0, 0)}),
                para(f"tmw{i}", p["bio"], {"font-size": 14, "line-height": 1.7, "margin": (18, 0, 0, 0)}),
                para(f"tmz{i}", p["quote"], {"font-family": F["script"], "font-size": 24, "line-height": 1.3,
                                             "margin": (14, 0, 0, 0)}),
            ], {"flex-direction": "column", "flex-grow": 3, "flex-basis": 280, "min-width": 0,
                "padding": (28, 28, 28, 28), "box-sizing": "border-box"}),
        ], {"flex-wrap": "wrap", "flex-grow": 1, "flex-basis": 520, "min-width": 0, "bg": "#FFFFFF",
            "border-radius": 12, "overflow": "hidden", "box-shadow": "soft"}))
    return wrap("team", [head, flex("tmcards", cards, {"flex-wrap": "wrap", "gap": 24, "margin": (48, 0, 0, 0)})],
                bg=C["soft"], pad=(80, 32, 88, 32), anchor="team", gap=0)


FORM = """<form class="pma-form" method="post" action="#" style="display:flex;flex-direction:column;gap:20px;font-family:Roboto,system-ui,sans-serif;color:#00416B">
<style>.pma-form label{display:block;margin-bottom:8px;font-size:14px;font-weight:500}.pma-form .opt{font-weight:400;color:#587077}.pma-form input[type=text],.pma-form input[type=email],.pma-form input[type=tel],.pma-form select,.pma-form textarea{width:100%;box-sizing:border-box;min-height:48px;padding:0 16px;border:1px solid #B7CDCD;border-radius:12px;background:#FEFEFE;font-size:15px;color:#00416B}.pma-form textarea{padding:14px 16px}.pma-form button{width:100%;min-height:48px;border:0;border-radius:12px;background:linear-gradient(135deg,#57D3D3,#25A0A0);color:#00314F;font-size:15px;font-weight:500;cursor:pointer}</style>
<div><label for="pma-name">Ihr Name</label><input id="pma-name" name="name" type="text" required></div>
<div><label for="pma-mail">E-Mail-Adresse</label><input id="pma-mail" name="email" type="email" required></div>
<div><label for="pma-tel">Telefon <span class="opt">(optional)</span></label><input id="pma-tel" name="phone" type="tel"></div>
<div><label for="pma-modul">Interesse an Modul</label><select id="pma-modul" name="modul">__OPTIONS__</select></div>
<div><label for="pma-msg">Nachricht <span class="opt">(optional)</span></label><textarea id="pma-msg" name="message" rows="4"></textarea></div>
<div style="display:flex;gap:12px;align-items:flex-start"><input id="pma-dsgvo" name="consent" type="checkbox" required style="width:20px;height:20px;margin:2px 0 0"><label for="pma-dsgvo" style="font-size:14px;line-height:1.6;margin:0;font-weight:400">Ich stimme der Verarbeitung meiner Daten gemäß <a href="/datenschutz">Datenschutzerklärung</a> zu.</label></div>
<button type="submit">Vormerkung absenden</button>
<p class="pma-thanks" hidden>__THANKS__</p>
</form>"""


def s_kontakt():
    d = CONTENT["kontakt"]
    opts = "".join(f"<option>{o}</option>" for o in ["Bitte auswählen"] + d["options"])
    form_html = FORM.replace("__OPTIONS__", opts).replace("__THANKS__", d["thanks"])
    left = flex("ktl", [
        eyebrow("kte", d["eyebrow"], "#FFFFFF"),
        heading("ktt", d["title"], "h2", {"font-size": 34, "line-height": 1.2, "color": "#FFFFFF",
                                          "margin": (24, 0, 0, 0)}, mobile={"font-size": 26}),
        para("ktp", d["text"], {"margin": (24, 0, 0, 0), "line-height": 1.75, "color": "#FFFFFF"}),
        flex("ktn", [html("ktni", svg("badge-check", 20, "1.8", "color:#B7CDCD")),
                     para("ktnp", d["note"], {"font-size": 14, "line-height": 1.7, "color": "#FFFFFF"})],
             {"margin": (40, 0, 0, 0), "padding": (24, 0, 0, 0), "border-width": (1, 0, 0, 0),
              "border-style": "solid", "border-color": "rgba(255,255,255,0.85)", "gap": 12, "align-items": "flex-start"}),
    ], {"flex-direction": "column", "flex-grow": 5, "flex-basis": 340, "min-width": 0, "padding": (48, 48, 48, 48),
        "box-sizing": "border-box"}, mobile={"padding": (24, 24, 24, 24)})
    right = flex("ktr", [html("ktform", form_html)],
                 {"flex-direction": "column", "flex-grow": 7, "flex-basis": 440, "min-width": 0, "bg": "#FFFFFF",
                  "padding": (48, 48, 48, 48), "box-sizing": "border-box"}, mobile={"padding": (24, 24, 24, 24)})
    card = flex("ktcard", [left, right], {"flex-wrap": "wrap", "border-radius": 12, "overflow": "hidden",
                                           "bg": C["navy"], "box-shadow": "soft"})
    return wrap("kontakt", [card], pad=(96, 32, 96, 32), mpad=(56, 20, 56, 20), anchor="kontakt")


def s_footer():
    d = CONTENT["footer"]

    def col(seed, kids, grow=1, basis=240):
        return flex(seed, kids, {"flex-direction": "column", "flex-grow": grow, "flex-basis": basis})

    lab = lambda s, t: para(s, t, {"color": C["aqua"], "font-weight": "500", "font-size": 14})
    txt = lambda s, t: para(s, t, {"color": "#D6D6D6", "font-size": 14, "line-height": 1.7})
    soc = flex("fsoc", [html(f"fs{i}", f'<a href="{u}" aria-label="{n}" style="width:44px;height:44px;border:1px solid #6B6B6B;border-radius:50%;color:#D6D6D6;display:inline-flex;align-items:center;justify-content:center">{svg(n.lower(), 20, "2")}</a>')
                        for i, (n, u) in enumerate(d["social"])], {"gap": 8})
    cols = [
        col("fc1", [heading("fb", d["brand"], "div", {"font-size": 24, "line-height": 1.2, "color": "#FFFFFF"}),
                    para("fbs", d["brand_sub"], {"color": C["aqua"], "font-weight": "500", "margin": (4, 0, 0, 0),
                                                 "font-size": 14})]),
        col("fc2", [lab("fk", "Kontakt"), txt("fa", d["address"]), txt("ft", "Tel: " + d["phone"]),
                    txt("fm", "Mail: " + d["mail"])]),
        col("fc3", [lab("fsm", "Social Media"), soc], 1, 160),
        col("fc4", [button("fi", "Impressum", d["impressum"], {"color": C["aqua"], "font-weight": "500",
                                                              "background-color": "transparent", "padding": (0, 0, 0, 0)}),
                    button("fd", "Datenschutz", d["datenschutz"], {"color": C["aqua"], "font-weight": "500",
                                                                  "background-color": "transparent",
                                                                  "padding": (0, 0, 0, 0)})], 1, 140),
    ]
    return flex("footer", [flex("footi", cols, {"max-width": 1200, "width": (100, "%"),
                                                           "margin": (0, "auto", 0, "auto"), "flex-wrap": "wrap",
                                                           "gap": 40, "column-gap": 56, "padding": (48, 32, 48, 32),
                                                           "box-sizing": "border-box"},
                                mobile={"padding": (40, 20, 40, 20)})],
                {"flex-direction": "column", "width": (100, "%"), "bg": C["navy_dark"], "color": "#D6D6D6"})


SECTIONS = [
    ("01-header", "PMA – Header (sticky)", s_header),
    ("02-hero", "PMA – Hero", s_hero),
    ("03-intro", "PMA – Intro", s_intro),
    ("04-angebot", "PMA – Unser Angebot", s_angebot),
    ("05-ausbildungen", "PMA – Ausbildungen & Module", s_ausbildungen),
    ("06-vorteile", "PMA – Vorteile", s_vorteile),
    ("07-sorgfalt", "PMA – Sorgfalt vor großen Versprechen", s_sorgfalt),
    ("08-team", "PMA – Team", s_team),
    ("09-kontakt", "PMA – Kontakt & Vormerkung", s_kontakt),
    ("10-footer", "PMA – Footer", s_footer),
]


def export(title, content, kind):
    return {"content": content, "page_settings": [], "version": "0.4", "title": title, "type": kind}


def main():
    out = ROOT / "templates/elementor"
    out.mkdir(parents=True, exist_ok=True)
    allc = []
    for slug, title, fn in SECTIONS:
        node = fn()
        allc.append(node)
        (out / f"{slug}.json").write_text(json.dumps(export(title, [node], "container"), ensure_ascii=False, indent=2) + "\n", "utf-8")
    wrapper = flex("page", allc, {"flex-direction": "column", "width": (100, "%")}, anchor="oben")
    (out / "full-page.json").write_text(
        json.dumps(export("PERMA Mind Academy – Landingpage", [wrapper], "page"), ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"{len(SECTIONS)} Sektionen + full-page.json -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
