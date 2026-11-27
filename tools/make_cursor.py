"""HOLLOW KIN mouse cursor: a small syringe pointing up-left (needle tip = hotspot), steel needle, glass barrel with
a dark-red dose, teal plunger and finger grips. Drawn 8x larger and downsampled for smooth edges.
Writes HollowKin/SourceArt/T_Cursor.png (32x32) and HollowKin/Content/Slate/Cursors/HK_Arrow.png (loose file the
packaged game loads as its hardware cursor), plus a 4x preview in marketing/icon/cursor_preview.png.
Run with a Python that has Pillow."""
import os, math
from PIL import Image, ImageDraw
R = os.path.join(os.path.dirname(__file__), '..')
S, K = 32, 8                      # final size, supersample factor
W = S * K
im = Image.new('RGBA', (W, W), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
ang = math.radians(45)            # syringe axis runs from the tip (top-left) to the bottom-right
ux, uy = math.cos(ang), math.sin(ang)
px, py = -uy, ux                  # perpendicular
def P(t, s):                      # point at distance t along the axis, s across it (in final px)
    return ((1.2 + t * ux + s * px) * K, (1.2 + t * uy + s * py) * K)
def quad(t0, t1, w0, w1, fill, outline=None, width=0):
    pts = [P(t0, -w0), P(t1, -w1), P(t1, w1), P(t0, w0)]
    d.polygon(pts, fill=fill)
    if outline: d.line(pts + [pts[0]], fill=outline, width=width)
OUT = (8, 10, 11, 255)
# dark outline pass (slightly fatter shapes) so it reads on light and dark scenes
quad(0, 9, 1.1, 1.1, OUT)                 # needle
quad(8.5, 11, 2.2, 2.2, OUT)              # hub
quad(10.5, 25, 3.6, 3.6, OUT)             # barrel
quad(24.5, 26.5, 5.6, 5.6, OUT)           # finger grips
quad(26, 33, 1.6, 1.6, OUT)               # plunger rod
quad(32.5, 35, 3.4, 3.4, OUT)             # plunger cap
# colour pass
quad(0.4, 9, 0.35, 0.45, (205, 214, 214, 255))            # steel needle
quad(9, 11, 1.4, 1.4, (150, 160, 160, 255))               # hub
quad(11, 24.6, 2.8, 2.8, (190, 214, 210, 150))            # glass barrel
quad(11.3, 19.5, 2.2, 2.2, (150, 16, 22, 255))            # dark red dose
quad(19.5, 20.6, 2.6, 2.6, (40, 52, 54, 255))             # rubber stopper
for k in range(3):                                        # graduation marks
    a, b = P(13.5 + k * 2.5, -2.8), P(13.5 + k * 2.5, -1.2)
    d.line([a, b], fill=(235, 240, 238, 200), width=K // 2)
quad(25, 26, 4.8, 4.8, (95, 163, 154, 255))               # teal grips
quad(26, 32.6, 0.8, 0.8, (95, 163, 154, 255))             # plunger rod
quad(33, 34.6, 2.6, 2.6, (95, 163, 154, 255))             # plunger cap
r = 1.1 * K                                               # blood bead at the tip
cx, cy = P(0.6, 0)
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(196, 24, 30, 255))
cur = im.resize((S, S), Image.LANCZOS)
for path in (os.path.join(R, 'HollowKin', 'SourceArt', 'T_Cursor.png'),
             os.path.join(R, 'HollowKin', 'Content', 'Slate', 'Cursors', 'HK_Arrow.png')):
    os.makedirs(os.path.dirname(path), exist_ok=True); cur.save(path)
prev = Image.new('RGBA', (S * 4 * 2, S * 4), (0, 0, 0, 0))
prev.paste((30, 34, 36, 255), (0, 0, S * 4, S * 4)); prev.paste((214, 220, 218, 255), (S * 4, 0, S * 8, S * 4))
big = cur.resize((S * 4, S * 4), Image.NEAREST)
prev.alpha_composite(big, (0, 0)); prev.alpha_composite(big, (S * 4, 0))
os.makedirs(os.path.join(R, 'marketing', 'icon'), exist_ok=True)
prev.save(os.path.join(R, 'marketing', 'icon', 'cursor_preview.png'))
print('cursor written')
