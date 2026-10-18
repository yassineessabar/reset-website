"""Trim the homepage footer to pages that exist and link them. Idempotent; run before build_pages.py."""
import re
from paths import PUBLIC as ROOT, CONTENT
s=open(ROOT+'index.html').read()
a=s.index('data-block-id="Footer"'); a=s.rfind('<div',0,a); b=s.index('<div data-block-content-id=',a+10)
f=s[a:b]
TXT=lambda h: re.sub(r'<[^>]+>','',h).replace('\xa0',' ').strip()

def balanced(h, start, tag):
    depth=0
    for m in re.finditer(rf'<(/?){tag}\b[^>]*>',h[start:]):
        depth+= -1 if m.group(1) else 1
        if depth==0: return start+m.end()
    raise ValueError

def li_items(h):
    out=[]; pos=0
    while True:
        m=re.search(r'<li\b[^>]*>',h[pos:])
        if not m: return out
        st=pos+m.start(); en=balanced(h,st,'li'); out.append((st,en,h[st:en])); pos=en

KEEP={'About us':'about.html','Partners':'partners.html','Gift cards':'gift-cards.html',
      'Book':'book.html','RESET for Business':'business.html','Clean':'earn.html',
      'Privacy':'privacy.html','Accessibility':'accessibility.html','Terms':'terms.html',
      'Book a reset':'book.html','Apply to clean':'earn.html','Legal':'legal.html','Cookies':'cookies.html'}   # renamed labels, so re-runs keep them
RENAME={'Book':'Book a reset','Clean':'Apply to clean'}
# 1) list items: keep and link the useful ones, drop the rest (social icons too)
items=li_items(f)
for st,en,li in reversed(items):
    t=TXT(li)
    if t in ('English','Sydney'): continue                       # language and city chips stay
    if t in KEEP:
        new=re.sub(r'href="[^"]*"',f'href="{KEEP[t]}"',li,count=1)
        if t in RENAME: new=new.replace(f'>{t}<',f'>{RENAME[t]}<',1)
        f=f[:st]+new+f[en:]
    else:
        f=f[:st]+f[en:]
# 2) move "Apply to clean" from Products into Our commitments ("Work with us"); rename columns
f=f.replace('>Products<','>Services<').replace('>Our commitments<','>Work with us<')
m=re.search(r'<li\b[^>]*>(?:(?!</li>).)*?>Apply to clean<.*?</li>',f,re.S)
if m and f.find('>Work with us<')>m.start() and '<ul' in f[f.find('>Work with us<'):f.find('>Work with us<')+400]:
    li=m.group(0); f=f[:m.start()]+f[m.end():]
    w=f.index('>Work with us<'); ul=f.index('<ul',w); ul_end=f.index('>',ul)+1
    f=f[:ul_end]+li+f[ul_end:]
# 2b) Partners and Gift cards belong under Company, after About us
for label in ('Gift cards','Partners'):
    m=re.search(rf'<li\b[^>]*>(?:(?!</li>).)*?>{label}<.*?</li>',f,re.S)
    c=f.find('>Company<')
    if m and m.start()>f.find('>Services<')>c:
        li=m.group(0); f=f[:m.start()]+f[m.end():]
        about=re.search(r'<li\b[^>]*>(?:(?!</li>).)*?>About us<.*?</li>',f,re.S)
        f=f[:about.end()]+li+f[about.end():]
# 2c) legal row: add Cookies and Legal after Terms (cloned from Terms)
t=re.search(r'<li\b[^>]*>(?:(?!</li>).)*?terms\.html.*?</li>',f,re.S)
if t:
    for label,url in (('Legal','legal.html'),('Cookies','cookies.html')):
        if f'>{label}<' not in f:
            x=re.sub(r'href="[^"]*"',f'href="{url}"',t.group(0),count=1); x=re.sub(r'(<p\b[^>]*>).*?(</p>)',rf'\g<1>{label}\2',x,count=1,flags=re.S)
            t2=re.search(r'<li\b[^>]*>(?:(?!</li>).)*?terms\.html.*?</li>',f,re.S); f=f[:t2.end()]+x+f[t2.end():]
# 3) drop the emptied Hosts column and the Help Centre / "how the apps work" links
for label in ('Hosts',):
    i=f.find(f'>{label}</h2>')
    if i>0:
        col=f.rfind('<div',0,f.rfind('<div',0,i))   # column wrapper = two divs above the heading
        f=f[:col]+f[balanced(f,col,'div'):]
for label in ('Visit Help Centre','apps and website work'):
    m=re.search(rf'<a\b[^>]*>(?:(?!</a>).)*?{re.escape(label)}.*?</a>',f,re.S)
    if m: f=f[:m.start()]+f[m.end():]
# 4) the empty social list
f=re.sub(r'<ul\b[^>]*>\s*</ul>(?=\s*<ul\b[^>]*>\s*<li\b[^>]*>\s*<button)','',f,count=1)   # the empty social list, right before the language chips
# 5) logo goes home
f=re.sub(r'(<a\b[^>]*?)href="#"([^>]*>\s*<img[^>]*reset-logo-white)',r'\1href="index.html"\2',f,count=1)
s=s[:a]+f+s[b:]
open(ROOT+'index.html','w').write(s)
print('footer links:',[TXT(x) for x in re.findall(r'<a\b[^>]*href="[a-z-]+\.html"[^>]*>.*?</a>',f,re.S)])
