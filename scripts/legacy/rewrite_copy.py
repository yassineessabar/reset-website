import re, html
P='public/index.html'
s=open(P).read()
NB='\xa0'
T={
'Uber clone (reference)':'RESET | Come home to done',
'Ride':'Book','Earn':'Join the team','Travel':'Hosts','Uber Eats':'Linen',
'How Uber works':'How RESET works','Autonomous':'Our standards','Uber Advertising':'Partners','Merchants':'Property managers',
'Taxi near me':'Cleaner near me',
'Drive & deliver':'Clean with RESET','Uber for Business':'RESET for Business',
'Go anywhere':'Come home to done','Pickup now':'This week','Pickup location':'Your address','Dropoff location':'Size of your home',
'Log in to check your activity':'Log in to see your visits','Ready to travel?':'Busy week ahead?',
'Explore what you can do with Uber':'Explore what you can do with RESET',
'Go anywhere with Uber. Request a ride, hop in, and go.':'Your whole home, put back to zero. Book a visit, head out, and come home to done.',
'Reserve':'Recurring',
'Reserve your ride in advance so you can relax on the day of your trip.':'Pick your rhythm once, weekly or every two weeks, and stop thinking about it.',
'Airport':'Holiday rental',
'Request a ride to or from the airport with room for your luggage.':'Turn your place around between guests, with fresh linen on every bed.',
'Taxi (Meter Fare)':'Move in / out',
'Request a local taxi and pay through the Uber app.':'Hand back the keys, or move into a home that is ready for you.',
'Berline':'Deep reset',
'Request a premium ride in a high-end vehicle with a top-rated driver.':'Every corner, cupboard and surface, for when your home needs more than a visit.',
'Van':'Linen & laundry',
'Get a spacious ride with room for up to 6 passengers and their luggage.':'We wash, fold and remake the beds, so every sheet is fresh.',
'How to request a ride':'How to book a reset',
f'Enter your destination on Uber.com or in the Uber app. Choose a ride and{NB}confirm.':f'Enter your address in the RESET app. Choose a visit and{NB}confirm.',
'Get matched with a driver':'Get matched with a RESET member',
f"A nearby driver accepts your request. You'll be notified when they're{NB}close.":f"A vetted RESET member accepts your visit. You'll see who is coming before they{NB}arrive.",
'Meet your driver':'Hand over your keys',
f"Verify your driver's name, vehicle details and your destination, then enter the{NB}vehicle.":f"Check your RESET member's name and photo, then head out. Your keys stay{NB}safe.",
'Enjoy the ride':'Get on with your day',
f'Your driver has turn-by-turn directions for the fastest{NB}route.':f"Your home is reset room by room while you're out. Follow along live, or{NB}don't.",
'Rate and tip':'Come home to a note',
f'Please leave feedback about your trip, and you’ll also be able to tip your{NB}driver.':f'“All done. You can breathe.” Rate your visit, and leave a tip if you{NB}like.',
'Planning your next getaway?':'Just moved to Paris?',
f"From weekend road trip to international destination, we've got you covered. Explore transport options, points of interest, and more with our new City{NB}Hub.":
f"From a studio in the Marais to a family flat in Boulogne, we've got you covered. Explore neighbourhoods, prices, and more with our new City{NB}Guide.",
'More ways to use Uber':'More ways to use RESET',
'Plan your trip in advance':'Moving in or out',
f'Book your ride up to 90 days ahead by choosing Reserve on Uber.com or in the{NB}app.':f'Book your move-out reset up to 90 days ahead, so you hand back the keys with{NB}confidence.',
'Reserve now':'Book ahead',
'Ride in style':'Host with ease',
f'Travel in high-end vehicles with our top-rated{NB}drivers.':f'Fresh linen, folded towels and a home ready for your next{NB}guests.',
'Order from your favorite spots':'Get your laundry done',
'Find local meals for delivery or pickup in the Uber Eats app or online.':'We pick up, wash and fold, and bring it back the way you like it.',
'Search restaurants':'Book laundry',
'Get essentials delivered':'Fresh sheets, every visit',
'Shop for groceries and everyday items from stores near you.':'We strip, wash and remake every bed, so you always sleep in fresh linen.',
'Stock up now':'Add linen',
'Get member savings on rides and delivery':'Get member savings on every visit',
'Join Uber One for member pricing and exclusive perks with Uber.':'Join RESET One for member pricing and priority booking with RESET.',
'Earn with Uber':'Earn with RESET',
'Drive and earn on your schedule':'Clean and earn on your schedule',
'Make money with rides, deliveries, or both. Use your car or rent one.':'Make money with home visits, linen runs, or both. We bring the kit.',
'Sign up to drive':'Sign up to clean',
'Deliver when you want':'Work when you want',
'Turn your commute into earnings. Just go online, pick up, and drop off.':'Pick visits near you. Just go online, accept, and reset.',
'All the benefits of Uber, reimagined for business':'All the benefits of RESET, reimagined for business',
'Uber for Business gives your organization more control, deeper insights, and features built for enterprise users. Manage and track business travel, meal programs, and more on one dashboard.':
'RESET for Business gives your offices, rentals and buildings one trusted team. Manage and track every visit, every site and every invoice on one dashboard.',
'Download the Uber app':'Download the RESET app','Download the Driver app':'Download the RESET Team app',
'How the Uber and Uber Eats apps and websites work':'How the RESET apps and website work',
'Uber One':'RESET One','Drive':'Clean','Deliver':'Laundry','Eat':'Linen','Uber Freight':'RESET for Hosts','Uber Health':'RESET Care',
'Global citizenship':'Our commitments','Airports':'Holiday rentals','Hotels':'Serviced flats',
'Uber Technologies Inc.':'RESET. Nothing left to think about.',
'Sign in to drive & deliver':'Sign in to clean with RESET','Sign in to ride':'Sign in to book',
'Sign in to order delivery with Uber Eats':'Sign in to order laundry','Sign in to your Uber for Business account':'Sign in to your RESET for Business account',
}
for city in ['Paris','Nice','Marseille','Lyon','Toulouse','Bordeaux','Lille','Nantes','Montpellier','Strasbourg']:
    T[f'Getting around {city}']=f'Home cleaning in {city}'
