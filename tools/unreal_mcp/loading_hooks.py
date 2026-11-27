"""Uses WBP_Loading: PROLOGUE card on NEW ADMISSION (WBP_Difficulty.StartRun -> GoCity after 6.5 s) and a
CHAPTER 1 card at the clinic door (BP_LevelDoor; chapter label/title/tip are instance-editable variables)."""
from ui_lib import call
import json
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
O = 'editor_toolset.toolsets.object.ObjectTools'
L = '/Game/HollowKin/UI/Menus/WBP_Loading.WBP_Loading_C'
DIF = '/Game/HollowKin/UI/Menus/WBP_Difficulty.WBP_Difficulty'
DOOR = '/Game/HollowKin/Blueprints/Interactables/BP_LevelDoor.BP_LevelDoor'
PRO = ("Six days ago a letter reached Max Hunt: his little sister Emilia, taken into state care when she was six, "
       "never arrived at her foster home. Nobody will say where she went. Tonight, in the rain, someone finally calls.")
call(BT, 'add_function_graph', {'blueprint': {'refPath': DIF}, 'graph_name': 'GoCity'})
print('GoCity', call(BT, 'write_graph_dsl', {'graph': {'refPath': DIF + ':GoCity'}, 'code': '''(fn GoCity ()
  (Game|OpenLevel(byName) "/Game/HollowKin/Maps/City/Lvl_City"))'''}))
print('StartRun', call(BT, 'write_graph_dsl', {'graph': {'refPath': DIF + ':StartRun'}, 'code': '''(fn StartRun ()
  (bind pc (Game|GetPlayerController 0))
  (SaveGame|DeleteGameInSlot "HollowKinSlot1" 0)
  (Input|SetInputModeGameOnly pc false)
  (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor false)
  (bind card (Utilities|Casting|CastToWBP_Loading (UserInterface|CreateWidget "%s" pc)))
  (Class|WBPLoading|SetupCard :self card :Chapter "PROLOGUE" :TitleText "MILLBROOK" :BodyText "%s" :TipText "TIP:  Hold right mouse, or press T, to aim. Every bullet counts." :Seconds 6.5)
  (UserInterface|Viewport|AddToViewport card 90)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "GoCity" :Time 6.5 :bLooping false))''' % (L, PRO)}))
for n in ('ChapterLabel', 'ChapterTitle', 'Tip'):
    call(BT, 'add_variable', {'blueprint': {'refPath': DOOR}, 'name': n, 'type_name': 'string'})
    call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': DOOR}, 'name': n, 'instance_editable': True})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': DOOR}, 'warnings_as_errors': False})
cdo = call(BT, 'get_default_object', {'blueprint': {'refPath': DOOR}})['returnValue']
print(call(O, 'set_properties', {'instance': cdo, 'values': json.dumps({'ChapterLabel': 'CHAPTER 1', 'ChapterTitle': "ST. BRIGID'S CLINIC",
      'Tip': 'TIP:  Your flashlight keeps your mind steady, but light carries. Switch it off to slip past what you cannot fight.'})}))
print('Door', call(BT, 'write_graph_dsl', {'graph': {'refPath': DOOR + ':EventGraph'}, 'code': '''(event Collision|EventActorBeginOverlap (OtherActor)
  (bind m (Utilities|Casting|CastToBP_Max OtherActor)
    (:then
      (if (not (Variables|Default|GetShown))
        (Variables|Default|SetShown true)
        (Input|DisableInput :self m :PlayerController (Game|GetPlayerController 0))
        (Audio|SpawnSound2D "/Game/Interface_And_Item_Sounds/WAV/Futuristic_Click_04.Futuristic_Click_04" 0.8 0.5)
        (CameraFades|StartCameraFade :self (Game|GetPlayerCameraManager 0) :FromAlpha 0.0 :ToAlpha 1.0 :Duration 1.2 :bHoldWhenFinished true)
        (Utilities|FlowControl|Delay 1.2)
        (bind card (Utilities|Casting|CastToWBP_Loading (UserInterface|CreateWidget "%s" (Game|GetPlayerController 0))))
        (Class|WBPLoading|SetupCard :self card :Chapter (Variables|Default|GetChapterLabel) :TitleText (Variables|Default|GetChapterTitle) :BodyText (Variables|Default|GetMessage) :TipText (Variables|Default|GetTip) :Seconds 6.5)
        (UserInterface|Viewport|AddToViewport card 90)
        (Utilities|FlowControl|Delay 6.5)
        (Game|OpenLevel(byName) (Variables|Default|GetTargetLevel))))
    (:CastFailed)))''' % L}))
for bp in (DIF, DOOR):
    print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': True}))
