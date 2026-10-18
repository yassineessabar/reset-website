"""Copy pass v2: confident, clear, Uber-style voice for an Australian (Sydney) launch.
Applied to a finished index.html; the RESET wordmark spans are flattened first and restored after."""
import re, html, sys
P=sys.argv[1]; WMARK=len(sys.argv)>2 and sys.argv[2]=='--wordmark'
s=open(P).read()
WM='<span class="rs-wm" role="img" aria-label="RESET"></span>'
s=s.replace(WM,'RESET')
NB='\xa0'
T={
# hero
'Size of your home':'Home size',
'Schedule ahead':'Schedule a reset',
# explore
'Your whole home, put back to zero. Book a visit, head out, and come home to done.':'A full clean, top to bottom. Book it, head out, come home to done.',
'Pick your rhythm once, weekly or every two weeks, and stop thinking about it.':'Weekly or every two weeks. Set it once and we take it from there.',
'Turn your place around between guests, with fresh linen on every bed.':'Quick turnovers between guests, with fresh linen on every bed.',
'Hand back the keys, or move into a home that is ready for you.':'A deep clean for the day you hand back the keys, or pick them up.',
'Every corner, cupboard and surface, for when your home needs more than a visit.':'Every corner, cupboard and surface. For when a regular clean isn’t enough.',
'We wash, fold and remake the beds, so every sheet is fresh.':'We wash, fold and remake every bed.',
# how to book
f'Enter your address in the RESET app. Choose a visit and{NB}confirm.':f'Enter your address in the RESET app, pick a time and{NB}confirm.',
f"A vetted RESET member accepts your visit. You'll see who is coming before they{NB}arrive.":f"A background-checked RESET member accepts your visit. You’ll see their name and photo before they{NB}arrive.",
f"Check your RESET member's name and photo, then head out. Your keys stay{NB}safe.":f"Leave a key or a door code. We return it the moment the visit is{NB}done.",
f"Your home is reset room by room while you're out. Follow along live, or{NB}don't.":f"We reset your home room by room while you’re out. Follow along live in the{NB}app.",
f'“All done. You can breathe.” Rate your visit, and leave a tip if you{NB}like.':f'“All done. You can breathe.” Rate your visit and add a tip if you{NB}like.',
# city
'Just moved to Paris?':'New to Sydney?',
f"From a studio in the Marais to a family flat in Boulogne, we've got you covered. Explore neighbourhoods, prices, and more with our new City{NB}Guide.":
f"From a studio in Surry Hills to a family home in Mosman, we’ve got you covered. See the suburbs we clean, prices and more in our City{NB}Guide.",
'Paris':'Sydney',
# more ways
f'Book your move-out reset up to 90 days ahead, so you hand back the keys with{NB}confidence.':f'Book your move-out clean ahead and hand back the keys with{NB}confidence.',
f'Fresh linen, folded towels and a home ready for your next{NB}guests.':f'Fresh linen, folded towels and a home ready for every{NB}check-in.',
# laundry / linen
'We pick up, wash and fold, and bring it back the way you like it.':'We pick up, wash, fold and drop it back, the way you like it.',
'We strip, wash and remake every bed, so you always sleep in fresh linen.':'We strip and remake every bed, so you sleep in fresh linen every time.',
# member
'Join RESET One for member pricing and priority booking with RESET.':'Join RESET One for member pricing and first pick of visit times.',
'Sign up now':'Join now',
# earn
'Make money with home visits, linen runs, or both. We bring the kit.':'Earn with home cleans, linen runs, or both. We supply the kit.',
'Sign up to clean':'Apply to clean',
'Pick visits near you. Just go online, accept, and reset.':'Choose visits near you. Go online, accept, and get paid.',
'Get details':'See how it works',
# business
'RESET for Business gives your offices, rentals and buildings one trusted team. Manage and track every visit, every site and every invoice on one dashboard.':
'RESET for Business gives your offices, rentals and buildings one trusted cleaning team. Manage every site, visit and invoice from one dashboard.',
# footer (Australian English)
'Visit Help Center':'Visit Help Centre','Serviced flats':'Serviced apartments',
}
AU=['Sydney','Melbourne','Brisbane','Perth','Adelaide','Gold Coast','Canberra','Newcastle','Hobart','Wollongong']
FR_HUB=['Paris','Nice','Marseille','Lyon','Toulouse','Bordeaux','Lille','Nantes','Montpellier','Strasbourg']
FR_TAXI=['Avignon','Grenoble','Lille','Lyon','Marseille','Nice','Paris','Reims','Strasbourg','Toulouse']
for fr,au in zip(FR_HUB,AU): T[f'Home cleaning in {fr}']=f'Home cleaning in {au}'
for fr,au in zip(FR_TAXI,AU): T[f'Cleaner {fr}']=f'Cleaners in {au}'
T['Cleaner near me']='Cleaners near me'

hits={}
def tn(m):
    raw=m.group(1); t=html.unescape(raw).strip()
    if t in T:
        hits[t]=hits.get(t,0)+1
        lead=raw[:len(raw)-len(raw.lstrip())]; trail=raw[len(raw.rstrip()):]
        return '>'+lead+html.escape(T[t],quote=False)+trail+'<'
    return m.group(0)
parts=re.split(r'(<style[\s\S]*?</style>|<svg[\s\S]*?</svg>|<script[\s\S]*?</script>|<title>.*?</title>)',s)
for i in range(0,len(parts),2): parts[i]=re.sub(r'>([^<>]+)<',tn,parts[i])
s=''.join(parts)
def at(m):
    name,val=m.group(1),m.group(2); t=html.unescape(val).strip()
    if t in T: return f'{name}="{html.escape(T[t])}"'
    return m.group(0)
s=re.sub(r'\b(alt|aria-label|title|label)="([^"]*)"',at,s)
s=s.replace('aria-label="Seeing information for this city: Paris"','aria-label="Seeing information for this city: Sydney"')
s=s.replace('alt="A bright Parisian apartment"','alt="A bright, calm living room"')
s=s.replace('assets/img/city-paris.jpg','assets/img/city-guide.jpg')
missing=[k for k in T if k not in hits]
if WMARK:
    parts=re.split(r'(<title>.*?</title>|<style[\s\S]*?</style>|<svg[\s\S]*?</svg>|<script[\s\S]*?</script>)',s)
    for i in range(0,len(parts),2):
        parts[i]=re.sub(r'>([^<>]*RESET[^<>]*)<',lambda m:'>'+re.sub(r'\bRESET\b',WM,m.group(1))+'<',parts[i])
    s=''.join(parts)
open(P,'w').write(s)
print(P,'replaced',sum(hits.values()),'unmatched',missing)
