"""Map, journal and objectives (2026-11-27).
- WBP_Journal: one screen with three tabs. MAP shows the current floor's plan (docs/floorplans/<L>.png, imported as
  /Game/HollowKin/UI/Maps/T_Plan_<L>) once Max has found that floor's evacuation plan (BP_MapBoard in the lift
  lobby; the clinic plans come with the building). JOURNAL lists every note, clue and message Max has read, newest
  first, in a handwritten font (Patrick Hand, SIL OFL) on paper. OBJECTIVES shows the current goal and the log.
- Keys: M opens the map, J the journal (Esc / M / J / Tab close). Both pause the game.
- BP_Max: Journal, ObjLog, MapsFound strings; JournalAdd (called from ShowNote), objective history from
  SetObjectiveNote; FloorLabel() works out the floor from the level and height."""
import json, os, subprocess
from menu_common import *
import menu_logic as ml
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
TT = 'editor_toolset.toolsets.texture.TextureTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
MB = '/Game/HollowKin/Blueprints/Floors/BP_MapBoard.BP_MapBoard'
P = '/Game/HollowKin/UI/Menus/WBP_Journal'; WJ = P + '.WBP_Journal'
HAND = '/Game/HollowKin/UI/Fonts/PatrickHand-Regular_Font.PatrickHand-Regular_Font'
BODY_F = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
HERE = os.path.dirname(os.path.abspath(__file__))
PLANS = os.path.abspath(os.path.join(HERE, '..', '..', 'docs', 'floorplans'))
LABELS = ['G', 'F1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15']
MAXC = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(bp, name, dsl, params=(), outs=()):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt in params:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': True})
    for pn, pt in outs:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': False})
    w(bp + ':' + name, dsl)
# ---------------- 1. plan textures ----------------
for L in LABELS:
    if not call(A, 'exists', {'path': '/Game/HollowKin/UI/Maps/T_Plan_' + L}).get('returnValue'):
        print(L, call(TT, 'import_file', {'folder_path': '/Game/HollowKin/UI/Maps', 'asset_name': 'T_Plan_' + L, 'source_file': os.path.join(PLANS, L + '.png')}).get('returnValue') is not None)
# ---------------- 2. Max data + hooks ----------------
have = call(BT, 'list_variables', {'blueprint': {'refPath': MAX}}).get('returnValue') or []
for n in ('Journal', 'ObjLog', 'MapsFound'):
    if n not in have: call(BT, 'add_variable', {'blueprint': {'refPath': MAX}, 'name': n, 'type_name': 'string'})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False})
fn(MAX, 'FloorLabel', '''(fn FloorLabel ()
  (bind lvl (Game|GetCurrentLevelName true))
  (bind z (Math|Vector|DotProduct (Transformation|GetActorLocation) (Math|Vector|MakeVector 0.0 0.0 1.0)))
  (return
    (select (Utilities|String|Contains lvl "Clinic") (select (> z 300.0) "F1" "G")
      (select (Utilities|String|Contains lvl "Wards") (Utilities|String|Append "B" (Utilities|String|ToString(Integer) (+ 2 (Math|Float|Round (/ (- 0.0 z) 1500.0)))))
        (select (Utilities|String|Contains lvl "Deep") (select (> z -1000.0) "B9" (Utilities|String|Append "B" (Utilities|String|ToString(Integer) (+ 10 (Math|Float|Round (/ (- -2000.0 z) 1500.0))))))
          (select (Utilities|String|Contains lvl "Containment") "B1" "MILLBROOK"))))))''', outs=[('Label', 'string')])
fn(MAX, 'JournalAdd', '''(fn JournalAdd (Text)
  (if (and (not (Utilities|String|Contains (Variables|Default|GetJournal) Text))
           (and (> (Utilities|String|Len Text) 30) (and (not (Utilities|String|Contains Text "WASD")) (not (Utilities|String|Contains Text "NEW OBJECTIVE")))))
    (Variables|Default|SetJournal (Utilities|String|Append (Utilities|String|Append (Utilities|String|Append (CallFunction|FloorLabel) "  -  ") (Utilities|String|Append Text "\n\n")) (Variables|Default|GetJournal)))))''', params=[('Text', 'string')])
