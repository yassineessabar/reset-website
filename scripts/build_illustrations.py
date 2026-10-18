"""Brand illustrations for the slots that used stock photos, drawn in the RESET app's own language:
arch-framed rooms and objects (never cleaning tools, never people), the app palette, on the pale blue tint.
Scenes LIVING, BED and DOOR are copied from the app flow prototype; LAUNDRY, EARN_KIT, EARN_PHONE and
OFFICE are new, built from the same shapes and colours."""
import base64, os, subprocess
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

from paths import REPO, IMG as OUT, RENDERS, DESIGN
TMP = DESIGN + 'scenes/'
os.makedirs(TMP, exist_ok=True)
TINT = (234, 240, 254)          # app tint #EAF0FE
ARCH_BG = '#EEF2FB'

FLOOR = '<rect y="232" width="270" height="70" fill="#E3B888"/><path d="M0 252h270M60 232l-12 70M135 232v70M210 232l12 70" stroke="#CF9E68" stroke-width="2.5"/>'
PLANT = lambda x: (f'<path d="M{x} 232l5-30h26l5 30z" fill="#fff"/><path d="M{x+18} 202c0-22 10-34 22-36 0 18-9 32-22 36z" fill="#2BB673"/>'
                   f'<path d="M{x+18} 202c-2-18-12-28-24-28 1 15 10 26 24 28z" fill="#5CD18E"/><path d="M{x+18} 204c4-14 14-22 24-20-3 12-12 19-24 20z" fill="#1F9D5C"/>')
WINDOW = lambda x, y, w, h, sun=True: (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#CFE0FF"/>'
                                      f'<path d="M{x + w / 2} {y}v{h}M{x} {y + h / 2}h{w}" stroke="#fff" stroke-width="5"/>'
                                      + (f'<circle cx="{x + w * 0.78}" cy="{y + h * 0.24}" r="9" fill="#FFD66B"/>' if sun else ''))

def logo_uri(color='white'):
    svg = open(OUT + f'brand/reset-logo-{color}.svg').read()
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()

LIVING = (WINDOW(150, 62, 74, 96) + FLOOR +
  '<path d="M58 98h34l-8 24H66z" fill="#FFC44D"/><path d="M75 122v110" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round"/><path d="M62 232h26" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/><path d="M66 122h18l26 70H40z" fill="#FFE7A3" opacity=".45"/>'
  '<rect x="96" y="176" width="126" height="50" rx="16" fill="#E8775A"/><rect x="104" y="150" width="110" height="42" rx="14" fill="#F08D72"/><rect x="88" y="182" width="22" height="44" rx="10" fill="#D9634A"/><rect x="208" y="182" width="22" height="44" rx="10" fill="#D9634A"/><path d="M110 226v8M208 226v8" stroke="#7A3A2A" stroke-width="5" stroke-linecap="round"/>'
  '<rect x="132" y="158" width="34" height="26" rx="8" fill="#FFF3E6" transform="rotate(-8 149 171)"/>'
  + PLANT(226) +
  '<g transform="rotate(-6 60 260)"><rect x="28" y="246" width="70" height="40" rx="5" fill="#fff"/><rect x="36" y="256" width="40" height="5" rx="2.5" fill="#000" opacity=".8"/><rect x="36" y="266" width="28" height="4" rx="2" fill="#000" opacity=".35"/></g>')

BED = (FLOOR +
  '<rect x="160" y="58" width="74" height="86" rx="6" fill="#FFD9B0"/><circle cx="198" cy="112" r="14" fill="#FFB25C"/><path d="M197 58v86M160 100h74" stroke="#fff" stroke-width="5"/>'
  '<rect x="24" y="128" width="150" height="70" rx="16" fill="#8DB2FF"/>'
  '<rect x="18" y="182" width="164" height="22" rx="8" fill="#fff"/><rect x="18" y="194" width="164" height="36" rx="10" fill="#C9D9FF"/><path d="M18 206h164" stroke="#B3C8FA" stroke-width="2"/>'
  '<rect x="34" y="160" width="56" height="28" rx="11" fill="#fff"/><rect x="98" y="160" width="56" height="28" rx="11" fill="#fff"/>'
  '<rect x="126" y="196" width="44" height="9" rx="3.5" fill="#8C6CF7"/><rect x="129" y="188" width="38" height="9" rx="3.5" fill="#B9A6FF"/>'
  '<path d="M30 230v8M170 230v8" stroke="#6E4A2B" stroke-width="5" stroke-linecap="round"/>'
  '<rect x="196" y="186" width="50" height="46" rx="5" fill="#fff"/><rect x="200" y="204" width="42" height="3" fill="#EEE"/><path d="M209 152h24l-5 16h-14z" fill="#FFC44D"/><path d="M221 168v18" stroke="#2B2B2B" stroke-width="3"/>')

