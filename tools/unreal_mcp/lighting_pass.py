"""Lighting pass: clamp auto-exposure in every level's unbound post-process volume so dark basements lift to a
readable level without lit rooms blowing out, with a per-level bias (clinic neutral, basements brighter)."""
import sys, json
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
LV = {'Lvl_Clinic': 0.0, 'Lvl_ContainmentWing': 0.7, 'Lvl_Wards': 0.6, 'Lvl_DeepLabs': 0.9, 'Lvl_City': 0.3}
for lv, bias in LV.items():
    path = {'Lvl_Clinic': 'Clinic/Lvl_Clinic', 'Lvl_ContainmentWing': 'Containment/Lvl_ContainmentWing', 'Lvl_Wards': 'Wards/Lvl_Wards',
            'Lvl_DeepLabs': 'Deep/Lvl_DeepLabs', 'Lvl_City': 'City/Lvl_City'}[lv]
    call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []})
    call(S, 'load_level', {'level_path': '/Game/HollowKin/Maps/' + path})
    if not str(call(S, 'get_current_level', {})['returnValue']).endswith(lv):
        print('could not open', lv); continue
    for a in call(S, 'find_actors', {'name': 'PostProcess', 'tag': '', 'collision_channels': []})['returnValue']:
        st = json.loads(call(O, 'get_properties', {'instance': a, 'properties': ['Settings']})['returnValue'])['Settings']
        st.update({'bOverride_AutoExposureMinBrightness': True, 'autoExposureMinBrightness': -1.5,
                   'bOverride_AutoExposureMaxBrightness': True, 'autoExposureMaxBrightness': 3.0,
                   'bOverride_AutoExposureBias': True, 'autoExposureBias': bias,
                   'bOverride_AutoExposureSpeedUp': True, 'autoExposureSpeedUp': 2.0,
                   'bOverride_AutoExposureSpeedDown': True, 'autoExposureSpeedDown': 1.0})
        r = call(O, 'set_properties', {'instance': a, 'values': json.dumps({'Settings': st})})
        print(lv, a['refPath'][-30:], r)
    print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
