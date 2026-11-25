#!/usr/bin/env python3
"""Draws architectural-style floor plans ("blueprints") of every generated floor from tools/floors_layout.py, so
the drawings always match the game. One sheet per floor + an overview sheet with all floors.
Writes docs/floorplans/<label>.png and docs/floorplans/ALL_FLOORS.png. Needs Pillow.
usage: python3 tools/draw_floorplans.py"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import floors_layout as FL
R = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(R, 'docs', 'floorplans'); os.makedirs(OUT, exist_ok=True)
SC = 0.5                                   # px per cm
PAD = 90
BG = (16, 38, 66); GRID = (28, 56, 92); LINE = (226, 238, 248); DIM = (150, 180, 210)
ZC = {'clinical': (52, 102, 160), 'support': (70, 120, 110), 'service': (78, 84, 96), 'staff': (110, 98, 70), 'core': (40, 52, 70)}
FONT = '/System/Library/Fonts/Supplemental/'
def f(n, s):
    for c in (n, 'Arial Bold.ttf', 'Arial.ttf'):
        try: return ImageFont.truetype(FONT + c, s)
        except Exception: pass
    return ImageFont.load_default()
F_T, F_R, F_S, F_X = f('Arial Bold.ttf', 30), f('Arial Bold.ttf', 15), f('Arial.ttf', 12), f('Arial.ttf', 10)
SYM = {'bed': 'BED', 'iv': 'IV', 'stretcher': 'STR', 'treat': 'TBL', 'xray': 'X-RAY', 'angio': 'MRI', 'angiomon': 'MON', 'anesth': 'ANS',
       'bloodtest': 'BLD', 'fume': 'FUME', 'micro': 'MIC', 'fridge': 'FRG', 'rack': 'RACK', 'reception': 'DESK', 'desk': 'DESK', 'bench': 'BENCH',
       'cabinet': 'CAB', 'bloodcab': 'BLD', 'washstand': 'WB', 'dentist': 'CHR', 'scanmon': 'MON', 'beddev': 'DEV', 'cylinder': 'O2', 'lift': 'LIFT'}
SIZE = {'bed': (95, 210), 'stretcher': (70, 200), 'treat': (80, 200), 'xray': (160, 160), 'angio': (220, 120), 'fume': (150, 75), 'rack': (150, 50),
        'reception': (220, 80), 'desk': (140, 70), 'bench': (180, 50), 'fridge': (80, 75), 'bloodcab': (110, 60), 'cabinet': (90, 50), 'lift': (180, 60),
        'iv': (30, 30), 'cylinder': (25, 25), 'washstand': (60, 45), 'dentist': (80, 120), 'anesth': (70, 60), 'beddev': (60, 50), 'scanmon': (70, 40),
        'angiomon': (100, 40), 'bloodtest': (80, 60), 'micro': (40, 40)}
def sheet(fl, d):
    z = fl['z']; lab = fl['label']
    xs = [-50, FL.EAST + 1150]; ys = [-FL.CORR - FL.DEPTH - 80, FL.CORR + FL.DEPTH + 80]
    W = int((xs[1] - xs[0]) * SC) + 2 * PAD; Hh = int((ys[1] - ys[0]) * SC) + 2 * PAD + 120
    im = Image.new('RGB', (W, Hh), BG); dr = ImageDraw.Draw(im)
    for gx in range(0, W, 25): dr.line([(gx, 0), (gx, Hh)], fill=GRID)
    for gy in range(0, Hh, 25): dr.line([(0, gy), (W, gy)], fill=GRID)
    P = lambda x, y: (PAD + (x - xs[0]) * SC, PAD + 60 + (y - ys[0]) * SC)
    rooms = fl['cores'] + fl['rooms']
    # zones
    corr = (FL.WEST - 350, -FL.CORR, FL.EAST + 350, FL.CORR)
    dr.rectangle([P(corr[0], corr[1]), P(corr[2], corr[3])], fill=(34, 64, 98))
    for r in rooms:
        dr.rectangle([P(r['x0'], r['y0']), P(r['x1'], r['y1'])], fill=ZC.get(r['zone'], ZC['core']))
    # furniture
    for it in d['furnish']:
        if it['z'] != z and not (it['kind'].startswith('sign') and abs(it['z'] - z) < 400): continue
        if it['kind'].startswith('sign') or it['kind'] in ('curtain', 'tray', 'monitor', 'chair', 'wastebin', 'bedside', 'barrier', 'cam', 'disinf', 'wheelchair'): continue
        sw, sh = SIZE.get(it['kind'], (50, 50))
        if int(it['yaw']) % 180 == 90: sw, sh = sh, sw
        a, b = P(it['x'] - sw / 2, it['y'] - sh / 2), P(it['x'] + sw / 2, it['y'] + sh / 2)
        dr.rectangle([a, b], outline=DIM, width=1)
        t = SYM.get(it['kind'], '')
        if t and b[0] - a[0] > 18: dr.text(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), t, font=F_X, fill=DIM, anchor='mm')
    # walls
    for bx in d['boxes']:
        if not bx['name'].startswith(lab + '_') or 'Wall' not in bx['name'] and 'Lintel' not in bx['name']: continue
        if 'Lintel' in bx['name']:
            dr.line([P(bx['x'], bx['y'] + bx['sy'] / 2), P(bx['x'] + bx['sx'], bx['y'] + bx['sy'] / 2)] if bx['sx'] > bx['sy'] else
                    [P(bx['x'] + bx['sx'] / 2, bx['y']), P(bx['x'] + bx['sx'] / 2, bx['y'] + bx['sy'])], fill=(240, 190, 90), width=1)
            continue
        dr.rectangle([P(bx['x'], bx['y']), P(bx['x'] + bx['sx'], bx['y'] + bx['sy'])], fill=LINE)
    # labels
    for r in rooms:
        name = {'core': 'LIFT LOBBY' if r['id'] == 'Lobby' else 'LIFT (DOWN)', 'stair': 'STAIRS', 'wc': 'W.C.'}.get(r['type']) or FL.ZONE[r['type']][2]
        cx, cy = P(r['x'], r['y'])
        dr.text((cx, cy - 8), name, font=F_R, fill=(255, 255, 255), anchor='mm')
        dr.text((cx, cy + 10), '%.1f x %.1f m' % ((r['x1'] - r['x0']) / 100, (r['y1'] - r['y0']) / 100), font=F_S, fill=DIM, anchor='mm')
    cx, cy = P((FL.WEST + FL.EAST) / 2, 0)
    dr.text((cx, cy), '4 M WIDE PASSAGE', font=F_R, fill=(200, 220, 240), anchor='mm')
    # stairs hatching
    for r in fl['cores']:
        if r['type'] == 'stair':
            for yy in range(int(r['y0']) + 20, int(r['y1']), 30):
                dr.line([P(r['x0'] + 15, yy), P(r['x1'] - 15, yy)], fill=DIM)
    # title block, legend, north arrow, scale bar
    dr.text((PAD, 30), 'HALVORSEN BIOLOGICS  //  %s  %s' % (lab, fl['name']), font=F_T, fill=(255, 255, 255))
    gate = {'keycard': 'EXIT LIFT: KEYCARD', 'switches': 'EXIT LIFT: 3 FLOOR SWITCHES (ORDER ON A NOTE)', 'power': 'EXIT LIFT: RESTART THE GENERATOR (PLANT ROOM)',
            'ending': 'ISOLATION CHAMBERS: EMILIA (L-03) + 5 CHILDREN'}[fl['gate']]
    dr.text((PAD, 66), gate, font=F_S, fill=(240, 190, 90))
    lx = PAD; ly = Hh - 50
    for zname in ('clinical', 'support', 'staff', 'service', 'core'):
        dr.rectangle([lx, ly, lx + 22, ly + 16], fill=ZC[zname], outline=LINE); dr.text((lx + 30, ly + 8), zname.upper(), font=F_S, fill=LINE, anchor='lm'); lx += 130
    sx = W - PAD - 250
    dr.rectangle([sx, ly + 4, sx + 500 * SC, ly + 12], outline=LINE); dr.rectangle([sx, ly + 4, sx + 250 * SC, ly + 12], fill=LINE)
    dr.text((sx, ly - 12), '0', font=F_S, fill=LINE); dr.text((sx + 500 * SC, ly - 12), '5 m', font=F_S, fill=LINE, anchor='ra')
    nx, ny = W - PAD - 30, 50
    dr.polygon([(nx, ny - 26), (nx - 10, ny + 8), (nx + 10, ny + 8)], fill=LINE); dr.text((nx, ny + 22), 'N', font=F_R, fill=LINE, anchor='mm')
    dr.text((W - PAD, Hh - 18), 'HOLLOW KIN  //  Terratales Media Entertainment  //  generated from tools/floors_layout.py', font=F_X, fill=DIM, anchor='rm')
    return im
sheets = []
for m in ('wards', 'deep'):
    d = FL.build(m)
    for fl in d['floors']:
        im = sheet(fl, d); im.save(os.path.join(OUT, fl['label'] + '.png')); sheets.append(im)
w = max(s.width for s in sheets); h = sum(s.height for s in sheets)
allim = Image.new('RGB', (w, h), BG); y = 0
for s in sheets: allim.paste(s, (0, y)); y += s.height
allim.thumbnail((w // 2, h // 2)); allim.save(os.path.join(OUT, 'ALL_FLOORS.png'))
print('plans:', len(sheets))
