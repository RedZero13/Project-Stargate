"""Enemy animation fixes (P1, 2026-11-26):
- Hollows/guards slid around in their idle pose: ABP_Unarmed only blends walk/run when the character accelerates and
  AI path following didn't report acceleration. NavMovementProperties.bUseAccelerationForPaths = true (set on the
  BP defaults by this script's caller, see notes) + orient-to-movement so they turn as they walk.
- AttackAnim: whenever a melee Hollow's attack timer fires (it just hit), it turns to Max and plays MM_Attack_01/02/03."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
DR = '/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone'
A = '/Game/Characters/Mannequins/Anims/Unarmed/Attack/'
have = call(BT, 'list_variables', {'blueprint': {'refPath': DR}}).get('returnValue') or []
if 'LastAttackSeen' not in have:
    call(BT, 'add_variable', {'blueprint': {'refPath': DR}, 'name': 'LastAttackSeen', 'type_name': 'float'})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': DR}, 'warnings_as_errors': False})
call(BT, 'add_function_graph', {'blueprint': {'refPath': DR}, 'graph_name': 'AttackAnim'})
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': DR + ':AttackAnim'}, 'code': '''(fn AttackAnim ()
  (bind na (Variables|Default|GetNextAttack))
  (if (!= na (Variables|Default|GetLastAttackSeen))
    (bind first (== (Variables|Default|GetLastAttackSeen) 0.0))
    (Variables|Default|SetLastAttackSeen na)
    (if (and (and (not first) (not (Variables|Default|GetRanged))) (not (Variables|Default|GetDead)))
      (bind p (Game|GetPlayerPawn 0))
      (bind look (Math|Rotator|FindLookatRotation (Transformation|GetActorLocation) (Transformation|GetActorLocation :self p)))
      (Transformation|SetActorRotation :self self :NewRotation (Math|Rotator|MakeRotator 0.0 0.0 (.yaw look)) :bTeleportPhysics false)
      (switch int (Math|Random|RandomIntegerInRange 0 2)
        (:0 (Animation|Montage|PlaySlotAnimationAsDynamicMontage :self (Components|SkeletalMesh|GetAnimInstance (Variables|Character|GetMesh)) :Asset "%sMM_Attack_01.MM_Attack_01" :SlotNodeName "DefaultSlot" :BlendInTime 0.1 :BlendOutTime 0.2 :InPlayRate 1.1))
        (:1 (Animation|Montage|PlaySlotAnimationAsDynamicMontage :self (Components|SkeletalMesh|GetAnimInstance (Variables|Character|GetMesh)) :Asset "%sMM_Attack_02.MM_Attack_02" :SlotNodeName "DefaultSlot" :BlendInTime 0.1 :BlendOutTime 0.2 :InPlayRate 1.1))
        (:Default (Animation|Montage|PlaySlotAnimationAsDynamicMontage :self (Components|SkeletalMesh|GetAnimInstance (Variables|Character|GetMesh)) :Asset "%sMM_Attack_03.MM_Attack_03" :SlotNodeName "DefaultSlot" :BlendInTime 0.1 :BlendOutTime 0.2 :InPlayRate 1.1))))))''' % (A, A, A)})
print('AttackAnim', r)
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': DR + ':EventGraph'}, 'code': '''(event EventTick (DeltaSeconds)
  (CallFunction|Think)
  (CallFunction|AlertCheck)
  (CallFunction|AttackAnim))'''})
print('Tick', r)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DR}, 'warnings_as_errors': False}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
