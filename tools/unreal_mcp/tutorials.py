"""Contextual tutorial prompts (2026-11-28), replacing the wall of key binds at the start of the prologue.
WBP_Tutorial: a card on the left, mid-screen: TUTORIAL caption, key cap(s), action name, one-line hint. It removes
itself after 6 s. BP_Max.TutorialTick (every 1 s, desktop / controller builds only) shows the first prompt whose moment
has come, at most one every 7 s, each once per play session (seen ids live in BP_HKGameInstance.TutSeen):
  move, look, run, flashlight (start) - interact (near a door / breaker / counter / choice) - throw (has a bottle)
  - aim, fire, reload, swap shoulder (has the pistol) - punch (a Hollow within 18 m) - backpack, workbench (items)
  - map (found a floor plan) - journal (first journal entry).
iOS (touch-first): no prompts at all; the touch HUD is added instead (AddTouchHUD is owned by this script).
BP_Max.Notify also turns 'E / (Y)' hints into 'USE' on iOS. Refuses to run during PIE."""
from menu_common import *
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
if call('EditorToolset.EditorAppToolset', 'IsPIERunning', {}).get('returnValue'): raise SystemExit('stop PIE first')
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
GI = '/Game/HollowKin/Blueprints/Systems/BP_HKGameInstance.BP_HKGameInstance'
P = '/Game/HollowKin/UI/HUD/WBP_Tutorial'; WT = P + '.WBP_Tutorial'
GIC = '(Utilities|Casting|CastToBP_HKGameInstance (Game|GetGameInstance))'
F_SEMI = {'refPath': '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'}
F_MED = {'refPath': '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-Medium_Font.BarlowSemiCondensed-Medium_Font'}
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(bp, name, dsl, params=(), outs=()):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt in params: call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': True})
    for pn, pt in outs: call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': False})
    w(bp + ':' + name, dsl)
def var(bp, n, t):
    if n not in (call(BT, 'list_variables', {'blueprint': {'refPath': bp}}).get('returnValue') or []):
        call(BT, 'add_variable', {'blueprint': {'refPath': bp}, 'name': n, 'type_name': t})
