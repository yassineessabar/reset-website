"""Check that every local file the site references exists, and that nothing in public/assets is unused.

    python3 scripts/check_links.py      (exit code 1 on a broken reference)
"""
import os, re, sys
from paths import PUBLIC

refs = {}
for dp, _, fs in os.walk(PUBLIC):
    for f in fs:
        if not f.endswith(('.html', '.css', '.js')):
            continue
        fp = os.path.join(dp, f)
        t = open(fp, errors='ignore').read()
        found = re.findall(r'(?:src|href|poster)="([^"]+)"', t)
        for s in re.findall(r'srcset="([^"]+)"', t):
            found += [x.strip().split(' ')[0] for x in s.split(',')]
        found += re.findall(r'url\(["\']?([^"\')]+)["\']?\)', t)
        found += re.findall(r'["\']([^"\'\s]+\.(?:webp|png|svg|jpg|woff2))["\']', t)
        base = PUBLIC if f.endswith(('.js', '.html')) else dp   # JS paths resolve against the page
        for r in found:
            r = r.split('?')[0].split('#')[0]
            r = re.sub(r'^https://www\.resetcleaning\.app/', '', r)   # our own absolute URLs (og:image) are local files too
            if not r or re.match(r'^(https?:|data:|mailto:|tel:|//|javascript:)', r) or not re.search(r'\.\w{2,5}$', r):
                continue
            refs.setdefault(os.path.normpath(os.path.join(base, r)), set()).add(os.path.relpath(fp, PUBLIC))

broken = {p: s for p, s in refs.items() if not os.path.exists(p)}
assets = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(PUBLIC, 'assets')) for f in fs]
unused = [os.path.relpath(a, PUBLIC) for a in assets if a not in refs]

for p, s in sorted(broken.items()):
    print('BROKEN', os.path.relpath(p, PUBLIC), '<-', ', '.join(sorted(s)))
for u in sorted(unused):
    print('UNUSED', u)
print(f'{len(refs)} references, {len(broken)} broken, {len(unused)} unused assets')
sys.exit(1 if broken else 0)
