"""Tightens menu typography so nothing overflows its panel on any screen shape:
letter spacing cut roughly in half, long captions/footers wrap at the panel width, one footer shortened."""
from ui_lib import *
M = '/Game/HollowKin/UI/Menus/'
D = '/Game/HollowKin/UI/Diegetic/'
# name -> (letterSpacing, wrapAt or None, new text or None)
POP = {'Cap': (150, 560, None), 'Head': (200, None, None), 'Foot': (100, 560, None)}
PLAN = {
    M + 'WBP_MainMenu.WBP_MainMenu': {'Cap': (220, None, None), 'Title': (250, None, None), 'Sub': (180, None, None),
        'CardCap': (80, None, None), 'CardFoot': (40, None, 'HALVORSEN BIOLOGICS  //  REF 0611-L04'), 'Build': (200, None, None)},
    M + 'WBP_Difficulty.WBP_Difficulty': dict(POP, Foot=(80, 560, 'EASY: LESS DAMAGE, MORE SUPPLIES.  BRUTAL: HARDER HITS, FEWER SUPPLIES.')),
    M + 'WBP_PauseMenu.WBP_PauseMenu': POP,
    M + 'WBP_Settings.WBP_Settings': POP,
    D + 'WBP_DeathScreen.WBP_DeathScreen': {'Cap': (220, None, None), 'Head': (350, None, None), 'Sub': (220, None, None)},
}
for w, plan in PLAN.items():
    ws = call(U, 'GetWidgets', {'widgetBlueprint': {'refPath': w}})['returnValue']['widgets']
    for x in ws:
        if x['widgetClassPath']['refPath'] != '/Script/UMG.TextBlock':
            continue
        ref = x['widget']['refPath']; name = ref.split('.')[-1]
        f = json.loads(call(O, 'get_properties', {'instance': {'refPath': ref}, 'properties': ['Font']})['returnValue'])['Font']
        if name in plan:
            ls, wrap, text = plan[name]
        elif name.startswith('Btn') and name.endswith('Label'):
            ls, wrap, text = 200, None, None
        elif name.startswith('Row'):
            ls, wrap, text = 60, None, None
        else:
            continue
        f['letterSpacing'] = ls
        v = {'font': f}
        if wrap: v.update({'autoWrapText': True, 'wrapTextAt': wrap})
        if text: v['text'] = text
        setp(ref, v)
    print(w.split('.')[-1], call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': w}}))
