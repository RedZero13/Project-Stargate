"""Choices with consequences + New Game+ (2026-11-27).
BP_Choice (Interactables): walk up, press E, pick one of two options on WBP_Choice (the game pauses). Each option can
change Bond / Taint / health gels / reserve rounds, set a flag on Max (Flags "|flag|", carried between levels and
written in the journal), play a voice line and spawn Hollows nearby. One-shot.
BP_FlagGate: 1.5 s after a level starts, keeps or removes the actors tagged GateTag depending on Max's flags
(NeedFlag / ForbidFlag; "NG+" is set on New Game+ runs). Consequences are pre-placed actors with that tag.
New Game+: unlocked after any ending (progress save). Max starts with the pistol, 24 rounds, 2 gels, last run's
journal as memories, flag NG+; Hollows have 30% more health; Emilia's echoes and the hidden ending need NG+."""
import json
from menu_common import *
import menu_logic as ml
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
GI = '/Game/HollowKin/Blueprints/Systems/BP_HKGameInstance.BP_HKGameInstance'
PS = '/Game/HollowKin/Blueprints/Systems/BP_ProgressSave.BP_ProgressSave'
DR = '/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone'
CH = '/Game/HollowKin/Blueprints/Interactables/BP_Choice.BP_Choice'
FG = '/Game/HollowKin/Blueprints/Interactables/BP_FlagGate.BP_FlagGate'
P = '/Game/HollowKin/UI/Menus/WBP_Choice'; WC = P + '.WBP_Choice'
MM = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'
MAXC = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'
GIC = '(Utilities|Casting|CastToBP_HKGameInstance (Game|GetGameInstance))'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(bp, name, dsl, params=(), outs=()):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt in params: call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': True})
    for pn, pt in outs: call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': False})
    w(bp + ':' + name, dsl)
