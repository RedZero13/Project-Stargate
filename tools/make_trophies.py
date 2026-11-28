"""Trophy badges for the Achievements screen (own art). One 256x256 PNG per achievement in
HollowKin/SourceArt/Trophies/T_Trophy_<id>.png: a medal (ring + glyph by category). Locked state is drawn in-game by
tinting the same image dark, so only one image per achievement is needed. Re-run after editing achievements_data.ACH."""
import os, sys, math
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'unreal_mcp'))
from achievements_data import ACH
R = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(R, 'HollowKin/SourceArt/Trophies'); os.makedirs(OUT, exist_ok=True)
S = 256; C = S / 2
# tier colours: bronze / silver / gold / red (secret)
TIER = {'bronze': ((176, 116, 66), (92, 56, 30)), 'silver': ((200, 208, 206), (92, 104, 104)),
        'gold': ((226, 184, 92), (120, 86, 28)), 'red': ((196, 44, 52), (90, 16, 22))}
GOLD = {'all_endings', 'drawings_all', 'files_all', 'kills_50', 'cells', 'isolation'}
SILVER = {'deep_labs', 'absolution', 'last_stand', 'whistle', 'elite', 'crafter', 'serum', 'end_lantern', 'end_kin',
          'end_home', 'end_hollow', 'end_six', 'end_lullaby'}
def tier(i):
    if i == 'end_true': return 'red'
    return 'gold' if i in GOLD else 'silver' if i in SILVER else 'bronze'
def glyph(i):
    if i.startswith('end_') or i == 'all_endings' or i == 'cells': return 'door'
    if i.startswith('drawings'): return 'crayon'
    if i.startswith('files'): return 'paper'
    if i.startswith('kills') or i == 'elite' or i == 'darkened': return 'skull'
    return {'first_light': 'gun', 'lights_on': 'bolt', 'electrician': 'bolt', 'mercy': 'heart', 'going_down': 'arrow',
            'deep_labs': 'arrow', 'isolation': 'arrow', 'absolution': 'heart', 'last_stand': 'bullet', 'whistle': 'radio',
            'safecracker': 'dial', 'serum': 'syringe', 'crafter': 'cross'}.get(i, 'star')
def draw_glyph(d, g, col, sh):
    k = S / 256
    P = lambda pts: [(x * k, y * k) for x, y in pts]
    if g == 'door':
        d.rectangle(P([(98, 70), (158, 186)]), outline=col, width=int(9 * k)); d.ellipse(P([(140, 124), (150, 134)]), fill=col)
    elif g == 'crayon':
        d.polygon(P([(84, 172), (150, 88), (172, 106), (106, 190)]), fill=col); d.polygon(P([(150, 88), (166, 66), (172, 106)]), fill=sh)
    elif g == 'paper':
        d.rectangle(P([(92, 66), (164, 190)]), fill=col)
        for y in (92, 112, 132, 152): d.line(P([(104, y), (152, y)]), fill=sh, width=int(6 * k))
    elif g == 'skull':
        d.ellipse(P([(86, 66), (170, 150)]), fill=col); d.rectangle(P([(104, 140), (152, 178)]), fill=col)
        d.ellipse(P([(102, 98), (124, 120)]), fill=sh); d.ellipse(P([(132, 98), (154, 120)]), fill=sh)
        for x in (114, 128, 142): d.line(P([(x, 160), (x, 178)]), fill=sh, width=int(5 * k))
    elif g == 'bolt':
        d.polygon(P([(140, 60), (96, 136), (126, 136), (112, 196), (162, 112), (130, 112)]), fill=col)
    elif g == 'heart':
        d.ellipse(P([(82, 84), (132, 134)]), fill=col); d.ellipse(P([(124, 84), (174, 134)]), fill=col)
        d.polygon(P([(86, 118), (170, 118), (128, 180)]), fill=col)
    elif g == 'arrow':
        d.rectangle(P([(116, 64), (140, 140)]), fill=col); d.polygon(P([(88, 132), (168, 132), (128, 188)]), fill=col)
    elif g == 'bullet':
        d.rectangle(P([(110, 110), (146, 186)]), fill=col); d.pieslice(P([(110, 70), (146, 150)]), 180, 360, fill=col)
        d.line(P([(110, 172), (146, 172)]), fill=sh, width=int(5 * k))
    elif g == 'radio':
        d.rectangle(P([(92, 104), (164, 184)]), fill=col); d.line(P([(140, 104), (160, 62)]), fill=col, width=int(7 * k))
        d.ellipse(P([(104, 124), (136, 156)]), fill=sh)
    elif g == 'dial':
        d.ellipse(P([(80, 80), (176, 176)]), outline=col, width=int(10 * k)); d.line(P([(128, 128), (128, 94)]), fill=col, width=int(9 * k))
        for a in range(0, 360, 45):
            r1, r2 = 54, 62; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            d.line(P([(128 + r1 * ca, 128 + r1 * sa), (128 + r2 * ca, 128 + r2 * sa)]), fill=col, width=int(4 * k))
    elif g == 'syringe':
        d.polygon(P([(96, 170), (150, 98), (166, 110), (112, 182)]), fill=col); d.line(P([(158, 104), (184, 72)]), fill=col, width=int(5 * k))
        d.line(P([(88, 178), (100, 188)]), fill=col, width=int(8 * k))
    elif g == 'cross':
        d.rectangle(P([(112, 72), (144, 184)]), fill=col); d.rectangle(P([(72, 112), (184, 144)]), fill=col)
    elif g == 'gun':
        d.rectangle(P([(76, 96), (180, 122)]), fill=col); d.polygon(P([(132, 118), (164, 118), (152, 176), (124, 176)]), fill=col)
    else:
        pts = [(128 + (60 if j % 2 == 0 else 26) * math.cos(math.radians(-90 + j * 36)),
                128 + (60 if j % 2 == 0 else 26) * math.sin(math.radians(-90 + j * 36))) for j in range(10)]
        d.polygon(P(pts), fill=col)
def badge(i):
    hi, lo = TIER[tier(i)]
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # soft shadow
    sh = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((18, 22, S - 14, S - 10), fill=(0, 0, 0, 150))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(8))); d = ImageDraw.Draw(im)
    d.ellipse((14, 14, S - 14, S - 14), fill=lo + (255,))
    d.ellipse((22, 22, S - 22, S - 22), fill=hi + (255,))
    d.ellipse((34, 34, S - 34, S - 34), fill=(16, 20, 21, 255))
    d.ellipse((40, 40, S - 40, S - 40), outline=lo + (255,), width=3)
    # notches round the rim
    for a in range(0, 360, 15):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.line((C + 104 * ca, C + 104 * sa, C + 112 * ca, C + 112 * sa), fill=lo + (255,), width=3)
    draw_glyph(d, glyph(i), hi + (255,), (16, 20, 21, 255))
    return im
if __name__ == '__main__':
    for i, t, _ in ACH:
        badge(i).save(os.path.join(OUT, 'T_Trophy_%s.png' % i))
    # contact sheet for review
    sheet = Image.new('RGBA', (6 * 140, 5 * 140), (11, 15, 16, 255))
    for n, (i, t, _) in enumerate(ACH):
        sheet.alpha_composite(badge(i).resize((128, 128), Image.LANCZOS), (6 + (n % 6) * 140, 6 + (n // 6) * 140))
    sheet.save(os.path.join(OUT, '_sheet.png')); print('wrote', len(ACH), 'badges to', OUT)
