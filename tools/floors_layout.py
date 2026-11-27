#!/usr/bin/env python3
"""HOLLOW KIN floor plans (docs/EXPANSION_PLAN.md, docs/floorplans/). Real-hospital style, after the reference
plans: a long 4 m double-loaded corridor ("passage"), a lift lobby + stair core at the west end, the exit lift and
a second stair at the east end, and rooms of different sizes on both sides grouped into ZONES:
  clinical (wards, ICU, OT, imaging, labs), support (nurse station, waiting, pharmacy), service (WC, store, sluice,
  plant), staff (doctors' rooms, offices, records, security), core (lifts, stairs).
Each room type furnishes itself from its rectangle (beds against the back wall, desks facing the door...).
Floors are stacked FLOOR_DZ apart in one map. JSON to stdout for build_floors.py and draw_floorplans.py:
  boxes, lights, furnish [{kind,x,y,z,yaw}], floors [{label,name,z,gate,arrival,lift,rooms:[{id,type,zone,x0,y0,x1,y1,x,y,side}]}]
usage: python3 tools/floors_layout.py wards|deep > floors.json"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import slice_layout as S

FLOOR_DZ = 1500
FLOOR_DZ_MAP = {'clinic': 470}   # the clinic is a real 2-storey building: G and F1 joined by stairs
H = 340                         # ceiling
CORR = 200                      # corridor half width (4 m passage)
DEPTH = 700                     # room depth from the corridor wall
WEST, EAST = 1200, 4400         # corridor run that rooms line
T = 25                          # wall thickness

ZONE = {  # type -> (zone, floor material, display name)
    'ward': ('clinical', 'tile', 'GENERAL WARD'), 'private': ('clinical', 'warm', 'PRIVATE ROOM'), 'icu': ('clinical', 'tile', 'I.C.U.'),
    'nicu': ('clinical', 'tile', 'N.I.C.U.'), 'ot': ('clinical', 'tile', 'OPERATING THEATRE'), 'scrub': ('service', 'tile', 'SCRUB'),
    'recovery': ('clinical', 'tile', 'RECOVERY'), 'xray': ('clinical', 'tile', 'X-RAY'), 'mri': ('clinical', 'tile', 'MRI / ANGIO'),
    'control': ('staff', 'warm', 'CONTROL'), 'lab': ('clinical', 'tile', 'LABORATORY'), 'blood': ('clinical', 'tile', 'BLOOD BANK'),
    'cold': ('service', 'concrete', 'COLD STORE'), 'morgue': ('clinical', 'concrete', 'MORGUE'), 'autopsy': ('clinical', 'tile', 'AUTOPSY'),
    'viewing': ('support', 'warm', 'VIEWING ROOM'), 'testing': ('clinical', 'tile', 'TEST ROOM'), 'observe': ('staff', 'warm', 'OBSERVATION'),
    'iso': ('clinical', 'tile', 'ISOLATION'), 'waiting': ('support', 'warm', 'WAITING AREA'), 'nurse': ('support', 'warm', 'NURSE STATION'),
    'reception': ('support', 'warm', 'RECEPTION'), 'pharmacy': ('support', 'warm', 'PHARMACY'), 'emergency': ('clinical', 'tile', 'EMERGENCY WARD'),
    'doctor': ('staff', 'warm', "DOCTOR'S ROOM"), 'office': ('staff', 'warm', 'OFFICE'), 'records': ('staff', 'warm', 'RECORDS'),
    'security': ('staff', 'warm', 'SECURITY'), 'wc': ('service', 'concrete', 'W.C.'), 'store': ('service', 'concrete', 'STORE'),
    'sluice': ('service', 'concrete', 'SLUICE'),
    'maternity': ('clinical', 'warm', 'MATERNITY WARD'), 'opd': ('support', 'warm', 'OPD CONSULT'), 'break': ('staff', 'warm', 'STAFF BREAK ROOM'),
    'recreation': ('support', 'warm', 'RECREATION ROOM'), 'lounge': ('support', 'warm', 'FAMILY LOUNGE'), 'suite': ('clinical', 'warm', 'PRIVATE SUITE'),
    'commonward': ('clinical', 'tile', 'COMMON WARD'), 'isoward': ('clinical', 'tile', 'ISOLATION WARD'), 'plant': ('service', 'concrete', 'PLANT ROOM'), 'cafeteria': ('support', 'warm', 'CAFETERIA'), 'stair_b': ('core', 'concrete', 'BASEMENT STAIRS'), 'storage': ('service', 'concrete', 'SPECIMEN STORE'),
}
# floor programs: north rooms west->east and south rooms west->east as (type, relative width)
MAPS = {
    'wards': [
        ('B2', 'COMMON WARDS', 'keycard', (1.0, 0.82, 0.6),
         [('commonward', 3), ('commonward', 3), ('store', 1)], [('nurse', 1.4), ('recreation', 2.4), ('wc', 1), ('break', 1.4)]),
        ('B3', 'PAEDIATRIC WARD', 'switches', (1.0, 0.75, 0.75),
         [('ward', 3), ('recreation', 2.2), ('private', 1.5)], [('nicu', 2.2), ('nurse', 1.4), ('wc', 1), ('store', 1), ('lounge', 1.5)]),
        ('B4', 'RADIOLOGY', 'keycard', (0.6, 0.85, 1.0),
         [('xray', 2), ('control', 1), ('xray', 2), ('mri', 2.6)], [('waiting', 2.2), ('nurse', 1.2), ('mri', 2.6), ('wc', 1), ('store', 1)]),
        ('B5', 'SURGERY', 'power', (0.75, 1.0, 0.85),
         [('ot', 3), ('scrub', 1), ('ot', 3)], [('recovery', 3), ('plant', 1.4), ('nurse', 1.2), ('sluice', 1), ('break', 1.2)]),
        ('B6', 'PHARMACY & BLOOD LAB', 'switches', (1.0, 0.55, 0.5),
         [('pharmacy', 3), ('blood', 2), ('lab', 2)], [('lab', 2), ('cold', 2), ('office', 1.2), ('wc', 1), ('store', 1)]),
        ('B7', 'MORGUE', 'keycard', (0.55, 0.75, 0.95),
         [('morgue', 3), ('autopsy', 2), ('cold', 2)], [('viewing', 2), ('office', 1.2), ('store', 1), ('sluice', 1), ('morgue', 2.4)]),
        ('B8', 'SECURITY & RECORDS', 'power', (0.9, 0.9, 1.0),
         [('security', 2), ('records', 3), ('office', 1.2)], [('records', 2), ('plant', 2), ('break', 1.4), ('wc', 1), ('store', 1)]),
    ],
    'clinic': [
        ('G', 'GROUND FLOOR  //  OPD & EMERGENCY', 'keycard', (1.0, 0.97, 0.92),
         [('reception', 2), ('waiting', 2.6), ('opd', 1.2), ('opd', 1.2)], [('emergency', 3), ('pharmacy', 1.6), ('wc', 1), ('break', 1.5)]),
        ('F1', 'FIRST FLOOR  //  MATERNITY & NICU', 'switches', (1.0, 0.97, 0.92),
         [('maternity', 3), ('suite', 1.6), ('suite', 1.6)], [('nicu', 2.4), ('nurse', 1.2), ('lounge', 1.8), ('wc', 1)]),
    ],
    'deep': [
        ('B10', 'SPECIMEN STORAGE', 'keycard', (0.6, 0.9, 0.85),
         [('storage', 2), ('cold', 2), ('lab', 2)], [('lab', 2), ('storage', 2), ('morgue', 2), ('wc', 1)]),
        ('B11', 'TESTING LAB A', 'switches', (0.85, 0.95, 1.0),
         [('testing', 2), ('observe', 1.2), ('testing', 2), ('testing', 2)], [('lab', 2), ('nurse', 1.2), ('store', 1), ('testing', 2), ('wc', 1)]),
        ('B12', 'TESTING LAB B', 'power', (1.0, 0.45, 0.4),
         [('ot', 2.4), ('testing', 2), ('morgue', 2)], [('testing', 2), ('lab', 2), ('plant', 1.6), ('sluice', 1)]),
        ('B13', 'OBSERVATION', 'keycard', (0.7, 0.8, 1.0),
         [('observe', 2), ('testing', 2), ('observe', 2)], [('security', 2), ('records', 2), ('office', 1.2), ('wc', 1)]),
        ('B14', 'SEDATION & ISOLATION', 'switches', (0.8, 0.7, 1.0),
         [('icu', 3), ('isoward', 3)], [('nurse', 1.2), ('suite', 1.5), ('suite', 1.5), ('store', 1), ('wc', 1)]),
        ('B15', 'ISOLATION CHAMBERS', 'ending', (0.75, 0.7, 1.0),
         [('iso', 1), ('iso', 1), ('iso', 1)], [('iso', 1), ('observe', 1.2), ('iso', 1), ('iso', 1)]),
    ],
}
BASE_Z = {'wards': 0, 'deep': -2000, 'clinic': 0}
DZ_SIGN = {'wards': -1, 'deep': -1, 'clinic': 1}       # clinic floors go UP (ground, first)
CLEAN = {'clinic'}                                     # bright modern interiors (above ground)
import random

def split(prog):
    """widths (cm, multiples of 25) for a side so rooms + walls exactly fill WEST..EAST."""
    span = EAST - WEST - T * (len(prog) - 1)
    tot = sum(w for _, w in prog)
    ws = [int(span * w / tot) // 25 * 25 for _, w in prog]
    ws[-1] += span - sum(ws)
    return ws

def furnish(t, x0, y0, x1, y1, side):
    """props for one room. side=-1 north (back wall at y0), +1 south (back wall at y1). Returns (kind, x, y, yaw)."""
    out = []; w = x1 - x0; d = y1 - y0
    back = y0 + 60 if side < 0 else y1 - 60          # just off the back wall
    front = y1 - 80 if side < 0 else y0 + 80          # near the corridor wall
    face = 0 if side < 0 else 180                     # yaw that faces the corridor (props' front)
    cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    inv = lambda yy: yy                               # readability
    def row(kind, n, y, yaw, margin=120):
        if n <= 0: return
        step = (w - 2 * margin) / max(1, n - 1) if n > 1 else 0
        kinds = kind if isinstance(kind, (list, tuple)) else [kind]
        for i in range(n): out.append((kinds[i % len(kinds)], x0 + margin + i * step if n > 1 else cx, y, yaw))
    nb = max(1, int((w - 100) // 230))
    by = back + (-side) * 60
    if t in ('ward', 'emergency', 'recovery', 'private'):
        n = 1 if t == 'private' else nb
        row('bed', n, by, face + 90 if False else (90 if side < 0 else 270), 140)
        row('iv', n, back + (-side) * -10 if False else back, 0, 230 if n > 1 else 0)
        if t != 'private': row('curtain', max(1, n - 1), cy, 0, 250)
        out.append(('bedside', x1 - 80, back, face)); out.append(('wastebin', x0 + 70, front, 0))
    elif t in ('icu', 'nicu', 'sedation'):
        row('bed', nb, by, 90 if side < 0 else 270, 140); row('beddev', nb, back, face, 230); row('iv', nb, by + (-side) * 120, 0, 200)
        out.append(('cabinet', x1 - 80, front, 90))
    elif t == 'ot' or t == 'autopsy':
        out += [('treat', cx, cy, 90), ('anesth', cx - 180, cy + side * 60, face), ('beddev', cx + 170, cy + side * 80, face), ('tray', cx + 110, cy - side * 60, 0),
                ('disinf', x0 + 80, back, face), ('wastebin', x1 - 70, back, 0)]
        if t == 'ot': out.append(('iv', cx - 100, cy - side * 120, 0))
    elif t == 'scrub' or t == 'wc' or t == 'sluice':
        row('washstand', max(1, int(w // 160)), back, face, 70); out.append(('wastebin', x1 - 60, front, 0))
    elif t == 'xray':
        out += [('xray', cx, cy + side * 60, face), ('barrier', x0 + 90, cy, 90), ('scanmon', x1 - 90, back, face)]
    elif t == 'mri':
        out += [('angio', cx, cy, 0), ('angiomon', x1 - 110, back, face), ('cylinder', x0 + 70, back, 0), ('cylinder', x0 + 130, back, 0), ('stretcher', x0 + 140, front, 0)]
    elif t in ('control', 'security', 'observe'):
        row('desk', max(1, int(w // 260)), back, face, 140); row('monitor', max(1, int(w // 260)), back, face, 140)
        row('chair', max(1, int(w // 260)), back + (-side) * 90, face + 180, 140)
        if t == 'security': out.append(('cam', x1 - 40, back, face + 45))
    elif t in ('lab', 'testing'):
        if t == 'lab':
            row(('fume', 'bloodtest', 'micro2'), max(1, int(w // 220)), back, face, 110); out += [('micro', cx, front, face + 180), ('bloodtest', x1 - 90, cy, 270)]
        else:
            out += [('dentist', cx, cy, face), ('scanmon', x0 + 90, back, face), ('beddev', x1 - 100, back, face), ('iv', cx + 120, cy, 0), ('tray', cx - 110, cy, 0)]
    elif t == 'blood':
        row(('bloodcab', 'fridge', 'bloodcab'), max(1, int(w // 170)), back, face, 90); out += [('treat', cx, cy, 90), ('iv', cx + 110, cy, 0), ('fridge', x1 - 60, front, 270)]
    elif t == 'cold' or t == 'morgue':
        row(('fridge', 'fridge', 'cabinet'), max(1, int(w // 120)), back, face, 60)
        if t == 'morgue': row('stretcher', max(1, int(w // 280)), cy, 90, 150)
    elif t == 'storage' or t == 'store' or t == 'records' or t == 'plant':
        if t == 'plant': out += [('cylinder', x0 + 80, back, 0), ('cylinder', x0 + 140, back, 0), ('cabinet', x1 - 80, back, face)]
        else: row(('rack', 'cabinet', 'rack', 'box3'), max(1, int(w // 190)), back, face, 100)
        if t == 'records': row(('cabinet', 'rack'), max(1, int(w // 220)), cy, face, 120)
    elif t == 'waiting' or t == 'viewing':
        row('bench', max(1, int(w // 260)), cy - side * 60, face, 150); row('bench', max(1, int(w // 260)), cy + side * 120, face, 150)
        out.append(('wastebin', x1 - 60, front, 0))
    elif t in ('nurse', 'reception'):
        out += [('reception', cx, cy - side * 20, face + 180), ('chair', cx, back, face), ('cabinet', x0 + 80, back, face), ('monitor', cx + 60, cy - side * 20, face)]
    elif t == 'pharmacy':
        row(('rack', 'cabinet'), max(1, int(w // 190)), back, face, 100); out.append(('reception', cx, front - side * -10, face + 180))
    elif t in ('doctor', 'office'):
        out += [('desk', cx, back + (-side) * 40, face), ('chair', cx, back + (-side) * 110, face + 180), ('monitor', cx, back + (-side) * 30, face),
                ('cabinet', x1 - 70, back, face), ('treat' if t == 'doctor' else 'rack', x0 + 110, cy, 90 if t == 'doctor' else face)]
    elif t in ('commonward', 'isoward'):
        n = max(2, int((w - 100) // 230))
        row('bed', n, by, 90 if side < 0 else 270, 140); row('iv', n, back, 0, 230)
        row('bed', max(1, n - 1), y0 + 160 if side > 0 else y1 - 160, 270 if side < 0 else 90, 230)     # second row facing
        if t == 'isoward': row('barrier', n - 1, cy, 0, 250)
        else: row('curtain', n - 1, by + (-side) * 30, 0, 250)
        out.append(('cabinet', x1 - 70, front, 90))
    elif t == 'maternity':
        n = max(1, int((w - 100) // 280))
        row('bed', n, by, 90 if side < 0 else 270, 160); row('beddev', n, by + (-side) * 150, face, 250)   # bassinet/monitor beside each bed
        row('chair', n, by + (-side) * 220, face + 180, 200); row('curtain', max(1, n - 1), cy, 0, 300)
        out.append(('bedside', x1 - 80, back, face))
    elif t == 'suite':
        out += [('bed', cx + 40, by, 90 if side < 0 else 270), ('bedside', cx + 170, back, face), ('booth', x0 + 90, cy + side * 40, 90),
                ('rtable', x0 + 120, front - side * -40, 0), ('cabinet', x1 - 70, front, 90), ('pot', x1 - 70, back, 0), ('monitor', x0 + 90, back, face)]
    elif t == 'opd':
        out += [('desk', cx + 40, back + (-side) * 40, face), ('chair', cx + 40, back + (-side) * 110, face + 180), ('rchair', cx + 40, back + (-side) * 220, face),
                ('treat', x0 + 100, cy, 90), ('curtain', x0 + 200, cy, 90), ('washstand', x1 - 60, front, 270), ('monitor', cx + 40, back + (-side) * 30, face)]
    elif t == 'break':
        out += [('rtable', cx, cy, 0), ('rchair', cx - 70, cy, 90), ('rchair', cx + 70, cy, 270), ('rchair', cx, cy - 70, 0), ('fridge', x1 - 60, back, face),
                ('washstand', x0 + 70, back, face), ('shelves', cx, back, face), ('mug', cx + 20, cy + 10, 0), ('rack', x1 - 60, front, 270)]
    elif t == 'recreation':
        for i in range(max(1, int(w // 300))):
            tx = x0 + 150 + i * 280
            out += [('rtable', tx, cy, 0), ('rchair', tx - 70, cy, 90), ('rchair', tx + 70, cy, 270)]
        out += [('shelves', x0 + 120, back, face), ('booth', x1 - 110, back + (-side) * 60, face), ('pot', x1 - 60, front, 0), ('monitor', cx, back, face)]
    elif t == 'lounge':
        out += [('booth', x0 + 110, back + (-side) * 60, face), ('booth', x1 - 110, back + (-side) * 60, face), ('rtable', cx, cy, 0),
                ('pot', x0 + 60, front, 0), ('pot', x1 - 60, front, 0), ('shelves', cx, back, face), ('mug', cx, cy, 0)]
    elif t == 'cafeteria':
        out += [('reception', x0 + 130, cy, 90), ('fridge', x0 + 60, back, face), ('shelves', x0 + 160, back, face), ('cart', x0 + 120, front, 0)]
        nt = max(1, int((w - 360) // 260)); nr = max(1, int((d - 200) // 230))
        for i in range(nt):
            for j in range(nr):
                tx = x0 + 330 + i * 260; ty = y0 + 140 + j * 230 + (0 if side < 0 else 0)
                if tx > x1 - 120: continue
                out += [('rtable', tx, ty, 0), ('rchair', tx - 70, ty, 90), ('rchair', tx + 70, ty, 270)]
        out += [('booth', x1 - 90, back + (-side) * 70, 270), ('pot', x1 - 60, front, 0), ('wastebin', x0 + 260, front, 0)]
    elif t == 'iso':
        out += [('bed', cx, back + (-side) * 50, 90 if side < 0 else 270), ('iv', cx + 110, back, 0)]
    return out

SIGN = {'maternity': 'sign_nursery', 'opd': 'sign_reception', 'emergency': 'sign_reception', 'xray': 'sign_xray', 'mri': 'sign_xray', 'ot': 'sign_surgery', 'scrub': 'sign_surgery', 'nicu': 'sign_nursery', 'lab': 'sign_lab',
        'blood': 'sign_lab', 'testing': 'sign_lab', 'reception': 'sign_reception', 'waiting': 'sign_reception'}

LED_CENTERS = {}   # label -> [(x, y, ceiling z)] of lit panels; every light is moved under one
def dressing(label, z, rooms, doors, clean, rnd, cor):
    """flat LED ceiling panels everywhere; clean floors also get floor inlay strips, accent door frames, handrails and
    frosted daylight windows on the outer walls."""
    bx = []
    def B(name, mat, x, y, zz, sx, sy, sz): bx.append(dict(name='%s_%s' % (label, name), mat=mat, x=x, y=y, z=z + zz, sx=sx, sy=sy, sz=sz))
    led = 'led' if clean else 'led_dim'
    n = 0
    for rid, (x0, y0, x1, y1, h, m) in rooms.items():
        w, d = x1 - x0, y1 - y0
        nx = max(1, int(w // 300)); ny = max(1, int(d // 300))
        if rid in ('StairW', 'StairE', 'WC1', 'WC2', 'CabE', 'CabW'): nx = ny = 1
        for i in range(nx):
            for j in range(ny):
                cx = x0 + (i + 0.5) * w / nx; cy = y0 + (j + 0.5) * d / ny
                if not clean and rid not in ('StairW', 'StairE', 'WC1', 'WC2', 'CabE', 'CabW') and rnd.random() < 0.18:
                    B('LEDDead%d' % n, 'metal', cx - 60, cy - 30, h - 3, 120, 60, 3); n += 1   # dead panel: dark, no light
                    continue
                B('LED%d' % n, led, cx - 60, cy - 30, h - 3, 120, 60, 3); n += 1
                LED_CENTERS.setdefault(label, []).append((cx, cy, z + h))
    if not clean: return bx
    corr = cor[0]
    if corr[2] - corr[0] > corr[3] - corr[1]:
        cy = (corr[1] + corr[3]) / 2
        for k, yy in enumerate((cy - 90, cy + 90)):                        # grey inlay strips along the main passage
            B('Inlay%d' % k, 'clean_inlay', corr[0] + 50, yy - 6, 0.0, corr[2] - corr[0] - 100, 12, 1.5)
        for xx in range(int(corr[0]) + 300, int(corr[2]) - 100, 400):
            B('Band%d' % xx, 'clean_inlay', xx, cy - 60, 0.0, 40, 120, 1.5)
    acc = 'clean_yellow' if label == 'G' else 'clean_teal'
    def in_cor(x, y): return any(c[0] <= x <= c[2] and c[1] <= y <= c[3] for c in cor)
    for rid, (dx0, dy0, dx1, dy1) in doors.items():
        if dy1 - dy0 != 25 or rid in ('Lobby', 'Lift', 'CabE', 'CabW'): continue
        dc = (dx0 + dx1) / 2
        if in_cor(dc, dy1 + 10): fy = dy1                                 # corridor below the door
        elif in_cor(dc, dy0 - 10): fy = dy0 - 4
        else: continue
        B('Frame%sL' % rid, acc, dx0 - 12, fy, 0, 12, 4, 245); B('Frame%sR' % rid, acc, dx1, fy, 0, 12, 4, 245)
        B('Frame%sT' % rid, acc, dx0 - 12, fy, 240, dx1 - dx0 + 24, 4, 12)
    for rid, (x0, y0, x1, y1, h, m) in rooms.items():                      # frosted daylight windows on outer walls
        if rid[0] in 'NS' and rid[1:].isdigit() and (y0 <= -925 or y1 >= 925):    # outer walls only
            wy = y0 - 1 if y0 <= -925 else y1 - 3     # window panes 3 cm proud of the wall face
            for i in range(max(1, int((x1 - x0) // 350))):
                cx = x0 + (i + 0.5) * (x1 - x0) / max(1, int((x1 - x0) // 350))
                B('Win%s%d' % (rid, i), 'window', cx - 90, wy, 110, 180, 4, 120)
    return bx

def clinic_stairs(label, k, z, rooms):
    """G (k=0): a straight flight of box steps in StairW rising one storey along -y, ceiling removed above it.
    F1 (k=1): no floor over the flight; a landing at the top, a walkway along the east side back to the door, a railing."""
    out = []
    dz = FLOOR_DZ_MAP['clinic']
    sx0, sy0, sx1, sy1 = rooms['StairW'][:4]           # x WEST-350..WEST-25, y -925..-225
    fx1 = sx0 + 200                                     # flight is 2 m wide on the west side
    n = 19; run = 32; ybot = sy1 - 35                   # first step just inside the door
    if k == 0:
        for i in range(n):
            out.append(dict(name='%s_Step%d' % (label, i), mat='concrete_floor', x=sx0, y=ybot - (i + 1) * run, z=z,
                            sx=fx1 - sx0, sy=run, sz=round(dz * (i + 1) / n)))
        top = ybot - n * run
        out.append(dict(name='%s_StairTop' % label, mat='concrete_floor', x=sx0, y=sy0, z=z, sx=sx1 - sx0, sy=top - sy0, sz=dz))  # solid block under the landing
        for (bx, by, bsx, bsy) in ((sx0 - 25, sy0 - 25, sx1 - sx0 + 50, 25), (sx0 - 25, sy1, sx1 - sx0 + 50, 25),
                                   (sx0 - 25, sy0, 25, sy1 - sy0), (sx1, sy0, 25, sy1 - sy0)):   # close the gap between the storeys
            out.append(dict(name='%s_StairFill' % label, mat='wall', x=bx, y=by, z=z + 450, sx=bsx, sy=bsy, sz=40))
    else:
        top = sy1 - 35 - n * run
        out.append(dict(name='%s_Walkway' % label, mat='concrete_floor', x=fx1, y=top, z=z - 20, sx=sx1 - fx1, sy=sy1 - top, sz=20))
        out.append(dict(name='%s_Rail' % label, mat='clean_rail', x=fx1 - 5, y=top + 60, z=z, sx=5, sy=sy1 - top - 60, sz=100))
        out.append(dict(name='%s_RailDoor' % label, mat='clean_rail', x=sx0, y=sy1 - 40, z=z, sx=fx1 - sx0, sy=5, sz=100))
    return out

# ---------------------------------------------------------------------------------------------------------------
# Layout v2 (2026-11-27): every floor has its own plan. Fixed on every floor: west lift lobby + west stair core +
# washroom 1, east lift room + east stair core + washroom 2. The middle (x 1200..4400) uses one of four shapes:
#   spine     one straight 4 m corridor, rooms both sides
#   ring      two 2.5 m corridors around a block of central rooms (racetrack), cross halls at both ends
#   jog       west corridor north, east corridor south, joined by an open hub; deep rooms on the far sides
#   hall      straight corridor broken by a big open hall in the middle (waiting / nurse hub / atrium)
# Rooms are cut from "strips" (x0, x1, y0, y1, side): side -1 = door on the y1 wall, +1 = door on the y0 wall.
VARIANT = {'G': 'hall', 'F1': 'spine', 'B2': 'ring', 'B3': 'jog', 'B4': 'spine', 'B5': 'hall', 'B6': 'ring', 'B7': 'jog',
           'B8': 'hall', 'B10': 'jog', 'B11': 'ring', 'B12': 'hall', 'B13': 'spine', 'B14': 'ring', 'B15': 'spine'}
OPEN_STAIR = {'B3', 'B6', 'B11'}          # basement stairwell open to a landing (others blocked by rubble)
PROGRAM = {   # per floor: the rooms that fill the strips (break room is added automatically; washrooms are fixed)
    'G': [('reception', 2), ('emergency', 3), ('opd', 1.3), ('pharmacy', 1.6), ('cafeteria', 3.2), ('opd', 1.3), ('doctor', 1.3), ('store', 1)],
    'F1': [('maternity', 3), ('nurse', 1.3), ('suite', 1.6), ('nicu', 2.4), ('lounge', 1.8), ('suite', 1.6), ('office', 1.2)],
    'B2': [('commonward', 3), ('nurse', 1.4), ('recreation', 2.4), ('store', 1), ('commonward', 3), ('office', 1.2), ('private', 1.4), ('sluice', 1)],
    'B3': [('ward', 3), ('recreation', 2.2), ('nicu', 2.2), ('nurse', 1.3), ('private', 1.5), ('lounge', 1.5), ('store', 1)],
    'B4': [('xray', 2), ('control', 1), ('mri', 2.6), ('waiting', 2.2), ('xray', 2), ('nurse', 1.2), ('records', 1.4), ('store', 1)],
    'B5': [('ot', 3), ('scrub', 1), ('recovery', 3), ('plant', 1.4), ('ot', 3), ('sluice', 1), ('store', 1.2)],
    'B6': [('pharmacy', 2.6), ('blood', 2), ('lab', 2), ('cold', 2), ('office', 1.2), ('lab', 2), ('store', 1)],
    'B7': [('morgue', 3), ('autopsy', 2), ('cold', 2), ('viewing', 2), ('office', 1.2), ('sluice', 1), ('morgue', 2.4)],
    'B8': [('security', 2), ('records', 3), ('office', 1.2), ('plant', 2), ('records', 2), ('control', 1.4), ('store', 1)],
    'B10': [('storage', 2.2), ('cold', 2), ('lab', 2), ('morgue', 2), ('storage', 2), ('plant', 1.4), ('lab', 2)],
    'B11': [('testing', 2.2), ('observe', 1.2), ('lab', 2), ('testing', 2.2), ('control', 1.2), ('store', 1), ('testing', 2)],
    'B12': [('ot', 2.6), ('testing', 2), ('morgue', 2), ('plant', 1.6), ('testing', 2), ('lab', 2), ('sluice', 1)],
    'B13': [('observe', 2), ('testing', 2), ('security', 2), ('records', 2), ('observe', 2), ('office', 1.2)],
    'B14': [('icu', 3), ('isoward', 3), ('nurse', 1.2), ('suite', 1.5), ('control', 1.2), ('store', 1), ('icu', 2.4)],
    'B15': [('iso', 1), ('iso', 1), ('iso', 1), ('observe', 1.2), ('iso', 1), ('iso', 1), ('iso', 1)],
}
CURATED = {   # strip-by-strip room lists (same strip order as shape())
    'G': [[('opd', 1.3), ('doctor', 1.2), ('store', 1)], [('cafeteria', 1)], [('pharmacy', 1)],
          [('emergency', 1)], [('reception', 1.3), ('break', 1)], [('waiting', 1)]],
    'F1': [[('maternity', 3), ('nurse', 1.2), ('suite', 1.6), ('office', 1.1)], [('nicu', 2.4), ('suite', 1.6), ('lounge', 1.8), ('break', 1.3)]],
}
FILL = {'clinical': ['cabinet', 'iv', 'beddev', 'bedside', 'scanmon', 'wastebin'], 'support': ['pot', 'cabinet', 'shelves', 'rchair', 'booth', 'bench'],
        'staff': ['cabinet', 'rack', 'pot', 'chair', 'shelves'], 'service': ['rack', 'box3', 'cabinet', 'cylinder']}
MACHINES = ['beddev', 'scanmon', 'anesth', 'bloodtest', 'fume', 'cylinder', 'fridge', 'cabinet', 'bloodcab', 'angiomon']

def shape(variant):
    """corridors (rects) and strips for the middle of the floor"""
    if variant == 'ring':
        cor = [(1200, -550, 4400, -300), (1200, 300, 4400, 550), (1200, -550, 1500, 550), (4100, -550, 4400, 550)]
        strips = [(1200, 4400, -925, -575, -1), (1525, 4075, -275, -25, 1), (1525, 4075, 0, 275, -1), (1200, 4400, 575, 925, 1)]
    elif variant == 'jog':
        cor = [(1200, -350, 2650, 0), (2650, -550, 3150, 550), (3150, 0, 4400, 350)]
        strips = [(1200, 2625, -925, -375, -1), (1225, 2625, 25, 925, 1), (2650, 3150, -925, -575, -1), (2650, 3150, 575, 925, 1),
                  (3175, 4375, -925, -25, -1), (3175, 4400, 375, 925, 1)]
    elif variant == 'hall':
        cor = [(1200, -200, 4400, 200), (2400, -575, 3200, 575)]
        strips = [(1200, 2375, -925, -225, -1), (3225, 4400, -925, -225, -1), (2400, 3200, -925, -600, -1),
                  (1200, 2375, 225, 925, 1), (3225, 4400, 225, 925, 1), (2400, 3200, 600, 925, 1)]
    else:
        cor = [(1200, -200, 4400, 200)]
        strips = [(1200, 4400, -925, -225, -1), (1200, 4400, 225, 925, 1)]
    return cor, strips

def order_program(prog, rnd):
    """shuffle so the same room type never sits next to itself"""
    for _ in range(200):
        p = prog[:]; rnd.shuffle(p)
        if all(p[i][0] != p[i + 1][0] for i in range(len(p) - 1)): return p
    return prog

def assign(strips, prog):
    """hand consecutive program rooms to strips in proportion to strip length; each strip gets >= 1 room"""
    total_len = sum(s[1] - s[0] for s in strips); total_w = sum(w for _, w in prog)
    out = []; i = 0
    for si, s in enumerate(strips):
        share = (s[1] - s[0]) / total_len * total_w
        got = []; acc = 0
        while i < len(prog) and (not got or acc + prog[i][1] / 2 <= share or si == len(strips) - 1):
            got.append(prog[i]); acc += prog[i][1]; i += 1
            if si == len(strips) - 1: continue
            if len(prog) - i <= len(strips) - si - 1: break
        if not got: got = [('store', 1)]
        out.append((s, got))
    return out

def cut(s, items):
    x0, x1 = s[0], s[1]
    span = x1 - x0 - T * (len(items) - 1)
    tot = sum(w for _, w in items)
    ws = [max(250, int(span * w / tot) // 25 * 25) for _, w in items]
    ws[-1] = span - sum(ws[:-1])
    x = x0; res = []
    for (t, _), w in zip(items, ws):
        res.append((t, x, x + w)); x += w + T
    return res

def wc_boxes(label, z, r, side):
    """washroom: two toilet stalls at the back, a shower cabin, partitions (boxes); toilets/sinks are furnish"""
    x0, y0, x1, y1 = r
    back = y1 if side > 0 else y0; inward = -side
    b = []
    stall_d = 150
    ys = back + inward * stall_d
    lo, hi = min(back, ys), max(back, ys)
    for px in (x0 + 105, x0 + 210):       # stall partitions
        b.append(dict(name='%s_WCPart' % label, mat='metal', x=px, y=lo, z=z, sx=4, sy=hi - lo, sz=190))
    sy0 = y0 + 230 if side > 0 else y1 - 230 - 120          # shower cabin by the side wall, mid-room
    b.append(dict(name='%s_ShowerA' % label, mat='glass', x=x1 - 115, y=sy0, z=z, sx=4, sy=120, sz=200))
    b.append(dict(name='%s_ShowerB' % label, mat='glass', x=x1 - 115, y=sy0, z=z, sx=115, sy=4, sz=200))
    b.append(dict(name='%s_ShowerTray' % label, mat='metal', x=x1 - 111, y=sy0 + 4, z=z, sx=111, sy=116, sz=2))
    return b

def wc_furnish(x0, y0, x1, y1, side):
    back = y1 - 45 if side > 0 else y0 + 45; face = 180 if side > 0 else 0
    f = [('toilet', x0 + 55, back, face), ('toilet', x0 + 160, back, face), ('toilet', x0 + 265, back, face)]
    sinky = (y0 + y1) / 2 + side * 120
    f += [('sink', x0 + 30, sinky, 90), ('sink', x0 + 30, sinky + 90, 90), ('mirror', x0 + 2, sinky + 45, 90), ('wastebin', x1 - 40, (y0 + y1) / 2 - side * 200, 0)]
    return f

def stair_down(label, z, r, open_):
    """basement stairwell: a flight going down to a landing 2.4 m below; blocked by rubble unless open_"""
    x0, y0, x1, y1 = r
    b = []; n = 10; run = 34; fx1 = x0 + 190
    ytop = y1 - 40
    for i in range(n):                     # step i: top surface at -24*(i+1)
        b.append(dict(name='%s_DStep%d' % (label, i), mat='concrete_floor', x=x0, y=ytop - (i + 1) * run, z=z - 24 * (i + 1) - 20, sx=fx1 - x0, sy=run, sz=20))
    land_y = ytop - n * run
    b.append(dict(name='%s_DLanding' % label, mat='concrete_floor', x=x0, y=y0, z=z - 260, sx=x1 - x0, sy=land_y - y0, sz=20))
    b.append(dict(name='%s_DWalk' % label, mat='concrete_floor', x=fx1, y=land_y, z=z - 20, sx=x1 - fx1, sy=ytop - land_y, sz=20))   # side walkway at floor level
    b.append(dict(name='%s_DTop' % label, mat='concrete_floor', x=x0, y=ytop, z=z - 20, sx=x1 - x0, sy=y1 - ytop, sz=20))
    b.append(dict(name='%s_DRail' % label, mat='metal', x=fx1, y=land_y + 40, z=z, sx=5, sy=ytop - land_y - 40, sz=100))
    for (bx, by, bsx, bsy) in ((x0 - 25, y0 - 25, x1 - x0 + 50, 25), (x0 - 25, y1, fx1 - x0 + 25, 25), (x0 - 25, y0, 25, y1 - y0), (x1, y0, 25, y1 - y0)):
        b.append(dict(name='%s_DPit' % label, mat='wall', x=bx, y=by, z=z - 300, sx=bsx, sy=bsy, sz=300))
    if not open_:                         # collapsed: rubble heaped on the upper steps
        for i, (dx, dy, h) in enumerate(((10, 60, 120), (70, 20, 160), (120, 80, 100), (40, 130, 70), (150, 140, 90))):
            b.append(dict(name='%s_Rubble%d' % (label, i), mat='concrete_floor', x=x0 + dx, y=ytop - 200 + dy, z=z - 120, sx=70, sy=70, sz=h))
    return b

def build(mapname):
    out = dict(boxes=[], lights=[], furnish=[], floors=[])
    for k, (label, name, gate, col, _n, _s) in enumerate(MAPS[mapname]):
        z = BASE_Z[mapname] + DZ_SIGN.get(mapname, -1) * k * FLOOR_DZ_MAP.get(mapname, FLOOR_DZ)
        clean = mapname in CLEAN
        if not clean:                                     # basements: cold, desaturated clinical light
            col = (0.78 + 0.04 * (k % 3), 0.86 + 0.02 * (k % 2), 1.0)
        rnd = random.Random(sum(map(ord, label)) * 7 + 3)
        rooms, doors, info_rooms = {}, {}, []
        variant = VARIANT.get(label, 'spine')
        cor, strips = shape(variant)
        # fixed blocks
        rooms['CorW'] = (WEST - 350, -CORR, WEST, CORR, H, 'tile')
        rooms['CorE'] = (EAST, -CORR, EAST + 350, CORR, H, 'tile')
        for i, c in enumerate(cor): rooms['Corr%d' % i] = (c[0], c[1], c[2], c[3], H, 'tile')
        rooms['Lobby'] = (0, -400, WEST - 375, 400, H, 'concrete')
        doors['Lobby'] = (WEST - 375, -CORR + 25, WEST - 350, CORR - 25)
        rooms['StairW'] = (WEST - 350, -CORR - 25 - DEPTH, WEST - 25, -CORR - 25, H, 'concrete')
        doors['StairW'] = (WEST - 300, -CORR - 25, WEST - 75, -CORR)
        rooms['WC1'] = (WEST - 350, CORR + 25, WEST - 25, CORR + 25 + DEPTH, H, 'concrete')
        doors['WC1'] = (WEST - 300, CORR, WEST - 175, CORR + 25)
        ex = EAST + 375
        rooms['Lift'] = (ex, -400, ex + 700, 400, H, 'concrete')
        doors['Lift'] = (EAST + 350, -150, ex, 150)
        rooms['StairE'] = (EAST + 25, -CORR - 25 - DEPTH, EAST + 350, -CORR - 25, H, 'concrete')
        doors['StairE'] = (EAST + 75, -CORR - 25, EAST + 300, -CORR)
        rooms['WC2'] = (EAST + 25, CORR + 25, EAST + 350, CORR + 25 + DEPTH, H, 'concrete')
        doors['WC2'] = (EAST + 200, CORR, EAST + 325, CORR + 25)
        LY = {'G': -130, 'F1': 130}.get(label, 0) if mapname == 'clinic' else 0
        if mapname == 'clinic':
            rooms['CabE'] = (ex + 725, 5, ex + 950, 255, H, 'concrete')
            doors['CabE'] = (ex + 700, 30, ex + 725, 230)
            stat = [(ex + 678, -130, 0)] + ([(ex + 678, 130, 50)] if label == 'G' else [])
            for (fx, fy, gap) in stat:
                out['furnish'] += [dict(kind='liftframe', x=fx, y=fy, z=z, yaw=0), dict(kind='liftdoorL', x=fx, y=fy + gap, z=z, yaw=0),
                                   dict(kind='liftdoorR', x=fx, y=fy - gap, z=z, yaw=0)]
            for part in ('liftframe', 'liftdoorL', 'liftdoorR'):
                out['furnish'].append(dict(kind=part, x=22, y=0, z=z, yaw=180))
        else:
            rooms['CabE'] = (ex + 725, -125, ex + 950, 125, H, 'concrete')
            doors['CabE'] = (ex + 700, -100, ex + 725, 100)
            rooms['CabW'] = (-250, -125, -25, 125, H, 'concrete')
            doors['CabW'] = (-25, -100, 0, 100)
        cores = [('Lobby', 'core'), ('StairW', 'stair'), ('Lift', 'core'), ('StairE', 'stair_b' if not clean else 'store')]
        for rid, t in cores:
            x0, y0, x1, y1 = rooms[rid][:4]
            info_rooms.append(dict(id=rid, type=t, zone='core', x0=x0, y0=y0, x1=x1, y1=y1, x=(x0 + x1) / 2, y=(y0 + y1) / 2, side=0))
        # washrooms (fixed, both sides of the floor)
        for rid, side in (('WC1', 1), ('WC2', 1)):
            x0, y0, x1, y1 = rooms[rid][:4]
            info_rooms.append(dict(id=rid, type='wc', zone='service', x0=x0, y0=y0, x1=x1, y1=y1, x=(x0 + x1) / 2, y=(y0 + y1) / 2, side=side,
                                   door=((doors[rid][0] + doors[rid][2]) / 2, (doors[rid][1] + doors[rid][3]) / 2)))
            out['boxes'] += wc_boxes(label, z, (x0, y0, x1, y1), side)
            for (kind, fx, fy, yaw) in wc_furnish(x0, y0, x1, y1, side):
                out['furnish'].append(dict(kind=kind, x=round(fx), y=round(fy), z=z, yaw=yaw % 360))
        # program rooms
        prog = PROGRAM[label][:]
        if label != 'B15': prog.append(('break', 1.4))
        prog = order_program(prog, rnd) if label != 'B15' else prog
        n_room = 0
        plan = list(zip(strips, CURATED[label])) if label in CURATED else assign(strips, prog)
        for s, items in plan:
            sx0, sx1, sy0, sy1, side = s
            for (t, x0, x1) in cut(s, items):
                y0, y1 = sy0, sy1
                rid = ('N' if side < 0 else 'S') + str(n_room); n_room += 1
                zone, mat, _ = ZONE.get(t, ('support', 'warm', t.upper()))
                rooms[rid] = (x0, y0, x1, y1, H, mat)
                wd = x1 - x0
                dw = 300 if t in ('nurse', 'reception', 'waiting', 'cafeteria') else 150 if wd < 400 else 175
                dw = min(dw, wd - 75) // 25 * 25
                dc = (x0 + x1) // 2 // 25 * 25
                if side < 0: doors[rid] = (dc - dw // 2, y1, dc + dw // 2, y1 + 25)
                else: doors[rid] = (dc - dw // 2, y0 - 25, dc + dw // 2, y0)
                dr = doors[rid]
                info_rooms.append(dict(id=rid, type=t, zone=zone, x0=x0, y0=y0, x1=x1, y1=y1, x=(x0 + x1) / 2, y=(y0 + y1) / 2, side=side,
                                       door=((dr[0] + dr[2]) / 2, (dr[1] + dr[3]) / 2), dw=dw))
                for (kind, fx, fy, yaw) in furnish(t, x0, y0, x1, y1, side):
                    out['furnish'].append(dict(kind=kind, x=round(fx), y=round(fy), z=z, yaw=yaw % 360))
                if not clean and t not in ('wc', 'store', 'iso', 'break', 'lounge', 'recreation', 'cafeteria', 'waiting'):
                    for j in range(1 + (wd > 450) + (t in ('testing', 'lab', 'ot', 'morgue', 'observe', 'control', 'plant', 'storage'))):
                        mk = rnd.choice(MACHINES)                     # machinery / test equipment along the side walls
                        mx = x0 + 60 if j % 2 == 0 else x1 - 60
                        my = (y0 + y1) / 2 + rnd.uniform(-120, 120)
                        out['furnish'].append(dict(kind=mk, x=round(mx), y=round(my), z=z, yaw=(90 if j % 2 == 0 else 270)))
                mine = [f for f in out['furnish'] if f['z'] == z and x0 <= f['x'] <= x1 and y0 <= f['y'] <= y1]
                want = int(wd * (y1 - y0) / 60000) - len(mine)
                pool = FILL.get(zone, FILL['support']) + ([] if clean else MACHINES[:4])
                if t not in ('iso', 'wc', 'scrub') and want > 0:
                    back = y0 if side < 0 else y1
                    spots = [(xx, back - side * 55, 0 if side < 0 else 180) for xx in range(int(x0) + 90, int(x1) - 60, 130)]
                    spots += [(x0 + 50, yy, 90) for yy in range(int(y0) + 110, int(y1) - 110, 140)] + [(x1 - 50, yy, 270) for yy in range(int(y0) + 110, int(y1) - 110, 140)]
                    rnd.shuffle(spots)
                    for (fx, fy, fyaw) in spots:
                        if want <= 0: break
                        if any((f['x'] - fx) ** 2 + (f['y'] - fy) ** 2 < 120 ** 2 for f in mine): continue
                        if side < 0 and fy > y1 - 160 and abs(fx - dc) < dw: continue      # keep the doorway clear
                        if side > 0 and fy < y0 + 160 and abs(fx - dc) < dw: continue
                        it = dict(kind=rnd.choice(pool), x=round(fx), y=round(fy), z=z, yaw=fyaw)
                        out['furnish'].append(it); mine.append(it); want -= 1
                if t in SIGN:
                    out['furnish'].append(dict(kind=SIGN[t], x=dc, y=(y1 + 2 if side < 0 else y0 - 2), z=z + 255, yaw=(270 if side < 0 else 90)))
                nl = max(1, int(wd // 450)) * max(1, int((y1 - y0) // 500))
                for j in range(nl):
                    out['lights'].append(dict(name='%s_L%s%d' % (label, rid, j), x=round(x0 + (j + 0.5) * wd / nl), y=round((y0 + y1) / 2), z=z + 300,
                                              i=int(130 * (3.0 if clean else 0.85)), r=col[0], g=col[1], b=col[2], rad=650))
        S.ROOMS = {label + '_' + n: r for n, r in rooms.items()}
        S.DOORS = {label + '_' + n: d for n, d in doors.items()}
        S.PROPS = []
        skip = set()
        if mapname == 'clinic': skip = {'G_StairW_Ceiling', 'F1_StairW_Floor', 'G_CabE_Floor', 'G_CabE_Ceiling'}
        elif label != 'B15': skip = {label + '_StairE_Floor'}
        for b in S.build():
            b = dict(b); b['z'] += z; b['name'] = label + '_' + b['name']
            if b['name'] in skip: continue
            if clean:
                b['mat'] = {'wall': 'clean_wall', 'ceiling': 'clean_ceiling'}.get(b['mat'], 'clean_floor' if b['mat'].endswith('_floor') else b['mat'])
            out['boxes'].append(b)
        if mapname == 'clinic':
            out['boxes'] += clinic_stairs(label, k, z, rooms)
            if label == 'G':
                cx0, cy0, cx1, cy1 = rooms['CabE'][:4]
                for (bx, by, bsx, bsy) in ((cx0 - 25, cy0 - 25, cx1 - cx0 + 50, 25), (cx0 - 25, cy1, cx1 - cx0 + 50, 25),
                                           (cx1, cy0, 25, cy1 - cy0), (cx0 - 25, cy0, 25, cy1 - cy0)):
                    out['boxes'].append(dict(name='G_Shaft', mat='metal', x=bx, y=by, z=z - 2000, sx=bsx, sy=bsy, sz=2000))
                out['boxes'].append(dict(name='G_ShaftBottom', mat='metal', x=cx0, y=cy0, z=z - 2020, sx=cx1 - cx0, sy=cy1 - cy0, sz=20))
                out['boxes'].append(dict(name='G_ShaftWreck', mat='metal', x=cx0 + 40, y=cy0 + 30, z=z - 2000, sx=140, sy=120, sz=60))
        elif label != 'B15':
            out['boxes'] += stair_down(label, z, rooms['StairE'][:4], label in OPEN_STAIR)
        out['boxes'] += dressing(label, z, rooms, doors, clean, rnd, cor)
        for i, c in enumerate(cor + [rooms['CorW'][:4], rooms['CorE'][:4]]):           # corridor lights every 8 m
            long_x = (c[2] - c[0]) >= (c[3] - c[1])
            L0, L1 = (c[0], c[2]) if long_x else (c[1], c[3])
            for j, v in enumerate(range(int(L0) + 200, int(L1), 800)):
                lx, ly = (v, (c[1] + c[3]) / 2) if long_x else ((c[0] + c[2]) / 2, v)
                out['lights'].append(dict(name='%s_LC%d_%d' % (label, i, j), x=round(lx), y=round(ly), z=z + 300, i=(330 if clean else 95), r=col[0], g=col[1], b=col[2], rad=800))
        for cid in ('StairW', 'StairE', 'WC1', 'WC2'):
            cx0, cy0, cx1, cy1 = rooms[cid][:4]
            out['lights'].append(dict(name='%s_L%s' % (label, cid), x=round((cx0 + cx1) / 2), y=round((cy0 + cy1) / 2), z=z + 300,
                                      i=(300 if clean else 80), r=col[0], g=col[1], b=col[2], rad=600))
        out['lights'] += [dict(name=label + '_LA', x=500, y=0, z=z + 300, i=(450 if clean else 150), r=1.0 if clean else col[0], g=(0.97 if clean else col[1]), b=(0.92 if clean else 1.0), rad=800),
                          dict(name=label + '_LL', x=ex + 350, y=0, z=z + 300, i=(450 if clean else 180), r=1.0 if clean else col[0], g=(0.85 if clean else col[1]), b=(0.6 if clean else 1.0), rad=800)]
        out['furnish'] += [dict(kind='bench', x=ex + 200, y=330, z=z, yaw=180), dict(kind='bench', x=500, y=-330, z=z, yaw=0)]
        leds = LED_CENTERS.get(label, [])
        for l in out['lights']:
            if not l['name'].startswith(label + '_') or not leds: continue
            cx, cy, cz = min(leds, key=lambda c: (c[0] - l['x']) ** 2 + (c[1] - l['y']) ** 2)
            l['x'], l['y'], l['z'] = round(cx), round(cy), round(cz - 12)
        progrooms = [r for r in info_rooms if r['side'] != 0 and r['type'] != 'wc']
        out['floors'].append(dict(label=label, name=name, z=z, gate=gate, variant=variant,
                                  arrival=((250 if mapname == 'clinic' else -140), 0, z + 100), lift=(ex + 682, LY, z), lift_w=(None if mapname == 'clinic' else (18, 0, z)),
                                  rooms=progrooms, wcs=[r for r in info_rooms if r['type'] == 'wc'], cores=[r for r in info_rooms if r['side'] == 0],
                                  corridors=[list(c) for c in cor + [rooms['CorW'][:4], rooms['CorE'][:4]]],
                                  doors={kk: list(v) for kk, v in doors.items()},
                                  floor_rects=[list(v[:4]) for v in rooms.values()] + [list(v) for v in doors.values()]))
    return out

if __name__ == '__main__':
    m = sys.argv[1] if len(sys.argv) > 1 else 'wards'
    d = build(m)
    json.dump(d, sys.stdout)
    print('%s: floors=%d boxes=%d lights=%d furnish=%d' % (m, len(d['floors']), len(d['boxes']), len(d['lights']), len(d['furnish'])), file=sys.stderr)
