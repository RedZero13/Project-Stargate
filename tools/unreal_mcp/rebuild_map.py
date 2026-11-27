"""Full rebuild of one stacked-floor map, in order: geometry + furniture (build_floors), lived-in dressing
(dress_floors), gameplay (place_floors), anti-clipping (declip). usage: python3 rebuild_map.py clinic|wards|deep"""
import subprocess, sys
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'
m = sys.argv[1]
LV = {'clinic': 'Clinic/Lvl_Clinic', 'wards': 'Wards/Lvl_Wards', 'deep': 'Deep/Lvl_DeepLabs'}[m]
call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []})
call(S, 'load_level', {'level_path': '/Game/HollowKin/Maps/' + LV})
cur = str(call(S, 'get_current_level', {})['returnValue'])
assert cur.endswith(LV.split('/')[1]), 'wrong level open: ' + cur
for step in (['build_floors.py', m, LV.split('/')[1]], ['dress_floors.py', m], ['place_floors.py', m], ['declip.py', m]):
    r = subprocess.run([sys.executable] + step, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    print('==', step[0], 'exit', r.returncode); print('\n'.join(out[-6:])[:1500], flush=True)
    if r.returncode: sys.exit(1)
