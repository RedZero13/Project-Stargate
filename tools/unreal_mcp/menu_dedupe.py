"""Main menu: 'Project Lantern' and the subject numbers appeared up to four times. Lantern now appears once (the
strip under the logo); the caption says ST. BRIGID'S // CASE FILE // RESTRICTED; the subtitle line is gone; the
SUBJECT FILES panel keeps the L-03 / L-04 file numbers."""
from ui_lib import *
W = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'; T = W + ':WidgetTree.'
setp(T + 'Cap', {'Text': "ST. BRIGID'S  //  CASE FILE  //  RESTRICTED"})
print(call(U, 'RemoveWidget', {'widgetBlueprint': {'refPath': W}, 'widget': {'refPath': T + 'Sub'}}))
print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': {'refPath': W}}))
print(call('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': {'refPath': W}, 'warnings_as_errors': False}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/HollowKin/UI/Menus/WBP_MainMenu']}))
