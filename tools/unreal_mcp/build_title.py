"""Splash + title layers for WBP_MainMenu (Control-style intro): animated smoke background (M_UI_MenuSmoke),
splash card 1 (prototype / Unreal Engine), splash card 2 (content warning), big centred HOLLOW KIN logo and a
pulsing PRESS ANY KEY. Animated by AnimTick (build_title_logic.py)."""
from menu_common import *
TITLE_F = '/Game/HollowKin/UI/Fonts/Cinzel-Variable_Font.Cinzel-Variable_Font'
BODY_F = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
W = Wbp('/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu')
brush, txt, box, cslot, bslot, rule, button = mk(W)
for n in ('BgSmoke', 'Splash1', 'Splash2', 'TitleLogo', 'PressText', 'TitleRule'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
def font(f, size, ls): return {'fontObject': f, 'typefaceFontName': 'Default', 'size': size, 'letterSpacing': ls}
def color(h, a=1.0): return {'specifiedColor': col(h, a), 'colorUseRule': 'UseColor_Specified'}
W.count['Root'] = 1
img, s = W.add('Image', 'BgSmoke', 'Root')
setp(img, {'brush': {'drawAs': 'Image', 'imageType': 'FullColor', 'resourceObject': '/Game/HollowKin/UI/Art/M_UI_MenuSmoke.M_UI_MenuSmoke',
           'tintColor': {'specifiedColor': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 'colorUseRule': 'UseColor_Specified'}}, 'renderOpacity': 0.0})
cslot(s, (0, 1), (0, 1), 0, 0, 0, 0)
W.count['Root'] = 200
def centred(name, lines):
    vb, s = W.add('VerticalBox', name, 'Root')
    cslot(s, 0.5, 0.5, 0, 0, 0, 0, alx=0.5, aly=0.5); setp(s, {'bAutoSize': True})
    setp(vb, {'renderOpacity': 0.0})
    for i, (text, f, size, ls, c, a) in enumerate(lines):
        t, ts = W.add('TextBlock', name + 'T%d' % i, name)
        setp(t, {'text': text, 'justification': 'Center', 'font': font(f, size, ls), 'colorAndOpacity': color(c, a),
                 'autoWrapText': False, 'wrapTextAt': 1100})
        bslot(ts, pad=(0, 8, 0, 8), h='HAlign_Center')
centred('Splash1', [('A SURVIVAL HORROR PROTOTYPE', BODY_F, 22, 600, TEAL, 0.9),
                    ('HOLLOW KIN', TITLE_F, 64, 300, WHITE, 1.0),
                    ('MADE WITH UNREAL ENGINE 5', BODY_F, 18, 400, DIM, 1.0)])
centred('Splash2', [('CONTENT WARNING', BODY_F, 24, 500, AMBER, 1.0),
                    ('This game contains violence, blood, and depictions of\nchild endangerment and psychological distress.', BODY_F, 30, 20, WHITE, 0.95),
                    ('Headphones recommended. Play in the dark.', BODY_F, 22, 60, TEAL, 0.9)])
t, s = W.add('TextBlock', 'TitleLogo', 'Root')
setp(t, {'text': 'HOLLOW KIN', 'justification': 'Center', 'font': font(TITLE_F, 168, 250), 'colorAndOpacity': color(WHITE),
         'shadowOffset': {'x': 0, 'y': 4}, 'shadowColorAndOpacity': {'r': 0, 'g': 0, 'b': 0, 'a': 0.85}, 'renderOpacity': 0.0})
cslot(s, 0.5, 0.46, 0, 0, 0, 0, alx=0.5, aly=0.5); setp(s, {'bAutoSize': True})
t, s = W.add('TextBlock', 'PressText', 'Root')
setp(t, {'text': 'PRESS ANY KEY', 'justification': 'Center', 'font': font(BODY_F, 22, 600), 'colorAndOpacity': color(WHITE, 0.85), 'renderOpacity': 0.0})
cslot(s, 0.5, 0.86, 0, 0, 0, 0, alx=0.5, aly=0.5); setp(s, {'bAutoSize': True})
for n in ('BgSmoke', 'Splash1', 'Splash2', 'TitleLogo', 'PressText'):
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
setp(W.path.replace('.WBP_MainMenu', '.Default__WBP_MainMenu_C') if False else W.tree, {}) if False else None
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
