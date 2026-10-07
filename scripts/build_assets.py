"""Build original, self-contained profile SVGs with Python's standard library."""

from html import escape
from math import cos, sin, pi
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
THEMES = {
    "dark": dict(bg="#0c131d", panel="#131e2c", line="#2c3e52",
                 text="#edf4fa", muted="#a3b4c7", accent="#63dfd3",
                 secondary="#b2a7ef", soft="#1a323b"),
    "light": dict(bg="#f7f9fc", panel="#eaf0f6", line="#b9c8d8",
                  text="#16293b", muted="#4e6379", accent="#00776e",
                  secondary="#66539d", soft="#d9efec"),
}


def text(x, y, value, color, size=18, mono=False, weight=400, anchor="start"):
    family = "Consolas, 'Liberation Mono', monospace" if mono else "'Segoe UI', Arial, sans-serif"
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')


def rect(x, y, w, h, fill, stroke="none", radius=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def line(x1, y1, x2, y2, stroke, width=1, dash=""):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{width}"' + (f' stroke-dasharray="{dash}"' if dash else "") + '/>')


def circle(x, y, r, fill, stroke="none", width=1):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def svg(w, h, title, description, body, p):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title>\n<desc id="desc">{escape(description)}</desc>\n'
            + rect(1, 1, w-2, h-2, p["bg"], p["line"], 16) + '\n'
            + '\n'.join(body) + '\n</svg>\n')


def mark(x, y, scale, p):
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" '
            f'stroke="{p["accent"]}" stroke-width="6" stroke-linecap="square" stroke-linejoin="miter">'
            '<path d="M7 44V8H36M7 25H28M42 16L54 28L42 40"/>'
            '<path d="M27 49H43" stroke-width="4"/></g>')


def header(p, number, name, detail, w=440):
    return [text(26, 34, number, p["accent"], 14, True),
            text(65, 34, name, p["muted"], 14, True),
            line(26, 52, w-26, 52, p["line"]),
            text(26, 87, detail, p["text"], 25, weight=600)]


def banner(p):
    body = []
    # A quiet graph-paper field, all geometry local to the SVG.
    for x in range(580, 820, 24):
        body.append(line(x, 60, x, 238, p["panel"]))
    for y in range(70, 239, 24):
        body.append(line(575, y, 812, y, p["panel"]))
    body += [text(34, 40, "PROFILE / FLACO332", p["muted"], 14, True),
             circle(744, 35, 4, p["accent"]),
             text(758, 40, "~/", p["muted"], 14, True),
             line(34, 56, 806, 56, p["line"]),
             text(34, 99, "$ open profile", p["accent"], 20, True),
             text(30, 172, "flaco332", p["text"], 78, weight=700),
             rect(391, 157, 19, 7, p["accent"]),
             text(34, 216, "Systems Engineering Student", p["muted"], 25),
             mark(625, 90, 2.2, p),
             text(681, 225, "SYSTEMS / SECURITY", p["muted"], 12, True, anchor="middle"),
             line(34, 244, 806, 244, p["line"]),
             text(34, 280, "CYBERSECURITY / CLOUD / LINUX / DEVSECOPS", p["accent"], 20, True)]
    return svg(840, 308, "flaco332 | systems & security", "Terminal-inspired profile for a Systems Engineering Student focused on Cybersecurity, Cloud, Linux and DevSecOps.", body, p)


def whoami(p):
    body = [text(32, 37, "01 / IDENTITY", p["muted"], 14, True),
            text(32, 87, "Understand the system.", p["text"], 38, weight=600),
            text(32, 132, "Trace the signal. Secure the path.", p["accent"], 32, weight=600),
            line(32, 157, 808, 157, p["line"]),
            text(32, 195, "NETWORKS", p["muted"], 17, True),
            text(223, 195, "LOW-LEVEL", p["muted"], 17, True),
            text(425, 195, "INFRASTRUCTURE", p["muted"], 17, True),
            text(686, 195, "CV / ML", p["muted"], 17, True)]
    return svg(840, 225, "whoami | engineering through exploration", "Understand the system, trace the signal, secure the path. Interests include networks, low-level programming, infrastructure, Computer Vision and ML.", body, p)


STACKS = {
    "security": ("02", "stack/security", "Cybersecurity", [
        ("ENVIRONMENT", ["Kali Linux"]),
        ("TRAFFIC / ANALYSIS", ["Nmap · Wireshark · Scapy", "Snort · Bettercap"]),
        ("PRACTICE", ["Network analysis · packet inspection", "IDS concepts"]),
    ]),
    "cloud": ("03", "stack/cloud-data", "Cloud & data", [
        ("PROVIDER", ["Google Cloud"]),
        ("MANAGED DATA", ["Cloud SQL · Spanner", "Firestore · Bigtable"]),
        ("DATABASES", ["PostgreSQL · SQLite · Supabase"]),
    ]),
    "code": ("04", "stack/code-web", "Languages & web", [
        ("SYSTEMS / SCRIPTING", ["C · C++ · Python · Bash"]),
        ("WEB LANGUAGES", ["TypeScript · JavaScript"]),
        ("FRONTEND", ["React · Vite · Tailwind CSS"]),
    ]),
    "systems": ("05", "stack/systems-vision", "Systems & vision", [
        ("WORKSPACE", ["Linux · WSL · VS Code"]),
        ("VERSIONING / CI", ["Git · GitHub Actions"]),
        ("IMAGE PROCESSING", ["OpenCV · SciPy", "scipy.ndimage · Pillow"]),
    ]),
}


