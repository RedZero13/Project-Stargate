"""Solid props: every furniture/dressing mesh used by build_floors.py and dress_floors.py gets convex collision
(4 hulls, so beds, racks, desks, machines and benches block Max, enemies and bullets). Pickup models and flat clutter
(papers, books, bandages, mugs, trays) stay walk-through. Edits the Fab pack meshes locally (re-run after reinstalling)."""
from ui_lib import call
import build_floors as BF, importlib.util, sys
SKIP = {'paper', 'paper2', 'book', 'bandage', 'bloodbag', 'mug', 'tray', 'sign_xray', 'sign_surgery', 'sign_nursery', 'sign_lab', 'sign_reception'}
meshes = set()
for k, v in BF.KINDS.items():
    if k in SKIP: continue
    meshes.add(('/Game/RestaurantScene/Meshes/%s.%s' % (v[2:], v[2:])) if v.startswith('R:') else BF.HH + v + '.' + v)
src = open('dress_floors.py').read()
start = src.index('PROPS = {'); end = src.index('\n}', start) + 2
ns = {'P': lambda n: BF.HH + n + '.' + n}
exec(src[start:end], ns)
for k, (mesh, wh, yo) in ns['PROPS'].items():
    if k not in SKIP: meshes.add(mesh)
ok = 0
for m in sorted(meshes):
    r = call('editor_toolset.toolsets.static_mesh.StaticMeshTools', 'generate_convex_collisions', {'mesh': {'refPath': m}, 'hull_count': 4, 'max_hull_verts': 16, 'hull_precision': 60000})
    good = isinstance(r, dict) and r.get('returnValue') is True
    ok += good
    if not good: print('FAIL', m.split('/')[-1], str(r)[:120])
print('collision generated on', ok, 'of', len(meshes), 'meshes')
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
