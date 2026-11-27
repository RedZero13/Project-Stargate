"""WBP_Loading: RE4-style chapter card shown before a level loads. Left: chapter label, title, 2-3 line recap,
a tip and a thin progress bar that fills over the card's duration; right: dim drifting smoke. Setup(Chapter,
Title, Body, Tip, Seconds); the caller opens the level when it finishes (BP_LevelDoor / menus)."""
from menu_common import *
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
BODY_F = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
TITLE_F = '/Game/HollowKin/UI/Fonts/Cinzel-Variable_Font.Cinzel-Variable_Font'
P = '/Game/HollowKin/UI/Menus/WBP_Loading'
if not call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Diegetic/WBP_DeathScreen', 'new_path': P})
W = Wbp(P + '.WBP_Loading')
for g in ('SetBreakdown', 'SetHomecoming', 'SetKin', 'SetLantern'):
    call(BT, 'remove_function_graph', {'blueprint': W.ref, 'graph_name': g})
for x in call(U, 'GetWidgets', {'widgetBlueprint': W.ref})['returnValue']['widgets']:
    n = x['widget']['refPath'].split('.')[-1]
    if n != 'Root' and x.get('parent') and str(x['parent']).endswith(".Root'}") or False: pass
root_children = [x['widget']['refPath'].split('.')[-1] for x in call(U, 'GetWidgets', {'widgetBlueprint': W.ref})['returnValue']['widgets']]
for n in ('Fade', 'Box', 'Bg', 'Smoke', 'LeftShade', 'Info', 'Bar'):
    if n in root_children: call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
brush, txt, box, cslot, bslot, rule, button = mk(W)
W.count = {}
def font(size, ls=20, f=BODY_F): return {'fontObject': f, 'typefaceFontName': 'Default', 'size': size, 'letterSpacing': ls}
def color(h, a=1.0): return {'specifiedColor': col(h, a), 'colorUseRule': 'UseColor_Specified'}
b, s = box('Bg', 'Root', '000000', 1.0); cslot(s, (0, 1), (0, 1), 0, 0, 0, 0)
img, s = W.add('Image', 'Smoke', 'Root')
setp(img, {'brush': {'drawAs': 'Image', 'imageType': 'FullColor', 'resourceObject': '/Game/HollowKin/UI/Art/M_UI_MenuSmoke.M_UI_MenuSmoke',
           'tintColor': {'specifiedColor': {'r': 1.6, 'g': 1.2, 'b': 1.0, 'a': 1}, 'colorUseRule': 'UseColor_Specified'}}})
cslot(s, (0.38, 1), (0, 1), 0, 0, 0, 0)
b, s = box('LeftShade', 'Root', '000000', 0.85); cslot(s, (0, 0.52), (0, 1), 0, 0, 0, 0)
vb, s = W.add('VerticalBox', 'Info', 'Root'); cslot(s, 0, 0, 210, 300, 760, 520)
for name, text, size, f, c, a, ls, pad in [
        ('Chap', 'CHAPTER 1', 22, BODY_F, TEAL, 1.0, 500, (0, 0, 0, 10)),
        ('Title', 'ST. BRIGID\'S CLINIC', 52, TITLE_F, WHITE, 1.0, 80, (0, 0, 0, 22)),
        ('Body', 'Story recap', 26, BODY_F, WHITE, 0.88, 10, (0, 0, 0, 30)),
        ('Tip', 'TIP:', 20, BODY_F, AMBER, 0.95, 40, (0, 0, 0, 0))]:
    t, ts = W.add('TextBlock', name, 'Info')
    setp(t, {'text': text, 'font': font(size, ls, f), 'colorAndOpacity': color(c, a), 'wrapTextAt': 720})
    bslot(ts, pad=pad)
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(name)}, 'bIsVariable': True})
sz, s = W.add('SizeBox', 'Bar', 'Root'); cslot(s, 0, 0, 212, 880, 0, 0); setp(s, {'bAutoSize': True})
setp(sz, {'widthOverride': 0, 'heightOverride': 3, 'bOverride_WidthOverride': True, 'bOverride_HeightOverride': True})
box('BarFill', 'Bar', WHITE, 0.85)
b2, s2 = box('BarTrack', 'Root', WHITE, 0.15); cslot(s2, 0, 0, 212, 880, 420, 3)
call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget('Bar')}, 'bIsVariable': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
B = W.ref
for n, t in [('T', 'float'), ('Dur', 'float')]:
    call(BT, 'add_variable', {'blueprint': B, 'name': n, 'type_name': t})
call(BT, 'add_function_graph', {'blueprint': B, 'graph_name': 'SetupCard'})
for p, t in [('Chapter', 'string'), ('TitleText', 'string'), ('BodyText', 'string'), ('TipText', 'string'), ('Seconds', 'float')]:
    call(BT, 'add_function_param', {'graph': {'refPath': P + '.WBP_Loading:SetupCard'}, 'param_name': p, 'param_type': t, 'input_param': True})
G = lambda n: '(Variables|WBP_Loading|Get%s)' % n
ST = lambda w, e: '(Widget|SetText(Text) %s (Utilities|Text|ToText(String) %s))' % (G(w), e)
print('SetupCard', call(BT, 'write_graph_dsl', {'graph': {'refPath': P + '.WBP_Loading:SetupCard'}, 'code': '''(fn SetupCard (Chapter TitleText BodyText TipText Seconds)
  %s
  %s
  %s
  %s
  (Variables|Default|SetDur Seconds)
  (Variables|Default|SetT 0.0))''' % (ST('Chap', 'Chapter'), ST('Title', 'TitleText'), ST('Body', 'BodyText'), ST('Tip', 'TipText'))}))
print('Tick', call(BT, 'write_graph_dsl', {'graph': {'refPath': P + '.WBP_Loading:EventGraph'}, 'code': '''(event UserInterface|EventTick (MyGeometry InDeltaTime)
  (Variables|Default|SetT (+ (Variables|Default|GetT) InDeltaTime))
  (Class|SizeBox|SetWidthOverride :self %s :WidthOverride (* 420.0 (Math|Float|Clamp(Float) (/ (Variables|Default|GetT) (Math|Float|Max(Float) (Variables|Default|GetDur) 0.1)) 0.0 1.0))))''' % G('Bar')}))
print(call(BT, 'compile_blueprint', {'blueprint': B, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': [P]}))
