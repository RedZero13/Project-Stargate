"""Playtest fixes (2026-11-26):
- Torch (F): debounced toggle (the input fired several times per press, so it often stayed on) + click sound.
- Pistol: auto-reload 0.5 s after the last round (or when you pull the trigger on empty with reserve left);
  reserve rounds capped at 40 so ammo stays scarce.
- CraftGel: 1 scrap part + 1 chemical -> 1 health gel (workbench).
- Sanity: being hurt costs sanity too (in addition to darkness drain / safe-room recovery / hallucinations).
- Blood overlay: softer (starts below 45 HP, max 0.32 opacity).
- Brute (Elite): takes 60% bullet damage (150% when stunned by a barrel/shock) instead of 25%.
- Hollows: dim red eye light + an audible stinger the first time one spots you (no more silent ambush from the dark).
- Barrels: their mesh now blocks the Visibility channel, so bullets hit and detonate them."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
DR = '/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone'
BAR = '/Game/HollowKin/Blueprints/Interactables/BP_HazardBarrel.BP_HazardBarrel'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl})
    print(g.split('.')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def newfn(bp, name):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
call(BT, 'add_variable', {'blueprint': {'refPath': MAX}, 'name': 'LastTorchToggle', 'type_name': 'float'})
call(BT, 'add_variable', {'blueprint': {'refPath': DR}, 'name': 'bAlerted', 'type_name': 'bool'})
0 and w(MAX + ':ToggleFlashlight', '''(fn ToggleFlashlight ()
  (bind now (Utilities|Time|GetTimeSeconds))
  (if (>= (- now (Variables|Default|GetLastTorchToggle)) 0.3)
    (Variables|Default|SetLastTorchToggle now)
    (Rendering|ToggleVisibility (Utilities|Casting|CastToSpotLightComponent (Actor|GetComponentByClass "/Script/Engine.SpotLightComponent")))
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_01.Flick_Switch_01" 0.5)))''')
src = open('/private/tmp/claude-501/-Users-piyushbanerjee-Documents-Unreal-Projects/3ad6895c-a061-4731-8ef0-b5a63d097acb/scratchpad/fire.dsl').read()
w(MAX + ':FirePistol', src)
w(MAX + ':ApplyHurt', '''(fn ApplyHurt (Amount)
  (if (not (Variables|Default|GetDead))
    (Variables|Default|SetHealth (Math|Float|Clamp(Float) (- (Variables|Default|GetHealth) (* Amount (Variables|Default|GetDmgMul))) 0.0 100.0))
    (Variables|Default|SetSanity (Math|Float|Clamp(Float) (- (Variables|Default|GetSanity) (* Amount 0.3)) 0.0 100.0))
    (Variables|Default|SetHurtFlash 1.0)
    (if (<= (Variables|Default|GetHealth) 0.0)
      (CallFunction|Die))))''')

0 and w(MAX + ':CraftGel', '''(fn CraftGel ()
  (if (and (>= (Variables|Default|GetParts) 1) (>= (Variables|Default|GetChem) 1))
    (Variables|Default|SetParts (- (Variables|Default|GetParts) 1))
    (Variables|Default|SetChem (- (Variables|Default|GetChem) 1))
    (Variables|Default|SetGels (+ (Variables|Default|GetGels) 1))
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_03.Flick_Switch_03" 0.8)))''')
# drone: elite damage + alert cue + eye light
td = call(BT, 'read_graph_dsl', {'graph': {'refPath': DR + ':TakeHit'}})['returnValue']
td2 = td.replace('(* Amount 0.25)', '(* Amount 0.6)').replace('(|Getb', '(Variables|Default|Get').replace('(|Setb', '(Variables|Default|Set')
assert td2 != td
w(DR + ':TakeHit', td2)
w(DR + ':AlertCheck', '''(fn AlertCheck ()
  (bind now (Utilities|Time|GetTimeSeconds))
  (if (and (and (Variables|Default|GetSeesNow) (not (Variables|Default|GetDead))) (not (Variables|Default|GetAlerted)))
    (Variables|Default|SetAlerted true)
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Discordant_GameOver_Musical_Short.Discordant_GameOver_Musical_Short" 0.45 0.75))
  (if (and (and (Variables|Default|GetSeesNow) (not (Variables|Default|GetDead))) (>= now (Variables|Default|GetNextAlert)))
    (Variables|Default|SetNextAlert (+ now 2.0))
    (for a (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone_C")
      (CallFunction|HearNoise (Utilities|Casting|CastToBP_HollowDrone a) (Transformation|GetActorLocation (Game|GetPlayerPawn 0)) 2500.0))))''')
newfn(DR, 'AddEyeGlow')
w(DR + ':AddEyeGlow', '''(fn AddEyeGlow ()
  (bind l (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "/Script/Engine.PointLightComponent")))
  (Transformation|AttachComponentToComponent l (Variables|Character|GetMesh) "head" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Transformation|SetRelativeLocation :self l :NewLocation (Math|Vector|MakeVector 0.0 14.0 6.0))
  (Rendering|Components|Light|SetIntensity :self l :NewIntensity 60.0)
  (Rendering|Components|Light|SetLightColor :self l :NewLightColor (Math|Color|MakeColor 1.0 0.12 0.08 1.0))
  (Rendering|Lighting|SetAttenuationRadius :self l :NewRadius 120.0)
  (Rendering|Components|Light|SetCastShadows :self l :bNewValue false))''')
eg = call(BT, 'read_graph_dsl', {'graph': {'refPath': DR + ':EventGraph'}})['returnValue']
if 'AddEyeGlow' not in eg:
    w(DR + ':EventGraph', '''(event EventBeginPlay
  (Collision|SetCollisionResponseToChannel (Variables|Character|GetMesh) "ECC_Visibility" "ECR_Block")
  (Collision|SetCollisionResponseToChannel (Variables|Character|GetCapsuleComponent) "ECC_Visibility" "ECR_Block")
  (CallFunction|ApplyHollowLook)
  (CallFunction|AddEyeGlow))''')
w(BAR + ':EventGraph', '''(event EventBeginPlay
  (for c (Actor|GetComponentsByClass "/Script/Engine.StaticMeshComponent")
    (bind p (Utilities|Casting|CastToPrimitiveComponent c))
    (Collision|SetCollisionEnabled :self p :NewType "QueryAndPhysics")
    (Collision|SetCollisionResponseToChannel :self p :Channel "ECC_Visibility" :NewResponse "ECR_Block")))''')
co = call(BT, 'read_graph_dsl', {'graph': {'refPath': MAX + ':Collect'}})['returnValue']
import re
m = re.search(r'\(Variables\|Default\|SetReserveAmmo (\(\+ .*?GetLootMul\)\)\)\))\)', co)
if m and 'Min(' not in co[:m.end()]:
    co2 = co[:m.start()] + '(Variables|Default|SetReserveAmmo (select (> %s 40) 40 %s))' % (m.group(1), m.group(1)) + co[m.end():]
    w(MAX + ':Collect', co2)
else:
    print('Collect pattern not found / already capped'); print(co[:400])