DOOR = (FLOOR +
  '<rect x="88" y="62" width="104" height="172" rx="6" fill="#fff"/><rect x="96" y="70" width="88" height="164" rx="4" fill="#F2B544"/>'
  '<rect x="106" y="82" width="68" height="62" rx="4" fill="#E39E2B"/><rect x="106" y="154" width="68" height="66" rx="4" fill="#E39E2B"/>'
  '<circle cx="170" cy="152" r="5" fill="#7A4E0F"/><rect x="100" y="234" width="80" height="9" rx="4.5" fill="#9B6A3C"/>'
  '<rect x="26" y="80" width="48" height="52" rx="6" fill="#fff"/><path d="M26 86a6 6 0 016-6h36a6 6 0 016 6v8H26z" fill="#FF5A4F"/>'
  '<text x="50" y="122" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="24" fill="#111">15</text>'
  '<circle cx="72" cy="80" r="11" fill="#06C167"/><path d="M66.5 80.5l3.6 3.6 6.8-7" stroke="#fff" stroke-width="2.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
  '<path d="M48 152v14" stroke="#8C99AA" stroke-width="3" stroke-linecap="round"/><circle cx="48" cy="174" r="7" fill="none" stroke="#FFB800" stroke-width="4"/><rect x="46" y="179" width="4" height="16" rx="2" fill="#FFB800"/>'
  + PLANT(210))

# --- new: laundry (washing machine, basket of folded towels, towel shelf) ---
LAUNDRY = (WINDOW(30, 62, 68, 80) + FLOOR +
  '<rect x="150" y="98" width="96" height="6" rx="3" fill="#C68A4E"/>'
  '<rect x="158" y="86" width="38" height="12" rx="4" fill="#B9A6FF"/><rect x="161" y="76" width="32" height="11" rx="4" fill="#DDD3FF"/>'
  '<rect x="204" y="86" width="36" height="12" rx="4" fill="#FFD9B0"/><rect x="207" y="76" width="30" height="11" rx="4" fill="#F7B48F"/>'
  '<rect x="112" y="138" width="96" height="96" rx="12" fill="#fff"/><rect x="112" y="138" width="96" height="22" rx="10" fill="#F1F4FA"/>'
  '<circle cx="192" cy="149" r="5" fill="#C3C9D3"/><rect x="124" y="146" width="28" height="6" rx="3" fill="#DDE3EC"/>'
  '<circle cx="160" cy="194" r="31" fill="#DDE3EC"/><circle cx="160" cy="194" r="24" fill="#BFE6FF"/>'
  '<path d="M137 198c8-6 15 6 23 0s15 6 23 0v5a24 24 0 01-46 0z" fill="#4FB3EF"/><circle cx="152" cy="186" r="3" fill="#fff" opacity=".9"/>'
  '<path d="M22 186h80l-8 46H30z" fill="#E8B47E"/><path d="M22 186h80" stroke="#C68A4E" stroke-width="4" stroke-linecap="round"/>'
  '<path d="M38 194l4 34M54 194l2 34M70 194v34M86 194l-2 34" stroke="#C68A4E" stroke-width="2" opacity=".7"/>'
  '<rect x="34" y="172" width="56" height="13" rx="5" fill="#F08D72"/><rect x="40" y="161" width="46" height="12" rx="5" fill="#FFD9B0"/>'
  + PLANT(214))

