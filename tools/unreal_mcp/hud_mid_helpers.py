"""WBP_ScreenFX helpers MidScalar(M, P, V) / MidColor(M, P, C): set a parameter on a MaterialInstanceDynamic.
Built node-by-node (the DSL resolves SetScalarParameterValue to the parameter-collection version)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
SFX = '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX'
B = {'refPath': SFX}
def info(n): return call(BT, 'get_node_infos', {'nodes': [n]})['returnValue'][0]
def pin(n, name, out):
    for p in (info(n)['output_pins'] if out else info(n)['input_pins']):
        if p['name'] == name: return p['pin_id']
    print('no pin', name, [p['name'] for p in (info(n)['output_pins'] if out else info(n)['input_pins'])])
for fname, node_t, vparam, vtype in [('MidScalar', 'Rendering|Material|SetScalarParameterValue', 'V', 'float'),
                                     ('MidColor', 'Rendering|Material|SetVectorParameterValue', 'C', 'LinearColor')]:
    call(BT, 'remove_function_graph', {'blueprint': B, 'graph_name': fname})
    call(BT, 'add_function_graph', {'blueprint': B, 'graph_name': fname})
    g = {'refPath': SFX + ':' + fname}
    call(BT, 'add_object_function_param', {'graph': g, 'param_name': 'M', 'object_class': {'refPath': '/Script/Engine.MaterialInstanceDynamic'}, 'input_param': True})
    call(BT, 'add_function_param', {'graph': g, 'param_name': 'P', 'param_type': 'name', 'input_param': True})
    if vtype == 'float':
        call(BT, 'add_function_param', {'graph': g, 'param_name': vparam, 'param_type': 'float', 'input_param': True})
    else:
        print(call(BT, 'add_struct_function_param', {'graph': g, 'param_name': vparam, 'struct_type': {'refPath': '/Script/CoreUObject.LinearColor'}, 'input_param': True}))
    entry = [n for n in call(BT, 'find_nodes', {'graph': g, 'title': ''})['returnValue'] if 'FunctionEntry' in n['refPath']][0]
    nd = call(BT, 'create_node', {'graph': g, 'type_id': node_t, 'pos': {'x': 400, 'y': 0}, 'declaring_class': {'refPath': '/Script/Engine.MaterialInstanceDynamic'}})['returnValue']
    ins = [p['name'] for p in info(nd)['input_pins']]
    print(fname, ins)
    pairs = [('then', 'execute'), ('M', 'self'), ('P', 'ParameterName'), (vparam, ins[-1])]
    for a, b in pairs:
        print(' ', a, '->', b, call(BT, 'connect_pins', {'output_pin': pin(entry, a, True), 'input_pin': pin(nd, b, False)}))
print(call(BT, 'compile_blueprint', {'blueprint': B, 'warnings_as_errors': False}))
