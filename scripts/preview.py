"""Render this README's Markdown subset to a portable, offline HTML preview.

This is a visual approximation, not GitHub's Markdown renderer or sanitizer.
The profile itself only needs README.md and the assets directory.
"""

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def slug(value):
    return re.sub(r"[^a-z0-9 _-]", "", value.lower()).replace(" ", "-")


def inline(value):
    value = escape(value)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', value)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)


def render(source):
    output, paragraph, code = [], [], None
    in_list = False

    def flush():
        if paragraph:
            output.append("<p>" + inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    for row in source.splitlines():
        if row.startswith("```"):
            flush()
            if code is None:
                code = []
            else:
                output.append("<pre><code>" + escape("\n".join(code)) + "</code></pre>")
                code = None
            continue
        if code is not None:
            code.append(row)
            continue
        if in_list and not row.startswith("- "):
            output.append("</ul>")
            in_list = False
        if not row.strip():
            flush()
        elif row.startswith("## "):
            flush()
            title = row[3:]
            output.append(f'<h2 id="{slug(title)}">{inline(title)}</h2>')
        elif row.startswith("- "):
            flush()
            if not in_list:
                output.append("<ul>")
                in_list = True
            output.append("<li>" + inline(row[2:]) + "</li>")
        elif row == "---":
            flush()
            output.append("<hr>")
        elif row.lstrip().startswith("<"):
            flush()
            output.append(row.replace('="assets/', '="../assets/'))
        else:
            paragraph.append(row)
    flush()
    if in_list:
        output.append("</ul>")
    return "\n".join(output)


PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>flaco332 · Profile preview</title>
<link rel="icon" type="image/svg+xml" href="../assets/logo.svg">
<style>
:root { color-scheme:light dark; --bg:#ffffff; --fg:#1f2328; --line:#d1d9e0; --code:#eff2f5; --link:#0969da; }
@media (prefers-color-scheme:dark) { :root { --bg:#0d1117; --fg:#f0f6fc; --line:#3d444d; --code:#151b23; --link:#4493f8; } }
html[data-mode="light"] { color-scheme:light; --bg:#ffffff; --fg:#1f2328; --line:#d1d9e0; --code:#eff2f5; --link:#0969da; }
html[data-mode="dark"] { color-scheme:dark; --bg:#0d1117; --fg:#f0f6fc; --line:#3d444d; --code:#151b23; --link:#4493f8; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif; font-size:16px; line-height:1.5; }
nav { max-width:906px; margin:20px auto 0; padding:0 32px; display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
nav small { margin-right:auto; color:var(--fg); opacity:.72; }
button { cursor:pointer; color:var(--fg); background:var(--code); border:1px solid var(--line); border-radius:6px; padding:5px 10px; font:inherit; font-size:13px; }
button[aria-pressed="true"] { border-color:var(--link); }
article { max-width:906px; margin:20px auto 40px; padding:32px; border:1px solid var(--line); border-radius:8px; overflow-wrap:break-word; }
h2 { margin:24px 0 16px; padding-bottom:.3em; font-size:1.5em; line-height:1.25; border-bottom:1px solid var(--line); }
p,ul,pre,details { margin-top:0; margin-bottom:16px; }
ul { padding-left:2em; } li+li { margin-top:.25em; }
a { color:var(--link); text-decoration:none; } a:hover { text-decoration:underline; }
img { max-width:100%; height:auto; vertical-align:baseline; background:transparent; box-sizing:content-box; }
picture { font-size:0; } p:has(>picture),p:has(>a>picture) { line-height:1.8; }
code { padding:.2em .4em; font-family:Consolas,"Liberation Mono",monospace; font-size:85%; background:var(--code); border-radius:6px; }
h2 code { font-size:85%; }
pre { padding:16px; overflow:auto; font-size:85%; background:var(--code); border-radius:6px; line-height:1.45; }
pre code { padding:0; background:none; font-size:100%; white-space:pre; }
summary { cursor:pointer; margin-bottom:12px; }
hr { height:1px; border:0; background:var(--line); margin:24px 0; }
@media(max-width:600px) { nav { padding:0 16px; } article { border:0; border-radius:0; padding:16px; margin-top:8px; } }
</style>
</head>
<body>
<nav aria-label="Preview theme">
  <small>Local preview · GitHub-style layout</small>
  <button type="button" data-theme="auto" aria-pressed="true">Auto</button>
  <button type="button" data-theme="dark" aria-pressed="false">Dark</button>
  <button type="button" data-theme="light" aria-pressed="false">Light</button>
</nav>
<article class="markdown-body">
CONTENT
</article>
<script>
document.querySelectorAll('[data-theme]').forEach(button => {
  button.addEventListener('click', () => {
    const mode = button.dataset.theme;
    document.documentElement.dataset.mode = mode;
    document.querySelectorAll('picture source').forEach(source => {
      source.dataset.originalMedia ||= source.media;
      source.media = mode === 'auto' ? source.dataset.originalMedia :
        source.dataset.originalMedia.includes(mode) ? 'all' : 'not all';
    });
    document.querySelectorAll('[data-theme]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  });
});
</script>
</body>
</html>
'''


if __name__ == "__main__":
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    page = PAGE.replace("CONTENT", render((ROOT / "README.md").read_text(encoding="utf-8")))
    (docs / "preview.html").write_text(page, encoding="utf-8", newline="\n")
    print("Built docs/preview.html (offline preview).")
