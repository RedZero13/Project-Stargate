"""Play-mode scan for stray / placeholder models (what the player actually sees). For each level: start PIE, wait for
BeginPlay, then flag on every non-StaticMeshActor actor (pickups, NPCs, enemies, props built at runtime):
  - skeletal mesh components showing a mannequin (rendered in the main pass and visible)
  - static mesh components still using an engine basic shape with no material (grey checker box)
StaticMeshActors (level dressing) are checked for basic shapes without a material. Nothing is changed.
Stops PIE even on errors.  usage: python3 scan_runtime.py [Folder/Lvl ...]"""
import sys, re, json, time
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
A = 'editor_toolset.toolsets.asset.AssetTools'; E = 'EditorToolset.EditorAppToolset'
LEVELS = sys.argv[1:] or ['City/Lvl_City', 'Clinic/Lvl_Clinic', 'Containment/Lvl_ContainmentWing', 'Wards/Lvl_Wards', 'Deep/Lvl_DeepLabs']
MANNY = re.compile(r'Mannequin|SKM_Manny|SKM_Quinn|UEFN', re.I)
SHAPE = re.compile(r'/Engine/BasicShapes/|/Engine/EngineMeshes/|/Engine/EditorMeshes/', re.I)
def props(c, names):
    r = call(O, 'get_properties', {'instance': c, 'properties': names})
    try: return json.loads(r['returnValue'])
    except Exception: return None
def find_all():
    for _ in range(5):
        try: return call(S, 'find_actors', {'name': '', 'tag': '', 'collision_channels': []})['returnValue']
        except Exception as e: print('retry', type(e).__name__, flush=True)
    return []
for lv in LEVELS:
    call(A, 'save_assets', {'asset_paths': []})
    call(S, 'load_level', {'level_path': '/Game/HollowKin/Maps/' + lv})
    name = lv.split('/')[-1]
    assert str(call(S, 'get_current_level', {})['returnValue']).endswith(name)
    call(E, 'StartPIE', {'options': {'warmupSeconds': 8}})
    hits = []
    try:
        acts = [a for a in find_all() if 'UEDPIE' in a['refPath']]
        for a in acts:
            cls = a['refPath'].split('.')[-1]
            dressing = cls.startswith('StaticMeshActor')
            r = call(AT, 'get_components', {'actor': a})
            for c in (r.get('returnValue') if isinstance(r, dict) else None) or []:
                p = props(c, ['SkeletalMeshAsset', 'bVisible', 'bHiddenInGame', 'bRenderInMainPass'])
                if p is not None and not dressing:
                    m = str(p.get('SkeletalMeshAsset') or '')
                    if MANNY.search(m) and p.get('bVisible') and not p.get('bHiddenInGame') and p.get('bRenderInMainPass', True):
                        hits.append(('MANNEQUIN', a, m)); continue
                p = props(c, ['StaticMesh', 'OverrideMaterials', 'bVisible', 'bHiddenInGame', 'bRenderInMainPass'])
                if p is not None:
                    m = str(p.get('StaticMesh') or '')
                    if SHAPE.search(m) and not p.get('OverrideMaterials') and p.get('bVisible') and not p.get('bHiddenInGame') and p.get('bRenderInMainPass', True):
                        hits.append(('SHAPE', a, m))
        for kind, a, m in hits:
            t = call(AT, 'get_actor_transform', {'actor': a}); lb = call(AT, 'get_label', {'actor': a})
            loc = ((t.get('returnValue') or {}) if isinstance(t, dict) else {}).get('location', {})
            print('  %-9s %-30s %-40s %-36s (%d,%d,%d)' % (kind, (lb.get('returnValue', '') if isinstance(lb, dict) else '')[:30], a['refPath'].split('.')[-1][:40], m.split('/')[-1][:36], loc.get('x', 0), loc.get('y', 0), loc.get('z', 0)), flush=True)
        print('==', lv, len(acts), 'actors in play,', len(hits), 'flagged', flush=True)
    finally:
        call(E, 'StopPIE', {}); time.sleep(2)
