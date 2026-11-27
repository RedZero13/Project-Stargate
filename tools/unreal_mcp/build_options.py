"""Rebuilds WBP_Settings as a full-screen Options page in the 007 First Light layout (docs/UI_REFERENCES.md):
'OPTIONS /' caption, category list (left), WidgetSwitcher of pages with name/value rows (centre), description
column with default value (right), version + copyright and button hints at the bottom. Keeps the Btn* names so
the existing settings logic keeps working."""
from menu_common import *
from options_spec import PAGES, KEYS
BODY_F = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
TITLE_F = '/Game/HollowKin/UI/Fonts/Cinzel-Variable_Font.Cinzel-Variable_Font'
W = Wbp('/Game/HollowKin/UI/Menus/WBP_Settings.WBP_Settings')
brush, txt, box, cslot, bslot, rule, button = mk(W)
def font(size, ls=40, f=BODY_F): return {'fontObject': f, 'typefaceFontName': 'Default', 'size': size, 'letterSpacing': ls}
def color(h, a=1.0): return {'specifiedColor': col(h, a), 'colorUseRule': 'UseColor_Specified'}
def T(name, parent, text, size, c=WHITE, a=1.0, ls=40, f=BODY_F, just='Left', **extra):
    t, s = W.add('TextBlock', name, parent)
    v = {'text': text, 'font': font(size, ls, f), 'colorAndOpacity': color(c, a), 'justification': just}; v.update(extra)
    setp(t, v); return t, s
def img(c, a):
    return {'drawAs': 'Image', 'imageType': 'FullColor', 'tintColor': {'specifiedColor': col(c, a), 'colorUseRule': 'UseColor_Specified'}, 'resourceName': 'None',
            'outlineSettings': {'width': 0, 'cornerRadii': {'x': 0, 'y': 0, 'z': 0, 'w': 0}, 'color': {'specifiedColor': {'r': 0, 'g': 0, 'b': 0, 'a': 0}, 'colorUseRule': 'UseColor_Specified'}, 'roundingType': 'FixedRadius', 'bUseBrushTransparency': False}}
def plain_button(name, parent):
    b, s = W.add('Button', name, parent)
    setp(b, {'widgetStyle': {'normal': img(AMBER, 0.0), 'hovered': img(AMBER, 0.10), 'pressed': img(AMBER, 0.22), 'disabled': img(AMBER, 0.0)}})
    return b, s
for n in ('Dim', 'Panel', 'Blur', 'Shade', 'OptCap', 'Cats', 'Pages', 'VDiv', 'Desc', 'Footer', 'Hints'):
    call(U, 'RemoveWidget', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}})
W.count = {}
# background: blur the game/menu behind + darken
b, s = W.add('BackgroundBlur', 'Blur', 'Root'); setp(b, {'blurStrength': 12.0}); cslot(s, (0, 1), (0, 1), 0, 0, 0, 0)
b, s = box('Shade', 'Root', '05080a', 0.78); cslot(s, (0, 1), (0, 1), 0, 0, 0, 0)
t, s = T('OptCap', 'Root', 'OPTIONS /', 16, DIM, 1.0, 700); cslot(s, 0, 0, 180, 140, 0, 0); setp(s, {'bAutoSize': True})
# categories
vb, s = W.add('VerticalBox', 'Cats', 'Root'); cslot(s, 0, 0, 170, 190, 0, 0); setp(s, {'bAutoSize': True})
for i, (page, rows) in enumerate(PAGES + [('BACK', None)]):
    nm = 'Cat%d' % i if page != 'BACK' else 'BtnBack'
    if page == 'BACK':
        sp, _ = W.add('Spacer', 'CatSpacer', 'Cats'); setp(sp, {'size': {'x': 1, 'y': 40}})
    bt, bs = plain_button(nm, 'Cats'); bslot(bs, pad=(0, 2, 0, 2))
    hb, _ = W.add('HorizontalBox', nm + 'Row', nm)
    t, ts = T(nm + 'Dot', nm + 'Row', u'■', 14, AMBER, 1.0, 0); bslot(ts, pad=(8, 0, 14, 0), v='VAlign_Center')
    t, ts = T(nm + 'Name', nm + 'Row', page, 26, WHITE, 1.0, 60); bslot(ts, pad=(0, 8, 24, 8), v='VAlign_Center')
    for n in (nm, nm + 'Dot', nm + 'Name'):
        call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
