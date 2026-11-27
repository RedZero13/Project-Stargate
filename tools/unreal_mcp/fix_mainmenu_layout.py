"""Main menu layout: menu column tall enough for five buttons (no overlap with the build label), CREDITS button
content aligned like the others, build label lower."""
from ui_lib import *
MM = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'
ws = call(U, 'GetWidgets', {'widgetBlueprint': {'refPath': MM}})['returnValue']['widgets']
slots = {x['widget']['refPath'].split('.')[-1]: x['slot']['refPath'] for x in ws if isinstance(x.get('slot'), dict)}
ref = json.loads(call(O, 'get_properties', {'instance': {'refPath': slots['BtnQuitRow']}, 'properties': ['HorizontalAlignment', 'VerticalAlignment', 'Padding']})['returnValue'])
print('quit row slot', ref)
setp(slots['BtnCreditsRow'], {'horizontalAlignment': ref['HorizontalAlignment'], 'verticalAlignment': ref['VerticalAlignment'], 'padding': ref['Padding']})
setp(slots['Left'], {'layoutData': {'offsets': {'left': 140, 'top': -20, 'right': 640, 'bottom': 760}, 'anchors': {'minimum': {'x': 0, 'y': 0.5}, 'maximum': {'x': 0, 'y': 0.5}}, 'alignment': {'x': 0, 'y': 0.5}}})
setp(slots['Build'], {'layoutData': {'offsets': {'left': 140, 'top': -36, 'right': 400, 'bottom': 20}, 'anchors': {'minimum': {'x': 0, 'y': 1}, 'maximum': {'x': 0, 'y': 1}}, 'alignment': {'x': 0, 'y': 1}}})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': MM}}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/HollowKin/UI/Menus/WBP_MainMenu']}))
