"""Mouse/gamepad sensitivity (50/75/100/125/150 %) + invert Y. BP_SettingsSave.LookSens (default 100), bInvertY.
BP_Max.ApplyInputPrefs swaps in one of the prebuilt contexts /Game/HollowKin/Input/Look/IMC_Look_<pct>[_Inv]
(build_look_imcs.py) at priority 5, above the sample's IMC_Sandbox. Called from EnsureCombatInput's ApplySettings."""
from ui_lib import call
import json
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
S = '/Game/HollowKin/Blueprints/Systems/BP_SettingsSave.BP_SettingsSave'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
D = '/Game/HollowKin/Input/Look/'
for n, t in [('LookSens', 'int'), ('bInvertY', 'bool'), ('bNoMotionBlur', 'bool'), ('bLargeText', 'bool')]:
    call(BT, 'add_variable', {'blueprint': {'refPath': S}, 'name': n, 'type_name': t})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': S}, 'warnings_as_errors': False})
cdo = call(BT, 'get_default_object', {'blueprint': {'refPath': S}})['returnValue']
call('editor_toolset.toolsets.object.ObjectTools', 'set_properties', {'instance': cdo, 'values': json.dumps({'LookSens': 100})})
OPT = "(bIgnoreAllPressedKeysUntilRelease=False,bForceImmediately=True,bNotifyUserSettings=False)"
def imc(p, inv): n = 'IMC_Look_%d%s' % (p, '_Inv' if inv else ''); return '"%s%s.%s"' % (D, n, n)
removes = '\n      '.join('(Input|RemoveMappingContext sub %s "%s")' % (imc(p, i), OPT) for p in (50, 75, 100, 125, 150) for i in (False, True))
def add(p): return '(if inv (Input|AddMappingContext sub %s 5 "%s") (else (Input|AddMappingContext sub %s 5 "%s")))' % (imc(p, True), OPT, imc(p, False), OPT)
DSL = '''(fn ApplyInputPrefs ()
  (bind pc (Utilities|Casting|CastToPlayerController (Pawn|GetController)))
  (bind sub (PlayerController|LocalPlayerSubsystems|GetEnhancedInputLocalPlayerSubsystem pc))
  (bind s (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then
      %(removes)s
      (bind sens (Class|BPSettingsSave|GetLookSens :self s))
      (bind inv (Class|BPSettingsSave|GetInvertY :self s))
      (if (<= sens 60) %(a50)s
        (elif (<= sens 85) %(a75)s
          (elif (<= sens 110) %(a100)s
            (elif (<= sens 135) %(a125)s
              (else %(a150)s))))))
    (:CastFailed
      (Input|AddMappingContext sub %(def)s 5 "%(opt)s"))))''' % {
    'removes': removes, 'a50': add(50), 'a75': add(75), 'a100': add(100), 'a125': add(125), 'a150': add(150),
    'def': imc(100, False), 'opt': OPT}
call(BT, 'add_function_graph', {'blueprint': {'refPath': MAX}, 'graph_name': 'ApplyInputPrefs'})
print('ApplyInputPrefs', call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':ApplyInputPrefs'}, 'code': DSL}))