for city in ['Avignon','Grenoble','Lille','Lyon','Marseille','Nice','Paris','Reims','Strasbourg','Toulouse']:
    T[f'Taxi {city}']=f'Cleaner {city}'

# text nodes (skip inside <style>/<svg>)
n_hit={}
def tn(m):
    raw=m.group(1); t=html.unescape(raw).strip()
    if t in T:
        n_hit[t]=n_hit.get(t,0)+1
        lead=raw[:len(raw)-len(raw.lstrip())]; trail=raw[len(raw.rstrip()):]
        return '>'+lead+html.escape(T[t],quote=False)+trail+'<'
    return m.group(0)
parts=re.split(r'(<style[\s\S]*?</style>|<svg[\s\S]*?</svg>)',s)
for i in range(0,len(parts),2): parts[i]=re.sub(r'>([^<>]+)<',tn,parts[i])
s=''.join(parts)
missing=[k for k in T if k not in n_hit]
print('unmatched keys:',missing)

# attributes: alt / aria-label / title / placeholder
A={'Travel collage: packing, navigation, taxis, luggage, and reunions during urban trips':'Collage: keys in hand, a window being cleaned, friends in the kitchen, a calm sofa, fresh bedding, reading by the window',
'Flower bouquets beside green Uber Eats delivery bags in sunlight':'Stacks of fresh folded towels',
'Brunch spread with waffles, berries, whipped cream, fried egg sandwich, fries, coffee, and syrup on a marble table':'Someone folding freshly washed clothes',
'Dog food, treats, a green bowl, and plush toy arranged on a kitchen counter':'A freshly made bed in morning light',
'Smiling couple exits a car; woman in orange striped dress waves upward, framed by a gold square and circular logo.':'A couple laughing while cooking at home, framed in sky blue with the RESET check',
'Family smiling inside a car, seen through reflections on the side window':'A family relaxing together on the sofa',
'Woman riding in an Uber car with luggage, chart, and clipboard icons below':'A bright office, with building, chart and clipboard icons below',
'Uber homepage':'RESET homepage','Ride with Uber':'Book with RESET','Ride — Request a ride':'Book — Request a visit',
'How Uber works to request rides':'How RESET works to book visits','Sign up to ride, drive, and get delivery':'Sign up to book, clean, and get laundry done',
'Request a local taxi and pay through the Uber app.':'Hand back the keys, or move into a home that is ready for you.',
'Pickup location needs to be filled in':'Your address needs to be filled in','Dropoff location needs to be filled in':'Size of your home needs to be filled in',
'Autonomous vehicle initiatives':'Our standards','Download the Uber app':'Download the RESET app','Download the Driver app':'Download the RESET Team app',
'Download the Uber app by QR code or select button':'Download the RESET app by QR code or select button',
'Download the Driver app by QR code or select button':'Download the RESET Team app by QR code or select button',
'Download the Uber app for Android':'Download the RESET app for Android','Download the Uber app for IOS':'Download the RESET app for iOS',
'Download the Uber app on Google Play':'Download the RESET app on Google Play','Download the Uber app on the App Store':'Download the RESET app on the App Store',
'How the Uber and Uber Eats apps and websites work':'How the RESET apps and website work'}
for k in list(T):
    if k in ('Ride','Reserve','Airport','Taxi (Meter Fare)','Berline','Van'):
        A[k]=T[k]; A[k+', Details']=T[k]+', Details'
