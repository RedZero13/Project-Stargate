"""Clean modern-hospital materials for the above-ground clinic floors (refs: white walls, glossy white floor with grey
inlay, yellow/teal accent frames, wood/blue handrails, white drop ceiling) and the flat LED panel (emissive) used on
every floor's ceiling. Simple constant materials in /Game/HollowKin/Materials/Clean."""
from ui_lib import call
import json
MT = 'editor_toolset.toolsets.material.MaterialTools'
O = 'editor_toolset.toolsets.object.ObjectTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
P = '/Game/HollowKin/Materials/Clean'
MATS = {  # name: (rgb linear, roughness, emissive strength, metallic)
    'M_Clean_Wall':    ((0.80, 0.80, 0.78), 0.55, 0.0, 0.0),
    'M_Clean_Floor':   ((0.72, 0.72, 0.70), 0.06, 0.0, 0.0),
    'M_Clean_Inlay':   ((0.18, 0.19, 0.20), 0.10, 0.0, 0.0),
    'M_Clean_Ceiling': ((0.86, 0.86, 0.85), 0.75, 0.0, 0.0),
    'M_Clean_Yellow':  ((0.85, 0.55, 0.02), 0.40, 0.0, 0.0),
    'M_Clean_Teal':    ((0.10, 0.38, 0.40), 0.45, 0.0, 0.0),
    'M_Clean_Rail':    ((0.45, 0.24, 0.10), 0.35, 0.0, 0.0),
    'M_Clean_Door':    ((0.10, 0.09, 0.08), 0.45, 0.0, 0.0),
    'M_LED_Panel':     ((1.00, 0.98, 0.94), 0.30, 6.0, 0.0),
    'M_LED_Dim':       ((0.80, 0.85, 0.80), 0.30, 1.2, 0.0),
}
def add(m, cls, x, y, **props):
    e = call(MT, 'add_expression', {'material_or_function': m, 'expression_class': {'refPath': '/Script/Engine.MaterialExpression' + cls}, 'x': x, 'y': y})['returnValue']
    if props: call(O, 'set_properties', {'instance': e, 'values': json.dumps(props)})
    return e
for name, (rgb, rough, emis, metal) in MATS.items():
    if call(A, 'exists', {'path': P + '/' + name}).get('returnValue'):
        call(A, 'delete', {'path': P + '/' + name})
    m = call(MT, 'create_material', {'folder_path': P, 'asset_name': name})['returnValue']
    c = add(m, 'Constant3Vector', -400, 0, Constant={'r': rgb[0], 'g': rgb[1], 'b': rgb[2], 'a': 1})
    call(MT, 'connect_to_output', {'expression': c, 'output_name': '', 'material_property': 'MP_BaseColor'})
    r = add(m, 'Constant', -400, 200, R=rough)
    call(MT, 'connect_to_output', {'expression': r, 'output_name': '', 'material_property': 'MP_Roughness'})
    if emis > 0:
        e = add(m, 'Constant3Vector', -400, 350, Constant={'r': rgb[0] * emis, 'g': rgb[1] * emis, 'b': rgb[2] * emis, 'a': 1})
        call(MT, 'connect_to_output', {'expression': e, 'output_name': '', 'material_property': 'MP_EmissiveColor'})
    print(name, call(MT, 'recompile', {'material_or_function': m}))
print(call(A, 'save_assets', {'asset_paths': []}))
