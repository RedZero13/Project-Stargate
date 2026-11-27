"""Main menu fit (2026-11-27): ACHIEVEMENTS lines up with the other buttons (its row was centred), and the button
column is tighter (6 px instead of 10 px vertical padding) and sits higher, so DISCHARGE no longer runs into the
PRE-ALPHA footer in a windowed game."""
import json
from ui_lib import *
W = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'; T = W + ':WidgetTree.'
ws = call(U, 'GetWidgets', {'widgetBlueprint': {'refPath': W}})['returnValue']['widgets']
PAD = {'left': 20, 'top': 6, 'right': 80, 'bottom': 6}
for x in ws:
    n = x['widget']['refPath'].split('.')[-1]
    if not isinstance(x['slot'], dict): continue
    if n.startswith('Btn') and n.endswith('Row'):
        setp(x['slot']['refPath'], {'HorizontalAlignment': 'HAlign_Left'})
    if n.startswith('Btn') and n.endswith('Label'):
        setp(x['slot']['refPath'], {'Padding': {'left': 16, 'top': 6, 'right': 16, 'bottom': 6}})
    if x['widgetClassPath']['refPath'].endswith('.Button'):
        st = json.loads(call(O, 'get_properties', {'instance': x['widget'], 'properties': ['WidgetStyle']})['returnValue'])['WidgetStyle']
        st['normalPadding'] = PAD; st['pressedPadding'] = PAD
        setp(x['widget']['refPath'], {'WidgetStyle': st})
    if n == 'Left':
        setp(x['slot']['refPath'], {'LayoutData': {'offsets': {'left': 140, 'top': -70, 'right': 640, 'bottom': 720},
             'anchors': {'minimum': {'x': 0, 'y': 0.5}, 'maximum': {'x': 0, 'y': 0.5}}, 'alignment': {'x': 0, 'y': 0.5}}})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': W}}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/HollowKin/UI/Menus/WBP_MainMenu']}))
