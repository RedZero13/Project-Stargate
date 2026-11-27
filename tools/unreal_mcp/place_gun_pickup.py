"""Places BP_GunPickup next to the first dead soldier in C1 (DS_C1_Guard), facing him. Tag SliceGunPickup."""
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'
for old in call(S, 'find_actors', {'name': '', 'tag': 'SliceGunPickup', 'collision_channels': []})['returnValue']:
    call(S, 'remove_from_scene', {'actor': old})
a = call(S, 'add_to_scene_from_asset', {'asset_path': '/Game/HollowKin/Blueprints/Interactables/BP_GunPickup.BP_GunPickup', 'name': 'GunPickup_C1',
          'xform': {'location': {'x': 480, 'y': -135, 'z': 100}, 'rotation': {'pitch': 0, 'yaw': -90, 'roll': 0}}})['returnValue']
call(AT, 'add_tag', {'actor': a, 'tag': 'SliceGunPickup'}); call(AT, 'set_label', {'actor': a, 'label': 'GunPickup_C1'})
call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Slice/Gameplay'})
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
