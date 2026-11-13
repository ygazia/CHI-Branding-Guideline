#!/usr/bin/env python3
"""Build the static CHI brand guidelines website from project/ into site/.

Usage:  pip install markdown && python3 build_site.py
Serve:  python3 -m http.server 8000 --directory site
"""
import html, json, re, shutil
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
SRC = ROOT / "project"
OUT = ROOT / "site"
T = json.loads((SRC / "tokens.json").read_text())
THEMES = [t["id"] for t in T["color"]["themes"]]
COLORS = {t["name"]: t for t in T["color"]["tokens"]}

PAGES = [  # slug, nav label, source, eyebrow
    ("index", "Overview", "README.md", "Brand guidelines"),
    ("foundation", "Brand foundation", "guide/01-brand-foundation.md", "01"),
    ("voice", "Voice and messaging", "guide/02-voice-and-messaging.md", "02"),
    ("logo", "Logo", "guide/03-logo.md", "03"),
    ("colour", "Colour", "guide/04-color.md", "04"),
    ("typography", "Typography", "guide/05-typography.md", "05"),
    ("imagery", "Imagery", "guide/06-imagery.md", "06"),
    ("applications", "Applications", "guide/07-applications.md", "07"),
    ("governance", "Governance", "guide/08-governance.md", "08"),
]
SUMMARY = {
    "foundation": "Origin, purpose, principles, audiences and how the lines fit under the master brand.",
    "voice": "How CHI sounds, what it says, and how to write names, numbers and trademarks.",
    "logo": "Versions, clear space, minimum size, backgrounds, misuse and downloads.",
    "colour": "The core three, proportion, the heat scale, contrast and the Salon Black theme.",
    "typography": "One family, two voices: heavy headlines and light capital descriptors.",
    "imagery": "Photography, graphic language, iconography and motion.",
    "applications": "Packaging, web, social, salon, stationery, advertising and partners.",
    "governance": "Approvals, claims, trademarks, accessibility, files and the release checklist.",
}
# component previews placed at the end of the named h2 section
EMBEDS = {
    "logo": {"Versions": ["LogoVersions"], "Minimum size": ["LogoClearSpace"], "Misuse": ["LogoMisuse"]},
    "colour": {"Proportion": ["ColorProportion"], "The heat scale": ["HeatScale"]},
    "applications": {
        "Website and e-commerce": ["Button", "ClaimBadge", "ProductCard"],
        "Social media": ["SocialPost"],
        "Stationery and documents": ["Stationery"],
    },
}
LOGO_FILES = [
    ("chi-mark-red.svg", "Mark, red", "white"), ("chi-mark-white.svg", "Mark, white", "red"),
    ("chi-mark-black.svg", "Mark, black", "white"), ("chi-infra-lockup-color.svg", "Line lockup, colour", "white"),
    ("chi-infra-lockup-reversed.svg", "Line lockup, reversed", "black"),
    ("chi-infra-lockup-white.svg", "Line lockup, white", "red"), ("chi-infra-lockup-black.svg", "Line lockup, black", "white"),
]


def resolve(name, theme, depth=0):
    v = COLORS[name]["value"]
    v = v if isinstance(v, str) else v.get(theme, v[THEMES[0]])
    m = re.fullmatch(r"\{(.+)\}", v)
    return resolve(m.group(1), theme, depth + 1) if m and depth < 16 else v


def tokens_css():
    def block(theme):
        return ";".join(f"--{n}:{resolve(n, theme)}" for n in COLORS)
    rest = [f"--{t['name']}:{t['value']}" for fam in ("spacing", "radius") for t in T[fam]["tokens"]]
    rest += [f"--font-{k}:{v}" for k, v in T["type"]["families"].items()]
    faces = "".join(
        f"@font-face{{font-family:\"{f['family']}\";src:url(\"{f['file']}\") format(\"woff2\");"
        f"font-weight:{f['weight']};font-style:{f.get('style', 'normal')};font-display:swap}}\n"
        for f in T["type"]["fonts"])
    styles = ""
    for g in T["type"]["groups"]:
        for s in g["styles"]:
            d = [f"font-family:var(--font-{g['family']})", f"font-size:{s['fontSize']}",
                 f"line-height:{s['lineHeight']}", f"font-weight:{s['fontWeight']}"]
            if "letterSpacing" in s:
                d.append(f"letter-spacing:{s['letterSpacing']}")
            styles += f".{s['name']}{{{';'.join(d)}}}\n"
    return (f"/* CHI Brand Guidelines: generated from tokens.json */\n{faces}"
            f":root,[data-theme=\"light\"]{{{block('light')};color-scheme:light}}\n"
            f"[data-theme=\"dark\"]{{{block('dark')};color-scheme:dark}}\n"
            f":root{{{';'.join(rest)}}}\n{styles}")


