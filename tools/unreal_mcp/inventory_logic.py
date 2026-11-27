"""Inventory / crafting / bottle lure on BP_Max.
- Gels, Sedatives, Bottles (start 2) are carried; Collect kind 1/2/6 adds them (kind 6 = bottle).
- UseGel (+40 HP), UseSedative (+35 sanity), CraftAmmo (2 parts + 1 chem -> 6 rounds), CraftTonic (2 chem -> 1 sedative).
- ThrowBottle (G): traces from the camera, the bottle shatters where it lands 0.6 s later and EmitNoise draws Hollows."""
from ui_lib import call
import json
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
B = {'refPath': MAX}
for n in ('Gels', 'Sedatives', 'Bottles', 'BottleHint'):
    call(BT, 'add_variable', {'blueprint': B, 'name': n, 'type_name': 'int'})
call(BT, 'add_struct_variable', {'blueprint': B, 'name': 'LandLoc', 'struct_type': {'refPath': '/Script/CoreUObject.Vector'}})
call(BT, 'compile_blueprint', {'blueprint': B, 'warnings_as_errors': False})
cdo = call(BT, 'get_default_object', {'blueprint': B})['returnValue']
print(call('editor_toolset.toolsets.object.ObjectTools', 'set_properties', {'instance': cdo, 'values': json.dumps({'Bottles': 2})}))
def fn(name, dsl):
    call(BT, 'add_function_graph', {'blueprint': B, 'graph_name': name})
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':' + name}, 'code': dsl})
    print(name, r if (not isinstance(r, dict) or r.get('returnValue') is not None) else 'ok')
N = lambda msg, s=3.0: '(CallFunction|Notify :Msg "%s" :Seconds %s)' % (msg, s)
fn('Collect', '''(fn Collect (Kind Amount)
  (if (== Kind 0)
    (Variables|Default|SetReserveAmmo (+ (Variables|Default|GetReserveAmmo) (Math|Float|Round (* Amount (Variables|Default|GetLootMul)))))
    (elif (== Kind 1)
      (Variables|Default|SetGels (+ (Variables|Default|GetGels) 1))
      %s
      (elif (== Kind 2)
        (Variables|Default|SetSedatives (+ (Variables|Default|GetSedatives) 1))
        %s
        (elif (== Kind 3)
          (Variables|Default|SetFuses (+ (Variables|Default|GetFuses) 1))
          %s
          (elif (== Kind 4)
            (Variables|Default|SetParts (+ (Variables|Default|GetParts) 1))
            %s
            (elif (== Kind 5)
              (Variables|Default|SetChem (+ (Variables|Default|GetChem) 1))
              %s
              (elif (== Kind 6)
                (Variables|Default|SetBottles (+ (Variables|Default|GetBottles) 1))
                %s
                (elif (== Kind 7)
                  (Variables|Default|SetBond (+ (Variables|Default|GetBond) 20.0))
                  %s)))))))))''' % (
    N('HEALTH GEL  +1     (open your backpack with I to use it)'), N('SEDATIVE  +1     (open your backpack with I to use it)'),
    N('FUSE COLLECTED'), N('SCRAP PARTS  +1     (workbench: I, then WORKBENCH)', 2.5), N('CHEMICALS  +1     (workbench: I, then WORKBENCH)', 2.5),
    N('GLASS BOTTLE  +1     (G throws it to lure Hollows away)', 2.5),
    N("EMILIA'S DRAWING.  Crayon: two stick figures holding hands, 'MAX + EM'. You fold it into your jacket.", 6.0)))
fn('UseGel', '''(fn UseGel ()
  (if (> (Variables|Default|GetGels) 0)
    (Variables|Default|SetGels (- (Variables|Default|GetGels) 1))
    (Variables|Default|SetHealth (Math|Float|Clamp(Float) (+ (Variables|Default|GetHealth) 40.0) 0.0 100.0))
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Special_Powerup_03.Special_Powerup_03" 0.6)))''')
fn('UseSedative', '''(fn UseSedative ()
  (if (> (Variables|Default|GetSedatives) 0)
    (Variables|Default|SetSedatives (- (Variables|Default|GetSedatives) 1))
    (Variables|Default|SetSanity (Math|Float|Clamp(Float) (+ (Variables|Default|GetSanity) 35.0) 0.0 100.0))
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Special_Powerup_03.Special_Powerup_03" 0.6)))''')
fn('CraftAmmo', '''(fn CraftAmmo ()
  (if (and (>= (Variables|Default|GetParts) 2) (>= (Variables|Default|GetChem) 1))
    (Variables|Default|SetParts (- (Variables|Default|GetParts) 2))
    (Variables|Default|SetChem (- (Variables|Default|GetChem) 1))
    (Variables|Default|SetReserveAmmo (+ (Variables|Default|GetReserveAmmo) 6))
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_03.Flick_Switch_03" 0.8)))''')
fn('CraftTonic', '''(fn CraftTonic ()
  (if (>= (Variables|Default|GetChem) 2)
    (Variables|Default|SetChem (- (Variables|Default|GetChem) 2))
    (Variables|Default|SetSedatives (+ (Variables|Default|GetSedatives) 1))
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_03.Flick_Switch_03" 0.8)))''')
fn('ThrowBottle', '''(fn ThrowBottle ()
  (if (and (> (Variables|Default|GetBottles) 0) (not (Variables|Default|GetDead)))
    (Variables|Default|SetBottles (- (Variables|Default|GetBottles) 1))
    (bind cam (Game|GetPlayerCameraManager 0))
    (bind start (Camera|GetCameraLocation cam))
    (bind endp (+ start (* (Math|Vector|GetForwardVector (Camera|GetCameraRotation cam)) 1800.0)))
    (bind (hit ok) (Collision|LineTraceByChannel :Start start :End endp :TraceChannel "Visibility" :bTraceComplex false :bIgnoreSelf true))
    (bind (bb io tm dist loc ip nm inm pm ha hc hbn bn hi ei fi ts te) (Collision|BreakHitResult hit))
    (Variables|Default|SetLandLoc (select ok ip endp))
    (Audio|PlaySound2D "/Game/Essential_Foosteps_SK/WAV/Glass/Footstep_Glass_Jump_3.Footstep_Glass_Jump_3" 0.35)
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "BottleLand" :Time 0.6 :bLooping false)
    (if (== (Variables|Default|GetBottleHint) 0)
      (Variables|Default|SetBottleHint 1)
      %s)))''' % N('The bottle shatters. Anything nearby will come to check the noise.', 4.0))
fn('BottleLand', '''(fn BottleLand ()
  (Audio|PlaySoundatLocation :Sound "/Game/Essential_Foosteps_SK/WAV/Glass/Footstep_Glass_Land_4.Footstep_Glass_Land_4" :Location (Variables|Default|GetLandLoc) :VolumeMultiplier 1.6)
  (Effects|SpawnEmitterAtLocation "/Game/Realistic_Starter_VFX_Pack_Vol2/Particles/Sparks/P_Sparks_E.P_Sparks_E" (Variables|Default|GetLandLoc) "0, 0, 0" (Math|Vector|MakeVector 0.3 0.3 0.3))
  (CallFunction|EmitNoise :Loc (Variables|Default|GetLandLoc) :Radius 2200.0))''')