def mkbp(path, folder):
    if not call(A, 'exists', {'path': path.split('.')[0]}).get('returnValue'):
        print(call(BT, 'create', {'folder_path': folder, 'asset_name': path.split('.')[-1], 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
def vars_(bp, vs, editable=True):
    have = call(BT, 'list_variables', {'blueprint': {'refPath': bp}}).get('returnValue') or []
    for n, t in vs:
        if n in have: continue
        if t.startswith('/'): call(BT, 'add_object_variable', {'blueprint': {'refPath': bp}, 'name': n, 'object_class': {'refPath': t}})
        else: call(BT, 'add_variable', {'blueprint': {'refPath': bp}, 'name': n, 'type_name': t})
        if editable: call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': bp}, 'variable_name': n, 'instance_editable': True})
    call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False})
# ---------------- data on Max / GI / progress ----------------
vars_(MAX, [('Flags', 'string')], editable=False)
vars_(GI, [('NGPlus', 'bool')], editable=False)
vars_(PS, [('NGUnlocked', 'bool'), ('LastJournal', 'string')], editable=False)
fn(MAX, 'HasFlag', '''(fn HasFlag (F)
  (return (Utilities|String|Contains (Variables|Default|GetFlags) (Utilities|String|Append (Utilities|String|Append "|" F) "|"))))''', params=[('F', 'string')], outs=[('Has', 'bool')])
fn(MAX, 'AddFlag', '''(fn AddFlag (F)
  (if (not (CallFunction|HasFlag :F F))
    (Variables|Default|SetFlags (Utilities|String|Append (Variables|Default|GetFlags) (Utilities|String|Append (Utilities|String|Append "|" F) "|")))
    (CallFunction|HKLog :Msg (Utilities|String|Append "FLAG " F))))''', params=[('F', 'string')])
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
# ---------------- BP_Choice ----------------
mkbp(CH, '/Game/HollowKin/Blueprints/Interactables')
vars_(CH, [('Prompt', 'string'), ('Question', 'string'), ('OptA', 'string'), ('OptB', 'string'), ('ResA', 'string'), ('ResB', 'string'),
           ('FlagA', 'string'), ('FlagB', 'string'), ('BondA', 'float'), ('BondB', 'float'), ('TaintA', 'float'), ('TaintB', 'float'),
           ('GelsA', 'int'), ('GelsB', 'int'), ('AmmoA', 'int'), ('AmmoB', 'int'), ('SpawnA', 'int'), ('SpawnB', 'int'),
           ('VoiceA', '/Script/Engine.SoundBase'), ('VoiceB', '/Script/Engine.SoundBase'), ('VoiceQ', '/Script/Engine.SoundBase'),
           ('KillTagA', 'string'), ('KillTagB', 'string'), ('Done', 'bool'), ('NextNag', 'float')])
w(CH + ':EventGraph', '''(event EventTick (DeltaSeconds)
  (bind m %s
    (:then
      (if (and (and (not (Variables|Default|GetDone)) (< (Transformation|GetDistanceTo self m) 200.0)) (> (Utilities|Time|GetTimeSeconds) (Variables|Default|GetNextNag)))
        (Variables|Default|SetNextNag (+ (Utilities|Time|GetTimeSeconds) 8.0))
        (Class|BPMax|Notify :self m :Msg (Utilities|String|Append "E   " (Variables|Default|GetPrompt)) :Seconds 3.0)))
    (:CastFailed)))''' % MAXC)
fn(CH, 'Pick', '''(fn Pick (Opt)
  (Variables|Default|SetDone true)
  (bind a (== Opt 0))
  (bind m %s
    (:then
      (Class|BPMax|SetBond :self m :Bond (Math|Float|Clamp(Float) (+ (Class|BPMax|GetBond :self m) (select a (Variables|Default|GetBondA) (Variables|Default|GetBondB))) 0.0 100.0))
      (Class|BPMax|SetTaint :self m :Taint (Math|Float|Clamp(Float) (+ (Class|BPMax|GetTaint :self m) (select a (Variables|Default|GetTaintA) (Variables|Default|GetTaintB))) 0.0 100.0))
      (bind ng (+ (Class|BPMax|GetGels :self m) (select a (Variables|Default|GetGelsA) (Variables|Default|GetGelsB))))
      (Class|BPMax|SetGels :self m :Gels (select (> ng 0) ng 0))
      (bind nr (+ (Class|BPMax|GetReserveAmmo :self m) (select a (Variables|Default|GetAmmoA) (Variables|Default|GetAmmoB))))
      (Class|BPMax|SetReserveAmmo :self m :ReserveAmmo (select (> nr 0) nr 0))
      (Class|BPMax|AddFlag :self m :F (select a (Variables|Default|GetFlagA) (Variables|Default|GetFlagB)))
      (Class|BPMax|HKLog :self m :Msg (Utilities|String|Append "CHOICE " (select a (Variables|Default|GetFlagA) (Variables|Default|GetFlagB))))
      (Class|BPMax|ShowNote :self m :Msg (select a (Variables|Default|GetResA) (Variables|Default|GetResB)) :Seconds 7.0)
      (bind kt (select a (Variables|Default|GetKillTagA) (Variables|Default|GetKillTagB)))
      (if (not (Utilities|String|EqualExactly(String) kt ""))
        (for x (Actor|GetAllActorswithTag (Utilities|String|StringToName kt))
          (Actor|DestroyActor :self x)))
      (bind n (select a (Variables|Default|GetSpawnA) (Variables|Default|GetSpawnB)))
      (if (>= n 1)
        (Game|SpawnActorfromClass :Class "%s_C" :SpawnTransform (Math|Transform|MakeTransform (+ (Transformation|GetActorLocation) (Math|Vector|MakeVector 450.0 250.0 120.0)) (Math|Rotator|MakeRotator 0.0 180.0 0.0) (Math|Vector|MakeVector 1.0 1.0 1.0))))
      (if (>= n 2)
        (Game|SpawnActorfromClass :Class "%s_C" :SpawnTransform (Math|Transform|MakeTransform (+ (Transformation|GetActorLocation) (Math|Vector|MakeVector -450.0 -250.0 120.0)) (Math|Rotator|MakeRotator 0.0 0.0 0.0) (Math|Vector|MakeVector 1.0 1.0 1.0))))
      (if a
        (Utilities|IsValid (Variables|Default|GetVoiceA) (:"Is Valid" (Audio|PlaySound2D :Sound (Variables|Default|GetVoiceA) :VolumeMultiplier 1.0)))
        (else (Utilities|IsValid (Variables|Default|GetVoiceB) (:"Is Valid" (Audio|PlaySound2D :Sound (Variables|Default|GetVoiceB) :VolumeMultiplier 1.0))))))
    (:CastFailed)))''' % (MAXC, DR.split('.')[0] + '.BP_HollowDrone', DR.split('.')[0] + '.BP_HollowDrone'), params=[('Opt', 'int')])
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': CH}, 'warnings_as_errors': False}))
# ---------------- WBP_Choice ----------------
if call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'delete', {'path': P})
call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Credits', 'new_path': P})
W = Wbp(WC)
for n in ('Scroll', 'Body', 'BtnBack', 'Hint'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
call(BT, 'remove_function_graph', {'blueprint': W.ref, 'graph_name': 'OnKeyDown'})
setp(W.widget('Cap'), {'text': 'DECIDE /'})
brush, txt, box, cslot, bslot, rule, button = mk(W)
W.count = {'Root': 4}
t, s = W.add('TextBlock', 'Q', 'Root'); setp(t, {'text': '', 'font': {'size': 34, 'typefaceFontName': 'Regular', 'letterSpacing': 10}, 'autoWrapText': True,
     'colorAndOpacity': {'specifiedColor': col(WHITE), 'colorUseRule': 'UseColor_Specified'}}); cslot(s, 0, 0, 180, 300, 1300, 200)
vb, s = W.add('VerticalBox', 'Opts', 'Root'); cslot(s, 0, 0, 180, 560, 1300, 300)
button('BtnA', 'Opts', 'A', pad=(0, 6, 0, 10)); button('BtnB', 'Opts', 'B', pad=(0, 6, 0, 10))
for n in ('Q', 'BtnALabel', 'BtnBLabel'):
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
vars_(WC, [('Src', CH.replace('.BP_Choice', '.BP_Choice_C'))], editable=False)
G = lambda n: '(Variables|WBP_Choice|Get%s)' % n
fn(WC, 'Setup', '''(fn Setup (S)
  (Variables|Default|SetSrc S)
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Class|BPChoice|GetQuestion :self S)))
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Class|BPChoice|GetOptA :self S)))
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Class|BPChoice|GetOptB :self S))))''' % (G('Q'), G('BtnALabel'), G('BtnBLabel')),
   params=[('S', CH.replace('.BP_Choice', '.BP_Choice_C'))] if False else [])
call(BT, 'add_object_function_param', {'graph': {'refPath': WC + ':Setup'}, 'param_name': 'S', 'object_class': {'refPath': CH.replace('.BP_Choice', '.BP_Choice_C')}, 'input_param': True})
w(WC + ':Setup', '''(fn Setup (S)
  (Variables|Default|SetSrc S)
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Class|BPChoice|GetQuestion :self S)))
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Class|BPChoice|GetOptA :self S)))
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Class|BPChoice|GetOptB :self S))))''' % (G('Q'), G('BtnALabel'), G('BtnBLabel')))
CLOSE = '''(bind pc (Game|GetPlayerController 0))
  (Widget|RemoveFromParent self)
  (Game|SetGamePaused false)
  (Input|SetInputModeGameOnly pc false)
  (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor false)'''
fn(WC, 'PickA', '(fn PickA ()\n  %s\n  (Class|BPChoice|Pick :self (Variables|Default|GetSrc) :Opt 0))' % CLOSE)
fn(WC, 'PickB', '(fn PickB ()\n  %s\n  (Class|BPChoice|Pick :self (Variables|Default|GetSrc) :Opt 1))' % CLOSE)
fn(WC, 'CloseCredits', '(fn CloseCredits ()\n  %s)' % CLOSE)
ml.wire(WC, 'BtnA', 'PickA', 0); ml.wire(WC, 'BtnB', 'PickB', 200)
ml.connect_clicks(WC, {'BtnA': 'PickA', 'BtnB': 'PickB'})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
fn(CH, 'Press', '''(fn Press ()
  (if (not (Variables|Default|GetDone))
    (bind pc (Game|GetPlayerController 0))
    (bind wdg (Utilities|Casting|CastToWBP_Choice (UserInterface|CreateWidget "%s_C" pc)))
    (Class|WBPChoice|Setup :self wdg :S self)
    (UserInterface|Viewport|AddToViewport wdg 65)
    (Game|SetGamePaused true)
    (Input|SetInputModeUIOnly :PlayerController pc :InWidgetToFocus wdg :InMouseLockMode "DoNotLock")
    (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor true)
    (Utilities|IsValid (Variables|Default|GetVoiceQ) (:"Is Valid" (Audio|PlaySound2D :Sound (Variables|Default|GetVoiceQ) :VolumeMultiplier 1.0)))))''' % WC)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': CH}, 'warnings_as_errors': False}))
# ---------------- BP_FlagGate ----------------
mkbp(FG, '/Game/HollowKin/Blueprints/Interactables')
vars_(FG, [('NeedFlag', 'string'), ('ForbidFlag', 'string'), ('GateTag', 'string')])
w(FG + ':EventGraph', '''(event EventBeginPlay
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Check" :Time 1.5 :bLooping false))''')
fn(FG, 'Check', '''(fn Check ()
  (bind m %s
    (:then
      (bind ok (and (or (Utilities|String|EqualExactly(String) (Variables|Default|GetNeedFlag) "") (Class|BPMax|HasFlag :self m :F (Variables|Default|GetNeedFlag)))
                    (or (Utilities|String|EqualExactly(String) (Variables|Default|GetForbidFlag) "") (not (Class|BPMax|HasFlag :self m :F (Variables|Default|GetForbidFlag))))))
      (if (not ok)
        (for x (Actor|GetAllActorswithTag (Utilities|String|StringToName (Variables|Default|GetGateTag)))
          (Actor|DestroyActor :self x))))
    (:CastFailed)))''' % MAXC)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': FG}, 'warnings_as_errors': False}))
# ---------------- Max.Interact includes choices ----------------
near = lambda cls, v, folder='Floors': '''(for %s (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/%s/%s.%s_C")
      (if (< (Transformation|GetDistanceTo self %s) 200.0)
        (Class|%s|Press :self (Utilities|Casting|CastTo%s %s))))''' % (v, folder, cls, cls, v, cls.replace('_', ''), cls, v)
w(MAX + ':Interact', '''(fn Interact ()
  (if (not (Variables|Default|GetDead))
    %s
    %s
    %s
    %s
    %s))''' % (near('BP_Breaker', 'b'), near('BP_Dial', 'd'), near('BP_CellConsole', 'c'), near('BP_Door', 'o'), near('BP_Choice', 'h', 'Interactables')))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
# ---------------- NG+: tougher Hollows ----------------
fn(DR, 'NGPlusBoost', '''(fn NGPlusBoost ()
  (bind gi %s
    (:then (if (Class|BPHKGameInstance|GetNGPlus :self gi) (Variables|Default|SetDroneHealth (* (Variables|Default|GetDroneHealth) 1.3))))
    (:CastFailed)))''' % GIC)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DR}, 'warnings_as_errors': False}))
