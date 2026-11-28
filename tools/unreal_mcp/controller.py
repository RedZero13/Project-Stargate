"""Full controller support (Xbox / PlayStation / MFi pads; Xbox names below).
Gameplay (IMC_Sandbox from the sample + IMC_Combat):
  Left stick move, right stick look, LB sprint, A jump / climb, B crouch, LT aim, RT fire, X reload, RB melee,
  Y interact (doors, puzzles, choices), D-pad up torch, D-pad down throw, D-pad left map / journal, D-pad right
  workbench, View backpack, Menu pause, R3 swap shoulder.
  Removed from the sample's map: D-pad left/right (debug 'next pawn' / 'next look') and RB walk.
Menus: the first button gets focus as soon as a pad button is pressed (D-pad / stick moves between buttons, A
presses), and B / Menu / View close the screen (main menu: B does nothing)."""
import json
from ui_lib import *
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
SAND = '/Game/Input/IMC_Sandbox.IMC_Sandbox'; COMB = '/Game/Input/IMC_Combat.IMC_Combat'
def maps(imc): return json.loads(call(O, 'get_properties', {'instance': {'refPath': imc}, 'properties': ['DefaultKeyMappings']})['returnValue'])['DefaultKeyMappings']
def put(imc, d): print(imc.split('.')[-1], call(O, 'set_properties', {'instance': {'refPath': imc}, 'values': json.dumps({'DefaultKeyMappings': d})}).get('returnValue'))
IA = lambda n: {'refPath': '/Game/Input/Actions/%s.%s' % (n, n)}
# --- sample map: neutralise the debug D-pad actions and RB walk (same size first: key -> None) ---
d = maps(SAND)
for m in d['mappings']:
    a = m['action']['refPath'].split('.')[-1]
    if (m['key'] in ('Gamepad_DPad_Left', 'Gamepad_DPad_Right') and a in ('IA_NextPawn', 'IA_NextVisualOverride')) or (m['key'] == 'Gamepad_RightShoulder' and a == 'IA_Walk'):
        m['key'] = 'None'
put(SAND, d)
# --- combat map: same size changes first ---
d = maps(COMB)
for m in d['mappings']:
    a = m['action']['refPath'].split('.')[-1]
    if a == 'IA_Interact' and m['key'] == 'Gamepad_DPad_Right': m['key'] = 'Gamepad_FaceButton_Top'
    if a == 'IA_Melee' and m['key'] == 'Gamepad_FaceButton_Right': m['key'] = 'Gamepad_RightShoulder'
put(COMB, d)
d = maps(COMB); have = {(m['action']['refPath'].split('.')[-1], m['key']) for m in d['mappings']}
for a, k in (('IA_Map', 'Gamepad_DPad_Left'), ('IA_Workbench', 'Gamepad_DPad_Right')):
    if (a, k) not in have:
        d['mappings'].append({'triggers': [], 'modifiers': [], 'action': IA(a), 'key': k, 'settingBehavior': 'InheritSettingsFromAction', 'playerMappableKeySettings': 'None'})
put(COMB, d)
print([(m['action']['refPath'].split('.')[-1], m['key']) for m in maps(COMB)['mappings'] if 'Gamepad' in m['key']])
call(A, 'save_assets', {'asset_paths': ['/Game/Input/IMC_Sandbox', '/Game/Input/IMC_Combat']})
# --- menus: focus + back ---
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
K = '(Utilities|String|ToString(Text) (Input|Key|GetKeyDisplayName (Input|KeyEvent|GetKey InKeyEvent)))'
EQ = lambda s: '(Utilities|String|Equal,CaseInsensitive(String) k "%s")' % s
HAS = lambda s: '(Utilities|String|Contains k "%s")' % s
BACK = '(or %s (or %s %s))' % (HAS('Face Button Right'), HAS('Special Right'), HAS('Special Left'))
def menu(wbp, first, close, keys=('Escape', 'P'), extra_back=True):
    P = '/Game/HollowKin/UI/Menus/%s.%s' % (wbp, wbp)
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': {'refPath': P}, 'widget': {'refPath': P + ':WidgetTree.' + first}, 'bIsVariable': True})
    call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': P}})
    call(BT, 'add_function_graph', {'blueprint': {'refPath': P}, 'graph_name': 'OnKeyDown'})
    kc = ' '.join(EQ(x) for x in keys)
    keycond = kc if len(keys) == 1 else '(or %s)' % ' '.join([EQ(x) for x in keys][:1]) if False else None
    cond = EQ(keys[0])
    for x in keys[1:]: cond = '(or %s %s)' % (cond, EQ(x))
    if extra_back and close: cond = '(or %s %s)' % (cond, BACK)
    focus = """(if (and %s (not (Widget|HasAnyUserFocusedDescendants self)))
      (Widget|SetKeyboardFocus (Variables|%s|Get%s))
      (return (Widget|EventReply|Handled))
      (else (return (Widget|EventReply|Unhandled))))""" % (HAS('Gamepad'), wbp, first)
    if close:
        body = """(if %s
    %s
    (return (Widget|EventReply|Handled))
    (else
      %s))""" % (cond, close, focus)
    else:
        body = focus
    w(P + ':OnKeyDown', """(fn OnKeyDown (MyGeometry InKeyEvent)
  (bind k %s)
  %s)""" % (K, body))
    print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': P}}))
menu('WBP_Credits', 'BtnBack', '(CallFunction|CloseCredits)')
menu('WBP_Achievements', 'BtnBack', '(CallFunction|CloseCredits)')
menu('WBP_Chapters', 'BtnCh0', '(CallFunction|CloseCredits)')
menu('WBP_Journal', 'BtnMap', '(CallFunction|CloseJournal)', keys=('Escape', 'Tab', 'M', 'J'))
menu('WBP_Choice', 'BtnA', None)
menu('WBP_Backpack', 'Tab0', '(CallFunction|CloseCase)', keys=('Escape', 'P', 'I', 'B'))
menu('WBP_Settings', 'Cat0', '(CallFunction|DoBack)')
menu('WBP_PauseMenu', 'BtnResume', '(CallFunction|DoResume)', keys=('Escape', 'P'))
menu('WBP_Difficulty', 'BtnResume', '(Widget|RemoveFromParent self)', keys=('Escape',))
# main menu: title "press any key" first, then pad focus on NEW ADMISSION
P = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'
call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': {'refPath': P}, 'widget': {'refPath': P + ':WidgetTree.BtnNew'}, 'bIsVariable': True})
w(P + ':OnKeyDown', '''(fn OnKeyDown (MyGeometry InKeyEvent)
  (bind k %s)
  (if (< (Variables|Default|GetPhase) 4)
    (CallFunction|AnyKey)
    (return (Widget|EventReply|Handled))
    (else
      (if (and %s (not (Widget|HasAnyUserFocusedDescendants self)))
        (Widget|SetKeyboardFocus (Variables|WBP_MainMenu|GetBtnNew))
        (return (Widget|EventReply|Handled))
        (else (return (Widget|EventReply|Unhandled)))))))''' % (K, HAS('Gamepad')))
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': P}}))
print(call(A, 'save_assets', {'asset_paths': []}))
