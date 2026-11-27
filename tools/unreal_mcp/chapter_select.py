"""Chapter select (2026-11-27). Main menu -> CHAPTERS. A chapter unlocks the first time Max reaches it (kept in the
progress save, across runs and endings). Starting a chapter clears the checkpoint and gives Max that chapter's kit:
  PROLOGUE  Millbrook (Lvl_City)            nothing
  CHAPTER 1 St. Brigid's Clinic (Lvl_Clinic) nothing
  CHAPTER 2 Containment Wing                nothing (the pistol is found there)
  CHAPTER 3 The Wards                       pistol, 8 + 16 rounds, 1 health gel
  CHAPTER 4 The Deep Labs                   pistol, 8 + 24 rounds, 2 health gels, 1 sedative
Bond / Taint / collectibles start at zero, so every ending is still reachable from chapters 3 and 4.
NEW ADMISSION now also clears the carried kit (a new run used to inherit the last run's items)."""
import json, subprocess, sys
from menu_common import *
import menu_logic as ml
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
GI = '/Game/HollowKin/Blueprints/Systems/BP_HKGameInstance.BP_HKGameInstance'
PS = '/Game/HollowKin/Blueprints/Systems/BP_ProgressSave.BP_ProgressSave'
DIF = '/Game/HollowKin/UI/Menus/WBP_Difficulty.WBP_Difficulty'
L = '/Game/HollowKin/UI/Menus/WBP_Loading.WBP_Loading_C'
P = '/Game/HollowKin/UI/Menus/WBP_Chapters'; WC = P + '.WBP_Chapters'
MM = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'
CH = [  # id, label, title, level, (pistol, ammo, reserve, gels, sedatives), recap
    ('P', 'PROLOGUE', 'MILLBROOK', '/Game/HollowKin/Maps/City/Lvl_City', (False, 0, 0, 0, 0), 'A phone call in the rain. A sister who was never in foster care.'),
    ('C1', 'CHAPTER 1', "ST. BRIGID'S CLINIC", '/Game/HollowKin/Maps/Clinic/Lvl_Clinic', (False, 0, 0, 0, 0), 'A clinic too clean to be real, and a lift that will not go down.'),
    ('C2', 'CHAPTER 2', 'CONTAINMENT WING', '/Game/HollowKin/Maps/Containment/Lvl_ContainmentWing', (False, 0, 0, 0, 0), 'B1. The first Hollows. The first drawing.'),
    ('C3', 'CHAPTER 3', 'THE WARDS', '/Game/HollowKin/Maps/Wards/Lvl_Wards', (True, 8, 16, 1, 0), 'Seven floors of wards nobody was meant to leave.'),
    ('C4', 'CHAPTER 4', 'THE DEEP LABS', '/Game/HollowKin/Maps/Deep/Lvl_DeepLabs', (True, 8, 24, 2, 1), 'The real program, and the children at the bottom of it.'),
]
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(bp, name, dsl, params=()):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt in params:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': True})
    w(bp + ':' + name, dsl)
have = call(BT, 'list_variables', {'blueprint': {'refPath': PS}}).get('returnValue') or []
if 'Chapters' not in have: call(BT, 'add_variable', {'blueprint': {'refPath': PS}, 'name': 'Chapters', 'type_name': 'string'})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': PS}, 'warnings_as_errors': False})
fn(GI, 'ReachChapter', '''(fn ReachChapter (Id)
  (CallFunction|LoadProgress)
  (bind p (Variables|Default|GetProgress))
  (bind key (Utilities|String|Append (Utilities|String|Append "|" Id) "|"))
  (if (not (Utilities|String|Contains (Class|BPProgressSave|GetChapters :self p) key))
    (Class|BPProgressSave|SetChapters :self p :Chapters (Utilities|String|Append (Class|BPProgressSave|GetChapters :self p) key))
    (CallFunction|SaveProgress)))''', params=[('Id', 'string')])
fn(GI, 'HasChapter', '''(fn HasChapter (Id)
  (CallFunction|LoadProgress)
  (return (or (Utilities|String|EqualExactly(String) Id "P") (Utilities|String|Contains (Class|BPProgressSave|GetChapters :self (Variables|Default|GetProgress)) (Utilities|String|Append (Utilities|String|Append "|" Id) "|")))))''', params=[('Id', 'string')])