# --- new: clean and earn (calendar, RESET kit bag on a bench, keys) ---
EARN_KIT = (WINDOW(156, 56, 74, 90) + FLOOR +
  '<rect x="26" y="66" width="84" height="88" rx="8" fill="#fff"/><path d="M26 74a8 8 0 018-8h68a8 8 0 018 8v10H26z" fill="#FF5A4F"/>'
  + ''.join(f'<rect x="{38 + c * 22}" y="{94 + r * 18}" width="14" height="12" rx="3" fill="{"#06C167" if (r, c) == (1, 1) else "#EEF2FB"}"/>' for r in range(3) for c in range(3)) +
  '<path d="M63.5 106.5l3 3 5.5-6" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
  '<rect x="30" y="202" width="210" height="10" rx="4" fill="#9B6A3C"/><path d="M44 212v20M226 212v20" stroke="#6E4A2B" stroke-width="6" stroke-linecap="round"/>'
  '<path d="M138 140c0-22 52-22 52 0" fill="none" stroke="#0E0E0E" stroke-width="6"/>'
  '<path d="M118 140h92l-8 62h-76z" fill="#0E0E0E"/>'
  f'<image href="{logo_uri("white")}" x="137" y="160" width="54" height="18"/>'
  '<circle cx="64" cy="190" r="7" fill="none" stroke="#FFB800" stroke-width="4"/><rect x="69" y="188" width="18" height="4" rx="2" fill="#FFB800"/><rect x="80" y="191" width="3" height="5" rx="1" fill="#FFB800"/>'
  '<path d="M214 202l3-18h20l3 18z" fill="#fff"/><path d="M227 184c0-14 6-22 14-23 0 12-6 21-14 23z" fill="#2BB673"/><path d="M227 184c-1-12-8-18-16-18 1 10 7 17 16 18z" fill="#5CD18E"/>')

# --- new: work when you want (phone with an accepted visit, coffee, clock, sunny window) ---
EARN_PHONE = (WINDOW(30, 60, 84, 96) + FLOOR +
  '<circle cx="204" cy="96" r="28" fill="#fff"/><circle cx="204" cy="96" r="28" fill="none" stroke="#2B2B2B" stroke-width="4"/>'
  '<path d="M204 96V80M204 96l11 7" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round"/><circle cx="204" cy="96" r="3" fill="#2B2B2B"/>'
  '<rect x="112" y="206" width="140" height="10" rx="4" fill="#fff"/><path d="M126 216v16M238 216v16" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>'
  '<rect x="128" y="108" width="60" height="100" rx="11" fill="#111"/><rect x="133" y="113" width="50" height="90" rx="7" fill="#3B6CF0"/>'
  '<rect x="138" y="140" width="40" height="34" rx="6" fill="#fff"/><circle cx="149" cy="152" r="6" fill="#06C167"/>'
  '<path d="M146 152l2 2 4-4.5" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
  '<rect x="158" y="148" width="15" height="3.5" rx="1.75" fill="#111" opacity=".8"/><rect x="143" y="163" width="30" height="3" rx="1.5" fill="#111" opacity=".3"/>'
  '<rect x="208" y="180" width="26" height="26" rx="5" fill="#F08D72"/><path d="M234 186a7 7 0 010 14" fill="none" stroke="#F08D72" stroke-width="4"/>'
  '<path d="M215 172c0-4 4-4 4-8M225 172c0-4 4-4 4-8" stroke="#C3C9D3" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
  + PLANT(40).replace('M40 232', 'M40 232'))

# --- new: office (city window, desk, laptop, chair, plant) ---
OFFICE = ('<rect x="28" y="56" width="214" height="96" rx="6" fill="#CFE0FF"/>'
  '<path d="M44 152v-40h22v40M72 152v-58h26v58M104 152v-32h18v32M128 152v-50h24v50M158 152v-38h20v38M184 152v-62h26v62M216 152v-28h18v28" fill="#A9C4F5"/>'
  '<path d="M99 56v96M171 56v96M28 104h214" stroke="#fff" stroke-width="5"/><circle cx="214" cy="76" r="9" fill="#FFD66B"/>'
  + FLOOR +
  '<rect x="34" y="172" width="150" height="10" rx="4" fill="#fff"/><path d="M48 182v50M170 182v50" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>'
  '<rect x="76" y="136" width="62" height="36" rx="4" fill="#2B2B2B"/><rect x="80" y="140" width="54" height="28" rx="2" fill="#8DB2FF"/><rect x="68" y="170" width="78" height="4" rx="2" fill="#C3C9D3"/>'
  '<rect x="150" y="156" width="16" height="16" rx="3" fill="#FFF3E6"/><path d="M166 160a5 5 0 010 9" fill="none" stroke="#FFF3E6" stroke-width="3"/>'
  '<rect x="186" y="150" width="14" height="48" rx="6" fill="#F08D72"/><rect x="164" y="190" width="44" height="14" rx="6" fill="#E8775A"/><path d="M186 204v26M176 230h20" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round"/>'
  + PLANT(216))