# ---------------- widget ----------------
if call(A, 'exists', {'path': P}).get('returnValue'): call(A, 'delete', {'path': P})
call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Credits', 'new_path': P})
W = Wbp(WT)
for n in ('Cap', 'Scroll', 'Body', 'BtnBack', 'Hint', 'Blur', 'Shade'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
call(BT, 'remove_function_graph', {'blueprint': W.ref, 'graph_name': 'OnKeyDown'})
brush, txt, box, cslot, bslot, rule, button = mk(W)
W.count = {'Root': 0}
def font(f, size, sp=0): return {'fontObject': f, 'typefaceFontName': 'Default', 'size': size, 'letterSpacing': sp}
def text(name, parent, s, f, size, sp, color, a=1.0, wrap=False):
    t, ts = W.add('TextBlock', name, parent)
    setp(t, {'text': s, 'font': font(f, size, sp), 'AutoWrapText': wrap, 'colorAndOpacity': {'specifiedColor': col(color, a), 'colorUseRule': 'UseColor_Specified'}})
    return t, ts
sz, s = W.add('SizeBox', 'CardSz', 'Root'); cslot(s, 0.0, 0.5, 70, -40, 0, 0, alx=0.0, aly=0.5); setp(s, {'bAutoSize': True})
setp(sz, {'widthOverride': 470, 'bOverride_WidthOverride': True})
row, _ = W.add('HorizontalBox', 'CardRow', 'CardSz')
bar, bs = W.add('SizeBox', 'AccentSz', 'CardRow'); setp(bar, {'widthOverride': 4, 'bOverride_WidthOverride': True}); bslot(bs, v='VAlign_Fill')
box('Accent', 'AccentSz', TEAL, 0.95)
_, cs = box('Card', 'CardRow', '070a0b', 0.86, padding={'left': 22, 'top': 16, 'right': 22, 'bottom': 18}); bslot(cs, fill=1.0)
vb, _ = W.add('VerticalBox', 'CardCol', 'Card')
_, s = text('Caption', 'CardCol', 'TUTORIAL', F_SEMI, 13, 450, TEAL); bslot(s, pad=(0, 0, 0, 10))
hb, s = W.add('HorizontalBox', 'KeyRow', 'CardCol'); bslot(s, pad=(0, 0, 0, 10))
_, s = box('KeyOuter', 'KeyRow', TEAL, 0.9, padding={'left': 2, 'top': 2, 'right': 2, 'bottom': 2}); bslot(s, v='VAlign_Center')
box('KeyInner', 'KeyOuter', '11181a', 1.0, padding={'left': 14, 'top': 5, 'right': 14, 'bottom': 6})
text('KeyText', 'KeyInner', 'W A S D', F_SEMI, 22, 120, WHITE)
_, s = text('Title', 'KeyRow', 'MOVE', F_SEMI, 28, 200, WHITE); bslot(s, pad=(18, 0, 0, 0), v='VAlign_Center')
text('HintText', 'CardCol', 'Walk around.', F_MED, 18, 0, WHITE, 0.75, True)
for n in ('KeyText', 'Title', 'HintText'):
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
print('compile', call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
fn(WT, 'SetupTutorial', '''(fn SetupTutorial (Keys TitleText Hint)
  (Widget|SetText(Text) (Variables|WBP_Tutorial|GetKeyText) (Utilities|Text|ToText(String) Keys))
  (Widget|SetText(Text) (Variables|WBP_Tutorial|GetTitle) (Utilities|Text|ToText(String) TitleText))
  (Widget|SetText(Text) (Variables|WBP_Tutorial|GetHintText) (Utilities|Text|ToText(String) Hint))
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "CloseTutorial" :Time 6.0 :bLooping false))''',
   params=[('Keys', 'string'), ('TitleText', 'string'), ('Hint', 'string')])
fn(WT, 'CloseTutorial', '(fn CloseTutorial ()\n  (Widget|RemoveFromParent self))')
print('compile', call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
call(A, 'save_assets', {'asset_paths': [P]})
# ---------------- game instance: seen list ----------------
var(GI, 'TutSeen', 'string')
call(BT, 'compile_blueprint', {'blueprint': {'refPath': GI}, 'warnings_as_errors': False})
# ---------------- Max ----------------
for n, t in (('NextTutT', 'float'), ('TutNear', 'bool'), ('TutEnemy', 'bool')): var(MAX, n, t)
call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False})
fn(MAX, 'TutSeen', '''(fn TutSeen (Id)
  (bind gi %s
    (:then (return (Utilities|String|Contains (Class|BPHKGameInstance|GetTutSeen :self gi) (Utilities|String|Append (Utilities|String|Append "|" Id) "|"))))
    (:CastFailed (return true))))''' % GIC, params=[('Id', 'string')], outs=[('Seen', 'bool')])
fn(MAX, 'ShowTutorial', '''(fn ShowTutorial (Id Keys TitleText Hint)
  (bind gi %s
    (:then
      (Class|BPHKGameInstance|SetTutSeen :self gi :TutSeen (Utilities|String|Append (Class|BPHKGameInstance|GetTutSeen :self gi) (Utilities|String|Append (Utilities|String|Append "|" Id) "|")))
      (Variables|Default|SetNextTutT (+ (Utilities|Time|GetGameTimeinSeconds) 7.0))
      (CallFunction|HKLog :Msg (Utilities|String|Append "TUTORIAL " Id))
      (bind t (Utilities|Casting|CastToWBP_Tutorial (UserInterface|CreateWidget "%s_C" (Game|GetPlayerController 0))))
      (UserInterface|Viewport|AddToViewport t 30)
      (Class|WBPTutorial|SetupTutorial :self t :Keys Keys :TitleText TitleText :Hint Hint))
    (:CastFailed)))''' % (GIC, WT), params=[('Id', 'string'), ('Keys', 'string'), ('TitleText', 'string'), ('Hint', 'string')])
# prompts in priority order: (id, condition, keys, title, hint)
NEAR = lambda cls, folder: '''(for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/%s/%s.%s_C")
      (if (< (Transformation|GetDistanceTo self x) 350.0) (Variables|Default|SetTutNear true)))''' % (folder, cls, cls)
G = lambda v: '(Variables|Default|Get%s)' % v
PROMPTS = [
    ('move', 'true', 'W  A  S  D', 'MOVE', 'Walk. Hold the left stick on a controller.'),
    ('look', 'true', 'MOUSE', 'LOOK', 'Look around. Right stick on a controller.'),
    ('run', 'true', 'SHIFT', 'RUN', 'Hold to run. Running is loud: Hollows hear it.'),
    ('torch', 'true', 'F', 'FLASHLIGHT', 'Turn your flashlight on or off. Darkness hides you, light shows the way.'),
    ('interact', G('TutNear'), 'E', 'INTERACT', 'Open doors, flip breakers, turn counters, make choices.'),
    ('throw', '(> %s 0)' % G('Bottles'), 'G', 'THROW', 'Throw a bottle. Hollows chase the noise.'),
    ('aim', G('HasPistol'), 'RMB  /  Q', 'AIM', 'Hold to aim the pistol (T toggles aiming).'),
    ('fire', G('HasPistol'), 'LMB', 'FIRE', 'Every bullet counts. Aim for the head.'),
    ('reload', G('HasPistol'), 'R', 'RELOAD', 'Reload from your reserve rounds.'),
    ('punch', G('TutEnemy'), 'V', 'PUNCH', 'Shove a Hollow away when it gets too close.'),
    ('shoulder', G('Aiming'), 'TAB', 'SWAP SHOULDER', 'Look past the other side of a corner.'),
    ('bag', '(> (+ (+ %s %s) (+ %s %s)) 0)' % (G('Gels'), G('Sedatives'), G('Parts'), G('Chem')), 'B', 'BACKPACK', 'Heal and use what you carry.'),
    ('bench', '(and (> %s 0) (> %s 0))' % (G('Parts'), G('Chem')), 'I', 'WORKBENCH', 'Craft gels and rounds from parts and chemicals.'),
    ('map', '(not (Utilities|String|EqualExactly(String) %s ""))' % G('MapsFound'), 'M', 'MAP', 'You found a floor plan. Check where you are.'),
    ('journal', '(> (Utilities|String|Len %s) 0)' % G('Journal'), 'J', 'JOURNAL', 'Notes, files and objectives you have found.'),
]
chain = ''
for pid, cond, keys, title, hint in reversed(PROMPTS):
    call_ = '(CallFunction|ShowTutorial :Id "%s" :Keys "%s" :TitleText "%s" :Hint "%s")' % (pid, keys, title, hint)
    test = '(and (not (CallFunction|TutSeen :Id "%s")) %s)' % (pid, cond)
    chain = '(if %s\n      %s%s)' % (test, call_, ('\n      (else ' + chain + ')') if chain else '')
fn(MAX, 'TutorialTick', '''(fn TutorialTick ()
  (if (and (not (Variables|Default|GetDead)) (> (Utilities|Time|GetGameTimeinSeconds) (Variables|Default|GetNextTutT)))
    (Variables|Default|SetTutNear false)
    %s
    %s
    %s
    %s
    (for e (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone_C")
      (if (< (Transformation|GetDistanceTo self e) 1800.0) (Variables|Default|SetTutEnemy true)))
    %s))''' % (NEAR('BP_Door', 'Floors'), NEAR('BP_Breaker', 'Floors'), NEAR('BP_Dial', 'Floors'), NEAR('BP_Choice', 'Interactables'), chain))
# level start: iOS gets the touch HUD, everything else the tutorial prompts (first one after 4 s)
fn(MAX, 'AddTouchHUD', '''(fn AddTouchHUD ()
  (if (Utilities|String|EqualExactly(String) (Game|GetPlatformName) "IOS")
    (UserInterface|Viewport|AddToViewport (UserInterface|CreateWidget "/Game/HollowKin/UI/HUD/WBP_TouchHUD.WBP_TouchHUD_C" (Game|GetPlayerController 0)) 5)
    (Game|Player|ActivateTouchInterface :self (Game|GetPlayerController 0) :NewTouchInterface "/Game/HollowKin/UI/Touch/TI_HollowKin.TI_HollowKin")
    (else
      (Variables|Default|SetNextTutT (+ (Utilities|Time|GetGameTimeinSeconds) 4.0))
      (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "TutorialTick" :Time 1.0 :bLooping true))))''')
# touch builds: key hints read USE instead of E / (Y)
fn(MAX, 'Notify', '''(fn Notify (Msg Seconds)
  (bind msg (select (Utilities|String|EqualExactly(String) (Game|GetPlatformName) "IOS") (Utilities|String|Replace :SourceString Msg :From "E / (Y)" :To "USE") Msg))
  (CallFunction|HKLog :Msg (Utilities|String|Append "MESSAGE " msg))
  (Utilities|IsValid (Variables|Default|GetScreenFXRef)
    (:"Is Valid"
      (Class|WBPScreenFX|ShowMessage :self (Variables|Default|GetScreenFXRef) :Msg msg :Seconds Seconds))))''', params=[('Msg', 'string'), ('Seconds', 'float')])
print('Max', call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': [P, MAX.split('.')[0], GI.split('.')[0]]}))
