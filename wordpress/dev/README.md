# Lokale Prüfung mit WordPress Playground

```bash
npx @wp-playground/cli@3.1.65 server --port=9400 --php=8.3 --wp=latest --login \
  --mount=wordpress/themes/perma-mind:/wordpress/wp-content/themes/perma-mind \
  --mount=wordpress/content:/perma-content \
  --mount=wordpress/dev/seed-pages.php:/wordpress/seed-pages.php \
  --blueprint=wordpress/dev/playground-blueprint.json
```

Danach `http://127.0.0.1:9400/seed-pages.php` aufrufen (legt die Seiten aus `wordpress/content/` an, setzt die Startseite).
Vergleich mit der Vorschau: `cd design/v2b && python3 -m http.server 9500`.
