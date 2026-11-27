"""Blood decals (Fab 'Blood Decals' pack: splatter / trail / pool-with-footprints) laid on the floor of the CURRENT
level around fallen soldiers, enemy posts and a few doorways. Re-runnable: removes its own decals (tag Blood) first.
usage: python3 place_blood.py   (run once per level: wing, city, deep labs)"""
from ui_lib import call
import json, random, math
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
M = '/Game/BloodDecals/Materials/'
MAT = {'pool': M + 'MI_Blood_PoolFootprints.MI_Blood_PoolFootprints', 'trail': M + 'MI_Blood_Trail.MI_Blood_Trail',
       'splat': M + 'MI_Blood_Splatter.MI_Blood_Splatter'}
random.seed(13)
lvl = str(call(S, 'get_current_level', {})['returnValue']); print('level', lvl)
for old in call(S, 'find_actors', {'name': '', 'tag': 'Blood', 'collision_channels': []})['returnValue']:
    call(S, 'remove_from_scene', {'actor': old})
def loc(a):
    t = call(AT, 'get_actor_transform', {'actor': a})['returnValue']; l = t['location']; return l['x'], l['y'], l['z']
def floor_z(x, y, z):
    try:
        d = call(S, 'trace_world', {'start': {'x': x, 'y': y, 'z': z + 50}, 'end': {'x': x, 'y': y, 'z': z - 400}})['returnValue']
        if d is not None: return z + 50 - d
    except Exception: pass
    return z - 90   # pawn origin sits ~90 above the floor
n = 0
doors = 0
def decal(kind, x, y, z, size, yaw):
    global n; n += 1
    a = call(S, 'add_to_scene_from_class', {'actor_type': {'refPath': '/Script/Engine.DecalActor'}, 'name': 'Blood_%d' % n,
        'xform': {'location': {'x': x, 'y': y, 'z': z + 5}, 'rotation': {'pitch': -90, 'yaw': yaw, 'roll': 0}}})['returnValue']
    c = call(AT, 'get_components', {'actor': a, 'component_type': {'refPath': '/Script/Engine.DecalComponent'}})['returnValue'][0]
    call(O, 'set_properties', {'instance': c, 'values': json.dumps({'DecalMaterial': MAT[kind],
        'DecalSize': {'x': 40, 'y': size, 'z': size}, 'SortOrder': n})})
    call(AT, 'add_tag', {'actor': a, 'tag': 'Blood'}); call(AT, 'set_label', {'actor': a, 'label': 'Blood_%s_%d' % (kind, n)})
    call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Dressing/Blood'})
seen = set(); spots = []
for key, role in (('Soldier', 'body'), ('DS_', 'body'), ('DeadBody', 'body'), ('Corpse', 'body'), ('Orderly', 'body'), ('Hollow', 'enemy'),
                  ('Brute', 'enemy'), ('Guard', 'enemy'), ('Door', 'door')):
    for a in call(S, 'find_actors', {'name': key, 'tag': '', 'collision_channels': []})['returnValue']:
        if a['refPath'] in seen or 'Blood' in a['refPath']: continue
        seen.add(a['refPath']); spots.append((role, a))
for role, a in spots:
    try: x, y, z = loc(a)
    except Exception: continue
    fz = floor_z(x, y, z)
    if role == 'body':
        decal('pool', x, y, fz, random.uniform(70, 95), random.uniform(0, 360))
        ang = random.uniform(0, 2 * math.pi); d = random.uniform(140, 200)
        decal('trail', x + math.cos(ang) * d, y + math.sin(ang) * d, fz, 110, math.degrees(ang))
    elif role == 'enemy':
        decal('splat', x + random.uniform(-120, 120), y + random.uniform(-120, 120), fz, random.uniform(60, 90), random.uniform(0, 360))
    elif role == 'door' and doors < 20 and random.random() < 0.15:
        doors += 1
        decal('trail', x + random.uniform(-60, 60), y + random.uniform(-60, 60), fz, 90, random.uniform(0, 360))
print('placed', n, 'decals from', len(spots), 'spots')
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
