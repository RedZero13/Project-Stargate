"""Menus: decorative widgets must not eat clicks. Images/texts become HitTestInvisible, visible panels/borders
SelfHitTestInvisible (their buttons still work). The faded-out title image (1400x615, centred) was sitting on top of
NEW ADMISSION and the upper menu buttons. Interactive widgets are left alone."""
from ui_lib import call
import json
U = 'UMGToolSet.UMGToolSet'; O = 'editor_toolset.toolsets.object.ObjectTools'
INTERACTIVE = ('Button', 'Slider', 'CheckBox', 'ComboBox', 'EditableText', 'EditableTextBox', 'SpinBox', 'ScrollBox')
LEAF = ('Image', 'TextBlock', 'RichTextBlock', 'ProgressBar', 'Spacer', 'Throbber', 'CircularThrobber')
for name in ('WBP_MainMenu', 'WBP_PauseMenu', 'WBP_Settings', 'WBP_Difficulty', 'WBP_Credits', 'WBP_Backpack', 'WBP_Loading'):
    P = '/Game/HollowKin/UI/Menus/%s.%s' % (name, name)
    ws = call(U, 'GetWidgets', {'widgetBlueprint': {'refPath': P}})['returnValue']['widgets']
    n = 0
    for w in ws:
        cls = w['widgetClassPath']['refPath'].split('.')[-1]
        if cls in INTERACTIVE or w['parent'] == 'None': continue
        vis = json.loads(call(O, 'get_properties', {'instance': w['widget'], 'properties': ['Visibility']})['returnValue'])['Visibility']
        if vis != 'Visible': continue
        new = 'HitTestInvisible' if cls in LEAF else 'SelfHitTestInvisible'
        call(O, 'set_properties', {'instance': w['widget'], 'values': json.dumps({'Visibility': new})}); n += 1
    print(name, 'fixed', n, call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': P}}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
