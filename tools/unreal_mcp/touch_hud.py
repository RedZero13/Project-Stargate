"""iPad touch controls (redesigned 2026-11-28): WBP_TouchHUD.
- Move / look: the virtual sticks of TI_HollowKin (touch_sticks.py), bottom-left and bottom-right corners.
- Action buttons: round, semi-transparent, teal ring, grouped above the right stick for the right thumb:
  FIRE (large), AIM, RELOAD, USE.
- Small pills along the top right: TORCH, BAG, MAP, PAUSE.
Buttons fire on touch-down and never take focus. BP_Max.AddTouchHUD (tutorials.py) adds this widget and activates the
sticks, only on iOS. Re-runnable (deletes and rebuilds the widget)."""
from menu_common import *
import menu_logic as ml
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
if call('EditorToolset.EditorAppToolset', 'IsPIERunning', {}).get('returnValue'): raise SystemExit('stop PIE first')
P = '/Game/HollowKin/UI/HUD/WBP_TouchHUD'; WT = P + '.WBP_TouchHUD'
MAXC = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'
F_SEMI = {'refPath': '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'}
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
if call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'delete', {'path': P})
call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Credits', 'new_path': P})   # a canvas to start from
W = Wbp(WT)
for n in ('Cap', 'Scroll', 'Body', 'BtnBack', 'Hint', 'Blur', 'Shade'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
call(BT, 'remove_function_graph', {'blueprint': W.ref, 'graph_name': 'OnKeyDown'})
brush, txt, box, cslot, bslot, rule, button = mk(W)
W.count = {'Root': 0}
def style(fill_a, ring_a, round_=True):
    def b(c_fill, a_fill):
        return {'drawAs': 'RoundedBox', 'imageType': 'FullColor', 'resourceName': 'None',
                'tintColor': {'specifiedColor': col(c_fill, a_fill), 'colorUseRule': 'UseColor_Specified'},
                'outlineSettings': {'width': 2.5, 'cornerRadii': {'x': 12, 'y': 12, 'z': 12, 'w': 12},
                                    'color': {'specifiedColor': col(TEAL, ring_a), 'colorUseRule': 'UseColor_Specified'},
                                    'roundingType': 'HalfHeightRadius' if round_ else 'FixedRadius', 'bUseBrushTransparency': True}}
    return {'normal': b(PANEL, fill_a), 'hovered': b(PANEL, fill_a), 'pressed': b(TEAL, 0.55), 'disabled': b(PANEL, fill_a),
            'normalPadding': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}, 'pressedPadding': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}}
# name, label, action, anchor (x,y), offset of the button centre from the anchor, size (w,h), round, font size
BTN = [('TFire', 'FIRE', '(Class|BPMax|FirePistol :self m)', (1, 1), (-250, -560), (170, 170), True, 26),
       ('TAim', 'AIM', '(Class|BPMax|SetAiming :self m :bAiming (not (Class|BPMax|GetAiming :self m)))', (1, 1), (-450, -500), (125, 125), True, 21),
       ('TReload', 'RELOAD', '(Class|BPMax|ReloadPistol :self m)', (1, 1), (-110, -720), (105, 105), True, 16),
       ('TUse', 'USE', '(Class|BPMax|Interact :self m)', (1, 1), (-560, -310), (125, 125), True, 22),
       ('TTorch', 'TORCH', '(Class|BPMax|ToggleFlashlight :self m)', (1, 0), (-470, 60), (120, 56), False, 17),
       ('TBag', 'BAG', '(Class|BPMax|OpenCaseItems :self m)', (1, 0), (-340, 60), (110, 56), False, 17),
       ('TMap', 'MAP', '(Class|BPMax|OpenMap :self m)', (1, 0), (-215, 60), (110, 56), False, 17),
       ('TPause', 'II', '(Class|BPMax|OpenPause :self m)', (1, 0), (-100, 60), (80, 56), False, 20)]
for name, label, act, anc, (cx, cy), (bw, bh), rnd, fs in BTN:
    b, s = W.add('Button', name, 'Root')
    cslot(s, anc[0], anc[1], cx, cy, bw, bh, alx=0.5, aly=0.5)
    setp(b, {'widgetStyle': style(0.42 if rnd else 0.55, 0.85 if rnd else 0.6, rnd), 'TouchMethod': 'Down', 'ClickMethod': 'MouseDown', 'IsFocusable': False})
    t, ts = W.add('TextBlock', name + 'L', name)
    setp(t, {'text': label, 'justification': 'Center', 'font': {'fontObject': F_SEMI, 'typefaceFontName': 'Default', 'size': fs, 'letterSpacing': 160},
             'colorAndOpacity': {'specifiedColor': col(WHITE, 0.95), 'colorUseRule': 'UseColor_Specified'}})
    setp(ts, {'horizontalAlignment': 'HAlign_Center', 'verticalAlignment': 'VAlign_Center'})
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(name)}, 'bIsVariable': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
w(WT + ':CloseCredits', '(fn CloseCredits ()\n  (Widget|RemoveFromParent self))')
for i, (name, label, act, *_r) in enumerate(BTN):
    call(BT, 'add_function_graph', {'blueprint': W.ref, 'graph_name': 'Do' + name})
    w(WT + ':Do' + name, '''(fn Do%s ()
  (bind m %s
    (:then %s)
    (:CastFailed)))''' % (name, MAXC, act))
    ml.wire(WT, name, 'Do' + name, 200 * i)
ml.connect_clicks(WT, dict((n, 'Do' + n) for n, *_r in BTN))
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
print(call(A, 'save_assets', {'asset_paths': [P]}))
