"""Deep Labs gameplay (tag DeepGP): enemies, AK guards, the brute, hazards, pickups (rewards in the tunnel dead
ends), save room, hints, fallen soldiers, ambience + music, and Emilia (BP_Emilia: Modern City Girl model at child
scale, idle, speaks when Max comes close) with the ending trigger in L-03. Re-runnable."""
from ui_lib import call
import json
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
B = '/Game/HollowKin/Blueprints/'
EM = B + 'Props/BP_Emilia.BP_Emilia'
# ---- BP_Emilia ---------------------------------------------------------------------------
if not call(A, 'exists', {'path': EM.split('.')[0]}).get('returnValue'):
    print(call(BT, 'create', {'folder_path': '/Game/HollowKin/Blueprints/Props', 'asset_name': 'BP_Emilia', 'asset_type': {'refPath': '/Script/Engine.Actor'}}))
call(BT, 'add_variable', {'blueprint': {'refPath': EM}, 'name': 'bSpoke', 'type_name': 'bool'})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': EM}, 'warnings_as_errors': False})
print('Emilia BeginPlay', call(BT, 'write_graph_dsl', {'graph': {'refPath': EM + ':EventGraph'}, 'code': '''(event EventBeginPlay
  (bind lead (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Components|SkeletalMesh|SetSkeletalMeshAsset lead "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple")
  (Components|Animation|PlayAnimation lead "/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle.MM_Idle" true)
  (bind look (Utilities|Casting|CastToSkeletalMeshComponent (Game|AddComponentbyClass self "/Script/Engine.SkeletalMeshComponent")))
  (Transformation|AttachComponentToComponent look lead "None" "SnapToTarget" "SnapToTarget" "SnapToTarget")
  (Components|SkeletalMesh|SetSkeletalMeshAsset look "/Game/civilian_girl/meshes/SKM_army_girl.SKM_army_girl")
  (Components|SkinnedMesh|SetLeaderPoseComponent look lead)
  (Rendering|SetRenderInMainPass :self lead :bValue false)
  (Rendering|SetRenderinDepthPass :self lead :bValue false)
  (Rendering|SetCastShadow :self lead :NewCastShadow false)
  (Transformation|SetActorScale3D :self self :NewScale3D (Math|Vector|MakeVector 0.82 0.82 0.82)))'''}))
