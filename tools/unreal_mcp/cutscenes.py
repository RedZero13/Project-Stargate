"""BP_Cutscene: a one-shot camera vignette (like the gun pickup). When Max comes within Radius: controls lock, the
view blends to a camera at (actor + CamOffset) looking at (actor + LookOffset), Line1..Line3 play as subtitles
(Hold seconds each), then the view blends back and controls return. Placed by place_cutscenes.py."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
CS = '/Game/HollowKin/Blueprints/Interactables/BP_Cutscene.BP_Cutscene'
if not call(A, 'exists', {'path': CS.split('.')[0]}).get('returnValue'):
    print(call(BT, 'create', {'folder_path': '/Game/HollowKin/Blueprints/Interactables', 'asset_name': 'BP_Cutscene', 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
have = call(BT, 'list_variables', {'blueprint': {'refPath': CS}}).get('returnValue') or []
for n, t in (('Line1', 'string'), ('Line2', 'string'), ('Line3', 'string'), ('Objective', 'string'), ('CamOffset', 'vector'), ('LookOffset', 'vector'),
             ('Radius', 'float'), ('Hold', 'float'), ('bDone', 'bool')):
    if n not in have:
        call(BT, 'add_variable', {'blueprint': {'refPath': CS}, 'name': n, 'type_name': t})
    call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': CS}, 'variable_name': n, 'instance_editable': True})
if 'Cam' not in have:
    call(BT, 'add_object_variable', {'blueprint': {'refPath': CS}, 'name': 'Cam', 'object_class': {'refPath': '/Script/Engine.CameraActor'}})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': CS}, 'warnings_as_errors': False})
if 'Step' not in have:
    call(BT, 'add_variable', {'blueprint': {'refPath': CS}, 'name': 'Step', 'type_name': 'int'})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': CS}, 'warnings_as_errors': False})
MAXC = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'
call(BT, 'add_function_graph', {'blueprint': {'refPath': CS}, 'graph_name': 'StepScene'})
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': CS + ':StepScene'}, 'code': '''(fn StepScene ()
  (Variables|Default|SetStep (+ (Variables|Default|GetStep) 1))
  (bind st (Variables|Default|GetStep))
  (bind msg (select (== st 1) (Variables|Default|GetLine1) (select (== st 2) (Variables|Default|GetLine2) (Variables|Default|GetLine3))))
  (bind m %s
    (:then
      (if (<= st 3)
        (if (not (Utilities|String|EqualExactly(String) msg ""))
          (Class|BPMax|ShowNote :self m :Msg msg :Seconds (- (Variables|Default|GetHold) 0.2))
          (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "StepScene" :Time (Variables|Default|GetHold) :bLooping false)
          (else (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "StepScene" :Time 0.05 :bLooping false)))
        (elif (== st 4)
          (Game|Player|SetViewTargetwithBlend :self (Game|GetPlayerController 0) :NewViewTarget m :BlendTime 1.0)
          (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "StepScene" :Time 1.0 :bLooping false)
          (else
            (Input|EnableInput :self m :PlayerController (Game|GetPlayerController 0))
            (if (not (Utilities|String|EqualExactly(String) (Variables|Default|GetObjective) ""))
              (Class|BPMax|SetObjectiveNote :self m :Msg (Variables|Default|GetObjective)))
            (Actor|DestroyActor :self (Variables|Default|GetCam))))))
    (:CastFailed)))''' % MAXC})
print('StepScene', r)
dsl = '''(event EventTick (DeltaSeconds)
  (bind m %s
    (:then
      (if (and (and (not (Variables|Default|GetDone)) (> (Utilities|Time|GetGameTimeinSeconds) 2.5)) (< (Transformation|GetDistanceTo self m) (Variables|Default|GetRadius)))
        (Variables|Default|SetDone true)
        (Variables|Default|SetStep 0)
        (bind pc (Game|GetPlayerController 0))
        (Input|DisableInput :self m :PlayerController pc)
        (bind camloc (+ (Transformation|GetActorLocation self) (Variables|Default|GetCamOffset)))
        (bind look (+ (Transformation|GetActorLocation self) (Variables|Default|GetLookOffset)))
        (Variables|Default|SetCam (Utilities|Casting|CastToCameraActor (Game|SpawnActorfromClass :Class "/Script/Engine.CameraActor" :SpawnTransform (Math|Transform|MakeTransform camloc (Math|Rotator|FindLookatRotation camloc look)) :CollisionHandlingOverride "AlwaysSpawn")))
        (Game|Player|SetViewTargetwithBlend :self pc :NewViewTarget (Variables|Default|GetCam) :BlendTime 1.2)
        (Audio|PlaySound2D "/Game/HorrorAmbientSFX/HorrorAmbientSFX_cue/AMB_Drone_Beneath_Cue.AMB_Drone_Beneath_Cue" 0.5)
        (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "StepScene" :Time 1.3 :bLooping false)))
    (:CastFailed)))''' % MAXC
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': CS + ':EventGraph'}, 'code': dsl})
print('Cutscene tick', r)
cdo = call(BT, 'get_default_object', {'blueprint': {'refPath': CS}})['returnValue']
import json
print(call('editor_toolset.toolsets.object.ObjectTools', 'set_properties', {'instance': cdo, 'values': json.dumps({'Radius': 260.0, 'Hold': 4.5})}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': CS}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
