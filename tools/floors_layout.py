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
    'commonward': ('clinical', 'tile', 'COMMON WARD'), 'isoward': ('clinical', 'tile', 'ISOLATION WARD'), 'plant': ('service', 'concrete', 'PLANT ROOM'), 'storage': ('service', 'concrete', 'SPECIMEN STORE'),
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
        for i in range(n): out.append((kind, x0 + margin + i * step if n > 1 else cx, y, yaw))
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
            row('fume', max(1, int(w // 220)), back, face, 110); out += [('micro', cx, front, face + 180), ('bloodtest', x1 - 90, cy, 270)]
        else:
            out += [('dentist', cx, cy, face), ('scanmon', x0 + 90, back, face), ('beddev', x1 - 100, back, face), ('iv', cx + 120, cy, 0), ('tray', cx - 110, cy, 0)]
    elif t == 'blood':
        row('bloodcab', max(1, int(w // 170)), back, face, 90); out += [('treat', cx, cy, 90), ('iv', cx + 110, cy, 0), ('fridge', x1 - 60, front, 270)]
    elif t == 'cold' or t == 'morgue':
        row('fridge', max(1, int(w // 110)), back, face, 60)
        if t == 'morgue': row('stretcher', max(1, int(w // 280)), cy, 90, 150)
    elif t == 'storage' or t == 'store' or t == 'records' or t == 'plant':
        if t == 'plant': out += [('cylinder', x0 + 80, back, 0), ('cylinder', x0 + 140, back, 0), ('cabinet', x1 - 80, back, face)]
        else: row('rack', max(1, int(w // 190)), back, face, 100)
        if t == 'records': row('rack', max(1, int(w // 190)), cy, face, 100)
    elif t == 'waiting' or t == 'viewing':
        row('bench', max(1, int(w // 260)), cy - side * 60, face, 150); row('bench', max(1, int(w // 260)), cy + side * 120, face, 150)
        out.append(('wastebin', x1 - 60, front, 0))
    elif t in ('nurse', 'reception'):
        out += [('reception', cx, cy - side * 20, face + 180), ('chair', cx, back, face), ('cabinet', x0 + 80, back, face), ('monitor', cx + 60, cy - side * 20, face)]
    elif t == 'pharmacy':
        row('rack', max(1, int(w // 190)), back, face, 100); out.append(('reception', cx, front - side * -10, face + 180))
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
    elif t == 'iso':
        out += [('bed', cx, back + (-side) * 50, 90 if side < 0 else 270), ('iv', cx + 110, back, 0)]
    return out

SIGN = {'maternity': 'sign_nursery', 'opd': 'sign_reception', 'emergency': 'sign_reception', 'xray': 'sign_xray', 'mri': 'sign_xray', 'ot': 'sign_surgery', 'scrub': 'sign_surgery', 'nicu': 'sign_nursery', 'lab': 'sign_lab',
        'blood': 'sign_lab', 'testing': 'sign_lab', 'reception': 'sign_reception', 'waiting': 'sign_reception'}

def dressing(label, z, rooms, doors, clean, rnd):
    """flat LED ceiling panels everywhere; clean floors also get floor inlay strips, accent door frames, handrails and
    frosted daylight windows on the outer walls."""
    bx = []
    def B(name, mat, x, y, zz, sx, sy, sz): bx.append(dict(name='%s_%s' % (label, name), mat=mat, x=x, y=y, z=z + zz, sx=sx, sy=sy, sz=sz))
    led = 'led' if clean else 'led_dim'
    n = 0
    for rid, (x0, y0, x1, y1, h, m) in rooms.items():
        w, d = x1 - x0, y1 - y0
        if rid in ('StairW', 'StairE', 'WCW'): continue
        nx = max(1, int(w // 300)); ny = max(1, int(d // 300))
        for i in range(nx):
            for j in range(ny):
                if not clean and rnd.random() < 0.18: continue          # dead panels in the basements
                cx = x0 + (i + 0.5) * w / nx; cy = y0 + (j + 0.5) * d / ny
                B('LED%d' % n, led, cx - 60, cy - 30, h - 3, 120, 60, 3); n += 1
    if not clean: return bx
    corr = rooms['Corr']
    for k, yy in enumerate((-90, 90)):                                     # grey inlay strips along the passage
        B('Inlay%d' % k, 'clean_inlay', corr[0] + 50, yy - 6, 0.2, corr[2] - corr[0] - 100, 12, 0.6)
    for xx in range(int(corr[0]) + 300, int(corr[2]) - 100, 400):          # cross bands every 4 m
        B('Band%d' % xx, 'clean_inlay', xx, -60, 0.2, 40, 120, 0.6)
    acc = 'clean_yellow' if label == 'G' else 'clean_teal'
    gaps = {-1: [], 1: []}
    for rid, (dx0, dy0, dx1, dy1) in doors.items():
        if dy1 - dy0 == 25 and abs(dy0 + 12.5) >= CORR - 15:              # doors in the corridor walls
            side = -1 if dy0 < 0 else 1
            gaps[side].append((dx0, dx1))
            fy = -CORR if side < 0 else CORR - 4
            B('Frame%sL' % rid, acc, dx0 - 12, fy, 0, 12, 4, 245); B('Frame%sR' % rid, acc, dx1, fy, 0, 12, 4, 245)
            B('Frame%sT' % rid, acc, dx0 - 12, fy, 240, dx1 - dx0 + 24, 4, 12)
    for side in (-1, 1):                                                   # handrails between the doors
        xs = [corr[0] + 20] + [v for g in sorted(gaps[side]) for v in (g[0] - 20, g[1] + 20)] + [corr[2] - 20]
        ry = -CORR if side < 0 else CORR - 6
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 40: B('Rail%d%d' % (side + 1, i), 'clean_rail', xs[i], ry, 88, xs[i + 1] - xs[i], 6, 8)
    for rid, (x0, y0, x1, y1, h, m) in rooms.items():                      # frosted daylight windows on outer walls
        if rid[0] in 'NS' and rid[1:].isdigit():
            wy = y0 - 2 if rid[0] == 'N' else y1 - 1
            for i in range(max(1, int((x1 - x0) // 350))):
                cx = x0 + (i + 0.5) * (x1 - x0) / max(1, int((x1 - x0) // 350))
                B('Win%s%d' % (rid, i), 'window', cx - 90, wy, 110, 180, 3, 120)
    return bx

def build(mapname):
    out = dict(boxes=[], lights=[], furnish=[], floors=[])
    for k, (label, name, gate, col, north, south) in enumerate(MAPS[mapname]):
        z = BASE_Z[mapname] + DZ_SIGN.get(mapname, -1) * k * FLOOR_DZ
        clean = mapname in CLEAN
        rnd = random.Random(hash(label) & 0xffff)
        rooms, doors, info_rooms = {}, {}, []
        # circulation + cores
        rooms['Corr'] = (WEST - 350, -CORR, EAST + 350, CORR, H, 'tile')
        rooms['Lobby'] = (0, -400, WEST - 375, 400, H, 'concrete')          # arrival lift lobby
        doors['Lobby'] = (WEST - 375, -CORR + 25, WEST - 350, CORR - 25)
        rooms['StairW'] = (WEST - 350, -CORR - 25 - DEPTH, WEST - 25, -CORR - 25, H, 'concrete')
        doors['StairW'] = (WEST - 300, -CORR - 25, WEST - 75, -CORR)
        rooms['WCW'] = (WEST - 350, CORR + 25, WEST - 25, CORR + 25 + DEPTH, H, 'concrete')
        doors['WCW'] = (WEST - 300, CORR, WEST - 75, CORR + 25)
        ex = EAST + 375
        rooms['Lift'] = (ex, -400, ex + 700, 400, H, 'concrete')            # exit lift room
        doors['Lift'] = (EAST + 350, -150, ex, 150)
        rooms['StairE'] = (EAST + 25, -CORR - 25 - DEPTH, EAST + 350, -CORR - 25, H, 'concrete')
        doors['StairE'] = (EAST + 75, -CORR - 25, EAST + 300, -CORR)
        for rid, t, zone in (('Lobby', 'core', 'core'), ('StairW', 'stair', 'core'), ('WCW', 'wc', 'service'), ('Lift', 'core', 'core'), ('StairE', 'stair', 'core')):
            x0, y0, x1, y1 = rooms[rid][:4]
            info_rooms.append(dict(id=rid, type=t, zone=zone, x0=x0, y0=y0, x1=x1, y1=y1, x=(x0 + x1) / 2, y=(y0 + y1) / 2, side=0))
        # program rooms
        for side, prog in ((-1, north), (1, south)):
            ws = split(prog); x = WEST
            for i, ((t, _), wd) in enumerate(zip(prog, ws)):
                x0, x1 = x, x + wd
                y0, y1 = (-CORR - 25 - DEPTH, -CORR - 25) if side < 0 else (CORR + 25, CORR + 25 + DEPTH)
                rid = ('N' if side < 0 else 'S') + str(i)
                zone, mat, _ = ZONE[t]
                rooms[rid] = (x0, y0, x1, y1, H, mat)
                dw = 300 if t in ('nurse', 'reception', 'waiting') else 200 if wd >= 400 else 150
                dw = min(dw, wd - 50) // 25 * 25
                dc = (x0 + x1) // 2 // 25 * 25
                doors[rid] = (dc - dw // 2, -CORR - 25, dc + dw // 2, -CORR) if side < 0 else (dc - dw // 2, CORR, dc + dw // 2, CORR + 25)
                info_rooms.append(dict(id=rid, type=t, zone=zone, x0=x0, y0=y0, x1=x1, y1=y1, x=(x0 + x1) / 2, y=(y0 + y1) / 2, side=side))
                for (kind, fx, fy, yaw) in furnish(t, x0, y0, x1, y1, side):
                    out['furnish'].append(dict(kind=kind, x=round(fx), y=round(fy), z=z, yaw=yaw % 360))
                if t in SIGN:
                    out['furnish'].append(dict(kind=SIGN[t], x=dc, y=side * (CORR - 2), z=z + 255, yaw=(90 if side > 0 else 270)))
                nl = max(1, int(wd // 450))
                for j in range(nl):
                    lx = x0 + (j + 0.5) * wd / nl
                    dim = 0.6 if t in ('morgue', 'cold', 'storage', 'plant', 'store') else 1.0
                    out['lights'].append(dict(name='%s_L%s%d' % (label, rid, j), x=round(lx), y=round((y0 + y1) / 2), z=z + 300, i=int(130 * dim),
                                              r=col[0], g=col[1], b=col[2], rad=650))
                x = x1 + T
        S.ROOMS = {label + '_' + n: r for n, r in rooms.items()}
        S.DOORS = {label + '_' + n: d for n, d in doors.items()}
        S.PROPS = []
        for b in S.build():
            b = dict(b); b['z'] += z; b['name'] = label + '_' + b['name']
            if clean:
                b['mat'] = {'wall': 'clean_wall', 'ceiling': 'clean_ceiling'}.get(b['mat'], 'clean_floor' if b['mat'].endswith('_floor') else b['mat'])
            out['boxes'].append(b)
        out['boxes'] += dressing(label, z, rooms, doors, clean, rnd)
        for i, lx in enumerate(range(WEST, EAST + 1, 800)):
            out['lights'].append(dict(name='%s_LC%d' % (label, i), x=lx, y=0, z=z + 300, i=110, r=col[0], g=col[1], b=col[2], rad=800))
        out['lights'] += [dict(name=label + '_LA', x=500, y=0, z=z + 300, i=170, r=1.0, g=(0.97 if clean else 0.7), b=(0.92 if clean else 0.45), rad=800),
                          dict(name=label + '_LL', x=ex + 350, y=0, z=z + 300, i=220, r=1.0, g=0.85, b=0.6, rad=800)]
        out['furnish'] += [dict(kind='lift', x=ex + 670, y=0, z=z, yaw=270), dict(kind='bench', x=ex + 200, y=330, z=z, yaw=180),
                           dict(kind='lift', x=30, y=0, z=z, yaw=90), dict(kind='bench', x=500, y=-330, z=z, yaw=0),
                           dict(kind='washstand', x=WEST - 190, y=CORR + 25 + DEPTH - 60, z=z, yaw=180)]
        prog = [r for r in info_rooms if r['side'] != 0]
        out['floors'].append(dict(label=label, name=name, z=z, gate=gate, arrival=(250, 0, z + 100), lift=(ex + 450, 0, z),
                                  rooms=prog, cores=[r for r in info_rooms if r['side'] == 0]))
    return out

if __name__ == '__main__':
    m = sys.argv[1] if len(sys.argv) > 1 else 'wards'
    d = build(m)
    json.dump(d, sys.stdout)
    print('%s: floors=%d boxes=%d lights=%d furnish=%d' % (m, len(d['floors']), len(d['boxes']), len(d['lights']), len(d['furnish'])), file=sys.stderr)
