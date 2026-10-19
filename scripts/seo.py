"""SEO pass for index.html. Idempotent: run it last, after the other tools, and again whenever index.html is rebuilt.

    python3 scripts/seo.py

What it does
- <head>: keyword title and description (home cleaning, Sydney), en-AU, robots, theme colour, Open Graph and
  Twitter cards, apple-touch-icon, hero image preload, JSON-LD (WebSite, Organization, local cleaning business
  with its six services and Sydney as the service area). Everything sits between <!-- seo:start/end --> markers.
- One h1: the hero is in the page three times (desktop, tablet, phone); the extra copies become <p>.
- Menu and dialog titles (drawer, language picker) stop being h2s, so the outline is the page's real sections.
- The RESET wordmark inside headings gets real text, so "Earn with" reads "Earn with RESET" to search engines.
- Image alt text for every photo, lazy loading below the fold, only the hero marked high priority.
- WebP copies of every PNG/JPG render in design/renders, written to public/assets/img (the page drops from ~11 MB of images to a fraction),
  and the page points at them. The PNG/JPG originals stay, so build_assets.py keeps working unchanged.
- robots.txt, plus sitemap.xml and canonical/og:url once SITE_URL is set.
"""
import json, os, re
from PIL import Image, ImageDraw, ImageFont

# The live address. Canonical, og:url, absolute image URLs and sitemap.xml are written from it.
SITE_URL = os.environ.get("SITE_URL", "https://www.resetcleaning.app").rstrip("/")

from paths import PUBLIC as ROOT, RENDERS as OUT, IMG, FONTS
PAGE = os.path.join(ROOT, "index.html")

TITLE = "Home Cleaning Sydney | Book a Cleaner Online | RESET"
DESCRIPTION = ("Home cleaning in Sydney, booked online in minutes. Vetted cleaners for regular, deep, "
               "move in/out and holiday rental cleans. Come home to done.")
OG_IMAGE = "assets/img/og-image.jpg"
SERVICES = [
    ("Reset", "A full clean, top to bottom. Book it, head out, come home to done."),
    ("Recurring cleaning", "Weekly or every two weeks. Set it once and we take it from there."),
    ("Holiday rental cleaning", "Quick turnovers between guests, with fresh linen on every bed."),
    ("Move in / move out cleaning", "A deep clean for the day you hand back the keys, or pick them up."),
    ("Deep cleaning", "Every corner, cupboard and surface. For when a regular clean isn't enough."),
    ("Linen and laundry", "We wash, fold and remake every bed."),
]
# Photos that had no description (Uber marked them decorative; for us they are content)
ALTS = {
    "step-1-book": "Booking a home clean on the RESET app",
    "step-2-matched": "A RESET member cleaning a bright living room",
    "step-3-keys": "Handing over house keys before a clean",
    "step-4-reset": "A RESET member mopping the floor while the owner is out",
    "step-5-note": "A thank-you note left on the table after the clean",
    "more-moving": "A couple carrying a box into their new home on moving day",
    "more-hosting": "A bright living room ready for the next guests",
    "banner-bucket": "A woman reading by the window in her clean, quiet home",
    "earn-team": "A RESET team member making a bed",
    "earn-flexible": "Plumping cushions on a sofa, cleaning on your own schedule",
    "app-icon-reset": "RESET app icon",
    "app-icon-team": "RESET Team app icon",
    "qr-reset": "QR code to download the RESET app",
    "qr-team": "QR code to download the RESET Team app",
}
HERO = "hero-collage"


def make_webp():
    """WebP in public/assets/img for every render a page uses (rebuilt when the render is newer)."""
    done = []
    pages = "".join(open(os.path.join(ROOT, p)).read() for p in os.listdir(ROOT) if p.endswith(".html"))
    for f in sorted(os.listdir(OUT)):
        stem, ext = os.path.splitext(f)
        if ext not in (".png", ".jpg") or f.startswith("og-image"):
            continue
        src, dst = os.path.join(OUT, f), os.path.join(IMG, stem + ".webp")
        if not os.path.exists(dst) and f"assets/img/{stem}." not in pages:
            continue  # a render no page uses
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            im = Image.open(src)
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
            if im.width > 1600:  # shown at most ~800 CSS px wide; 2x is plenty
                im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            im.save(dst, "WEBP", quality=80, method=6)
        done.append(f)
    return done


