"""Adds ApplySavedVolumes to WBP_MainMenu and WBP_ScreenFX and calls it at the end of Event Construct,
so saved volume settings take effect in the menu and in every level."""
from ui_lib import call
import json
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
FN = '''(fn ApplySavedVolumes ()
  (bind s (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then (Class|BPSettingsSave|ApplyVolumes :self s :Ctx self))
    (:CastFailed)))'''
for w in ['/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu', '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX']:
    call(BT, 'add_function_graph', {'blueprint': {'refPath': w}, 'graph_name': 'ApplySavedVolumes'})
    print(w, call(BT, 'write_graph_dsl', {'graph': {'refPath': w + ':ApplySavedVolumes'}, 'code': FN}))
    g = {'refPath': w + ':EventGraph'}
    nodes = call(BT, 'find_nodes', {'graph': g, 'title': ''})['returnValue']
    infos = call(BT, 'get_node_infos', {'nodes': nodes})['returnValue']
    by = {n['node']['refPath']: n for n in infos}
    ev = [n for n in infos if 'EventConstruct' in n['type_id']][0]
    # walk the exec chain to its last node
    cur = ev
    while True:
        outs = [p for p in cur['output_pins'] if p['type_id'] == 'Exec']
        if not outs or not outs[0]['connected_pins']:
            break
        cur = by[outs[0]['connected_pins'][0]['node']['refPath']]
    out = [p for p in cur['output_pins'] if p['type_id'] == 'Exec'][0]['pin_id']
    cf = call(BT, 'create_node', {'graph': g, 'type_id': 'CallFunction|ApplySavedVolumes', 'pos': {'x': 900, 'y': 200}})['returnValue']
    print(' connect after', cur['type_id'], call(BT, 'connect_pins', {'output_pin': out, 'input_pin': {'direction': 'EGPD_Input', 'index_id': 0, 'node': cf}}))
    print(' compile', call(BT, 'compile_blueprint', {'blueprint': {'refPath': w}, 'warnings_as_errors': False}))
