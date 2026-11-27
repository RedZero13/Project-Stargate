"""Volume settings: BP_SettingsSave gets MasterVol/MusicVol/SfxVol (0-100) and ApplyVolumes(Ctx), which writes
Music and SFX sound-class volumes into the SM_HKVolume sound mix and pushes it. Effects default class = engine SFX,
music loops are put in the engine Music class (see DefaultEngine.ini + set_music_class below)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
S = '/Game/HollowKin/Blueprints/Systems/BP_SettingsSave.BP_SettingsSave'
MIX = '/Game/HollowKin/Audio/SM_HKVolume.SM_HKVolume'
DSL = '''(fn ApplyVolumes (Ctx)
  (Audio|SetSoundMixClassOverride :WorldContextObject Ctx :InSoundMixModifier "%(mix)s" :InSoundClass "/Engine/EngineSounds/Music.Music"
     :Volume (* (/ (Variables|Default|GetMasterVol) 100.0) (/ (Variables|Default|GetMusicVol) 100.0)) :Pitch 1.0 :FadeInTime 0.0 :bApplyToChildren true)
  (Audio|SetSoundMixClassOverride :WorldContextObject Ctx :InSoundMixModifier "%(mix)s" :InSoundClass "/Engine/EngineSounds/SFX.SFX"
     :Volume (* (/ (Variables|Default|GetMasterVol) 100.0) (/ (Variables|Default|GetSfxVol) 100.0)) :Pitch 1.0 :FadeInTime 0.0 :bApplyToChildren true)
  (Audio|PushSoundMixModifier :WorldContextObject Ctx :InSoundMixModifier "%(mix)s"))''' % {'mix': MIX}
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': S + ':ApplyVolumes'}, 'code': DSL}))
