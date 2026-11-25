#!/usr/bin/env python3
"""HOLLOW KIN multi-floor generator (docs/EXPANSION_PLAN.md). Each floor is a corridor with 6 themed rooms (3 north,
3 south), an arrival lift room at the west end and the exit lift room at the east end. Floors are stacked
FLOOR_DZ apart in one map. Output JSON (stdout) for tools/unreal_mcp/build_floors.py:
  boxes   - greybox walls/floors/ceilings/lintels (same format as slice_layout.py), z already offset per floor
  lights  - point lights
  furnish - [{kind, x, y, z, yaw}] props placed with Horror Hospital meshes (build_floors.KINDS)
  floors  - per floor: name, label, z, arrival (x,y,z), lift (x,y,z), gate, keycard/switches/generator spots
usage: python3 tools/floors_layout.py wards|deep > floors.json"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import slice_layout as S

FLOOR_DZ = 1500           # vertical distance between floors (cm)
RW, RD = 700, 600         # room width (x) and depth (y)
CW = 150                  # corridor half-width
H = 340                   # ceiling height
X0 = 0                    # west end of the corridor

# themed room templates: furniture relative to the room centre (x along the corridor, y away from it: +y = deeper
# into the room), yaw. Rooms on the north side are mirrored automatically.
T = {
    'ward':      [('bed', -220, 120, 90), ('iv', -120, 200, 0), ('bed', 0, 120, 90), ('iv', 100, 200, 0), ('bed', 220, 120, 90),
                  ('bedside', -300, 230, 0), ('curtain', -110, 60, 0), ('curtain', 110, 60, 0), ('wastebin', 300, 240, 0)],
    'paed':      [('bed', -230, 150, 90), ('bed', 0, 150, 90), ('bed', 230, 150, 90), ('iv', -130, 220, 0), ('iv', 120, 220, 0),
                  ('wheelchair', 280, -150, 200), ('bedside', 320, 240, 0)],
    'xray':      [('xray', 0, 120, 0), ('scanmon', -260, 230, 0), ('desk', 250, 220, 180), ('monitor', 250, 230, 180),
                  ('chair', 250, 150, 0), ('barrier', -200, -40, 90)],
    'mri':       [('angio', 0, 100, 0), ('angiomon', 260, 230, 180), ('cylinder', -280, 240, 0), ('cylinder', -230, 250, 0), ('stretcher', -150, -120, 0)],
    'surgery':   [('treat', 0, 80, 90), ('anesth', -180, 120, 0), ('beddev', 170, 140, 0), ('tray', 120, 30, 0), ('iv', -80, 200, 0),
                  ('disinf', -300, 240, 0), ('wastebin', 300, 240, 0)],
    'lab':       [('fume', -250, 250, 180), ('fume', 0, 250, 180), ('micro', 220, 230, 180), ('desk', 220, 230, 180),
                  ('fridge', 320, -100, 270), ('bloodtest', -250, 0, 90)],
    'blood':     [('bloodcab', -250, 250, 180), ('bloodcab', -100, 250, 180), ('bloodtest', 150, 240, 180), ('fridge', 320, 60, 270),
                  ('treat', 0, 30, 90), ('iv', 80, 100, 0)],
    'morgue':    [('stretcher', -230, 80, 90), ('stretcher', 0, 80, 90), ('stretcher', 230, 80, 90), ('fridge', -300, 250, 180),
                  ('fridge', -200, 250, 180), ('fridge', -100, 250, 180), ('wastebin', 300, 250, 0)],
    'office':    [('desk', -150, 200, 180), ('chair', -150, 120, 0), ('monitor', -150, 210, 180), ('cabinet', 280, 250, 180),
                  ('rack', 0, 260, 180), ('wastebin', -300, 260, 0)],
    'records':   [('rack', -250, 250, 180), ('rack', -80, 250, 180), ('rack', 90, 250, 180), ('rack', 260, 250, 180), ('desk', 0, 20, 0), ('chair', 0, -40, 180)],
    'security':  [('desk', 0, 220, 180), ('monitor', -80, 230, 180), ('monitor', 80, 230, 180), ('chair', 0, 150, 0), ('cam', 300, 280, 225), ('rack', -280, 250, 180)],
    'storage':   [('rack', -250, 250, 180), ('rack', 0, 250, 180), ('rack', 250, 250, 180), ('cylinder', 300, -100, 0), ('cylinder', 260, -60, 0), ('fridge', -320, 0, 90)],
    'testing':   [('treat', 0, 120, 90), ('dentist', -230, 160, 0), ('scanmon', 230, 230, 180), ('beddev', 130, 200, 0), ('iv', -100, 220, 0), ('tray', 60, 40, 0)],
    'observe':   [('desk', -200, 230, 180), ('monitor', -200, 240, 180), ('chair', -200, 160, 0), ('desk', 150, 230, 180), ('monitor', 150, 240, 180), ('bench', 0, -80, 0)],
    'sedation':  [('bed', -230, 140, 90), ('bed', 0, 140, 90), ('bed', 230, 140, 90), ('iv', -120, 220, 0), ('iv', 120, 220, 0), ('anesth', 320, 200, 270)],
    'reception': [('reception', 0, 150, 180), ('bench', -230, -60, 0), ('bench', 230, -60, 0), ('wastebin', 300, 250, 0), ('cabinet', -300, 250, 180)],
    'isolation': [('bed', 0, 180, 0), ('iv', 120, 220, 0), ('bedside', -150, 240, 0)],
}
SIGN = {'xray': 'sign_xray', 'mri': 'sign_xray', 'surgery': 'sign_surgery', 'paed': 'sign_nursery', 'lab': 'sign_lab',
        'blood': 'sign_lab', 'testing': 'sign_lab', 'reception': 'sign_reception'}

# floor specs: (label, name, [6 room themes: north west->east, then south west->east], gate, light colour)
MAPS = {
    'wards': [
        ('B2', 'ADMISSIONS',        ['reception', 'office', 'ward', 'ward', 'records', 'storage'],  'keycard', (1.0, 0.82, 0.6)),
        ('B3', 'PAEDIATRIC WARD',   ['paed', 'paed', 'office', 'paed', 'storage', 'paed'],          'switches', (1.0, 0.75, 0.75)),
        ('B4', 'RADIOLOGY',         ['xray', 'mri', 'office', 'xray', 'storage', 'mri'],            'keycard', (0.6, 0.85, 1.0)),
        ('B5', 'SURGERY',           ['surgery', 'surgery', 'storage', 'ward', 'surgery', 'office'], 'power', (0.75, 1.0, 0.85)),
        ('B6', 'PHARMACY & BLOOD LAB', ['lab', 'blood', 'storage', 'blood', 'lab', 'office'],       'switches', (1.0, 0.55, 0.5)),
        ('B7', 'MORGUE',            ['morgue', 'morgue', 'office', 'morgue', 'storage', 'surgery'], 'keycard', (0.55, 0.75, 0.95)),
        ('B8', 'SECURITY & RECORDS', ['security', 'records', 'office', 'records', 'storage', 'security'], 'power', (0.9, 0.9, 1.0)),
    ],
    'deep': [
        ('B10', 'SPECIMEN STORAGE', ['storage', 'lab', 'storage', 'morgue', 'storage', 'lab'],      'keycard', (0.6, 0.9, 0.85)),
        ('B11', 'TESTING LAB A',    ['testing', 'lab', 'testing', 'observe', 'testing', 'storage'], 'switches', (0.85, 0.95, 1.0)),
        ('B12', 'TESTING LAB B',    ['testing', 'surgery', 'morgue', 'testing', 'lab', 'testing'],  'power', (1.0, 0.45, 0.4)),
        ('B13', 'OBSERVATION',      ['observe', 'testing', 'security', 'observe', 'records', 'testing'], 'keycard', (0.7, 0.8, 1.0)),
        ('B14', 'SEDATION WARD',    ['sedation', 'sedation', 'office', 'sedation', 'storage', 'sedation'], 'switches', (0.8, 0.7, 1.0)),
        ('B15', 'ISOLATION CHAMBERS', ['isolation', 'isolation', 'isolation', 'isolation', 'isolation', 'isolation'], 'ending', (0.75, 0.7, 1.0)),
    ],
}
# where each map's generated floors start (deep: below the existing B9 Deep Labs level)
BASE_Z = {'wards': 0, 'deep': -2000}

def floor_rooms():
    """Room rectangles of one floor (z-independent): 3 north + 3 south rooms, west arrival, east lift."""
    rooms, doors = {}, {}
    L = 3 * RW + 4 * 25 + 600            # corridor length
    rooms['Corr'] = (X0 + 600, -CW, X0 + 600 + L, CW, H, 'tile')
    rooms['Arrive'] = (X0, -300, X0 + 575, 300, H, 'concrete')
    doors['Arrive'] = (X0 + 575, -CW + 25, X0 + 600, CW - 25)
    ex = X0 + 600 + L + 25
    rooms['Lift'] = (ex, -300, ex + 600, 300, H, 'concrete')
    doors['Lift'] = (ex - 25, -100, ex, 100)
    slots = []
    for i in range(3):
        x0 = X0 + 900 + i * (RW + 25)
        rooms['N%d' % i] = (x0, -CW - 25 - RD, x0 + RW, -CW - 25, H, 'warm')
        doors['N%d' % i] = (x0 + RW // 2 - 100, -CW - 25, x0 + RW // 2 + 100, -CW)
        slots.append(('N%d' % i, x0 + RW / 2, -CW - 25 - RD / 2, -1))
    for i in range(3):
        x0 = X0 + 900 + i * (RW + 25)
        rooms['S%d' % i] = (x0, CW + 25, x0 + RW, CW + 25 + RD, H, 'warm')
        doors['S%d' % i] = (x0 + RW // 2 - 100, CW, x0 + RW // 2 + 100, CW + 25)
        slots.append(('S%d' % i, x0 + RW / 2, CW + 25 + RD / 2, 1))
    return rooms, doors, slots, ex

def build(mapname):
    out = dict(boxes=[], lights=[], furnish=[], floors=[])
    for k, (label, name, themes, gate, col) in enumerate(MAPS[mapname]):
        z = BASE_Z[mapname] - k * FLOOR_DZ
        rooms, doors, slots, ex = floor_rooms()
        S.ROOMS = {label + '_' + n: r for n, r in rooms.items()}
        S.DOORS = {label + '_' + n: d for n, d in doors.items()}
        S.PROPS = []
        for b in S.build():
            b = dict(b); b['z'] = b['z'] + z; b['name'] = label + '_' + b['name']; out['boxes'].append(b)
        # lights: corridor (3), each room, arrival, lift
        for i, lx in enumerate((X0 + 1100, X0 + 1900, X0 + 2700)):
            out['lights'].append(dict(name='%s_LC%d' % (label, i), x=lx, y=0, z=z + 300, i=140, r=col[0], g=col[1], b=col[2], rad=900))
        out['lights'].append(dict(name=label + '_LA', x=X0 + 300, y=0, z=z + 300, i=160, r=1.0, g=0.7, b=0.45, rad=800))
        out['lights'].append(dict(name=label + '_LL', x=ex + 300, y=0, z=z + 300, i=220, r=1.0, g=0.85, b=0.6, rad=800))
        info = dict(label=label, name=name, z=z, gate=gate, arrival=(X0 + 250, 0, z + 100), lift=(ex + 400, 0, z), rooms=[])
        for (rn, cx, cy, side), theme in zip(slots, themes):
            out['lights'].append(dict(name='%s_L%s' % (label, rn), x=cx, y=cy, z=z + 300, i=120 if theme != 'morgue' else 70,
                                      r=col[0], g=col[1], b=col[2], rad=700))
            for (kind, fx, fy, yaw) in T[theme]:
                out['furnish'].append(dict(kind=kind, x=cx + fx, y=cy + side * fy, z=z, yaw=(yaw if side > 0 else (yaw + 180) % 360)))
            if theme in SIGN:   # sign over the doorway, on the corridor side
                out['furnish'].append(dict(kind=SIGN[theme], x=cx, y=side * (CW + 2), z=z + 250, yaw=(90 if side > 0 else 270)))
            info['rooms'].append(dict(id=rn, theme=theme, x=cx, y=cy, side=side))
        # lift room dressing
        out['furnish'] += [dict(kind='lift', x=ex + 580, y=0, z=z, yaw=270), dict(kind='bench', x=ex + 150, y=250, z=z, yaw=180)]
        out['floors'].append(info)
    return out

if __name__ == '__main__':
    m = sys.argv[1] if len(sys.argv) > 1 else 'wards'
    d = build(m)
    json.dump(d, sys.stdout)
    print('%s: floors=%d boxes=%d lights=%d furnish=%d' % (m, len(d['floors']), len(d['boxes']), len(d['lights']), len(d['furnish'])), file=sys.stderr)
