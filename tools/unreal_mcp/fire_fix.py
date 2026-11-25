"""FirePistol rewritten with auto-reload (0.5 s after the last round, or on an empty trigger pull with reserve left)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':FirePistol'}, 'code': '''(fn FirePistol ()
  (bind now (Utilities|Time|GetTimeSeconds))
  (bind cam (Game|GetPlayerCameraManager 0))
  (bind start (Camera|GetCameraLocation cam))
  (bind dir (Math|Random|RandomUnitVectorInConeInDegrees (Math|Vector|GetForwardVector (Camera|GetCameraRotation cam)) (+ 0.3 (* (- 100.0 (Variables|Default|GetSanity)) 0.04))))
  (bind endp (+ start (* dir (Variables|Default|GetPistolRange))))
  (if (and (Variables|Default|GetAiming) (>= (- now (Variables|Default|GetLastFireTime)) (Variables|Default|GetFireInterval)))
    (Variables|Default|SetLastFireTime now)
    (if (> (Variables|Default|GetAmmo) 0)
      (Variables|Default|SetAmmo (- (Variables|Default|GetAmmo) 1))
      (CallFunction|EmitNoise :Loc (Transformation|GetActorLocation :self self) :Radius 2500.0)
      (bind (hit ok) (Collision|SphereTraceByChannel :Start start :End endp :Radius 12.0 :TraceChannel "Visibility" :bTraceComplex false :bIgnoreSelf true))
      (bind (bb io tm dist loc ip nm inm pm ha hc hbn bn hi ei fi ts te) (Collision|BreakHitResult hit))
      (if ok
        (Game|Damage|ApplyDamage :DamagedActor ha :BaseDamage (Variables|Default|GetPistolDamage) :EventInstigator (Pawn|GetController) :DamageCauser self))
      (CallFunction|MuzzleFx :Target (select ok ip endp))
      (if (and (<= (Variables|Default|GetAmmo) 0) (> (Variables|Default|GetReserveAmmo) 0))
        (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "ReloadPistol" :Time 0.5 :bLooping false))
      (else
        (if (> (Variables|Default|GetReserveAmmo) 0)
          (CallFunction|ReloadPistol)
          (else
            (Audio|PlaySound2D "/Game/MW_Pistol_SK/CUE/Reload/Type_01/SQ_Pistol_Reload_Type_1_Slide_1_Cue.SQ_Pistol_Reload_Type_1_Slide_1_Cue" 0.6)))))))'''})
print(r)
