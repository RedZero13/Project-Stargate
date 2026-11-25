"""WBP_Credits: CREDITS & LICENCES screen (main menu -> CREDITS). Company copyright + CIN, Epic's Unreal notice,
font licences (SIL OFL 1.1), Fab packs (Fab Standard License). Esc / P / BACK closes it.
Also adds the CREDITS button to WBP_MainMenu."""
from menu_common import *
import menu_logic as ml
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
BODY_F = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
TITLE_F = '/Game/HollowKin/UI/Fonts/Cinzel-Variable_Font.Cinzel-Variable_Font'
P = '/Game/HollowKin/UI/Menus/WBP_Credits'
TEXT = u"""HOLLOW KIN   —   pre-alpha build 0.1
A survival horror game by Terratales Media Entertainment.

© 2026 Terratales Media Entertainment Private Limited. All rights reserved.
CIN  U59112DL2012PTC229544   ·   New Delhi, India
(formerly Chhanda Management Consultants Private Limited)

This is a pre-release prototype for testing. It is not for sale or distribution. All characters, places and events are fictional.


ENGINE
Unreal® Engine, Copyright 1998–2026, Epic Games, Inc. All rights reserved.
Unreal® is a trademark or registered trademark of Epic Games, Inc. in the United States of America and elsewhere.
Game Animation Sample © Epic Games, Inc.


FONTS
Cinzel  —  Copyright The Cinzel Project Authors. Licensed under the SIL Open Font License, Version 1.1.
Barlow  —  Copyright The Barlow Project Authors. Licensed under the SIL Open Font License, Version 1.1.


THIRD-PARTY CONTENT
Used under the Fab Standard License. All rights belong to their respective creators.
Survival Character  ·  Whisper  ·  Tactical Soldier Outfit for MetaHuman  ·  Horror Hospital  ·  Assetsville Town  ·  Mega Street Props Pack  ·  Abandoned Power Plant
M1911  ·  Modern Pistols SFX  ·  NEON WEX Free Muzzle Flash  ·  Realistic Starter VFX Pack Vol 2  ·  Dead Bodies Sitting & Lying Poses  ·  Warning Signs Decals Vol 1
Kid Chalk Drawing  ·  Table Lamp  ·  Military Radio  ·  Horror Music Free Starter Kit  ·  Save Room Music Pack  ·  Horror Ambient Sound Effects Pack 01
Interface & Item Sounds Pack  ·  Essential Footsteps SFX  ·  Thunder Sounds  ·  Free City Ambiences


Thank you for playing."""
if call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'delete', {'path': P})
call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Loading', 'new_path': P})
W = Wbp(P + '.WBP_Credits')
call(BT, 'remove_function_graph', {'blueprint': W.ref, 'graph_name': 'SetupCard'})
for n in ('Bg', 'Smoke', 'LeftShade', 'Info', 'Bar', 'BarTrack'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
brush, txt, box, cslot, bslot, rule, button = mk(W)
W.count = {}
def font(size, ls=20, f=BODY_F): return {'fontObject': f, 'typefaceFontName': 'Default', 'size': size, 'letterSpacing': ls}
def color(h, a=1.0): return {'specifiedColor': col(h, a), 'colorUseRule': 'UseColor_Specified'}
b, s = W.add('BackgroundBlur', 'Blur', 'Root'); setp(b, {'blurStrength': 12.0}); cslot(s, (0, 1), (0, 1), 0, 0, 0, 0)
b, s = box('Shade', 'Root', '05080a', 0.86); cslot(s, (0, 1), (0, 1), 0, 0, 0, 0)
t, s = W.add('TextBlock', 'Cap', 'Root'); setp(t, {'text': 'CREDITS & LICENCES /', 'font': font(16, 700), 'colorAndOpacity': color(DIM)})
cslot(s, 0, 0, 180, 120, 0, 0); setp(s, {'bAutoSize': True})
sb, s = W.add('ScrollBox', 'Scroll', 'Root'); cslot(s, 0, 0, 180, 170, 1560, 790)
t, ts = W.add('TextBlock', 'Body', 'Scroll')
setp(t, {'text': TEXT, 'font': font(22, 10), 'colorAndOpacity': color(WHITE, 0.88), 'wrapTextAt': 1520, 'lineHeightPercentage': 1.15})
bt = button('BtnBack', 'Root', 'BACK')
for x in call(U, 'GetWidgets', {'widgetBlueprint': W.ref})['returnValue']['widgets']:
    if x['widget']['refPath'].endswith('.BtnBack'):
        cslot(x['slot']['refPath'], 0, 1, 180, -120, 0, 0); setp(x['slot']['refPath'], {'bAutoSize': True})
t, s = W.add('TextBlock', 'Hint', 'Root'); setp(t, {'text': 'ESC   Back', 'font': font(18, 120), 'colorAndOpacity': color(WHITE, 0.7)})
cslot(s, 1, 1, -170, -100, 0, 0, alx=1.0); setp(s, {'bAutoSize': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
B = W.ref
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': P + '.WBP_Credits:EventGraph'}, 'code': '''(event UserInterface|EventTick (MyGeometry InDeltaTime)
  (Variables|Default|SetT 0.0))'''}))
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': P + '.WBP_Credits:EventGraph'}, 'code': '''(event UserInterface|EventConstruct
  (Variables|Interaction|SetIsFocusable :bIsFocusable true)
  (Widget|SetKeyboardFocus self))'''}))
for name, body in [('CloseCredits', '(fn CloseCredits ()\n  (Widget|RemoveFromParent self))'),
                   ('OnKeyDown', '''(fn OnKeyDown (MyGeometry InKeyEvent)
  (bind k (Utilities|String|ToString(Text) (Input|Key|GetKeyDisplayName (Input|KeyEvent|GetKey InKeyEvent))))
  (if (or (Utilities|String|Equal,CaseInsensitive(String) k "Escape") (Utilities|String|Equal,CaseInsensitive(String) k "P"))
    (CallFunction|CloseCredits)
    (return (Widget|EventReply|Handled))
    (else (return (Widget|EventReply|Unhandled)))))''')]:
    call(BT, 'add_function_graph', {'blueprint': B, 'graph_name': name})
    print(name, call(BT, 'write_graph_dsl', {'graph': {'refPath': P + '.WBP_Credits:' + name}, 'code': body}))
ml.wire(P + '.WBP_Credits', 'BtnBack', 'CloseCredits', 0)
ml.connect_clicks(P + '.WBP_Credits', {'BtnBack': 'CloseCredits'})
print(call(A, 'save_assets', {'asset_paths': [P]}))
# --- main menu button ---
MM = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'
W2 = Wbp(MM)
b2 = mk(W2)
call(U, 'RemoveWidget', {'widgetBlueprint': W2.ref, 'widget': {'refPath': W2.widget('BtnCredits')}})
W2.count['Left'] = 8
b2[6]('BtnCredits', 'Left', 'CREDITS')
lab = W2.widget('BtnCreditsLabel')
ref_lab = W2.widget('BtnQuitLabel')
f = json.loads(call(O, 'get_properties', {'instance': {'refPath': ref_lab}, 'properties': ['Font']})['returnValue'])['Font']
setp(lab, {'font': f})
call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W2.ref, 'widget': {'refPath': W2.widget('BtnCredits')}, 'bIsVariable': True})
call(BT, 'add_function_graph', {'blueprint': {'refPath': MM}, 'graph_name': 'OpenCredits'})
print('OpenCredits', call(BT, 'write_graph_dsl', {'graph': {'refPath': MM + ':OpenCredits'}, 'code': '''(fn OpenCredits ()
  (UserInterface|Viewport|AddToViewport (UserInterface|CreateWidget "%s" (Game|GetPlayerController 0)) 70))''' % (P + '.WBP_Credits_C')}))
ml.wire(MM, 'BtnCredits', 'OpenCredits', 0)
ml.connect_clicks(MM, {'BtnCredits': 'OpenCredits'})
print(call(A, 'save_assets', {'asset_paths': ['/Game/HollowKin/UI/Menus/WBP_MainMenu']}))
