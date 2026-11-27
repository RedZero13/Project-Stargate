"""RE4-style weapon/vitals ring, bottom-right of WBP_ScreenFX: inner ring = rounds in the magazine (6),
outer thin ring = health (teal / amber / red), loaded count big in the centre, reserve small, weapon name below.
Dim while idle, bright while aiming. WBP_ScreenFX.UpdateRing(Ammo, Reserve, Health, Aiming) is called from
BP_Max.TickFX."""
from menu_common import *
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
BODY_F = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
SFX = '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
RING = '/Game/HollowKin/UI/Art/M_UI_Ring.M_UI_Ring'
W = Wbp(SFX)
brush, txt, box, cslot, bslot, rule, button = mk(W)
call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget('WeaponHUD')}})
W.count['Root'] = 30
def font(size, ls=20): return {'fontObject': BODY_F, 'typefaceFontName': 'Default', 'size': size, 'letterSpacing': ls}
def color(h, a=1.0): return {'specifiedColor': col(h, a), 'colorUseRule': 'UseColor_Specified'}
vb, s = W.add('VerticalBox', 'WeaponHUD', 'Root'); cslot(s, 1, 1, -70, -60, 0, 0, alx=1.0, aly=1.0); setp(s, {'bAutoSize': True})
sz, ss = W.add('SizeBox', 'RingSize', 'WeaponHUD')
setp(sz, {'widthOverride': 190, 'heightOverride': 190, 'bOverride_WidthOverride': True, 'bOverride_HeightOverride': True})
ov, _ = W.add('Overlay', 'RingOv', 'RingSize')
def ring(name, pad):
    im, s = W.add('Image', name, 'RingOv')
    setp(im, {'brush': {'drawAs': 'Image', 'imageType': 'FullColor', 'resourceObject': RING, 'imageSize': {'x': 190, 'y': 190},
              'tintColor': {'specifiedColor': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 'colorUseRule': 'UseColor_Specified'}}})
    setp(s, {'horizontalAlignment': 'HAlign_Fill', 'verticalAlignment': 'VAlign_Fill', 'padding': {'left': pad, 'top': pad, 'right': pad, 'bottom': pad}})
ring('HPRing', 0)
ring('AmmoRing', 20)
cv, cs = W.add('VerticalBox', 'RingText', 'RingOv'); setp(cs, {'horizontalAlignment': 'HAlign_Center', 'verticalAlignment': 'VAlign_Center'})
t, ts = W.add('TextBlock', 'AmmoNum', 'RingText')
setp(t, {'text': '6', 'justification': 'Center', 'font': font(44, 0), 'colorAndOpacity': color('ece4d2')}); bslot(ts, h='HAlign_Center')
t, ts = W.add('TextBlock', 'AmmoRes', 'RingText')
setp(t, {'text': '/ 12', 'justification': 'Center', 'font': font(20, 40), 'colorAndOpacity': color('ece4d2', 0.7)}); bslot(ts, h='HAlign_Center')
t, ts = W.add('TextBlock', 'WeaponName', 'WeaponHUD')
setp(t, {'text': 'M1911  //  SIDEARM', 'justification': 'Center', 'font': font(16, 300), 'colorAndOpacity': color(TEAL, 0.9)}); bslot(ts, pad=(0, 8, 0, 0), h='HAlign_Center')
for n in ('WeaponHUD', 'HPRing', 'AmmoRing', 'AmmoNum', 'AmmoRes'):
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
G = lambda n: '(Variables|WBP_ScreenFX|Get%s)' % n
call(BT, 'add_function_graph', {'blueprint': {'refPath': SFX}, 'graph_name': 'UpdateRing'})
for p, t in [('Ammo', 'int'), ('Reserve', 'int'), ('Health', 'float'), ('Aiming', 'bool')]:
    call(BT, 'add_function_param', {'graph': {'refPath': SFX + ':UpdateHUD'}, 'param_name': p, 'param_type': t, 'input_param': True})
dsl = '''(fn UpdateRing (Ammo Reserve Health Aiming)
  (CallFunction|InitRingMats)
  (bind am (Variables|Default|GetAmmoMID))
  (bind hm (Variables|Default|GetHpMID))
  (CallFunction|MidScalar :M am :P "Fill" :V (/ (Math|Conversions|ToFloat(Integer) Ammo) 6.0))
  (CallFunction|MidScalar :M am :P "Inner" :V 0.40)
  (CallFunction|MidColor :M am :P "Color" :C (select (<= Ammo 1) (Math|Color|MakeColor 0.9 0.25 0.22 1.0) (Math|Color|MakeColor 0.86 0.9 0.88 1.0)))
  (CallFunction|MidScalar :M hm :P "Fill" :V (/ Health 100.0))
  (CallFunction|MidScalar :M hm :P "Inner" :V 0.465)
  (CallFunction|MidColor :M hm :P "Color" :C (select (< Health 30.0) (Math|Color|MakeColor 0.85 0.12 0.14 1.0) (select (< Health 60.0) (Math|Color|MakeColor 0.95 0.62 0.2 1.0) (Math|Color|MakeColor 0.3 0.75 0.68 1.0))))
  (Widget|SetText(Text) %(an)s (Utilities|Text|ToText(Integer) Ammo))
  (Widget|SetText(Text) %(rs)s (Utilities|Text|ToText(String) (Utilities|String|BuildString(Integer) :Prefix "/ " :InInt Reserve :Suffix "")))
  (Widget|SetRenderOpacity %(hud)s (select Aiming 1.0 (select (< Health 60.0) 0.85 0.5))))''' % {
    'ar': G('AmmoRing'), 'hr': G('HPRing'), 'an': G('AmmoNum'), 'rs': G('AmmoRes'), 'hud': G('WeaponHUD')}
print('UpdateRing', call(BT, 'write_graph_dsl', {'graph': {'refPath': SFX + ':UpdateHUD'}, 'code': dsl}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': SFX}, 'warnings_as_errors': True}))
