"""WBP_Achievements (main menu -> ACHIEVEMENTS): a summary (unlocked count, best collectible counts, endings seen,
kills) and a 3-column grid of trophy cards (badge, title, description, UNLOCKED / LOCKED). Locked cards are dimmed.
Badges: tools/make_trophies.py -> import_trophies.py (/Game/HollowKin/UI/Trophies/T_Trophy_<id>).
Built from WBP_Credits (same look, BACK / Esc close). Adds the ACHIEVEMENTS button to WBP_MainMenu above CREDITS.
Note: newlines in DSL string literals must be real newline characters ("\n" in a normal Python string), never "\\n"."""
from menu_common import *
import menu_logic as ml
from achievements_data import ACH, TOTAL_DRAWINGS, TOTAL_FILES
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
P = '/Game/HollowKin/UI/Menus/WBP_Achievements'
W_ = P + '.WBP_Achievements'
NL = '\n'
if not call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Credits', 'new_path': P})
W = Wbp(W_)
brush, txt, box, cslot, bslot, rule, button = mk(W)
setp(W.widget('Cap'), {'text': 'ACHIEVEMENTS /'})
def vis(name):
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(name)}, 'bIsVariable': True})
vis('Body')
# ---- layout: summary (Body) on top of the scroll area, then the card grid ----
have = {x['widget']['refPath'].split('.')[-1] for x in call(U, 'GetWidgets', {'widgetBlueprint': W.ref})['returnValue']['widgets']}
for n in ('Grid',):
    if n in have: call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
BODYFONT = json.loads(call(O, 'get_properties', {'instance': {'refPath': W.widget('Cap')}, 'properties': ['Font']})['returnValue'])['Font']
def font(size, spacing=0):
    f = json.loads(json.dumps(BODYFONT)); f['size'] = size; f['letterSpacing'] = spacing; return f
setp(W.widget('Body'), {'text': '', 'font': font(22, 20), 'AutoWrapText': True})
W.count['Scroll'] = 1
g, gs = W.add('WrapBox', 'Grid', 'Scroll')
setp(g, {'bExplicitWrapSize': True, 'WrapSize': 1545})
setp(gs, {'padding': {'left': 0, 'top': 18, 'right': 0, 'bottom': 30}})
CARD_W, CARD_H, ICON = 495, 118, 92
for n, (i, t, d) in enumerate(ACH):
    c, cs = W.add('SizeBox', 'Card_%d' % n, 'Grid')
    setp(c, {'widthOverride': CARD_W, 'bOverride_WidthOverride': True, 'heightOverride': CARD_H, 'bOverride_HeightOverride': True})
    setp(cs, {'padding': {'left': 0, 'top': 0, 'right': 18, 'bottom': 16}})
    box('CardBg_%d' % n, 'Card_%d' % n, '121a1b', 0.92, padding={'left': 12, 'top': 12, 'right': 16, 'bottom': 12})
    W.add('HorizontalBox', 'CardRow_%d' % n, 'CardBg_%d' % n)
    sz, szs = W.add('SizeBox', 'IcoSz_%d' % n, 'CardRow_%d' % n)
    setp(sz, {'widthOverride': ICON, 'bOverride_WidthOverride': True, 'heightOverride': ICON, 'bOverride_HeightOverride': True})
    bslot(szs, v='VAlign_Center')
    tex = '/Game/HollowKin/UI/Trophies/T_Trophy_%s.T_Trophy_%s' % (i, i)
    im, _ = W.add('Image', 'Ico_%d' % n, 'IcoSz_%d' % n)
    setp(im, {'Brush': {'resourceObject': {'refPath': tex}, 'imageSize': {'x': ICON, 'y': ICON}, 'drawAs': 'Image',
                        'tintColor': {'specifiedColor': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 'colorUseRule': 'UseColor_Specified'}}})
    vb, vbs = W.add('VerticalBox', 'CardTxt_%d' % n, 'CardRow_%d' % n)
    bslot(vbs, pad=(16, 0, 0, 0), fill=1.0, v='VAlign_Center')
    for nm, text, size, sp, color, a, wrap in (('Title_%d' % n, t.upper(), 19, 120, WHITE, 1.0, False),
                                               ('Desc_%d' % n, d, 16, 0, WHITE, 0.72, True),
                                               ('State_%d' % n, 'LOCKED', 13, 300, TEAL, 1.0, False)):
        tw, ts = W.add('TextBlock', nm, 'CardTxt_%d' % n)
        setp(tw, {'text': text, 'font': font(size, sp), 'AutoWrapText': wrap,
                  'colorAndOpacity': {'specifiedColor': col(color, a), 'colorUseRule': 'UseColor_Specified'}})
        bslot(ts, pad=(0, 0, 0, 3))
    vis('Card_%d' % n); vis('State_%d' % n)
