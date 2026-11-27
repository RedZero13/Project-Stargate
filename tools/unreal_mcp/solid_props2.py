"""Collision for the meshes added with layout v2 (washrooms, cafeteria cart, lab kit, door and lift leaves, puzzle props)."""
from ui_lib import call
HH = '/Game/Horror_Hospital/Meshes/'
MESHES = [HH + m + '.' + m for m in ('SM_Toilet_01_v1', 'SM_Washstand_01_v1', 'SM_Box_01_v01', 'SM_Pathology_Microscope_01_v01', 'SM_Lift_01_p02',
          'SM_Lift_01_p03', 'SM_Door_01_p01', 'SM_Computer_Monitor_01_v01', 'SM_Scanner_Monitor_01_v1', 'SM_Board_04_v01')] + \
         ['/Game/RestaurantScene/Meshes/SM_UtilityCart.SM_UtilityCart']
for m in MESHES:
    hulls = 1 if any(k in m for k in ('Lift_01_p0', 'Door_01_p01', 'Board_04')) else 4     # flat leaves: one box-like hull
    r = call('editor_toolset.toolsets.static_mesh.StaticMeshTools', 'generate_convex_collisions', {'mesh': {'refPath': m}, 'hull_count': hulls, 'max_hull_verts': 16, 'hull_precision': 60000})
    print(m.split('.')[-1], r)
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
