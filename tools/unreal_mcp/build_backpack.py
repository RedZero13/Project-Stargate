"""WBP_Backpack: RE4-style backpack screen (I key / pause menu). ITEMS tab: tiles with a coloured icon block, name and
count (gel and sedative tiles are buttons: click to use). WORKBENCH tab: visual recipe cards
[ingredient tiles with have/need] -> [result tile] [CRAFT]. Hover shows a description. I / Esc / P closes."""
from menu_common import *
import menu_logic as ml
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
BODY_F = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
TITLE_F = '/Game/HollowKin/UI/Fonts/Cinzel-Variable_Font.Cinzel-Variable_Font'
P = '/Game/HollowKin/UI/Menus/WBP_Backpack'
from backpack_spec import ITEMS, RECIPES
if call(A, 'exists', {'path': P}).get('returnValue'):
    call(A, 'delete', {'path': P})
call(A, 'duplicate', {'path': '/Game/HollowKin/UI/Menus/WBP_Loading', 'new_path': P})
W = Wbp(P + '.WBP_Backpack')
call(BT, 'remove_function_graph', {'blueprint': W.ref, 'graph_name': 'SetupCard'})
for n in ('Bg', 'Smoke', 'LeftShade', 'Info', 'Bar', 'BarTrack'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
brush, txt, box, cslot, bslot, rule, button = mk(W)
W.count = {}
def font(size, ls=20, f=BODY_F): return {'fontObject': f, 'typefaceFontName': 'Default', 'size': size, 'letterSpacing': ls}
def color(h, a=1.0): return {'specifiedColor': col(h, a), 'colorUseRule': 'UseColor_Specified'}
def T(name, parent, text, size, c=WHITE, a=1.0, ls=20, f=BODY_F, just='Left', **kw):
    t, s = W.add('TextBlock', name, parent); v = {'text': text, 'font': font(size, ls, f), 'colorAndOpacity': color(c, a), 'justification': just}; v.update(kw); setp(t, v); return t, s
def img(c, a):
    return {'drawAs': 'Image', 'imageType': 'FullColor', 'tintColor': {'specifiedColor': col(c, a), 'colorUseRule': 'UseColor_Specified'}, 'resourceName': 'None',
            'outlineSettings': {'width': 0, 'cornerRadii': {'x': 0, 'y': 0, 'z': 0, 'w': 0}, 'color': {'specifiedColor': {'r': 0, 'g': 0, 'b': 0, 'a': 0}, 'colorUseRule': 'UseColor_Specified'}, 'roundingType': 'FixedRadius', 'bUseBrushTransparency': False}}
def var(*names):
    for n in names: call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
ICONS = {k: '/Game/HollowKin/UI/Icons/T_Item_%s.T_Item_%s' % (k, k) for k in ('Ammo', 'Gel', 'Sed', 'Fuse', 'Parts', 'Chem', 'Bottle', 'Drawing')}
OUTKEY = {'RAmmo': 'Ammo', 'RTonic': 'Sed', 'RGel': 'Gel'}
def tile(prefix, parent, label, icon, icol, clickable, key=None):
    """Tile: [Button or Border] -> Border(frame) -> VBox: icon block, name, count."""
    if clickable:
        b, s = W.add('Button', prefix, parent)
        setp(b, {'widgetStyle': {'normal': img(TEAL, 0.0), 'hovered': img(AMBER, 0.16), 'pressed': img(AMBER, 0.3), 'disabled': img(TEAL, 0.0)}})
        inner_parent = prefix
    else:
        b, s = W.add('Button', prefix, parent)   # buttons for hover descriptions too
        setp(b, {'widgetStyle': {'normal': img(TEAL, 0.0), 'hovered': img(TEAL, 0.10), 'pressed': img(TEAL, 0.10), 'disabled': img(TEAL, 0.0)}})
        inner_parent = prefix
    fr, fs = box(prefix + 'Frame', inner_parent, '0e1517', 0.92, padding={'left': 14, 'top': 12, 'right': 14, 'bottom': 12})
    sz, _ = W.add('SizeBox', prefix + 'Size', prefix + 'Frame')
    setp(sz, {'widthOverride': 190, 'heightOverride': 150, 'bOverride_WidthOverride': True, 'bOverride_HeightOverride': True})
    vb, _ = W.add('VerticalBox', prefix + 'VB', prefix + 'Size')
    isz, iss = W.add('SizeBox', prefix + 'IconSz', prefix + 'VB')
    setp(isz, {'widthOverride': 96, 'heightOverride': 80, 'bOverride_WidthOverride': True, 'bOverride_HeightOverride': True}); bslot(iss, h='HAlign_Left')
    if key in ICONS:   # rendered item model (same mesh as the pickup in the world) on a soft coloured disc
        ib, _ = box(prefix + 'IconBg', prefix + 'IconSz', icol, 0.18, padding={'left': 2, 'top': 2, 'right': 2, 'bottom': 2}, horizontalAlignment='HAlign_Fill', verticalAlignment='VAlign_Fill')
        im, _ = W.add('Image', prefix + 'Icon', prefix + 'IconBg')
        setp(im, {'brush': {'resourceObject': {'refPath': ICONS[key]}, 'imageSize': {'x': 92, 'y': 76}, 'drawAs': 'Image'}})
    else:
        ib, _ = box(prefix + 'Icon', prefix + 'IconSz', icol, 0.85, padding={'left': 4, 'top': 4, 'right': 4, 'bottom': 4}, horizontalAlignment='HAlign_Center', verticalAlignment='VAlign_Center')
        T(prefix + 'IconT', prefix + 'Icon', icon, 20, '0b0f10', 1.0, 40, just='Center')
    t, ts = T(prefix + 'Name', prefix + 'VB', label, 18, WHITE, 0.95, 60); bslot(ts, pad=(0, 10, 0, 2))
    t, ts = T(prefix + 'Count', prefix + 'VB', 'x 0', 26, WHITE, 1.0, 20); bslot(ts, pad=(0, 0, 0, 0))
    var(prefix, prefix + 'Count')
    return b, s
b, s = W.add('BackgroundBlur', 'Blur', 'Root'); setp(b, {'blurStrength': 12.0}); cslot(s, (0, 1), (0, 1), 0, 0, 0, 0)
b, s = box('Shade', 'Root', '05080a', 0.82); cslot(s, (0, 1), (0, 1), 0, 0, 0, 0)
T('Cap', 'Root', 'BACKPACK /', 16, DIM, 1.0, 700); cslot(W.add('Spacer', 'CapSp', 'Root')[1], 0, 0, 0, 0, 1, 1)
for x in call(U, 'GetWidgets', {'widgetBlueprint': W.ref})['returnValue']['widgets']:
    if x['widget']['refPath'].endswith('.Cap'): cslot(x['slot']['refPath'], 0, 0, 180, 120, 0, 0); setp(x['slot']['refPath'], {'bAutoSize': True})
# tabs
hb, s = W.add('HorizontalBox', 'Tabs', 'Root'); cslot(s, 0.5, 0, 0, 110, 0, 0, alx=0.5); setp(s, {'bAutoSize': True})
for i, name in enumerate(('ITEMS', 'WORKBENCH')):
    tb, ts = W.add('Button', 'Tab%d' % i, 'Tabs')
    setp(tb, {'widgetStyle': {'normal': img(AMBER, 0.0), 'hovered': img(AMBER, 0.12), 'pressed': img(AMBER, 0.25), 'disabled': img(AMBER, 0.0)}}); bslot(ts, pad=(18, 0, 18, 0))
    vb, _ = W.add('VerticalBox', 'Tab%dVB' % i, 'Tab%d' % i)
    T('Tab%dName' % i, 'Tab%dVB' % i, name, 28, WHITE, 1.0, 200, just='Center')
    sz, ss = W.add('SizeBox', 'Tab%dLineSz' % i, 'Tab%dVB' % i); setp(sz, {'heightOverride': 3, 'bOverride_HeightOverride': True}); bslot(ss, pad=(0, 6, 0, 0))
    box('Tab%dLine' % i, 'Tab%dLineSz' % i, AMBER, 0.9)
    var('Tab%d' % i, 'Tab%dName' % i, 'Tab%dLine' % i)
sw, s = W.add('WidgetSwitcher', 'CasePages', 'Root'); cslot(s, 0.5, 0, 0, 200, 0, 0, alx=0.5); setp(s, {'bAutoSize': True})
var('CasePages')
# items page: 4 x 2 grid
g, _ = W.add('UniformGridPanel', 'ItemGrid', 'CasePages')
setp(g, {'slotPadding': {'left': 10, 'top': 10, 'right': 10, 'bottom': 10}})
for i, (k, label, icon, icol, mv, desc, use) in enumerate(ITEMS):
    b, s = tile('It' + k, 'ItemGrid', label, icon, icol, bool(use), key=k)
    setp(s, {'row': i // 4, 'column': i % 4})
# workbench page: recipe cards
rv, _ = W.add('VerticalBox', 'Recipes', 'CasePages')
labels = {k: (label, icon, icol) for (k, label, icon, icol, mv, desc, use) in ITEMS}
for (rk, rlabel, ricon, rcol, ings, cfn, rdesc) in RECIPES:
    card, cs = box(rk + 'Card', 'Recipes', '0b1113', 0.9, padding={'left': 24, 'top': 12, 'right': 24, 'bottom': 12}); bslot(cs, pad=(0, 0, 0, 12))
    row, _ = W.add('HorizontalBox', rk + 'Row', rk + 'Card')
    for j, (ik, need) in enumerate(ings):
        if j:
            t, ts = T(rk + 'Plus%d' % j, rk + 'Row', '+', 40, WHITE, 0.6, 0); bslot(ts, pad=(14, 0, 14, 0), v='VAlign_Center')
        lb, ic, cc = labels[ik]
        b, s = tile(rk + ik, rk + 'Row', lb, ic, cc, False, key=ik)
        bslot(s, v='VAlign_Center')
    t, ts = T(rk + 'Arrow', rk + 'Row', u'→', 48, AMBER, 0.9, 0); bslot(ts, pad=(26, 0, 26, 0), v='VAlign_Center')
    b, s = tile(rk + 'Out', rk + 'Row', rlabel, ricon, rcol, False, key=OUTKEY.get(rk)); bslot(s, v='VAlign_Center')
    cb, cbs = W.add('Button', rk + 'Craft', rk + 'Row')
    setp(cb, {'widgetStyle': {'normal': img(AMBER, 0.85), 'hovered': img(AMBER, 1.0), 'pressed': img(AMBER, 0.7), 'disabled': img(DIM, 0.6)}})
    bslot(cbs, pad=(32, 0, 0, 0), v='VAlign_Center')
    T(rk + 'CraftT', rk + 'Craft', 'CRAFT', 24, '0b0f10', 1.0, 300, just='Center')
    var(rk + 'Craft')
# description + hints
vb, s = W.add('VerticalBox', 'DescBox', 'Root'); cslot(s, 0.5, 1, 0, -150, 0, 0, alx=0.5, aly=1.0); setp(s, {'bAutoSize': True})
T('DescName', 'DescBox', '', 30, WHITE, 1.0, 60, TITLE_F, just='Center'); T('DescText', 'DescBox', 'Hover over an item.', 22, WHITE, 0.8, 10, just='Center', wrapTextAt=900)
var('DescName', 'DescText')
T('Hints', 'Root', 'B  Backpack     I  Workbench     ESC  Close     CLICK  Use / Craft', 18, WHITE, 0.7, 120, just='Center')
for x in call(U, 'GetWidgets', {'widgetBlueprint': W.ref})['returnValue']['widgets']:
    if x['widget']['refPath'].endswith('.Hints'): cslot(x['slot']['refPath'], 0.5, 1, 0, -70, 0, 0, alx=0.5); setp(x['slot']['refPath'], {'bAutoSize': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
print(call(A, 'save_assets', {'asset_paths': [P]}))
