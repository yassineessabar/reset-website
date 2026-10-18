"""Images for business.html (Uber for Business layout), sized to the slots they replace."""
from paths import REPO, RENDERS, IMG
SRC=REPO+'scripts/build_assets.py'
code=open(SRC).read(); g={}
exec(code[:code.index('# ---------- hero collage')],g)
Image,ImageDraw,cover,photo,save,rmask,brand_icon,ICO,R=[g[k] for k in ('Image','ImageDraw','cover','photo','save','rmask','brand_icon','ICO','R')]
import subprocess
def webp(name):
    subprocess.run(['cwebp','-quiet','-q','84','-alpha_q','90',RENDERS+name,'-o',IMG+name.rsplit('.',1)[0]+'.webp'])
def ph(src,name,w,h,cx=0.5,cy=0.5):
    save(cover(photo(src),w,h,cx,cy),name); webp(name)
# hero 552x552 @2x
ph('biz_office','biz-hero.jpg',1104,1104,0.45,0.5)
# value icons: the 3D object alone, transparent
for icon in ['money_bag','clipboard','handshake','key']:
    ic=brand_icon(ICO+icon+'.png'); ic=ic.crop(ic.getbbox()); ic.thumbnail((192,192),Image.LANCZOS)
    c=Image.new('RGBA',(192,192),(0,0,0,0)); c.alpha_composite(ic,((192-ic.width)//2,(192-ic.height)//2)); save(c,f'biz-icon-{icon}.png'); webp(f'biz-icon-{icon}.png')
# use-case circles
for src,name,cx,cy in [('biz_office','biz-use-offices.png',0.5,0.5),('life_bedroom_window','biz-use-rentals.png',0.55,0.6),('hero_keys','biz-use-property.png',0.5,0.45)]:
    p=cover(photo(src),480,480,cx,cy).convert('RGBA'); m=Image.new('L',(480,480),0); ImageDraw.Draw(m).ellipse([0,0,479,479],fill=255); p.putalpha(m); save(p,name); webp(name)
# steps 552x311 @2x
ph('biz_office','biz-step-sites.jpg',1104,622,0.5,0.5)
ph('earn_making_bed','biz-step-team.jpg',1104,622,0.5,0.4)
ph('step_phone_app','biz-step-dashboard.jpg',1104,622,0.55,0.3)
# sector row: the 3D object centred in the logo slot (552x311 @2x)
for icon in ['office','hotel','classical_building']:
    c=Image.new('RGBA',(1104,622),(0,0,0,0)); ic=brand_icon(ICO+icon+'.png'); ic=ic.crop(ic.getbbox()); ic.thumbnail((360,360),Image.LANCZOS)
    c.alpha_composite(ic,((1104-ic.width)//2,(622-ic.height)//2)); save(c,f'biz-sector-{icon}.png'); webp(f'biz-sector-{icon}.png')
# manifesto image 1314x740: the brand bucket (hands, cloth, handle), no baked logo
b=g['grade'](Image.open(g['SRC']+'brand_bucket.jpg').crop((0,120,940,650)),seed=3)
save(cover(b,1314,740,0.5,0.5),'biz-manifesto.jpg'); webp('biz-manifesto.jpg')
# guides 552x552 @2x
ph('step_mop','biz-guide-office.jpg',1104,1104,0.5,0.5)
ph('life_hydrangea_window','biz-guide-rental.jpg',1104,1104,0.55,0.55)
ph('more_move','biz-guide-vacate.jpg',1104,1104,0.5,0.4)
print('business assets ok')
