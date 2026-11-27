"""Options page alignment: row buttons fill the column (name left, value right), category buttons left-aligned,
bullet glyph the font has."""
from ui_lib import *
SET = '/Game/HollowKin/UI/Menus/WBP_Settings.WBP_Settings'
ws = call(U, 'GetWidgets', {'widgetBlueprint': {'refPath': SET}})['returnValue']['widgets']
for x in ws:
    name = x['widget']['refPath'].split('.')[-1]
    slot = x.get('slot', {}).get('refPath') if isinstance(x.get('slot'), dict) else None
    if not slot: continue
    if name.endswith('Row') and (name.startswith('Btn') or name.startswith('Cat')):
        cat = name.startswith('Cat') or name == 'BtnBackRow'
        setp(slot, {'horizontalAlignment': 'HAlign_Left' if cat else 'HAlign_Fill', 'verticalAlignment': 'VAlign_Center',
                    'padding': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}})
    if (name.startswith('Btn') or name.startswith('Cat')) and not name.endswith(('Row', 'Name', 'Label', 'Dot', 'Sep', 'SepL')) and name[3:].isalnum():
        setp(slot, {'horizontalAlignment': 'HAlign_Fill'})
    if name.endswith('Dot'):
        setp(x['widget']['refPath'], {'text': u'•'})
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': SET}}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/HollowKin/UI/Menus/WBP_Settings']}))
