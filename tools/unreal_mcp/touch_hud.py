"""iPad touch controls: WBP_TouchHUD, a column of large buttons on the right (FIRE, AIM, USE, RELOAD, TORCH, BAG,
MAP, PAUSE). The move / look sticks are Unreal's DefaultVirtualJoysticks (Config/IOS/IOSInput.ini). Max adds the HUD
once per level, only on iOS (BP_Max.AddTouchHUD, called from SetObjectiveNote's level-start branch)."""
from menu_common import *
import menu_logic as ml
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
P = '/Game/HollowKin/UI/HUD/WBP_TouchHUD'; WT = P + '.WBP_TouchHUD'
MAXC = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
if call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'delete', {'path': P})
print(call(U, 'CreateWidgetBlueprint', {'path': '/Game/HollowKin/UI/HUD', 'name': 'WBP_TouchHUD'}) if False else '')
# start from the loading card (a canvas + fonts), strip it
call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Credits', 'new_path': P})
W = Wbp(WT)
for n in ('Cap', 'Scroll', 'Body', 'BtnBack', 'Hint', 'Blur', 'Shade'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
call(BT, 'remove_function_graph', {'blueprint': W.ref, 'graph_name': 'OnKeyDown'})
w(WT + ':CloseCredits', '(fn CloseCredits ()\n  (Widget|RemoveFromParent self))')
brush, txt, box, cslot, bslot, rule, button = mk(W)
W.count = {'Root': 0}
BTN = [('TFire', 'FIRE', '(Class|BPMax|FirePistol :self m)'),
       ('TAim', 'AIM', '(Class|BPMax|SetAiming :self m :bAiming (not (Class|BPMax|GetAiming :self m)))'),
       ('TUse', 'USE', '(Class|BPMax|Interact :self m)'),
       ('TReload', 'RELOAD', '(Class|BPMax|ReloadPistol :self m)'),
       ('TTorch', 'TORCH', '(Class|BPMax|ToggleFlashlight :self m)'),
       ('TBag', 'BAG', '(Class|BPMax|OpenCaseItems :self m)'),
       ('TMap', 'MAP', '(Class|BPMax|OpenMap :self m)'),
       ('TPause', 'PAUSE', '(Class|BPMax|OpenPause :self m)')]
vb, s = W.add('VerticalBox', 'Col', 'Root'); cslot(s, 1, (0, 1), -260, 140, 220, 140, alx=0.0)
for name, label, act in BTN:
    b, bs = W.add('Button', name, 'Col')
    setp(b, {'widgetStyle': {'normal': {'drawAs': 'Box', 'tintColor': {'specifiedColor': col(PANEL, 0.55), 'colorUseRule': 'UseColor_Specified'}},
                             'hovered': {'drawAs': 'Box', 'tintColor': {'specifiedColor': col(TEAL, 0.45), 'colorUseRule': 'UseColor_Specified'}},
                             'pressed': {'drawAs': 'Box', 'tintColor': {'specifiedColor': col(TEAL, 0.7), 'colorUseRule': 'UseColor_Specified'}}}})
    bslot(bs, pad=(0, 6, 0, 6), fill=1.0)
    t, ts = W.add('TextBlock', name + 'L', name)
    setp(t, {'text': label, 'justification': 'Center', 'font': {'size': 26, 'typefaceFontName': 'Bold', 'letterSpacing': 200},
             'colorAndOpacity': {'specifiedColor': col(WHITE), 'colorUseRule': 'UseColor_Specified'}})
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(name)}, 'bIsVariable': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
for i, (name, label, act) in enumerate(BTN):
    call(BT, 'add_function_graph', {'blueprint': W.ref, 'graph_name': 'Do' + name})
    w(WT + ':Do' + name, '''(fn Do%s ()
  (bind m %s
    (:then %s)
    (:CastFailed)))''' % (name, MAXC, act))
    ml.wire(WT, name, 'Do' + name, 200 * i)
ml.connect_clicks(WT, dict((n, 'Do' + n) for n, _, _ in BTN))
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
call(BT, 'add_function_graph', {'blueprint': {'refPath': MAX}, 'graph_name': 'AddTouchHUD'})
w(MAX + ':AddTouchHUD', '''(fn AddTouchHUD ()
  (if (Utilities|String|EqualExactly(String) (Game|GetPlatformName) "IOS")
    (UserInterface|Viewport|AddToViewport (UserInterface|CreateWidget "%s_C" (Game|GetPlayerController 0)) 5)))''' % WT)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
