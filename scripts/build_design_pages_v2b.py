#!/usr/bin/env python3
"""Erzeugt die Design-Vorschau v2b (Kundenwünsche Dokument V5): Startseite, drei Angebotsseiten,
Impressum und Datenschutz. Präfix bw-, keine Inline-Styles, Stile in design/v2b/styles.css.

    python3 scripts/build_tokens.py v2b
    python3 scripts/build_design_pages_v2b.py

Texte: scripts/v2b_content.py. Impressum und Datenschutz werden aus design/v2 übernommen
(Texte liefert die Academy noch).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2b_content as C  # noqa: E402

OUT = ROOT / "design/v2b"
ICONS = json.loads((ROOT / "assets/icons/icons.json").read_text("utf-8"))
ICONS.update({
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "badge": '<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "user": '<path d="M18 20a6 6 0 0 0-12 0"/><circle cx="12" cy="10" r="4"/><circle cx="12" cy="12" r="10"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    # Stufen (Basic = Stufe 1, Advanced = Stufe 2 hervorgehoben): zeigt, dass die Ausbildungen aufeinander aufbauen
    "steps-1": '<rect x="2.5" y="15" width="5" height="6" rx="1" fill="currentColor"/><rect x="9.5" y="10" width="5" height="11" rx="1"/><rect x="16.5" y="4" width="5" height="17" rx="1"/>',
    "steps-2": '<rect x="2.5" y="15" width="5" height="6" rx="1"/><rect x="9.5" y="10" width="5" height="11" rx="1" fill="currentColor"/><rect x="16.5" y="4" width="5" height="17" rx="1"/>',
    # Zwei Personen im Gespräch (Clinical Expert: Therapie und Behandlung)
    "conversation": '<circle cx="6" cy="11" r="2.5"/><path d="M2 21v-1a4 4 0 0 1 8 0v1"/><circle cx="18" cy="11" r="2.5"/><path d="M14 21v-1a4 4 0 0 1 8 0v1"/><path d="M10 2.5h4a1.5 1.5 0 0 1 1.5 1.5v2a1.5 1.5 0 0 1-1.5 1.5h-1.25L12 9l-.75-1.5H10A1.5 1.5 0 0 1 8.5 6V4A1.5 1.5 0 0 1 10 2.5z"/>',
})
# Reagenzglas nicht verwenden (Wunsch der Academy, 25.11.2026): überall das Buch
ICONS.pop("flask", None)
OFFER_ICON = {"basic": "steps-1", "advanced": "steps-2", "clinical": "conversation"}
OFFER_CHIP = {"basic": "Einstieg", "advanced": "Vertiefung", "clinical": "Klinische Fortbildung"}

CONTACT = {"address": "Plüddemanngasse 104, 8042 Graz, Österreich", "phone": "+43 676 511 2763",
           "mail": "info@perma-academy.at"}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500&amp;'
         'family=Roboto:ital,wght@0,300;0,400;0,500;1,300&amp;display=swap" rel="stylesheet">')


def ph(text):
    """[Platzhalter] gelb markieren."""
    return re.sub(r"\[([^\]]+)\]", r'<span class="bw-placeholder">[\1]</span>', text)


def icon(name, px=20, sw="1.8", cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="{px}" height="{px}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def offer_file(key):
    return C.META[key]["file"]


def privacy(link_cls=""):
    return C.PRIVACY_NOTE.format(link='<a href="datenschutz.html">Datenschutzerklärung</a>')


# ------------------------------------------------------------------ Header, Footer, Seite
def header(page):
    on_index = page == "index"
    home = "" if on_index else "index.html"
    ac = ' aria-current="page"'
    sub = "".join(
        f'<a class="bw-nav-menu__link" href="{offer_file(o["key"])}"{ac if page == o["key"] else ""}>{o["name"]}</a>'
        for o in C.OFFERS)
    msub = "".join(f'<a class="bw-mnav__link bw-mnav__link--sub" href="{offer_file(o["key"])}">{o["name"]}</a>' for o in C.OFFERS)
    current = ' aria-current="page"' if page in ("basic", "advanced", "clinical") else ""
    items = [("Über uns", "ueber-uns"), ("Zertifizierung", "zertifizierung"), ("Fragen", "fragen"), ("Kontakt", "kontakt")]
    links = "".join(f'<a class="bw-header__link" href="{home}#{a}">{t}</a>' for t, a in items)
    mlinks = "".join(f'<a class="bw-mnav__link" href="{home}#{a}">{t}</a>' for t, a in items)
    cta = "#interessentenliste" if page in ("index", "basic", "advanced", "clinical") else "index.html#interessentenliste"
    acc = next((o["accent"] for o in C.OFFERS if o["key"] == page), None)  # Angebotsseite: Header im Kartenverlauf
    hcls = f"bw-header bw-header--accent bw-accent--{acc}" if acc else "bw-header"
    logo = "assets/logo-white.svg" if acc else "assets/logo.svg"
    btn = "bw-button--light" if acc else "bw-button--primary"
    return f"""<header class="{hcls}">
