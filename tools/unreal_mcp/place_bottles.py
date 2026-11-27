"""Containment Wing: glass bottles (BP_Pickup kind 6) for the bottle lure, plus one extra health gel and sedative
now that they are carried in the backpack. Tag SliceBottles. Re-runnable."""
from ui_lib import call
import json
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
ITEMS = [('PU_Bottle_C1', 6, 1, 640, 170, 40), ('PU_Bottle_C2', 6, 1, 2250, -120, 40), ('PU_Bottle_C4', 6, 1, 3700, -420, 40),
         ('PU_Gel_C2', 1, 40, 1500, 120, 40), ('PU_Sed_C4', 2, 35, 3900, 450, 40)]
for old in call(S, 'find_actors', {'name': '', 'tag': 'SliceBottles', 'collision_channels': []})['returnValue']:
    call(S, 'remove_from_scene', {'actor': old})
for label, kind, amt, x, y, z in ITEMS:
    a = call(S, 'add_to_scene_from_asset', {'asset_path': '/Game/HollowKin/Blueprints/Items/BP_Pickup.BP_Pickup', 'name': label,
              'xform': {'location': {'x': x, 'y': y, 'z': z}}})['returnValue']
    call(O, 'set_properties', {'instance': a, 'values': json.dumps({'PickupKind': kind, 'Amount': amt})})
    call(AT, 'add_tag', {'actor': a, 'tag': 'SliceBottles'}); call(AT, 'set_label', {'actor': a, 'label': label})
    call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Slice/Gameplay'})
    print('placed', label)