fn(MAX, 'NGBoostAll', """(fn NGBoostAll ()
  (for d (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone_C")
    (Class|BPHollowDrone|NGPlusBoost :self (Utilities|Casting|CastToBP_HollowDrone d))))""")
# objective log + NG+ boost once per level (same body as journal_map.py, plus the boost)
w(MAX + ':SetObjectiveNote', r"""(fn SetObjectiveNote (Msg)
  (if (not (Variables|Default|GetTraceOn))
    (Variables|Default|SetTraceOn true)
    (CallFunction|HKLog :Msg "LEVEL START")
    (CallFunction|NGBoostAll)
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "HKTrace" :Time 2.0 :bLooping true))
  (if (not (Utilities|String|EqualExactly(String) Msg (Variables|Default|GetLastObjective)))
    (Variables|Default|SetLastObjective Msg)
    (Variables|Default|SetObjLog (Utilities|String|Append (Utilities|String|Append (Utilities|String|Append (CallFunction|FloorLabel) "   ") (Utilities|String|Append Msg "\n")) (Variables|Default|GetObjLog)))
    (CallFunction|HKLog :Msg (Utilities|String|Append "OBJECTIVE " Msg)))
  (Utilities|IsValid (Variables|Default|GetScreenFXRef)
    (:"Is Valid"
      (Class|WBPScreenFX|SetObjective :self (Variables|Default|GetScreenFXRef) :Msg Msg))))""")
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
# ---------------- NG+ unlock (called from ShowEnding) and start ----------------
vars_(GI, [('CFlags', 'string'), ('CJournal', 'string'), ('CObjLog', 'string'), ('CMapsFound', 'string')], editable=False)
fn(GI, 'UnlockNG', """(fn UnlockNG (J)
  (CallFunction|LoadProgress)
  (bind p (Variables|Default|GetProgress))
  (Class|BPProgressSave|SetNGUnlocked :self p :NGUnlocked true)
  (Class|BPProgressSave|SetLastJournal :self p :LastJournal J)
  (CallFunction|SaveProgress))""", params=[('J', 'string')])
