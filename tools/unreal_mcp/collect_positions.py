"""Collects the world positions of every objective actor in each level (for playtest_full.py) -> route_positions.json."""
import json
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
LEVELS = {'Lvl_City': 'City/Lvl_City', 'Lvl_Clinic': 'Clinic/Lvl_Clinic', 'Lvl_ContainmentWing': 'Containment/Lvl_ContainmentWing',
          'Lvl_Wards': 'Wards/Lvl_Wards', 'Lvl_DeepLabs': 'Deep/Lvl_DeepLabs'}
KEYS = ('BP_LevelDoor', 'BP_PhoneCall', 'BP_Pickup', 'BP_BreakerPanel', 'BP_PowerDoor', 'BP_GunPickup', 'BP_HollowChild', 'BP_EndingTrigger',
        'BP_FloorLift', 'BP_Keycard', 'BP_SeqSwitch', 'BP_FloorGenerator', 'BP_SaveTerminal', 'BP_Emilia', 'BP_Cutscene', 'PlayerStart', 'BP_HollowDrone', 'BP_Guard')
out = {}
for lv, path in LEVELS.items():
    call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []})
    call(S, 'load_level', {'level_path': '/Game/HollowKin/Maps/' + path})
    assert str(call(S, 'get_current_level', {})['returnValue']).endswith(lv)
    items = []
    acts = None
    for attempt in range(4):
        try:
            acts = call(S, 'find_actors', {'name': '', 'tag': '', 'collision_channels': []})['returnValue']; break
        except Exception as e:
            print('retry', lv, e)
    for a in acts or []:
        cls = a['refPath'].split('.')[-1]
        k = next((k for k in KEYS if cls.startswith(k)), None)
        if not k: continue
        t = call(AT, 'get_actor_transform', {'actor': a})['returnValue']['location']
        lbl = call(AT, 'get_label', {'actor': a}).get('returnValue', '')
        extra = {}
        if k == 'BP_Pickup':
            try: extra = json.loads(call(O, 'get_properties', {'instance': a, 'properties': ['PickupKind', 'Amount']})['returnValue'])
            except Exception: pass
        items.append(dict(cls=k, label=lbl, ref=a['refPath'], x=t['x'], y=t['y'], z=t['z'], **extra))
    out[lv] = items
    print(lv, len(items), sorted({i['cls'] for i in items}))
json.dump(out, open('route_positions.json', 'w'), indent=1)
