"""B9 (the original Deep Labs) now leads further down: Emilia and the ending move to B15. The old chamber (D9) gets
the lift to B10; it needs the generator in the generator hall (D7) restarted. A second nav volume covers B10-B15."""
from ui_lib import call
import json
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
F = '/Game/HollowKin/Blueprints/Floors/'
floors = json.load(open('floors_deep.json'))
for name in ('Emilia', 'D9_EndingTrigger', 'B9_Lift', 'B9_Generator', 'H_D9', 'NavFloors'):
    for a in call(S, 'find_actors', {'name': name, 'tag': '', 'collision_channels': []})['returnValue']:
        if name == 'Emilia' and 'B15' in a['refPath']: continue
        lbl = call(AT, 'get_label', {'actor': a}).get('returnValue', '')
        if name == 'Emilia' and lbl.startswith('B15'): continue
        call(S, 'remove_from_scene', {'actor': a}); print('removed', lbl)
def put(cls, label, x, y, z, props=None, tags=()):
    a = call(S, 'add_to_scene_from_asset', {'asset_path': cls, 'name': label, 'xform': {'location': {'x': x, 'y': y, 'z': z}}})['returnValue']
    if props: print(label, call(O, 'set_properties', {'instance': a, 'values': json.dumps(props)}))
    for t in ('DeepGP',) + tuple(tags): call(AT, 'add_tag', {'actor': a, 'tag': t})
    call(AT, 'set_label', {'actor': a, 'label': label}); call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Deep/Gameplay'})
    return a
b10 = floors[0]
put(F + 'BP_FloorLift.BP_FloorLift', 'B9_Lift', 10850, 0, 100, props={'Label': 'B9', 'Gate': 3, 'NextLabel': b10['label'], 'NextName': b10['name'],
    'Target': {'x': b10['arrival'][0], 'y': b10['arrival'][1], 'z': b10['arrival'][2]}}, tags=('Lift_B9',))
put(F + 'BP_FloorGenerator.BP_FloorGenerator', 'B9_Generator', 8600, -1150, 2, props={'Label': 'B9'})
put('/Game/HollowKin/Blueprints/Interactables/BP_Hint.BP_Hint', 'H_D9', 10200, 0, 100,
    props={'Message': "L-03 is empty. A service lift goes further down, six more floors. It is dead: the old generator in the hall behind you powers it."})
nav = call(S, 'add_to_scene_from_class', {'actor_type': {'refPath': '/Script/NavigationSystem.NavMeshBoundsVolume'}, 'name': 'NavFloors',
    'xform': {'location': {'x': 2850, 'y': 0, 'z': -5800}, 'scale': {'x': 30, 'y': 11, 'z': 41}}})['returnValue']
call(AT, 'set_label', {'actor': nav, 'label': 'NavFloors'})
print(call(AT, 'get_actor_bounds', {'actor': nav}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
