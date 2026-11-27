"""M_UI_Ring: radial progress ring for the HUD (UI domain, translucent). Parameters: Fill (0-1, clockwise from
the top), Color, Inner (inner radius 0-0.5). The unfilled part shows as a faint track."""
from ui_lib import call
import json
MT = 'editor_toolset.toolsets.material.MaterialTools'
O = 'editor_toolset.toolsets.object.ObjectTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
P = '/Game/HollowKin/UI/Art'
if call(A, 'exists', {'path': P + '/M_UI_Ring'}).get('returnValue'):
    call(A, 'delete', {'path': P + '/M_UI_Ring'})
m = call(MT, 'create_material', {'folder_path': P, 'asset_name': 'M_UI_Ring'})['returnValue']
call(O, 'set_properties', {'instance': m, 'values': json.dumps({'MaterialDomain': 'MD_UI', 'BlendMode': 'BLEND_Translucent'})})
def add(cls, x, y, **props):
    e = call(MT, 'add_expression', {'material_or_function': m, 'expression_class': {'refPath': '/Script/Engine.MaterialExpression' + cls}, 'x': x, 'y': y})['returnValue']
    if props: call(O, 'set_properties', {'instance': e, 'values': json.dumps(props)})
    return e
def link(a, b, inp, out=''):
    r = call(MT, 'connect_expressions', {'from_expression': a, 'from_output_name': out, 'to_expression': b, 'to_input_name': inp})
    if not isinstance(r, dict) or r.get('returnValue') is False: print('link fail', inp, str(r)[:200])
def names(e): return call(MT, 'get_expression_input_names', {'expression': e})['returnValue']
uv = add('TextureCoordinate', -1600, 0)
c = add('Subtract', -1400, 0, ConstB=0.5); link(uv, c, 'A')
r = add('Length', -1200, -100); link(c, r, names(r)[0])
mx = add('ComponentMask', -1200, 100, R=True, G=False, B=False, A=False); link(c, mx, names(mx)[0])
my = add('ComponentMask', -1200, 250, R=False, G=True, B=False, A=False); link(c, my, names(my)[0])
ny = add('Multiply', -1050, 250, ConstB=-1.0); link(my, ny, 'A')
at = add('Arctangent2', -900, 150)
an = names(at); link(mx, at, an[0]); link(ny, at, an[1])   # atan2(x, -y): 0 at top, clockwise
fr = add('Divide', -750, 150, ConstB=6.2831853); link(at, fr, 'A')
fa = add('Frac', -600, 150); link(fr, fa, '')
fill = add('ScalarParameter', -600, 350, ParameterName='Fill', DefaultValue=0.75)
stp = add('Step', -450, 250); sn = names(stp); link(fa, stp, sn[0]); link(fill, stp, sn[1])   # Fill >= angle
inner = add('ScalarParameter', -1200, -300, ParameterName='Inner', DefaultValue=0.40)
a1 = add('Subtract', -1000, -250); link(r, a1, 'A'); link(inner, a1, 'B')
k1 = add('Multiply', -850, -250, ConstB=60.0); link(a1, k1, 'A')
s1 = add('Saturate', -700, -250); link(k1, s1, '')
a2 = add('Subtract', -1000, -100, ConstA=0.495); link(r, a2, 'B')
k2 = add('Multiply', -850, -100, ConstB=60.0); link(a2, k2, 'A')
s2 = add('Saturate', -700, -100); link(k2, s2, '')
band = add('Multiply', -550, -150); link(s1, band, 'A'); link(s2, band, 'B')
lp = add('LinearInterpolate', -300, 150, ConstA=0.14, ConstB=1.0); link(stp, lp, 'Alpha')
op = add('Multiply', -150, 0); link(band, op, 'A'); link(lp, op, 'B')
colp = add('VectorParameter', -300, -350, ParameterName='Color', DefaultValue={'r': 0.85, 'g': 0.9, 'b': 0.88, 'a': 1})
call(MT, 'connect_to_output', {'expression': colp, 'output_name': '', 'material_property': 'MP_EmissiveColor'})
call(MT, 'connect_to_output', {'expression': op, 'output_name': '', 'material_property': 'MP_Opacity'})
print(call(MT, 'recompile', {'material_or_function': m}))
print(call(A, 'save_assets', {'asset_paths': [P + '/M_UI_Ring']}))