print('compile layout', call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
# ---- logic ----
def cat(parts):
    e = parts[0]
    for p in parts[1:]: e = '(Utilities|String|Append %s %s)' % (e, p)
    return e
UNL = '(Class|BPProgressSave|GetAchList :self p)'
END = '(Class|BPProgressSave|GetEndings :self p)'
I = 'Utilities|String|ToString(Integer)'
count = '0'
for i, t, d in ACH:
    count = '(+ %s (select (Utilities|String|Contains %s "|%s|") 1 0))' % (count, UNL, i)
ends = [('LANTERN', 'Lantern'), ('KIN', 'Kin'), ('HOMECOMING', 'Homecoming'), ('HOLLOW', 'Hollow'), ('SIXDOORS', 'Six Doors'), ('LULLABY', 'Lullaby')]
ends_txt = [('(select (Utilities|String|Contains %s "|%s|") "%s   " "")' % (END, k, v)) for k, v in ends]
ends_txt.append('(select (Utilities|String|Contains %s "|end_true|") "Lantern Lit" "")' % UNL)
header = cat(['"UNLOCKED   "', '(%s %s)' % (I, count), '" / %d%s"' % (len(ACH), NL),
              '"BEST RUN   Emilia\'s drawings  "', '(%s (Class|BPProgressSave|GetBestDrawings :self p))' % I, '" / %d      Patient files  "' % TOTAL_DRAWINGS,
              '(%s (Class|BPProgressSave|GetBestFiles :self p))' % I, '" / %d      Hollows put down  "' % TOTAL_FILES,
              '(%s (Class|BPProgressSave|GetKills :self p))' % I,
              '"%sENDINGS SEEN   "' % NL] + ends_txt +
             ['"%sREWARDS   every 5 drawings hides a health gel, every 5 patient files a box of rounds."' % NL])
cards = []
for n, (i, t, d) in enumerate(ACH):
    has = '(Utilities|String|Contains %s "|%s|")' % (UNL, i)
    cards.append('(Widget|SetRenderOpacity (Variables|WBP_Achievements|GetCard_%d) (select %s 1.0 0.38))' % (n, has))
    cards.append('(Widget|SetText(Text) (Variables|WBP_Achievements|GetState_%d) (Utilities|Text|ToText(String) (select %s "UNLOCKED" "LOCKED")))' % (n, has))
dsl = '''(event UserInterface|EventConstruct
  (Variables|Interaction|SetIsFocusable :bIsFocusable true)
  (Widget|SetKeyboardFocus self)
  (bind gi (Utilities|Casting|CastToBP_HKGameInstance (Widget|GetGameInstance))
    (:then
      (Class|BPHKGameInstance|LoadProgress :self gi)
      (bind p (Class|BPHKGameInstance|GetProgress :self gi))
      (Widget|SetText(Text) (Variables|WBP_Achievements|GetBody) (Utilities|Text|ToText(String) %s))
      %s)
    (:CastFailed)))''' % (header, '\n      '.join(cards))
print('construct', call(BT, 'write_graph_dsl', {'graph': {'refPath': W_ + ':EventGraph'}, 'code': dsl}))
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
print(call(A, 'save_assets', {'asset_paths': [P]}))
# --- main menu button (above CREDITS): only added once ---
MM = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'
W2 = Wbp(MM)
have2 = [x['widget']['refPath'].split('.')[-1] for x in call(U, 'GetWidgets', {'widgetBlueprint': W2.ref})['returnValue']['widgets']]
if 'BtnAchievements' not in have2:
    b2 = mk(W2)
    W2.count['Left'] = 8
    b2[6]('BtnAchievements', 'Left', 'ACHIEVEMENTS')
    f = json.loads(call(O, 'get_properties', {'instance': {'refPath': W2.widget('BtnQuitLabel')}, 'properties': ['Font']})['returnValue'])['Font']
    setp(W2.widget('BtnAchievementsLabel'), {'font': f})
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W2.ref, 'widget': {'refPath': W2.widget('BtnAchievements')}, 'bIsVariable': True})
    import subprocess, sys; subprocess.run([sys.executable, 'menu_fit.py'])   # align the new button with the others
    PAD = {'left': 20, 'top': 10, 'right': 80, 'bottom': 10}
    for x in call(U, 'GetWidgets', {'widgetBlueprint': W2.ref})['returnValue']['widgets']:
        if x['widget']['refPath'].endswith('.BtnAchievements'):
            st = json.loads(call(O, 'get_properties', {'instance': x['widget'], 'properties': ['WidgetStyle']})['returnValue'])['WidgetStyle']
            st['normalPadding'] = PAD; st['pressedPadding'] = PAD
            call(O, 'set_properties', {'instance': x['widget'], 'values': json.dumps({'WidgetStyle': st})})
            call(O, 'set_properties', {'instance': x['slot'], 'values': json.dumps({'Padding': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}, 'HorizontalAlignment': 'HAlign_Fill'})})
    call(BT, 'add_function_graph', {'blueprint': {'refPath': MM}, 'graph_name': 'OpenAchievements'})
    print('OpenAchievements', call(BT, 'write_graph_dsl', {'graph': {'refPath': MM + ':OpenAchievements'}, 'code': '''(fn OpenAchievements ()
  (UserInterface|Viewport|AddToViewport (UserInterface|CreateWidget "%s" (Game|GetPlayerController 0)) 70))''' % (W_ + '_C')}))
    ml.wire(MM, 'BtnAchievements', 'OpenAchievements', 0)
    ml.connect_clicks(MM, {'BtnAchievements': 'OpenAchievements'})
    print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W2.ref}))
    print(call(A, 'save_assets', {'asset_paths': ['/Game/HollowKin/UI/Menus/WBP_MainMenu']}))