def stack_card(p, key):
    number, name, title, groups = STACKS[key]
    body = header(p, number, name, title)
    y = 124
    for label, rows in groups:
        body += [text(26, y, label, p["accent"], 13, True)]
        for value in rows:
            y += 27
            body += [text(26, y, value, p["text"], 18)]
        y += 36
    return svg(440, 370, title, "; ".join(label + ": " + ", ".join(rows) for label, rows in groups), body, p)


PROJECTS = {
    "packet-tracer-security": ("01", "Packet Tracer Security", "DEFENSIVE / EXPERIMENTAL", ["Rule-based traffic analysis.", "Explainable alerts & evidence replay."], "Python / Scapy / Prolog", "traffic  >  rules  >  evidence"),
    "grep-c": ("02", "Grep-C / Mini Grep", "TERMINAL / ALGORITHMS", ["Exact filename search with binary", "search, a Textual TUI & a CLI."], "Python / Textual / CLI", "index  >  search  >  inspect"),
    "onca": ("03", "ONCA", "DESKTOP / LOCAL DATA", ["Student, payment & activity records.", "SQLite storage & verified backups."], "Python / Tkinter / SQLite", "interface  >  data  >  backup"),
}


def project(p, key):
    number, title, category, rows, tags, flow = PROJECTS[key]
    body = [text(26, 33, f"PROJECT / {number}", p["muted"], 13, True),
            text(410, 35, "↗", p["accent"], 23, anchor="end"),
            text(26, 77, title, p["text"], 28, weight=600),
            text(26, 104, category, p["accent"], 13, True),
            line(26, 124, 414, 124, p["line"]),
            text(26, 158, rows[0], p["text"], 19),
            text(26, 185, rows[1], p["text"], 19),
            rect(26, 209, 388, 40, p["panel"], radius=6),
            text(40, 235, tags, p["muted"], 16, True),
            text(26, 277, flow, p["accent"], 14, True)]
    return svg(440, 300, title, f"{category}. {' '.join(rows)} Built with {tags}.", body, p)


def radar(p, languages=False):
    title = "Language map" if languages else "Focus map"
    subtitle = "languages / equal spokes" if languages else "skills / connected areas"
    body = header(p, "07" if languages else "06", subtitle, title)
    cx, cy = 220, 248
    for radius in (37, 67, 98):
        body.append(circle(cx, cy, radius, "none", p["line"]))
    labels = (["Python", "C", "C++", "TypeScript", "JavaScript", "Bash"] if languages else
              ["Cybersecurity", "Cloud", "Linux /", "Networking", "Low-level", "CV / ML"])
    positions = [(220, 120, "middle"), (354, 187, "middle"), (354, 323, "middle"),
                 (220, 387, "middle"), (86, 323, "middle"), (86, 187, "middle")]
    for i, (label, (lx, ly, anchor)) in enumerate(zip(labels, positions)):
        angle = -pi / 2 + i * pi / 3
        x, y = round(cx + 98 * cos(angle), 2), round(cy + 98 * sin(angle), 2)
        body += [line(cx, cy, x, y, p["line"]), circle(x, y, 7, p["bg"], p["accent"], 2),
                 circle(x, y, 2, p["accent"]), text(lx, ly, label, p["text"], 18, weight=600, anchor=anchor)]
        if not languages and i == 2:
            body += [text(lx, ly + 23, "DevSecOps", p["text"], 17, anchor=anchor)]
        if not languages and i == 4:
            body += [text(lx, ly + 23, "programming", p["muted"], 15, anchor=anchor)]
    body += [circle(cx, cy, 31, p["soft"], p["accent"]),
             text(cx, cy+6, "</>" if languages else "~/", p["accent"], 22, True, anchor="middle"),
             line(26, 420, 414, 420, p["line"]),
             text(26, 448, "COVERAGE / NO PROFICIENCY SCORES", p["muted"], 13, True)]
    return svg(440, 468, title, ", ".join(labels).replace("Linux /,", "Linux / DevSecOps,") + ". Equal spokes express coverage, without scores or percentages.", body, p)


def logo(p):
    return svg(128, 128, "flaco332 | terminal mark", "Original geometric F, command chevron and terminal cursor.", [mark(23, 25, 1.5, p)], p)


def main():
    ASSETS.mkdir(exist_ok=True)
    for mode, palette in THEMES.items():
        suffix = "" if mode == "dark" else "-light"
        content = {f"banner-{mode}": banner(palette), f"whoami{suffix}": whoami(palette),
                   f"radar-skills{suffix}": radar(palette), f"radar-langs{suffix}": radar(palette, True),
                   f"logo{suffix}": logo(palette)}
        for key in STACKS:
            content[f"tech-stack-{key}{suffix}"] = stack_card(palette, key)
        for key in PROJECTS:
            content[f"project-card-{key}{suffix}"] = project(palette, key)
        for name, data in content.items():
            (ASSETS / f"{name}.svg").write_text(data, encoding="utf-8", newline="\n")
    print(f"Built {len(list(ASSETS.glob('*.svg')))} local SVGs.")


if __name__ == "__main__":
    main()
