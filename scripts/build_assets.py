from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np, qrcode, subprocess, os
from paths import PHOTOS as SRC, RENDERS, IMG, DESIGN, FONTS
R=RENDERS                        # PNG/JPG renders; seo.py turns them into the WebPs in public/assets/img
U=DESIGN+'masks/'                # alpha masks of the original slot shapes
ICO=DESIGN+'icons/'; GL=DESIGN+'glyphs/'
# Black and white world: names kept from the colour version, values are monochrome
INDIGO=(14,14,14); INDIGO_UP=(26,26,26); INDIGO_LINE=(46,46,46); SKY=(255,255,255); MIST=(242,242,242); WHITE=(255,255,255)
INK=INDIGO
BLACK=INDIGO
FONT_TITLE=FONTS+'InterTight-var.ttf'; FONT_BODY=FONTS+'Inter-var.ttf'
from PIL import ImageFont

def grade(im, seed=0):
    # Uber-style warm photography: amber light in skin, wood and sun; whites kept clean; rich colour, full contrast.
    a=np.asarray(im.convert('RGB')).astype(float)/255
    lum=(a*[0.299,0.587,0.114]).sum(axis=2,keepdims=True)
    a=lum+(a-lum)*1.10                     # richer colour
    mid=np.clip(1-np.abs(lum-0.45)*2.2,0,1)   # warmth lives in the midtones
    a=a*(1+mid*np.array([0.09,0.02,-0.10]))  # amber, not yellow
    clean=np.clip((lum-0.82)*5,0,1)        # near-white stays near-white
    a=a*(1-0.6*clean)+np.clip(a,0,1).mean(axis=2,keepdims=True)*np.array([1.01,1.0,0.97])*0.6*clean
    sh=np.clip(1-lum*2.2,0,1)
    a=a*(1-0.08*sh)+np.array([0.18,0.11,0.07])*0.08*sh    # warm brown shadows
    a=np.clip(a,0,1); a=a*a*(3-2*a)*0.3+a*0.7             # gentle S for depth
    return Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))

def brand_icon(path):
    # 3D objects keep their own colour: they are the colour accents on the black and white interface.
    return Image.open(path).convert('RGBA')

