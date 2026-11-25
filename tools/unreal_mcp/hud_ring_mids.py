"""WBP_ScreenFX.InitRingMats: creates the ring material instances (AmmoMID / HpMID) from the two ring images.
Built node-by-node because 'GetDynamicMaterial' is ambiguous in the DSL (needs declaring_class Image)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
SFX = '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX'
B = {'refPath': SFX}
for n in ('AmmoMID', 'HpMID'):
    call(BT, 'add_object_variable', {'blueprint': B, 'name': n, 'object_class': {'refPath': '/Script/Engine.MaterialInstanceDynamic'}})
call(BT, 'remove_function_graph', {'blueprint': B, 'graph_name': 'InitRingMats'})
call(BT, 'add_function_graph', {'blueprint': B, 'graph_name': 'InitRingMats'})
g = {'refPath': SFX + ':InitRingMats'}
call(BT, 'compile_blueprint', {'blueprint': B, 'warnings_as_errors': False})
def node(t, x, y, decl=None):
    a = {'graph': g, 'type_id': t, 'pos': {'x': x, 'y': y}}
    if decl: a['declaring_class'] = {'refPath': decl}
    r = call(BT, 'create_node', a); 
    if not isinstance(r, dict) or 'returnValue' not in r: print('FAIL', t, r); return None
    return r['returnValue']
def info(n): return call(BT, 'get_node_infos', {'nodes': [n]})['returnValue'][0]
def pin(n, name, out):
    i = info(n); ps = i['output_pins'] if out else i['input_pins']
    for p in ps:
        if p['name'] == name or (name == '*exec' and p['type_id'] == 'Exec'): return p['pin_id']
    print('no pin', name, [(p['name'], p['type_id']) for p in ps])
def link(a, an, b, bn):
    print(an, '->', bn, call(BT, 'connect_pins', {'output_pin': pin(a, an, True), 'input_pin': pin(b, bn, False)}))
entry = [n for n in call(BT, 'find_nodes', {'graph': g, 'title': ''})['returnValue'] if 'FunctionEntry' in n['refPath']][0]
prev, prev_pin = entry, 'then'
for i, (img, var) in enumerate([('AmmoRing', 'AmmoMID'), ('HPRing', 'HpMID')]):
    get = node('Variables|WBP_ScreenFX|Get' + img, 200, 200 + i * 300)
    dm = node('Appearance|GetDynamicMaterial', 450, 100 + i * 300, '/Script/UMG.Image')
    st = node('Variables|Default|Set' + var, 800, 100 + i * 300)
    link(prev, prev_pin, dm, 'execute')
    link(get, [p['name'] for p in info(get)['output_pins']][0], dm, 'self')
    link(dm, 'then', st, 'execute')
    link(dm, 'ReturnValue', st, var)
    prev, prev_pin = st, 'then'
print(call(BT, 'compile_blueprint', {'blueprint': B, 'warnings_as_errors': False}))
