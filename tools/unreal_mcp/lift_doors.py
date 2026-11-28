"""Real lifts and room doors (2026-11-27).
BP_FloorLift (unless NoDoors, used by the old B9 lift): builds its own door frame, two sliding leaves, a floor
indicator and a cabin light. Doors slide open when Max walks up and the lift works (Unlocked or Gate 0); stand in
the cabin for a second and they close, the cabin hums for 4 s, and the doors open on the next floor's arrival lift
(Target = that cabin). Lifts that change level (F1 -> Wing, B8 -> Deep Labs) open the next level after the ride.
Arrival lifts (Arrival = true) only open and close. Locked lifts keep their doors shut and say why.
BP_Door: a hinged door leaf (one, or two for wide doorways). E opens/closes it; Hollows open doors they reach.
BP_Max.Interact also presses doors."""
import os, subprocess
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
F = '/Game/HollowKin/Blueprints/Floors'
LIFT = F + '/BP_FloorLift.BP_FloorLift'; DOOR = F + '/BP_Door.BP_Door'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
MAXCAST = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'
HH = '/Game/Horror_Hospital/Meshes/'
SMC = '/Script/Engine.StaticMeshComponent'; PL = '/Script/Engine.PointLightComponent'; TR = '/Script/Engine.TextRenderComponent'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(bp, name, dsl, params=()):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt in params:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': True})
    w(bp + ':' + name, dsl)
def vars_(bp, vs, editable=()):
    have = call(BT, 'list_variables', {'blueprint': {'refPath': bp}}).get('returnValue') or []
    for n, t in vs:
        if n in have: continue
        if t.startswith('/Script'): call(BT, 'add_object_variable', {'blueprint': {'refPath': bp}, 'name': n, 'object_class': {'refPath': t}})
        else: call(BT, 'add_variable', {'blueprint': {'refPath': bp}, 'name': n, 'type_name': t})
        if n in editable: call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': bp}, 'variable_name': n, 'instance_editable': True})
    call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False})
# ------------------------------------------------------------------ lift
vars_(LIFT, [('NoDoors', 'bool'), ('Arrival', 'bool'), ('DoorAlpha', 'float'), ('InCabT', 'float'), ('Riding', 'bool'), ('RideT', 'float'),
             ('LeafL', SMC), ('LeafR', SMC), ('CabLight', PL)], editable=('NoDoors', 'Arrival'))
MSG = ('(select (== (Variables|Default|GetGate) 1) "LIFT LOCKED.  It needs this floor\'s KEYCARD." '
       '(select (== (Variables|Default|GetGate) 2) "LIFT LOCKED.  Three floor switches must be pressed in the right order. Somebody wrote the order down." '
       '(select (== (Variables|Default|GetGate) 4) "TRIPPED BREAKERS.  Find the breaker panel and get all four breakers green (E flips one and its neighbours)." '
       '(select (== (Variables|Default|GetGate) 5) "LIFT LOCKED.  Three-digit code on the counters beside the lift. Three notes on this floor each hold one digit." '
       '(select (== (Variables|Default|GetGate) 6) "OUT OF ORDER.  A sign taped to the doors: \'BASEMENT ACCESS FROM THE FIRST FLOOR SERVICE LIFT ONLY. USE THE STAIRS (WEST END).\'" '
       '"NO POWER.  Restart this floor\'s generator.")))))')
