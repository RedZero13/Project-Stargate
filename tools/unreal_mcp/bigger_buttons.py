"""Bigger click areas for menu buttons (2026-11-26): each button gets 10 px top/bottom + 20/80 px side padding inside
its style (the hit area grows, the text stays put) and fills its row horizontally."""
from ui_lib import call
import json
U = 'UMGToolSet.UMGToolSet'; O = 'editor_toolset.toolsets.object.ObjectTools'
PAD = {'left': 20, 'top': 10, 'right': 80, 'bottom': 10}
for P in ['/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu', '/Game/HollowKin/UI/Menus/WBP_PauseMenu.WBP_PauseMenu',
          '/Game/HollowKin/UI/Menus/WBP_Difficulty.WBP_Difficulty', '/Game/HollowKin/UI/Menus/WBP_Credits.WBP_Credits']:
    ws = call(U, 'GetWidgets', {'widgetBlueprint': {'refPath': P}})['returnValue']['widgets']
    n = 0
    for w in ws:
        if not w['widgetClassPath']['refPath'].endswith('.Button'): continue
        st = json.loads(call(O, 'get_properties', {'instance': w['widget'], 'properties': ['WidgetStyle']})['returnValue'])['WidgetStyle']
        st['normalPadding'] = PAD; st['pressedPadding'] = PAD
        call(O, 'set_properties', {'instance': w['widget'], 'values': json.dumps({'WidgetStyle': st})})
        if w['slot'] != 'None' and 'VerticalBoxSlot' in w['slot']['refPath']:
            call(O, 'set_properties', {'instance': w['slot'], 'values': json.dumps({'Padding': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}, 'HorizontalAlignment': 'HAlign_Fill'})})
        n += 1
    print(P.split('.')[-1], n, call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': P}}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
