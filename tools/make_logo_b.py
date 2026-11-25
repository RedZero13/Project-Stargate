"""HOLLOW KIN logo, variant B (medical survival horror): distressed hospital-stencil wordmark, an ECG line that
spikes through the title and flatlines, a cracked red medical cross, blood drips from the letters and a
specimen-tag subtitle. Own art, no AI imagery. Writes SourceArt/T_Logo_HollowKin_B.png and a dark preview."""
import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
OUT = os.path.join(os.path.dirname(__file__), '..', 'HollowKin', 'SourceArt')
W, H = 2048, 900
WHITE = (226, 232, 228); RED = (150, 18, 24); DRED = (95, 8, 12); TEAL = (95, 163, 154); DIM = (120, 140, 136)
F = lambda n, s: ImageFont.truetype('/System/Library/Fonts/Supplemental/' + n, s)
random.seed(7)
def tracked(d, xy, text, font, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + track
    return x
def width(d, text, font, track): return sum(d.textlength(c, font=font) + track for c in text) - track
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
# --- wordmark (mask) -----------------------------------------------------------
mask = Image.new('L', (W, H), 0); md = ImageDraw.Draw(mask)
f = F('DIN Condensed Bold.ttf', 300); title = 'HOLLOW KIN'
wt = int(width(md, title, f, 38)); tx, ty = (W - wt) // 2, 210
tracked(md, (tx, ty), title, f, 255, 38)
# stencil bridges: thin horizontal cuts through every letter
for y in (ty + 150, ty + 152):
    pass
cut = Image.new('L', (W, H), 255); cd = ImageDraw.Draw(cut)
cd.rectangle((0, ty + 168, W, ty + 178), fill=0)
mask = ImageChops.multiply(mask, cut)
# distress: speckle erosion + scratches
noise = Image.effect_noise((W, H), 90).filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 0 if v < 70 else 255)
mask = ImageChops.multiply(mask, noise)
sd = ImageDraw.Draw(mask)
for _ in range(60):
    x = random.randint(tx, tx + int(wt)); y = random.randint(ty + 40, ty + 330); l = random.randint(20, 90); a = random.uniform(-0.5, 0.5)
    sd.line((x, y, x + l * math.cos(a), y + l * math.sin(a)), fill=0, width=random.choice((2, 3)))
letters = Image.new('RGBA', (W, H), WHITE + (255,)); letters.putalpha(mask)
# --- blood drips from a few letters --------------------------------------------
blood = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(blood)
bbox = mask.getbbox(); base_y = bbox[3] - 10          # bottom edge of the letters
cands = [x for x in range(tx, tx + wt) if mask.getpixel((x, base_y - 4)) > 0]
for k in range(9):
    x = random.choice(cands); L = random.randint(25, 120); w = random.randint(5, 10)
    bd.rounded_rectangle((x - w // 2, base_y - 6, x + w // 2, base_y + L), radius=w // 2, fill=RED + (230,))
    bd.ellipse((x - w, base_y + L - w, x + w, base_y + L + w), fill=RED + (230,))
blood = blood.filter(ImageFilter.GaussianBlur(0.8))
# --- ECG line: flat, spike in the middle of the title, then flatlines ----------------
ecg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ed = ImageDraw.Draw(ecg)
yb = ty + 175; x0, x1 = tx - 140, tx + int(wt) + 140
pts = [(x0, yb), (tx + wt * 0.30, yb), (tx + wt * 0.33, yb - 40), (tx + wt * 0.355, yb + 120), (tx + wt * 0.38, yb - 230),
       (tx + wt * 0.405, yb + 70), (tx + wt * 0.43, yb), (tx + wt * 0.55, yb), (tx + wt * 0.57, yb - 30), (tx + wt * 0.59, yb), (x1, yb)]
ed.line(pts, fill=RED + (255,), width=7, joint='curve')
glow = ecg.filter(ImageFilter.GaussianBlur(10)); ecg = Image.alpha_composite(glow, ecg)
# --- cracked medical cross, left of the title ----------------------------------------
cross = Image.new('RGBA', (W, H), (0, 0, 0, 0)); xd = ImageDraw.Draw(cross)
cx, cy, s = tx - 120, ty + 165, 46
xd.rectangle((cx - s // 3, cy - s, cx + s // 3, cy + s), fill=RED + (255,)); xd.rectangle((cx - s, cy - s // 3, cx + s, cy + s // 3), fill=RED + (255,))
xd.line((cx - s, cy - 10, cx - 4, cy + 4, cx + 10, cy - 18, cx + s, cy + 6), fill=(0, 0, 0, 0), width=4)
# --- specimen-tag subtitle ------------------------------------------------------------
tag = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tag)
f2 = F('DIN Alternate Bold.ttf', 40); sub = 'SUBJECT L-03   //   SURVIVAL HORROR   //   PROJECT LANTERN'
ws = int(width(td, sub, f2, 10)); sx, sy = (W - ws) // 2, ty + 450
bw = 200
sx -= (bw + 40) // 2
td.rectangle((sx - 30, sy - 16, sx + ws + bw + 70, sy + 60), outline=DIM + (200,), width=3)
for i in range(bw // 6):  # barcode inside the tag
    bx = sx + ws + 40 + i * 6
    td.rectangle((bx, sy - 4, bx + random.choice((1, 2, 3)), sy + 48), fill=DIM + (210,))
tracked(td, (sx, sy), sub, f2, TEAL + (235,), 10)
for layer in (ecg, letters, blood, cross, tag):
    img = Image.alpha_composite(img, layer)
img.save(os.path.join(OUT, 'T_Logo_HollowKin_B.png'))
for name in ('T_Logo_HollowKin', 'T_Logo_HollowKin_B'):
    src = Image.open(os.path.join(OUT, name + '.png')).convert('RGBA')
    bg = Image.new('RGBA', src.size, (11, 15, 16, 255)); Image.alpha_composite(bg, src).convert('RGB').save(os.path.join(OUT, name + '_preview.jpg'), quality=88)
print('ok')
