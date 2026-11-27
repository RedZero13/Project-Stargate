"""Tactical Soldier Outfit: the FBX download had no textures, so every imported material was flat white.
Rebuilds each material as rough military fabric (olive / khaki / black, with a subtle procedural mottling)."""
from ui_lib import call
import json
MT = 'editor_toolset.toolsets.material.MaterialTools'; O = 'editor_toolset.toolsets.object.ObjectTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
F = '/Game/Fab/Tactical_Soldier_Outfit_for_MetaHuman__UE_5_6+_/'
F2 = '/Game/Fab/Tactical_Soldier_Outfit/'
PAL = {  # material -> (r,g,b linear, roughness, metallic)
    'Texture_set_1': (0.050, 0.055, 0.035, 0.85, 0), 'Texture_set_2': (0.085, 0.075, 0.050, 0.9, 0), 'Texture_set_2_001': (0.020, 0.020, 0.020, 0.7, 0),
    'Texture_set_3': (0.040, 0.048, 0.030, 0.85, 0), 'Texture_set_4': (0.110, 0.095, 0.065, 0.9, 0), 'Texture_set_5': (0.018, 0.018, 0.018, 0.6, 0),
    'Texture_set_6': (0.055, 0.060, 0.040, 0.85, 0), 'Texture_set_7': (0.060, 0.062, 0.055, 0.8, 0), 'Texture_set_7_003': (0.015, 0.015, 0.015, 0.55, 0.2),
    'Texture_set_7_004': (0.045, 0.032, 0.022, 0.75, 0), 'Sniper': (0.020, 0.020, 0.022, 0.45, 0.6),
    'Textureset_1': (0.045, 0.052, 0.033, 0.7, 0.1), 'Textureset_1_002': (0.020, 0.020, 0.020, 0.6, 0.2),
}
done = []
for folder in (F, F2):
    for name, (r, g, b, rough, metal) in PAL.items():
        path = folder + name
        if not call(A, 'exists', {'path': path}).get('returnValue'): continue
        if call(A, 'get_asset_class', {'asset_path': path}).get('returnValue') != 'Material': print('skip', path, call(A, 'get_asset_class', {'asset_path': path})); continue
        m = {'refPath': path + '.' + name}
        for e in call(MT, 'get_expressions', {'material_or_function': m})['returnValue']:
            call(MT, 'delete_expression', {'material_or_function': m, 'expression': e})
        def add(cls, x, y, **p):
            e = call(MT, 'add_expression', {'material_or_function': m, 'expression_class': {'refPath': '/Script/Engine.MaterialExpression' + cls}, 'x': x, 'y': y})['returnValue']
            if p: call(O, 'set_properties', {'instance': e, 'values': json.dumps(p)})
            return e
        def link(a, b_, inp): call(MT, 'connect_expressions', {'from_expression': a, 'from_output_name': '', 'to_expression': b_, 'to_input_name': inp})
        base = add('VectorParameter', -600, 0, ParameterName='BaseColor', DefaultValue={'r': r, 'g': g, 'b': b, 'a': 1})
        wp = add('WorldPosition', -900, 200)
        sc = add('Multiply', -750, 200, ConstB=0.02); link(wp, sc, 'A')
        nz = add('Noise', -600, 200, Scale=1.0, Levels=3, OutputMin=0.75, OutputMax=1.15)
        nin = call(MT, 'get_expression_input_names', {'expression': nz})['returnValue'][0]; link(sc, nz, nin)
        mul = add('Multiply', -350, 50); link(base, mul, 'A'); link(nz, mul, 'B')
        ro = add('Constant', -350, 250, R=rough); me = add('Constant', -350, 350, R=metal)
        call(MT, 'connect_to_output', {'expression': mul, 'output_name': '', 'material_property': 'MP_BaseColor'})
        call(MT, 'connect_to_output', {'expression': ro, 'output_name': '', 'material_property': 'MP_Roughness'})
        call(MT, 'connect_to_output', {'expression': me, 'output_name': '', 'material_property': 'MP_Metallic'})
        call(O, 'set_properties', {'instance': m, 'values': json.dumps({'BlendMode': 'BLEND_Opaque', 'TwoSided': True})})
        call(MT, 'recompile', {'material_or_function': m}); done.append(path)
print(len(done), call(A, 'save_assets', {'asset_paths': done}))
