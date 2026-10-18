"""Insert the blue RESET app showcase into index.html, just above "It's easier in the apps". Idempotent."""
import re
from paths import PUBLIC as ROOT, CONTENT
s=open(ROOT+'index.html').read()
block=open(CONTENT+'app-section.html').read().strip()
WM='<span class="rs-wm" role="img" aria-label="RESET"><span class="rs-vh">RESET</span></span>'
block=re.sub(r'>([^<>]*\bRESET\b[^<>]*)<',lambda m:'>'+m.group(1).replace('RESET',WM)+'<',block)
s=re.sub(r'<div data-block-content-id="reset-app-showcase".*?</section></div>','',s,flags=re.S)
i=s.index('data-block-id="MultiLink"'); i=s.rfind('<div',0,i)
s=s[:i]+block+s[i:]
# the QR section is the target of "Get the app"
if 'id="apps"' not in s:
    s=s.replace('data-block-id="MultiLink"','data-block-id="MultiLink" id="apps"',1)
open(ROOT+'index.html','w').write(s)
print('app showcase inserted')
