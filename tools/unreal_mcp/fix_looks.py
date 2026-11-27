"""Leader-pose looks without see-through holes: the hidden posing mannequin is removed from the depth pass too
(it was drawn into depth but not colour, punching holes through the clothes). Ranged guards now wear the
tactical soldier outfit over the human body (hair/clothes/backpack sections hidden)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
DR = '/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone'
DS = '/Game/HollowKin/Blueprints/Props/BP_DeadSoldier.BP_DeadSoldier'
SOL = '/Game/Fab/Tactical_Soldier_Outfit_for_MetaHuman__UE_5_6+_/'
HIDE = lambda m: '(Rendering|SetRenderInMainPass :self %s :bValue false)\n    (Rendering|SetRenderinDepthPass :self %s :bValue false)\n    (Rendering|SetCastShadow :self %s :NewCastShadow false)' % (m, m, m)
def layer(var, mesh, lead):
    return '''(bind %s (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
    (Transformation|AttachComponentToComponent %s %s "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
    (Components|SkeletalMesh|SetSkeletalMeshAsset %s "%s")
    (Components|SkinnedMesh|SetLeaderPoseComponent %s %s)''' % (var, var, lead, var, mesh, var, lead)
SECT = lambda c: '\n      '.join('(Components|SkinnedMesh|ShowMaterialSection :self %s :MaterialID %d :SectionIndex %d :bShow false :LODIndex 0)' % (c, i, i) for i in (4, 5, 7, 8, 9, 10))
print('Max', call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':ApplyMaxLook'}, 'code': '''(fn ApplyMaxLook ()
  (bind mesh (Variables|Character|GetMesh))
  %s
  %s)''' % (layer('look', '/Game/Survival_Character/Meshes/SK_Survival_Character.SK_Survival_Character', 'mesh'), HIDE('mesh'))}))
print('Hollow', call(BT, 'write_graph_dsl', {'graph': {'refPath': DR + ':ApplyHollowLook'}, 'code': '''(fn ApplyHollowLook ()
  (bind mesh (Variables|Character|GetMesh))
  (if (not (Variables|Default|GetRanged))
    %s
    %s
    (else
      %s
      %s
      %s
      %s
      %s)))''' % (layer('look', '/Game/Whisper/Base_Mesh/SK_Whisper.SK_Whisper', 'mesh'), HIDE('mesh'),
                  layer('body', '/Game/Survival_Character/Meshes/SK_Survival_Character.SK_Survival_Character', 'mesh'), SECT('body'),
                  layer('suit', SOL + 'Soldier_Outfit_v1.Soldier_Outfit_v1', 'mesh'), layer('helm', SOL + 'Soldier_Helmet_Outfit_v1.Soldier_Helmet_Outfit_v1', 'mesh'), HIDE('mesh'))}))
for bp in (MAX, DR):
    print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False}))
