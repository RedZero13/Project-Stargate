#!/bin/bash
# usage: nodeinfo.sh <graph refPath> [type substring]  -> one line per node: name, type, input pin values, connected?
D="$(cd "$(dirname "$0")" && pwd)"
NODES=$("$D/ct.sh" editor_toolset.toolsets.blueprint.BlueprintTools find_nodes "{\"graph\":{\"refPath\":\"$1\"},\"title\":\"\"}" | python3 -c "import sys,json;print(json.dumps({'nodes':json.loads(sys.stdin.read())['returnValue']}))")
"$D/ct.sh" editor_toolset.toolsets.blueprint.BlueprintTools get_node_infos "$NODES" | python3 -c "
import sys,json
f=sys.argv[1] if len(sys.argv)>1 else ''
for n in json.loads(sys.stdin.read())['returnValue']:
  if f and f not in n['type_id']: continue
  ins=['%s=%s%s'%(p['name'],p['value'],'*' if p['connected_pins'] else '') for p in n['input_pins']]
  outc=sum(len(p['connected_pins']) for p in n['output_pins'])
  print(n['node']['refPath'].split('.')[-1], n['type_id'], 'outs=%d'%outc, ' '.join(ins)[:300])" "$2"
