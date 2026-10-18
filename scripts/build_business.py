"""business.html in the Uber for Business layout (scripts/content/business-source.html), rebranded for RESET.
Run after scripts/build_pages.py: it keeps that page's head, nav and footer and replaces the body blocks.
Uber's customer logos, named testimonial and survey statistic are not carried over (they would be false
claims for RESET); those slots hold RESET sectors, the RESET manifesto and a plain-language promise."""
import re, html
from paths import PUBLIC as ROOT, CONTENT
WM='<span class="rs-wm" role="img" aria-label="RESET"><span class="rs-vh">RESET</span></span>'
dom=open(CONTENT+'business-source.html').read()
starts=[m.start() for m in re.finditer(r'<div data-block-content-id="',dom)]
blocks=[]
for i,a in enumerate(starts):
    b=starts[i+1] if i+1<len(starts) else dom.index('</main>',a)
    blocks.append((re.search(r'data-block-id="([^"]*)"',dom[a:a+300]).group(1),dom[a:b]))

def clean(h):
    h=re.sub(r'<script[\s\S]*?</script>','',h)
    h=re.sub(r'<noscript[\s\S]*?</noscript>','',h)
    h=re.sub(r' data-(?:hydrate[a-z-]*|tracking-name|tracking|bits-testid)="[^"]*"','',h)
    h=re.sub(r'href="[^"]*"','href="#"',h)
    h=re.sub(r'<source\b[^>]*>','',h)
    h=re.sub(r' srcset="[^"]*"','',h)
    return h

# images per block, in order of appearance (by block index in the source)
IMG={1:['biz-hero.webp'],
     2:['biz-icon-money_bag.webp','biz-icon-clipboard.webp'], 3:['biz-icon-handshake.webp','biz-icon-key.webp'],
     4:['biz-use-offices.webp','biz-use-rentals.webp','biz-use-property.webp'],
     5:['biz-step-sites.webp','biz-step-team.webp','biz-step-dashboard.webp'],
     7:['biz-sector-office.webp','biz-sector-hotel.webp','biz-sector-classical_building.webp'],
     8:['biz-manifesto.webp'],
     10:['biz-guide-office.webp','biz-guide-rental.webp','biz-guide-vacate.webp']}
ALT={'biz-hero.webp':'A bright, empty office ready for the day','biz-use-offices.webp':'An office','biz-use-rentals.webp':'A made bed in a holiday rental',
     'biz-use-property.webp':'Keys being handed over','biz-step-sites.webp':'An office floor','biz-step-team.webp':'A RESET member making a bed',
     'biz-step-dashboard.webp':'The RESET app on a phone','biz-sector-office.webp':'Offices','biz-sector-hotel.webp':'Holiday rentals',
     'biz-sector-classical_building.webp':'Buildings and strata','biz-manifesto.webp':'Hands wringing a cloth over a bucket',
     'biz-guide-office.webp':'A RESET member cleaning a bright room','biz-guide-rental.webp':'Fresh flowers by a made bed','biz-guide-vacate.webp':'A couple moving in with a box'}
def imgs(h,files):
    it=iter(files)
    def sub(m):
        try: f=next(it)
        except StopIteration: return m.group(0)
        tag=re.sub(r'src="[^"]*"',f'src="assets/img/{f}"',m.group(0))
        tag=re.sub(r'alt="[^"]*"',f'alt="{ALT.get(f,"")}"',tag) if 'alt=' in tag else tag.replace('<img','<img alt="%s"'%ALT.get(f,''),1)
        return tag
    return re.sub(r'<img\b[^>]*>',sub,h)

