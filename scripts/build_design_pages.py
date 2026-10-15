#!/usr/bin/env python3
"""Erzeugt die statischen Unterseiten der Design-Vorschau.

    python3 scripts/build_design_pages.py       # Version 1 -> design/reference/
    python3 scripts/build_design_pages.py v2    # Corporate Design v2 -> design/v2/

Ausgabe: {kontakt,impressum,datenschutz}.html
Header/Footer entsprechen Main.dc.html; Stile in design/reference/site.css.
Platzhalter stehen in [eckigen Klammern] und werden gelb hinterlegt.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V2 = len(sys.argv) > 1 and sys.argv[1] == "v2"
OUT = ROOT / ("design/v2" if V2 else "design/reference")
ICONS = json.loads((ROOT / "assets/icons/icons.json").read_text("utf-8"))
CONTENT = json.loads((ROOT / "content/content.json").read_text("utf-8"))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500&amp;'
         'family=Roboto:ital,wght@0,300;0,400;0,500;1,300&amp;family=Great+Vibes&amp;display=swap" rel="stylesheet">')
if V2:
    FONTS = FONTS.replace("&amp;family=Great+Vibes", "")


ICONS.update({
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
})


def ph(text):
    """[Platzhalter] gelb markieren."""
    return re.sub(r"\[([^\]]+)\]", r'<span class="ph">[\1]</span>', text)


def icon(name, px=20, sw="1.8"):
    return (f'<svg width="{px}" height="{px}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


NAV = [("Über uns", "Main.dc.html#ueber-uns"), ("Angebot", "Main.dc.html#angebot"),
       ("Ausbildungen", "Main.dc.html#ausbildungen"), ("Team", "Main.dc.html#team"),
       ("Kontakt", "kontakt.html")]


def header(current):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == current else ""}>{t}</a>' for t, h in NAV)
    mlinks = "".join(f'<a href="{h}">{t}</a>' for t, h in NAV)
    return f"""<header class="site-header"><div class="wrap">
<a class="logo" href="Main.dc.html" aria-label="PERMA Mind Academy – zur Startseite"><img src="assets/logo.svg" alt="PERMA Mind Academy – We create wellbeing"></a>
<nav aria-label="Hauptnavigation">{links}</nav>
<a class="btn-pill" href="kontakt.html">Unverbindlich anfragen</a>
<details class="mnav"><summary aria-label="Menü öffnen">{icon("menu", 22, "2")}</summary>
<div class="mnav-panel">{mlinks}<a class="cta" href="kontakt.html">Unverbindlich anfragen</a></div></details>
</div></header>"""


def footer():
    f = CONTENT["footer"]
    brand = ('<img src="assets/logo-white.svg" alt="PERMA Mind Academy – We create wellbeing" style="display:block;height:56px;width:auto;align-self:flex-start">'
             if V2 else f'<div class="brand">{f["brand"]}</div><div class="sub">{f["brand_sub"]}</div>')
    return f"""<footer class="site-footer"><div class="wrap">
<div class="col">{brand}</div>
<div class="col"><h4>Kontakt</h4><div>{ph(f["address"])}</div><div>Tel: {ph(f["phone"])}</div><div>Mail: {ph(f["mail"])}</div></div>
<div class="col s"><h4>Social Media</h4><div class="social">
<a href="#" aria-label="Instagram">{icon("instagram", 20, "2")}</a><a href="#" aria-label="LinkedIn">{icon("linkedin", 20, "2")}</a></div></div>
<div class="col l"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></div>
</div></footer>"""


# Corporate Design v2: Kontaktdaten laut Visitenkarte (Mag. Michael Wohlkönig, Founder)
V2_FACTS = [
    ('<span class="ph">[Straße Nr., PLZ Ort]</span>', 'Plüddemanngasse 104, 8042 Graz'),
    ('<span class="ph">[Straße Nr.]</span>', 'Plüddemanngasse 104'),
    ('<span class="ph">[PLZ Ort]</span>', '8042 Graz'),
    ('<span class="ph">[Telefon]</span>', '+43 676 511 2763'),
    ('<span class="ph">[E-Mail]</span>', 'michael@perma-academy.at'),
    ('<span class="ph">[Domain]</span>', 'www.perma-academy.at'),
    ('<span class="ph">[Name]</span>', 'Mag. Michael Wohlkönig'),
    ('<span class="ph">[Funktion, z. B. Leitung Organisation]</span>', 'Founder'),
]


def page(fname, title, current, body, desc):
    html = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} – PERMA Mind Academy</title>
<meta name="description" content="{desc}">
{FONTS}
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="site.css">
</head>
<body>
{header(current)}
<main>
{body}
</main>
{footer()}
</body>
</html>
"""
    if V2:
        for old, new in V2_FACTS:
            html = html.replace(old, new)
        html = html.replace("Roboto, Montserrat, Great Vibes", "Roboto, Montserrat")
    (OUT / fname).write_text(html, "utf-8")


