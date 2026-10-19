# RESET website

Marketing site for RESET, home cleaning in Sydney. It's a static site: plain HTML, CSS and a little JavaScript, with no framework and no build step needed to serve it.

```sh
make serve          # http://localhost:8768
```

(Or point any static host or server at `public/`, e.g. `python3 -m http.server 8768 -d public`.)

## Repository layout

```
public/                  The deployable site. Point the host at this folder.
  *.html                 Home, Book, Earn, Business, About, Partners, Gift cards, legal pages
  robots.txt
  assets/
    css/                 base.css (layout system), site.css (brand layer, motion), pages.css (subpages),
                         business.css (Business page), fonts.css
    js/                  motion.js (wipes, carousels), book.js, apply.js, forms.js
    fonts/               Inter and Inter Tight (woff2, latin + latin-ext)
    img/                 Page images (WebP); brand/ logo, app/ app screens, arch/ illustrations,
                         menu/ and icons/ small 3D icons, ui/ store badges and layout images
scripts/                 Python build scripts (see Build)
  content/               Hand-written sections and legal copy the pages are built from
  legacy/                One-shot migration scripts, kept as a record and not run anymore
design/                  Source material, never served
  photos/                Full-size source photos (credits in design/CREDITS.md)
  renders/               PNG/JPG renders the WebPs are made from
  scenes/ masks/ icons/ glyphs/ fonts/ logo/
```

## Pages

| Page | What it is |
|---|---|
| `index.html` | Homepage: hero, services, how to book, More ways, the app, FAQ |
| `book.html` | Booking flow: address, size, timing, then options, then a "You're set." confirmation (logic in `book.js`) |
| `earn.html` | Cleaner application form, then how it works and FAQ (`apply.js`) |
| `business.html` | RESET for Business |
| `about.html`, `partners.html`, `gift-cards.html` | Company pages; the forms use `forms.js` |
| `legal.html` + 8 documents | Privacy, Terms, Accessibility, Cookies, Refunds, Gift card terms, Member terms, Complaints |

## Build

Python 3.10+ with `pip install -r requirements.txt`, plus `cwebp` and `rsvg-convert` (`brew install webp librsvg`).

```sh
make pages     # footer, app section, subpages, business page, SEO pass, then link check
make images    # illustrations and the bright step / More ways photos
make check     # every referenced file exists, no unused assets
```

`index.html` is the source of truth for shared blocks (nav, footer, FAQ). `scripts/build_pages.py` composes the subpages from it and from `scripts/content/`, so edit the homepage or the content files and then run `make pages`. Every page script is idempotent, so running it twice gives the same output.

`scripts/seo.py` writes the meta tags, Open Graph, JSON-LD and WebP images. Canonical URLs and `sitemap.xml` use https://www.resetcleaning.app (override with `SITE_URL=...`).

`scripts/build_assets.py` regenerates the original composite photos. Run it only on purpose: it rewrites renders that the illustration and bright-photo scripts have since replaced.

## Design system

- **Interface:** black and white, on one monochrome ramp from ink `#0E0E0E` to white. Inter Tight for titles, Inter for text.
- **Blue `#3B6CF0`** (tint `#EAF0FE`), only for the moments that mean booked, done or you're set: the homepage "Book once" panel, the confirmations, the app showcase and the Business band. It is the RESET app's blue, used with its arch illustrations.
- **The name:** every "RESET" in running text is drawn in the wordmark's lettering (`.rs-wm`, a mask of the logo; screen readers still read "RESET"). Legal copy keeps it as plain text.
- **Photography:** real, bright, warm photos of people at home, in colour (Unsplash, credited in `design/CREDITS.md`).
- **Motion:** a wipe, the trail of a cloth. It's used for the hero reveal, photo reveals and the drip pattern. Everything is visible without JavaScript and static with reduced motion.

## Before launch

- **Backend:** forms (Earn, Partners, Gift cards) and the Book flow send nothing yet. Connect them to a backend before launch, and add payment for gift cards.
- **Prices:** Book shows `$ —` until pricing is set.
- **Legal:** the legal pages are drafts with bracketed placeholders and need a lawyer's review.
- **Claims:** service claims (vetting, insurance, member pricing) need confirming.
- **Layout origin:** the page layout and `base.css` are derived from Uber's public site, and `scripts/content/business-source.*` is a capture of Uber for Business. Rebuild these in RESET's own code before treating the site as production.

## Credits

Photos are from Unsplash (Unsplash License). The 3D icons are Microsoft Fluent Emoji (MIT). The fonts are Inter and Inter Tight (SIL OFL).
