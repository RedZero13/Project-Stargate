"""Dead soldier fixes (2026-11-27):
- the Survival Character head is bigger than the MetaHuman helmet it wore, so the head poked through: the helmet
  is dropped and the soldier's own hair is shown instead;
- parts vanished at some camera angles because each layer kept standing-pose bounds while lying down: every
  component now uses 3x bounds."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
B = '/Game/HollowKin/Blueprints/Props/BP_DeadSoldier.BP_DeadSoldier'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], r)
w(B + ':AddLayer', '''(fn AddLayer (Mesh Leader)
  (Utilities|IsValid Mesh
    (:"Is Valid"
      (bind c (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
      (Transformation|AttachComponentToComponent c Leader "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
      (Components|SkeletalMesh|SetSkeletalMeshAsset c Mesh)
      (Components|SkinnedMesh|SetLeaderPoseComponent c Leader)
      (Rendering|SetBoundsScale c 3.0))))''')
w(B + ':EventGraph', '''(event EventBeginPlay
  (bind lead (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Components|SkeletalMesh|SetSkeletalMeshAsset lead "/Game/DeadBodies_Poses_nikoff/Demo/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple")
  (Components|Animation|PlayAnimation lead (Variables|Default|GetPoseAnim) false)
  (Rendering|SetBoundsScale lead 3.0)
  (bind body (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Transformation|AttachComponentToComponent body lead "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Components|SkeletalMesh|SetSkeletalMeshAsset body (Variables|Default|GetBodyMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent body lead)
  (Rendering|SetBoundsScale body 3.0)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 7 :SectionIndex 7 :bShow false :LODIndex 0)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 8 :SectionIndex 8 :bShow false :LODIndex 0)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 9 :SectionIndex 9 :bShow false :LODIndex 0)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 10 :SectionIndex 10 :bShow false :LODIndex 0)
  (CallFunction|AddLayer :Mesh (Variables|Default|GetOutfitMesh) :Leader lead)
  (Rendering|SetRenderInMainPass lead false)
  (Rendering|SetRenderinDepthPass :self lead :bValue false)
  (Rendering|SetCastShadow lead false))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': B}, 'warnings_as_errors': False}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/HollowKin/Blueprints/Props/BP_DeadSoldier']}))
# live guards (ranged BP_HollowDrone): same outfit, same problem -> no helmet, own hair, 3x bounds
DR = '/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone'
SOL = '/Game/Fab/Tactical_Soldier_Outfit_for_MetaHuman__UE_5_6+_/'
HIDE = '(Rendering|SetRenderInMainPass :self mesh :bValue false)\n    (Rendering|SetRenderinDepthPass :self mesh :bValue false)\n    (Rendering|SetCastShadow :self mesh :NewCastShadow false)'
def layer(var, m):
    return '''(bind %s (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
      (Transformation|AttachComponentToComponent %s mesh "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
      (Components|SkeletalMesh|SetSkeletalMeshAsset %s "%s")
      (Components|SkinnedMesh|SetLeaderPoseComponent %s mesh)
      (Rendering|SetBoundsScale %s 2.0)''' % (var, var, var, m, var, var)
SECT = '\n      '.join('(Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID %d :SectionIndex %d :bShow false :LODIndex 0)' % (i, i) for i in (7, 8, 9, 10))
w(DR + ':ApplyHollowLook', '''(fn ApplyHollowLook ()
  (bind mesh (Variables|Character|GetMesh))
  (if (not (Variables|Default|GetRanged))
    %s
    %s
    (else
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
                  layer('suit', SOL + 'Soldier_Outfit_v1.Soldier_Outfit_v1'), HIDE))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DR}, 'warnings_as_errors': False}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/HollowKin/Blueprints/AI/BP_HollowDrone']}))