# ----------------------------------------------------------------- Kontakt
def kontakt():
    k = CONTENT["kontakt"]
    opts = "".join(f"<option>{o}</option>" for o in ["Bitte auswählen"] + k["options"])
    body = f"""
<section class="page-hero"><div class="wrap">
<p class="crumbs"><a href="Main.dc.html">Startseite</a> / Kontakt</p>
<p class="eyebrow">Kontakt &amp; Vormerkung</p>
<h1>Sie haben Fragen?</h1>
<p class="lead">Ob Sie eine Ausbildung in Erwägung ziehen, sich bereits einen Platz sichern möchten oder einfach mehr über Inhalte, Termine und Voraussetzungen wissen wollen: Wir freuen uns über Ihre Nachricht und melden uns persönlich bei Ihnen. {ph("[Antwortzeit ergänzen, z. B. innerhalb von zwei Werktagen]")}</p>
</div></section>

<section class="block"><div class="wrap">
<div class="cols">
<div>
<h2 class="title">So erreichen Sie uns</h2>
<p style="margin:16px 0 0;font-size:var(--pma-fs-base);line-height:var(--pma-lh-body);max-width:520px">Die Anmeldung zu einer Ausbildung ist in wenigen Schritten erledigt. Wenn Sie unsicher sind, welches Modul zu Ihrem beruflichen Kontext passt, oder wenn Sie Unterstützung bei der Anmeldung brauchen, sprechen wir gern persönlich mit Ihnen, {ph("[per E-Mail, Telefon oder Messenger – Kanäle bestätigen]")}.</p>
<ul class="contact-list">
<li>{icon("mail")}<span>{ph("[E-Mail]")}<small>Für allgemeine Anfragen</small></span></li>
<li>{icon("phone")}<span>{ph("[Telefon]")}<small>{ph("[Erreichbarkeit, z. B. Mo–Fr 9–16 Uhr]")}</small></span></li>
<li>{icon("pin")}<span>{ph("[Straße Nr., PLZ Ort]")}<small>{ph("[Standort / Seminarort ergänzen]")}</small></span></li>
</ul>
</div>
<div class="card" style="align-self:flex-start">
<p class="label">Ansprechperson</p>
<h3>{ph("[Name]")}</h3>
<p>{ph("[Funktion, z. B. Leitung Organisation]")}<br>{ph("[Telefon]")} · {ph("[E-Mail]")}</p>
<p>Persönliche Fragen zu Inhalten, Terminen und Voraussetzungen beantworten wir Ihnen gern im direkten Gespräch.</p>
</div>
</div>

<div class="info-box" style="margin-top:48px;max-width:780px">
<h3>Gut zu wissen</h3>
<p>Ihre Vormerkung ist unverbindlich und verpflichtet Sie zu nichts. Sie erhalten von uns keinen Newsletter ohne Ihre ausdrückliche Einwilligung. Informationen zu Anerkennung, Dauer und Terminen der Module ergänzen wir vor dem Programmstart transparent. {ph("[Prüfen und bestätigen]")}</p>
</div>
</div></section>

<section class="block alt"><div class="wrap">
<h2 class="title">In drei Schritten zur Vormerkung</h2>
<ol class="steps">
<li><div class="n">01</div><h3>Formular ausfüllen</h3><p>Teilen Sie uns mit, an welchem Modul Sie interessiert sind. Wenn Sie noch unsicher sind, wählen Sie „Noch unsicher, bitte beraten Sie mich“.</p></li>
<li><div class="n">02</div><h3>Persönliche Rückmeldung</h3><p>Wir melden uns bei Ihnen und beantworten Ihre Fragen zu Inhalten, Terminen und Voraussetzungen.</p></li>
<li><div class="n">03</div><h3>Entscheiden Sie in Ruhe</h3><p>Erst wenn alles geklärt ist, entscheiden Sie, ob und wann Sie starten. Die Vormerkung bleibt bis dahin unverbindlich.</p></li>
</ol>
</div></section>

<section class="block" id="formular"><div class="wrap">
<div class="form-card">
<div class="form-side">
<p class="eyebrow">Kontakt &amp; Vormerkung</p>
<h2>Jetzt unverbindlich<br>vormerken</h2>
<p>{k["text"]}</p>
<div class="note">{icon("badge-check")}<p>{k["note"]}</p></div>
</div>
<form class="pma-form" id="pma-form" action="#" method="post" novalidate>
<div><label for="name">Ihr Name</label><input id="name" name="name" type="text" placeholder="Ihr Name" autocomplete="name" required></div>
<div><label for="mail">E-Mail-Adresse</label><input id="mail" name="email" type="email" placeholder="name@beispiel.at" autocomplete="email" required></div>
<div><label for="tel">Telefon <span class="opt">(optional)</span></label><input id="tel" name="phone" type="tel" placeholder="+43" autocomplete="tel"></div>
<div><label for="modul">Interesse an Modul</label><select id="modul" name="modul">{opts}</select></div>
<div><label for="msg">Nachricht <span class="opt">(optional)</span></label><textarea id="msg" name="message" rows="4" placeholder="z. B. beruflicher Kontext oder eine Frage"></textarea></div>
<div class="check"><input id="dsgvo" name="consent" type="checkbox" required><label for="dsgvo">Ich stimme der Verarbeitung meiner Daten gemäß <a href="datenschutz.html">Datenschutzerklärung</a> zu.</label></div>
<button type="submit">Vormerkung absenden {icon("send", 16, "2")}</button>
<p class="thanks" id="pma-thanks" role="status" hidden>{k["thanks"]}</p>
</form>
</div>
</div></section>
<script>
/* Nur Vorschau: zeigt die Bestätigung an, sendet nichts. */
document.getElementById('pma-form').addEventListener('submit',function(e){{
  e.preventDefault();
  if(!this.checkValidity()){{this.reportValidity();return;}}
  document.getElementById('pma-thanks').hidden=false;
  this.querySelector('button').disabled=true;
}});
</script>
"""
    page("kontakt.html", "Kontakt & Vormerkung", "kontakt.html", body,
         "Kontakt und unverbindliche Vormerkung zu den Ausbildungen der PERMA Mind Academy.")