MARK = re.search(r"<g.*</g>", (SRC / "assets/Logos/chi-mark-red.svg").read_text(), re.S).group(0)
MARK = re.sub(r'fill="#[0-9A-Fa-f]{6}"', "", MARK)
MARK_SVG = f'<svg class="mark" viewBox="80.9 78.5 563.4 227" role="img" aria-label="CHI">{MARK}</svg>'


def embed(name):
    h = int(re.search(r"height=(\d+)", (SRC / f"components/{name}/preview.html").read_text()).group(1))
    return (f'<figure class="embed"><iframe src="previews/{name}.html" title="{name} live reference" '
            f'style="height:{h}px" loading="lazy"></iframe></figure>')


def swatch(name):
    t = COLORS[name]
    lv, dv = resolve(name, "light"), resolve(name, "dark")
    same = lv == dv
    hexes = (f'<button class="hex" type="button" data-copy="{lv.upper()}">{lv.upper()}</button>' if same else
             f'<button class="hex" type="button" data-copy="{lv.upper()}">{lv.upper()}<small>Light</small></button>'
             f'<button class="hex" type="button" data-copy="{dv.upper()}">{dv.upper()}<small>Salon Black</small></button>')
    chips = (f'<span class="chip" style="background:{lv}"></span>' if same else
             f'<span class="chip half" style="background:{lv}"></span><span class="chip half" style="background:{dv}"></span>')
    return (f'<li class="sw"><div class="chips">{chips}</div><div class="swt"><code>{name}</code>'
            f'<div class="hexes">{hexes}</div><p>{inline(t["usage"])}</p></div></li>')


def inline(text):
    return re.sub(r"`([^`]+)`", lambda m: code(m.group(1)), html.escape(text, quote=False))


def code(name):
    if name in COLORS:
        return f'<code class="tk"><i style="background:var(--{name})"></i>{name}</code>'
    return f"<code>{html.escape(name)}</code>"


def colour_tokens():
    groups = [("Core", ["chi-red", "chi-black", "chi-white"]),
              ("Brand roles", ["brand", "on-brand", "brand-strong", "brand-text", "brand-tint"]),
              ("Surfaces and ink", ["surface", "surface-raised", "surface-sunken", "ink", "ink-muted", "line", "line-strong", "focus"]),
              ("Silk and heat", ["silk", "on-silk", "heat-low", "heat-mid", "heat-high", "on-heat"]),
              ("Status", ["success", "caution", "error"])]
    out = '<section class="block"><h2 id="all-tokens">All colour tokens</h2><p>Select a value to copy it.</p>'
    for title, names in groups:
        out += f'<h3>{title}</h3><ul class="swatches">{"".join(swatch(n) for n in names)}</ul>'
    return out + "</section>"


def type_specimens():
    out = '<div class="specimens">'
    for g in T["type"]["groups"]:
        for s in g["styles"]:
            caps = ' style="text-transform:uppercase"' if s["name"].startswith("descriptor") else ""
            meta = f"{s['fontSize'].replace('px', '')} / {s['lineHeight'].replace('px', '')} · {s['fontWeight']}"
            out += (f'<div class="spec"><div class="specm"><code>{s["name"]}</code><span>{meta}</span></div>'
                    f'<p class="{s["name"]} specs"{caps}>{html.escape(s["sample"])}</p></div>')
    return out + "</div>"


def logo_downloads():
    out = ('<section class="block"><h2 id="downloads">Downloads</h2><p>Vector artwork, cropped tight to the letters. '
           'Add 1X of clear space when placing it.</p><ul class="dl">')
    for f, label, ground in LOGO_FILES:
        out += (f'<li><a href="assets/logos/{f}" download><span class="dlp g-{ground}"><img src="assets/logos/{f}" alt="{label}"></span>'
                f'<b>{label}</b><small>{f}</small></a></li>')
    return out + "</ul></section>"


def render_md(slug, src):
    text = (SRC / src).read_text()
    text = text.split("\n## Where to find things")[0]
    text = re.sub(r"^# .*\n", "", text, count=1)
    text = text.replace(" in Components.", " below.").replace(" in Components", " below")
    text = text.replace("the artwork in **Logos**", "the supplied logo artwork").replace("artwork from **Logos**", "artwork")
    body = markdown.markdown(text, extensions=["tables", "sane_lists"])
    body = re.sub(r"<code>([^<]+)</code>", lambda m: code(html.unescape(m.group(1))), body)
    body = re.sub(r"<li>\[ \] ", '<li class="check"><input type="checkbox" aria-label="Done"> ', body)
    body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    if slug == "index":
        return body
    # split on h2 so embeds can follow their section
    parts = re.split(r"(?=<h2>)", body)
    out = ""
    for p in parts:
        m = re.match(r"<h2>(.*?)</h2>", p)
        if not m:
            out += f'<div class="intro">{p}</div>' if p.strip() else ""
            continue
        title = re.sub(r"<[^>]+>", "", m.group(1))
        sid = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        p = p.replace("<h2>", f'<h2 id="{sid}">', 1)
        extra = "".join(embed(n) for n in EMBEDS.get(slug, {}).get(title, []))
        if slug == "typography" and title == "The scale":
            extra = type_specimens()
        if slug == "colour" and title == "The core three":
            extra = f'<ul class="swatches core">{"".join(swatch(n) for n in ("chi-red", "chi-black", "chi-white"))}</ul>'
        out += f'<section class="block">{p}{extra}</section>'
    if slug == "colour":
        out += colour_tokens()
    if slug == "logo":
        out += logo_downloads()
    return out


