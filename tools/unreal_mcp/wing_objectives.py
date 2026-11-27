"""Containment Wing objectives: BP_Max.RefreshObjective picks the line from fuses/power state;
called when the wing starts (BP_SliceGameMode), when anything is picked up, and at the breaker."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
def w(g, dsl):
    print(g.split(':')[-1], call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}))
call(BT, 'add_function_graph', {'blueprint': {'refPath': MAX}, 'graph_name': 'RefreshObjective'})
w(MAX + ':RefreshObjective', '''(fn RefreshObjective ()
  (if (Variables|Default|GetPowerOn)
    (CallFunction|SetObjectiveNote :Msg "Power is back. Go through the open blast door at the end of the wing to Emilia's room (L-03).")
    (elif (>= (Variables|Default|GetFuses) 2)
      (CallFunction|SetObjectiveNote :Msg "You have both fuses. Take them to the breaker panel (red glow) in the dark corridor.")
      (elif (>= (Variables|Default|GetFuses) 1)
        (CallFunction|SetObjectiveNote :Msg "One fuse found. Find the second: one is in Cell Block A, one in the Children's Dorm.")
        (else
          (CallFunction|SetObjectiveNote :Msg "Restore power to reach Emilia. Find two fuses: one in Cell Block A, one in the Children's Dorm."))))))''')
w('/Game/HollowKin/Blueprints/Items/BP_Pickup.BP_Pickup:OnTaken', '''(fn OnTaken (Who)
  (bind m (Utilities|Casting|CastToBP_Max Who))
  (Class|BPMax|Collect m (Variables|Default|GetPickupKind) (Variables|Default|GetAmount))
  (Audio|SpawnSound2D "/Game/Interface_And_Item_Sounds/WAV/Special_Powerup_03.Special_Powerup_03" 0.6)
  (if (== (Utilities|String|Contains (Game|GetCurrentLevelName true) "Containment") true)
    (Class|BPMax|RefreshObjective m))
  (Actor|DestroyActor self))''')
w('/Game/HollowKin/Blueprints/Interactables/BP_BreakerPanel.BP_BreakerPanel:BreakerTouched', '''(fn BreakerTouched (Who)
  (bind m (Utilities|Casting|CastToBP_Max Who))
  (if (not (Class|BPMax|GetPowerOn :self m))
    (if (>= (Class|BPMax|GetFuses :self m) 2)
      (Class|BPMax|SetPowerOn :self m :bPowerOn true)
      (Audio|SpawnSound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_03.Flick_Switch_03" 0.9)
      (Class|BPMax|ShowNote m "POWER RESTORED. The door to Emilia's room (L-03) is open." 6.0)
      (Class|BPMax|RefreshObjective m)
      (else
        (Audio|SpawnSound2D "/Game/Interface_And_Item_Sounds/WAV/Error_Buzz_02.Error_Buzz_02" 0.7)
        (Class|BPMax|ShowNote m "The breaker is dead. It needs two fuses: one in Cell Block A, one in the Children's Dorm." 6.0)
        (Class|BPMax|RefreshObjective m)))))''')
# Wing start: the HUD widget (created by BP_Max in every level) runs WingIntro 1.5 s after it opens.
SFX = '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX'
call(BT, 'add_function_graph', {'blueprint': {'refPath': SFX}, 'graph_name': 'WingIntro'})
w(SFX + ':WingIntro', '''(fn WingIntro ()
  (if (Utilities|String|Contains (Game|GetCurrentLevelName true) "Containment")
    (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
      (:then
        (Class|BPMax|ShowNote :self m :Msg "ST. BRIGID'S  //  SUB-LEVEL 2  //  CONTAINMENT WING.   The service lift brought you down. Somewhere below: Emilia." :Seconds 7.0)
        (Class|BPMax|RefreshObjective :self m))
      (:CastFailed))))''')
w(SFX + ':ApplySavedVolumes', '''(fn ApplySavedVolumes ()
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "WingIntro" :Time 1.5 :bLooping false)
  (bind s (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then (Class|BPSettingsSave|ApplyVolumes :self s :Ctx self))
    (:CastFailed)))''')
for bp in [MAX, '/Game/HollowKin/Blueprints/Items/BP_Pickup.BP_Pickup', '/Game/HollowKin/Blueprints/Interactables/BP_BreakerPanel.BP_BreakerPanel', SFX]:
    print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': True}))
