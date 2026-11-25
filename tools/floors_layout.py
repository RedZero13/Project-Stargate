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
    'sluice': ('service', 'concrete', 'SLUICE'), 'plant': ('service', 'concrete', 'PLANT ROOM'), 'storage': ('service', 'concrete', 'SPECIMEN STORE'),
}
# floor programs: north rooms west->east and south rooms west->east as (type, relative width)
MAPS = {
    'wards': [
        ('B2', 'ADMISSIONS', 'keycard', (1.0, 0.82, 0.6),
         [('waiting', 3), ('reception', 2), ('doctor', 1.2), ('doctor', 1.2)], [('pharmacy', 2), ('emergency', 3), ('wc', 1), ('office', 1.4)]),
        ('B3', 'PAEDIATRIC WARD', 'switches', (1.0, 0.75, 0.75),
         [('ward', 3), ('ward', 3), ('private', 1.5)], [('nicu', 2.2), ('nurse', 1.4), ('wc', 1), ('store', 1), ('private', 1.5)]),
        ('B4', 'RADIOLOGY', 'keycard', (0.6, 0.85, 1.0),
         [('xray', 2), ('control', 1), ('xray', 2), ('mri', 2.6)], [('waiting', 2.2), ('nurse', 1.2), ('mri', 2.6), ('wc', 1), ('store', 1)]),
        ('B5', 'SURGERY', 'power', (0.75, 1.0, 0.85),
         [('ot', 3), ('scrub', 1), ('ot', 3)], [('recovery', 3), ('plant', 1.4), ('nurse', 1.2), ('sluice', 1), ('store', 1)]),
        ('B6', 'PHARMACY & BLOOD LAB', 'switches', (1.0, 0.55, 0.5),
         [('pharmacy', 3), ('blood', 2), ('lab', 2)], [('lab', 2), ('cold', 2), ('office', 1.2), ('wc', 1), ('store', 1)]),
        ('B7', 'MORGUE', 'keycard', (0.55, 0.75, 0.95),
         [('morgue', 3), ('autopsy', 2), ('cold', 2)], [('viewing', 2), ('office', 1.2), ('store', 1), ('sluice', 1), ('morgue', 2.4)]),
        ('B8', 'SECURITY & RECORDS', 'power', (0.9, 0.9, 1.0),
         [('security', 2), ('records', 3), ('office', 1.2)], [('records', 2), ('plant', 2), ('office', 1.2), ('wc', 1), ('store', 1)]),
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
        ('B14', 'SEDATION WARD', 'switches', (0.8, 0.7, 1.0),
         [('icu', 3), ('icu', 3)], [('nurse', 1.2), ('private', 1.5), ('private', 1.5), ('store', 1), ('wc', 1)]),
        ('B15', 'ISOLATION CHAMBERS', 'ending', (0.75, 0.7, 1.0),
         [('iso', 1), ('iso', 1), ('iso', 1)], [('iso', 1), ('observe', 1.2), ('iso', 1), ('iso', 1)]),
    ],
}
BASE_Z = {'wards': 0, 'deep': -2000}

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
    elif t == 'iso':
        out += [('bed', cx, back + (-side) * 50, 90 if side < 0 else 270), ('iv', cx + 110, back, 0)]
    return out

SIGN = {'xray': 'sign_xray', 'mri': 'sign_xray', 'ot': 'sign_surgery', 'scrub': 'sign_surgery', 'nicu': 'sign_nursery', 'lab': 'sign_lab',
        'blood': 'sign_lab', 'testing': 'sign_lab', 'reception': 'sign_reception', 'waiting': 'sign_reception'}

def build(mapname):
    out = dict(boxes=[], lights=[], furnish=[], floors=[])
    for k, (label, name, gate, col, north, south) in enumerate(MAPS[mapname]):
        z = BASE_Z[mapname] - k * FLOOR_DZ
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
            b = dict(b); b['z'] += z; b['name'] = label + '_' + b['name']; out['boxes'].append(b)
        for i, lx in enumerate(range(WEST, EAST + 1, 800)):
            out['lights'].append(dict(name='%s_LC%d' % (label, i), x=lx, y=0, z=z + 300, i=110, r=col[0], g=col[1], b=col[2], rad=800))
        out['lights'] += [dict(name=label + '_LA', x=500, y=0, z=z + 300, i=170, r=1.0, g=0.7, b=0.45, rad=800),
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