def drip(w,h,bg,fg,seed=7,pill=None,gap=None,dots=True,depth=(0.35,0.95)):
    # The trail a wipe leaves: rounded pills from the top edge breaking into dots.
    import random
    rnd=random.Random(seed); im=Image.new('RGBA',(w,h),bg+(255,) if bg else (0,0,0,0)); d=ImageDraw.Draw(im)
    pw=pill or max(8,w//60); g=gap or int(pw*0.9); x=g//2
    while x<w:
        L=int(h*rnd.uniform(*depth)); d.rounded_rectangle([x,-pw,x+pw,L],pw//2,fill=fg)
        if dots:
            y=L+int(pw*rnd.uniform(0.8,1.6))
            for _ in range(rnd.randint(0,3)):
                if rnd.random()<0.5:
                    seg=int(pw*rnd.uniform(1.2,2.6)); d.rounded_rectangle([x,y,x+pw,y+seg],pw//2,fill=fg); y+=seg+int(pw*rnd.uniform(0.7,1.5))
                else:
                    d.ellipse([x,y,x+pw,y+pw],fill=fg); y+=pw+int(pw*rnd.uniform(0.8,1.8))
                if y>h: break
        x+=pw+g
    return im

def check_pill(text,scale=2):
    f=ImageFont.truetype(FONT_BODY,15*scale); f.set_variation_by_axes([650])
    tw=int(f.getlength(text)); h=30*scale; pad=10*scale; c=20*scale
    w=pad+c+8*scale+tw+pad+4*scale
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,w-1,h-1],h//2,fill=WHITE+(242,))
    cx=pad+c//2; cy=h//2; d.ellipse([cx-c//2,cy-c//2,cx+c//2,cy+c//2],fill=INDIGO)
    d.line([cx-5*scale,cy,cx-1.5*scale,cy+3.5*scale,cx+5*scale,cy-4*scale],fill=WHITE,width=int(2.2*scale),joint='curve')
    d.text((pad+c+8*scale,h//2),text,font=f,fill=INDIGO,anchor='lm')
    return im

os.makedirs(RENDERS,exist_ok=True)
def photo(name):
    if name=='bucket_hands':   # top of the brand bucket photo: hands wringing the cloth
        return grade(Image.open(SRC+'brand_bucket.jpg').crop((0,0,940,640)))
    return grade(Image.open(SRC+name+'.jpg'))
def cover(im,w,h,cx=0.5,cy=0.5):
    return ImageOps.fit(im,(w,h),Image.LANCZOS,centering=(cx,cy))
def rmask(w,h,r):
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],r,fill=255); return m
def save(im,name,q=86):
    p=RENDERS+name
    if name.endswith('.png'): im.save(p,optimize=True)
    else: im.convert('RGB').save(p,quality=q,optimize=True,progressive=True)
    return name


def object_tile(icon, tw, th, S, radius=16, obj=0.9, floor=0.84):
    """One icon language: a big 3D object standing on a raised, top-lit dark tile and breaking
    out of its top edge, with a soft contact shadow. Returns (image, left pad, top offset)."""
    ic=brand_icon(ICO+icon+'.png'); ic=ic.crop(ic.getbbox())
    k=th*obj/max(ic.width,ic.height); ic=ic.resize((int(ic.width*k),int(ic.height*k)),Image.LANCZOS)
    pad=int(20*S); base=int(th*floor)                    # where the object stands, from the tile top
    pop=max(0,ic.height-base+int(6*S))                   # how far it rises above the tile
    W,H=tw+2*pad, th+pop+2*pad; ty=pad+pop
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    drop=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(drop).rounded_rectangle([pad,ty+int(8*S),pad+tw,ty+th+int(8*S)],radius*S,fill=(0,0,0,130))
    im=Image.alpha_composite(im,drop.filter(ImageFilter.GaussianBlur(14*S)))
    g=np.linspace(0,1,th)[:,None]; top=np.array([40,40,40]); bot=np.array([20,20,20])
    grad=(top*(1-g)+bot*g)[:,None,:].repeat(tw,axis=1).reshape(th,tw,3)
    tile=Image.fromarray(grad.astype(np.uint8)).convert('RGBA'); tile.putalpha(rmask(tw,th,radius*S))
    td=ImageDraw.Draw(tile)
    td.rounded_rectangle([0,0,tw-1,th-1],radius*S,outline=(54,54,54,255),width=max(1,S))
    td.line([radius*S,1*S,tw-radius*S,1*S],fill=(255,255,255,26),width=max(1,S))   # top light catch
    im.alpha_composite(tile,(pad,ty))
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); cx=pad+tw/2; by=ty+base
    ImageDraw.Draw(sh).ellipse([cx-ic.width*0.42,by-9*S,cx+ic.width*0.42,by+8*S],fill=(0,0,0,190))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(7*S)))
    im.alpha_composite(ic,(int(cx-ic.width/2),by-ic.height))
    return im, pad, pop

# ---------- hero collage (Uber: 2 columns x 3 tiles on black, 672px; rendered 2x) ----------
S=2
canvas=Image.new('RGB',(672*S,672*S),INDIGO)
boxes={ # (x0,y0,x1,y1) from the original layout
 'hero_keys':(0,35,332,255),'bucket_hands':(0,277,332,497),'life_woman_armchair':(0,520,332,671),
 'life_bed_shadows':(344,0,671,233),'life_bedroom_window':(344,255,671,483),'life_mug_sunlight':(344,505,671,671)}