<div class="bw-header__bar">
<a class="bw-header__logo" href="{home or '#oben'}" aria-label="PERMA Mind Academy – zur Startseite"><img class="bw-header__logo-img" src="{logo}" alt="PERMA Mind Academy – We create wellbeing"></a>
<nav class="bw-header__nav" aria-label="Hauptnavigation">
<div class="bw-nav-menu"><a class="bw-header__link" href="{home}#ausbildungen"{current}>Ausbildungen {icon("chevron", 16, "2", "bw-nav-menu__chevron")}</a>
<div class="bw-nav-menu__panel">{sub}</div></div>
{links}
</nav>
<a class="bw-button {btn} bw-header__cta" href="{cta}">Zur Interessentenliste</a>
<details class="bw-mnav"><summary class="bw-mnav__toggle" aria-label="Menü öffnen">{icon("menu", 22, "2")}</summary>
<div class="bw-mnav__panel"><a class="bw-mnav__link" href="{home}#ausbildungen">Ausbildungen</a>{msub}{mlinks}<a class="bw-button bw-button--primary bw-mnav__cta" href="{cta}">Zur Interessentenliste</a></div></details>
</div>
</header>"""


def footer(page):
    home = "" if page == "index" else "index.html"
    return f"""<footer class="bw-footer">
<div class="bw-container bw-footer__inner">
<div class="bw-footer__col"><img class="bw-footer__logo" src="assets/logo-white.svg" alt="PERMA Mind Academy – We create wellbeing"></div>
<div class="bw-footer__col"><div class="bw-footer__title">Kontakt</div><div>{CONTACT["address"]}</div><div>Tel: {CONTACT["phone"]}</div><div>Mail: {CONTACT["mail"]}</div></div>
<div class="bw-footer__col bw-footer__col--social"><div class="bw-footer__title">Social Media</div>
<div class="bw-footer__social">
<a class="bw-footer__social-link" href="#" aria-label="Instagram">{icon("instagram", 20, "2")}</a><a class="bw-footer__social-link" href="#" aria-label="LinkedIn">{icon("linkedin", 20, "2")}</a></div></div>
<div class="bw-footer__col bw-footer__col--legal"><a class="bw-footer__link" href="{home}#kontakt">Kontakt</a><a class="bw-footer__link" href="{home}#newsletter">Newsletter</a><a class="bw-footer__link" href="impressum.html">Impressum</a><a class="bw-footer__link" href="datenschutz.html">Datenschutz</a></div>
</div>
</footer>"""


def page(fname, key, title, desc, body):
    html = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{FONTS}
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="bw-page">
{header(key)}
<main id="oben">
{body}
</main>
{footer(key)}
</div>
<script src="preview.js"></script>
</body>
</html>
"""
    (OUT / fname).write_text(html, "utf-8")


# ------------------------------------------------------------------ Bausteine
def section_head(title, eyebrow=None, lead=None, center=False, level="h2", hid=None):
    cls = "bw-section-head bw-section-head--center" if center else "bw-section-head"
    e = f'<p class="bw-eyebrow">{eyebrow}</p>' if eyebrow else ""
    i = f' id="{hid}"' if hid else ""
    l = f'<p class="bw-section-head__lead">{lead}</p>' if lead else ""
    return f'<div class="{cls}">{e}<{level} class="bw-heading-section"{i}>{title}</{level}>{l}</div>'


def accordion(title, body_html, level="h3", open_=False):
    o = " open" if open_ else ""
    return (f'<details class="bw-accordion"{o}><summary class="bw-accordion__summary">'
            f'<{level} class="bw-accordion__title">{title}</{level}><span class="bw-accordion__icon" aria-hidden="true"></span></summary>'
            f'<div class="bw-accordion__body">{body_html}</div></details>')


