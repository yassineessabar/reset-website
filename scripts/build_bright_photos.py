"""'How to book a reset' and 'More ways to use RESET': real photos only, bright and inspiring (Uber-style).
No icon badge or object tile: each photo fills its slot, with soft rounded corners."""
import subprocess
from PIL import Image, ImageDraw, ImageOps
import numpy as np
from paths import PHOTOS as SRC, RENDERS, IMG as OUT

def bright(im):
    # Uber-style: bright exposure, clean whites, colour a touch richer, gentle contrast, no grain
    a=np.asarray(im.convert('RGB')).astype(float)/255
    a=np.clip(a*1.05+0.02,0,1)                                  # lift exposure
    lum=(a*[0.299,0.587,0.114]).sum(axis=2,keepdims=True)
    a=lum+(a-lum)*1.10                                          # richer colour
    a=np.clip(a,0,1); a=a*a*(3-2*a)*0.18+a*0.82                 # gentle S-curve
    a=a*np.array([1.012,1.0,0.985])                             # a little warmth
    return Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))

def slot(src,name,w,h,cx=0.5,cy=0.5,r=32):
    im=ImageOps.fit(bright(Image.open(SRC+src+'.jpg')),(w,h),Image.LANCZOS,centering=(cx,cy)).convert('RGBA')
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],r,fill=255); im.putalpha(m)
    png=RENDERS+name+'.png'; im.save(png)
    subprocess.run(['cwebp','-quiet','-q','86','-alpha_q','100',png,'-o',OUT+name+'.webp'],check=True)
    print(name)

# steps (708x398 slot, @2x)
slot('step_phone_app','step-1-book',1416,796,0.55,0.32)
slot('br_step_member','step-2-matched',1416,796,0.5,0.3)
slot('br_step_keys','step-3-keys',1416,796,0.5,0.45)
slot('br_step_day','step-4-reset',1416,796,0.5,0.45)
slot('br_step_home','step-5-note',1416,796,0.45,0.5)
# more ways (720x480 slot, @2x)
slot('br_more_move','more-moving',1440,960,0.5,0.4)
slot('br_more_host','more-hosting',1440,960,0.5,0.45)