def make_og_image():
    """1200x630 share card: headline left on ink, the made-bed photo right, wordmark."""
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), (14, 14, 14))
    photo = Image.open(os.path.join(OUT, "card-linen.jpg")).convert("RGB")
    pw = 560
    scale = max(pw / photo.width, H / photo.height)
    photo = photo.resize((round(photo.width * scale), round(photo.height * scale)), Image.LANCZOS)
    l, t = (photo.width - pw) // 2, (photo.height - H) // 2
    card.paste(photo.crop((l, t, l + pw, t + H)), (W - pw, 0))
    d = ImageDraw.Draw(card)
    font = os.path.join(FONTS, "InterTight-var.ttf")
    big = ImageFont.truetype(font, 64)
    try:
        big.set_variation_by_axes([700])
    except Exception:
        pass
    small = ImageFont.truetype(font, 30)
    d.text((64, 250), "Home cleaning", font=big, fill=(255, 255, 255), anchor="ls")
    d.text((64, 330), "in Sydney.", font=big, fill=(163, 163, 163), anchor="ls")
    d.text((64, 400), "Book online. Come home to done.", font=small, fill=(220, 220, 220), anchor="ls")
    logo = os.path.join(OUT, "_og_logo.png")
    os.system(f"rsvg-convert -w 170 '{os.path.join(ROOT, 'assets/img/brand/reset-logo-white.svg')}' -o '{logo}'")
    if os.path.exists(logo):
        lg = Image.open(logo).convert("RGBA")
        card.paste(lg, (64, H - lg.height - 64), lg)
        os.remove(logo)
    card.save(os.path.join(ROOT, OG_IMAGE), quality=88, optimize=True, progressive=True)


def absolute(path):
    return f"{SITE_URL}/{path}" if SITE_URL else path


