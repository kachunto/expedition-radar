#!/usr/bin/env python3
"""Build the static site into dist/. Usage: python3 scripts/build.py

Reads content/items.json, config/site.json and src/*.html. The environment variable
REPO_URL overrides the repo url in config/site.json.
"""
import json, os, shutil, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def p(*a): return os.path.join(ROOT, *a)

site = json.load(open(p("config", "site.json"), encoding="utf-8"))
repo = os.environ.get("REPO_URL", site["repo_url"]).rstrip("/")
data = json.load(open(p("content", "items.json"), encoding="utf-8"))

blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = open(p("src", "template.html"), encoding="utf-8").read()
for key, val in (("__DATA__", blob), ("__REPO__", repo), ("__VERSION__", site["version_label"])):
    assert key in html, "template is missing " + key
    html = html.replace(key, val)

os.makedirs(p("dist"), exist_ok=True)
open(p("dist", "index.html"), "w", encoding="utf-8").write(html)
shutil.copy(p("src", "legal.html"), p("dist", "legal.html"))
# Cloudflare Pages / Netlify style headers. Add the Supabase domain to connect-src when accounts arrive.
open(p("dist", "_headers"), "w").write(
    "/*\n"
    "  X-Content-Type-Options: nosniff\n"
    "  Referrer-Policy: strict-origin-when-cross-origin\n"
    "  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com; "
    "style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://cloudflareinsights.com\n")

print("built dist/index.html (%d items, %.0f KB)" % (len(data["items"]), len(html) / 1024))
todo = [f for f in ("index.html", "legal.html") if "FILL_IN" in open(p("dist", f), encoding="utf-8").read()]
if todo: print("NOTE: FILL_IN markers remain in " + ", ".join(todo) + " - fill them in before sharing publicly.")
if "OWNER/expedition-radar" in repo: print("NOTE: set repo_url in config/site.json (or REPO_URL) so the report links work.")
