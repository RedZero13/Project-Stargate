"""WBP_Achievements (main menu -> ACHIEVEMENTS): list of all achievements (unlocked / locked) from the progress save,
plus best collectible counts, endings seen and total kills. Built from WBP_Credits (same look, BACK / Esc close).
Adds the ACHIEVEMENTS button to WBP_MainMenu above CREDITS."""
from menu_common import *
import menu_logic as ml
from achievements_data import ACH, TOTAL_DRAWINGS, TOTAL_FILES
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
P = '/Game/HollowKin/UI/Menus/WBP_Achievements'
W_ = P + '.WBP_Achievements'
if not call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Credits', 'new_path': P})
W = Wbp(W_)
setp(W.widget('Cap'), {'text': 'ACHIEVEMENTS /'})
call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget('Body')}, 'bIsVariable': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
G = '(Variables|Default|GetProgress)'
def cat(parts):
    e = parts[0]
    for p in parts[1:]: e = '(Utilities|String|Append %s %s)' % (e, p)
    return e
UNL = '(Class|BPProgressSave|GetAchList :self p)'
count = '0'
for i, t, d in ACH:
    count = '(+ %s (select (Utilities|String|Contains %s "|%s|") 1 0))' % (count, UNL, i)
lines = []
for i, t, d in ACH:
    d = d.replace('"', "'")
    lines.append('(select (Utilities|String|Contains %s "|%s|") "[ UNLOCKED ]    %s   -   %s\\n" "[  locked  ]    %s   -   %s\\n")' % (UNL, i, t.upper(), d, t.upper(), d))
I = 'Utilities|String|ToString(Integer)'
header = cat(['"UNLOCKED  "', '(%s %s)' % (I, count), '" / %d\\n"' % len(ACH),
              '"BEST RUN:  Emilia\'s drawings  "', '(%s (Class|BPProgressSave|GetBestDrawings :self p))' % I, '" / %d      Patient files  "' % TOTAL_DRAWINGS,
              '(%s (Class|BPProgressSave|GetBestFiles :self p))' % I, '" / %d\\n"' % TOTAL_FILES,
              '"ENDINGS SEEN:  "', '(select (Utilities|String|Contains (Class|BPProgressSave|GetEndings :self p) "|LANTERN|") "Lantern  " "")',
              '(select (Utilities|String|Contains (Class|BPProgressSave|GetEndings :self p) "|KIN|") "Kin  " "")',
              '(select (Utilities|String|Contains (Class|BPProgressSave|GetEndings :self p) "|HOMECOMING|") "Homecoming" "")',
              '"\\nHOLLOWS PUT DOWN:  "', '(%s (Class|BPProgressSave|GetKills :self p))' % I,
              '"\\n\\nREWARDS:  every 5 drawings hides a health gel, every 5 patient files a box of rounds.\\n\\n"'])
dsl = '''(event UserInterface|EventConstruct
  (Variables|Interaction|SetIsFocusable :bIsFocusable true)
  (Widget|SetKeyboardFocus self)
  (bind gi (Utilities|Casting|CastToBP_HKGameInstance (Widget|GetGameInstance))
    (:then
      (Class|BPHKGameInstance|LoadProgress :self gi)
      (bind p (Class|BPHKGameInstance|GetProgress :self gi))
      (Widget|SetText(Text) (Variables|WBP_Achievements|GetBody) (Utilities|Text|ToText(String) %s)))
    (:CastFailed)))''' % cat([header] + lines)
print('construct', call(BT, 'write_graph_dsl', {'graph': {'refPath': W_ + ':EventGraph'}, 'code': dsl}))
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
print(call(A, 'save_assets', {'asset_paths': [P]}))
# --- main menu button (above CREDITS) ---
MM = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'
W2 = Wbp(MM)
b2 = mk(W2)
have = [x['widget']['refPath'].split('.')[-1] for x in call(U, 'GetWidgets', {'widgetBlueprint': W2.ref})['returnValue']['widgets']]
if 'BtnAchievements' in have:
    call(U, 'RemoveWidget', {'widgetBlueprint': W2.ref, 'widget': {'refPath': W2.widget('BtnAchievements')}})
W2.count['Left'] = 8
b2[6]('BtnAchievements', 'Left', 'ACHIEVEMENTS')
f = json.loads(call(O, 'get_properties', {'instance': {'refPath': W2.widget('BtnQuitLabel')}, 'properties': ['Font']})['returnValue'])['Font']
setp(W2.widget('BtnAchievementsLabel'), {'font': f})
call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W2.ref, 'widget': {'refPath': W2.widget('BtnAchievements')}, 'bIsVariable': True})
# same big hit area as the other buttons (bigger_buttons.py)
PAD = {'left': 20, 'top': 10, 'right': 80, 'bottom': 10}
for x in call(U, 'GetWidgets', {'widgetBlueprint': W2.ref})['returnValue']['widgets']:
    if x['widget']['refPath'].endswith('.BtnAchievements'):
        st = json.loads(call(O, 'get_properties', {'instance': x['widget'], 'properties': ['WidgetStyle']})['returnValue'])['WidgetStyle']
        st['normalPadding'] = PAD; st['pressedPadding'] = PAD
        call(O, 'set_properties', {'instance': x['widget'], 'values': json.dumps({'WidgetStyle': st})})
        call(O, 'set_properties', {'instance': x['slot'], 'values': json.dumps({'Padding': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}, 'HorizontalAlignment': 'HAlign_Fill'})})
call(BT, 'add_function_graph', {'blueprint': {'refPath': MM}, 'graph_name': 'OpenAchievements'})
print('OpenAchievements', call(BT, 'write_graph_dsl', {'graph': {'refPath': MM + ':OpenAchievements'}, 'code': '''(fn OpenAchievements ()
  (UserInterface|Viewport|AddToViewport (UserInterface|CreateWidget "%s" (Game|GetPlayerController 0)) 70))''' % (W_ + '_C')}))
ml.wire(MM, 'BtnAchievements', 'OpenAchievements', 0)
ml.connect_clicks(MM, {'BtnAchievements': 'OpenAchievements'})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W2.ref}))
print(call(A, 'save_assets', {'asset_paths': ['/Game/HollowKin/UI/Menus/WBP_MainMenu']}))
