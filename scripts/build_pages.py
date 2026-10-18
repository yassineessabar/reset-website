"""Build book.html, earn.html and business.html from index.html's own blocks, and wire the nav.

Each page = the homepage's head, nav and footer + a selection of its blocks with page-specific copy
and images, plus an FAQ. Re-run after editing index.html: pages always follow the homepage design.
"""
import re, html
from paths import PUBLIC as ROOT, CONTENT
WM = '<span class="rs-wm" role="img" aria-label="RESET"><span class="rs-vh">RESET</span></span>'
WM_ANY = re.compile(r'<span class="rs-wm" role="img" aria-label="RESET">(?:<span class="rs-vh">RESET</span>)?</span>')
NB = '\xa0'

src = open(ROOT + 'index.html').read()
starts = [m.start() for m in re.finditer(r'<div data-block-content-id="', src)]
ends = starts[1:] + [None]
blocks = {}
for i, (a, b) in enumerate(zip(starts, ends)):
    b = b if b is not None else src.index('</main>', a)
    bid = re.search(r'data-block-id="([^"]*)"', src[a:a + 300]).group(1)
    blocks.setdefault(bid, []).append(src[a:b])
head, tail = src[:starts[0]], src[src.index('</main>', starts[-1]):]
last = src[starts[-1]:src.index('</main>', starts[-1])]   # CROGuidedTour (menus); keep with the tail

def B(name, n=0):
    return blocks[name][n]

# ---------- text helpers (wordmark-aware) ----------
def flat(h): return WM_ANY.sub('RESET', h)

def wordmark(h):
    parts = re.split(r'(<title>.*?</title>|<style[\s\S]*?</style>|<svg[\s\S]*?</svg>|<script[\s\S]*?</script>)', h)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'>([^<>]*RESET[^<>]*)<', lambda m: '>' + re.sub(r'\bRESET\b', WM, m.group(1)) + '<', parts[i])
    return ''.join(parts)

def rewrite(h, T, imgs=None):
    h = flat(h); hit = set()
    def tn(m):
        raw = m.group(1); t = html.unescape(raw).strip()
        if t in T:
            hit.add(t)
            return '>' + raw[:len(raw) - len(raw.lstrip())] + html.escape(T[t], quote=False) + raw[len(raw.rstrip()):] + '<'
        return m.group(0)
    parts = re.split(r'(<svg[\s\S]*?</svg>)', h)
    for i in range(0, len(parts), 2): parts[i] = re.sub(r'>([^<>]+)<', tn, parts[i])
    h = ''.join(parts)
    h = re.sub(r'\b(alt|aria-label|label)="([^"]*)"',
               lambda m: f'{m.group(1)}="{html.escape(T[html.unescape(m.group(2)).strip()])}"' if html.unescape(m.group(2)).strip() in T else m.group(0), h)
    for a, b in (imgs or {}).items():   # swap by name, whatever the extension (the site serves .webp)
        sa, sb = a.rsplit('.', 1)[0], b.rsplit('.', 1)[0]
        h = re.sub(rf'assets/img/{re.escape(sa)}\.(?:png|webp|jpg)', f'assets/img/{sb}.webp', h)
    miss = [k for k in T if k not in hit]
    if miss: print('   unmatched:', miss[:6])
    return wordmark(h)

def to_h1(h):   # the page's first heading becomes its h1 (same classes, same look)
    return re.sub(r'<h2(\b[^>]*)>(.*?)</h2>', r'<h1\1>\2</h1>', h, count=1, flags=re.S)

# ---------- nav: real links + current page ----------
def nav(current):
    h = B('Navigation')
    h = re.sub(r'(data-testid="wcb3-navigation-logo"[^>]*?)href="[^"]*"', r'\1href="index.html"', h)
    h = re.sub(r'href="[^"]*"(?=[^>]*data-testid="wcb3-navigation-logo")', 'href="index.html"', h)
    for label, url in (('Book', 'book.html'), ('Earn', 'earn.html'), ('Business', 'business.html')):
        def fix(m, label=label, url=url):
            tag = m.group(0)
            tag = re.sub(r'href="[^"]*"', f'href="{url}"', tag)
            if label == current: tag = tag.replace('class="css-MDldu"', 'class="css-MDldu" aria-current="page"')
            return tag
        h = re.sub(rf'<a\b[^>]*class="css-MDldu"[^>]*>(?=\s*{label}\s*<)', fix, h)
    return h

