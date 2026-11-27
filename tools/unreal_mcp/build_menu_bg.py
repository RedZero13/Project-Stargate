"""M_UI_MenuSmoke: animated dark-teal smoke for the title/main-menu background (UI domain, procedural noise,
no textures). Two noise layers drifting with Time, darkened toward the edges (vignette)."""
from ui_lib import call
import json
MT = 'editor_toolset.toolsets.material.MaterialTools'
O = 'editor_toolset.toolsets.object.ObjectTools'
P = '/Game/HollowKin/UI/Art'
m = call(MT, 'create_material', {'folder_path': P, 'asset_name': 'M_UI_MenuSmoke'})['returnValue']
print(m)
call(O, 'set_properties', {'instance': m, 'values': json.dumps({'MaterialDomain': 'MD_UI', 'BlendMode': 'BLEND_Opaque'})})
def add(cls, x, y, **props):
    e = call(MT, 'add_expression', {'material_or_function': m, 'expression_class': {'refPath': '/Script/Engine.MaterialExpression' + cls}, 'x': x, 'y': y})['returnValue']
    if props:
        call(O, 'set_properties', {'instance': e, 'values': json.dumps(props)})
    return e
def link(a, b, inp, out=''):
    r = call(MT, 'connect_expressions', {'from_expression': a, 'from_output_name': out, 'to_expression': b, 'to_input_name': inp})
    if not isinstance(r, dict) or r.get('returnValue') is False: print('link fail', inp, str(r)[:150])
uv = add('TextureCoordinate', -1400, 0)
tm = add('Time', -1400, 200)
s1 = add('Multiply', -1200, 0, ConstB=2.2); link(uv, s1, 'A')
t1 = add('Multiply', -1200, 200, ConstB=0.045); link(tm, t1, 'A')
a1 = add('AppendVector', -1000, 0); link(s1, a1, 'A'); link(t1, a1, 'B')
n1 = add('Noise', -800, 0, Scale=1.0, Levels=5, OutputMin=0.0, OutputMax=1.0, bTurbulence=True, NoiseFunction='NOISEFUNCTION_GradientALU')
link(a1, n1, 'World Position')
s2 = add('Multiply', -1200, 400, ConstB=6.0); link(uv, s2, 'A')
t2 = add('Multiply', -1200, 600, ConstB=0.11); link(tm, t2, 'A')
a2 = add('AppendVector', -1000, 400); link(s2, a2, 'A'); link(t2, a2, 'B')
n2 = add('Noise', -800, 400, Scale=1.0, Levels=3, OutputMin=0.0, OutputMax=1.0, bTurbulence=False, NoiseFunction='NOISEFUNCTION_GradientALU')
link(a2, n2, 'World Position')
mix = add('Multiply', -600, 200); link(n1, mix, 'A'); link(n2, mix, 'B')
pw = add('Power', -450, 200, ConstExponent=1.6); link(mix, pw, 'Base')
# vignette
c = add('Constant2Vector', -1000, 800, R=0.5, G=0.5)
dist = add('Distance', -800, 800); link(uv, dist, 'A'); link(c, dist, 'B')
vm = add('Multiply', -650, 800, ConstB=1.55); link(dist, vm, 'A')
om = add('OneMinus', -500, 800); link(vm, om, '')
sat = add('Saturate', -380, 800); link(om, sat, '')
v = add('Multiply', -300, 400); link(pw, v, 'A'); link(sat, v, 'B')
col = add('Constant3Vector', -300, 600, Constant={'r': 0.10, 'g': 0.42, 'b': 0.40, 'a': 1})
fin = add('Multiply', -120, 400); link(v, fin, 'A'); link(col, fin, 'B')
print(call(MT, 'connect_to_output', {'expression': fin, 'output_name': '', 'material_property': 'MP_EmissiveColor'}))
print(call(MT, 'recompile', {'material_or_function': m}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': [P + '/M_UI_MenuSmoke']}))
