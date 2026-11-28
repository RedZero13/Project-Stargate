"""iPad move / look sticks: TI_HollowKin (copy of the engine's DefaultVirtualJoysticks, kept in the project so it is
always cooked: DefaultGame.ini DirectoriesToAlwaysCook /Game/HollowKin/UI/Touch; Config/IOS/IOSInput.ini points to it
and BP_Max.AddTouchHUD activates it). Bigger sticks, further in from the corners; they fade when not touched."""
from ui_lib import call, O
import json
A = 'editor_toolset.toolsets.asset.AssetTools'
P = '/Game/HollowKin/UI/Touch/TI_HollowKin'
if not call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'duplicate', {'path': '/Engine/MobileResources/HUD/DefaultVirtualJoysticks', 'new_path': P})
ref = {'refPath': P + '.TI_HollowKin'}
c = json.loads(call(O, 'get_properties', {'instance': ref, 'properties': ['Controls']})['returnValue'])['Controls']
for ctl, cx in zip(c, (230, -230)):
    ctl.update({'center': {'x': cx, 'y': -230}, 'visualSize': {'x': 250, 'y': 250}, 'thumbSize': {'x': 120, 'y': 120},
                'interactionSize': {'x': 420, 'y': 380}})
print(call(O, 'set_properties', {'instance': ref, 'values': json.dumps({'Controls': c, 'InactiveOpacity': 0.35, 'ActiveOpacity': 0.9})}))
print(call(A, 'save_assets', {'asset_paths': [P]}))