print('Emilia Tick', call(BT, 'write_graph_dsl', {'graph': {'refPath': EM + ':EventGraph'}, 'code': '''(event EventTick (DeltaSeconds)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then
      (if (and (not (Variables|Default|GetSpoke)) (< (Transformation|GetDistanceTo self m) 650.0))
        (Variables|Default|SetSpoke true)
        (Class|BPMax|ShowNote :self m :Msg "EMILIA:  ...Max?  You came.  They told me you'd forgotten me.  Don't come closer if you're scared of what I am now." :Seconds 7.0)
        (Class|BPMax|SetObjectiveNote :self m :Msg "Go to Emilia.")))
    (:CastFailed)))'''}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': EM}, 'warnings_as_errors': False}))
# ---- placement ---------------------------------------------------------------------------
assert 'Lvl_DeepLabs' in call(S, 'get_current_level', {})['returnValue']
for old in call(S, 'find_actors', {'name': '', 'tag': 'DeepGP', 'collision_channels': []})['returnValue']:
    call(S, 'remove_from_scene', {'actor': old})
def put(cls, label, x, y, z=100, yaw=0, scale=1.0, props=None, tags=(), folder='Deep/Gameplay'):
    a = call(S, 'add_to_scene_from_asset', {'asset_path': cls, 'name': label, 'xform': {'location': {'x': x, 'y': y, 'z': z},
         'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}, 'scale': {'x': scale, 'y': scale, 'z': scale}}})
    a = a.get('returnValue') if isinstance(a, dict) else None
    if not a: print('FAIL', label); return None
    if props: call(O, 'set_properties', {'instance': a, 'values': json.dumps(props)})
    for t in ('DeepGP',) + tuple(tags): call(AT, 'add_tag', {'actor': a, 'tag': t})
    call(AT, 'set_label', {'actor': a, 'label': label}); call(S, 'set_actor_folder', {'actor': a, 'folder_path': folder})
    return a
DR = B + 'AI/BP_HollowDrone.BP_HollowDrone'; GD = B + 'AI/BP_Guard.BP_Guard'
for lbl, x, y in (('D2_Hollow', 1650, 300), ('D4_Hollow', 2800, -500), ('D5_Hollow', 2900, 650), ('T3_Hollow', 5900, 1200), ('T5_Hollow', 6300, -300)):
    put(DR, lbl, x, y)
put(DR, 'D7_Brute', 8000, -200, 120, scale=1.3, tags=('Elite',))
put(GD, 'T7_Guard', 6950, -800); put(GD, 'D7_Guard', 8500, 450)
for lbl, x, y in (('D7_Shock1', 7700, 0), ('D7_Shock2', 8200, -700), ('D4_Shock', 2500, -650)):
    put(B + 'Interactables/BP_HazardShock.BP_HazardShock', lbl, x, y, 60, scale=0.85)
for lbl, x, y in (('D7_Barrel1', 7450, -450), ('D7_Barrel2', 8650, 150), ('D7_Barrel3', 7900, -1050)):
    put(B + 'Interactables/BP_HazardBarrel.BP_HazardBarrel', lbl, x, y, 60)
PU = B + 'Items/BP_Pickup.BP_Pickup'
for lbl, k, amt, x, y in (('D2_Ammo', 0, 6, 1000, -350), ('D4_Ammo', 0, 6, 2300, -900), ('T4_Ammo', 0, 12, 5500, 1820), ('T6_Gel', 1, 40, 5400, -800),
                          ('D5_Sed', 2, 35, 3250, 850), ('D4_Parts', 4, 1, 3300, -300), ('D5_Chem', 5, 1, 2300, 300), ('T6_Chem', 5, 1, 5450, -760),
                          ('D3_Bottle', 6, 1, 3000, 80), ('T4_Drawing', 7, 20, 5500, 1720), ('D7_Gel', 1, 40, 7300, -1300), ('D7_Ammo', 0, 6, 8700, -1300),
                          ('D8_Bottle', 6, 1, 8900, 100)):
    put(PU, lbl, x, y, 40, props={'PickupKind': k, 'Amount': amt})
put(B + 'Interactables/BP_SaveTerminal.BP_SaveTerminal', 'D6_SaveTerminal', 4400, -450, 0)
put(B + 'Interactables/BP_SafeZone.BP_SafeZone', 'D6_SafeZone', 4212, 0, 150, props=None)
for lbl, msg, x, y in (
        ('H_D1', "The lift is dead behind you. Old Halvorsen labs, emergency lights only. Emilia is somewhere below.", 500, 0),
        ('H_D3', "Diagnostic labs on either side of the hall. Supplies, and whatever they were testing.", 2100, 0),
        ('H_D6', "A records room with a working save terminal. The lamp is warm. Breathe.", 3900, 0),
        ('H_T1', "Maintenance tunnels. Some branches dead-end, but the dead ends were where people hid things. Listen before each corner.", 4700, 0),
        ('H_D7', "The old generator plant. Live puddles and fuel barrels hurt anything: use them. The big one barely feels bullets.", 7200, -800),
        ('H_D8', "A bridge over the dark. On the far side, someone is humming a lullaby you know.", 8900, 0),
        ('H_D9', "L-03.", 10100, 0)):
    put(B + 'Interactables/BP_Hint.BP_Hint', lbl, x, y, 100, props={'Message': msg})
SOL = B + 'Props/BP_DeadSoldier.BP_DeadSoldier'; AN = '/Game/DeadBodies_Poses_nikoff/Animations/'
for lbl, pose, x, y, yaw in (('DS_D2', 'AS_DeadBody_Pose_Sit_02', 1100, 260, 270), ('DS_D3', 'AS_DeadBody_Pose_Lie_06', 2500, -60, 30),
                             ('DS_T1', 'AS_DeadBody_Pose_Lie_09', 4900, 40, 160), ('DS_D7', 'AS_DeadBody_Pose_Lie_12', 7800, 600, 80), ('DS_D8', 'AS_DeadBody_Pose_Sit_05', 9200, -100, 90)):
    put(SOL, lbl, x, y, 0, yaw=yaw, props={'PoseAnim': {'refPath': AN + pose + '.' + pose}}, folder='Deep/Dressing')
put(EM, 'Emilia', 10850, 0, 92, yaw=180)
put(B + 'Interactables/BP_EndingTrigger.BP_EndingTrigger', 'D9_EndingTrigger', 10650, 0, 100)
for lbl, snd, x, y, vol in (('A_D_Labs', '/Game/HorrorAmbientSFX/HorrorAmbientSFX_wav/AMB_Drone_Corridor.AMB_Drone_Corridor', 2000, 0, 0.6),
                            ('A_D_Tunnels', '/Game/HorrorAmbientSFX/HorrorAmbientSFX_wav/AMB_Drone_Anxiety.AMB_Drone_Anxiety', 5800, 300, 0.7),
                            ('M_D_Bed', '/Game/InfinitelyCloseNightmareMusicPack/BottomDepths.BottomDepths', 3000, 0, 0.45),
                            ('M_D_Generator', '/Game/InfinitelyCloseNightmareMusicPack/HeavyPressure.HeavyPressure', 8000, 0, 0.5),
                            ('M_D_Chamber', '/Game/InfinitelyCloseNightmareMusicPack/PianoHope.PianoHope', 10650, 0, 0.6)):
    a = call(S, 'add_to_scene_from_class', {'actor_type': {'refPath': '/Script/Engine.AmbientSound'}, 'name': lbl, 'xform': {'location': {'x': x, 'y': y, 'z': 200}}})['returnValue']
    c = call(AT, 'get_components', {'actor': a, 'component_type': {'refPath': '/Script/Engine.AudioComponent'}})['returnValue'][0]
    call(O, 'set_properties', {'instance': c, 'values': json.dumps({'Sound': {'refPath': snd}, 'VolumeMultiplier': vol, 'bAutoActivate': True})})
    for t in ('DeepGP', 'DeepAudio'): call(AT, 'add_tag', {'actor': a, 'tag': t})
    call(AT, 'set_label', {'actor': a, 'label': lbl}); call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Deep/Audio'})
print(call(A, 'save_assets', {'asset_paths': []}))
