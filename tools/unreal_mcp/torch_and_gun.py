"""1) Torch in Max's left hand: the FP Flashlight pack's SM_Flashlight is attached to the existing spotlight
   (tag Flashlight, already on hand_l and aimed every frame) so the torch always points down the beam.
2) Max starts unarmed (BP_Max.HasPistol): aiming is gated, the HUD ring is hidden until he has the gun.
3) BP_GunPickup: placed by the first dead soldier (C1). Walking up to it plays a short scene: camera blends to a
   side shot, Max stands over the body and draws the M1911 (MM_Pistol_Equip), 6 + 6 rounds, then control returns.
   If a checkpoint already exists (respawn after saving) the pistol is given at once and the scene is skipped."""
from ui_lib import call
import json
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
O = 'editor_toolset.toolsets.object.ObjectTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
SFX = '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX'
GP = '/Game/HollowKin/Blueprints/Interactables/BP_GunPickup.BP_GunPickup'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl})
    print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
# --- torch -----------------------------------------------------------------------------
w(MAX + ':ApplyMaxLook', '''(fn ApplyMaxLook ()
  (bind mesh (Variables|Character|GetMesh))
  (bind look (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Transformation|AttachComponentToComponent look mesh "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Components|SkeletalMesh|SetSkeletalMeshAsset look "/Game/Survival_Character/Meshes/SK_Survival_Character.SK_Survival_Character")
  (Components|SkinnedMesh|SetLeaderPoseComponent look mesh)
  (Rendering|SetRenderInMainPass :self mesh :bValue false)
  (Rendering|SetRenderinDepthPass :self mesh :bValue false)
  (Rendering|SetCastShadow :self mesh :NewCastShadow false)
  (bind spot (Utilities|Casting|CastToSceneComponent (Utilities|Array|Get(acopy) (Actor|GetComponentsByTag "/Script/Engine.ActorComponent" "Flashlight") 0)))
  (bind torch (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent")))
  (Components|StaticMesh|SetStaticMesh torch "/Game/FPFlashlightAnims/Mesh/SM_Flashlight.SM_Flashlight")
  (Transformation|AttachComponentToComponent torch spot "None" "SnapToTarget" "SnapToTarget" "KeepRelative")
  (Transformation|SetRelativeLocation :self torch :NewLocation (Math|Vector|MakeVector -16.0 0.0 0.0))
  (Transformation|SetRelativeRotation :self torch :NewRotation (Math|Rotator|MakeRotator 0.0 0.0 -90.0))
  (Collision|SetCollisionEnabled :self torch :NewType "NoCollision"))''')
# --- unarmed until the pickup --------------------------------------------------------------
call(BT, 'add_variable', {'blueprint': {'refPath': MAX}, 'name': 'bHasPistol', 'type_name': 'bool'})
w(MAX + ':SetAimMode', '''(fn SetAimMode (NewAiming)
  (Variables|Default|SetAiming (and NewAiming (Variables|Default|GetHasPistol))))''')
call(BT, 'add_function_graph', {'blueprint': {'refPath': SFX}, 'graph_name': 'SetRingShown'})
call(BT, 'add_function_param', {'graph': {'refPath': SFX + ':SetRingShown'}, 'param_name': 'Shown', 'param_type': 'bool', 'input_param': True})
w(SFX + ':SetRingShown', '''(fn SetRingShown (Shown)
  (if Shown
    (Widget|SetVisibility (Variables|WBP_ScreenFX|GetWeaponHUD) "HitTestInvisible")
    (else (Widget|SetVisibility (Variables|WBP_ScreenFX|GetWeaponHUD) "Collapsed"))))''')
s = open('tickfx.py').read()
s = s.replace(":Aiming (Variables|Default|GetAiming)))\n    (:\"Is Not Valid\"", ":Aiming (Variables|Default|GetAiming))\n      (Class|WBPScreenFX|SetRingShown :self %(fx)s :Shown (Variables|Default|GetHasPistol)))\n    (:\"Is Not Valid\"")
open('tickfx.py', 'w').write(s)
exec(compile(s.split("print(call(BT")[0] + "print(call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':TickFX'}, 'code': dsl}))", 'tickfx', 'exec'))
for bp in (MAX, SFX):
    print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False}))
