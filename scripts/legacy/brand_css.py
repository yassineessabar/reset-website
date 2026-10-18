"""Rebuild assets/css/base.css from ../uber-clone in RESET black and white.

- Uber Move (display) -> Inter Tight, Uber Move Text (body) -> Inter (the wordmark's family); Uber font files dropped.
- Every neutral grey is remapped onto one monochrome ramp: ink #0E0E0E -> paper -> white. Alpha is kept.
- Uber's link/focus blue becomes a mid grey.
"""
import re
SRC='uber.css'  # the original Uber capture (not in this repo)
OUT='public/assets/css/base.css'
u=open(SRC).read()
u=re.sub(r'@font-face\s*{[^}]*}','',u)
u=u.replace('UberMoveText','Inter').replace('UberMove','"Inter Tight"')

# RESET ramp: position (0 = black, 1 = white) -> colour
STOPS=[(0.00,(14,14,14)),    # ink #0E0E0E (the wordmark black)
       (0.10,(26,26,26)),    # raised black (cards, pills on dark)
       (0.25,(46,46,46)),    # hover / hairlines on dark
       (0.45,(88,88,88)),    # muted text (>=4.5:1 on white)
       (0.70,(163,163,163)), # soft grey
       (0.92,(239,239,239)), # paper
       (1.00,(255,255,255))]
def ramp(t):
    for (a,ca),(b,cb) in zip(STOPS,STOPS[1:]):
        if t<=b:
            k=(t-a)/(b-a) if b>a else 0
            return tuple(round(ca[i]+(cb[i]-ca[i])*k) for i in range(3))
    return STOPS[-1][1]
def mapc(r,g,b):
    if max(r,g,b)-min(r,g,b)<=6:                  # neutral grey
        return ramp(((r+g+b)/3)/255)
    if (r,g,b) in ((39,110,241),(26,115,232),(17,117,221)):  # Uber link / focus blue
        return (110,110,110)
    return (r,g,b)
def hex2(h):
    h=h[1:]
    if len(h)==3: h=''.join(c*2 for c in h)
    return tuple(int(h[i:i+2],16) for i in (0,2,4)), (h[6:8] if len(h)==8 else '')
def sub_hex(m):
    (r,g,b),a=hex2(m.group(0)); nr,ng,nb=mapc(r,g,b)
    return '#%02X%02X%02X%s'%(nr,ng,nb,a)
def sub_rgb(m):
    fn,args=m.group(1),[x.strip() for x in m.group(2).split(',')]
    r,g,b=(int(float(x)) for x in args[:3]); nr,ng,nb=mapc(r,g,b)
    rest=(', '+args[3]) if len(args)>3 else ''
    return f'{fn}({nr}, {ng}, {nb}{rest})'
u=re.sub(r'#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b',sub_hex,u)
u=re.sub(r'(rgba?)\(([^)]*)\)',sub_rgb,u)
u=re.sub(r'\b(black)\b(?=\s*[;!}])','#0E0E0E',u)
u=re.sub(r'\b(white)\b(?=\s*[;!}])','#FFFFFF',u)
# Uber CSS url() paths pointed at the clone's own img folder; keep only what still exists
open(OUT,'w').write(u)
print('written',len(u))
