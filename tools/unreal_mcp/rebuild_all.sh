#!/bin/bash
# Rebuild every stacked-floor map (layout v2) and re-place the Deep Labs extras that live outside FloorGP.
cd "$(dirname "$0")"
for m in ${MAPS:-clinic wards deep}; do python3 rebuild_map.py $m || exit 1; done
python3 place_cutscenes.py | tail -2
python3 - <<'PY'
import json
from ui_lib import call
S='editor_toolset.toolsets.scene.SceneTools'; O='editor_toolset.toolsets.object.ObjectTools'
b10 = next(f for f in json.load(open('floors_deep.json')) if f['label'] == 'B10')
for a in call(S, 'find_actors', {'name': '', 'tag': 'Lift_B9', 'collision_channels': []})['returnValue']:
    print('B9 lift', call(O, 'set_properties', {'instance': a, 'values': json.dumps({'NoDoors': True,
        'Target': {'x': b10['arrival'][0], 'y': b10['arrival'][1], 'z': b10['arrival'][2]}})}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
PY
echo REBUILD DONE
