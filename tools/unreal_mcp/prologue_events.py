"""Longer prologue on Main Street (Lvl_City; open it first). Voiced with the Kokoro lines (tools/voice/lines.py).
Beats, south to north:
  start      title, controls, Jaz's call (now voiced) and Max's reply after it
  -5200      abandoned police car, lights still flashing, radio: quarantine order (voiced) + a glass bottle (G throw)
  -1800      fence of MISSING posters, all children from state care (Max, voiced)
   1500      cutscene: a small figure in a hospital gown under a far streetlight; it is gone when you look again
   4500      Jaz calls back: don't follow it, get inside (voiced)
   7300      crashed ambulance, back doors open, empty stretcher, dead paramedic, a health gel
   7900      Max at the door (voiced)
BP_StreetEvent: one-shot proximity event (note, voice, optional objective, optional flashing police lights, optional
'HideTag': actors with that tag vanish a few seconds after it fires). Tag CityEvents (re-runnable)."""
import json
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
EV = '/Game/HollowKin/Blueprints/Interactables/BP_StreetEvent.BP_StreetEvent'
PHONE = '/Game/HollowKin/Blueprints/Interactables/BP_PhoneCall.BP_PhoneCall'
MAXC = '(Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))'
VO = lambda i: '/Game/HollowKin/Audio/VO/VO_%s.VO_%s' % (i, i)
assert 'Lvl_City' in str(call(S, 'get_current_level', {})['returnValue']), 'open Lvl_City first'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
# ---------------- BP_StreetEvent ----------------
if not call(A, 'exists', {'path': EV.split('.')[0]}).get('returnValue'):
    print(call(BT, 'create', {'folder_path': '/Game/HollowKin/Blueprints/Interactables', 'asset_name': 'BP_StreetEvent', 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
have = call(BT, 'list_variables', {'blueprint': {'refPath': EV}}).get('returnValue') or []
for n, t in (('Radius', 'float'), ('Msg', 'string'), ('Seconds', 'float'), ('Objective', 'string'), ('HideTag', 'string'), ('Flash', 'bool'), ('Done', 'bool'), ('FlashOn', 'bool')):
    if n not in have:
        call(BT, 'add_variable', {'blueprint': {'refPath': EV}, 'name': n, 'type_name': t})
        call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': EV}, 'variable_name': n, 'instance_editable': True})
for n, c in (('Voice', '/Script/Engine.SoundBase'), ('LightA', '/Script/Engine.PointLightComponent'), ('LightB', '/Script/Engine.PointLightComponent')):
    if n not in have:
        call(BT, 'add_object_variable', {'blueprint': {'refPath': EV}, 'name': n, 'object_class': {'refPath': c}})
        if n == 'Voice': call(BT, 'set_variable_instance_editable', {'blueprint': {'refPath': EV}, 'variable_name': n, 'instance_editable': True})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': EV}, 'warnings_as_errors': False})
w(EV + ':EventGraph', '''(event EventBeginPlay
  (if (Variables|Default|GetFlash)
    (bind a (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "/Script/Engine.PointLightComponent")))
    (Transformation|SetRelativeLocation :self a :NewLocation (Math|Vector|MakeVector 0.0 -60.0 170.0))
    (Rendering|Components|Light|SetLightColor :self a :NewLightColor (Math|Color|MakeColor 1.0 0.05 0.05 1.0))
    (Rendering|Components|Light|SetIntensity :self a :NewIntensity 900.0)
    (Rendering|Lighting|SetAttenuationRadius :self a :NewRadius 900.0)
    (Variables|Default|SetLightA a)
    (bind b (Utilities|Casting|CastToPointLightComponent (Game|AddComponentbyClass self "/Script/Engine.PointLightComponent")))
    (Transformation|SetRelativeLocation :self b :NewLocation (Math|Vector|MakeVector 0.0 60.0 170.0))
    (Rendering|Components|Light|SetLightColor :self b :NewLightColor (Math|Color|MakeColor 0.05 0.2 1.0 1.0))
    (Rendering|Components|Light|SetIntensity :self b :NewIntensity 0.0)
    (Rendering|Lighting|SetAttenuationRadius :self b :NewRadius 900.0)
    (Variables|Default|SetLightB b)
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "FlashTick" :Time 0.45 :bLooping true)))''')
call(BT, 'add_function_graph', {'blueprint': {'refPath': EV}, 'graph_name': 'FlashTick'})
w(EV + ':FlashTick', '''(fn FlashTick ()
  (Variables|Default|SetFlashOn (not (Variables|Default|GetFlashOn)))
  (Rendering|Components|Light|SetIntensity :self (Variables|Default|GetLightA) :NewIntensity (select (Variables|Default|GetFlashOn) 900.0 0.0))
  (Rendering|Components|Light|SetIntensity :self (Variables|Default|GetLightB) :NewIntensity (select (Variables|Default|GetFlashOn) 0.0 900.0)))''')
call(BT, 'add_function_graph', {'blueprint': {'refPath': EV}, 'graph_name': 'HideNow'})
w(EV + ':HideNow', '''(fn HideNow ()
  (for x (Actor|GetAllActorswithTag (Utilities|String|StringToName (Variables|Default|GetHideTag)))
    (Actor|DestroyActor :self x)))''')
w(EV + ':EventGraph', '''(event EventTick (DeltaSeconds)
  (bind m %s
    (:then
      (if (and (and (not (Variables|Default|GetDone)) (> (Utilities|Time|GetGameTimeinSeconds) 3.0)) (< (Transformation|GetDistanceTo self m) (Variables|Default|GetRadius)))
        (Variables|Default|SetDone true)
        (Class|BPMax|HKLog :self m :Msg (Utilities|String|Append "EVENT " (Variables|Default|GetMsg)))
        (if (not (Utilities|String|EqualExactly(String) (Variables|Default|GetMsg) ""))
          (Class|BPMax|ShowNote :self m :Msg (Variables|Default|GetMsg) :Seconds (Variables|Default|GetSeconds)))
        (Utilities|IsValid (Variables|Default|GetVoice) (:"Is Valid" (Audio|PlaySound2D :Sound (Variables|Default|GetVoice) :VolumeMultiplier 1.0)))
        (if (not (Utilities|String|EqualExactly(String) (Variables|Default|GetObjective) ""))
          (Class|BPMax|SetObjectiveNote :self m :Msg (Variables|Default|GetObjective)))
        (if (not (Utilities|String|EqualExactly(String) (Variables|Default|GetHideTag) ""))
          (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "HideNow" :Time 9.0 :bLooping false))))
    (:CastFailed)))''' % MAXC)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': EV}, 'warnings_as_errors': False}))
# ---------------- phone call: voiced ----------------
OBJ1 = 'Answer your phone. Stay on Main Street.'
OBJ2 = "Walk north up Main Street to St. Brigid's Clinic. Its door is under the green light."
SAY = lambda txt, vo, secs: '(Class|BPMax|ShowNote m "%s" %s)\n    (Audio|PlaySound2D "%s" 1.0)\n    (Utilities|FlowControl|Delay %s)' % (txt, secs, VO(vo), secs)
w(PHONE + ':EventGraph', '''(event EventBeginPlay
  (Utilities|FlowControl|Delay 0.5)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0)))
  (if (not (Variables|Default|GetShown))
    (Variables|Default|SetShown true)
    (Class|BPMax|SetObjectiveNote m "%(o1)s")
    (Utilities|FlowControl|Delay 1.0)
    (Class|BPMax|ShowNote m "MILLBROOK  //  11:47 PM  //  SIX DAYS AFTER THE LETTER" 5.0)
    (Utilities|FlowControl|Delay 5.0)
    (Class|BPMax|ShowNote m "WASD  move     Mouse  look     Shift  run     F  flashlight     RMB / Q  aim  (T toggles)     LMB  fire     E  interact / doors     V  punch     B  backpack     I  workbench     G  throw     M  map     J  journal     P / Esc  pause" 10.0)
    (Utilities|FlowControl|Delay 10.0)
    (Audio|SpawnSound2D "/Game/Interface_And_Item_Sounds/WAV/Ringtone_01.Ringtone_01" 0.7)
    (Class|BPMax|ShowNote m "*  Your phone buzzes.  UNKNOWN NUMBER  *" 3.5)
    (Utilities|FlowControl|Delay 3.5)
    %(j1)s
    %(j2)s
    %(j3)s
    %(mp)s
    (Class|BPMax|SetObjectiveNote m "%(o2)s")
    (Class|BPMax|ShowNote m "NEW OBJECTIVE  (top left of the screen).  Walk up to the clinic door to go inside." 6.0)
    (Utilities|FlowControl|Delay 6.5)
    %(m1)s))''' % {'o1': OBJ1, 'o2': OBJ2,
    'j1': SAY("JAZ:  Max Hunt? Don't hang up. My name is Jaz. I used to work for Project LANTERN.", 'jaz_1', '6.0'),
    'j2': SAY("JAZ:  Your sister is alive. Emilia. They never put her in foster care. She's under St. Brigid's clinic, at the end of this street.", 'jaz_2', '8.0'),
    'j3': SAY("JAZ:  They're shutting the place down tonight, and they'll erase everything down there. Her too. The front door is open. Go. Now.", 'jaz_3', '7.5'),
    'mp': SAY("MAX:  ...Em?   (The line goes dead.)", 'max_phone', '3.0'),
    'm1': SAY("MAX:  Six days since that letter. And now a stranger calls me at midnight. Okay. Okay, Em. I'm coming.", 'max_city_1', '6.5')})
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': PHONE}, 'warnings_as_errors': False}))
# ---------------- placements ----------------
for a in call(S, 'find_actors', {'name': '', 'tag': 'CityEvents', 'collision_channels': []})['returnValue']:
    call(S, 'remove_from_scene', {'actor': a})
def put(asset, label, x, y, z, yaw=0, scale=1.0, props=None, tags=()):
    a = call(S, 'add_to_scene_from_asset', {'asset_path': asset, 'name': label, 'xform': {'location': {'x': x, 'y': y, 'z': z},
         'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}, 'scale': {'x': scale, 'y': scale, 'z': scale}}})
    a = a.get('returnValue') if isinstance(a, dict) else None
    if not a: print('FAIL', label); return None
    if props: print(label, call(O, 'set_properties', {'instance': a, 'values': json.dumps(props)}).get('returnValue'))
    for t in ('CityEvents',) + tuple(tags): call(AT, 'add_tag', {'actor': a, 'tag': t})
    call(AT, 'set_label', {'actor': a, 'label': label}); call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'City/Prologue'})
    return a
V = '/Game/AssetsvilleTown/Meshes/Vehicles/'
HH = '/Game/Horror_Hospital/Meshes/'
B = '/Game/HollowKin/Blueprints/'
FENCE = '/Game/Mega_Street_Props_Pack/Street_Props_pack_V2/Meshes/SM_Fence_2_A.SM_Fence_2_A'
SO = lambda i: {'refPath': VO(i)}
# 1) police car + radio + a bottle to throw
put(V + 'SK_veh_PoliceCarSedan_01.SK_veh_PoliceCarSedan_01', 'PR_PoliceCar', -5200, -150, 0, yaw=18)
put(EV, 'PR_Radio', -5200, -150, 0, props={'Radius': 750.0, 'Seconds': 7.0, 'Flash': True, 'Voice': SO('radio_1'),
    'Msg': "A patrol car, doors open, engine still ticking. The radio crackles:  'All units, avoid Main Street. State quarantine order is in effect. Do not engage.'"})
put(B + 'Items/BP_Pickup.BP_Pickup', 'PR_Bottle', -5050, -520, 40, props={'PickupKind': 6, 'Amount': 1})
# 2) missing posters on a fence
for i in range(4):
    put(FENCE, 'PR_Fence%d' % i, -2300 + i * 300, -1500, 0, yaw=0)
for i, k in enumerate(['SM_Image_Board_02_v01', 'SM_Board_04_v01', 'SM_Image_Board_05_v01', 'SM_Board_01_v01', 'SM_Image_Board_02_v01']):
    put(HH + k + '.' + k, 'PR_Poster%d' % i, -2250 + i * 230, -1490, 110 + (i % 2) * 30, yaw=180)
put(EV, 'PR_Posters', -1800, -1150, 0, props={'Radius': 520.0, 'Seconds': 7.0, 'Voice': SO('max_city_2'),
    'Msg': "MISSING.  MISSING.  MISSING.  A fence papered with faded posters of children. Every one says 'last seen in state care'."})
# 3) the child in the gown (cutscene), gone afterwards
put(B + 'Props/BP_Child.BP_Child', 'PR_GownChild', 3600, -1650, 2, yaw=180, tags=('PrologueGhost',))
put(B + 'Interactables/BP_Cutscene.BP_Cutscene', 'CS_City_Child', 1500, -800, 100, props={'Radius': 320.0, 'Hold': 4.2,
    'CamOffset': {'x': -250, 'y': 150, 'z': 110}, 'LookOffset': {'x': 2100, 'y': -850, 'z': 60},
    'Line1': "Under the last working streetlight: a small figure in a hospital gown. Barefoot in the rain. Watching you.",
    'Line2': "MAX:  Hey! Hey, wait! ...Em?", 'Voice2': SO('max_city_3'),
    'Line3': "You blink. The street is empty. Only small wet footprints, leading toward the clinic."})
put(EV, 'PR_ChildGone', 1500, -800, 0, props={'Radius': 320.0, 'HideTag': 'PrologueGhost'})
# 4) Jaz calls back
put(EV, 'PR_JazCall2', 4500, -800, 0, props={'Radius': 400.0, 'Seconds': 6.0, 'Voice': SO('jaz_4'),
    'Msg': "JAZ:  Max, it's Jaz. Whatever you just saw out there, don't follow it. Get inside the clinic. Now."})
# 5) crashed ambulance
put(V + 'SK_veh_Van_01.SK_veh_Van_01', 'PR_Ambulance', 7300, -250, 0, yaw=35)
put(B + 'Props/BP_DeadNurse.BP_DeadNurse', 'PR_Paramedic', 7050, -620, 0, yaw=200,
    props={'PoseAnim': {'refPath': '/Game/DeadBodies_Poses_nikoff/Animations/AS_DeadBody_Pose_Lie_05.AS_DeadBody_Pose_Lie_05'}})
put(HH + 'SM_Stretcher_02_v01.SM_Stretcher_02_v01', 'PR_Stretcher', 6900, -350, 0, yaw=80)
put(B + 'Items/BP_Pickup.BP_Pickup', 'PR_Gel', 6950, -420, 40, props={'PickupKind': 1, 'Amount': 1})
put(EV, 'PR_AmbulanceNote', 7200, -700, 0, props={'Radius': 450.0, 'Seconds': 7.0,
    'Msg': "An ambulance, nose-first into a lamp post. The back doors hang open. The stretcher is empty. The straps were cut from the inside."})
# 6) the door
put(EV, 'PR_Door', 7950, -800, 0, props={'Radius': 380.0, 'Seconds': 4.0, 'Voice': SO('max_city_4'),
    'Msg': "MAX:  St. Brigid's. Every light on, and nobody home."})
print(call(A, 'save_assets', {'asset_paths': []}))