call(BT, 'add_function_param', {'graph': {'refPath': GI + ':HasChapter'}, 'param_name': 'Has', 'param_type': 'bool', 'input_param': False})
w(GI + ':HasChapter', '''(fn HasChapter (Id)
  (CallFunction|LoadProgress)
  (return (or (Utilities|String|EqualExactly(String) Id "P") (Utilities|String|Contains (Class|BPProgressSave|GetChapters :self (Variables|Default|GetProgress)) (Utilities|String|Append (Utilities|String|Append "|" Id) "|")))))''')
kit = []
for i, (cid, lab, title, lvl, (pistol, ammo, res, gels, sed), recap) in enumerate(CH):
    kit.append('''(if (== Index %d)
      (Variables|Default|SetCarry %s)
      (Variables|Default|SetCarryPistol %s)
      (Variables|Default|SetCAmmo %d) (Variables|Default|SetCReserveAmmo %d) (Variables|Default|SetCGels %d) (Variables|Default|SetCSedatives %d))''' %
               (i, 'true' if pistol else 'false', 'true' if pistol else 'false', ammo, res, gels, sed))
fn(GI, 'SetChapterKit', '''(fn SetChapterKit (Index)
  (Variables|Default|SetCHealth 100.0) (Variables|Default|SetCSanity 100.0) (Variables|Default|SetCBond 0.0) (Variables|Default|SetCTaint 0.0)
  (Variables|Default|SetCBottles 0) (Variables|Default|SetCParts 0) (Variables|Default|SetCChem 0) (Variables|Default|SetCTapes 0)
  (Variables|Default|SetCDrawings 0) (Variables|Default|SetCFiles 0) (Variables|Default|SetCRunKills 0)
  %s)''' % '\n  '.join(kit), params=[('Index', 'int')])
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': GI}, 'warnings_as_errors': False}))
# NEW ADMISSION: clean kit
w(DIF + ':StartRun', '''(fn StartRun ()
  (bind pc (Game|GetPlayerController 0))
  (SaveGame|DeleteGameInSlot "HollowKinSlot1" 0)
  (Class|BPHKGameInstance|SetChapterKit :self (Utilities|Casting|CastToBP_HKGameInstance (Widget|GetGameInstance)) :Index 0)
  (Input|SetInputModeGameOnly pc false)
  (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor false)
  (bind card (Utilities|Casting|CastToWBP_Loading (UserInterface|CreateWidget "%s" pc)))
  (Class|WBPLoading|SetupCard :self card :Chapter "PROLOGUE" :TitleText "MILLBROOK" :BodyText "Six days ago a letter reached Max Hunt: his little sister Emilia, taken into state care when she was six, never arrived at her foster home. Nobody will say where she went. Tonight, in the rain, someone finally calls." :TipText "TIP:  Hold right mouse, or press T, to aim. Every bullet counts." :Seconds 6.5)
  (UserInterface|Viewport|AddToViewport card 90)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "GoCity" :Time 6.5 :bLooping false))''' % L)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DIF}, 'warnings_as_errors': False}))
# ---------------- WBP_Chapters ----------------
if call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'delete', {'path': P})
call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Credits', 'new_path': P})
W = Wbp(WC)
for n in ('Scroll', 'Body'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
setp(W.widget('Cap'), {'text': 'CHAPTERS /'})
brush, txt, box, cslot, bslot, rule, button = mk(W)
W.count = {'Root': 4}
vb, s = W.add('VerticalBox', 'List', 'Root'); cslot(s, 0, 0, 180, 190, 1300, 760)
for i, (cid, lab, title, lvl, k, recap) in enumerate(CH):
    button('BtnCh%d' % i, 'List', '%s   //   %s' % (lab, title), pad=(0, 6, 0, 2))
    t, s2 = W.add('TextBlock', 'Recap%d' % i, 'List'); setp(t, {'text': recap, 'font': {'size': 18, 'typefaceFontName': 'Regular', 'letterSpacing': 20},
        'colorAndOpacity': {'specifiedColor': col(WHITE, 0.6), 'colorUseRule': 'UseColor_Specified'}}); bslot(s2, pad=(22, 0, 0, 16))
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget('BtnCh%d' % i)}, 'bIsVariable': True})
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget('BtnCh%dLabel' % i)}, 'bIsVariable': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
G = lambda n: '(Variables|WBP_Chapters|Get%s)' % n
GIC = '(Utilities|Casting|CastToBP_HKGameInstance (Widget|GetGameInstance))'
lock = '\n      '.join('''(if (not (Class|BPHKGameInstance|HasChapter :self gi :Id "%s"))
        (Widget|SetIsEnabled :self %s :bInIsEnabled false)
        (Widget|SetText(Text) %s (Utilities|Text|ToText(String) "%s   //   LOCKED")))''' % (cid, G('BtnCh%d' % i), G('BtnCh%dLabel' % i), lab) for i, (cid, lab, *_r) in enumerate(CH))