def paras(lst, cls="bw-text"):
    return "".join(f'<p class="{cls}">{ph(p)}</p>' for p in lst)


def field(fid, label, typ="text", required=True, auto="", textarea=False, form="f"):
    opt = "" if required else ' <span class="bw-form__optional">(optional)</span>'
    req = " required" if required else ""
    a = f' autocomplete="{auto}"' if auto else ""
    if textarea:
        ctrl = f'<textarea class="bw-form__input bw-form__input--textarea" id="{form}-{fid}" name="{fid}" rows="4"{req}></textarea>'
    else:
        ctrl = f'<input class="bw-form__input" id="{form}-{fid}" name="{fid}" type="{typ}"{a}{req}>'
    return f'<div class="bw-form__field"><label class="bw-form__label" for="{form}-{fid}">{label}{opt}</label>{ctrl}</div>'


def interest_form(pre=None):
    L = C.LIST
    opts = "".join(
        f'<label class="bw-form__option"><input class="bw-form__checkbox" type="checkbox" name="interesse" value="{o["key"]}"{" checked" if pre == o["key"] else ""}><span>{o["form_label"]}</span></label>'
        for o in C.OFFERS)
    return f"""<form class="bw-form" action="#" method="post" novalidate data-preview-form>
<div class="bw-form__row">{field("vorname", "Vorname", auto="given-name", form="il")}{field("nachname", "Nachname", auto="family-name", form="il")}</div>
{field("email", "E-Mail-Adresse", "email", auto="email", form="il")}
<fieldset class="bw-form__group" data-require-one><legend class="bw-form__label">{L["interest_legend"]}</legend>{opts}</fieldset>
{field("beruf", "Beruf oder bisherige Ausbildung", required=False, form="il")}
{field("nachricht", "Deine Nachricht an uns", required=False, textarea=True, form="il")}
<p class="bw-form__hint">{L["hint"]} {privacy()}</p>
<div class="bw-form__check"><input class="bw-form__checkbox" id="il-newsletter" name="newsletter" type="checkbox"><label class="bw-form__check-label" for="il-newsletter">{L["newsletter"]}</label></div>
<button class="bw-button bw-button--accent bw-button--block" type="submit">{L["button"]}</button>
<p class="bw-form__thanks" role="status" hidden>{L["done"]}</p>
</form>"""


def interest_section(title, texts, pre=None, eyebrow="Unverbindliche Interessentenliste", accent=None):
    side = "".join(f'<p class="bw-form-card__text">{t}</p>' for t in texts)
    return f"""<section class="bw-block" id="interessentenliste"><div class="bw-container">
<div class="bw-form-card{f" bw-form-card--accent bw-accent--{accent}" if accent else ""}">
<div class="bw-form-card__side">
<p class="bw-eyebrow bw-eyebrow--on-dark">{eyebrow}</p>
<h2 class="bw-form-card__title">{title}</h2>
{side}
<div class="bw-form-card__note">{icon("badge-check", cls="bw-form-card__note-icon")}<p class="bw-form-card__note-text">{C.LIST["intro2"]}</p></div>
</div>
{interest_form(pre)}
</div>
</div></section>"""


def offer_card(o):
    facts = "".join(f'<li class="bw-offer-card__fact">{f.strip()}</li>' for f in o["card_meta"].split("·"))
    return f"""<article class="bw-offer-card bw-accent--{o["accent"]}">
<div class="bw-offer-card__head"><div class="bw-chip">{OFFER_CHIP[o["key"]]}</div><span class="bw-offer-card__icon">{icon(OFFER_ICON[o["key"]], 30, "1.6")}</span></div>
<h3 class="bw-offer-card__title">{o["name"]}</h3>
<p class="bw-offer-card__text">{o["card_text"]}</p>
<ul class="bw-offer-card__facts">{facts}</ul>
<a class="bw-link bw-link--on-dark bw-link--strong bw-offer-card__link" href="{offer_file(o["key"])}">{o["card_button"]} →</a>
</article>"""


