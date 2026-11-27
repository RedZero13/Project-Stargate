"""Lvl_City: the demo map's vehicles (skeletal meshes) had no working collision, so the player walked into them.
Adds a BlockAll box (VehicleBlocker) sized to each vehicle's bounds. Re-runnable."""
from ui_lib import call
import json
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
acts = call(S, 'find_actors', {'name': 'veh', 'tag': '', 'collision_channels': []})['returnValue']
n = 0
for a in acts:
    comps = call(AT, 'get_components', {'actor': a, 'component_type': {'refPath': '/Script/Engine.BoxComponent'}})['returnValue']
    box = next((c for c in comps if 'VehicleBlocker' in c['refPath']), None)
    if not box:
        r = call(AT, 'add_component', {'owner': a, 'component_type': {'refPath': '/Script/Engine.BoxComponent'}, 'name': 'VehicleBlocker'})
        box = r.get('returnValue') if isinstance(r, dict) else None
        if not box: print('fail', a['refPath'][-40:], r); continue
    b = call(AT, 'get_actor_bounds', {'actor': a})['returnValue']
    mn, mx = b['min'], b['max']
    c = {k: (mn[k] + mx[k]) / 2 for k in 'xyz'}; e = {k: (mx[k] - mn[k]) / 2 for k in 'xyz'}
    # world-space box: absolute location/rotation, extents slightly inside the axis-aligned bounds
    call(O, 'set_properties', {'instance': box, 'values': json.dumps({
        'bAbsoluteLocation': True, 'bAbsoluteRotation': True, 'bAbsoluteScale': True,
        'RelativeLocation': c, 'RelativeRotation': {'pitch': 0, 'yaw': 0, 'roll': 0}, 'RelativeScale3D': {'x': 1, 'y': 1, 'z': 1},
        'BoxExtent': {'x': e['x'] * 0.88, 'y': e['y'] * 0.88, 'z': e['z']},
        'bHiddenInGame': True})})
    call(O, 'set_properties', {'instance': box, 'values': json.dumps({'BodyInstance': {'collisionProfileName': 'BlockAll', 'collisionEnabled': 'QueryAndPhysics', 'objectType': 'ECC_WorldStatic',
        'collisionResponses': {'responseArray': [{'channel': ch, 'response': 'ECR_Block'} for ch in ('WorldStatic', 'WorldDynamic', 'Pawn', 'Visibility', 'Camera', 'PhysicsBody', 'Vehicle', 'Destructible')]}}})})
    n += 1
print('vehicles', len(acts), 'blockers added', n)