def arch_svg(scene, key, size=1000):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size * 270 // 300}" height="{size}" viewBox="0 0 270 300">'
            f'<defs><clipPath id="c{key}"><path d="M20 300V125a115 115 0 01230 0v175z"/></clipPath></defs>'
            f'<g clip-path="url(#c{key})"><rect width="270" height="300" fill="{ARCH_BG}"/>{scene}</g>'
            f'<path d="M20 300V125a115 115 0 01230 0v175" fill="none" stroke="#fff" stroke-width="6"/></svg>')

def render(scene, key, h):
    svg = TMP + key + '.svg'; png = TMP + key + '.png'
    open(svg, 'w').write(arch_svg(scene, key))
    subprocess.run(['rsvg-convert', '-h', str(h), svg, '-o', png], check=True)
    return Image.open(png).convert('RGBA')

def shadow(im, blur=26, alpha=70, dy=10):
    a = np.asarray(im)[:, :, 3]
    sh = Image.new('RGBA', im.size, (40, 70, 160, 0)); sh.putalpha(Image.fromarray((a * (alpha / 255)).astype(np.uint8)))
    return sh.filter(ImageFilter.GaussianBlur(blur)), dy

def card(scene, key, w, h, arch_h, name):
    bg = Image.new('RGBA', (w, h), TINT + (255,))
    a = render(scene, key, arch_h)
    x = (w - a.width) // 2; y = h - a.height
    sh, dy = shadow(a); bg.alpha_composite(sh, (x, y - dy + 6)); bg.alpha_composite(a, (x, y))
    path = OUT + name; png = RENDERS + name.replace('.webp', '.png'); bg.convert('RGB').save(png)
    subprocess.run(['cwebp', '-quiet', '-q', '88', png, '-o', path], check=True)
    return path

# service cards (576x384 @2x)
card(LAUNDRY, 'laundry', 1152, 768, 700, 'card-laundry.webp')
card(BED, 'linen', 1152, 768, 700, 'card-linen.webp')
# earn cards (576x324 @2x)
card(EARN_KIT, 'earnkit', 1152, 647, 600, 'earn-team.webp')
card(EARN_PHONE, 'earnphone', 1152, 647, 600, 'earn-flexible.webp')

# wide banner: the three rooms of the app, side by side (1152x270 @2x -> 2304x540)
bg = Image.new('RGBA', (2304, 540), TINT + (255,))
for i, (scene, key) in enumerate(((LIVING, 'bn1'), (BED, 'bn2'), (DOOR, 'bn3'))):
    a = render(scene, key, 500)
    x = 2304 // 2 + (i - 1) * 560 - a.width // 2
    sh, dy = shadow(a); bg.alpha_composite(sh, (x, 540 - a.height - dy + 6)); bg.alpha_composite(a, (x, 540 - a.height))
bg.convert('RGB').save(RENDERS + '_banner.png'); subprocess.run(['cwebp', '-quiet', '-q', '88', RENDERS + '_banner.png', '-o', OUT + 'banner-bucket.webp'], check=True); os.remove(RENDERS + '_banner.png')

# business: the office arch with the three 3D tiles in front (576x576 @2x, same geometry as before)
code = open(REPO + 'scripts/build_assets.py').read(); g = {}
exec(code[:code.index('# ---------- hero collage')], g)
S = 2; W = 576 * S
im = Image.new('RGBA', (W, W), (0, 0, 0, 0))
a = render(OFFICE, 'office', 880)
sh, dy = shadow(a); im.alpha_composite(sh, ((W - a.width) // 2, 40 - dy + 6)); im.alpha_composite(a, ((W - a.width) // 2, 40))
for x0, icon in [(20, 'office'), (205, 'chart'), (391, 'clipboard')]:
    tw, th = 166 * S, 158 * S; ty = 372 * S
    tile = Image.new('RGBA', (tw, th), g['INDIGO_UP'] + (250,)); tile.putalpha(g['rmask'](tw, th, 16 * S))
    ImageDraw.Draw(tile).rounded_rectangle([1, 1, tw - 2, th - 2], 16 * S, outline=g['INDIGO_LINE'] + (255,), width=2)
    ic = g['brand_icon'](g['ICO'] + icon + '.png').resize((96 * S, 96 * S), Image.LANCZOS)
    tile.alpha_composite(ic, ((tw - ic.width) // 2, (th - ic.height) // 2))
    im.alpha_composite(tile, (x0 * S, ty))
im.save(RENDERS + '_business.png'); subprocess.run(['cwebp', '-quiet', '-q', '88', '-alpha_q', '100', RENDERS + '_business.png', '-o', OUT + 'business.webp'], check=True); os.remove(RENDERS + '_business.png')
print('illustrations built')
