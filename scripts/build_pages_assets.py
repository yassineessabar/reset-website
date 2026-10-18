"""Assets for book.html / earn.html / business.html, built with build_assets.py's own helpers."""
import re
from paths import REPO, RENDERS, IMG
SRC=REPO+'scripts/build_assets.py'
code=open(SRC).read()
g={}
exec(code[:code.index('# ---------- hero collage')],g)
prod=code[code.index('def product('):code.index("for icon in")]
exec(prod,g)
for icon in ['office','hotel','key','classical_building','shopping_bags','money_bag']:
    g['product'](icon,f'product-{icon}.png')
biz=code[code.index('# ---------- business:'):code.index('# ---------- city hub')]
earn=(biz.replace("photo('biz_office')","photo('step_member2')")
         .replace("[(20,'office'),(205,'chart'),(391,'clipboard')]","[(20,'calendar'),(205,'money_bag'),(391,'house')]")
         .replace("'business.png'","'earn-hero.png'"))
exec(earn,g)
print('ok')
# "Why clean with RESET": a plain rounded photo in the member slot's shape (576x384, transparent margins)
S=2; W,H=576*S,384*S
Image=g['Image']
im=Image.new('RGBA',(W,H),(0,0,0,0))
p=g['cover'](g['photo']('earn_cushions'),W,(354-30+1)*S,0.5,0.35).convert('RGBA'); p.putalpha(g['rmask'](p.width,p.height,12*S))
im.alpha_composite(p,(0,30*S)); g['save'](im,'earn-why.png')
print('earn-why ok')