# ShowNote -> JournalAdd (ShowNote only forwarded to Notify before); SetObjectiveNote also keeps an objective log
fn(MAX, 'ShowNote', """(fn ShowNote (Msg Seconds)
  (CallFunction|JournalAdd :Text Msg)
  (CallFunction|Notify :Msg Msg :Seconds Seconds))""", params=[('Msg', 'string'), ('Seconds', 'float')])
w(MAX + ':SetObjectiveNote', """(fn SetObjectiveNote (Msg)
  (if (not (Variables|Default|GetTraceOn))
    (Variables|Default|SetTraceOn true)
    (CallFunction|HKLog :Msg "LEVEL START")
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "HKTrace" :Time 2.0 :bLooping true))
  (if (not (Utilities|String|EqualExactly(String) Msg (Variables|Default|GetLastObjective)))
    (Variables|Default|SetLastObjective Msg)
    (Variables|Default|SetObjLog (Utilities|String|Append (Utilities|String|Append (Utilities|String|Append (CallFunction|FloorLabel) "   ") (Utilities|String|Append Msg "\n")) (Variables|Default|GetObjLog)))
    (CallFunction|HKLog :Msg (Utilities|String|Append "OBJECTIVE " Msg)))
  (Utilities|IsValid (Variables|Default|GetScreenFXRef)
    (:"Is Valid"
      (Class|WBPScreenFX|SetObjective :self (Variables|Default|GetScreenFXRef) :Msg Msg))))""")
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
# ---------------- 3. BP_MapBoard: evacuation plan on the lobby wall ----------------
if not call(A, 'exists', {'path': MB.split('.')[0]}).get('returnValue'):
    print(call(BT, 'create', {'folder_path': '/Game/HollowKin/Blueprints/Floors', 'asset_name': 'BP_MapBoard', 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
hv = call(BT, 'list_variables', {'blueprint': {'refPath': MB}}).get('returnValue') or []
for n, t in (('Label', 'string'), ('Done', 'bool')):
    if n not in hv:
        call(BT, 'add_variable', {'blueprint': {'refPath': MB}, 'name': n, 'type_name': t})
        call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': MB}, 'variable_name': n, 'instance_editable': True})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': MB}, 'warnings_as_errors': False})
w(MB + ':EventGraph', """(event EventBeginPlay
  (bind c (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent")))
  (Components|StaticMesh|SetStaticMesh c "/Game/Horror_Hospital/Meshes/SM_Board_04_v01.SM_Board_04_v01")
  (Transformation|SetRelativeScale3D :self c :NewScale3D (Math|Vector|MakeVector 1.3 1.3 1.3))
  (bind t (Utilities|Casting|CastToTextRenderComponent (Game|AddComponentbyClass self "/Script/Engine.TextRenderComponent")))
  (Rendering|Components|TextRender|SetText :self t :Value (Utilities|Text|ToText(String) "EVACUATION PLAN"))
  (Rendering|Components|TextRender|SetWorldSize :self t :Value 12.0)
  (Rendering|Components|TextRender|SetHorizontalAlignment :self t :Value "EHTA_Center")
  (Rendering|Components|TextRender|SetTextRenderColor :self t :Value (Math|Color|MakeColor 0.2 0.9 0.4 1.0))
  (Transformation|SetRelativeLocation :self t :NewLocation (Math|Vector|MakeVector 0.0 -8.0 205.0))
  (Transformation|SetRelativeRotation :self t :NewRotation (Math|Rotator|MakeRotator 0.0 -90.0 0.0)))""")
