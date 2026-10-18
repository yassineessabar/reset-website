"""Add RESET's live pieces to index.html (idempotent):
- the linen banner as an inline SVG drip panel (pills grow in with JS, static without it)
- an inline SVG drip band at the top of the footer
- the hero check pills as real HTML over the collage
- motion.js
"""
import re, random
P='public/index.html'
s=open(P).read()
INDIGO='#223961'; INDIGO_UP='#2A436E'; SKY='#B4CFFF'; WHITE='#FFFFFF'

def drip_svg(x0, w, h, fill, seed, pill, gap, depth):
    rnd=random.Random(seed); out=[]; x=x0+gap//2; i=0
    while x+pill<=x0+w:
        L=int(h*rnd.uniform(*depth)); d=rnd.randint(0,520)
        out.append(f'<rect class="rs-pill" x="{x}" y="{-pill}" width="{pill}" height="{L+pill}" rx="{pill/2}" fill="{fill}" style="--d:{d}ms"/>')
        y=L+int(pill*rnd.uniform(0.8,1.6)); k=0
        for _ in range(rnd.randint(0,3)):
            dd=d+380+k*90; k+=1
            if rnd.random()<0.5:
                seg=int(pill*rnd.uniform(1.2,2.6))
                out.append(f'<rect class="rs-drop" x="{x}" y="{y}" width="{pill}" height="{seg}" rx="{pill/2}" fill="{fill}" style="--d:{dd}ms"/>'); y+=seg+int(pill*rnd.uniform(0.7,1.5))
            else:
                out.append(f'<circle class="rs-drop" cx="{x+pill/2}" cy="{y+pill/2}" r="{pill/2}" fill="{fill}" style="--d:{dd}ms"/>'); y+=pill+int(pill*rnd.uniform(0.8,1.8))
            if y>h: break
        x+=pill+gap; i+=1
    return ''.join(out)

# ---- linen banner -> live drip panel ----
banner=('<svg class="rs-drip rs-banner" viewBox="0 0 2304 540" preserveAspectRatio="xMidYMid slice" role="img" aria-label="You come home. It\'s done." xmlns="http://www.w3.org/2000/svg">'
        f'<rect width="2304" height="540" fill="{SKY}"/>'
        +
        f'<text x="104" y="276" font-family="Quicksand, Urbanist, sans-serif" font-weight="700" font-size="128" fill="{INDIGO}" letter-spacing="-2">You come home.</text>'
        f'<text x="104" y="420" font-family="Quicksand, Urbanist, sans-serif" font-weight="700" font-size="128" fill="{INDIGO}" letter-spacing="-2">It’s done.</text>'
        '</svg>')
s,n=re.subn(r'<picture>(?:(?!</picture>).)*banner-linen\.jpg(?:(?!</picture>).)*</picture>',banner,s,flags=re.S)
print('banner',n)

# ---- footer drip band: removed (no pattern on the site) ----
s=re.sub(r'<svg class="rs-drip rs-footer-band".*?</svg>','',s,flags=re.S)

# ---- hero check pills over the collage (the bedroom tile) ----
if 'rs-checks' not in s:
    tick='<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="10"/><path d="M5.6 10.3l2.9 2.9 5.9-6.1"/></svg>'
    pills=''.join(f'<li style="--i:{i}">{tick}<span>{t}</span></li>' for i,t in enumerate(['Fresh sheets','Kitchen','Time for you']))
    checks=f'<ul class="rs-checks" aria-label="Done today: fresh sheets, kitchen, time for you">{pills}</ul>'
    s,n=re.subn(r'(<picture>(?:(?!</picture>).)*hero-collage\.jpg(?:(?!</picture>).)*</picture>)',lambda m:m.group(1)+checks,s,flags=re.S); print('checks',n)

s=s.replace('alt="Collage: keys in hand, a window being cleaned, friends in the kitchen, a calm sofa, fresh bedding, reading by the window"',
            'alt="Collage: keys in hand, a window being cleaned, a calm armchair, sunlight on fresh bedding, a made bed, coffee in the morning light"')


# ---- the word RESET in running text is set as the wordmark (the logo's own lettering) ----
WM='<span class="rs-wm" role="img" aria-label="RESET"></span>'
parts=re.split(r'(<title>.*?</title>|<style[\s\S]*?</style>|<svg[\s\S]*?</svg>|<script[\s\S]*?</script>)',s)
n_wm=0
for i in range(0,len(parts),2):
    def tn(m):
        global n_wm
        t=m.group(1)
        new,k=re.subn(r'\bRESET\b',WM,t); n_wm+=k
        return '>'+new+'<'
    parts[i]=re.sub(r'>([^<>]*RESET[^<>]*)<',tn,parts[i])
s=''.join(parts); print('wordmarks',n_wm)

# ---- motion script ----
if 'motion.js' not in s:
    s=s.replace('</body>','<script src="assets/js/motion.js" defer></script></body>',1)
open(P,'w').write(s)