# --- gun pickup scene -------------------------------------------------------------------------
if not call('editor_toolset.toolsets.asset.AssetTools', 'exists', {'path': GP.split('.')[0]}).get('returnValue'):
    print(call(BT, 'create', {'folder_path': '/Game/HollowKin/Blueprints/Interactables', 'asset_name': 'BP_GunPickup', 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
call(BT, 'add_variable', {'blueprint': {'refPath': GP}, 'name': 'bDone', 'type_name': 'bool'})
call(BT, 'add_object_variable', {'blueprint': {'refPath': GP}, 'name': 'Cam', 'object_class': {'refPath': '/Script/Engine.CameraActor'}})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': GP}, 'warnings_as_errors': False})
w(GP + ':EventGraph', '''(event EventBeginPlay
  (if (SaveGame|DoesSaveGameExist "HollowKinSlot1" 0)
    (Variables|Default|SetDone true)
    (Utilities|FlowControl|Delay 0.5)
    (bind m0 (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
      (:then (Class|BPMax|SetHasPistol :self m0 :bHasPistol true))
      (:CastFailed))))''')
w(GP + ':EventGraph', '''(event EventTick (DeltaSeconds)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then
      (if (and (not (Variables|Default|GetDone)) (< (Transformation|GetDistanceTo self m) 170.0))
        (Variables|Default|SetDone true)
        (bind pc (Game|GetPlayerController 0))
        (Input|DisableInput :self m :PlayerController pc)
        (Transformation|SetActorLocationAndRotation :self m :NewLocation (Math|Vector|MakeVector (.x (Transformation|GetActorLocation self)) (.y (Transformation|GetActorLocation self)) (.z (Transformation|GetActorLocation m))) :NewRotation (Transformation|GetActorRotation self) :bSweep false :bTeleport true)
        (bind camloc (+ (+ (Transformation|GetActorLocation self) (* (Transformation|GetActorRightVector self) -210.0)) (Math|Vector|MakeVector 0.0 0.0 60.0)))
        (bind target (+ (Transformation|GetActorLocation self) (* (Transformation|GetActorForwardVector self) 70.0)))
        (Variables|Default|SetCam (Utilities|Casting|CastToCameraActor (Game|SpawnActorfromClass :Class "/Script/Engine.CameraActor" :SpawnTransform (Math|Transform|MakeTransform camloc (Math|Rotator|FindLookAtRotation camloc target) (Math|Vector|MakeVector 1.0 1.0 1.0)))))
        (Game|Player|SetViewTargetwithBlend :self pc :NewViewTarget (Variables|Default|GetCam) :BlendTime 0.9)
        (Utilities|FlowControl|Delay 0.9)
        (Animation|Montage|PlaySlotAnimationAsDynamicMontage (Components|SkeletalMesh|GetAnimInstance (Class|Character|GetMesh :self m)) "/Game/Characters/Mannequins/Anims/Pistol/MM_Pistol_Equip.MM_Pistol_Equip" "DefaultSlot" 0.15 0.25 0.9)
        (Utilities|FlowControl|Delay 1.5)
        (Class|BPMax|SetHasPistol :self m :bHasPistol true)
        (Class|BPMax|SetAmmo :self m :Ammo 6)
        (Class|BPMax|SetReserveAmmo :self m :ReserveAmmo 6)
        (Audio|PlaySound2D "/Game/MW_Pistol_SK/CUE/Reload/Type_01/SQ_Pistol_Reload_Type_1_Full_Cue.SQ_Pistol_Reload_Type_1_Full_Cue" 0.8)
        (Class|BPMax|ShowNote :self m :Msg "M1911.  The guard won't need it now.  6 rounds loaded, 6 spare.   Hold right mouse (or T) to aim." :Seconds 6.0)
        (Utilities|FlowControl|Delay 1.6)
        (Game|Player|SetViewTargetwithBlend :self pc :NewViewTarget m :BlendTime 0.8)
        (Utilities|FlowControl|Delay 0.8)
        (Input|EnableInput :self m :PlayerController pc)
        (Actor|DestroyActor (Variables|Default|GetCam))))
    (:CastFailed)))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': GP}, 'warnings_as_errors': False}))
