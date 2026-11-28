"""New puzzle mechanics (2026-11-26), all used through a new INTERACT key (E / gamepad D-pad right):
- BP_Breaker (gate 4, "Lights Out"): four breakers on a wall. E flips a breaker AND its neighbours. All four green
  powers the lift. Four in a row is always solvable.
- BP_Dial (gate 5, "bed numbers"): three wall counters 0-9. E turns one up by 1. The lift Code (3 digits, first never 0)
  is spread over three notes on the floor, one digit each.
- BP_CellConsole (B15): opens all six cells if Max has read at least 5 patient files (needed for the SIX DOORS ending).
- BP_FloorLift: BreakerHit / DialCheck, locked-lift messages for gates 4 and 5.
- BP_Max: Interact (E) presses the nearest breaker / dial / console within 2 m. FreedChildren flag.
E used to be a spare FIRE key; left mouse / Enter still fire."""
import json, os, subprocess
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
F = '/Game/HollowKin/Blueprints/Floors'
LIFT = F + '/BP_FloorLift.BP_FloorLift'; BRK = F + '/BP_Breaker.BP_Breaker'; DIAL = F + '/BP_Dial.BP_Dial'; CON = F + '/BP_CellConsole.BP_CellConsole'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
MAXCAST = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'
HH = '/Game/Horror_Hospital/Meshes/'
def mk(path, vars_):
    if not call(A, 'exists', {'path': path.split('.')[0]}).get('returnValue'):
        print(call(BT, 'create', {'folder_path': F, 'asset_name': path.split('.')[-1], 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
    have = call(BT, 'list_variables', {'blueprint': {'refPath': path}}).get('returnValue') or []
    for n, t in vars_:
        if n in have: continue
        call(BT, 'add_variable', {'blueprint': {'refPath': path}, 'name': n, 'type_name': t})
        call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': path}, 'variable_name': n, 'instance_editable': True})
    call(BT, 'compile_blueprint', {'blueprint': {'refPath': path}, 'warnings_as_errors': False})
def objvar(path, name, cls):
    have = call(BT, 'list_variables', {'blueprint': {'refPath': path}}).get('returnValue') or []
    if name not in have:
        call(BT, 'add_object_variable', {'blueprint': {'refPath': path}, 'name': name, 'object_class': {'refPath': cls}})
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(bp, name, dsl, params=()):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt, inp in params:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': inp})
    w(bp + ':' + name, dsl)
ev = lambda bp, dsl: w(bp + ':EventGraph', dsl)
PL = '/Script/Engine.PointLightComponent'; TR = '/Script/Engine.TextRenderComponent'
mk(BRK, [('Label', 'string'), ('Idx', 'int'), ('On', 'bool'), ('NextNag', 'float')])
objvar(BRK, 'Lamp', PL); objvar(BRK, 'Txt', TR)
mk(DIAL, [('Label', 'string'), ('Idx', 'int'), ('Digit', 'int'), ('NextNag', 'float')])
objvar(DIAL, 'Txt', TR)
mk(CON, [('Done', 'bool'), ('NextNag', 'float')])
mk(MAX, [('FreedChildren', 'bool')])
for p in (BRK, DIAL, CON): call(BT, 'compile_blueprint', {'blueprint': {'refPath': p}, 'warnings_as_errors': False})
# prompt helper shared by the three props: "E  <verb>" once every 6 s while Max stands close
def prompt(verb):
    return '''(event EventTick (DeltaSeconds)
  (bind m %s
    (:then
      (bind now (Utilities|Time|GetTimeSeconds))
      (if (and (< (Transformation|GetDistanceTo self m) 190.0) (> now (Variables|Default|GetNextNag)))
        (Variables|Default|SetNextNag (+ now 8.0))
        (Class|BPMax|Notify :self m :Msg "%s" :Seconds 2.5)))
    (:CastFailed)))''' % (MAXCAST, verb)
# ---------------- breaker ----------------
fn(BRK, 'SetOn', '''(fn SetOn (V)
  (Variables|Default|SetOn V)
  (Rendering|Components|Light|SetLightColor :self (Variables|Default|GetLamp) :NewLightColor (select V (Math|Color|MakeColor 0.2 1.0 0.4 1.0) (Math|Color|MakeColor 1.0 0.15 0.1 1.0)))
  (Rendering|Components|TextRender|SetTextRenderColor :self (Variables|Default|GetTxt) :Value (select V (Math|Color|MakeColor 0.3 1.0 0.5 1.0) (Math|Color|MakeColor 1.0 0.25 0.2 1.0))))''', params=[('V', 'bool', True)])
ev(BRK, '''(event EventBeginPlay
  (bind c (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent")))
  (Components|StaticMesh|SetStaticMesh c "%sSM_Switcher_01_v01.SM_Switcher_01_v01")
  (Transformation|SetRelativeScale3D :self c :NewScale3D (Math|Vector|MakeVector 3.0 3.0 3.0))
  (bind t (Utilities|Casting|CastToTextRenderComponent (Game|AddComponentbyClass self "%s")))
  (Rendering|Components|TextRender|SetText :self t :Value (select (== (Variables|Default|GetIdx) 0) "A" (select (== (Variables|Default|GetIdx) 1) "B" (select (== (Variables|Default|GetIdx) 2) "C" "D"))))
  (Rendering|Components|TextRender|SetWorldSize :self t :Value 22.0)
  (Rendering|Components|TextRender|SetHorizontalAlignment :self t :Value "EHTA_Center")
  (Transformation|SetRelativeLocation :self t :NewLocation (Math|Vector|MakeVector 0.0 -4.0 46.0))
  (Transformation|SetRelativeRotation :self t :NewRotation (Math|Rotator|MakeRotator 0.0 -90.0 0.0))
  (Variables|Default|SetTxt t)
  (bind l (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "%s")))
  (Transformation|SetRelativeLocation :self l :NewLocation (Math|Vector|MakeVector 0.0 -25.0 20.0))
  (Rendering|Components|Light|SetIntensity :self l :NewIntensity 40.0)
  (Rendering|Lighting|SetAttenuationRadius :self l :NewRadius 120.0)
  (Variables|Default|SetLamp l)
  (CallFunction|SetOn :V (Variables|Default|GetOn)))''' % (HH, TR, PL))
ev(BRK, prompt('E / (Y)   flip breaker   (it flips its neighbours too)'))
fn(BRK, 'Press', '''(fn Press ()
  (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_03.Flick_Switch_03" 0.9)
  (for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_FloorLift.BP_FloorLift_C")
    (bind lf (Utilities|Casting|CastToBP_FloorLift x))
    (if (Utilities|String|EqualExactly(String) (Class|BPFloorLift|GetLabel :self lf) (Variables|Default|GetLabel))
      (Class|BPFloorLift|BreakerHit :self lf :Idx (Variables|Default|GetIdx)))))''')
# ---------------- dial ----------------
ev(DIAL, '''(event EventBeginPlay
  (bind c (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent")))
  (Components|StaticMesh|SetStaticMesh c "%sSM_Computer_Monitor_01_v01.SM_Computer_Monitor_01_v01")
  (bind t (Utilities|Casting|CastToTextRenderComponent (Game|AddComponentbyClass self "%s")))
  (Rendering|Components|TextRender|SetWorldSize :self t :Value 30.0)
  (Rendering|Components|TextRender|SetHorizontalAlignment :self t :Value "EHTA_Center")
  (Rendering|Components|TextRender|SetTextRenderColor :self t :Value (Math|Color|MakeColor 0.4 1.0 0.7 1.0))
  (Transformation|SetRelativeLocation :self t :NewLocation (Math|Vector|MakeVector 0.0 -12.0 16.0))
  (Transformation|SetRelativeRotation :self t :NewRotation (Math|Rotator|MakeRotator 0.0 -90.0 0.0))
  (Variables|Default|SetTxt t)
  (Rendering|Components|TextRender|SetText :self t :Value (Utilities|String|ToString(Integer) (Variables|Default|GetDigit)))
  (bind l (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "%s")))
  (Transformation|SetRelativeLocation :self l :NewLocation (Math|Vector|MakeVector 0.0 -40.0 30.0))
  (Rendering|Components|Light|SetIntensity :self l :NewIntensity 30.0)
  (Rendering|Components|Light|SetLightColor :self l :NewLightColor (Math|Color|MakeColor 0.4 1.0 0.7 1.0))
  (Rendering|Lighting|SetAttenuationRadius :self l :NewRadius 120.0))''' % (HH, TR, PL))
ev(DIAL, prompt('E / (Y)   turn the counter'))
fn(DIAL, 'Press', '''(fn Press ()
  (Variables|Default|SetDigit (select (>= (Variables|Default|GetDigit) 9) 0 (+ (Variables|Default|GetDigit) 1)))
  (Rendering|Components|TextRender|SetText :self (Variables|Default|GetTxt) :Value (Utilities|String|ToString(Integer) (Variables|Default|GetDigit)))
  (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_01.Flick_Switch_01" 0.7)
  (for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_FloorLift.BP_FloorLift_C")
    (bind lf (Utilities|Casting|CastToBP_FloorLift x))
    (if (Utilities|String|EqualExactly(String) (Class|BPFloorLift|GetLabel :self lf) (Variables|Default|GetLabel))
      (Class|BPFloorLift|DialCheck :self lf))))''')
# ---------------- cell console (B15) ----------------
ev(CON, '''(event EventBeginPlay
  (bind c (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent")))
  (Components|StaticMesh|SetStaticMesh c "%sSM_Scanner_Monitor_01_v1.SM_Scanner_Monitor_01_v1")
  (bind l (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "%s")))
  (Transformation|SetRelativeLocation :self l :NewLocation (Math|Vector|MakeVector 0.0 -60.0 160.0))
  (Rendering|Components|Light|SetIntensity :self l :NewIntensity 60.0)
  (Rendering|Components|Light|SetLightColor :self l :NewLightColor (Math|Color|MakeColor 0.5 0.7 1.0 1.0))
  (Rendering|Lighting|SetAttenuationRadius :self l :NewRadius 260.0))''' % (HH, PL))
ev(CON, prompt('E / (Y)   use the cell release console'))
fn(CON, 'Press', '''(fn Press ()
  (bind m %s
    (:then
      (if (not (Variables|Default|GetDone))
        (if (>= (Class|BPMax|GetFiles :self m) 5)
          (Variables|Default|SetDone true)
          (Class|BPMax|SetFreedChildren :self m :FreedChildren true)
          (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Special_Powerup_03.Special_Powerup_03" 0.9)
          (Class|BPMax|HKLog :self m :Msg "CELLS opened")
          (Class|BPMax|Ach :self m :Id "cells" :Title "Open Every Door")
          (Class|BPMax|ShowNote :self m :Msg "The patient files had the release codes. Six locks clunk open at once. The children step out of their cells and look at you." :Seconds 6.0)
          (else
            (Class|BPMax|Notify :self m :Msg (Utilities|String|Append (Utilities|String|Append "RELEASE CODE REQUIRED.  The patient files list the codes. Files read: " (Utilities|String|ToString(Integer) (Class|BPMax|GetFiles :self m))) " / 5") :Seconds 4.0)))))
    (:CastFailed)))''' % MAXCAST)
# ---------------- lift: breaker + dial logic, locked messages ----------------
fn(LIFT, 'BreakerHit', '''(fn BreakerHit (Idx)
  (for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_Breaker.BP_Breaker_C")
    (bind b (Utilities|Casting|CastToBP_Breaker x))
    (if (and (Utilities|String|EqualExactly(String) (Class|BPBreaker|GetLabel :self b) (Variables|Default|GetLabel)) (and (>= (- (Class|BPBreaker|GetIdx :self b) Idx) -1) (<= (- (Class|BPBreaker|GetIdx :self b) Idx) 1)))
      (Class|BPBreaker|SetOn :self b :V (not (Class|BPBreaker|GetOn :self b)))))
  (Variables|Default|SetProgress 0)
  (for y (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_Breaker.BP_Breaker_C")
    (bind b2 (Utilities|Casting|CastToBP_Breaker y))
    (if (and (Utilities|String|EqualExactly(String) (Class|BPBreaker|GetLabel :self b2) (Variables|Default|GetLabel)) (Class|BPBreaker|GetOn :self b2))
      (Variables|Default|SetProgress (+ (Variables|Default|GetProgress) 1))))
  (if (>= (Variables|Default|GetProgress) 4)
    (Class|BPMax|Ach :self %s :Id "electrician" :Title "Electrician")
    (CallFunction|PowerLift)))''' % MAXCAST, params=[('Idx', 'int', True)])
fn(LIFT, 'DialCheck', '''(fn DialCheck ()
  (Variables|Default|SetProgress 0)
  (for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_Dial.BP_Dial_C")
    (bind d (Utilities|Casting|CastToBP_Dial x))
    (if (Utilities|String|EqualExactly(String) (Class|BPDial|GetLabel :self d) (Variables|Default|GetLabel))
      (Variables|Default|SetProgress (+ (Variables|Default|GetProgress) (* (Class|BPDial|GetDigit :self d) (select (== (Class|BPDial|GetIdx :self d) 0) 100 (select (== (Class|BPDial|GetIdx :self d) 1) 10 1)))))))
  (if (Utilities|String|EqualExactly(String) (Utilities|String|ToString(Integer) (Variables|Default|GetProgress)) (Variables|Default|GetCode))
    (Class|BPMax|Ach :self %s :Id "safecracker" :Title "Bed Numbers")
    (CallFunction|PowerLift)))''' % MAXCAST)
MSG = ('(select (== (Variables|Default|GetGate) 1) "LIFT LOCKED.  It needs this floor\'s KEYCARD." '
       '(select (== (Variables|Default|GetGate) 2) "LIFT LOCKED.  Three floor switches must be pressed in the right order. Somebody wrote the order down." '
       '(select (== (Variables|Default|GetGate) 4) "TRIPPED BREAKERS.  Find the breaker panel and get all four breakers green (E flips one and its neighbours)." '
       '(select (== (Variables|Default|GetGate) 5) "LIFT LOCKED.  Three-digit code on the counters by the lift. Three notes on this floor each hold one digit." '
       '(select (== (Variables|Default|GetGate) 6) "OUT OF ORDER.  A sign taped to the doors: \'STAFF - BASEMENT ACCESS FROM THE FIRST FLOOR SERVICE LIFT ONLY. USE THE STAIRS (WEST END).\'" '
       '"NO POWER.  Restart this floor\'s generator.")))))')
ev(LIFT, '''(event EventTick (DeltaSeconds)
  (bind m %s
    (:then
      (if (and (not (Variables|Default|GetBusy)) (< (Transformation|GetDistanceTo self m) 230.0))
        (if (or (Variables|Default|GetUnlocked) (== (Variables|Default|GetGate) 0))
          (CallFunction|GoDown)
          (else
            (bind now (Utilities|Time|GetTimeSeconds))
            (if (> now (Variables|Default|GetNextNag))
              (Variables|Default|SetNextNag (+ now 5.0))
              (Class|BPMax|Notify :self m :Msg %s :Seconds 4.0))))))
    (:CastFailed)))''' % (MAXCAST, MSG))
for p in (BRK, DIAL, CON, LIFT):
    print(p.split('.')[-1], call(BT, 'compile_blueprint', {'blueprint': {'refPath': p}, 'warnings_as_errors': False}))
# ---------------- Max: Interact ----------------
def near(cls, short):
    return '''(for %s (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/%s.%s_C")
    (if (< (Transformation|GetDistanceTo self %s) 200.0)
      (Class|%s|Press :self (Utilities|Casting|CastTo%s %s))))''' % (short, cls, cls, short, cls.replace('_', ''), cls, short)
fn(MAX, 'Interact', '''(fn Interact ()
  (if (not (Variables|Default|GetDead))
    %s
    %s
    %s))''' % (near('BP_Breaker', 'b'), near('BP_Dial', 'd'), near('BP_CellConsole', 'c')))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
# ---------------- input: IA_Interact on E (was a spare Fire key) + D-pad right ----------------
IA = '/Game/Input/Actions/IA_Interact'
if not call(A, 'exists', {'path': IA}).get('returnValue'):
    print(call(A, 'duplicate', {'path': '/Game/Input/Actions/IA_Melee', 'new_path': IA}))
imc = '/Game/Input/IMC_Combat.IMC_Combat'
d = json.loads(call(O, 'get_properties', {'instance': {'refPath': imc}, 'properties': ['DefaultKeyMappings']})['returnValue'])['DefaultKeyMappings']
maps = d['mappings']
for m in maps:   # step 1: same size, E -> IA_Interact
    if m['key'] == 'E': m['action'] = {'refPath': IA + '.IA_Interact'}
print('imc1', call(O, 'set_properties', {'instance': {'refPath': imc}, 'values': json.dumps({'DefaultKeyMappings': dict(d, mappings=maps)})}))
d = json.loads(call(O, 'get_properties', {'instance': {'refPath': imc}, 'properties': ['DefaultKeyMappings']})['returnValue'])['DefaultKeyMappings']
if not any(m['key'] == 'Gamepad_DPad_Right' for m in d['mappings']):   # step 2: append
    d['mappings'].append({'triggers': [], 'modifiers': [], 'action': {'refPath': IA + '.IA_Interact'}, 'key': 'Gamepad_DPad_Right',
                          'settingBehavior': 'InheritSettingsFromAction', 'playerMappableKeySettings': 'None'})
    print('imc2', call(O, 'set_properties', {'instance': {'refPath': imc}, 'values': json.dumps({'DefaultKeyMappings': d})}))
d = json.loads(call(O, 'get_properties', {'instance': {'refPath': imc}, 'properties': ['DefaultKeyMappings']})['returnValue'])['DefaultKeyMappings']
print([(m['action']['refPath'].split('.')[-1], m['key']) for m in d['mappings'] if 'Interact' in m['action']['refPath']])
call(A, 'save_assets', {'asset_paths': ['/Game/Input/IMC_Combat', IA]})
D = os.path.dirname(os.path.abspath(__file__))
if not os.environ.get('NOWIRE'): print('wire', subprocess.run([D + '/wire.sh', MAX, 'IA_Interact', 'Interact', '3200'], capture_output=True, text=True).stdout[-200:])
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
