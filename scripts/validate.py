"""Validate local SVGs, README markup, assets and internal links offline."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import xml.etree.ElementTree as ET

from preview import slug

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_URLS = {
    "https://github.com/flaco332",
    "https://github.com/flaco332/packet-tracer-security",
    "https://github.com/flaco332/grep-c",
    "https://github.com/flaco332/Onca",
    "https://flaco332.github.io/carlos-portafolio/",
    "https://t.me/cr0dev",
    "mailto:crdeveloper@proton.me",
}


class ProfileHTML(HTMLParser):
    void = {"source", "img"}
    allowed = {"picture", "source", "img", "p", "a", "details", "summary", "code"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.references, self.pictures = [], [], []

    def handle_starttag(self, tag, attrs):
        assert tag in self.allowed, f"Unexpected README HTML tag: {tag}"
        attrs = dict(attrs)
        assert not any(a.startswith("on") or a == "style" for a in attrs), "Inline JS/CSS in README"
        if tag == "picture":
            self.pictures.append([])
        if tag in {"source", "img"}:
            assert self.stack[-1] == "picture", f"{tag} outside picture"
            self.pictures[-1].append((tag, attrs))
        if tag == "img":
            assert attrs.get("alt"), "Image without descriptive alt"
            assert 0 < int(attrs["width"]) <= 840, "Unexpected image width"
        if tag == "a":
            self.references.append(attrs["href"])
        if tag in self.void:
            self.references.append(attrs["srcset"] if tag == "source" else attrs["src"])
        else:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, f"Unbalanced HTML: {tag}"


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    parser = ProfileHTML()
    parser.feed(readme)
    assert not parser.stack, f"Unclosed HTML tags: {parser.stack}"
    for picture in parser.pictures:
        assert [tag for tag, _ in picture] == ["source", "source", "img"]
        assert picture[0][1]["media"] == "(prefers-color-scheme: dark)"
        assert picture[1][1]["media"] == "(prefers-color-scheme: light)"
        assert picture[2][1]["src"] == picture[0][1]["srcset"], "Missing dark fallback"
        roots = [ET.parse(ROOT / pic[1]["srcset"]).getroot() for pic in picture[:2]]
        assert roots[0].get("viewBox") == roots[1].get("viewBox"), "Theme pair dimensions differ"
    headings = {slug(row[3:]) for row in readme.splitlines() if row.startswith("## ")}
    links = parser.references + re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)
    for link in links:
        if link.startswith("#"):
            assert link[1:] in headings, f"Broken section link: {link}"
        elif urlparse(link).scheme:
            assert link in ALLOWED_URLS, f"Unapproved public URL: {link}"
        else:
            assert (ROOT / link).is_file(), f"Missing local asset: {link}"
    svgs = list((ROOT / "assets").glob("*.svg"))
    assert len(svgs) == 24, f"Expected 24 SVGs, found {len(svgs)}"
    for path in svgs:
        raw = path.read_text(encoding="utf-8")
        root = ET.fromstring(raw)
        ns = {"s": "http://www.w3.org/2000/svg"}
        assert root.tag == "{http://www.w3.org/2000/svg}svg"
        assert root.find("s:title", ns) is not None and root.find("s:desc", ns) is not None
        assert root.get("viewBox") and root.get("role") == "img"
        assert not re.search(r"<(script|foreignObject|image|animate)\b", raw)
        assert "href=" not in raw and "url(" not in raw, "Non-local SVG dependency"
        ids = [el.attrib["id"] for el in root.iter() if "id" in el.attrib]
        assert len(ids) == len(set(ids)), f"Duplicate IDs in {path.name}"
    for name in ("C++", "TypeScript", "Kali Linux", "Bettercap", "Spanner", "Bigtable",
                 "Supabase", "scipy.ndimage", "Pillow", "GitHub Actions", "WSL"):
        assert name in readme, f"Missing stack term: {name}"
    assert "████    ███   ███" in readme and "Brazilian Jiu-Jitsu" in readme
    assert readme.count("```") % 2 == 0, "Unclosed code fence"
    print(f"PASS: {len(svgs)} SVGs; {len(parser.pictures)} theme pairs; HTML nesting; local assets; internal links; authorized URLs; stack; BJJ.")
    print("External availability requires a separate network check; this script validates URLs offline.")


if __name__ == "__main__":
    main()