fn(GI, 'CanNG', """(fn CanNG ()
  (CallFunction|LoadProgress)
  (return (Class|BPProgressSave|GetNGUnlocked :self (Variables|Default|GetProgress))))""", outs=[('Can', 'bool')])
fn(GI, 'StartNG', r"""(fn StartNG ()
  (CallFunction|SetChapterKit :Index 0)
  (CallFunction|LoadProgress)
  (Variables|Default|SetNGPlus true)
  (Variables|Default|SetCarry true)
  (Variables|Default|SetCarryPistol true)
  (Variables|Default|SetCAmmo 8) (Variables|Default|SetCReserveAmmo 24) (Variables|Default|SetCGels 2)
  (Variables|Default|SetCFlags "|NG+|")
  (Variables|Default|SetCJournal (Utilities|String|Append "MEMORIES.  You have done this before.  You remember:\n\n" (Class|BPProgressSave|GetLastJournal :self (Variables|Default|GetProgress)))))""")
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': GI}, 'warnings_as_errors': False}))
# main menu: NEW GAME + (shown only after an ending)
W2 = Wbp(MM); b2 = mk(W2)
have = [x['widget']['refPath'].split('.')[-1] for x in call(U, 'GetWidgets', {'widgetBlueprint': W2.ref})['returnValue']['widgets']]
if 'BtnNGPlus' in have: call(U, 'RemoveWidget', {'widgetBlueprint': W2.ref, 'widget': {'refPath': W2.widget('BtnNGPlus')}})
W2.count['Left'] = 5
b2[6]('BtnNGPlus', 'Left', 'NEW GAME +')
f = json.loads(call(O, 'get_properties', {'instance': {'refPath': W2.widget('BtnQuitLabel')}, 'properties': ['Font']})['returnValue'])['Font']
setp(W2.widget('BtnNGPlusLabel'), {'font': f})
call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W2.ref, 'widget': {'refPath': W2.widget('BtnNGPlus')}, 'bIsVariable': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W2.ref}))
fn(MM, 'NewGamePlus', """(fn NewGamePlus ()
  (bind gi (Utilities|Casting|CastToBP_HKGameInstance (Widget|GetGameInstance))
    (:then
      (SaveGame|DeleteGameInSlot "HollowKinSlot1" 0)
      (Class|BPHKGameInstance|StartNG :self gi)
      (Game|OpenLevel(byName) "/Game/HollowKin/Maps/City/Lvl_City"))
    (:CastFailed)))""")
fn(MM, 'RefreshNG', """(fn RefreshNG ()
  (bind gi (Utilities|Casting|CastToBP_HKGameInstance (Widget|GetGameInstance))
    (:then
      (if (Class|BPHKGameInstance|CanNG :self gi)
        (Widget|SetVisibility :self (Variables|WBP_MainMenu|GetBtnNGPlus) :InVisibility "Visible")
        (else (Widget|SetVisibility :self (Variables|WBP_MainMenu|GetBtnNGPlus) :InVisibility "Collapsed"))))
    (:CastFailed)))""")
ml.wire(MM, 'BtnNGPlus', 'NewGamePlus', 0)
ml.connect_clicks(MM, {'BtnNGPlus': 'NewGamePlus'})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W2.ref}))
print(call(A, 'save_assets', {'asset_paths': []}))