# --------------------------------------------------------------- Impressum
def impressum():
    body = f"""
<section class="page-hero"><div class="wrap">
<p class="crumbs"><a href="Main.dc.html">Startseite</a> / Impressum</p>
<p class="eyebrow">Rechtliches</p><h1>Impressum</h1></div></section>
<div class="wrap"><article class="prose">
<p class="draft"><strong>Entwurf.</strong> Struktur und Wortlaut orientieren sich an gängigen Impressen von Bildungsanbietern. Alle gelb markierten Angaben sind zu ergänzen. Vor Veröffentlichung bitte rechtlich prüfen lassen; welche Pflichtangaben gelten, hängt von Rechtsform und Sitz ab (hier angenommen: Österreich).</p>

<h2>Angaben gemäß § 5 E-Commerce-Gesetz (ECG) und § 14 UGB</h2>
<address>{ph("[Firmenname inkl. Rechtsform]")}<br>{ph("[Straße Nr.]")}<br>{ph("[PLZ Ort]")}<br>Österreich</address>

<h2>Kontakt</h2>
<p>Telefon: {ph("[Telefon]")}<br>E-Mail: {ph("[E-Mail]")}<br>Web: {ph("[Domain]")}</p>

<h2>Vertretung</h2>
<p>{ph("[Geschäftsführung / vertretungsbefugte Person(en)]")}</p>

<h2>Unternehmensgegenstand</h2>
<p>{ph("[z. B. Aus- und Weiterbildung im Bereich Positive Psychologie]")}</p>

<h2>Register und Steuer</h2>
<p>Firmenbuchnummer: {ph("[FN …]")}<br>Firmenbuchgericht: {ph("[Gericht]")}<br>UID-Nummer: {ph("[ATU …]")}</p>

<h2>Aufsichts- und Kammerzugehörigkeit</h2>
<p>Mitglied der {ph("[Wirtschaftskammer … / Fachgruppe …, falls zutreffend]")}<br>Anwendbare Rechtsvorschriften: {ph("[z. B. Gewerbeordnung, abrufbar unter www.ris.bka.gv.at]")}<br>Aufsichtsbehörde / Gewerbebehörde: {ph("[Bezirkshauptmannschaft / Magistrat]")}</p>

<h2>Inhaltlich verantwortlich</h2>
<p>{ph("[Name, Anschrift der inhaltlich verantwortlichen Person]")}</p>

<h2>Verbraucherstreitbeilegung</h2>
<p>Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung bereit: <a href="https://ec.europa.eu/consumers/odr">ec.europa.eu/consumers/odr</a>. Wir sind {ph("[nicht / grundsätzlich]")} bereit, an einem Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen. {ph("[Zutreffende Formulierung wählen und ggf. Schlichtungsstelle nennen]")}</p>

<h2>Haftung für Inhalte</h2>
<p>Wir erstellen die Inhalte dieser Website mit größtmöglicher Sorgfalt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte können wir jedoch keine Gewähr übernehmen. Die Inhalte dienen der allgemeinen Information über unser Bildungsangebot und ersetzen weder eine psychologische noch eine medizinische Beratung oder Behandlung.</p>

<h2>Haftung für Links</h2>
<p>Unsere Website enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Für diese fremden Inhalte übernehmen wir keine Gewähr; verantwortlich ist stets der jeweilige Anbieter. Bei Bekanntwerden von Rechtsverletzungen entfernen wir derartige Links umgehend.</p>

<h2>Urheberrecht</h2>
<p>Die von uns erstellten Inhalte und Werke auf dieser Website unterliegen dem österreichischen Urheberrecht. Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung der jeweiligen Rechteinhaber:innen.</p>

<h2>Bildnachweis</h2>
<p>{ph("[Fotograf:in / Bildquelle für Hero-, Team- und Bannerbilder ergänzen]")}</p>

<p style="margin-top:40px;font-size:var(--pma-fs-base);color:var(--pma-slate)">Stand: {ph("[Datum]")}</p>
</article></div>
"""
    page("impressum.html", "Impressum", "impressum.html", body,
         "Impressum der PERMA Mind Academy.")


