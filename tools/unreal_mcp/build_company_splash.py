"""Company splash for WBP_MainMenu: Terratales Media Entertainment logo (Image CoLogo; texture T_Terratales_Logo
when imported) + gold wordmark + PRESENTS, and the copyright footer on the title screen."""
from menu_common import *
TITLE_F = '/Game/HollowKin/UI/Fonts/Cinzel-Variable_Font.Cinzel-Variable_Font'
BODY_F = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
GOLD = 'd6a941'
LOGO = '/Game/HollowKin/UI/Art/T_Terratales_Logo.T_Terratales_Logo'
W = Wbp('/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu')
brush, txt, box, cslot, bslot, rule, button = mk(W)
for n in ('SplashCo', 'Copyright'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
def font(f, size, ls): return {'fontObject': f, 'typefaceFontName': 'Default', 'size': size, 'letterSpacing': ls}
def color(h, a=1.0): return {'specifiedColor': col(h, a), 'colorUseRule': 'UseColor_Specified'}
W.count['Root'] = 300
vb, s = W.add('VerticalBox', 'SplashCo', 'Root')
cslot(s, 0.5, 0.5, 0, 0, 0, 0, alx=0.5, aly=0.5); setp(s, {'bAutoSize': True})
setp(vb, {'renderOpacity': 0.0, 'renderTransformPivot': {'x': 0.5, 'y': 0.5}})
sz, ss = W.add('SizeBox', 'CoLogoSize', 'SplashCo')
setp(sz, {'widthOverride': 460, 'heightOverride': 460, 'bOverride_WidthOverride': True, 'bOverride_HeightOverride': True})
bslot(ss, h='HAlign_Center')
img, _ = W.add('Image', 'CoLogo', 'CoLogoSize')
import json as _j
has_logo = call('editor_toolset.toolsets.asset.AssetTools', 'exists', {'path': LOGO.split('.')[0]}).get('returnValue')
setp(img, {'brush': {'drawAs': 'Image', 'imageType': 'FullColor', 'resourceObject': LOGO if has_logo else None,
           'imageSize': {'x': 460, 'y': 460},
           'tintColor': {'specifiedColor': {'r': 1, 'g': 1, 'b': 1, 'a': 1 if has_logo else 0}, 'colorUseRule': 'UseColor_Specified'}}})
for i, (text, f, size, ls, c, a, pad) in enumerate([
        ('TERRATALES MEDIA ENTERTAINMENT', TITLE_F, 34, 300, GOLD, 1.0, (0, 26, 0, 6)),
        ('PRESENTS', BODY_F, 18, 900, GOLD, 0.7, (0, 4, 0, 0))]):
    t, ts = W.add('TextBlock', 'SplashCoT%d' % i, 'SplashCo')
    setp(t, {'text': text, 'justification': 'Center', 'font': font(f, size, ls), 'colorAndOpacity': color(c, a)})
    bslot(ts, pad=pad, h='HAlign_Center')
t, s = W.add('TextBlock', 'Copyright', 'Root')
setp(t, {'text': u'© 2026 Terratales Media Entertainment Private Limited. All rights reserved.   Unreal® Engine © Epic Games, Inc.',
         'justification': 'Center', 'font': font(BODY_F, 14, 60), 'colorAndOpacity': color(DIM, 1.0), 'renderOpacity': 0.0})
cslot(s, 0.5, 1.0, 0, -28, 0, 0, alx=0.5, aly=1.0); setp(s, {'bAutoSize': True})
for n in ('SplashCo', 'CoLogo', 'Copyright'):
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
print('logo texture present:', has_logo, call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
