"""BP_HollowChild (Children's Dorm): the bare mannequin now wears the Modern City Girl model (civilian_girl),
leader-posed on the hidden mannequin (kept out of the main and depth passes)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
HC = '/Game/HollowKin/Blueprints/AI/BP_HollowChild.BP_HollowChild'
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': HC + ':EventGraph'}, 'code': '''(event EventBeginPlay
  (bind body (Variables|Default|GetBody))
  (Components|Animation|PlayAnimation body "/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle.MM_Idle" true)
  (bind look (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Transformation|AttachComponentToComponent look body "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Components|SkeletalMesh|SetSkeletalMeshAsset look "/Game/civilian_girl/meshes/SKM_army_girl.SKM_army_girl")
  (Components|SkinnedMesh|SetLeaderPoseComponent look body)
  (Rendering|SetRenderInMainPass :self body :bValue false)
  (Rendering|SetRenderinDepthPass :self body :bValue false)
  (Rendering|SetCastShadow :self body :NewCastShadow false))'''}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': HC}, 'warnings_as_errors': False}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/HollowKin/Blueprints/AI/BP_HollowChild']}))
