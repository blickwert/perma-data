# Abnahme WordPress-Umsetzung (Phase 4)

Stand: 23. November 2026. Dev-Installation `https://dev.blickwert.at/wp/2604-perma/`, Theme `perma-mind` 0.5.1, Plugin `bw-perma-forms` 0.3.0, WordPress 7.1.5, PHP 8.3, Contact Form 7 6.2.5, Yoast SEO, Brevo-Plugin.

## Ergebnis

| Prüfpunkt | Ergebnis |
|---|---|
| Seiten wie v2b bei 1440 px und 390 px | ✅ 6 Seiten × 2 Breiten verglichen; Seitenlängen ±2 %, Abweichungen unten |
| Keine Inline-Styles mit Rohwerten, keine freien Farben | ✅ keine `style`-Attribute in Patterns, Vorlagen, Teilen, Seiteninhalten; im Editor freie Farben, Verläufe, Schriftgrößen, Abstände aus |
| Neue Seite nur aus Patterns und Stilen | ✅ Playground: Seite aus 4 Patterns, Text geändert, Akzent Blau → Grün und Abschnitt Neutral → Mint per Stil; 0 ungültige Blöcke, Frontend richtig |
| Schriften lokal, keine fremden Server | ✅ alle Anfragen der 7 Seiten nur an die eigene Domain (Turnstile folgt auf der Live-Seite) |
| Je Seite eine H1, Hierarchie, Tastatur | ✅ 7 Seiten: genau eine H1, keine Sprünge; Akkordeon per Enter/Leertaste; Fokus sichtbar (2 px); alle Bilder mit Alt-Attribut |
| Formulare, Mails, Brevo, Spamschutz | ✅ Interessentenliste und Kontakt: Mails an bw-cms@blickwert.at angekommen; Newsletter: Double-Opt-in-Mail von Brevo, Bestätigung per Webhook zurück („Angemeldet“); Honeypot greift; Turnstile auf der Live-Seite |
| `php -l`, Tests, Debug-Log | ✅ `php -l` grün, 30 Plugin-Tests grün, Typprüfung grün; Debug-Log ohne Meldungen aus Theme/Plugin (Theme-Notice zum Button-Stil „Kontur“ behoben, 0.5.1); verbleibend nur eine Meldung aus dem WordPress-Kern (`widgets.php`, Dashboard-RSS) |
| Doku | ✅ `CLAUDE.md`, `WP-UMSETZUNG.md`, `WP-THEME.md`, `WP-PLUGIN.md`, diese Datei |
| Ladezeit (Lighthouse) | Handy 95, Desktop 98; Barrierefreiheit 100, Best Practices 100; SEO 63 nur wegen gesperrter Dev-Seite |

## Abweichungen von v2b (gewollt oder begründet)

- **Hero:** Foto statt Platzhalter; mobil ohne Textkasten, Hochformat-Bild, kurzer Satz statt Absatz, Hero bis zum unteren Rand mit Profilmerkmalen als Slider (Wunsch des Auftraggebers).
- **Schwebender Button:** erscheint erst nach dem Hero.
- **Etiketten auf den Angebotskarten:** dunklere Schrift (Blau, Orange) bzw. dunkleres Lila für ausreichenden Kontrast.
- **Akkordeon-Titel** sind keine Überschriften (core/details); **mobiles Menü** ist das Vollbild-Menü von WordPress.
- **Rechtstexte:** ohne Brotkrumen; die Einleitung der Datenschutzerklärung steht über dem Text statt im Seitenkopf.
- **Newsletter-Knopf** ist ausgegraut, bis die Einwilligung angehakt ist (Verhalten von Contact Form 7).

Details: `docs/WP-THEME.md`.

## Vor dem Livegang

1. **Hoster:** Seiten-Cache (Antwortzeit derzeit 0,7 s), HTTP/2, Cache-Dauer für Bilder, CSS, JS.
2. **Turnstile-Schlüssel** in Contact Form 7 › Integration (Auftraggeber).
3. **Empfänger** der Formular-Mails auf `info@perma-academy.at` umstellen (PERMA Kontakte › Einstellungen).
4. **Rechtstexte:** Entwürfe sind vorgeschrieben (`content/rechtstexte/impressum.html`, `datenschutz.html`, abgestimmt auf die Technik der Website: Kontaktdatenbank, Brevo, Turnstile, lokale Schriften, keine Tracking-Cookies). Offen: gelb markierte Angaben (Rechtsform, Firmenbuch, UID, Gewerbe, Hoster, Speicherfristen, Brevo-Öffnungsstatistik, Bildnachweis) ergänzen und rechtlich prüfen lassen.
   - **AGB** (`content/rechtstexte/agb.html`, Seite `/agb/`, im Footer verlinkt) aus der Vorlage der Academy übernommen. Offen: Abschnitt 10 „Haftung“ bricht in der Vorlage mitten im Satz ab, Firmenname und Rechtsform.
   - Bis zur Gründung der OG muss im Impressum eine verantwortliche Person stehen (Platzhalter angepasst).
   - Social Media: Instagram und Facebook im Footer; LinkedIn folgt (Adresse in `SOCIAL` in `scripts/v2b_content.py` eintragen, das Symbol erscheint dann automatisch).
5. **Offene Inhalte:** Trainerfotos, ECQA-Logo, Termine, Orte, Fristen, Zertifizierungsgebühren.
6. **Live-Seite:** Suchmaschinen zulassen (Einstellungen › Lesen), Brevo-Webhook auf die Live-Adresse („Brevo einrichten“ erneut ausführen), `WP_DEBUG` aus.
