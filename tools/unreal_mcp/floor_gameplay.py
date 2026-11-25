"""Floor gameplay for the stacked floors (docs/EXPANSION_PLAN.md). Creates/updates:
- BP_FloorLift: stands in each floor's lift room. Locked until that floor's puzzle is solved (Gate 0 open,
  1 keycard, 2 switch sequence, 3 generator power). Walking in: fade out, floor card, Max is moved to the next
  floor's arrival room (or another level opens when NextLevel is set), checkpoint saved there.
- BP_Keycard: glowing card; picking it up unlocks the lift tagged Lift_<Label>.
- BP_SeqSwitch: floor switch with a roman numeral; three per floor must be stepped on in the order given by
  that floor's note (lift Code, e.g. "201"). A wrong step resets the sequence with a buzz.
- BP_FloorGenerator: a dead generator; walking up restarts it and powers that floor's lift.
Run once after the BPs compile-safe (no Fab import in progress)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
F = '/Game/HollowKin/Blueprints/Floors'
LIFT, CARD, SW, GEN = F + '/BP_FloorLift.BP_FloorLift', F + '/BP_Keycard.BP_Keycard', F + '/BP_SeqSwitch.BP_SeqSwitch', F + '/BP_FloorGenerator.BP_FloorGenerator'
LOADING = '/Game/HollowKin/UI/Menus/WBP_Loading.WBP_Loading_C'
def mk(path, vars_):
    if not call(A, 'exists', {'path': path.split('.')[0]}).get('returnValue'):
        print(call(BT, 'create', {'folder_path': F, 'asset_name': path.split('.')[-1], 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
    have = call(BT, 'list_variables', {'blueprint': {'refPath': path}}).get('returnValue') or []
    for n, t in vars_:
        if n in have: continue
        call(BT, 'add_variable', {'blueprint': {'refPath': path}, 'name': n, 'type_name': t})
        call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': path}, 'variable_name': n, 'instance_editable': True})
    call(BT, 'compile_blueprint', {'blueprint': {'refPath': path}, 'warnings_as_errors': False})
def fn(bp, name, dsl, params=()):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt, inp in params:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': inp})
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': bp + ':' + name}, 'code': dsl})
    print(bp.split('.')[-1], name, 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def ev(bp, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': bp + ':EventGraph'}, 'code': dsl})
    print(bp.split('.')[-1], 'EventGraph', 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
MAXCAST = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'

mk(LIFT, [('Label', 'string'), ('Gate', 'int'), ('bUnlocked', 'bool'), ('Target', 'vector'), ('NextLabel', 'string'), ('NextName', 'string'),
          ('NextLevel', 'string'), ('bBusy', 'bool'), ('NextNag', 'float'), ('Progress', 'int'), ('Code', 'string')])
mk(CARD, [('Label', 'string'), ('bTaken', 'bool')])
mk(SW, [('Label', 'string'), ('Idx', 'int'), ('bLit', 'bool'), ('Cool', 'float')])
mk(GEN, [('Label', 'string'), ('bDone', 'bool')])
for bp in (SW, GEN):
    have = call(BT, 'list_variables', {'blueprint': {'refPath': bp}}).get('returnValue') or []
    if 'Lamp' not in have:
        print(call(BT, 'add_object_variable', {'blueprint': {'refPath': bp}, 'name': 'Lamp', 'object_class': {'refPath': '/Script/Engine.PointLightComponent'}}))
    call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False})

# ---------------- lift ----------------
fn(LIFT, 'PowerLift', '''(fn PowerLift ()
  (if (not (Variables|Default|GetUnlocked))
    (Variables|Default|SetUnlocked true)
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Special_Powerup_03.Special_Powerup_03" 0.6)
    (bind m %s
      (:then
        (Class|BPMax|Notify :self m :Msg "THE LIFT IS LIVE.  Get to the lift room at the east end of the corridor." :Seconds 4.0)
        (Class|BPMax|SetObjectiveNote :self m :Msg "The lift is working. Take it down."))
      (:CastFailed))))''' % MAXCAST)
fn(LIFT, 'SeqHit', '''(fn SeqHit (Idx)
  (bind want (Utilities|String|GetSubstring :SourceString (Variables|Default|GetCode) :StartIndex (Variables|Default|GetProgress) :Length 1))
  (if (Utilities|String|EqualExactly(String) want (Utilities|String|ToString(Integer) Idx))
    (Variables|Default|SetProgress (+ (Variables|Default|GetProgress) 1))
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_03.Flick_Switch_03" 0.8)
    (if (>= (Variables|Default|GetProgress) 3) (CallFunction|PowerLift))
    (return true)
    (else
      (Variables|Default|SetProgress 0)
      (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Error_Buzz_02.Error_Buzz_02" 0.7)
      (for s (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_SeqSwitch.BP_SeqSwitch_C")
        (bind sw (Utilities|Casting|CastToBP_SeqSwitch s))
        (if (Utilities|String|EqualExactly(String) (Class|BPSeqSwitch|GetLabel :self sw) (Variables|Default|GetLabel))
          (Class|BPSeqSwitch|SetLit :self sw :On false)))
      (return false))))''', params=[('Idx', 'int', True), ('Ok', 'bool', False)])
fn(LIFT, 'GoDown', '''(fn GoDown ()
  (Variables|Default|SetBusy true)
  (CameraFades|StartCameraFade :self (Game|GetPlayerCameraManager 0) :FromAlpha 0.0 :ToAlpha 1.0 :Duration 0.8 :bHoldWhenFinished true)
  (Audio|PlaySound2D "/Game/HorrorAmbientSFX/HorrorAmbientSFX_cue/AMB_Drone_Server_Cue.AMB_Drone_Server_Cue" 0.5)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Arrive" :Time 1.2 :bLooping false))''')
fn(LIFT, 'Arrive', '''(fn Arrive ()
  (bind m %s
    (:then
      (if (not (Utilities|String|EqualExactly(String) (Variables|Default|GetNextLevel) ""))
        (Class|BPMax|StoreCarry :self m)
        (Game|OpenLevel(byName) :LevelName (Utilities|String|StringToName (Variables|Default|GetNextLevel)))
        (else
          (Transformation|SetActorLocation :self m :NewLocation (Variables|Default|GetTarget) :bSweep false :bTeleport true)
          (bind card (Utilities|Casting|CastToWBP_Loading (UserInterface|CreateWidget "%s" (Game|GetPlayerController 0))))
          (Class|WBPLoading|SetupCard :self card :Chapter (Variables|Default|GetNextLabel) :TitleText (Variables|Default|GetNextName) :BodyText "The cage shudders to a stop. The air is colder down here.")
          (UserInterface|Viewport|AddToViewport card 90)
          (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "FadeIn" :Time 3.5 :bLooping false)
          (Class|BPMax|SetObjectiveNote :self m :Msg (Utilities|String|Append (Variables|Default|GetNextLabel) ": find a way to power the next lift."))
          (Class|BPMax|SaveCheckpoint :self m))))
    (:CastFailed)))''' % (MAXCAST, LOADING))
fn(LIFT, 'FadeIn', '''(fn FadeIn ()
  (for w (Widget|GetAllWidgetsOfClass :WidgetClass "%s" :TopLevelOnly true)
    (Widget|RemovefromParent w))
  (CameraFades|StartCameraFade :self (Game|GetPlayerCameraManager 0) :FromAlpha 1.0 :ToAlpha 0.0 :Duration 1.2 :bHoldWhenFinished false)
  (Variables|Default|SetBusy false))''' % LOADING)
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
              (Class|BPMax|Notify :self m :Msg (select (== (Variables|Default|GetGate) 1) "LIFT LOCKED.  It needs this floor's KEYCARD." (select (== (Variables|Default|GetGate) 2) "LIFT LOCKED.  Three floor switches must be pressed in the right order. Somebody wrote the order down." "NO POWER.  Restart this floor's generator.")) :Seconds 4.0))))))
    (:CastFailed)))''' % MAXCAST)
call(BT, 'compile_blueprint', {'blueprint': {'refPath': LIFT}, 'warnings_as_errors': False})

# ---------------- keycard ----------------
ev(CARD, '''(event EventBeginPlay
  (bind c (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent")))
  (Components|StaticMesh|SetStaticMesh c "/Game/LevelPrototyping/Meshes/SM_Cube.SM_Cube")
  (Transformation|SetRelativeScale3D :self c :NewScale3D (Math|Vector|MakeVector 0.09 0.055 0.006))
  (Collision|SetCollisionEnabled :self c :NewType "NoCollision")
  (bind l (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "/Script/Engine.PointLightComponent")))
  (Rendering|Components|Light|SetIntensity :self l :NewIntensity 120.0)
  (Rendering|Components|Light|SetLightColor :self l :NewLightColor (Math|Color|MakeColor 1.0 0.25 0.2 1.0))
  (Rendering|Lighting|SetAttenuationRadius :self l :NewRadius 160.0))''')
ev(CARD, '''(event EventTick (DeltaSeconds)
  (Transformation|AddActorWorldRotation :self self :DeltaRotation (Math|Rotator|MakeRotator 0.0 0.0 (* DeltaSeconds 60.0)))
  (bind m %s
    (:then
      (if (and (not (Variables|Default|GetTaken)) (< (Transformation|GetDistanceTo self m) 120.0))
        (Variables|Default|SetTaken true)
        (Class|BPMax|Notify :self m :Msg (Utilities|String|Append (Utilities|String|Append "KEYCARD  " (Variables|Default|GetLabel)) "  -  the lift will accept it.") :Seconds 3.5)
        (for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_FloorLift.BP_FloorLift_C")
          (bind lf (Utilities|Casting|CastToBP_FloorLift x))
          (if (Utilities|String|EqualExactly(String) (Class|BPFloorLift|GetLabel :self lf) (Variables|Default|GetLabel))
            (Class|BPFloorLift|PowerLift :self lf)))
        (Actor|DestroyActor :self self)))
    (:CastFailed)))''' % MAXCAST)

# ---------------- switch ----------------
fn(SW, 'SetLit', '''(fn SetLit (On)
  (Variables|Default|SetLit On)
  (Rendering|Components|Light|SetLightColor :self (Variables|Default|GetLamp) :NewLightColor (select On (Math|Color|MakeColor 0.2 1.0 0.4 1.0) (Math|Color|MakeColor 1.0 0.15 0.1 1.0))))''', params=[('On', 'bool', True)])
ev(SW, '''(event EventBeginPlay
  (bind c (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent")))
  (Components|StaticMesh|SetStaticMesh c "/Game/LevelPrototyping/Meshes/SM_Cylinder.SM_Cylinder")
  (Transformation|SetRelativeScale3D :self c :NewScale3D (Math|Vector|MakeVector 0.7 0.7 0.05))
  (Collision|SetCollisionEnabled :self c :NewType "NoCollision")
  (bind t (Utilities|Casting|CastToTextRenderComponent (Game|AddComponentbyClass self "/Script/Engine.TextRenderComponent")))
  (Rendering|Components|TextRender|SetText :self t :Value (select (== (Variables|Default|GetIdx) 0) "I" (select (== (Variables|Default|GetIdx) 1) "II" "III")))
  (Rendering|Components|TextRender|SetWorldSize :self t :Value 40.0)
  (Transformation|SetRelativeLocation :self t :NewLocation (Math|Vector|MakeVector 0.0 0.0 6.0))
  (Transformation|SetRelativeRotation :self t :NewRotation (Math|Rotator|MakeRotator 90.0 0.0 0.0))
  (bind l (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "/Script/Engine.PointLightComponent")))
  (Transformation|SetRelativeLocation :self l :NewLocation (Math|Vector|MakeVector 0.0 0.0 40.0))
  (Rendering|Components|Light|SetIntensity :self l :NewIntensity 80.0)
  (Rendering|Lighting|SetAttenuationRadius :self l :NewRadius 180.0)
  (Variables|Default|SetLamp l)
  (CallFunction|SetLit :On false))''')
ev(SW, '''(event EventTick (DeltaSeconds)
  (bind m %s
    (:then
      (bind now (Utilities|Time|GetTimeSeconds))
      (if (and (and (not (Variables|Default|GetLit)) (> now (Variables|Default|GetCool))) (< (Transformation|GetDistanceTo self m) 150.0))
        (Variables|Default|SetCool (+ now 1.5))
        (for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_FloorLift.BP_FloorLift_C")
          (bind lf (Utilities|Casting|CastToBP_FloorLift x))
          (if (Utilities|String|EqualExactly(String) (Class|BPFloorLift|GetLabel :self lf) (Variables|Default|GetLabel))
            (bind ok (Class|BPFloorLift|SeqHit :self lf :Idx (Variables|Default|GetIdx)))
            (if ok (CallFunction|SetLit :On true))))))
    (:CastFailed)))''' % MAXCAST)

# ---------------- generator ----------------
ev(GEN, '''(event EventBeginPlay
  (bind c (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent")))
  (Components|StaticMesh|SetStaticMesh c "/Game/Horror_Hospital/Meshes/SM_Generator_01_v01.SM_Generator_01_v01")
  (bind l (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "/Script/Engine.PointLightComponent")))
  (Transformation|SetRelativeLocation :self l :NewLocation (Math|Vector|MakeVector 0.0 0.0 120.0))
  (Rendering|Components|Light|SetIntensity :self l :NewIntensity 60.0)
  (Rendering|Components|Light|SetLightColor :self l :NewLightColor (Math|Color|MakeColor 1.0 0.35 0.1 1.0))
  (Rendering|Lighting|SetAttenuationRadius :self l :NewRadius 260.0)
  (Variables|Default|SetLamp l))''')
ev(GEN, '''(event EventTick (DeltaSeconds)
  (bind m %s
    (:then
      (if (and (not (Variables|Default|GetDone)) (< (Transformation|GetDistanceTo self m) 280.0))
        (Variables|Default|SetDone true)
        (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_01.Flick_Switch_01" 0.9)
        (Rendering|Components|Light|SetLightColor :self (Variables|Default|GetLamp) :NewLightColor (Math|Color|MakeColor 0.3 1.0 0.5 1.0))
        (Class|BPMax|Notify :self m :Msg "The generator coughs, then roars.  Power returns to the lift." :Seconds 3.5)
        (for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_FloorLift.BP_FloorLift_C")
          (bind lf (Utilities|Casting|CastToBP_FloorLift x))
          (if (Utilities|String|EqualExactly(String) (Class|BPFloorLift|GetLabel :self lf) (Variables|Default|GetLabel))
            (Class|BPFloorLift|PowerLift :self lf)))))
    (:CastFailed)))''' % MAXCAST)
for bp in (LIFT, CARD, SW, GEN):
    print(bp.split('.')[-1], call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