# ------------------------------------------------------------------ Startseite
def index():
    H = C.HERO
    feats = "".join(
        f'<li class="bw-highlight bw-accent--{a}"><span class="bw-highlight__icon">{icon(i, 22)}</span><span>{t}</span></li>'
        for (a, i), t in zip([("blue", "globe"), ("purple", "book"), ("green", "badge")], H["features"]))
    why = "".join(
        f'<article class="bw-feature bw-feature--raised bw-accent--{a}"><span class="bw-feature__icon">{icon(i, 26)}</span>'
        f'<h3 class="bw-feature__title">{t}</h3><p class="bw-feature__text">{x}</p></article>'
        for a, i, t, x in C.WHY["items"])
    cards = "".join(offer_card(o) for o in C.OFFERS)
    perma = [("P", "blue", "Positive Emotionen"), ("E", "purple", "Engagement"), ("R", "orange", "Beziehungen"),
             ("M", "green", "Sinn"), ("A", "red", "Persönlich bedeutsame Ziele erreichen")]
    perma_html = "".join(f'<li class="bw-perma__item bw-accent--{a}"><span class="bw-perma__letter">{l}</span><span class="bw-perma__label">{t}</span></li>' for l, a, t in perma)
    steps = ["Ziele klären", "Methoden auswählen", "Erfahrungen reflektieren", "Die Anwendung anpassen"]
    steps_html = "".join(f'<li class="bw-steps__item"><div class="bw-steps__number">0{n}</div><h3 class="bw-steps__title">{s}</h3></li>' for n, s in enumerate(steps, 1))
    A = C.ABOUT
    about_acc = "".join(accordion(t, paras(p)) for t, p in A["accordions"])
    trainers = ""
    for t in A["trainers"]:
        body = paras(t["profile"])
        if t["quote"]:
            body += f'<blockquote class="bw-quote"><p class="bw-quote__text">{t["quote"][0]}</p><footer class="bw-quote__source">{t["quote"][1]}</footer></blockquote>'
        body += paras(t["after"])
        trainers += f"""<article class="bw-person">
<div class="bw-person__photo" role="img" aria-label="{t["alt"]}"><span class="bw-person__role">{t["role"]}</span>{icon("user", 72, "1.2")}<span class="bw-person__photo-label">{t["photo"]}</span></div>
<h3 class="bw-person__name">{t["name"]}</h3>
<p class="bw-person__bio">{t["teaser"]}</p>
{accordion("Profil lesen", body, level="h4")}
</article>"""
    Z = C.CERT
    cert_acc = "".join(accordion(t, paras(p)) for t, p in Z["accordions"])
    faq = "".join(accordion(q, f'<p class="bw-text">{a}</p>') for q, a in C.FAQ["items"])
    N, K = C.NEWSLETTER, C.CONTACT
    body = f"""
<!-- 1 HERO -->
<section class="bw-hero bw-hero--v2b">
<div class="bw-hero__caption">[Hero-Bild / Illustration: Menschen in ruhiger, positiver Atmosphäre]</div>
<div class="bw-hero__box bw-hero__box--wide">
<h1 class="bw-hero__title">{H["h1"]}</h1>
<p class="bw-hero__text">{H["paras"][0]}</p>
<div class="bw-hero__actions">
<a class="bw-button bw-button--primary" href="#interessentenliste">{H["button_secondary"]}</a>
<a class="bw-button bw-button--secondary" href="#ausbildungen">{H["button_primary"]}</a>
</div>
</div>
</section>

<!-- Profilmerkmale -->
<section class="bw-highlights" aria-label="Profilmerkmale"><div class="bw-container"><ul class="bw-highlights__list">{feats}</ul></div></section>

<!-- Intro -->
<section class="bw-intro"><p class="bw-intro__lead">{H["paras"][1]}</p></section>

<!-- Warum -->
<section class="bw-block bw-block--neutral"><div class="bw-container">
{section_head(C.WHY["title"], center=True)}
<div class="bw-grid bw-grid--3">{why}</div>
</div></section>

<!-- Ausbildungen -->
<section class="bw-block bw-block--tint" id="ausbildungen"><div class="bw-container">
{section_head(C.COURSES["title"], C.COURSES["eyebrow"], center=True)}
<div class="bw-offer-grid">{cards}</div>
</div></section>

<!-- Verstehen und Anwenden -->
<section class="bw-block"><div class="bw-container">
<div class="bw-split">
<div class="bw-split__main">{section_head(C.UNDERSTAND["left_title"])}{paras(C.UNDERSTAND["left"])}</div>
<div class="bw-split__aside"><p class="bw-eyebrow">Das PERMA-Modell</p><ul class="bw-perma">{perma_html}</ul></div>
</div>
<div class="bw-apply">
{section_head(C.UNDERSTAND["right_title"])}{paras(C.UNDERSTAND["right"])}
<ol class="bw-steps bw-steps--compact">{steps_html}</ol>
</div>
</div></section>

<!-- Über uns -->
<section class="bw-block bw-block--neutral" id="ueber-uns"><div class="bw-container">
{section_head(A["title"], A["eyebrow"], A["intro"])}
<div class="bw-accordion-list bw-accordion-list--limit">{about_acc}</div>
<div class="bw-team__list">{trainers}</div>
</div></section>

<!-- Zertifizierung -->
<section class="bw-block" id="zertifizierung"><div class="bw-container">
<div class="bw-split">
<div class="bw-split__main">{section_head(Z["title"], Z["eyebrow"])}{paras(Z["paras"])}
<a class="bw-button bw-button--secondary bw-cert__button" href="#ausbildungen">{Z["button"]}</a></div>
<div class="bw-split__aside"><div class="bw-cert__logo">{ph(Z["logo_placeholder"])}</div><div class="bw-accordion-list">{cert_acc}</div></div>
</div>
</div></section>

<!-- Interessentenliste -->
{interest_section(C.NEXT_STEP["title"], [C.NEXT_STEP["text"]])}

<!-- Fragen -->
<section class="bw-block bw-block--neutral" id="fragen"><div class="bw-container">
{section_head(C.FAQ["title"], C.FAQ["eyebrow"], center=True)}
<div class="bw-accordion-list bw-accordion-list--center">{faq}</div>
</div></section>

<!-- Newsletter -->
<section class="bw-block bw-block--tint" id="newsletter"><div class="bw-container">
<div class="bw-columns">
<div class="bw-columns__item">{section_head(N["title"], N["eyebrow"], N["text"])}</div>
<form class="bw-form bw-form--card bw-columns__item" action="#" method="post" novalidate data-preview-form>
{field("email", "E-Mail-Adresse", "email", auto="email", form="nl")}
{field("vorname", "Vorname", required=False, auto="given-name", form="nl")}
<div class="bw-form__check"><input class="bw-form__checkbox" id="nl-consent" name="consent" type="checkbox" required><label class="bw-form__check-label" for="nl-consent">{N["consent"].replace("Datenschutzerklärung", '<a href="datenschutz.html">Datenschutzerklärung</a>')}</label></div>
<button class="bw-button bw-button--accent bw-button--block" type="submit">{N["button"]}</button>
<p class="bw-form__thanks" role="status" hidden>{N["done"]}</p>
</form>
</div>
</div></section>

<!-- Kontakt -->
<section class="bw-block" id="kontakt"><div class="bw-container">
<div class="bw-columns">
<div class="bw-columns__item">{section_head(K["title"], lead=K["text"])}
<ul class="bw-contact-list">
<li class="bw-contact-list__item">{icon("mail", cls="bw-contact-list__icon")}<span>{CONTACT["mail"]}</span></li>
<li class="bw-contact-list__item">{icon("phone", cls="bw-contact-list__icon")}<span>{CONTACT["phone"]}</span></li>
<li class="bw-contact-list__item">{icon("pin", cls="bw-contact-list__icon")}<span>{CONTACT["address"]}</span></li>
</ul></div>
<form class="bw-form bw-form--card bw-columns__item" action="#" method="post" novalidate data-preview-form>
{field("name", "Name", auto="name", form="kf")}
{field("email", "E-Mail-Adresse", "email", auto="email", form="kf")}
{field("nachricht", "Nachricht", textarea=True, form="kf")}
<p class="bw-form__hint">{privacy()}</p>
<button class="bw-button bw-button--accent bw-button--block" type="submit">{K["button"]}</button>
<p class="bw-form__thanks" role="status" hidden>{K["done"]}</p>
</form>
</div>
</div></section>

<a class="bw-fab" href="#interessentenliste">{icon("send", 22)}Zur Interessentenliste</a>
"""
    m = C.META["index"]
    page(m["file"], "index", m["title"], m["desc"], body)


