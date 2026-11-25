"""Containment Wing: the south rooms (C5 Cell Block A, C7 Isolation) were too dark to read even with the
flashlight. Adds dim fixtures over the cells and corridors (tag SliceLightsExtra) and raises L_C7. Re-runnable."""
from ui_lib import call
import json
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
LIGHTS = [  # label, x, y, z, candela, radius, colour
    ('LX_C5_Cell1', 3870, -1380, 250, 30, 520, (1.0, 0.82, 0.6)), ('LX_C5_Cell3', 4360, -1380, 250, 22, 520, (1.0, 0.82, 0.6)),
    ('LX_C5_Cell5', 4850, -1380, 250, 30, 520, (1.0, 0.82, 0.6)), ('LX_C5_Hall', 3800, -900, 320, 55, 800, (0.9, 0.85, 0.75)),
    ('LX_C7_Hall', 5900, -1000, 280, 55, 750, (0.6, 0.72, 0.95)), ('LX_C7_Far', 6300, -900, 280, 45, 650, (0.6, 0.72, 0.95)),
    ('LX_C7_Booth', 5820, -1400, 240, 25, 420, (1.0, 0.55, 0.4)),
]
for old in call(S, 'find_actors', {'name': '', 'tag': 'SliceLightsExtra', 'collision_channels': []})['returnValue']:
    call(S, 'remove_from_scene', {'actor': old})
for label, x, y, z, cd, rad, c in LIGHTS:
    a = call(S, 'add_to_scene_from_class', {'actor_type': {'refPath': '/Script/Engine.PointLight'}, 'name': label, 'xform': {'location': {'x': x, 'y': y, 'z': z}}})['returnValue']
    comp = call(AT, 'get_components', {'actor': a, 'component_type': {'refPath': '/Script/Engine.PointLightComponent'}})['returnValue'][0]
    call(O, 'set_properties', {'instance': comp, 'values': json.dumps({'Mobility': 'Movable', 'IntensityUnits': 'Candelas', 'Intensity': cd, 'AttenuationRadius': rad,
          'LightColor': {'r': int(c[0] * 255), 'g': int(c[1] * 255), 'b': int(c[2] * 255), 'a': 255}, 'CastShadows': False})})
    call(AT, 'add_tag', {'actor': a, 'tag': 'SliceLightsExtra'}); call(AT, 'set_label', {'actor': a, 'label': label})
    call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Slice/Lighting'})
    print('light', label)
for a in call(S, 'find_actors', {'name': 'L_C7', 'tag': '', 'collision_channels': []})['returnValue']:
    if call(AT, 'get_label', {'actor': a})['returnValue'] != 'L_C7': continue
    comps = call(AT, 'get_components', {'actor': a, 'component_type': {'refPath': '/Script/Engine.PointLightComponent'}})['returnValue']
    if comps: print('L_C7', call(O, 'set_properties', {'instance': comps[0], 'values': json.dumps({'Intensity': 90})}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
