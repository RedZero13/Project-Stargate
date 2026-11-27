"""Lived-in dressing for the stacked floors (on top of build_floors.py furniture), after real hospitals:
wall clocks, notice boards and posters, AC units, extinguisher boxes, exit signs, radiators, chairs beside beds,
plants, bins, boxes, scattered papers and supplies; corridors get benches, parked wheelchairs/stretchers and signage.
Then decals: floor dirt, wall grunge, water/rust leaks, cracks, chipped tiles, broken glass and blood, scaled by the
map's grime level (clinic light, wards medium, deep heavy).
usage: python3 dress_floors.py clinic|wards|deep [labels...]   (the level must be open). Tag Dress_<label>."""
import sys, json, random, os
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
HH = '/Game/Horror_Hospital/Meshes/'; DC = '/Game/Horror_Hospital/Decals/'; BD = '/Game/BloodDecals/Materials/'
m = sys.argv[1]; only = sys.argv[2:]
GRIME = {'clinic': 0.25, 'wards': 0.65, 'deep': 1.0}[m]
CORR = 200; H = 340
floors = json.load(open(os.path.join(os.path.dirname(__file__), 'floors_%s.json' % m)))
lvl = str(call(S, 'get_current_level', {})['returnValue'])
assert {'clinic': 'Lvl_Clinic', 'wards': 'Lvl_Wards', 'deep': 'Lvl_DeepLabs'}[m] in lvl, 'open the right level first: ' + lvl
P = lambda n: HH + n + '.' + n
# kind: (mesh, wall_height or None (floor), yaw offset so the front faces away from the wall)
PROPS = {
    'clock': (P('SM_Clock_01_v01'), 230, 0), 'board': (P('SM_Board_04_v01'), 150, 0), 'board2': (P('SM_Board_01_v01'), 150, 0),
    'poster': (P('SM_Image_Board_02_v01'), 160, 0), 'poster2': (P('SM_Image_Board_05_v01'), 160, 0), 'ac': (P('SM_Air_Conditioner_01_v01'), 270, 0),
    'extbox': (P('SM_Extinguisher_Box_02_v01'), 110, 0), 'exit': (P('SM_Emergency_Exit_01_v01'), 255, 0), 'firept': (P('SM_Fire_Point_01_v01'), 140, 0),
    'radiator': (P('SM_Radiator_01_v01'), 15, 0), 'vent': (P('SM_Vent_02_v01'), 300, 0), 'calendar': (P('SM_Calendar_01_v01'), 160, 0),
    'speaker': (P('SM_Speaker_01_v01'), 290, 0), 'sign': (P('SM_Hospital_Board_Sign_01_v01'), 230, 0),
    'chair': (P('SM_Chair_01_v01'), None, 0), 'chair2': (P('SM_Chair_02_v01'), None, 0), 'plant': (P('SM_Plant_01_v01'), None, 0),
    'trash': (P('SM_TrashCan_01_v01'), None, 0), 'basket': (P('SM_TrashBasket_01_v01'), None, 0), 'box': (P('SM_Cardboard_01_v01'), None, 0),
    'box2': (P('SM_Cardboard_04_v01'), None, 0), 'paper': (P('SM_Paper_01_v02'), None, 0), 'paper2': (P('SM_Paper_02_v01'), None, 0),
    'book': (P('SM_Book_01_v05'), None, 0), 'bandage': (P('SM_Bandage_01_v03'), None, 0), 'bloodbag': (P('SM_BloodBag_01_v01'), None, 0),
    'wheelchair': (P('SM_Wheel_Chair_01_v01'), None, 0), 'stretcher': (P('SM_Stretcher_02_v01'), None, 0), 'bench': (P('SM_Bench_01_v01'), None, 0),
    'bin': (P('SM_Medical_Waste_Bin_02_v01'), None, 0), 'bucket': (P('SM_Bucket_01_v01') if False else P('SM_TrashBasket_01_v01'), None, 0),
    'cart': ('/Game/RestaurantScene/Meshes/SM_UtilityCart.SM_UtilityCart', None, 0), 'tray': (P('SM_Tray_01_v01'), None, 0),
}
DEC = {'dirt': [DC + 'MI_Floor_Dirt_0%d_Decal' % i for i in range(1, 6)], 'grunge': [DC + 'MI_Grunge_01_Decal', DC + 'MI_Grunge_02_Decal'],
       'leak': [DC + 'MI_Water_Leak_Decal', DC + 'MI_Rust_Leak_Decal'], 'crack': [DC + 'MI_Crack_0%d_Decal' % i for i in range(1, 5)],
       'chip': [DC + 'MI_Chipped_Ceramic_Decal', DC + 'MI_Concrete_Demage_01_Decal'], 'glass': [DC + 'MI_Glass_Broken_Decal'],
       'blood': [DC + 'MI_Blood_Stain_01_Decal', DC + 'MI_Blood_Stain_02_Decal', DC + 'MI_Blood_Puddle_01_Decal', BD + 'MI_Blood_Splatter', BD + 'MI_Blood_Trail'],
       'bloodwall': [DC + 'MI_Blood_Leaks_Decal', BD + 'MI_Blood_Splatter']}