def head_block():
    org = {"@type": "Organization", "@id": "#org", "name": "RESET", "slogan": "Nothing left to think about."}
    business = {
        "@type": "HomeAndConstructionBusiness", "@id": "#business", "name": "RESET",
        "description": DESCRIPTION,
        "slogan": "Home, sorted.",
        "areaServed": {"@type": "City", "name": "Sydney",
                       "containedInPlace": {"@type": "State", "name": "New South Wales",
                                            "containedInPlace": {"@type": "Country", "name": "Australia"}}},
        "knowsLanguage": "en-AU",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Home cleaning services",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {
                                "@type": "Service", "name": n, "description": t, "serviceType": "House cleaning",
                                "areaServed": "Sydney NSW"}} for n, t in SERVICES]},
        "parentOrganization": {"@id": "#org"},
    }
    site = {"@type": "WebSite", "@id": "#website", "name": "RESET", "inLanguage": "en-AU",
            "publisher": {"@id": "#org"}}
    if SITE_URL:
        for node in (org, business, site):
            node["@id"] = SITE_URL + "/" + node["@id"]
            node["url"] = SITE_URL + "/"
        org["logo"] = absolute("assets/img/app-icon-reset.png")
        business["image"] = absolute(OG_IMAGE)
        business["parentOrganization"] = {"@id": org["@id"]}
        site["publisher"] = {"@id": org["@id"]}
    graph = {"@context": "https://schema.org", "@graph": [site, org, business]}

    tags = [
        f"<title>{TITLE}</title>",
        f'<meta name="description" content="{DESCRIPTION}">',
        '<meta name="robots" content="index, follow, max-image-preview:large">',
        '<meta name="theme-color" content="#0E0E0E">',
        '<meta name="format-detection" content="telephone=no">',
        '<meta name="geo.region" content="AU-NSW"><meta name="geo.placename" content="Sydney">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="RESET">',
        '<meta property="og:locale" content="en_AU">',
        f'<meta property="og:title" content="{TITLE}">',
        f'<meta property="og:description" content="{DESCRIPTION}">',
        f'<meta property="og:image" content="{absolute(OG_IMAGE)}">',
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="Home cleaning in Sydney. Book online. Come home to done.">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{TITLE}">',
        f'<meta name="twitter:description" content="{DESCRIPTION}">',
        f'<meta name="twitter:image" content="{absolute(OG_IMAGE)}">',
        '<link rel="apple-touch-icon" href="assets/img/app-icon-reset.png">',
        f'<link rel="preload" as="image" href="assets/img/{HERO}.webp" type="image/webp" fetchpriority="high">',
        # the two faces every heading and paragraph uses; without this they arrive after the CSS and repaint the page
        '<link rel="preload" as="font" type="font/woff2" href="assets/fonts/inter-tight-latin.woff2" crossorigin>',
        '<link rel="preload" as="font" type="font/woff2" href="assets/fonts/inter-latin.woff2" crossorigin>',
    ]
    if SITE_URL:
        tags += [f'<link rel="canonical" href="{SITE_URL}/">', f'<meta property="og:url" content="{SITE_URL}/">']
    tags.append('<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False) + "</script>")
    return "<!-- seo:start -->" + "".join(tags) + "<!-- seo:end -->"


def update_page(webp_sources):
    s = open(PAGE).read()

    # head: drop the old title/description and any previous SEO block, then add ours after the viewport tag
    s = re.sub(r"<!-- seo:start -->.*?<!-- seo:end -->", "", s, flags=re.S)
    head_end = s.index("</head>")
    head = re.sub(r"<title>.*?</title>|<meta name=\"description\"[^>]*>", "", s[:head_end], flags=re.S)
    head = re.sub(r'(<meta name="viewport"[^>]*>)', lambda m: m.group(1) + head_block(), head, count=1)
    s = head + s[head_end:]
    s = re.sub(r'<html lang="[^"]*">', '<html lang="en-AU">', s, count=1)

    # one h1: keep the first hero copy, the responsive duplicates become <p> with the same look
    h1s = list(re.finditer(r"<h1(\s[^>]*)?>(.*?)</h1>", s, re.S))
    for m in reversed(h1s[1:]):
        attrs = (m.group(1) or "")
        if "data-rs-headline" not in attrs:
            attrs += " data-rs-headline"
        s = s[:m.start()] + f"<p{attrs}>{m.group(2)}</p>" + s[m.end():]
    if h1s and "data-rs-headline" not in (h1s[0].group(1) or ""):
        s = s.replace(h1s[0].group(0), h1s[0].group(0).replace("<h1", "<h1 data-rs-headline", 1), 1)

    # menu drawers and the language dialog: titles, not page sections
    s = re.sub(r'<h2( data-baseweb="typo-(?:headingxlarge|displayxsmall)"[^>]*)>(.*?)</h2>',
               r'<div role="presentation"\1>\2</div>', s, flags=re.S)

    # the wordmark in headings gets real text (visually hidden; it is exactly what the logo says)
    s = re.sub(r'<span class="rs-wm" role="img" aria-label="RESET"></span>',
               '<span class="rs-wm" role="img" aria-label="RESET"><span class="rs-vh">RESET</span></span>', s)

    # images: alt text, priority only for the hero, lazy loading for the rest
    def fix_img(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]*)"', tag)
        if not src:
            return tag
        stem = os.path.splitext(os.path.basename(src.group(1)))[0]
        if stem.startswith("product-"):  # 3D icon next to its own caption: decorative, the caption is the text
            tag = re.sub(r'\salt="[^"]*"', ' alt=""', tag)
        if stem in ALTS:
            tag = re.sub(r'\salt="[^"]*"', f' alt="{ALTS[stem]}"', tag)
            tag = re.sub(r'\s(aria-hidden="true"|role="presentation")', "", tag)
        if stem == HERO or stem.startswith("reset-logo"):  # above the fold: never lazy
            return re.sub(r'\s(loading="lazy"|decoding="async")', "", tag)
        tag = re.sub(r'\s(fetchpriority="high"|loading="eager")', "", tag)
        if "loading=" not in tag:
            tag = tag.replace("<img", '<img loading="lazy" decoding="async"', 1)
        return tag
    s = re.sub(r"<img\b[^>]*>", fix_img, s)

    # point the page at the WebP copies (src and srcset); the head keeps PNG/JPG for icons and share cards
    a, b = s.index("<!-- seo:end -->"), s.index("</head>")
    body = s[b:]
    for f in webp_sources:
        body = body.replace(f"assets/img/{f}", "assets/img/" + os.path.splitext(f)[0] + ".webp")
    s = s[:b] + body

    open(PAGE, "w").write(s)
    return s


def write_robots_and_sitemap():
    robots = "User-agent: *\nAllow: /\n"
    if SITE_URL:
        robots += f"\nSitemap: {SITE_URL}/sitemap.xml\n"
        open(os.path.join(ROOT, "sitemap.xml"), "w").write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"  <url><loc>{SITE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n"
            + "".join(f"  <url><loc>{SITE_URL}/{f}</loc></url>\n" for f in sorted(os.listdir(ROOT))
                      if f.endswith(".html") and f != "index.html")
            + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(robots)


if __name__ == "__main__":
    make_og_image()
    sources = make_webp()
    page = update_page(sources)
    write_robots_and_sitemap()
    print(f"seo: {len(sources)} images as WebP, h1={page.count('<h1')}, "
          f"h2={page.count('<h2')}, SITE_URL={'set' if SITE_URL else 'not set (canonical/sitemap skipped)'}")