fn(LIFT, 'LegacyTick', '''(fn LegacyTick ()
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
fn(LIFT, 'StartRide', '''(fn StartRide ()
  (Variables|Default|SetRiding true)
  (Variables|Default|SetRideT 0.0)
  (Audio|PlaySound2D "/Game/HorrorAmbientSFX/HorrorAmbientSFX_cue/AMB_Drone_Server_Cue.AMB_Drone_Server_Cue" 0.6)
  (Rendering|Components|Light|SetIntensity :self (Variables|Default|GetCabLight) :NewIntensity 25.0)
  (bind m %s
    (:then
      (Class|BPMax|HKLog :self m :Msg (Utilities|String|Append "LIFT ride from " (Variables|Default|GetLabel)))
      (Class|BPMax|Notify :self m :Msg (Utilities|String|Append (Utilities|String|Append "The cabin shudders and drops.   " (Variables|Default|GetLabel)) (Utilities|String|Append "   >>   " (Variables|Default|GetNextLabel))) :Seconds 3.5))
    (:CastFailed)))''' % MAXCAST)
fn(LIFT, 'EndRide', '''(fn EndRide ()
  (Variables|Default|SetRiding false)
  (Variables|Default|SetInCabT -100.0)
  (Rendering|Components|Light|SetIntensity :self (Variables|Default|GetCabLight) :NewIntensity 60.0)
  (bind m %s
    (:then
      (if (not (Utilities|String|EqualExactly(String) (Variables|Default|GetNextLevel) ""))
        (Class|BPMax|StoreCarry :self m)
        (Game|OpenLevel(byName) :LevelName (Utilities|String|StringToName (Variables|Default|GetNextLevel)))
        (else
          (Transformation|SetActorLocation :self m :NewLocation (Variables|Default|GetTarget) :bSweep false :bTeleport true)
          (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_02.Flick_Switch_02" 0.8)
          (Class|BPMax|Notify :self m :Msg (Utilities|String|Append (Utilities|String|Append (Variables|Default|GetNextLabel) "   //   ") (Variables|Default|GetNextName)) :Seconds 4.0)
          (Class|BPMax|SetObjectiveNote :self m :Msg (Variables|Default|GetNextObjective))
          (Class|BPMax|SaveCheckpoint :self m))))
    (:CastFailed)))''' % MAXCAST)
fn(LIFT, 'DoorTick', '''(fn DoorTick (Dt)
  (bind m %s
    (:then
      (bind rel (- (Transformation|GetActorLocation m) (Transformation|GetActorLocation self)))
      (bind lx (Math|Vector|DotProduct rel (Transformation|GetActorForwardVector self)))
      (bind ly (Math|Vector|DotProduct rel (Transformation|GetActorRightVector self)))
      (bind ok (or (Variables|Default|GetArrival) (or (Variables|Default|GetUnlocked) (== (Variables|Default|GetGate) 0))))
      (bind incab (and (and (> lx 40.0) (< lx 300.0)) (and (> ly -120.0) (< ly 120.0))))
      (bind near (and (and (> lx -380.0) (< lx 300.0)) (and (> ly -260.0) (< ly 260.0))))
      (if incab
        (Variables|Default|SetInCabT (+ (Variables|Default|GetInCabT) Dt))
        (else (Variables|Default|SetInCabT 0.0)))
      (bind want (and (and ok near) (and (not (Variables|Default|GetRiding)) (or (Variables|Default|GetArrival) (< (Variables|Default|GetInCabT) 1.0)))))
      (Variables|Default|SetDoorAlpha (Math|Float|Clamp(Float) (+ (Variables|Default|GetDoorAlpha) (* Dt (select want 1.1 -1.1))) 0.0 1.0))
      (Transformation|SetRelativeLocation :self (Variables|Default|GetLeafL) :NewLocation (Math|Vector|MakeVector 0.0 (* (Variables|Default|GetDoorAlpha) 92.0) 0.0))
      (Transformation|SetRelativeLocation :self (Variables|Default|GetLeafR) :NewLocation (Math|Vector|MakeVector 0.0 (* (Variables|Default|GetDoorAlpha) -92.0) 0.0))
      (if (and (and incab ok) (and (not (Variables|Default|GetArrival)) (and (not (Variables|Default|GetRiding)) (and (> (Variables|Default|GetInCabT) 1.0) (<= (Variables|Default|GetDoorAlpha) 0.0)))))
        (CallFunction|StartRide))
      (if (Variables|Default|GetRiding)
        (Variables|Default|SetRideT (+ (Variables|Default|GetRideT) Dt))
        (if (>= (Variables|Default|GetRideT) 4.0) (CallFunction|EndRide)))
      (if (and (and (not ok) near) (< lx 0.0))
        (if (> (Utilities|Time|GetTimeSeconds) (Variables|Default|GetNextNag))
          (Variables|Default|SetNextNag (+ (Utilities|Time|GetTimeSeconds) 5.0))
          (Class|BPMax|Notify :self m :Msg %s :Seconds 4.0))))
    (:CastFailed)))''' % (MAXCAST, MSG), params=[('Dt', 'float')])
w(LIFT + ':EventGraph', '''(event EventTick (DeltaSeconds)
  (if (Variables|Default|GetNoDoors)
    (CallFunction|LegacyTick)
    (else (CallFunction|DoorTick :Dt DeltaSeconds))))''')
w(LIFT + ':EventGraph', '''(event EventBeginPlay
  (if (not (Variables|Default|GetNoDoors))
    (bind fr (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "%(SMC)s")))
    (Components|StaticMesh|SetStaticMesh fr "%(HH)sSM_Lift_01_p01.SM_Lift_01_p01")
    (Collision|SetCollisionEnabled :self fr :NewType "NoCollision")
    (bind l (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "%(SMC)s")))
    (Components|StaticMesh|SetStaticMesh l "%(HH)sSM_Lift_01_p02.SM_Lift_01_p02")
    (Variables|Default|SetLeafL l)
    (bind r (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "%(SMC)s")))
    (Components|StaticMesh|SetStaticMesh r "%(HH)sSM_Lift_01_p03.SM_Lift_01_p03")
    (Variables|Default|SetLeafR r)
    (bind cl (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "%(PL)s")))
    (Transformation|SetRelativeLocation :self cl :NewLocation (Math|Vector|MakeVector 160.0 0.0 290.0))
    (Rendering|Components|Light|SetIntensity :self cl :NewIntensity 60.0)
    (Rendering|Components|Light|SetLightColor :self cl :NewLightColor (Math|Color|MakeColor 0.85 0.92 1.0 1.0))
    (Rendering|Lighting|SetAttenuationRadius :self cl :NewRadius 260.0)
    (Variables|Default|SetCabLight cl)
    (bind t (Utilities|Casting|CastToTextRenderComponent (Game|AddComponentbyClass self "%(TR)s")))
    (Rendering|Components|TextRender|SetText :self t :Value (Utilities|String|Replace :SourceString (Variables|Default|GetLabel) :From "W" :To ""))
    (Rendering|Components|TextRender|SetWorldSize :self t :Value 26.0)
    (Rendering|Components|TextRender|SetHorizontalAlignment :self t :Value "EHTA_Center")
    (Rendering|Components|TextRender|SetTextRenderColor :self t :Value (Math|Color|MakeColor 1.0 0.45 0.2 1.0))
    (Transformation|SetRelativeLocation :self t :NewLocation (Math|Vector|MakeVector -24.0 0.0 252.0))
    (Transformation|SetRelativeRotation :self t :NewRotation (Math|Rotator|MakeRotator 0.0 180.0 0.0))))''' % {'SMC': SMC, 'HH': HH, 'PL': PL, 'TR': TR})
print('lift', call(BT, 'compile_blueprint', {'blueprint': {'refPath': LIFT}, 'warnings_as_errors': False}))
# ------------------------------------------------------------------ door
if not call(A, 'exists', {'path': DOOR.split('.')[0]}).get('returnValue'):
    print(call(BT, 'create', {'folder_path': F, 'asset_name': 'BP_Door', 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
vars_(DOOR, [('Width', 'float'), ('OpenYaw', 'float'), ('Open', 'bool'), ('Alpha', 'float'), ('NextNag', 'float'), ('LeafA', SMC), ('LeafB', SMC)], editable=('Width', 'OpenYaw', 'Open'))
w(DOOR + ':EventGraph', '''(event EventBeginPlay
  (bind dbl (> (Variables|Default|GetWidth) 200.0))
  (bind half (select dbl (* (Variables|Default|GetWidth) 0.5) (Variables|Default|GetWidth)))
  (bind a (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "%(SMC)s")))
  (Components|StaticMesh|SetStaticMesh a "%(HH)sSM_Door_01_p01.SM_Door_01_p01")
  (Transformation|SetRelativeLocation :self a :NewLocation (Math|Vector|MakeVector (* (Variables|Default|GetWidth) 0.5) 4.5 192.0))
  (Transformation|SetRelativeScale3D :self a :NewScale3D (Math|Vector|MakeVector (/ half 96.0) 1.0 1.0))
  (Variables|Default|SetLeafA a)
  (if dbl
    (bind b (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "%(SMC)s")))
    (Components|StaticMesh|SetStaticMesh b "%(HH)sSM_Door_01_p01.SM_Door_01_p01")
    (Transformation|SetRelativeLocation :self b :NewLocation (Math|Vector|MakeVector (* (Variables|Default|GetWidth) -0.5) -4.5 192.0))
    (Transformation|SetRelativeRotation :self b :NewRotation (Math|Rotator|MakeRotator 0.0 180.0 0.0))
    (Transformation|SetRelativeScale3D :self b :NewScale3D (Math|Vector|MakeVector (/ half 96.0) 1.0 1.0))
    (Variables|Default|SetLeafB b))
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "EnemyCheck" :Time 0.5 :bLooping true))''' % {'SMC': SMC, 'HH': HH})
fn(DOOR, 'EnemyCheck', '''(fn EnemyCheck ()
  (if (not (Variables|Default|GetOpen))
    (for e (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone_C")
      (if (< (Transformation|GetDistanceTo self e) 170.0)
        (Variables|Default|SetOpen true)))))''')
fn(DOOR, 'Press', '''(fn Press ()
  (Variables|Default|SetOpen (not (Variables|Default|GetOpen)))
  (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_04.Flick_Switch_04" 0.5))''')
# second leaf exists when Width > 200 (as in BeginPlay); an IsValid branch here used to end the tick (fixed 2026-11-28)
w(DOOR + ':EventGraph', '''(event EventTick (DeltaSeconds)
  (Variables|Default|SetAlpha (Math|Float|Clamp(Float) (+ (Variables|Default|GetAlpha) (* DeltaSeconds (select (Variables|Default|GetOpen) 1.6 -1.6))) 0.0 1.0))
  (Transformation|SetRelativeRotation :self (Variables|Default|GetLeafA) :NewRotation (Math|Rotator|MakeRotator 0.0 (* (Variables|Default|GetOpenYaw) (Variables|Default|GetAlpha)) 0.0))
  (if (> (Variables|Default|GetWidth) 200.0)
    (Transformation|SetRelativeRotation :self (Variables|Default|GetLeafB) :NewRotation (Math|Rotator|MakeRotator 0.0 (- 180.0 (* (Variables|Default|GetOpenYaw) (Variables|Default|GetAlpha))) 0.0)))
  (bind m %s
    (:then
      (if (and (not (Variables|Default|GetOpen)) (and (< (Transformation|GetDistanceTo self m) 170.0) (> (Utilities|Time|GetTimeSeconds) (Variables|Default|GetNextNag))))
        (Variables|Default|SetNextNag (+ (Utilities|Time|GetTimeSeconds) 10.0))
        (Class|BPMax|Notify :self m :Msg "E / (Y)   open the door" :Seconds 2.0)))
    (:CastFailed)))''' % MAXCAST)
print('door', call(BT, 'compile_blueprint', {'blueprint': {'refPath': DOOR}, 'warnings_as_errors': False}))
# ------------------------------------------------------------------ Max: Interact also opens doors (nearest only)
near = lambda cls, v: '''(for %s (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/%s.%s_C")
      (if (< (Transformation|GetDistanceTo self %s) 200.0)
        (Class|%s|Press :self (Utilities|Casting|CastTo%s %s))))''' % (v, cls, cls, v, cls.replace('_', ''), cls, v)
w(MAX + ':Interact', '''(fn Interact ()
  (if (not (Variables|Default|GetDead))
    %s
    %s
    %s
    %s))''' % (near('BP_Breaker', 'b'), near('BP_Dial', 'd'), near('BP_CellConsole', 'c'), near('BP_Door', 'o')))
print('max', call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
