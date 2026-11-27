"""Zombie Nurse (Fab, free) in the facility:
- Undead nurses: BP_HollowDrone with the tag "Nurse" wears the nurse body + uniform (same AI and animations,
  driven through leader pose like the Whisper look).
- BP_DeadNurse: a dead nurse in one of the Dead Bodies poses (mannequin leader + nurse body), like BP_DeadSoldier."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
DR = '/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone'
DN = '/Game/HollowKin/Blueprints/Props/BP_DeadNurse.BP_DeadNurse'
NB = '/Game/ZombieFemale/Asset/Meshes/SK_ZombieFemale.SK_ZombieFemale'
NO = '/Game/ZombieFemale/Asset/Meshes/ZombieFemale_NurseOutfit.ZombieFemale_NurseOutfit'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
call(BT, 'add_function_graph', {'blueprint': {'refPath': DR}, 'graph_name': 'ApplyNurseLook'})
w(DR + ':ApplyNurseLook', '''(fn ApplyNurseLook ()
  (bind mesh (Variables|Character|GetMesh))
  (bind body (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Transformation|AttachComponentToComponent body mesh "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Components|SkeletalMesh|SetSkeletalMeshAsset body "%s")
  (Components|SkinnedMesh|SetLeaderPoseComponent body mesh)
  (bind cloth (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Transformation|AttachComponentToComponent cloth mesh "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Components|SkeletalMesh|SetSkeletalMeshAsset cloth "%s")
  (Components|SkinnedMesh|SetLeaderPoseComponent cloth mesh)
  (Rendering|SetRenderInMainPass :self mesh :bValue false)
  (Rendering|SetRenderinDepthPass :self mesh :bValue false)
  (Rendering|SetCastShadow :self mesh :NewCastShadow false))''' % (NB, NO))
w(DR + ':EventGraph', '''(event EventBeginPlay
  (Collision|SetCollisionResponseToChannel (Variables|Character|GetMesh) "ECC_Visibility" "ECR_Block")
  (Collision|SetCollisionResponseToChannel (Variables|Character|GetCapsuleComponent) "ECC_Visibility" "ECR_Block")
  (if (Actor|ActorHasTag :self self :Tag "Nurse")
    (CallFunction|ApplyNurseLook)
    (else (CallFunction|ApplyHollowLook)))
  (CallFunction|AddEyeGlow))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DR}, 'warnings_as_errors': False}))
if not call(A, 'exists', {'path': DN.split('.')[0]}).get('returnValue'):
    print(call(BT, 'create', {'folder_path': '/Game/HollowKin/Blueprints/Props', 'asset_name': 'BP_DeadNurse', 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
have = call(BT, 'list_variables', {'blueprint': {'refPath': DN}}).get('returnValue') or []
if 'PoseAnim' not in have:
    print(call(BT, 'add_object_variable', {'blueprint': {'refPath': DN}, 'name': 'PoseAnim', 'object_class': {'refPath': '/Script/Engine.AnimSequence'}}))
    call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': DN}, 'variable_name': 'PoseAnim', 'instance_editable': True})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': DN}, 'warnings_as_errors': False})
w(DN + ':EventGraph', '''(event EventBeginPlay
  (bind lead (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Components|SkeletalMesh|SetSkeletalMeshAsset lead "/Game/DeadBodies_Poses_nikoff/Demo/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple")
  (Components|Animation|PlayAnimation lead (Variables|Default|GetPoseAnim) false)
  (bind body (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Transformation|AttachComponentToComponent body lead "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Components|SkeletalMesh|SetSkeletalMeshAsset body "%s")
  (Components|SkinnedMesh|SetLeaderPoseComponent body lead)
  (bind cloth (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Transformation|AttachComponentToComponent cloth lead "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Components|SkeletalMesh|SetSkeletalMeshAsset cloth "%s")
  (Components|SkinnedMesh|SetLeaderPoseComponent cloth lead)
  (Rendering|SetRenderInMainPass :self lead :bValue false)
  (Rendering|SetRenderinDepthPass :self lead :bValue false)
  (Rendering|SetCastShadow :self lead :NewCastShadow false))''' % (NB, NO))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DN}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