# ------------------------------------------------------------------ Angebotsseiten
def offer_page(key):
    P = C.PAGES[key]
    o = next(x for x in C.OFFERS if x["key"] == key)
    facts = ""
    for f in P["facts"]:
        note = f'<span class="bw-facts__note">{f[2]}</span>' if len(f) > 2 else ""
        val = "".join(f'<span class="bw-facts__price">{x.strip()}</span>' for x in f[1].split(" / ")) if f[0] == "Kosten" else f[1]
        facts += f'<div class="bw-facts__row"><dt class="bw-facts__term">{f[0]}</dt><dd class="bw-facts__value">{val}{note}</dd></div>'
    lead = P["lead"]
    lead_html = f'<p class="bw-page-hero__lead">{lead[0]}</p>' + "".join(f'<p class="bw-page-hero__text">{p}</p>' for p in lead[1:])
    if key == "advanced":  # Voraussetzung verlinkt zur Basic-Ausbildung
        lead_html = lead_html.replace("abgeschlossene Basic-Ausbildung", f'abgeschlossene <a href="{offer_file("basic")}">Basic-Ausbildung</a>')
    mods = "".join(accordion(m[0], f'<p class="bw-text">{m[1]}</p>') for m in P["modules"])
    scope = paras(P["scope"])
    if P.get("scope_more"):
        scope += f'<h4 class="bw-card__subtitle">{P["scope_more"][0]}</h4>' + paras(P["scope_more"][1])
    if P.get("scope_link"):
        k, label = P["scope_link"]
        scope += f'<p class="bw-text"><a class="bw-link bw-link--strong" href="{offer_file(k)}">{label} →</a></p>'
    extra = "".join(f'<div class="bw-card"><h3 class="bw-card__title">{t}</h3>{paras(x)}</div>' for t, x in P.get("extras", []))
    body = f"""
<section class="bw-page-hero bw-page-hero--offer bw-accent--{o["accent"]}"><div class="bw-container bw-page-hero__inner">
<p class="bw-crumbs"><a href="index.html">Startseite</a> / <a href="index.html#ausbildungen">Ausbildungen</a> / {o["name"]}</p>
<p class="bw-chip bw-page-hero__chip">{P["eyebrow"]}</p>
<h1 class="bw-page-hero__title">{P["h1"]}</h1>
{lead_html}
<div class="bw-page-hero__actions">
<a class="bw-button bw-button--light" href="#interessentenliste">{o["list_button"]}</a>
<a class="bw-button bw-button--secondary bw-button--on-dark" href="index.html#ausbildungen">Alle Ausbildungen vergleichen</a>
</div>
</div></section>

<section class="bw-block"><div class="bw-container">
<div class="bw-split">
<div class="bw-split__main">
{section_head(P["content_title"])}
<div class="bw-accordion-list">{mods}</div>
<div class="bw-card bw-card--plain"><h3 class="bw-card__title">{P["scope_title"]}</h3>{scope}</div>
{extra}
</div>
<aside class="bw-split__aside">
<div class="bw-facts-card bw-accent--{o["accent"]}">
<h2 class="bw-facts-card__title">Das Angebot auf einen Blick</h2>
<dl class="bw-facts">{facts}</dl>
<a class="bw-button bw-button--primary bw-button--block" href="#interessentenliste">{o["list_button"]}</a>
</div>
<nav class="bw-related" aria-label="Weiterführend">
<a class="bw-related__link" href="index.html#ausbildungen">Zur Ausbildungsauswahl →</a>
<a class="bw-related__link" href="index.html#ueber-uns">Trainer kennenlernen →</a>
<a class="bw-related__link" href="index.html#zertifizierung">ECQA-Zertifizierung →</a>
<a class="bw-related__link" href="index.html#fragen">Häufige Fragen →</a>
</nav>
</aside>
</div>
</div></section>

{interest_section(P["list_title"], [P["list_text"]], pre=key, accent=o["accent"])}

<a class="bw-fab" href="#interessentenliste">{icon("send", 22)}Zur Interessentenliste</a>
"""
    m = C.META[key]
    page(m["file"], key, m["title"], m["desc"], body)


# ------------------------------------------------------------------ Impressum, Datenschutz (aus v2)
def legal(fname, title, desc):
    src = (ROOT / "design/v2" / fname).read_text("utf-8")
    main = re.search(r"<main>(.*?)</main>", src, re.S).group(1)
    main = main.replace('href="Main.dc.html"', 'href="index.html"')
    page(fname, fname.replace(".html", ""), f"{title} | PERMA Mind Academy", desc, main)


if __name__ == "__main__":
    index()
    for k in ("basic", "advanced", "clinical"):
        offer_page(k)
    legal("impressum.html", "Impressum", "Impressum der PERMA Mind Academy.")
    legal("datenschutz.html", "Datenschutz", "Datenschutzerklärung der PERMA Mind Academy.")
    print("index, 3 Angebotsseiten, impressum, datenschutz ->", OUT.relative_to(ROOT))