# pages
sw, s = W.add('WidgetSwitcher', 'Pages', 'Root'); cslot(s, 0, 0, 600, 150, 700, 790)
def rowsep(name, parent):
    sz, ss = W.add('SizeBox', name, parent); setp(sz, {'heightOverride': 1, 'bOverride_HeightOverride': True})
    box(name + 'L', name, DIM, 0.55)
for i, (page, rows) in enumerate(PAGES):
    pv, _ = W.add('VerticalBox', 'Page%d' % i, 'Pages')
    t, ts = T('Page%dCap' % i, 'Page%d' % i, page if page != 'CONTROLS' else 'CAMERA AND LOOK', 16, TEAL, 1.0, 600); bslot(ts, pad=(16, 0, 0, 14))
    rowsep('Page%dTop' % i, 'Page%d' % i)
    for (bn, label, default, desc) in rows:
        bt, bs = plain_button(bn, 'Page%d' % i); bslot(bs, pad=(0, 0, 0, 0))
        hb, _ = W.add('HorizontalBox', bn + 'Row', bn)
        t, ts = T(bn + 'Name', bn + 'Row', label, 26, WHITE, 1.0, 20); bslot(ts, pad=(16, 16, 12, 16), fill=1.0, v='VAlign_Center')
        t, ts = T(bn + 'Label', bn + 'Row', default, 24, WHITE, 0.9, 40, just='Right'); bslot(ts, pad=(12, 16, 16, 16), v='VAlign_Center')
        rowsep(bn + 'Sep', 'Page%d' % i)
        for n in (bn, bn + 'Label'):
            call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
    if page == 'CONTROLS':
        t, ts = T('KeysCap', 'Page%d' % i, 'KEYBOARD AND MOUSE', 16, TEAL, 1.0, 600); bslot(ts, pad=(16, 30, 0, 10))
        for k, (a, keys) in enumerate(KEYS):
            hb, hs = W.add('HorizontalBox', 'Key%d' % k, 'Page%d' % i)
            t, ts = T('Key%dA' % k, 'Key%d' % k, a, 20, WHITE, 0.75, 20); bslot(ts, pad=(16, 5, 12, 5), fill=1.0)
            t, ts = T('Key%dK' % k, 'Key%d' % k, keys, 20, AMBER, 0.95, 60, just='Right'); bslot(ts, pad=(12, 5, 16, 5))
# divider + description column
b, s = box('VDiv', 'Root', AMBER, 0.55); cslot(s, 0, 0, 1335, 150, 2, 790)
vb, s = W.add('VerticalBox', 'Desc', 'Root'); cslot(s, 0, 0, 1380, 150, 420, 700)
t, ts = T('DescTag', 'Desc', 'HK_OPT  //  L-04  //  PROJECT LANTERN', 13, DIM, 1.0, 300); bslot(ts, pad=(0, 0, 0, 18))
t, ts = T('DescTitle', 'Desc', 'OPTIONS', 40, WHITE, 1.0, 40, TITLE_F, autoWrapText=False, wrapTextAt=420); bslot(ts, pad=(0, 0, 0, 14))
t, ts = T('DescBody', 'Desc', 'Choose a category on the left. Changes are saved automatically.', 22, WHITE, 0.85, 10, wrapTextAt=420); bslot(ts, pad=(0, 0, 0, 22))
rowsep('DescSep', 'Desc')
t, ts = T('DescDefault', 'Desc', '', 20, DIM, 1.0, 20); bslot(ts, pad=(0, 14, 0, 0))
for n in ('DescTitle', 'DescBody', 'DescDefault', 'Pages'):
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
# footer + hints
t, s = T('Footer', 'Root', u'Game version: 0.1 (pre-alpha)\n© 2026 Terratales Media Entertainment Private Limited', 16, WHITE, 0.6, 20)
cslot(s, 0, 1, 600, -110, 0, 0, aly=0.0); setp(s, {'bAutoSize': True})
t, s = T('Hints', 'Root', 'ESC   Back          CLICK   Change', 18, WHITE, 0.75, 120, just='Right')
cslot(s, 1, 1, -170, -100, 0, 0, alx=1.0); setp(s, {'bAutoSize': True})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))