w(MB + ':EventGraph', """(event EventTick (DeltaSeconds)
  (bind m %s
    (:then
      (if (and (not (Variables|Default|GetDone)) (< (Transformation|GetDistanceTo self m) 200.0))
        (Variables|Default|SetDone true)
        (Class|BPMax|SetMapsFound :self m :MapsFound (Utilities|String|Append (Class|BPMax|GetMapsFound :self m) (Utilities|String|Append (Utilities|String|Append "|" (Variables|Default|GetLabel)) "|")))
        (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Futuristic_Click_04.Futuristic_Click_04" 0.6)
        (Class|BPMax|Notify :self m :Msg (Utilities|String|Append (Utilities|String|Append "EVACUATION PLAN  " (Variables|Default|GetLabel)) "  -  photographed. Press M for the map.") :Seconds 4.0)))
    (:CastFailed)))""" % MAXC)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MB}, 'warnings_as_errors': False}))
# ---------------- 4. WBP_Journal ----------------
if call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'delete', {'path': P})
call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Credits', 'new_path': P})
W = Wbp(WJ)
for g in ('OnKeyDown',):
    call(BT, 'remove_function_graph', {'blueprint': W.ref, 'graph_name': g})
for n in ('Cap', 'Scroll', 'Body', 'BtnBack', 'Hint'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
brush, txt, box, cslot, bslot, rule, button = mk(W)
W.count = {'Root': 3}
def font(size, f=BODY_F, ls=20): return {'fontObject': f, 'typefaceFontName': 'Default', 'size': size, 'letterSpacing': ls}
def color(h, a=1.0): return {'specifiedColor': col(h, a), 'colorUseRule': 'UseColor_Specified'}
t, s = W.add('TextBlock', 'Cap', 'Root'); setp(t, {'text': 'FIELD KIT /', 'font': font(16, ls=700), 'colorAndOpacity': color(DIM)}); cslot(s, 0, 0, 140, 80, 0, 0); setp(s, {'bAutoSize': True})
hb, s = W.add('HorizontalBox', 'Tabs', 'Root'); cslot(s, 0, 0, 140, 120, 900, 70)
for name, label in (('BtnMap', 'MAP'), ('BtnJournal', 'JOURNAL'), ('BtnObj', 'OBJECTIVES')):
    button(name, 'Tabs', label, pad=(0, 0, 24, 0))
# map panel
cv, s = W.add('CanvasPanel', 'MapPanel', 'Root'); cslot(s, 0, 0, 140, 210, 1640, 760)
im, s = W.add('Border', 'MapImg', 'MapPanel'); cslot(s, 0, 0, 0, 0, 1640, 650)
t, s = W.add('TextBlock', 'MapNote', 'MapPanel'); setp(t, {'text': '', 'font': font(22), 'colorAndOpacity': color(WHITE, 0.85), 'autoWrapText': True})
cslot(s, 0, 0, 0, 670, 1600, 80)
# journal panel (paper)
b, s = box('Paper', 'Root', 'e9dfc6', 0.97); cslot(s, 0, 0, 140, 210, 1640, 760)
setp(b, {'padding': {'left': 60, 'top': 40, 'right': 60, 'bottom': 40}})
sb, s = W.add('ScrollBox', 'JScroll', 'Paper')
t, s = W.add('TextBlock', 'JText', 'JScroll')
setp(t, {'text': '', 'font': {'fontObject': HAND, 'typefaceFontName': 'Default', 'size': 30, 'letterSpacing': 0}, 'colorAndOpacity': color('1c2733', 0.92),
         'autoWrapText': True, 'lineHeightPercentage': 1.05})
# objectives panel
vb, s = W.add('VerticalBox', 'ObjPanel', 'Root'); cslot(s, 0, 0, 140, 210, 1640, 760)
t, s = W.add('TextBlock', 'OHead', 'ObjPanel'); setp(t, {'text': 'CURRENT OBJECTIVE', 'font': font(18, ls=500), 'colorAndOpacity': color(TEAL)})
t, s = W.add('TextBlock', 'OCur', 'ObjPanel'); setp(t, {'text': '', 'font': font(34, ls=10), 'colorAndOpacity': color(WHITE), 'autoWrapText': True})
bslot(s, pad=(0, 10, 0, 40))
t, s = W.add('TextBlock', 'OLogHead', 'ObjPanel'); setp(t, {'text': 'EARLIER', 'font': font(16, ls=500), 'colorAndOpacity': color(DIM)})
sb, s = W.add('ScrollBox', 'OScroll', 'ObjPanel'); bslot(s, fill=1.0)
t, s = W.add('TextBlock', 'OLog', 'OScroll'); setp(t, {'text': '', 'font': font(20, ls=10), 'colorAndOpacity': color(WHITE, 0.7), 'autoWrapText': True})
t, s = W.add('TextBlock', 'Hint', 'Root'); setp(t, {'text': 'M  Map     J  Journal     ESC  Close', 'font': font(18, ls=120), 'colorAndOpacity': color(WHITE, 0.7)})
cslot(s, 1, 1, -170, -60, 0, 0, alx=1.0); setp(s, {'bAutoSize': True})
for n in ('MapImg', 'MapNote', 'MapPanel', 'Paper', 'JText', 'ObjPanel', 'OCur', 'OLog'):
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
G = lambda n: '(Variables|WBP_Journal|Get%s)' % n
VIS = lambda n, on: '(Widget|SetVisibility :self %s :InVisibility "%s")' % (G(n), 'Visible' if on else 'Collapsed')
mapset = '(Widget|SetText(Text) %s (Utilities|Text|ToText(String) "No plan of this floor yet. Look for the EVACUATION PLAN board in the lift lobby."))' % G('MapNote')
for L in reversed(LABELS):
    mapset = '''(if (and (Utilities|String|EqualExactly(String) fl "%(L)s") (or (Utilities|String|Contains (Class|BPMax|GetMapsFound :self m) "|%(L)s|") (or (Utilities|String|EqualExactly(String) fl "G") (Utilities|String|EqualExactly(String) fl "F1"))))
          (Appearance|SetBrushfromTexture :self %(img)s :Texture "/Game/HollowKin/UI/Maps/T_Plan_%(L)s.T_Plan_%(L)s")
          (Widget|SetVisibility :self %(img)s :InVisibility "Visible")
          (Widget|SetText(Text) %(note)s (Utilities|Text|ToText(String) "%(L)s  -  you are on this floor. The exit lift is at the east end."))
          (else %(rest)s))''' % {'L': L, 'img': G('MapImg'), 'note': G('MapNote'), 'rest': mapset}
for name, body in [
    ('SetTab', '''(fn SetTab (Tab)
  (if (== Tab 0) %s (else %s))
  (if (== Tab 1) %s (else %s))
  (if (== Tab 2) %s (else %s))
  (bind m %s
    (:then
      (bind fl (Class|BPMax|FloorLabel :self m))
      (Widget|SetVisibility :self %s :InVisibility "Collapsed")
      %s
      (Widget|SetText(Text) %s (Utilities|Text|ToText(String) (select (Utilities|String|EqualExactly(String) (Class|BPMax|GetJournal :self m) "") "Nothing written down yet." (Class|BPMax|GetJournal :self m))))
      (Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Class|BPMax|GetLastObjective :self m)))
      (Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Class|BPMax|GetObjLog :self m))))
    (:CastFailed)))''' % (VIS('MapPanel', True), VIS('MapPanel', False), VIS('Paper', True), VIS('Paper', False), VIS('ObjPanel', True), VIS('ObjPanel', False),
                          MAXC, G('MapImg'), mapset, G('JText'), G('OCur'), G('OLog'))),
    ('TabMap', '(fn TabMap ()\n  (CallFunction|SetTab :Tab 0))'), ('TabJournal', '(fn TabJournal ()\n  (CallFunction|SetTab :Tab 1))'), ('TabObj', '(fn TabObj ()\n  (CallFunction|SetTab :Tab 2))'),
    ('CloseJournal', '''(fn CloseJournal ()
  (bind pc (Game|GetPlayerController 0))
  (Widget|RemoveFromParent self)
  (Game|SetGamePaused false)
  (Input|SetInputModeGameOnly pc false)
  (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor false))'''),
    ('CloseCredits', '(fn CloseCredits ()\n  (CallFunction|CloseJournal))'),
    ('OnKeyDown', '''(fn OnKeyDown (MyGeometry InKeyEvent)
  (bind k (Utilities|String|ToString(Text) (Input|Key|GetKeyDisplayName (Input|KeyEvent|GetKey InKeyEvent))))
  (if (or (or (Utilities|String|Equal,CaseInsensitive(String) k "Escape") (Utilities|String|Equal,CaseInsensitive(String) k "Tab")) (or (Utilities|String|Equal,CaseInsensitive(String) k "M") (Utilities|String|Equal,CaseInsensitive(String) k "J")))
    (CallFunction|CloseJournal)
    (return (Widget|EventReply|Handled))
    (else (return (Widget|EventReply|Unhandled)))))''')]:
    call(BT, 'add_function_graph', {'blueprint': W.ref, 'graph_name': name})
    if name == 'SetTab': call(BT, 'add_function_param', {'graph': {'refPath': WJ + ':SetTab'}, 'param_name': 'Tab', 'param_type': 'int', 'input_param': True})
    w(WJ + ':' + name, body)
for btn, f, y in (('BtnMap', 'TabMap', 0), ('BtnJournal', 'TabJournal', 200), ('BtnObj', 'TabObj', 400)):
    ml.wire(WJ, btn, f, y)
ml.connect_clicks(WJ, {'BtnMap': 'TabMap', 'BtnJournal': 'TabJournal', 'BtnObj': 'TabObj'})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
# ---------------- 5. Max: OpenJournal + keys M / J ----------------
fn(MAX, 'OpenJournal', '''(fn OpenJournal (Tab)
  (bind pc (Game|GetPlayerController 0))
  (bind w (Utilities|Casting|CastToWBP_Journal (UserInterface|CreateWidget "%s_C" pc)))
  (UserInterface|Viewport|AddToViewport w 60)
  (Class|WBPJournal|SetTab :self w :Tab Tab)
  (Game|SetGamePaused true)
  (Input|SetInputModeUIOnly :PlayerController pc :InWidgetToFocus w :InMouseLockMode "DoNotLock")
  (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor true))''' % WJ, params=[('Tab', 'int')])
fn(MAX, 'OpenMap', '(fn OpenMap ()\n  (CallFunction|OpenJournal :Tab 0))')
fn(MAX, 'OpenJournalTab', '(fn OpenJournalTab ()\n  (CallFunction|OpenJournal :Tab 1))')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
imc = '/Game/Input/IMC_Combat.IMC_Combat'
for ia in ('IA_Map', 'IA_Journal'):
    if not call(A, 'exists', {'path': '/Game/Input/Actions/' + ia}).get('returnValue'):
        print(ia, call(A, 'duplicate', {'path': '/Game/Input/Actions/IA_Melee', 'new_path': '/Game/Input/Actions/' + ia}))
d = json.loads(call(O, 'get_properties', {'instance': {'refPath': imc}, 'properties': ['DefaultKeyMappings']})['returnValue'])['DefaultKeyMappings']
keys = {m['key'] for m in d['mappings']}
for ia, k in (('IA_Map', 'M'), ('IA_Journal', 'J')):
    if k not in keys:
        d['mappings'].append({'triggers': [], 'modifiers': [], 'action': {'refPath': '/Game/Input/Actions/%s.%s' % (ia, ia)}, 'key': k,
                              'settingBehavior': 'InheritSettingsFromAction', 'playerMappableKeySettings': 'None'})
print('imc', call(O, 'set_properties', {'instance': {'refPath': imc}, 'values': json.dumps({'DefaultKeyMappings': d})}))
call(A, 'save_assets', {'asset_paths': ['/Game/Input/IMC_Combat', '/Game/Input/Actions/IA_Map', '/Game/Input/Actions/IA_Journal']})
if not os.environ.get('NOWIRE'):
    for ia, f, y in (('IA_Map', 'OpenMap', 3400), ('IA_Journal', 'OpenJournalTab', 3600)):
        print(ia, subprocess.run([os.path.join(HERE, 'wire.sh'), MAX, ia, f, str(y)], capture_output=True, text=True).stdout[-200:])
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
