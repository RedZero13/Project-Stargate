"""Links the Containment Wing to the Deep Labs and carries progress between levels.
- BP_HKGameInstance holds a carry snapshot (health, sanity, ammo, items, pistol, Bond, Taint).
- BP_Max.StoreCarry / RestoreCarry; EnsureCombatInput: look, ApplyMaxSettings, RestoreCarry, then LoadCheckpoint
  (a checkpoint saved in this level still wins).
- BP_EndingTrigger: in the Containment Wing it now takes Max down to the Deep Labs (CHAPTER 2 card) once power
  is on; in the Deep Labs (Emilia's chamber) it shows the ending.
- WBP_ScreenFX.WingIntro also introduces the Deep Labs and sets its objective."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
GI = '/Game/HollowKin/Blueprints/Systems/BP_HKGameInstance.BP_HKGameInstance'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
ET = '/Game/HollowKin/Blueprints/Interactables/BP_EndingTrigger.BP_EndingTrigger'
SFX = '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX'
L = '/Game/HollowKin/UI/Menus/WBP_Loading.WBP_Loading_C'
F = [('Health', 'float'), ('Sanity', 'float'), ('Bond', 'float'), ('Taint', 'float'),
     ('Ammo', 'int'), ('ReserveAmmo', 'int'), ('Gels', 'int'), ('Sedatives', 'int'), ('Bottles', 'int'), ('Parts', 'int'), ('Chem', 'int'), ('Tapes', 'int')]
for n, t in F + [('bCarry', 'bool'), ('bCarryPistol', 'bool')]:
    call(BT, 'add_variable', {'blueprint': {'refPath': GI}, 'name': 'C' + n if not n.startswith('b') else n, 'type_name': t})
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': GI}, 'warnings_as_errors': False}))
def fn(bp, name, dsl):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': bp + ':' + name}, 'code': dsl})
    print(name, 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
store = '\n      '.join('(Class|BPHKGameInstance|SetC%s :self gi :C%s (Variables|Default|Get%s))' % (n, n, n) for n, t in F)
restore = '\n        '.join('(Variables|Default|Set%s (Class|BPHKGameInstance|GetC%s :self gi))' % (n, n) for n, t in F)
fn(MAX, 'StoreCarry', '''(fn StoreCarry ()
  (bind gi (Utilities|Casting|CastToBP_HKGameInstance (Game|GetGameInstance))
    (:then
      %s
      (Class|BPHKGameInstance|SetCarryPistol :self gi :bCarryPistol (Variables|Default|GetHasPistol))
      (Class|BPHKGameInstance|SetCarry :self gi :bCarry true))
    (:CastFailed)))''' % store)
fn(MAX, 'RestoreCarry', '''(fn RestoreCarry ()
  (bind gi (Utilities|Casting|CastToBP_HKGameInstance (Game|GetGameInstance))
    (:then
      (if (Class|BPHKGameInstance|GetCarry :self gi)
        %s
        (Variables|Default|SetHasPistol (Class|BPHKGameInstance|GetCarryPistol :self gi))))
    (:CastFailed)))''' % restore)
fn(MAX, 'EnsureCombatInput', '''(fn EnsureCombatInput ()
  (if (not (Variables|Default|GetCombatInputReady))
    (bind pc (Utilities|Casting|CastToPlayerController (Pawn|GetController)))
    (Input|AddMappingContext (PlayerController|LocalPlayerSubsystems|GetEnhancedInputLocalPlayerSubsystem pc) "/Game/Input/IMC_Combat.IMC_Combat" 1 "(bIgnoreAllPressedKeysUntilRelease=True,bForceImmediately=False,bNotifyUserSettings=False)")
    (Variables|Default|SetCombatInputReady true)
    (CallFunction|ApplyMaxLook)
    (CallFunction|ApplyMaxSettings)
    (CallFunction|RestoreCarry)
    (CallFunction|LoadCheckpoint)))''')
fn(MAX, 'OpenDeepLabs', '(fn OpenDeepLabs ()\n  (Game|OpenLevel(byName) "/Game/HollowKin/Maps/Deep/Lvl_DeepLabs"))')
fn(MAX, 'TravelDeep', '''(fn TravelDeep ()
  (bind pc (Game|GetPlayerController 0))
  (CallFunction|StoreCarry)
  (Input|DisableInput :self self :PlayerController pc)
  (CameraFades|StartCameraFade :self (Game|GetPlayerCameraManager 0) :FromAlpha 0.0 :ToAlpha 1.0 :Duration 1.0 :bHoldWhenFinished true)
  (bind card (Utilities|Casting|CastToWBP_Loading (UserInterface|CreateWidget "%s" pc)))
  (Class|WBPLoading|SetupCard :self card :Chapter "CHAPTER 2" :TitleText "THE DEEP LABS" :BodyText "Behind L-03 there is no bed and no girl, only a second lift going further down. Halvorsen built the real program under the clinic: labs, tunnels, an old generator plant. Emilia's signal is still below you." :TipText "TIP:  Bottles (G) pull Hollows away. Some fights are better avoided than won." :Seconds 6.5)
  (UserInterface|Viewport|AddToViewport card 90)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "OpenDeepLabs" :Time 6.5 :bLooping false))''' % L)
for bp in (MAX,):
    print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False}))
call(BT, 'add_variable', {'blueprint': {'refPath': ET}, 'name': 'bShown', 'type_name': 'bool'})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': ET}, 'warnings_as_errors': False})
fn(ET, 'EndingTouched', '''(fn EndingTouched (Who)
  (bind m (Utilities|Casting|CastToBP_Max Who)
    (:then
      (if (Utilities|String|Contains (Game|GetCurrentLevelName true) "Containment")
        (if (Class|BPMax|GetPowerOn :self m)
          (if (not (Variables|Default|GetShown))
            (Variables|Default|SetShown true)
            (Class|BPMax|TravelDeep :self m))
          (else (Class|BPMax|ShowNote :self m :Msg "Sealed. Restore power at the breaker first." :Seconds 4.0)))
        (else (Class|BPMax|ShowEnding :self m))))
    (:CastFailed)))''')
fn(SFX, 'WingIntro', '''(fn WingIntro ()
  (bind lvl (Game|GetCurrentLevelName true))
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then
      (if (Utilities|String|Contains lvl "Containment")
        (Class|BPMax|ShowNote :self m :Msg "ST. BRIGID'S  //  SUB-LEVEL 2  //  CONTAINMENT WING.   The service lift brought you down. Somewhere below: Emilia." :Seconds 7.0)
        (Class|BPMax|RefreshObjective :self m))
      (if (Utilities|String|Contains lvl "DeepLabs")
        (Class|BPMax|ShowNote :self m :Msg "SUB-LEVEL 3  //  DEEP LABS.   The lift doors grind open on dark, warm air. Somewhere past the old generator plant, a child is humming." :Seconds 7.0)
        (Class|BPMax|SetObjectiveNote :self m :Msg "Go deeper. Cross the labs and the maintenance tunnels; Emilia's chamber (L-03) is past the generator hall.")))
    (:CastFailed)))''')
for bp in (ET, SFX):
    print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False}))