# ---------- FAQ ----------
def faq(title, items):
    qa = ''.join(f'<details class="rs-faq-item"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in items)
    return wordmark(f'<section class="rs-faq" aria-labelledby="faq-title"><div class="rs-faq-inner"><h2 id="faq-title">{title}</h2>{qa}</div></section>')

CTAS = (('See prices', 'book.html'), ('Details', 'book.html'), ('Book ahead', 'book.html'), ('Book laundry', 'book.html'), ('Add linen', 'book.html'),
        ('Join now', 'book.html'), ('Apply to clean', 'earn.html'), ('See how it works', 'earn.html'), ('Learn more', 'business.html'),
        ('Schedule a reset', 'book.html'))
def link_ctas(h):
    for label, url in CTAS:
        h = re.sub(rf'(<a\b[^>]*?)href="#"([^>]*>(?:(?!</a>).)*?>{re.escape(label)}<)', rf'\1href="{url}"\2', h, flags=re.S)
    return h

ALTS = {'earn-hero.png': 'A smiling RESET member at work, with calendar, money and home icons below',
        'earn-why.png': 'A RESET member smoothing cushions in a bright living room'}
def set_alts(h):
    for f, alt in ALTS.items():
        st = re.escape(f.rsplit('.', 1)[0])
        h = re.sub(rf'(<img\b[^>]*src="assets/img/{st}\.\w+"[^>]*?)alt="[^"]*"', rf'\1alt="{alt}"', h)
        h = re.sub(rf'(<img\b[^>]*?)alt="[^"]*"([^>]*src="assets/img/{st}\.\w+")', rf'\1alt="{alt}"\2', h)
    return h

def page(name, title, desc, current, parts):
    h = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', head, count=1, flags=re.S)
    d = html.escape(desc)
    h = re.sub(r'(<meta name="description" content=")[^"]*(")', rf'\g<1>{d}\2', h)
    for k in ('og:title', 'twitter:title'):
        h = re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*(")', rf'\g<1>{html.escape(title)}\2', h)
    for k in ('og:description', 'twitter:description'):
        h = re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*(")', rf'\g<1>{d}\2', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', '', h, flags=re.S)   # the homepage's structured data stays on the homepage
    parts = [p.replace(' data-rs-headline', '') for p in parts]
    if 'reset/pages.css' not in h:
        extra = '<link rel="stylesheet" href="assets/css/pages.css">'
        if name == 'earn.html': extra += '<script src="assets/js/apply.js" defer></script>'
        if name in ('gift-cards.html', 'partners.html'): extra += '<script src="assets/js/forms.js" defer></script>'
        h = h.replace('</head>', extra + '</head>', 1)
    open(ROOT + name, 'w').write(set_alts(link_ctas(h + nav(current) + ''.join(parts) + B('Footer') + last + tail)))
    print('wrote', name)

# =====================================================================
# BOOK
# =====================================================================
print('book')
book = [
    rewrite(B('CROMapHero'), {'Home, sorted.': 'Book a reset.', 'Busy week ahead?': 'Need it sooner?'}),
    rewrite(B('CROProductSuggestions'), {'Explore what you can do with RESET': 'Choose your reset'}),
    B('BulletsCarousel', 0),
    rewrite(B('BulletsCarousel', 1), {'More ways to use RESET': 'Moving or hosting?'}),
    rewrite(B('ContentItems', 1), {'Get your laundry done': 'Add laundry', 'Fresh sheets, every visit': 'Add fresh linen'}),
    B('Highlight', 0),
    faq('Questions, answered', [
        ('How do I book a reset?', 'Enter your address and home size, pick a time and confirm. You see your price before you book.'),
        ('Who comes into my home?', 'A background-checked RESET member. You see their name and photo before they arrive.'),
        ('What do I do with my keys?', 'Leave a key or a door code. We return it the moment the visit is done.'),
        ('Can I change or pause my rhythm?', 'Yes. Change, pause or stop your recurring visits whenever you like, right from the RESET app.'),
        ('What if something isn’t right?', 'Tell us after your visit and we will come back to put it right.'),
    ]),
    B('MultiLink'),
]
# book.html is the standalone booking app (Uber Go layout), maintained by hand: not generated here
# page('book.html', 'Book a Home Clean in Sydney | RESET', 'Book a home clean in minutes. See your price, pick a time, and come home to done.', 'Book', book)

# =====================================================================
# EARN
# =====================================================================
print('earn')
earn_hero = to_h1(rewrite(B('Highlight', 1), {
    'All the benefits of RESET, reimagined for business': 'Clean when you want, earn what you need',
    'RESET for Business gives your offices, rentals and buildings one trusted cleaning team. Manage every site, visit and invoice from one dashboard.':
        'Clean homes near you, choose the visits that suit you, and get paid for every one.',
    'Learn more': 'Apply to clean',
}, {'business.png': 'earn-hero.png'}))
earn = [
    wordmark(open(CONTENT + 'earn-apply.html').read()),   # the application form (hand-written section)
    rewrite(B('BulletsCarousel', 0), {
        'How to book a reset': 'How to start earning',
        'Get started': 'Apply in the app',
        f'Enter your address in the RESET app, pick a time and{NB}confirm.': f'Download the RESET Team app and tell us where and when you want to{NB}work.',
        'Get matched with a RESET member': 'Get approved',
        f'A background-checked RESET member accepts your visit. You’ll see their name and photo before they{NB}arrive.': f'We check your ID and background, then show you how RESET{NB}works.',
        'Hand over your keys': 'Pick your visits',
        f'Leave a key or a door code. We return it the moment the visit is{NB}done.': f'Choose visits near you that fit your week. Accept the ones you{NB}want.',
        'Get on with your day': 'Reset the home',
        f'We reset your home room by room while you’re out. Follow along live in the{NB}app.': f'Follow the visit checklist room by room. We supply the{NB}kit.',
        'Come home to a note': 'Leave the note, get paid',
        f'“All done. You can breathe.” Rate your visit and add a tip if you{NB}like.': f'Leave “All done. You can breathe.” and get paid for the visit, tips{NB}included.',
    }),
    faq('Questions from future RESET members', [
        ('Do I need experience?', 'Experience helps, but it is not required. We show you how RESET works before your first visit.'),
        ('Do I need my own supplies?', 'No. We supply the kit you need for every visit.'),
        ('How do I choose when I work?', 'Go online in the RESET Team app and accept the visits that suit your week.'),
        ('How do I get paid?', 'You get paid for every visit you complete, tips included, straight to your account.'),
        ('What checks are there?', 'We confirm your identity and run a background check before your first visit.'),
    ]),
    B('MultiLink'),
]
page('earn.html', 'Cleaning Jobs in Sydney, On Your Schedule | RESET', 'Clean homes near you on your schedule. Choose your visits, we supply the kit, and you get paid for every one.', 'Earn', earn)

# =====================================================================
# BUSINESS
# =====================================================================
print('business')
biz_hero = to_h1(rewrite(B('Highlight', 1), {
    'All the benefits of RESET, reimagined for business': 'RESET for Business',
    'Learn more': 'Talk to our team',
}))
biz_grid = rewrite(B('CROProductSuggestions'), {
    'Explore what you can do with RESET': 'Built for every kind of space',
    'Reset': 'Offices',
    'A full clean, top to bottom. Book it, head out, come home to done.': 'Before your team arrives or after they leave. Daily, weekly or on demand.',
    'Recurring': 'Recurring contracts',
    'Weekly or every two weeks. Set it once and we take it from there.': 'One schedule across all your sites, managed for you.',
    'Holiday rental': 'Holiday rentals',
    'Quick turnovers between guests, with fresh linen on every bed.': 'Turnovers between every booking, linen included.',
    'Move in / out': 'Property managers',
    'A deep clean for the day you hand back the keys, or pick them up.': 'Vacate cleans and handovers across your whole portfolio.',
    'Deep reset': 'Buildings & strata',
    'Every corner, cupboard and surface. For when a regular clean isn’t enough.': 'Common areas, lobbies and lifts, on a set schedule.',
    'Linen & laundry': 'Retail & showrooms',
    'We wash, fold and remake every bed.': 'Floors and displays ready before you open.',
}, {'product-sponge.png': 'product-office.png', 'product-bed.png': 'product-hotel.png', 'product-package.png': 'product-key.png',
    'product-couch.png': 'product-classical_building.png', 'product-basket.png': 'product-shopping_bags.png'})
business = [
    biz_hero,
    biz_grid,
    rewrite(B('BulletsCarousel', 0), {
        'How to book a reset': 'How RESET for Business works',
        'Get started': 'Tell us about your sites',
        f'Enter your address in the RESET app, pick a time and{NB}confirm.': f'Share your locations, size and how often you need{NB}us.',
        'Get matched with a RESET member': 'Get your plan',
        f'A background-checked RESET member accepts your visit. You’ll see their name and photo before they{NB}arrive.': f'We put together one plan and one price for every{NB}site.',
        'Hand over your keys': 'Meet your team',
        f'Leave a key or a door code. We return it the moment the visit is{NB}done.': f'Background-checked RESET members, the same faces on every{NB}visit.',
        'Get on with your day': 'We reset on schedule',
        f'We reset your home room by room while you’re out. Follow along live in the{NB}app.': f'Every visit is tracked live, room by room, site by{NB}site.',
        'Come home to a note': 'One invoice',
        f'“All done. You can breathe.” Rate your visit and add a tip if you{NB}like.': f'Every site, visit and invoice in one{NB}dashboard.',
    }),
    faq('Questions from businesses', [
        ('What kinds of businesses do you work with?', 'Offices, holiday rentals, property managers, buildings and strata, retail and showrooms.'),
        ('Can you manage several sites?', 'Yes. One plan, one team contact and one invoice across all your locations.'),
        ('Who does the work?', 'Background-checked RESET members, with the same faces on every visit wherever possible.'),
        ('How do I get a quote?', 'Talk to our team with your sites and how often you need us, and we will come back with one plan and one price.'),
    ]),
]
page('business.html', 'Commercial Cleaning for Offices and Rentals in Sydney | RESET for Business', 'One trusted cleaning team for your offices, rentals and buildings. Every site, visit and invoice in one dashboard.', 'Business', business)

# =====================================================================
# ABOUT, GIFT CARDS, PARTNERS
# =====================================================================
def section_src(n): return wordmark(open(CONTENT + '' + n).read())
page('about.html', 'About RESET | Home Cleaning in Sydney', 'RESET doesn\u2019t sell cleaning. We give you back the pleasure of coming home. Meet the home cleaning company built around one moment.', None,
     [section_src('about.html')])
page('gift-cards.html', 'RESET Gift Cards | Give a Home Clean in Sydney', 'Give someone their weekend back. RESET gift cards go towards any home clean in Sydney, sent by email.', None,
     [section_src('gift-cards.html'), faq('Gift card questions', [
        ('How long is a gift card valid?', 'At least three years from the date you buy it, as Australian law requires.'),
        ('What can it be used for?', 'Any reset: a one-off clean, a deep reset, a move in or out, or recurring visits until the balance runs out.'),
        ('Can I choose when it arrives?', 'Yes. Send it now, tomorrow or on a date you choose, with your own message.'),
        ('Can a gift card be refunded?', 'Gift cards cannot be exchanged for cash, except where the law requires it.')])])
page('partners.html', 'Partner with RESET | Cleaning for Property Managers and Hosts in Sydney', 'One trusted cleaning team for property managers, real estate agents, strata managers and short-stay hosts across Sydney.', None,
     [section_src('partners.html'), faq('Partner questions', [
        ('What does a partnership include?', 'One contact for all your properties, vacate and turnover cleans booked in minutes, every visit tracked, and one monthly invoice.'),
        ('Do you work across Sydney?', 'Tell us your suburbs in the form and we will confirm what we can cover.'),
        ('Who does the work?', 'Background-checked RESET members, with the same faces on repeat visits wherever possible.')])])

# =====================================================================
# LEGAL: privacy, terms, accessibility (drafts, see scripts/content/legal.py)
# =====================================================================
import importlib.util
spec = importlib.util.spec_from_file_location('legal', CONTENT + 'legal.py'); legal = importlib.util.module_from_spec(spec); spec.loader.exec_module(legal)
def doc(key):
    d = legal.PAGES[key]
    toc = ''.join(f'<li><a href="#s{i}">{html.escape(t)}</a></li>' for i, (t, _) in enumerate(d['sections']))
    body = ''
    for i, (t, parts) in enumerate(d['sections']):
        body += f'<h2 id="s{i}">{html.escape(t)}</h2>'
        for part in parts:
            body += ('<ul>' + ''.join(f'<li>{html.escape(x)}</li>' for x in part[1]) + '</ul>') if isinstance(part, tuple) else f'<p>{html.escape(part)}</p>'
    cur = ' aria-current="page"'
    others = '<a href="legal.html">All legal</a>' + ''.join(f'<a href="{k}.html"{cur if k == key else ""}>{legal.PAGES[k]["title"]}</a>' for k in legal.PAGES)
    # legal text keeps the name as plain words (company name, defined terms): no wordmark here
    return (f'''<section class="rs-doc-head"><div class="rs-wrap"><nav class="rs-doc-tabs" aria-label="Legal">{others}</nav>
<h1>{d["title"]}</h1><p class="rs-doc-meta">Last updated {legal.UPDATED}</p></div></section>
<section class="rs-doc"><div class="rs-wrap rs-doc-grid"><aside class="rs-doc-toc" aria-label="On this page"><p>On this page</p><ol>{toc}</ol></aside>
<article class="rs-doc-body"><p class="rs-doc-draft">Draft for review. Bracketed details are placeholders and this page will be checked by a lawyer before launch.</p><p class="rs-doc-intro">{html.escape(d["intro"])}</p>{body}</article></div></section>''')
for key in legal.PAGES:
    d = legal.PAGES[key]
    page(f'{key}.html', f'{d["title"]} | RESET', d['meta'], None, [doc(key)])
# the legal hub: every document, one line each
cards = ''.join(f'<li><a href="{k}.html"><h2>{html.escape(d["title"])}</h2><p>{html.escape(d["summary"])}</p><span aria-hidden="true">→</span></a></li>' for k, d in legal.PAGES.items())
hub = (f'<section class="rs-doc-head"><div class="rs-wrap"><h1>Legal</h1><p class="rs-doc-meta">Everything that governs how RESET works, in plain English. Last updated {legal.UPDATED}.</p></div></section>'
       f'<section class="rs-doc"><div class="rs-wrap"><ul class="rs-legal-grid">{cards}</ul></div></section>')
page('legal.html', 'Legal | RESET', 'RESET\u2019s legal documents: privacy, terms, cookies, cancellations and refunds, gift cards, member terms, complaints and accessibility.', None, [hub])

# =====================================================================
# Home: same nav wiring + key CTAs point at the new pages
# =====================================================================
home = src
a = home.index('data-block-id="Navigation"'); a = home.rfind('<div', 0, a); b = home.index('<div data-block-content-id=', a + 10)
home = home[:a] + nav(None) + home[b:]
home = link_ctas(home)
open(ROOT + 'index.html', 'w').write(home)
print('index wired')
