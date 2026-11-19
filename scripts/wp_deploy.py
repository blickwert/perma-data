#!/usr/bin/env python3
"""Überträgt Theme, Plugin und Seiten auf eine WordPress-Installation mit BW WP Bridge (ab 1.10).

    python3 scripts/wp_deploy.py --site perma build      # ZIPs bauen (Theme, Plugin inkl. Admin-App)
    python3 scripts/wp_deploy.py --site perma install    # ZIPs installieren und aktivieren (überschreibt)
    python3 scripts/wp_deploy.py --site perma pages      # Seiten aus wordpress/content anlegen/aktualisieren, Startseite setzen
    python3 scripts/wp_deploy.py --site perma all

Zugangsdaten aus Umgebungsvariablen (nie ins Repo): WP_<SITE>_URL, WP_<SITE>_USER, WP_<SITE>_APP_PASSWORD,
WP_<SITE>_BRIDGE_KEY. Seiteninhalte enthalten {{home:/pfad}}; das Skript setzt die Adresse der Installation ein.
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
THEME = ROOT / "wordpress/themes/perma-mind"
PLUGIN = ROOT / "wordpress/plugins/bw-perma-forms"
CONTENT = ROOT / "wordpress/content"


class Site:
    def __init__(self, name):
        p = f"WP_{name.upper()}_"
        try:
            self.url = os.environ[p + "URL"].rstrip("/")
            auth = os.environ[p + "USER"] + ":" + os.environ[p + "APP_PASSWORD"]
        except KeyError as e:
            sys.exit(f"Umgebungsvariable fehlt: {e}")
        self.headers = {"Authorization": "Basic " + base64.b64encode(auth.encode()).decode(), "Content-Type": "application/json"}
        if os.environ.get(p + "BRIDGE_KEY"):
            self.headers["X-BW-Bridge-Key"] = os.environ[p + "BRIDGE_KEY"]

    def call(self, method, route, body=None, query=None):
        q = {"rest_route": "/" + route}
        q.update(query or {})
        req = urllib.request.Request(self.url + "/?" + urllib.parse.urlencode(q), method=method, headers=self.headers,
                                     data=None if body is None else json.dumps(body).encode())
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            sys.exit(f"{method} {route}: HTTP {e.code} {e.read()[:400].decode(errors='replace')}")


def zip_dir(src: Path, prefix: str, out: Path, skip=()):
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            rel = f.relative_to(src).as_posix()
            if f.is_file() and not any(rel.startswith(s) for s in skip):
                z.write(f, f"{prefix}/{rel}")
    print(f"{out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")


def build():
    subprocess.run([sys.executable, str(ROOT / "scripts/build_theme.py")], check=True)
    subprocess.run(["npm", "run", "build"], cwd=PLUGIN, check=True, stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, str(PLUGIN / "scripts/build-i18n.py")], check=True)
    if not (PLUGIN / "free/build/admin.js").exists():
        sys.exit("Admin-App fehlt (npm install && npm run build in wordpress/plugins/bw-perma-forms)")
    zip_dir(THEME, "perma-mind", DIST / "perma-mind.zip")
    zip_dir(PLUGIN / "free", "bw-perma-forms", DIST / "bw-perma-forms.zip")


def install(site: Site):
    for kind, file in (("themes", "perma-mind.zip"), ("plugins", "bw-perma-forms.zip")):
        data = base64.b64encode((DIST / file).read_bytes()).decode()
        r = site.call("POST", f"bw-bridge/v1/{kind}/install", {"zip_base64": data, "activate": True, "overwrite": True})
        print(f"{kind}: {r.get('stylesheet') or r.get('plugin')} {r.get('version')} aktiv={r.get('active')}")


def pages(site: Site):
    index = json.loads((CONTENT / "pages.json").read_text("utf-8"))["pages"]
    front = 0
    for p in index:
        markup = (CONTENT / p["file"]).read_text("utf-8")
        markup = re.sub(r"\{\{home:([^}]*)\}\}", lambda m: site.url + m.group(1), markup)
        found = site.call("GET", "wp/v2/pages", query={"slug": p["slug"], "status": "publish,draft,private", "_fields": "id"})
        body = {"title": p["title"], "slug": p["slug"], "content": markup, "status": "publish", "template": p["template"]}
        if found:
            r = site.call("POST", f"wp/v2/pages/{found[0]['id']}", body)
            state = "aktualisiert"
        else:
            r = site.call("POST", "wp/v2/pages", body)
            state = "angelegt"
        print(f"{p['slug']:34} #{r['id']} {state}")
        if p["front_page"]:
            front = r["id"]
    if front:
        site.call("POST", "wp/v2/settings", {"show_on_front": "page", "page_on_front": front})
        print(f"Startseite: #{front}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", default="perma")
    ap.add_argument("step", choices=["build", "install", "pages", "all"])
    a = ap.parse_args()
    if a.step in ("build", "all"):
        build()
    if a.step in ("install", "all"):
        install(Site(a.site))
    if a.step in ("pages", "all"):
        pages(Site(a.site))
