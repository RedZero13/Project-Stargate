"""App icons + mouse cursor in the logo-B style (own art). Writes:
- HollowKin/Build/Mac/Resources/Assets.xcassets/AppIcon.appiconset/*.png (+ Contents.json) - packaged Mac app icon
- HollowKin/Build/IOS/Resources/Assets.xcassets/AppIcon.appiconset/*.png - iPad/iPhone icon (full-bleed, no alpha;
  iOS rounds the corners itself). Without it the iPad app shows the Unreal logo.
- HollowKin/Build/Windows/Application.ico - Windows build icon
- marketing/icon/HollowKin_Icon_1024.png
- HollowKin/SourceArt/T_Cursor.png (64x64, hotspot top-left) - imported as the in-game cursor."""
import os, json, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
R = os.path.join(os.path.dirname(__file__), '..')
RED = (165, 20, 28); WHITE = (226, 232, 228); TEAL = (95, 163, 154); BG = (11, 15, 16)
F = lambda n, s: ImageFont.truetype('/System/Library/Fonts/Supplemental/' + n, s)
random.seed(3)
def icon(S=1024):
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pad = int(S * 0.06); rad = int(S * 0.2)
    d.rounded_rectangle((pad, pad, S - pad, S - pad), radius=rad, fill=BG + (255,), outline=(40, 52, 54, 255), width=max(2, S // 128))
    # stencil HK
    f = F('DIN Condensed Bold.ttf', int(S * 0.48))
    mask = Image.new('L', (S, S), 0); md = ImageDraw.Draw(mask)
    gap = S * 0.05; wh = md.textlength('H', font=f); wk = md.textlength('K', font=f); bb = md.textbbox((0, 0), 'HK', font=f)
    x0 = (S - (wh + gap + wk)) / 2; y0 = S * 0.5 - (bb[1] + bb[3]) / 2
    md.text((x0, y0), 'H', font=f, fill=255); md.text((x0 + wh + gap, y0), 'K', font=f, fill=255)
    cut = Image.new('L', (S, S), 255); ImageDraw.Draw(cut).rectangle((0, S * 0.5 - S * 0.012, S, S * 0.5 + S * 0.012), fill=0)
    mask = ImageChops.multiply(mask, cut)
    noise = Image.effect_noise((S, S), 90).filter(ImageFilter.GaussianBlur(S / 900)).point(lambda v: 0 if v < 62 else 255)
    mask = ImageChops.multiply(mask, noise)
    letters = Image.new('RGBA', (S, S), WHITE + (255,)); letters.putalpha(mask)
    # ECG
    e = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ed = ImageDraw.Draw(e); y = S * 0.5
    pts = [(pad * 2, y), (S * 0.36, y), (S * 0.40, y - S * 0.05), (S * 0.44, y + S * 0.13), (S * 0.49, y - S * 0.28), (S * 0.54, y + S * 0.08), (S * 0.58, y), (S - pad * 2, y)]
    ed.line(pts, fill=RED + (255,), width=max(2, S // 70), joint='curve')
    e = Image.alpha_composite(e.filter(ImageFilter.GaussianBlur(S / 90)), e)
    # small cracked cross top-left
    c = Image.new('RGBA', (S, S), (0, 0, 0, 0)); cd = ImageDraw.Draw(c); cx, cy, s = S * 0.24, S * 0.24, S * 0.07
    cd.rectangle((cx - s / 3, cy - s, cx + s / 3, cy + s), fill=RED + (255,)); cd.rectangle((cx - s, cy - s / 3, cx + s, cy + s / 3), fill=RED + (255,))
    cd.line((cx - s, cy - s * 0.2, cx, cy + s * 0.1, cx + s * 0.3, cy - s * 0.4, cx + s, cy + s * 0.1), fill=BG + (255,), width=max(1, S // 200))
    for l in (letters, e, c): im = Image.alpha_composite(im, l)
    return im
big = icon(1024)
os.makedirs(os.path.join(R, 'marketing', 'icon'), exist_ok=True)
big.save(os.path.join(R, 'marketing', 'icon', 'HollowKin_Icon_1024.png'))
iconset = os.path.join(R, 'HollowKin', 'Build', 'Mac', 'Resources', 'Assets.xcassets', 'AppIcon.appiconset')
os.makedirs(iconset, exist_ok=True)
images = []
for size in (16, 32, 128, 256, 512):
    for scale in (1, 2):
        px = size * scale; name = 'icon_%dx%d%s.png' % (size, size, '@2x' if scale == 2 else '')
        big.resize((px, px), Image.LANCZOS).save(os.path.join(iconset, name))
        images.append({'filename': name, 'idiom': 'mac', 'scale': '%dx' % scale, 'size': '%dx%d' % (size, size)})
json.dump({'images': images, 'info': {'author': 'xcode', 'version': 1}}, open(os.path.join(iconset, 'Contents.json'), 'w'), indent=2)
xc = os.path.join(R, 'HollowKin', 'Build', 'Mac', 'Resources', 'Assets.xcassets', 'Contents.json')
if not os.path.exists(xc): json.dump({'info': {'author': 'xcode', 'version': 1}}, open(xc, 'w'), indent=2)
os.makedirs(os.path.join(R, 'HollowKin', 'Build', 'Windows'), exist_ok=True)
big.save(os.path.join(R, 'HollowKin', 'Build', 'Windows', 'Application.ico'), sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
# iOS: full-bleed square without transparency (crop the inner plate, flatten on the background colour)
ios = os.path.join(R, 'HollowKin', 'Build', 'IOS', 'Resources', 'Assets.xcassets', 'AppIcon.appiconset')
os.makedirs(ios, exist_ok=True)
pad = int(1024 * 0.06) + 4
full = Image.new('RGBA', (1024, 1024), BG + (255,))
full.alpha_composite(big.crop((pad, pad, 1024 - pad, 1024 - pad)).resize((1024, 1024), Image.LANCZOS))
full = full.convert('RGB')
IOS = [('IPhoneIcon60@2x.png', 120, '60x60', 'iphone', '2x'), ('IPadIcon76@2x.png', 152, '76x76', 'ipad', '2x'),
       ('IPadIcon83.5@2x.png', 167, '83.5x83.5', 'ipad', '2x'), ('Icon1024.png', 1024, '1024x1024', 'ios-marketing', '1x')]
for name, px, size, idiom, scale in IOS:
    full.resize((px, px), Image.LANCZOS).save(os.path.join(ios, name))
json.dump({'images': [{'size': sz, 'idiom': idm, 'filename': n, 'scale': sc} for n, px, sz, idm, sc in IOS], 'info': {'version': 1, 'author': 'xcode'}},
          open(os.path.join(ios, 'Contents.json'), 'w'), indent=2)
xi = os.path.join(R, 'HollowKin', 'Build', 'IOS', 'Resources', 'Assets.xcassets', 'Contents.json')
if not os.path.exists(xi): json.dump({'info': {'author': 'xcode', 'version': 1}}, open(xi, 'w'), indent=2)
# cursor: clinical arrow, teal outline, amber tip dot
S = 64; cur = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(cur)
arrow = [(2, 2), (2, 46), (14, 35), (22, 54), (30, 50), (22, 32), (38, 32)]
d.polygon(arrow, fill=(11, 15, 16, 235), outline=TEAL + (255,))
d.line(arrow + [arrow[0]], fill=TEAL + (255,), width=3)
d.ellipse((0, 0, 7, 7), fill=(224, 165, 71, 255))
cur.save(os.path.join(R, 'HollowKin', 'SourceArt', 'T_Cursor.png'))
print('icons + cursor written')
