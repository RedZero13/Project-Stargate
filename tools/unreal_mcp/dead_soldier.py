"""BP_DeadSoldier: a fallen soldier prop. At BeginPlay it builds a hidden posing body (SKM_Manny_Simple
playing PoseAnim, a dead-body pose) and layers the human body + tactical soldier outfit + helmet on it
with leader pose (same trick as Max's look). Instance-editable: PoseAnim, BodyMesh, OutfitMesh, HelmetMesh."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
B = '/Game/HollowKin/Blueprints/Props/BP_DeadSoldier.BP_DeadSoldier'
call(BT, 'add_function_graph', {'blueprint': {'refPath': B}, 'graph_name': 'AddLayer'})
for p, c in [('Mesh', '/Script/Engine.SkeletalMesh'), ('Leader', '/Script/Engine.SkeletalMeshComponent')]:
    call(BT, 'add_object_function_param', {'graph': {'refPath': B + ':AddLayer'}, 'param_name': p, 'object_class': {'refPath': c}, 'input_param': True})
print('AddLayer', call(BT, 'write_graph_dsl', {'graph': {'refPath': B + ':AddLayer'}, 'code': '''(fn AddLayer (Mesh Leader)
  (Utilities|IsValid Mesh
    (:"Is Valid"
      (bind c (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
      (Transformation|AttachComponentToComponent c Leader "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
      (Components|SkeletalMesh|SetSkeletalMeshAsset c Mesh)
      (Components|SkinnedMesh|SetLeaderPoseComponent c Leader))))'''}))
print('BeginPlay', call(BT, 'write_graph_dsl', {'graph': {'refPath': B + ':EventGraph'}, 'code': '''(event EventBeginPlay
  (bind lead (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Components|SkeletalMesh|SetSkeletalMeshAsset lead "/Game/DeadBodies_Poses_nikoff/Demo/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple")
  (Components|Animation|PlayAnimation lead (Variables|Default|GetPoseAnim) false)
  (CallFunction|AddLayer :Mesh (Variables|Default|GetBodyMesh) :Leader lead)
  (CallFunction|AddLayer :Mesh (Variables|Default|GetOutfitMesh) :Leader lead)
  (CallFunction|AddLayer :Mesh (Variables|Default|GetHelmetMesh) :Leader lead)
  (Rendering|SetRenderInMainPass lead false)
  (Rendering|SetCastShadow lead false))'''}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': B}, 'warnings_as_errors': False}))
