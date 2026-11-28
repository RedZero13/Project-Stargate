"""Finds placeholder / stray models in every game level: visible mannequins (Manny/Quinn), engine basic shapes,
template meshes and Game Animation Sample actors. Lists label, class, mesh and position (nothing is changed).
usage: python3 scan_placeholders.py [Folder/Lvl ...]"""
import sys, re, json
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
LEVELS = sys.argv[1:] or ['City/Lvl_City', 'Clinic/Lvl_Clinic', 'Containment/Lvl_ContainmentWing', 'Wards/Lvl_Wards', 'Deep/Lvl_DeepLabs', 'Lvl_MainMenu']
SUS = re.compile(r'Mannequin|SKM_Manny|SKM_Quinn|UEFN|BasicShapes|EngineMeshes|/Engine/.*(Cube|Sphere|Cylinder|Plane|Cone)|Template|SM_Cube|EditorCube|Sandbox|TestCube', re.I)
for lv in LEVELS:
    call(A, 'save_assets', {'asset_paths': []})
    call(S, 'load_level', {'level_path': '/Game/HollowKin/Maps/' + lv})
    assert str(call(S, 'get_current_level', {})['returnValue']).endswith(lv.split('/')[-1])
    acts = []
    for attempt in range(5):
        try: acts = call(S, 'find_actors', {'name': '', 'tag': '', 'collision_channels': []})['returnValue']; break
        except Exception as e: print('retry', lv, type(e).__name__, flush=True)
    hits = 0
    for a in acts:
        cls = a['refPath'].split('.')[-1]
        comps = call(AT, 'get_components', {'actor': a}).get('returnValue') or []
        for c in comps:
            cn = c['refPath'].split('.')[-1]
            p = None
            for prop in ('StaticMesh', 'SkeletalMeshAsset'):   # asking for a property the class lacks fails the whole call
                pr = call(O, 'get_properties', {'instance': c, 'properties': [prop, 'bVisible', 'bHiddenInGame']})
                try: p = json.loads(pr['returnValue']); break
                except Exception: pass
            if p is None: continue
            mesh = str(p.get('StaticMesh') or p.get('SkeletalMeshAsset') or '')
            if (mesh and SUS.search(mesh)) or SUS.search(cls):
                loc = call(AT, 'get_actor_transform', {'actor': a})['returnValue']['location']
                print('  %-28s %-34s %-60s vis=%s hiddenInGame=%s at (%d,%d,%d)' % (call(AT, 'get_label', {'actor': a}).get('returnValue', '')[:28], cls[:34], mesh.split('/')[-1][:60] or '-', p.get('bVisible'), p.get('bHiddenInGame'), loc['x'], loc['y'], loc['z']), flush=True)
                hits += 1
    print('==', lv, len(acts), 'actors,', hits, 'suspicious', flush=True)
