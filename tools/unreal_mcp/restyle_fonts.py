"""Switches every TextBlock in the menus/diegetic widgets to the project fonts:
size >= 40 -> Cinzel (titles), otherwise Barlow Semi Condensed SemiBold; text under 18 pt is raised to 18."""
from ui_lib import *
TITLE = '/Game/HollowKin/UI/Fonts/Cinzel-Variable_Font.Cinzel-Variable_Font'
BODY = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
WBPS = ['/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu', '/Game/HollowKin/UI/Menus/WBP_Difficulty.WBP_Difficulty',
        '/Game/HollowKin/UI/Menus/WBP_PauseMenu.WBP_PauseMenu', '/Game/HollowKin/UI/Menus/WBP_Settings.WBP_Settings',
        '/Game/HollowKin/UI/Diegetic/WBP_DeathScreen.WBP_DeathScreen', '/Game/HollowKin/UI/Diegetic/WBP_GunDisplay.WBP_GunDisplay',
        '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX']
for w in WBPS:
    ws = call(U, 'GetWidgets', {'widgetBlueprint': {'refPath': w}})
    ws = ws['returnValue']['widgets']
    n = 0
    for x in ws:
        if x['widgetClassPath']['refPath'] != '/Script/UMG.TextBlock':
            continue
        ref = x['widget']['refPath']
        f = json.loads(call(O, 'get_properties', {'instance': {'refPath': ref}, 'properties': ['Font']})['returnValue'])['Font']
        size = f.get('size', 24)
        if ref.endswith('MsgText') or ref.endswith('.Cross'):
            continue
        big = size >= 40
        f['fontObject'] = TITLE if big else BODY
        f['typefaceFontName'] = 'Default'
        f['size'] = max(size, 18)
        f.pop('fontMaterial', None)
        setp(ref, {'font': f})
        n += 1
    print(w.split('.')[-1], 'texts restyled:', n, call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': w}}))
