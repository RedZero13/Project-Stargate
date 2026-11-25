"""BP_DeadSoldier: a fallen soldier prop. At BeginPlay it builds a hidden posing body (SKM_Manny_Simple
playing PoseAnim, a dead-body pose) and layers the human body + tactical soldier outfit + helmet on it
with leader pose (same trick as Max's look). The Survival Character body keeps only face, hands and
body skin: hair, cap, jacket, jeans, shoes and backpack sections (4,5,7,8,9,10) are hidden under the outfit. Instance-editable: PoseAnim, BodyMesh, OutfitMesh, HelmetMesh."""
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
  (bind body (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Transformation|AttachComponentToComponent body lead "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Components|SkeletalMesh|SetSkeletalMeshAsset body (Variables|Default|GetBodyMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent body lead)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 4 :SectionIndex 4 :bShow false :LODIndex 0)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 5 :SectionIndex 5 :bShow false :LODIndex 0)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 7 :SectionIndex 7 :bShow false :LODIndex 0)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 8 :SectionIndex 8 :bShow false :LODIndex 0)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 9 :SectionIndex 9 :bShow false :LODIndex 0)
  (Components|SkinnedMesh|ShowMaterialSection :self body :MaterialID 10 :SectionIndex 10 :bShow false :LODIndex 0)
  (CallFunction|AddLayer :Mesh (Variables|Default|GetOutfitMesh) :Leader lead)
  (CallFunction|AddLayer :Mesh (Variables|Default|GetHelmetMesh) :Leader lead)
  (Rendering|SetRenderInMainPass lead false)
  (Rendering|SetRenderinDepthPass :self lead :bValue false)
  (Rendering|SetCastShadow lead false))'''}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': B}, 'warnings_as_errors': False}))