focus={'hero_keys':(0.5,0.45),'bucket_hands':(0.5,0.0),'life_woman_armchair':(0.45,0.5),'life_bed_shadows':(0.5,0.45),'life_bedroom_window':(0.55,0.6),'life_mug_sunlight':(0.5,0.62)}
for k,(x0,y0,x1,y1) in boxes.items():
    w,h=(x1-x0+1)*S,(y1-y0+1)*S
    canvas.paste(cover(photo(k),w,h,*focus[k]),(x0*S,y0*S))
save(canvas,'hero-collage.jpg')   # check pills are live HTML on the page

# ---------- product tiles: 3D object, soft floor shadow, transparent 360px (2x) ----------
def product(icon, name, scale=0.62):
    W=720; im=Image.new('RGBA',(W,W),(0,0,0,0))
    ic=brand_icon(ICO+icon+'.png')
    s=int(W*scale); ic=ic.resize((s,s),Image.LANCZOS)
    bbox=ic.getbbox(); ic=ic.crop(bbox)
    x=(W-ic.width)//2; y=int(W*0.56)-ic.height//2
    sh=Image.new('RGBA',(W,W),(0,0,0,0)); d=ImageDraw.Draw(sh)
    cx=W//2; base=y+ic.height
    d.ellipse([cx-ic.width*0.42,base-26,cx+ic.width*0.42,base+22],fill=(0,0,0,160))
    sh=sh.filter(ImageFilter.GaussianBlur(18))
    im=Image.alpha_composite(im,sh); im.alpha_composite(ic,(x,y))
    return save(im,name)
for icon in ['sponge','calendar','bed','package','couch','basket']: product(icon,f'product-{icon}.png')

# ---------- step cards: photo top-right + white badge bottom-left (708x398, 2x) ----------
ref=np.array(Image.open(U+'6d3fb9b08e4b6a14.png').convert('RGBA'))[:,:,3]>10
ph_rows=np.where(ref[:,400])[0]; PY1=int(ph_rows.max())
GLYPH_INK=INDIGO
def uber_glyph(kind, size, ink):
    """Solid one-colour glyph in Uber's step-badge style, drawn at 8x and downsampled."""
    Z=512; im=Image.new('RGBA',(Z,Z),(0,0,0,0)); d=ImageDraw.Draw(im)
    K=ink+(255,); O=(0,0,0,0)
    if kind=='pin':
        d.ellipse([106,24,406,324],fill=K); d.ellipse([206,124,306,224],fill=O)
        d.rounded_rectangle([226,300,286,488],30,fill=K)
    elif kind=='person':
        d.ellipse([171,40,341,210],fill=K)
        d.pieslice([86,250,426,590],180,360,fill=K); d.rectangle([86,420,426,470],fill=K)
        d.rectangle([0,471,Z,Z],fill=O)
    elif kind=='key':
        d.ellipse([24,106,324,406],fill=K); d.ellipse([110,192,238,320],fill=O)
        d.rounded_rectangle([290,216,488,296],14,fill=K)
        d.rectangle([420,290,476,392],fill=K); d.rectangle([336,290,388,370],fill=K)
    elif kind=='sparkle':
        d.ellipse([36,36,476,476],fill=K)
        c=256; r=150; w=34
        d.polygon([(c,c-r),(c+w,c-w),(c+r,c),(c+w,c+w),(c,c+r),(c-w,c+w),(c-r,c),(c-w,c-w)],fill=O)
    elif kind=='note':
        d.rounded_rectangle([86,40,426,472],40,fill=K)
        for y in (150,236,322): d.rounded_rectangle([156,y,356 if y<322 else 286,y+36],18,fill=O)
    return im.resize((size,size),Image.LANCZOS)