# copy: exact or prefix match on text nodes ('' empties a node)
T=[
('The best of Uber for your business','One trusted team for every space you run'),
('Uber for Business gives your organisation','RESET for Business gives your offices, rentals and buildings one cleaning team. Plan, track and pay for every visit from one dashboard.'),
('How to get started','Talk to our team'),('Check out our solutions','See how it works'),
('A global platform built on','Everything your spaces need, in one place'),
('Achieve up to 10% cost savings','One plan, one price'),
('Customers have praised the reduction','Every site on a single plan and a single invoice. No chasing quotes from different cleaners.'),
('Meet sustainability goals','Track every visit live'),
('Track CO₂ emissions','See when your RESET team arrives, what is done room by room, and when they leave.'),
('Provide benefits to employees','The same faces on every visit'),
('Offer simplified expense reimbursement','Your team gets to know your spaces, so nothing gets missed and nothing needs explaining twice.'),
('Prioritise safety and security','Background-checked RESET members'),
('We offer additional crash-alert','Every RESET member is background-checked before their first visit. Keys and access codes are handled with care.'),
('US Safety Report',''),('shows that 99.9%',''),
('How companies leverage Uber for Business','How businesses use RESET'),
('Business travel','Offices'),('Courtesy rides','Holiday rentals'),('Meal programs','Property managers'),
('Get started with no upfront costs','Get started in three steps'),
('Customise your travel and meal programs','Tell us about your sites'),
('Set your own policies','Share your locations, their size and how often you need us. We put together one plan and one price.'),
('Onboard people at your own pace','Meet your RESET team'),
('Add individuals, specific teams','Background-checked RESET members, the same faces on every visit, briefed on each of your spaces.'),
('Set up amenities for customers','Manage everything in one dashboard'),
('Send Uber credit in the form of','Every visit, site and invoice in the RESET app. Change schedules, add sites and follow visits live.'),
('gift cards',''),('and',''),('vouchers',''),('for rides, meals and more',''),
('Join over 200,000 companies','Built for offices, rentals and buildings'),
("'Pay and basic benefits","‘When you hand your space to someone, you’re not buying an hour of cleaning. You’re buying the moment you walk in and everything is already done.’"),
('Ryan Carter','The RESET idea'),(', Founder and CEO',''),
('9 out of 10 customers recommend','One team. One plan. One invoice.'),
('Interested in learning more?','Guides for busy teams'),
('How to reduce the carbon footprint','How often should an office be cleaned?'),('See how','Read the guide'),
('The perks and benefits your employees','The holiday rental turnover checklist'),('Find out','Read the guide'),
('The road to sustainability','What a vacate clean should cover'),('Keep reading','Read the guide'),
('Product and feature availability','Service availability may vary by suburb. To find out more, talk to our team.'),
('here',''),('.',''),('¹Based on',''),('²Uber Electric',''),('³Based on',''),
]
def copy(h):
    used=set()
    def tn(m):
        raw=m.group(1); t=html.unescape(raw).strip()
        if not t: return m.group(0)
        for k,v in T:
            if t==k or (len(k)>6 and t.startswith(k)):
                used.add(k); return '>'+html.escape(v,quote=False)+'<'
        return m.group(0)
    parts=re.split(r'(<svg[\s\S]*?</svg>|<style[\s\S]*?</style>)',h)
    for i in range(0,len(parts),2): parts[i]=re.sub(r'>([^<>]+)<',tn,parts[i])
    return ''.join(parts), used

body=[]; used_all=set()
for idx,(bid,h) in enumerate(blocks):
    if bid in ('Navigation','Footer'): continue
    h=clean(h)
    if idx==8:   # testimonial video: keep the still, drop the player controls
        h=re.sub(r'<button\b[\s\S]*?</button>','',h); h=re.sub(r'<video[\s\S]*?</video>','',h)
    if idx in IMG: h=imgs(h,IMG[idx])
    h,u=copy(h); used_all|=u
    # the Uber-blue stat band becomes RESET black
    h=re.sub(r'background-color:\s*rgb\((\d+),\s*(\d+),\s*(\d+)\)',lambda m: m.group(0) if max(map(int,m.groups()))-min(map(int,m.groups()))<8 else 'background-color: rgb(26, 26, 26)',h)
    body.append(h)
missing=[k for k,_ in T if k not in used_all]
if missing: print('unmatched:',missing)
# wordmark for the name in running text
def wordmark(h):
    parts=re.split(r'(<svg[\s\S]*?</svg>)',h)
    for i in range(0,len(parts),2):
        parts[i]=re.sub(r'>([^<>]*RESET[^<>]*)<',lambda m:'>'+re.sub(r'\bRESET\b',WM,m.group(1))+'<',parts[i])
    return ''.join(parts)
body=wordmark(''.join(body))

page=open(ROOT+'business.html').read()
nav_start=page.index('data-block-id="Navigation"'); nav_start=page.rfind('<div',0,nav_start)
after_nav=page.index('<div data-block-content-id=',nav_start+10)
foot=page.index('data-block-id="Footer"'); foot=page.rfind('<div',0,foot)
page=page[:after_nav]+body+page[foot:]
if 'assets/css/business.css' not in page:
    page=page.replace('<link rel="stylesheet" href="assets/css/base.css">','<link rel="stylesheet" href="assets/css/base.css"><link rel="stylesheet" href="assets/css/business.css">',1)
for label,url in (('See how it works','book.html'),):
    page=re.sub(rf'(<a\b[^>]*?)href="#"([^>]*>(?:(?!</a>).)*?>{re.escape(label)}<)',rf'\1href="{url}"\2',page,flags=re.S)
open(ROOT+'business.html','w').write(page)
css=open(ROOT+'assets/css/business.css').read()
fix='''
/* RESET: business page fixes on top of Uber's layout */
h1.css-cgxnTe { white-space: normal; text-wrap: balance; max-width: 13ch; }
img.css-kqnRke { object-fit: contain; }
.css-ovtAW { background-color: #3B6CF0 !important; position: relative; overflow: hidden; }   /* the band is one of RESET's blue moments */
.css-ovtAW::after { content: ""; position: absolute; right: max(24px, calc(50% - 600px)); bottom: -6px; width: 170px; height: 189px; background: url("../img/arch/home-reset-bed.svg") no-repeat bottom / contain; pointer-events: none; }
@media (max-width: 899px) { .css-ovtAW::after { display: none; } }
.css-kEkqPW { display: none !important; }              /* video play overlay: the manifesto image is a still */
'''
css=css.split('\n/* RESET: business page fixes')[0]
open(ROOT+'assets/css/business.css','w').write(css+fix)
print('business.html written', len(page))
