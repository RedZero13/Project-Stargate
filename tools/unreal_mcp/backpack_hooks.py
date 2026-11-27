"""Opens the backpack: BP_Max.OpenCase(Tab) (pauses, UI input), I key (IA_Inventory) and G key (IA_Throw) in
IMC_Combat, and the pause menu's WORKBENCH button now opens the case on the WORKBENCH tab."""
from ui_lib import call
import json, subprocess, os
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
O = 'editor_toolset.toolsets.object.ObjectTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
CASE = '/Game/HollowKin/UI/Menus/WBP_Backpack.WBP_Backpack_C'
call(BT, 'add_function_graph', {'blueprint': {'refPath': MAX}, 'graph_name': 'OpenCase'})
call(BT, 'add_function_param', {'graph': {'refPath': MAX + ':OpenCase'}, 'param_name': 'Tab', 'param_type': 'int', 'input_param': True})
print('OpenCase', call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':OpenCase'}, 'code': '''(fn OpenCase (Tab)
  (if (not (Variables|Default|GetDead))
    (bind pc (Game|GetPlayerController 0))
    (bind w (Utilities|Casting|CastToWBP_Backpack (UserInterface|CreateWidget "%s" pc)))
    (UserInterface|Viewport|AddToViewport w 25)
    (Class|WBPBackpack|ShowTab :self w :Idx Tab)
    (Game|SetGamePaused true)
    (Input|SetInputModeUIOnly pc w)
    (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor true)))''' % CASE}))
call(BT, 'add_function_graph', {'blueprint': {'refPath': MAX}, 'graph_name': 'OpenCaseItems'})
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':OpenCaseItems'}, 'code': '(fn OpenCaseItems ()\n  (CallFunction|OpenCase :Tab 0))'}))
call(BT, 'add_function_graph', {'blueprint': {'refPath': MAX}, 'graph_name': 'OpenCaseCraft'})
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':OpenCaseCraft'}, 'code': '(fn OpenCaseCraft ()\n  (CallFunction|OpenCase :Tab 1))'}))
for ia in ('IA_Inventory', 'IA_Throw', 'IA_Workbench'):
    if not call(A, 'exists', {'path': '/Game/Input/Actions/' + ia}).get('returnValue'):
        print(ia, call(A, 'duplicate', {'path': '/Game/Input/Actions/IA_Melee', 'new_path': '/Game/Input/Actions/' + ia}))
imc = '/Game/Input/IMC_Combat.IMC_Combat'
d = json.loads(call(O, 'get_properties', {'instance': {'refPath': imc}, 'properties': ['DefaultKeyMappings']})['returnValue'])['DefaultKeyMappings']
maps = [m for m in d['mappings'] if m['action']['refPath'].split('.')[-1] not in ('IA_Inventory', 'IA_Throw', 'IA_Workbench')]
for ia, keys in (('IA_Inventory', ('B', 'Gamepad_Special_Left')), ('IA_Workbench', ('I', 'Gamepad_DPad_Up')), ('IA_Throw', ('G', 'Gamepad_DPad_Down'))):
    for k in keys:
        maps.append({'triggers': [], 'modifiers': [], 'action': {'refPath': '/Game/Input/Actions/%s.%s' % (ia, ia)}, 'key': k,
                     'settingBehavior': 'InheritSettingsFromAction', 'playerMappableKeySettings': 'None'})
print(call(O, 'set_properties', {'instance': {'refPath': imc}, 'values': json.dumps({'DefaultKeyMappings': dict(d, mappings=maps)})}))
print(call(A, 'save_assets', {'asset_paths': ['/Game/Input/IMC_Combat', '/Game/Input/Actions/IA_Inventory', '/Game/Input/Actions/IA_Throw', '/Game/Input/Actions/IA_Workbench']}))
D = os.path.dirname(os.path.abspath(__file__))
for ia, f, y in (('IA_Inventory', 'OpenCaseItems', 2600), ('IA_Throw', 'ThrowBottle', 2800), ('IA_Workbench', 'OpenCaseCraft', 3000)):
    print(ia, subprocess.run([D + '/wire.sh', MAX, ia, f, str(y)], capture_output=True, text=True).stdout[-200:])
PM = '/Game/HollowKin/UI/Menus/WBP_PauseMenu.WBP_PauseMenu'
print('DoCraft', call(BT, 'write_graph_dsl', {'graph': {'refPath': PM + ':DoCraft'}, 'code': '''(fn DoCraft ()
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then
      (Widget|RemoveFromParent self)
      (Class|BPMax|OpenCase :self m :Tab 1))
    (:CastFailed)))'''}))
lab = PM + ':WidgetTree.BtnExamineLabel'
print(call(O, 'set_properties', {'instance': {'refPath': lab}, 'values': json.dumps({'Text': 'BACKPACK  /  WORKBENCH'})}))
for bp in (MAX, PM):
    print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': ['/Game/HollowKin/Blueprints/Player/BP_Max', '/Game/HollowKin/UI/Menus/WBP_PauseMenu']}))