def step(src,glyph,name,cx=0.5,cy=0.5):
    # Uber's "How to request a ride" card: photo top-right, white square badge bottom-left with one solid glyph
    S=2; W,H=708*S,398*S
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    px0,px1,py1=132*S,664*S,PY1*S
    p=cover(photo(src),px1-px0,py1,cx,cy).convert('RGBA'); p.putalpha(rmask(p.width,p.height,16*S))
    im.alpha_composite(p,(px0,0))
    bw,bh=164*S,168*S; by=H-bh
    badge=Image.new('RGBA',(bw,bh),(255,255,255,255)); badge.putalpha(rmask(bw,bh,14*S))
    g=uber_glyph(glyph,64*S,GLYPH_INK)
    badge.alpha_composite(g,((bw-g.width)//2,(bh-g.height)//2))
    im.alpha_composite(badge,(0,by))
    return save(im,name)
step('step_phone_app','pin','step-1-book.png',0.55,0.28)
step('step_member2','person','step-2-matched.png',0.5,0.35)
step('step_keys','key','step-3-keys.png',0.5,0.4)
step('step_mop','sparkle','step-4-reset.png',0.5,0.5)
step('step_note','note','step-5-note.png',0.5,0.5)

# ---------- more ways: photo + light tile with 3D object (720x480, 2x) ----------
ref=np.array(Image.open(U+'4c675e4b4fa4ff82.png').convert('RGBA'))[:,:,3]>10
mrow=np.where(ref[:,400])[0]; MY1=int(mrow.max())
def more(src,name,cx=0.5,cy=0.5):
    # "More ways to use": the photo alone, filling the frame (no 3D object tile)
    S=2; W,H=720*S,480*S
    p=cover(photo(src),W,H,cx,cy).convert('RGBA'); p.putalpha(rmask(W,H,12*S))
    return save(p,name)
more('more_move','more-moving.png',0.5,0.4)
more('life_living_bright','more-hosting.png',0.5,0.62)

# ---------- wide banners ----------
bn=drip(1104,540,SKY,WHITE,seed=11,pill=54,gap=40,depth=(0.3,0.92))
panel=Image.new('RGBA',(2304,540),SKY+(255,)); panel.alpha_composite(bn,(1200,0))
dd=ImageDraw.Draw(panel); ft=ImageFont.truetype(FONT_TITLE,128)
dd.text((104,276),'You come home.',font=ft,fill=INDIGO,anchor='ls'); dd.text((104,420),"It's done.",font=ft,fill=INDIGO,anchor='ls')
save(panel,'banner-linen.jpg')
save(cover(photo('life_living_warm'),2304,540,0.5,0.62),'banner-family.jpg')

# ---------- service cards with sky border (576x384, 2x) ----------
def bordered(src,name,cx=0.5,cy=0.5):
    S=2; W,H=576*S,384*S; b=3*S
    im=Image.new('RGB',(W,H),INK)
    im.paste(cover(photo(src),W-2*b,H-2*b,cx,cy),(b,b))
    return save(im,name)
bordered('life_folded_linen','card-laundry.jpg',0.5,0.55)
bordered('life_hydrangea_window','card-linen.jpg',0.5,0.6)

# ---------- member photo with sky frame + check badge (576x384 transparent margins, 2x) ----------
S=2; W,H=576*S,384*S
im=Image.new('RGBA',(W,H),(0,0,0,0))
p=cover(photo('member_couple'),W,(354-30+1)*S,0.5,0.35).convert('RGBA'); p.putalpha(rmask(p.width,p.height,12*S))
im.alpha_composite(p,(0,30*S))
d=ImageDraw.Draw(im)
fx0,fy0,fx1,fy1=226*S,60*S,410*S,300*S
d.rounded_rectangle([fx0,fy0,fx1,fy1],10*S,outline=SKY,width=3*S)
cx,cy,r=fx1-34*S,fy1-34*S,22*S
d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=SKY)
d.line([cx-9*S,cy+1*S,cx-2*S,cy+8*S,cx+10*S,cy-7*S],fill=BLACK,width=4*S,joint='curve')
save(im,'member.png')

# ---------- earn ----------
save(cover(photo('earn_making_bed'),1152,647,0.5,0.4),'earn-team.jpg')
save(cover(photo('earn_cushions'),1152,647,0.5,0.4),'earn-flexible.jpg')

# ---------- business: circle photo + 3 dark tiles with 3D objects (576, 2x) ----------
S=2; W=576*S
im=Image.new('RGBA',(W,W),(0,0,0,0))
cxx,cyy,rr=288*S,287*S,241*S
ph=cover(photo('biz_office'),2*rr,2*rr,0.5,0.5).convert('RGBA')
m=Image.new('L',(2*rr,2*rr),0); ImageDraw.Draw(m).ellipse([0,0,2*rr-1,2*rr-1],fill=255); ph.putalpha(m)
im.alpha_composite(ph,(cxx-rr,cyy-rr))
for x0,icon in [(20,'office'),(205,'chart'),(391,'clipboard')]:
    tw,th=166*S,158*S; ty=372*S
    tile=Image.new('RGBA',(tw,th),INDIGO_UP+(250,)); tile.putalpha(rmask(tw,th,16*S))
    ImageDraw.Draw(tile).rounded_rectangle([1,1,tw-2,th-2],16*S,outline=INDIGO_LINE+(255,),width=2)
    ic=brand_icon(ICO+icon+'.png').resize((96*S,96*S),Image.LANCZOS)
    tile.alpha_composite(ic,((tw-ic.width)//2,(th-ic.height)//2))
    im.alpha_composite(tile,(x0*S,ty))
save(im,'business.png')

# ---------- city hub still (replaces Uber's video) ----------
save(cover(photo('life_living_bright'),1152,768,0.5,0.55),'city-guide.jpg')

# ---------- app icons (60px svg slots) and QR codes ----------
logo_w=IMG+'brand/reset-logo-white.svg'; logo_b=IMG+'brand/reset-logo-black.svg'
subprocess.run(['rsvg-convert','-w','150',logo_w,'-o',RENDERS+'_lw.png']); subprocess.run(['rsvg-convert','-w','150',logo_b,'-o',RENDERS+'_lb.png'])
def appicon(bg,logo,name):
    W=240; im=Image.new('RGBA',(W,W),(0,0,0,0))
    sq=Image.new('RGBA',(W,W),bg+(255,)); sq.putalpha(rmask(W,W,54)); im.alpha_composite(sq)
    lg=Image.open(logo).convert('RGBA'); im.alpha_composite(lg,((W-lg.width)//2,(W-lg.height)//2))
    return save(im,name)
appicon(BLACK,RENDERS+'_lw.png','app-icon-reset.png')
appicon(SKY,RENDERS+'_lb.png','app-icon-team.png')
def qr(text,name,badge):
    q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=36,border=0); q.add_data(text); q.make(fit=True)
    im=q.make_image(fill_color=INDIGO,back_color='white').convert('RGBA').resize((1152,1152),Image.NEAREST)
    b=Image.open(RENDERS+badge).convert('RGBA').resize((260,260),Image.LANCZOS)
    pad=Image.new('RGBA',(300,300),(255,255,255,255)); pad.alpha_composite(b,(20,20))
    im.alpha_composite(pad,((1152-300)//2,(1152-300)//2))
    return save(im,name)
qr('RESET: your place, sorted. App coming soon.','qr-reset.png','app-icon-reset.png')
qr('RESET Team: clean on your schedule. App coming soon.','qr-team.png','app-icon-team.png')
for f in ['_lw.png','_lb.png']: os.remove(RENDERS+f)
# ---------- brand banner: the photo alone, full width, no text (Uber's banners are just a picture) (2304x540) ----------
panel=cover(photo('life_woman_window'),2304,540,0.5,0.665)   # reading by the window: you come home, it's done
save(panel,'banner-bucket.jpg',q=88)
print(sorted(os.listdir(RENDERS)))
