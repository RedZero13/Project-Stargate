"""Anti-clipping pass over the stacked floors (run last, after build_floors / dress_floors / place_floors), level open.
usage: python3 declip.py clinic|wards|deep [labels...]
For every floor it reads the real world bounds of each placed object and:
1) pushes floor furniture, floor dressing, dead bodies and pickups back inside the room they stand in (no more
   beds or bodies half inside a wall);
2) separates overlapping objects: biggest first, a smaller object that overlaps a bigger one is slid to the nearest
   free spot in the same room; dressing that cannot find a spot is removed (furniture and bodies are always kept).
Wall-mounted dressing, desk-top items, lifts, signs and puzzle props are obstacles only and never move."""
import json, os, re, sys
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'
HERE = os.path.dirname(os.path.abspath(__file__))
m = sys.argv[1]; only = sys.argv[2:]
floors = json.load(open(os.path.join(HERE, 'floors_%s.json' % m)))
src = open(os.path.join(HERE, 'dress_floors.py')).read()
DRESS_WH = {k: (None if v == 'None' else int(v)) for k, v in re.findall(r"'(\w+)': \(P\('[^']+'\), (None|-?\d+)", src)}
FIXED_WORDS = ('lift', 'sign', 'Breaker', 'Dial', 'CellConsole', 'Generator', 'Keycard', 'Switch', 'Hint', 'Emilia', 'Child',
               'EndingTrigger', 'monitor', 'micro', 'cam', 'mug', 'Cutscene', 'CS_')
def rect_rooms(fl):
    rs = [(r['x0'], r['y0'], r['x1'], r['y1']) for r in fl['rooms'] + fl.get('cores', [])]
    rs.append((850, -200, 4750, 200))                    # corridor (WEST-350 .. EAST+350, 4 m wide)
    return rs
def room_of(rs, x, y):
    best = None
    for r in rs:
        if r[0] <= x <= r[2] and r[1] <= y <= r[3]: return r
        d = max(r[0] - x, 0, x - r[2]) + max(r[1] - y, 0, y - r[3])
        if best is None or d < best[0]: best = (d, r)
    return best[1]
def bounds(a):
    b = call(AT, 'get_actor_bounds', {'actor': a}).get('returnValue')
    return (b['min']['x'], b['min']['y'], b['min']['z'], b['max']['x'], b['max']['y'], b['max']['z']) if b else None
def overlap(a, b, pad=2):
    ix = min(a[3], b[3]) - max(a[0], b[0]) - pad; iy = min(a[4], b[4]) - max(a[1], b[1]) - pad; iz = min(a[5], b[5]) - max(a[2], b[2])
    return ix > 0 and iy > 0 and iz > 8
def move(a, dx, dy):
    t = call(AT, 'get_actor_transform', {'actor': a})['returnValue']
    loc = t['location']; loc = {'x': loc['x'] + dx, 'y': loc['y'] + dy, 'z': loc['z']}
    xf = {'location': loc, 'rotation': t['rotation']}
    if 'scale' in t: xf['scale'] = t['scale']
    call(AT, 'set_actor_transform', {'actor': a, 'xform': xf, 'worldspace': True})
def fit(bb, r, inset=3):
    """shift that keeps bb inside room r (0 on an axis where the object is bigger than the room)"""
    dx = dy = 0.0
    if bb[3] - bb[0] < r[2] - r[0] - 2 * inset:
        if bb[0] < r[0] + inset: dx = r[0] + inset - bb[0]
        elif bb[3] > r[2] - inset: dx = r[2] - inset - bb[3]
    if bb[4] - bb[1] < r[3] - r[1] - 2 * inset:
        if bb[1] < r[1] + inset: dy = r[1] + inset - bb[1]
        elif bb[4] > r[3] - inset: dy = r[3] - inset - bb[4]
    return dx, dy
def sh(bb, dx, dy): return (bb[0] + dx, bb[1] + dy, bb[2], bb[3] + dx, bb[4] + dy, bb[5])
STEPS = [(dx, dy) for rad in (30, 60, 90, 120, 160, 200, 250) for dx, dy in
         ((rad, 0), (-rad, 0), (0, rad), (0, -rad), (rad, rad), (-rad, rad), (rad, -rad), (-rad, -rad))]
total = {'pushed': 0, 'slid': 0, 'removed': 0}
for fl in floors:
    L = fl['label']
    if only and L not in only: continue
    rs = rect_rooms(fl)
    acts = []
    for tag, cat in (('Floor_' + L, 'furn'), ('Dress_' + L, 'dress'), ('FloorGP', 'gp')):
        for a in call(S, 'find_actors', {'name': '', 'tag': tag, 'collision_channels': []})['returnValue']:
            name = str(call(AT, 'get_label', {'actor': a}).get('returnValue') or '')
            if not name.startswith(L + '_') and not name.startswith('CS_'): continue
            if cat == 'furn':
                parts = name.split('_')
                if len(parts) < 3 or not parts[-1].isdigit(): continue        # geometry boxes / lights / LEDs
                kind = parts[1]
                if kind in ('curtain', 'barrier', 'rug'): continue            # meant to wrap around beds
                role = 'fixed' if any(w in kind for w in FIXED_WORDS) else 'keep'
            elif cat == 'dress':
                kind = name.split('_')[1] if name.count('_') >= 2 else ''
                wh = DRESS_WH.get(kind)
                if kind not in DRESS_WH: continue                              # decals
                role = 'fixed' if (wh is not None and wh > 0) else 'drop'
            else:
                if any(w in name for w in FIXED_WORDS) or 'Lift' in name: role = 'fixed'
                elif 'Dead' in name or 'Pickup' in name or 'Drawing' in name or 'PatientFile' in name or 'Serum' in name: role = 'keep'
                else: continue                                                 # enemies, hints
            bb = bounds(a)
            if bb and bb[3] - bb[0] < 2000: acts.append([a, name, role, bb])
    # 1) inside the room
    for it in acts:
        if it[2] == 'fixed': continue
        bb = it[3]; r = room_of(rs, (bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2)
        dx, dy = fit(bb, r)
        if abs(dx) > 1 or abs(dy) > 1:
            move(it[0], dx, dy); it[3] = sh(bb, dx, dy); total['pushed'] += 1
    # 2) separate overlaps, biggest first
    area = lambda bb: (bb[3] - bb[0]) * (bb[4] - bb[1])
    placed = [it for it in acts if it[2] == 'fixed']
    for it in sorted([i for i in acts if i[2] != 'fixed'], key=lambda i: -area(i[3])):
        bb = it[3]
        if not any(overlap(bb, p[3]) for p in placed):
            placed.append(it); continue
        r = room_of(rs, (bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2)
        done = False
        for dx, dy in STEPS:
            nb = sh(bb, dx, dy); fx, fy = fit(nb, r)
            if abs(fx) > 1 or abs(fy) > 1: continue
            if not any(overlap(nb, p[3]) for p in placed):
                move(it[0], dx, dy); it[3] = nb; placed.append(it); total['slid'] += 1; done = True; break
        if not done:
            if it[2] == 'drop':
                call(S, 'remove_from_scene', {'actor': it[0]}); total['removed'] += 1
            else:
                placed.append(it)
    print(L, len(acts), dict(total), flush=True)
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
