"""Release-readiness checks for a rendered Quarto website.

Run as: python tests/audit_built_site.py docs
No external dependencies or network access are required.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
import xml.etree.ElementTree as ET

ROOT = Path(sys.argv[1] if len(sys.argv)>1 else "docs").resolve()
ERRORS=[]
class Audit(HTMLParser):
    def __init__(self,filename):
        super().__init__(convert_charrefs=True)
        self.file=filename
        self.ids=set()
        self.anchors=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:self.ids.add(a["id"])
        if tag in ("img","iframe"):
            key="src"
            if tag=="img" and a.get("alt") is None:
                ERRORS.append(f"{self.file}: missing descriptive alt for {a.get(key)}")
            if tag=="iframe" and not a.get("title"):
                ERRORS.append(f"{self.file}: missing iframe title for {a.get(key)}")
        if tag in ("a","script","link","img","iframe"):
            key="href" if tag in ("a","link") else "src"
            url=a.get(key,"")
            if not url or url.startswith(("mailto:","javascript:","data:","tel:")):return
            u=urlsplit(url)
            if u.scheme or u.netloc or url.startswith("//"):return
            if not u.path:
                if tag=="a" and u.fragment:self.anchors.append(u.fragment)
                return
            target=(self.file.parent/unquote(u.path)).resolve()
            if ROOT not in target.parents and ROOT!=target:
                ERRORS.append(f"{self.file}: unsafe local path {url}")
                return
            if target.is_dir():target/= "index.html"
            if not target.exists():
                ERRORS.append(f"{self.file}: missing {url}")
    def close(self):
        super().close()
        for anchor in self.anchors:
            if anchor and anchor not in self.ids:
                ERRORS.append(f"{self.file}: broken in-page anchor #{anchor}")

if not ROOT.is_dir():raise SystemExit(f"Missing site output: {ROOT}")
html=list(ROOT.rglob("*.html"))
if len(html)<20:ERRORS.append(f"Expected website output >=20 pages, found {len(html)}")
for f in html:
    p=Audit(f)
    p.feed(f.read_text(encoding="utf-8",errors="replace"))
    p.close()
for svg in ROOT.rglob("*.svg"):
    try:ET.parse(svg)
    except ET.ParseError as e:ERRORS.append(f"{svg}: invalid SVG/XML: {e}")
for needed in ("index.html","privacy.html","reuse.html","lessons/index.html",
               "lessons/gosling-genome-tracks.html"):
    if not (ROOT/needed).exists():ERRORS.append(f"missing expected page {needed}")
if ERRORS:
    print("RELEASE AUDIT FAILED")
    for x in ERRORS[:80]:print("-",x)
    raise SystemExit(f"{len(ERRORS)} failures")
print(f"Release audit passed: {len(html)} HTML pages, {len(list(ROOT.rglob('*.svg')))} SVGs; no missing local assets, absent alt text, unlabeled iframes or broken same-page anchors.")