# -------------------------------------------------------------- Datenschutz
SECTIONS = [
    ("verantwortlicher", "Verantwortlicher und Kontakt", f"""
<p>Verantwortlich für die Verarbeitung personenbezogener Daten auf dieser Website ist:</p>
<address>{ph("[Firmenname inkl. Rechtsform]")}<br>{ph("[Straße Nr., PLZ Ort]")}, Österreich<br>E-Mail: {ph("[E-Mail]")} · Telefon: {ph("[Telefon]")}</address>
<p>Die Übertragung von Daten auf dieser Website erfolgt verschlüsselt (SSL/TLS). Sie erkennen das an dem Schloss-Symbol und dem Präfix „https://“ in der Adresszeile Ihres Browsers.</p>"""),
    ("grundlagen", "Grundlagen der Verarbeitung", """
<p>Wir verarbeiten personenbezogene Daten im Einklang mit der Datenschutz-Grundverordnung (DSGVO) und dem österreichischen Datenschutzgesetz (DSG). Rechtsgrundlagen sind je nach Zweck Ihre Einwilligung (Art. 6 Abs. 1 lit. a DSGVO), die Erfüllung eines Vertrags oder die Durchführung vorvertraglicher Maßnahmen (lit. b), eine rechtliche Verpflichtung (lit. c) oder unser berechtigtes Interesse an einem sicheren und funktionsfähigen Webauftritt (lit. f).</p>
<p>Wir erheben nur die Daten, die für den jeweiligen Zweck erforderlich sind, und speichern sie nicht länger, als es dieser Zweck oder gesetzliche Aufbewahrungsfristen verlangen.</p>"""),
    ("hosting", "Hosting und Server-Logfiles", f"""
<p>Diese Website wird bei {ph("[Hostinganbieter, Sitz, Serverstandort]")} gehostet. Mit dem Anbieter besteht ein Auftragsverarbeitungsvertrag gemäß Art. 28 DSGVO.</p>
<p>Beim Aufruf der Website speichert der Server automatisch Informationen in sogenannten Logfiles: IP-Adresse, Datum und Uhrzeit der Anfrage, aufgerufene Seite, Referrer-URL, Browsertyp und -version sowie das Betriebssystem. Diese Daten dienen der technisch fehlerfreien Darstellung und der Sicherheit der Website (berechtigtes Interesse, Art. 6 Abs. 1 lit. f DSGVO). Sie werden nicht mit anderen Datenquellen zusammengeführt und nach {ph("[Speicherdauer, z. B. 14 Tagen]")} gelöscht.</p>"""),
    ("cookies", "Cookies", f"""
<p>{ph("[Je nach Einsatz anpassen.]")} Diese Website verwendet ausschließlich technisch notwendige Cookies, die für die Darstellung und Sicherheit erforderlich sind. Für Cookies, die nicht technisch notwendig sind (z. B. Statistik oder eingebettete Inhalte), holen wir vorab Ihre Einwilligung ein. Sie können Cookies jederzeit in den Einstellungen Ihres Browsers löschen oder blockieren; dann sind einzelne Funktionen eventuell eingeschränkt.</p>"""),
    ("kontakt", "Kontaktformular und Vormerkung", """
<p>Wenn Sie uns über das Kontaktformular oder die Vormerkung schreiben, verarbeiten wir die Angaben aus dem Formular (Name, E-Mail-Adresse, optional Telefonnummer, gewünschtes Modul, Nachricht) sowie Zeitpunkt Ihrer Anfrage, um Ihr Anliegen zu bearbeiten und uns bei Ihnen zu melden. Rechtsgrundlage ist Ihre Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) bzw. die Durchführung vorvertraglicher Maßnahmen (lit. b).</p>
<p>Ihre Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen. Wir löschen Ihre Angaben, sobald der Zweck entfällt und keine gesetzlichen Aufbewahrungspflichten entgegenstehen, spätestens jedoch nach <span class="ph">[Löschfrist, z. B. 12 Monaten]</span> ohne Folgekontakt. Eine Weitergabe an Dritte erfolgt nur, soweit dies zur Bearbeitung erforderlich ist (z. B. E-Mail-Dienstleister) oder Sie eingewilligt haben.</p>"""),
    ("anfragen", "Anfragen per E-Mail oder Telefon", """
<p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, speichern und verarbeiten wir Ihre Anfrage einschließlich aller darin enthaltenen personenbezogenen Daten zur Bearbeitung Ihres Anliegens. Diese Daten geben wir nicht ohne Ihre Einwilligung weiter.</p>"""),
    ("fonts", "Schriftarten", f"""
<p>{ph("[Auswahl treffen:]")} Diese Website bindet Schriftarten (Roboto, Montserrat, Great Vibes) ein. Variante A: Die Schriften werden lokal von unserem Server ausgeliefert, es findet keine Verbindung zu Google statt. Variante B: Die Schriften werden von Google Fonts geladen; dabei übermittelt Ihr Browser Ihre IP-Adresse an Google. In diesem Fall ist Ihre Einwilligung erforderlich. Wir empfehlen die lokale Einbindung.</p>"""),
    ("newsletter", "Newsletter", f"""
<p>{ph("[Nur falls ein Newsletter angeboten wird.]")} Für den Versand des Newsletters verwenden wir das Double-Opt-in-Verfahren: Nach der Anmeldung erhalten Sie eine Bestätigungs-E-Mail. Gespeichert werden E-Mail-Adresse, Zeitpunkt der Anmeldung und Bestätigung sowie die IP-Adresse. Sie können sich jederzeit über den Link in jeder E-Mail abmelden.</p>"""),
    ("rechte", "Ihre Rechte", """
<p>Ihnen stehen nach der DSGVO folgende Rechte zu:</p>
<ul>
<li>Auskunft über die verarbeiteten Daten (Art. 15)</li>
<li>Berichtigung unrichtiger Daten (Art. 16)</li>
<li>Löschung (Art. 17) und Einschränkung der Verarbeitung (Art. 18)</li>
<li>Datenübertragbarkeit (Art. 20)</li>
<li>Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen (Art. 21)</li>
<li>Widerruf einer erteilten Einwilligung mit Wirkung für die Zukunft (Art. 7 Abs. 3)</li>
</ul>
<p>Zur Ausübung dieser Rechte genügt eine formlose Nachricht an die oben genannte Kontaktadresse. Sie haben außerdem das Recht, sich bei der zuständigen Aufsichtsbehörde zu beschweren. In Österreich ist das die <a href="https://www.dsb.gv.at">Datenschutzbehörde</a>, Barichgasse 40–42, 1030 Wien.</p>"""),
    ("speicherdauer", "Speicherdauer", """
<p>Wir speichern personenbezogene Daten, solange der Zweck der Verarbeitung besteht. Gesetzliche Aufbewahrungspflichten, etwa nach Unternehmens- und Steuerrecht, bleiben unberührt.</p>"""),
    ("aenderungen", "Änderungen dieser Erklärung", f"""
<p>Wir passen diese Datenschutzerklärung an, wenn sich Rechtslage oder Angebot ändern. Es gilt die jeweils hier veröffentlichte Fassung. Stand: {ph("[Datum]")}</p>"""),
]


