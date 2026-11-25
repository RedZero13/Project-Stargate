"""Makes menu widgets resolution-independent: Root > ScaleBox(ScaleToFit, fills screen) > SizeBox(1920x1080) > CanvasPanel
holding the original layout. Fixes menus overflowing small windows / ultrawide screens. Skips widgets already wrapped."""
import sys
from ui_lib import *
WBPS = sys.argv[1:] or ['/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu']
for path in WBPS:
    ref = {'refPath': path}
    ws = call(U, 'GetWidgets', {'widgetBlueprint': ref})['returnValue']['widgets']
    root = [w for w in ws if w['parent'] == 'None'][0]
    rp = root['widget']['refPath']
    kids = [w for w in ws if isinstance(w['parent'], dict) and w['parent']['refPath'] == rp]
    if any(w['widgetClassPath']['refPath'].endswith('ScaleBox') for w in kids):
        print(path, 'already wrapped'); continue
    r1 = call(U, 'WrapWidgets', {'widgetBlueprint': ref, 'widgets': [k['widget'] for k in kids], 'wrapperClass': {'refPath': '/Script/UMG.CanvasPanel'}})
    canvas = r1['returnValue'][0]
    r2 = call(U, 'WrapWidgets', {'widgetBlueprint': ref, 'widgets': [canvas['widget']], 'wrapperClass': {'refPath': '/Script/UMG.SizeBox'}})
    sbox = r2['returnValue'][0]
    setp(sbox['widget']['refPath'], {'bOverride_WidthOverride': True, 'WidthOverride': 1920, 'bOverride_HeightOverride': True, 'HeightOverride': 1080})
    r3 = call(U, 'WrapWidgets', {'widgetBlueprint': ref, 'widgets': [sbox['widget']], 'wrapperClass': {'refPath': '/Script/UMG.ScaleBox'}})
    scl = r3['returnValue'][0]
    setp(scl['widget']['refPath'], {'Stretch': 'ScaleToFit'})
    setp(scl['slot']['refPath'], {'layoutData': {'offsets': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}, 'anchors': {'minimum': {'x': 0, 'y': 0}, 'maximum': {'x': 1, 'y': 1}}, 'alignment': {'x': 0, 'y': 0}}})
    # keep a full-screen backdrop (if any) outside the scaled area so wide screens have no bare sides
    tree = path + ':WidgetTree'
    for k in kids:
        if k['widgetName'] in ('Backdrop', 'BG', 'Background'):
            m = call(U, 'MoveWidget', {'widgetBlueprint': ref, 'widget': k['widget'], 'newParent': {'refPath': tree + '.' + root['widgetName']}, 'childIndex': 0})
            setp(m['returnValue']['slot']['refPath'], {'layoutData': {'offsets': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}, 'anchors': {'minimum': {'x': 0, 'y': 0}, 'maximum': {'x': 1, 'y': 1}}}})
    print(path.split('.')[-1], 'wrapped', len(kids), 'children (compile separately)')
