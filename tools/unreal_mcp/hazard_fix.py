"""BP_HazardShock: zaps Max always, but Hollow enemies only while they are chasing (lured in) -
wandering/patrolling enemies no longer kill themselves in the puddle."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
B = '/Game/HollowKin/Blueprints/Interactables/BP_HazardShock.BP_HazardShock'
DSL = '''(fn ShockTick ()
  (bind now (Utilities|Time|GetTimeSeconds))
  (if (>= now (Variables|Default|GetNextZap))
    (Variables|Default|SetNextZap (+ now 0.5))
    (Variables|Default|SetZapTargets (Collision|GetOverlappingActors (Variables|Default|GetTrigger) "/Script/Engine.Pawn"))
    (for t (Variables|Default|GetZapTargets)
      (bind d (Utilities|Casting|CastToBP_HollowDrone t)
        (:then
          (if (Class|BPHollowDrone|GetChasing :self d)
            (Game|Damage|ApplyDamage t 9.0 0 self)
            (Effects|SpawnEmitterAtLocation "/Game/Realistic_Starter_VFX_Pack_Vol2/Particles/Sparks/P_Sparks_E.P_Sparks_E" (Transformation|GetActorLocation t) "0, 0, 0" (Math|Vector|MakeVector 0.5 0.5 0.5))
            (Class|BPHollowDrone|ExposeHollow d 2.5)))
        (:CastFailed
          (Game|Damage|ApplyDamage t 9.0 0 self)
          (Effects|SpawnEmitterAtLocation "/Game/Realistic_Starter_VFX_Pack_Vol2/Particles/Sparks/P_Sparks_E.P_Sparks_E" (Transformation|GetActorLocation t) "0, 0, 0" (Math|Vector|MakeVector 0.5 0.5 0.5))
          (Audio|PlaySoundAtLocation "/Game/Interface_And_Item_Sounds/WAV/Error_Buzz_02.Error_Buzz_02" (Transformation|GetActorLocation t) "0, 0, 0" 0.5 0.6))))))'''
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': B + ':ShockTick'}, 'code': DSL}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': B}, 'warnings_as_errors': True}))