def datenschutz():
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t, _ in SECTIONS)
    secs = "".join(f'<h2 id="{i}">{t}</h2>{b}' for i, t, b in SECTIONS)
    body = f"""
<section class="page-hero"><div class="wrap">
<p class="crumbs"><a href="Main.dc.html">Startseite</a> / Datenschutz</p>
<p class="eyebrow">Rechtliches</p><h1>Datenschutzerklärung</h1>
<p class="lead">Wir nehmen den Schutz Ihrer Daten ernst. Hier erfahren Sie, welche Daten wir verarbeiten, wofür wir sie brauchen und welche Rechte Sie haben.</p></div></section>
<div class="wrap"><article class="prose">
<p class="draft"><strong>Entwurf.</strong> Der Text folgt dem üblichen Aufbau einer Datenschutzerklärung für Bildungsanbieter und ist eine Arbeitsgrundlage, keine Rechtsberatung. Gelb markierte Angaben sind zu ergänzen. Abschnitte müssen zur tatsächlichen Technik passen (Hosting, Formular-Dienst, Schriften, Statistik). Vor Veröffentlichung bitte rechtlich prüfen lassen.</p>
<nav class="toc" aria-label="Inhalt"><strong>Inhalt</strong><ol>{toc}</ol></nav>
{secs}
</article></div>
"""
    page("datenschutz.html", "Datenschutz", "datenschutz.html", body,
         "Datenschutzerklärung der PERMA Mind Academy.")


if __name__ == "__main__":
    kontakt()
    impressum()
    datenschutz()
    print("kontakt.html, impressum.html, datenschutz.html ->", OUT.relative_to(ROOT))
