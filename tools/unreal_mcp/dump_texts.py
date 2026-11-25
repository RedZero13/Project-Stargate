"""Lists every TextBlock in the menu widgets: size, letter spacing, wrap, text (for layout fixes)."""
import sys
from ui_lib import *
W = sys.argv[1:] or ['/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu']
for w in W:
    ws = call(U, 'GetWidgets', {'widgetBlueprint': {'refPath': w}})['returnValue']['widgets']
    print('==', w.split('.')[-1])
    for x in ws:
        cls = x['widgetClassPath']['refPath'].split('.')[-1]
        ref = x['widget']['refPath']
        if cls != 'TextBlock':
            print('  [%s] %s' % (cls, ref.split('.')[-1])); continue
        p = json.loads(call(O, 'get_properties', {'instance': {'refPath': ref}, 'properties': ['Font', 'Text', 'AutoWrapText']})['returnValue'])
        f = p['Font']
        print('  T %-22s s=%s ls=%s wrap=%s %r' % (ref.split('.')[-1], f.get('size'), f.get('letterSpacing'), p.get('AutoWrapText'), str(p.get('Text'))[:60]))