def full(p): return p if '.' in p.split('/')[-1] else p + '.' + p.split('/')[-1]
def tag(a, L, lbl, folder):
    call(AT, 'add_tag', {'actor': a, 'tag': 'Dress_' + L}); call(AT, 'add_tag', {'actor': a, 'tag': 'Dress'})
    call(AT, 'set_label', {'actor': a, 'label': lbl}); call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Floors/%s/Lived' % L + folder})
n = [0]
def prop(L, kind, x, y, z, wall=None, yaw=0.0):
    """wall: (axis 'y', plane value, normal sign) -> back of the prop touches the wall plane, front faces the normal."""
    mesh, wh, yo = PROPS[kind]
    if wall:
        yaw = (0 if wall[2] > 0 else 180) + yo
    a = call(S, 'add_to_scene_from_asset', {'asset_path': mesh, 'name': '%s_L%d' % (L, n[0]), 'xform': {'location': {'x': x, 'y': y, 'z': z + 400}, 'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}}})
    a = a.get('returnValue') if isinstance(a, dict) else None
    if not a: return
    bb = call(AT, 'get_actor_bounds', {'actor': a})['returnValue']
    nz = z + 400 + ((z + wh) - bb['min']['z'] if wh is not None else z - bb['min']['z'] + 0.5 - 0) - 0 if False else None
    nz = (z + 400) + ((z + (wh if wh is not None else 0)) - bb['min']['z'])
    ny = y
    if wall:
        plane, sgn = wall[1], wall[2]
        ny = y + ((plane + 1 - bb['min']['y']) if sgn > 0 else (plane - 1 - bb['max']['y']))
    call(AT, 'set_actor_transform', {'actor': a, 'xform': {'location': {'x': x, 'y': ny, 'z': nz}, 'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}}, 'worldspace': True})
    tag(a, L, '%s_%s_%d' % (L, kind, n[0]), ''); n[0] += 1
def decal(L, cat, x, y, z, size, pitch=-90, yaw=0, depth=30):
    a = call(S, 'add_to_scene_from_class', {'actor_type': {'refPath': '/Script/Engine.DecalActor'}, 'name': '%s_D%d' % (L, n[0]),
        'xform': {'location': {'x': x, 'y': y, 'z': z}, 'rotation': {'pitch': pitch, 'yaw': yaw, 'roll': 0}}})['returnValue']
    c = call(AT, 'get_components', {'actor': a, 'component_type': {'refPath': '/Script/Engine.DecalComponent'}})['returnValue'][0]
    call(O, 'set_properties', {'instance': c, 'values': json.dumps({'DecalMaterial': full(random.choice(DEC[cat])), 'DecalSize': {'x': depth, 'y': size, 'z': size}, 'SortOrder': n[0] % 50})})
    tag(a, L, '%s_decal_%s_%d' % (L, cat, n[0]), ''); n[0] += 1
def wall_decal(L, cat, x, wall_y, normal, z, size):
    # decal projects along +X: yaw so X points INTO the wall
    decal(L, cat, x, wall_y - normal * 5, z, size, pitch=0, yaw=(-90 if normal > 0 else 90), depth=20)
for fl in floors:
    L = fl['label']
    if only and L not in only: continue
    z = fl['z']; rnd = random.Random(sum(map(ord, L)) * 31 + 5); random.seed(sum(map(ord, L)))
    for a in call(S, 'find_actors', {'name': '', 'tag': 'Dress_' + L, 'collision_channels': []})['returnValue']:
        call(S, 'remove_from_scene', {'actor': a})
    clean = (m == 'clinic')
    # ---------- corridors (any shape: spine / ring / jog / hall) ----------
    FR = fl.get('floor_rects', [])
    def solid(x, y):        # is (x, y) inside a wall (not on any floor area)?
        return not any(r[0] - 1 <= x <= r[2] + 1 and r[1] - 1 <= y <= r[3] + 1 for r in FR)
    cors = fl.get('corridors', [[850, -CORR, 4750, CORR]])
    for ci, (cx0, cy0, cx1, cy1) in enumerate(cors):
        if cx1 - cx0 < 600: continue
        for wy, nrm in ((cy0, 1), (cy1, -1)):          # the two long walls
            xs = [x for x in range(int(cx0) + 150, int(cx1) - 150, 120)
                  if solid(x, wy - nrm * 13) and solid(x - 60, wy - nrm * 13) and solid(x + 60, wy - nrm * 13)]
            for i, x in enumerate(xs):
                if i % 9 == 2: prop(L, 'bench', x, wy, z, wall=('y', wy, nrm))
                elif i % 9 == 5: prop(L, rnd.choice(['poster', 'poster2', 'board']), x, wy, z, wall=('y', wy, nrm))
                elif i % 9 == 7: prop(L, 'extbox' if nrm > 0 else 'firept', x, wy, z, wall=('y', wy, nrm))
                elif i % 9 == 0 and i: prop(L, 'ac', x, wy, z, wall=('y', wy, nrm))
            if xs and nrm > 0 and ci == 0: prop(L, 'exit', xs[-1], wy, z, wall=('y', wy, nrm))
        cxm = (cx0 + cx1) / 2; cym = (cy0 + cy1) / 2; hw = (cy1 - cy0) / 2 - 70
        if ci == 0:
            prop(L, 'wheelchair', cx0 + 0.27 * (cx1 - cx0), cy1 - 70, z, yaw=200); prop(L, 'stretcher', cx0 + 0.7 * (cx1 - cx0), cy0 + 70, z, yaw=0)
            if not clean or rnd.random() < 0.5: prop(L, 'cart', cxm, cy1 - 60, z, yaw=90)
        area = (cx1 - cx0) * (cy1 - cy0) / 1e6
        for k in range(int((3 * GRIME + 1) * area)): prop(L, rnd.choice(['paper', 'paper2']), rnd.uniform(cx0 + 40, cx1 - 40), rnd.uniform(cy0 + 40, cy1 - 40), z, yaw=rnd.uniform(0, 360))
        for k in range(int((5 * GRIME + 1) * area)): decal(L, 'dirt', rnd.uniform(cx0, cx1), rnd.uniform(cy0 + 30, cy1 - 30), z + 2, rnd.uniform(90, 170), yaw=rnd.uniform(0, 360))
        for k in range(int(3 * GRIME * GRIME * area)): decal(L, 'blood', rnd.uniform(cx0, cx1), rnd.uniform(cy0 + 30, cy1 - 30), z + 2, rnd.uniform(50, 110), yaw=rnd.uniform(0, 360))
        for k in range(int((3 * GRIME + 1) * area / 2)):
            wy, nrm = rnd.choice(((cy0, 1), (cy1, -1))); x = rnd.uniform(cx0 + 50, cx1 - 50)
            if solid(x, wy - nrm * 13): wall_decal(L, rnd.choice(['grunge', 'grunge', 'leak', 'crack', 'chip'] + (['bloodwall'] if GRIME > 0.5 else [])), x, wy, nrm, rnd.uniform(60, 280), rnd.uniform(70, 150))
    # ---------- rooms: dressed by zone ----------
    # type -> (back-wall items left->right, floor items [(kind, fx 0..1 across, fy 0..1 from corridor to back)])
    WALL = {
        'reception': ['board', 'clock', 'poster'], 'waiting': ['poster', 'clock', 'poster2', 'ac'], 'opd': ['calendar', 'clock'],
        'emergency': ['board2', 'clock', 'ac', 'speaker'], 'pharmacy': ['board', 'clock'], 'break': ['calendar', 'clock', 'board2'],
        'maternity': ['poster2', 'clock', 'poster', 'ac'], 'nicu': ['board', 'clock', 'ac'], 'suite': ['poster', 'ac'], 'lounge': ['poster2', 'clock', 'poster'],
        'recreation': ['poster', 'board', 'clock', 'poster2'], 'commonward': ['board2', 'clock', 'ac', 'poster'], 'isoward': ['board', 'clock', 'speaker'],
        'ward': ['poster', 'clock', 'ac'], 'private': ['poster2', 'clock'], 'icu': ['board', 'clock', 'ac'], 'recovery': ['clock', 'ac'],
        'ot': ['clock', 'speaker'], 'scrub': [], 'xray': ['board2', 'clock'], 'mri': ['clock', 'board'], 'control': ['calendar', 'clock'],
        'lab': ['board2', 'clock'], 'blood': ['board', 'clock'], 'cold': ['clock'], 'morgue': ['clock', 'board2'], 'autopsy': ['clock'],
        'viewing': ['poster', 'clock'], 'testing': ['board', 'clock', 'speaker'], 'observe': ['calendar', 'clock'], 'iso': ['speaker'],
        'nurse': ['board', 'clock', 'calendar'], 'doctor': ['calendar', 'clock', 'board2'], 'office': ['calendar', 'clock', 'board2'],
        'records': ['clock'], 'security': ['board', 'clock'], 'store': [], 'storage': [], 'plant': ['vent'], 'wc': [], 'sluice': []}
    FLOOR = {
        'waiting': [('plant', 0.06, 0.8), ('plant', 0.94, 0.8), ('trash', 0.5, 0.95)], 'reception': [('plant', 0.08, 0.85), ('box', 0.9, 0.9)],
        'opd': [('basket', 0.9, 0.9), ('bin', 0.92, 0.15)], 'emergency': [('wheelchair', 0.9, 0.2), ('stretcher', 0.1, 0.2), ('bin', 0.95, 0.9), ('bandage', 0.4, 0.5), ('bloodbag', 0.6, 0.45)],
        'pharmacy': [('box', 0.85, 0.85), ('box2', 0.92, 0.7)], 'break': [('basket', 0.08, 0.9), ('box2', 0.92, 0.2)],
        'maternity': [('chair2', 0.5, 0.35), ('basket', 0.95, 0.9), ('tray', 0.3, 0.5)], 'nicu': [('chair2', 0.85, 0.3), ('bin', 0.05, 0.9)],
        'suite': [('plant', 0.94, 0.2)], 'lounge': [('plant', 0.5, 0.95)], 'recreation': [('box2', 0.06, 0.15), ('book', 0.4, 0.5)],
        'commonward': [('wheelchair', 0.92, 0.25), ('chair', 0.3, 0.45), ('chair2', 0.7, 0.45), ('bin', 0.05, 0.15)],
        'isoward': [('bin', 0.05, 0.15), ('bin', 0.95, 0.15), ('tray', 0.5, 0.5)], 'ward': [('chair', 0.3, 0.45), ('chair2', 0.7, 0.45)],
        'private': [('chair', 0.7, 0.4)], 'icu': [('chair', 0.5, 0.35), ('bin', 0.95, 0.15)], 'recovery': [('chair2', 0.5, 0.35), ('bin', 0.05, 0.15)],
        'ot': [('bin', 0.95, 0.9), ('bucket', 0.05, 0.15)], 'office': [('box', 0.9, 0.85), ('basket', 0.1, 0.85)], 'doctor': [('basket', 0.1, 0.85)],
        'records': [('box', 0.1, 0.2), ('box2', 0.15, 0.25), ('box', 0.85, 0.2)], 'store': [('box', 0.2, 0.3), ('box2', 0.3, 0.25), ('box', 0.7, 0.3)],
        'storage': [('box', 0.2, 0.3), ('box2', 0.75, 0.25)], 'security': [('basket', 0.9, 0.2)], 'nurse': [('basket', 0.1, 0.2), ('box2', 0.9, 0.85)],
        'morgue': [('bucket', 0.05, 0.2), ('bin', 0.95, 0.2)], 'lab': [('box2', 0.9, 0.2)], 'blood': [('bin', 0.95, 0.2)], 'testing': [('bin', 0.9, 0.2), ('tray', 0.3, 0.4)],
        'observe': [('basket', 0.1, 0.2)], 'iso': [], 'wc': [('basket', 0.9, 0.3)], 'sluice': [('bucket', 0.5, 0.3), ('bin', 0.85, 0.3)]}
    for r in fl['rooms']:
        x0, y0, x1, y1, side, t = r['x0'], r['y0'], r['x1'], r['y1'], r['side'], r['type']
        back = y0 if side < 0 else y1; bn = -side; front = y1 if side < 0 else y0
        cxr = (x0 + x1) / 2; w = x1 - x0
        wl = WALL.get(t, ['clock'])
        for i, k in enumerate(wl):
            prop(L, k, x0 + w * (i + 1) / (len(wl) + 1), back, z, wall=('y', back, bn))
        if t not in ('wc', 'sluice', 'scrub', 'store', 'storage', 'cold', 'iso'):
            prop(L, 'radiator', x0 + 70, back, z, wall=('y', back, bn))
        for k, fx, fy in FLOOR.get(t, []):
            if clean is False or k not in ('bucket',):
                prop(L, k, x0 + 40 + fx * (w - 80), front + (back - front) * (0.08 + fy * 0.84), z, yaw=(90 if side < 0 else 270))
        for k in range(int(4 * GRIME) + (0 if clean else 1)):
            prop(L, rnd.choice(['paper', 'paper2']), rnd.uniform(x0 + 60, x1 - 60), rnd.uniform(y0 + 60, y1 - 60), z, yaw=rnd.uniform(0, 360))
        # room decals
        for k in range(int(5 * GRIME) + 1): decal(L, 'dirt', rnd.uniform(x0 + 50, x1 - 50), rnd.uniform(y0 + 50, y1 - 50), z + 2, rnd.uniform(90, 180), yaw=rnd.uniform(0, 360))
        for k in range(int(3 * GRIME) + 1): wall_decal(L, rnd.choice(['grunge', 'leak', 'crack', 'chip']), rnd.uniform(x0 + 80, x1 - 80), back, bn, rnd.uniform(60, 280), rnd.uniform(80, 160))
        if GRIME > 0.5 or t in ('morgue', 'ot', 'autopsy', 'testing'):
            for k in range(int(3 * GRIME) + (2 if t in ('morgue', 'ot', 'autopsy', 'testing', 'iso') else 0)):
                decal(L, 'blood', rnd.uniform(x0 + 60, x1 - 60), rnd.uniform(y0 + 60, y1 - 60), z + 2, rnd.uniform(50, 120), yaw=rnd.uniform(0, 360))
            if rnd.random() < GRIME * 0.7: wall_decal(L, 'bloodwall', rnd.uniform(x0 + 80, x1 - 80), back, bn, rnd.uniform(80, 200), rnd.uniform(70, 130))
        if GRIME > 0.5 and rnd.random() < 0.3: decal(L, 'glass', rnd.uniform(x0 + 80, x1 - 80), rnd.uniform(y0 + 80, y1 - 80), z + 2, 90)
    print(L, 'dressed, actors so far', n[0], flush=True)
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
