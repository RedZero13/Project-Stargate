"""Menus must not use the engine fallback font (Roboto). menu_common.mk() text helpers leave the font object unset, so
after (re)building a menu run this: labels/headers -> Barlow SemiBold, longer body text (recaps, questions) -> Barlow
Medium. Size and letter spacing are kept. The HUD / diegetic widgets keep their own fonts and are not touched."""
from ui_lib import *
A = 'editor_toolset.toolsets.asset.AssetTools'
SEMI = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
MED = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-Medium_Font.BarlowSemiCondensed-Medium_Font'
MENUS = ['Achievements', 'Chapters', 'Choice', 'Credits', 'Journal', 'MainMenu', 'PauseMenu', 'Settings', 'Difficulty', 'Backpack', 'Loading']
for m in MENUS:
    w = '/Game/HollowKin/UI/Menus/WBP_%s.WBP_%s' % (m, m); n = 0
    for x in call(U, 'GetWidgets', {'widgetBlueprint': {'refPath': w}})['returnValue']['widgets']:
        if not x['widgetClassPath']['refPath'].endswith('.TextBlock'): continue
        ref = x['widget']['refPath']; name = ref.split('.')[-1]
        f = json.loads(call(O, 'get_properties', {'instance': {'refPath': ref}, 'properties': ['Font']})['returnValue'])['Font']
        if 'Roboto' not in str(f.get('fontObject')): continue
        body = name.startswith(('Recap', 'Desc', 'Body')) or name == 'Q'
        f['fontObject'] = {'refPath': MED if body else SEMI}; f['typefaceFontName'] = 'Default'
        setp(ref, {'Font': f}); n += 1
    if n:
        print(m, n, 'fixed', call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': w}}))
        call(A, 'save_assets', {'asset_paths': [w.split('.')[0]]})