for k in T:
    if len(k)>12: A.setdefault(k,T[k])
def at(m):
    name,val=m.group(1),m.group(2); t=html.unescape(val).strip()
    if t in A: return f'{name}="{html.escape(A[t])}"'
    return m.group(0)
s=re.sub(r'\b(alt|aria-label|title|placeholder)="([^"]*)"',at,s)

# logo text -> RESET wordmark
s,n=re.subn(r'(data-testid="wcb3-navigation-logo"[^>]*>)Uber(</a>)',r'\1<img src="assets/img/brand/reset-logo-white.svg" alt="RESET" style="height:24px;width:auto;display:block">\2',s); print('nav logos',n)
s,n=re.subn(r'(data-testid="footer-logo-typography-logo"[^>]*>)Uber(</a>)',r'\1<img src="assets/img/brand/reset-logo-white.svg" alt="RESET" style="height:26px;width:auto;display:block">\2',s); print('footer logo',n)

# images
IMG={'1692704b22ba731d':'hero-collage.jpg','79ebda781122b4c1':'hero-collage.jpg','f72f0bf5cda0b7ea':'hero-collage.jpg',
'844ef8761df674eb':'product-sponge.png','1cd399d26bed0216':'product-calendar.png','196687e93664ea0f':'product-bed.png',
'a8409842927fde88':'product-package.png','f863e4a5e827ed58':'product-couch.png','99d6161aa79863fb':'product-basket.png',
'6d3fb9b08e4b6a14':'step-1-book.png','6d5ff252958ee833':'step-2-matched.png','e907b6210aca5087':'step-3-keys.png','f20ee6485e85c48e':'step-4-reset.png','cf1b9692ce2bd831':'step-5-note.png',
'4c675e4b4fa4ff82':'more-moving.png','4d65d5e9caa4f42f':'more-hosting.png',
'e9c3ef445bbefc2b':'banner-linen.jpg','fca2f9b552e867fa':'banner-linen.jpg','d956e7e3b1fd1e26':'banner-linen.jpg',
'6cea42d2dde9e308':'card-laundry.jpg','ebe9b25508260b72':'card-laundry.jpg','3bd2d02ccac1d269':'card-laundry.jpg',
'3d32db85f41de32d':'card-linen.jpg','90ee3588764db6d6':'card-linen.jpg','2cac7cd4bccfc9a7':'card-linen.jpg',
'dec21c645deb6d4f':'member.png','fbecd990d08a7df1':'member.png','4a630c32a827f1b8':'member.png',
'311155e917d68d50':'banner-family.jpg','9cc96ee007042c3f':'banner-family.jpg','8d6df6f79d16b81a':'banner-family.jpg',
'earn-5a3dc9b1-ff52-4243-bea9-f86af73fc41b':'earn-team.jpg','earn-71d59488-6bbc-4df3-8055-7c849e7e9243':'earn-flexible.jpg',
'6b8f62b9a3be6f86':'business.png','1df96eeccb042748':'business.png','82b3aa29b631d8e6':'business.png',
'422bb87aca455599':'app-icon-reset.png','d4b9678318547259':'app-icon-team.png',
'320998cb2d702197':'qr-reset.png','5a152904f394b6a3':'qr-reset.png','449b5df40af7b09e':'qr-reset.png',
'd280134400509e5c':'qr-team.png','132b1ca40dc91bb6':'qr-team.png','7bb0d8e3d3ff1643':'qr-team.png'}
cnt=0
def im(m):
    global cnt
    key=m.group(1)
    if key in IMG: cnt+=1; return 'assets/img/'+IMG[key]
    return m.group(0)
s=re.sub(r'assets/img/([0-9a-f]{16}|earn-[0-9a-f-]+)\.(?:webp|png|svg|jpg)',im,s)
print('image refs swapped',cnt)
# 2x srcset descriptors would now point to the same file; drop the duplicate second candidate
s=re.sub(r'srcset="(assets/img/[^", ]+), \1 2x"',r'srcset="\1"',s)

# city hub video -> still photo
s,n=re.subn(r'<video[^>]*>[\s\S]*?</video>','<img src="assets/img/city-paris.jpg" alt="A bright Parisian apartment" style="width:100%;height:100%;object-fit:cover;display:block">',s); print('video',n)

open(P,'w').write(s)
vis=re.sub(r'<(style|svg)[\s\S]*?</\1>','',s)
left=sorted(set(html.unescape(x).strip() for x in re.findall(r'>([^<>]*Uber[^<>]*)<',vis)))
print('text still mentioning Uber:',left)
print('attrs with Uber:',sorted(set(re.findall(r'(?:alt|aria-label|title)="([^"]*Uber[^"]*)"',s)))[:20])