def page(i):
    slug, label, src, eyebrow = PAGES[i]
    href = lambda s: "index.html" if s == "index" else f"{s}.html"
    nav = "".join(
        f'<a href="{href(s)}"{" aria-current=\"page\"" if s == slug else ""}><span>{e if s != "index" else "00"}</span>{l}</a>'
        for s, l, _, e in PAGES)
    body = render_md(slug, src)
    if slug == "index":
        intro, rest = body.split("<h2>", 1)
        lead = re.sub(r"</?p>", "", intro).strip()
        cards = "".join(
            f'<a class="card" href="{href(s)}"><span class="descriptor-s">{e}</span><b>{l}</b><p>{SUMMARY[s]}</p></a>'
            for s, l, _, e in PAGES[1:])
        main = f'''<section class="hero"><div class="herot"><p class="eyebrow">Brand guidelines · Draft 1.0</p>
<h1>Heavy and light.<br>Heat and care.</h1><p class="lead">{lead}</p>
<p class="heroa"><a class="btn pri" href="logo.html">Get the logo</a><a class="btn sec" href="foundation.html">Start reading</a></p></div>
<div class="herop" aria-hidden="true"><div class="hp-red">{MARK_SVG}</div><div class="hp-ink"><i></i><i></i><i></i></div><div class="hp-silk"></div></div></section>
<div class="prose"><h2>{rest}</div>
<section class="block"><h2>Sections</h2><div class="cards">{cards}</div></section>'''
    else:
        main = f'<header class="ph"><p class="eyebrow">{eyebrow} · {SUMMARY[slug]}</p><h1>{label}</h1></header><div class="prose">{body}</div>'
    prev = f'<a class="pn" href="{href(PAGES[i-1][0])}"><small>Previous</small>{PAGES[i-1][1]}</a>' if i else "<span></span>"
    nxt = f'<a class="pn nx" href="{href(PAGES[i+1][0])}"><small>Next</small>{PAGES[i+1][1]}</a>' if i + 1 < len(PAGES) else "<span></span>"
    title = "CHI Brand Guidelines" if slug == "index" else f"{label} · CHI Brand Guidelines"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script>(function(){{var t;try{{t=localStorage.getItem("chi-theme")}}catch(e){{}}if(!t)t=matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";document.documentElement.dataset.theme=t}})();</script>
<link rel="icon" href="assets/favicon.svg">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
<a class="home" href="index.html" aria-label="CHI Brand Guidelines, home">{MARK_SVG}<span>Brand guidelines</span></a>
<button class="theme" type="button" id="theme" aria-label="Switch theme"><span class="tl">Salon Black</span></button>
</header>
<div class="shell">
<nav class="side" aria-label="Sections">{nav}</nav>
<main id="main">
{main}
<nav class="pager" aria-label="Previous and next">{prev}{nxt}</nav>
<footer class="foot"><p>CHI® is a registered trademark of Farouk Systems, Inc. Draft 1.0 of proposed guidelines, pending brand approval.</p></footer>
</main>
</div>
<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>
<script src="site.js"></script>
</body>
</html>
'''


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "previews").mkdir(parents=True)
    (OUT / "assets/logos").mkdir(parents=True)
    shutil.copytree(SRC / "fonts", OUT / "fonts")
    for f, _, _ in LOGO_FILES:
        shutil.copy(SRC / "assets/Logos" / f, OUT / "assets/logos" / f)
    (OUT / "assets/favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#D9212D"/>'
        '<rect x="14" y="14" width="10" height="36" fill="#fff"/><rect x="27" y="14" width="10" height="36" fill="#fff"/>'
        '<rect x="40" y="14" width="10" height="36" fill="#fff"/></svg>')
    (OUT / "tokens.css").write_text(tokens_css())
    shutil.copy(ROOT / "site_src/site.css", OUT / "site.css")
    shutil.copy(ROOT / "site_src/site.js", OUT / "site.js")
    inject = ('<head><link rel="stylesheet" href="../tokens.css"><script>try{document.documentElement.dataset.theme='
              'parent.document.documentElement.dataset.theme||"light"}catch(e){}</script>')
    for d in sorted((SRC / "components").iterdir()):
        if d.name == "Cover":
            continue
        h = (d / "preview.html").read_text().split("\n", 1)[1].replace("<head>", inject, 1)
        (OUT / "previews" / f"{d.name}.html").write_text(h)
    for i, (slug, *_r) in enumerate(PAGES):
        (OUT / f"{slug}.html").write_text(page(i))
    print("built", len(PAGES), "pages into", OUT)


if __name__ == "__main__":
    build()