w(WC + ':EventGraph', '''(event UserInterface|EventConstruct
  (Variables|Interaction|SetIsFocusable :bIsFocusable true)
  (Widget|SetKeyboardFocus self)
  (bind gi %s
    (:then
      %s)
    (:CastFailed)))''' % (GIC, lock))
have = call(BT, 'list_variables', {'blueprint': {'refPath': WC}}).get('returnValue') or []
if 'Pick' not in have: call(BT, 'add_variable', {'blueprint': {'refPath': WC}, 'name': 'Pick', 'type_name': 'int'})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': WC}, 'warnings_as_errors': False})
fn(WC, 'GoChapter', '''(fn GoChapter ()
  (bind gi %s
    (:then
      (SaveGame|DeleteGameInSlot "HollowKinSlot1" 0)
      (Class|BPHKGameInstance|SetChapterKit :self gi :Index (Variables|Default|GetPick))
      %s)
    (:CastFailed)))''' % (GIC, '\n      '.join('(if (== (Variables|Default|GetPick) %d) (Game|OpenLevel(byName) "%s"))' % (i, c[3]) for i, c in enumerate(CH))))
for i, (cid, lab, title, lvl, k, recap) in enumerate(CH):
    fn(WC, 'PlayCh%d' % i, '''(fn PlayCh%d ()
  (Variables|Default|SetPick %d)
  (bind pc (Game|GetPlayerController 0))
  (Input|SetInputModeGameOnly pc false)
  (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor false)
  (bind card (Utilities|Casting|CastToWBP_Loading (UserInterface|CreateWidget "%s" pc)))
  (Class|WBPLoading|SetupCard :self card :Chapter "%s" :TitleText "%s" :BodyText "%s" :TipText "Chapter select: Bond, Taint and collectibles start fresh." :Seconds 4.0)
  (UserInterface|Viewport|AddToViewport card 95)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "GoChapter" :Time 4.0 :bLooping false))''' % (i, i, L, lab, title.replace('"', "'"), recap))
    ml.wire(WC, 'BtnCh%d' % i, 'PlayCh%d' % i, 200 * i)
ml.connect_clicks(WC, dict(('BtnCh%d' % i, 'PlayCh%d' % i) for i in range(len(CH))))
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
# ---------------- main menu button ----------------
W2 = Wbp(MM); b2 = mk(W2)
have = [x['widget']['refPath'].split('.')[-1] for x in call(U, 'GetWidgets', {'widgetBlueprint': W2.ref})['returnValue']['widgets']]
if 'BtnChapters' in have: call(U, 'RemoveWidget', {'widgetBlueprint': W2.ref, 'widget': {'refPath': W2.widget('BtnChapters')}})
W2.count['Left'] = 6
b2[6]('BtnChapters', 'Left', 'CHAPTERS')
f = json.loads(call(O, 'get_properties', {'instance': {'refPath': W2.widget('BtnQuitLabel')}, 'properties': ['Font']})['returnValue'])['Font']
setp(W2.widget('BtnChaptersLabel'), {'font': f})
call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W2.ref, 'widget': {'refPath': W2.widget('BtnChapters')}, 'bIsVariable': True})
fn(MM, 'OpenChapters', '''(fn OpenChapters ()
  (UserInterface|Viewport|AddToViewport (UserInterface|CreateWidget "%s_C" (Game|GetPlayerController 0)) 70))''' % WC)
ml.wire(MM, 'BtnChapters', 'OpenChapters', 0)
ml.connect_clicks(MM, {'BtnChapters': 'OpenChapters'})
subprocess.run([sys.executable, 'menu_fit.py'])
print(call(A, 'save_assets', {'asset_paths': []}))
