"""BP_Max.ApplyMaxSettings (renamed from ApplySettings, which clashed with GameUserSettings.ApplySettings): difficulty multipliers, overlay HUD, reduce flashing, motion blur, look prefs."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
dsl = '''(fn ApplyMaxSettings ()
  (Variables|Default|SetDmgMul 1.0)
  (Variables|Default|SetDrainMul 1.0)
  (Variables|Default|SetLootMul 1.0)
  (CallFunction|ApplyInputPrefs)
  (bind s (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then
      (Variables|Default|SetShowOverlayHUD (Class|BPSettingsSave|GetOverlayHUD :self s))
      (Variables|Default|SetReduceFlash (Class|BPSettingsSave|GetReduceFlash :self s))
      (if (Class|BPSettingsSave|GetNoMotionBlur :self s)
        (Development|ExecuteConsoleCommand "r.MotionBlurQuality 0")
        (else (Development|ExecuteConsoleCommand "r.MotionBlurQuality 4")))
      (if (== (Class|BPSettingsSave|GetDifficulty :self s) 0)
        (Variables|Default|SetDmgMul 0.5)
        (Variables|Default|SetDrainMul 0.5)
        (Variables|Default|SetLootMul 1.5))
      (if (== (Class|BPSettingsSave|GetDifficulty :self s) 2)
        (Variables|Default|SetDmgMul 1.5)
        (Variables|Default|SetDrainMul 1.4)
        (Variables|Default|SetLootMul 0.7))
      (if (== (Class|BPSettingsSave|GetDifficulty :self s) 3)
        (Variables|Default|SetDmgMul 2.0)
        (Variables|Default|SetDrainMul 1.8)
        (Variables|Default|SetLootMul 0.5)))
    (:CastFailed)))'''
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':ApplyMaxSettings'}, 'code': dsl}))
