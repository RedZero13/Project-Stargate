"""Containment Wing: replaces the two mannequin dead bodies (D_C1_DeadGuard, D_C5_DeadOrderly) with BP_DeadSoldier
(tactical soldier outfit) and adds four more fallen soldiers. Tag SliceSoldiers, folder Slice/Dressing. Re-runnable."""
from ui_lib import call
import json
S = 'editor_toolset.toolsets.scene.SceneTools'
AT = 'editor_toolset.toolsets.actor.ActorTools'
O = 'editor_toolset.toolsets.object.ObjectTools'
BP = '/Game/HollowKin/Blueprints/Props/BP_DeadSoldier.BP_DeadSoldier'
A = '/Game/DeadBodies_Poses_nikoff/Animations/'
SOLDIERS = [  # label, pose, x, y, z, yaw
    ('DS_C1_Guard', 'AS_DeadBody_Pose_Sit_01', 480, -255, 0, 0),       # replaces the fallen mannequin at the start
    ('DS_C1_Second', 'AS_DeadBody_Pose_Lie_02', 260, 120, 0, 130),
    ('DS_C2_Decon', 'AS_DeadBody_Pose_Lie_05', 1650, 40, 0, 200),
    ('DS_C4_Ring', 'AS_DeadBody_Pose_Sit_03', 3800, 480, 0, 270),
    ('DS_C5_Cells', 'AS_DeadBody_Pose_Lie_04', 4700, -800, 0, 60),     # replaces the dead orderly
    ('DS_C7_Isolation', 'AS_DeadBody_Pose_Lie_08', 5950, -900, 0, 90),
]
def find(name='', tag=''):
    return call(S, 'find_actors', {'name': name, 'tag': tag, 'collision_channels': []})['returnValue']
for old in find('D_C1_DeadGuard') + find('D_C5_DeadOrderly') + find(tag='SliceSoldiers'):
    print('remove', old['refPath'].split('.')[-1], call(S, 'remove_from_scene', {'actor': old}))
for label, pose, x, y, z, yaw in SOLDIERS:
    a = call(S, 'add_to_scene_from_asset', {'asset_path': BP, 'name': label,
        'xform': {'location': {'x': x, 'y': y, 'z': z}, 'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}}})['returnValue']
    call(O, 'set_properties', {'instance': a, 'values': json.dumps({'PoseAnim': {'refPath': A + pose + '.' + pose}})})
    call(AT, 'add_tag', {'actor': a, 'tag': 'SliceSoldiers'})
    call(AT, 'set_label', {'actor': a, 'label': label})
    call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Slice/Dressing'})
    print('placed', label)
