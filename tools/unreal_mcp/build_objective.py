"""Persistent objective panel, top-left of WBP_ScreenFX ("OBJECTIVE" + one line), plus
WBP_ScreenFX.SetObjective(Msg) and BP_Max.SetObjectiveNote(Msg) (callable from any Blueprint).
Also stops the message box from collapsing into a narrow column (fixed wrap width instead of auto-wrap)."""
from menu_common import *
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
F_BODY = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
SFX = '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
W = Wbp(SFX)
brush, txt, box, cslot, bslot, rule, button = mk(W)
call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget('ObjBox')}})
W.count['Root'] = 21
b, s = box('ObjBox', 'Root', '050607', 0.55, padding={'left': 22, 'top': 12, 'right': 26, 'bottom': 14})
cslot(s, 0.0, 0.0, 48, 40, 0, 0)
setp(s, {'bAutoSize': True})
setp(b, {'visibility': 'Collapsed'})
vb, _ = W.add('VerticalBox', 'ObjVB', 'ObjBox')
t, _ = W.add('TextBlock', 'ObjCap', 'ObjVB')
setp(t, {'text': 'OBJECTIVE', 'colorAndOpacity': {'specifiedColor': col(TEAL), 'colorUseRule': 'UseColor_Specified'},
         'font': {'fontObject': F_BODY, 'typefaceFontName': 'Default', 'size': 18, 'letterSpacing': 250}})
t, _ = W.add('TextBlock', 'ObjText', 'ObjVB')
setp(t, {'text': 'Objective', 'wrapTextAt': 620, 'colorAndOpacity': {'specifiedColor': col('ece4d2'), 'colorUseRule': 'UseColor_Specified'},
         'shadowOffset': {'x': 1, 'y': 1}, 'shadowColorAndOpacity': {'r': 0, 'g': 0, 'b': 0, 'a': 0.9},
         'font': {'fontObject': F_BODY, 'typefaceFontName': 'Default', 'size': 24, 'letterSpacing': 20}})
for n in ('ObjBox', 'ObjText'):
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
# message box: fixed wrap width (auto-wrap inside an auto-sized slot sometimes wrapped to a narrow column)
setp(W.widget('MsgText'), {'autoWrapText': False, 'wrapTextAt': 1300})
print('compile', call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))

def fn(bp, name, params, dsl):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for p in params:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': p, 'param_type': 'string', 'input_param': True})
    print(name, call(BT, 'write_graph_dsl', {'graph': {'refPath': bp + ':' + name}, 'code': dsl}))

fn(SFX, 'SetObjective', ['Msg'], '''(fn SetObjective (Msg)
  (Widget|SetText(Text) (Variables|WBP_ScreenFX|GetObjText) (Utilities|Text|ToText(String) Msg))
  (Widget|SetVisibility (Variables|WBP_ScreenFX|GetObjBox) "HitTestInvisible"))''')
fn(MAX, 'SetObjectiveNote', ['Msg'], '''(fn SetObjectiveNote (Msg)
  (Utilities|IsValid (Variables|Default|GetScreenFXRef)
    (:"Is Valid"
      (Class|WBPScreenFX|SetObjective (Variables|Default|GetScreenFXRef) Msg))))''')
for bp in (SFX, MAX):
    print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False}))
