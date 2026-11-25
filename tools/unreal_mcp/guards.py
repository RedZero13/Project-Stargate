"""Guards (ranged BP_HollowDrone) in the tactical outfit carry an AK-47 (AssetsvilleTown SM_Rifle_02, held at the chest, pointing forward).
Their fire is readable: the first time a guard opens fire it raises the rifle (MF_Rifle_Idle_ADS) and calls out
(warning, no damage); after that every shot plays MM_Rifle_Fire, a loud gunshot, a muzzle flash, and an impact
near Max when it misses. Hollows (melee) are unchanged."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
DR = '/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone'
SOL = '/Game/Fab/Tactical_Soldier_Outfit_for_MetaHuman__UE_5_6+_/'
call(BT, 'add_variable', {'blueprint': {'refPath': DR}, 'name': 'bWarned', 'type_name': 'bool'})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': DR}, 'warnings_as_errors': False})
HIDE = '(Rendering|SetRenderInMainPass :self mesh :bValue false)\n    (Rendering|SetRenderinDepthPass :self mesh :bValue false)\n    (Rendering|SetCastShadow :self mesh :NewCastShadow false)'
def layer(var, m):
    return '''(bind %s (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
      (Transformation|AttachComponentToComponent %s mesh "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
      (Components|SkeletalMesh|SetSkeletalMeshAsset %s "%s")
      (Components|SkinnedMesh|SetLeaderPoseComponent %s mesh)''' % (var, var, var, m, var)
SECT = '\n      '.join('(Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID %d :SectionIndex %d :bShow false :LODIndex 0)' % (i, i) for i in (4, 5, 7, 8, 9, 10))
look = '''(fn ApplyHollowLook ()
  (bind mesh (Variables|Character|GetMesh))
  (if (not (Variables|Default|GetRanged))
    %s
    %s
    (else
      %s
      %s
      %s
      %s
      (bind rifle (Utilities|Casting|CastToStaticMeshComponent (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent")))
      (Components|StaticMesh|SetStaticMesh rifle "/Game/AssetsvilleTown/Meshes/Weapons/SM_Rifle_02.SM_Rifle_02")
      (Transformation|AttachComponentToComponent rifle mesh "None" "SnapToTarget" "SnapToTarget" "KeepRelative")
      (Transformation|SetRelativeLocation :self rifle :NewLocation (Math|Vector|MakeVector 14.0 32.0 122.0))
      (Transformation|SetRelativeRotation :self rifle :NewRotation (Math|Rotator|MakeRotator 0.0 90.0 0.0))
      (Collision|SetCollisionEnabled :self rifle :NewType "NoCollision")
      %s)))''' % (layer('look', '/Game/Whisper/Base_Mesh/SK_Whisper.SK_Whisper'), HIDE,
                 layer('body', '/Game/Survival_Character/Meshes/SK_Survival_Character.SK_Survival_Character'), SECT,
                 layer('suit', SOL + 'Soldier_Outfit_v1.Soldier_Outfit_v1'), layer('helm', SOL + 'Soldier_Helmet_Outfit_v1.Soldier_Helmet_Outfit_v1'), HIDE)
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': DR + ':ApplyHollowLook'}, 'code': look}); print('look', r)
shoot = '''(fn GuardShoot (Target)
  (bind here (+ (Transformation|GetActorLocation) (Math|Vector|MakeVector 0.0 0.0 50.0)))
  (bind anim (Components|SkeletalMesh|GetAnimInstance (Variables|Character|GetMesh)))
  (if (not (Variables|Default|GetWarned))
    (Variables|Default|SetWarned true)
    (Animation|Montage|PlaySlotAnimationAsDynamicMontage anim "/Game/Characters/Mannequins/Anims/Rifle/MF_Rifle_Idle_ADS.MF_Rifle_Idle_ADS" "DefaultSlot" 0.2 0.3 1.0)
    (Audio|PlaySoundAtLocation :Sound "/Game/Interface_And_Item_Sounds/WAV/Error_Buzz_02.Error_Buzz_02" :Location here :VolumeMultiplier 1.4 :PitchMultiplier 0.6)
    (else
      (Animation|Montage|PlaySlotAnimationAsDynamicMontage anim "/Game/Characters/Mannequins/Anims/Rifle/MM_Rifle_Fire.MM_Rifle_Fire" "DefaultSlot" 0.05 0.2 1.0)
      (Audio|PlaySoundAtLocation :Sound "/Game/MW_Pistol_SK/CUE/Fire/SQ_03_Pistol_Type3_Fire_Cue.SQ_03_Pistol_Type3_Fire_Cue" :Location here :VolumeMultiplier 1.6 :PitchMultiplier 0.75)
      (Niagara|SpawnSystemAtLocation :SystemTemplate "/Game/NW_MuzzleFX/Particle_FX/FXS_Pistol_MuzzleFlash.FXS_Pistol_MuzzleFlash" :Location (+ here (* (Transformation|GetActorForwardVector) 70.0)) :Rotation (Transformation|GetActorRotation))
      (if (< (Math|Random|RandomFloatInRange 0.0 1.0) 0.6)
        (Game|Damage|ApplyDamage Target 12.0 (Pawn|GetController) self)
        (else
          (Effects|SpawnEmitterAtLocation "/Game/Realistic_Starter_VFX_Pack_Vol2/Particles/Hit/P_Concrete.P_Concrete" (+ (Transformation|GetActorLocation Target) (Math|Vector|MakeVector (Math|Random|RandomFloatInRange -90.0 90.0) (Math|Random|RandomFloatInRange -90.0 90.0) -60.0)) "0, 0, 0" (Math|Vector|MakeVector 0.6 0.6 0.6)))))))'''
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': DR + ':GuardShoot'}, 'code': shoot}); print('shoot', r)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DR}, 'warnings_as_errors': False}))
