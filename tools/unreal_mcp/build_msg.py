"""Adds the on-screen message panel (MsgBox/MsgText) to WBP_ScreenFX: big readable hint/notice text,
bottom centre, Barlow Semi Condensed on a dark translucent plate. Run once (removes an old MsgBox first)."""
from menu_common import *
F_BODY = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
W = Wbp('/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX')
brush, txt, box, cslot, bslot, rule, button = mk(W)
call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget('MsgBox')}})
W.count['Root'] = 20
b, s = box('MsgBox', 'Root', '050607', 0.72, padding={'left': 36, 'top': 16, 'right': 36, 'bottom': 18})
cslot(s, 0.5, 1.0, 0, -96, 0, 0, alx=0.5, aly=1.0)
setp(s, {'bAutoSize': True})
setp(b, {'visibility': 'Collapsed'})
t, s2 = W.add('TextBlock', 'MsgText', 'MsgBox')
setp(t, {'text': 'Message', 'justification': 'Center', 'autoWrapText': True, 'wrapTextAt': 1300,
         'colorAndOpacity': {'specifiedColor': col('ece4d2'), 'colorUseRule': 'UseColor_Specified'},
         'shadowOffset': {'x': 2, 'y': 2}, 'shadowColorAndOpacity': {'r': 0, 'g': 0, 'b': 0, 'a': 0.9},
         'font': {'fontObject': F_BODY, 'typefaceFontName': 'Default', 'size': 30, 'letterSpacing': 40}})
for n in ('MsgBox', 'MsgText'):
    print(n, call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True}))
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
