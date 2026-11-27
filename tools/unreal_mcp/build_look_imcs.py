"""Sensitivity / invert-Y without touching the sample's IMC at runtime: ten small mapping contexts
/Game/HollowKin/Input/Look/IMC_Look_<pct>[_Inv] (mouse + gamepad look only, scalars pre-set). BP_Max.ApplyInputPrefs
adds the chosen one above IMC_Sandbox (higher priority wins the Mouse2D / right stick keys)."""
from ui_lib import call
import json
A = 'editor_toolset.toolsets.asset.AssetTools'
O = 'editor_toolset.toolsets.object.ObjectTools'
SRC = '/Game/Input/IMC_Sandbox'
D = '/Game/HollowKin/Input/Look'
call(A, 'create_folder', {'path': D})
src = json.loads(call(O, 'get_properties', {'instance': {'refPath': SRC + '.IMC_Sandbox'}, 'properties': ['DefaultKeyMappings']})['returnValue'])['DefaultKeyMappings']
maps = src['mappings'] if isinstance(src, dict) else src
keep = [m for m in maps if m.get('action', {}).get('refPath', '').split('.')[-1] in ('IA_Look', 'IA_Look_Gamepad')]
print('look mappings', len(keep))
made = []
for pct in (50, 75, 100, 125, 150):
    for inv in (False, True):
        name = 'IMC_Look_%d%s' % (pct, '_Inv' if inv else '')
        path = D + '/' + name
        if not call(A, 'exists', {'path': path}).get('returnValue'):
            call(A, 'duplicate', {'path': SRC, 'new_path': path})
        obj = path + '.' + name
        mk = json.loads(json.dumps(keep).replace(SRC + '.IMC_Sandbox:', obj + ':'))
        val = dict(src, mappings=mk) if isinstance(src, dict) else mk
        r = call(O, 'set_properties', {'instance': {'refPath': obj}, 'values': json.dumps({'DefaultKeyMappings': val})})
        k = pct / 100.0; sy = -1.0 if inv else 1.0
        call(O, 'set_properties', {'instance': {'refPath': obj + ':InputModifierScalar_1'}, 'values': json.dumps({'Scalar': {'x': 0.3 * k, 'y': -0.3 * k * sy, 'z': 1}})})
        call(O, 'set_properties', {'instance': {'refPath': obj + ':InputModifierScalar_0'}, 'values': json.dumps({'Scalar': {'x': 90 * k, 'y': 70 * k * sy, 'z': 1}})})
        made.append(path)
print(call(A, 'save_assets', {'asset_paths': made}))
chk = json.loads(call(O, 'get_properties', {'instance': {'refPath': D + '/IMC_Look_150_Inv.IMC_Look_150_Inv'}, 'properties': ['DefaultKeyMappings']})['returnValue'])['DefaultKeyMappings']
cm = chk['mappings'] if isinstance(chk, dict) else chk
print([(m['action']['refPath'].split('.')[-1], m.get('key'), [x['refPath'].split(':')[-1] for x in m.get('modifiers', [])]) for m in cm])
print(call(O, 'get_properties', {'instance': {'refPath': D + '/IMC_Look_150_Inv.IMC_Look_150_Inv:InputModifierScalar_1'}, 'properties': ['Scalar']}))
