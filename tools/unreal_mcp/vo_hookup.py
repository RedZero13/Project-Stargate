"""Voice lines (Kokoro, tools/voice/lines.py -> /Game/HollowKin/Audio/VO/VO_<id>) wired into the game:
- BP_Cutscene: Voice1..Voice3 (Sound) play with Line1..Line3.
- Cutscene actors get their voices set (place_cutscenes.py / place_floors.py also set them on re-runs).
Run after the VO wavs are imported."""
import json
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
S = 'editor_toolset.toolsets.scene.SceneTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
CS = '/Game/HollowKin/Blueprints/Interactables/BP_Cutscene.BP_Cutscene'
MAXC = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'
VO = lambda i: {'refPath': '/Game/HollowKin/Audio/VO/VO_%s.VO_%s' % (i, i)}
have = call(BT, 'list_variables', {'blueprint': {'refPath': CS}}).get('returnValue') or []
for n in ('Voice1', 'Voice2', 'Voice3'):
    if n not in have:
        call(BT, 'add_object_variable', {'blueprint': {'refPath': CS}, 'name': n, 'object_class': {'refPath': '/Script/Engine.SoundBase'}})
        call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': CS}, 'variable_name': n, 'instance_editable': True})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': CS}, 'warnings_as_errors': False})
def play(n):
    return '(Utilities|IsValid (Variables|Default|GetVoice%d) (:"Is Valid" (Audio|PlaySound2D :Sound (Variables|Default|GetVoice%d) :VolumeMultiplier 1.0)))' % (n, n)
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': CS + ':StepScene'}, 'code': '''(fn StepScene ()
  (Variables|Default|SetStep (+ (Variables|Default|GetStep) 1))
  (bind st (Variables|Default|GetStep))
  (bind msg (select (== st 1) (Variables|Default|GetLine1) (select (== st 2) (Variables|Default|GetLine2) (Variables|Default|GetLine3))))
  (bind m %s
    (:then
      (if (<= st 3)
        (if (not (Utilities|String|EqualExactly(String) msg ""))
          (Class|BPMax|ShowNote :self m :Msg msg :Seconds (- (Variables|Default|GetHold) 0.2))
          (if (== st 1) %s)
          (if (== st 2) %s)
          (if (== st 3) %s)
          (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "StepScene" :Time (Variables|Default|GetHold) :bLooping false)
          (else (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "StepScene" :Time 0.05 :bLooping false)))
        (elif (== st 4)
          (Game|Player|SetViewTargetwithBlend :self (Game|GetPlayerController 0) :NewViewTarget m :BlendTime 1.0)
          (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "StepScene" :Time 1.0 :bLooping false)
          (else
            (Input|EnableInput :self m :PlayerController (Game|GetPlayerController 0))
            (Class|BPMax|HKLog :self m :Msg "CUTSCENE end")
            (Class|BPMax|SetDmgMul :self m :DmgMul (Variables|Default|GetSavedMul))
            (if (not (Utilities|String|EqualExactly(String) (Variables|Default|GetObjective) ""))
              (Class|BPMax|SetObjectiveNote :self m :Msg (Variables|Default|GetObjective)))
            (Actor|DestroyActor :self (Variables|Default|GetCam))))))
    (:CastFailed)))''' % (MAXC, play(1), play(2), play(3))})
print('StepScene', r)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': CS}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
