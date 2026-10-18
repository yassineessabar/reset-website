"""Put the RESET booking screen into the blank phone in step_phone.jpg -> src/step_phone_app.jpg.
The app is warped onto the screen quad and multiplied by the photo's light, so the thumb's
shadow falls on it; skin, frame and notch stay from the photo."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os
from paths import PHOTOS as SRC
APP=os.environ.get('RESET_APP_SCREEN', os.path.expanduser('~/Documents/GitHub/reset/brand/assets/png/app/03-book.png'))  # booking screen from the reset brand repo
photo=Image.open(SRC+'step_phone.jpg').convert('RGB'); W,H=photo.size
quad=[(842,452),(1550,420),(1538,2048),(782,2050)]   # TL TR BR BL of the screen glass
app=Image.open(APP).convert('RGB'); aw,ah=app.size
def coeffs(dst,src):
    A=[];B=[]
    for (x,y),(u,v) in zip(dst,src):
        A+= [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]; B+=[u,v]
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()
c=coeffs(quad,[(0,0),(aw,0),(aw,ah),(0,ah)])
warp=photo.copy(); warp=app.transform((W,H),Image.PERSPECTIVE,c,Image.BICUBIC)
# rounded screen mask
m=Image.new('L',(aw,ah),0); ImageDraw.Draw(m).rounded_rectangle([0,0,aw-1,ah-1],int(aw*0.12),fill=255)
mask=m.transform((W,H),Image.PERSPECTIVE,c,Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.2))
p=np.asarray(photo).astype(float); a=np.asarray(warp).astype(float); mk=np.asarray(mask).astype(float)/255
lum=p.mean(axis=2); sat=p.max(axis=2)-p.min(axis=2)
screenish=np.clip((lum-70)/60,0,1)*np.clip((70-sat)/25,0,1)        # bright-or-shadowed and neutral = glass
light=np.clip(lum/np.percentile(lum[mk>0.9],90),0,1.05)[...,None]   # photo light, incl. thumb shadow
comp=a*light
k=(mk*screenish)[...,None]
out=p*(1-k)+comp*k
Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(SRC+'step_phone_app.jpg',quality=92)
print('ok')
