"""BP_LevelDoor: instead of a hard cut, freeze the player, fade to black, show the door's Message as an
arrival card, then load TargetLevel."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
B = '/Game/HollowKin/Blueprints/Interactables/BP_LevelDoor.BP_LevelDoor'
DSL = '''(event Collision|EventActorBeginOverlap (OtherActor)
  (bind m (Utilities|Casting|CastToBP_Max OtherActor)
    (:then
      (if (not (Variables|Default|GetShown))
        (Variables|Default|SetShown true)
        (Input|DisableInput :self m :PlayerController (Game|GetPlayerController 0))
        (Audio|SpawnSound2D "/Game/Interface_And_Item_Sounds/WAV/Futuristic_Click_04.Futuristic_Click_04" 0.8 0.5)
        (CameraFades|StartCameraFade :self (Game|GetPlayerCameraManager 0) :FromAlpha 0.0 :ToAlpha 1.0 :Duration 1.5 :bHoldWhenFinished true)
        (Class|BPMax|ShowNote :self m :Msg (Variables|Default|GetMessage) :Seconds 7.0)
        (Utilities|FlowControl|Delay 5.5)
        (Game|OpenLevel(byName) (Variables|Default|GetTargetLevel))))
    (:CastFailed)))'''
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': B + ':EventGraph'}, 'code': DSL}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': B}, 'warnings_as_errors': True}))
