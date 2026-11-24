#!/bin/bash
# usage: prune.sh <graph refPath>  -> deletes nodes not connected (via exec or data) to the function entry
D="$(cd "$(dirname "$0")" && pwd)"
NODES=$("$D/ct.sh" editor_toolset.toolsets.blueprint.BlueprintTools find_nodes "{\"graph\":{\"refPath\":\"$1\"},\"title\":\"\"}" | python3 -c "import sys,json;print(json.dumps({'nodes':json.loads(sys.stdin.read())['returnValue']}))")
"$D/ct.sh" editor_toolset.toolsets.blueprint.BlueprintTools get_node_infos "$NODES" | python3 -c "
import sys,json
ns=json.loads(sys.stdin.read())['returnValue']
by={n['node']['refPath']:n for n in ns}
roots=[r for r in by if 'FunctionEntry' in r or 'K2Node_Event' in r or 'K2Node_CustomEvent' in r or 'ComponentBoundEvent' in r or 'InputAction' in r or 'EnhancedInput' in r]
live=set(roots); st=list(roots)
while st:   # follow exec wires forward
  n=by[st.pop()]
  for p in n['output_pins']:
    if p['type_id']=='Exec':
      for c in p['connected_pins']:
        b=c['node']['refPath']
        if b not in live: live.add(b); st.append(b)
st=list(live)
while st:   # add everything feeding data into live nodes
  n=by.get(st.pop())
  if not n: continue
  for p in n['input_pins']:
    if p['type_id']!='Exec':
      for c in p['connected_pins']:
        b=c['node']['refPath']
        if b not in live: live.add(b); st.append(b)
for r in by:
  if r not in live and 'FunctionResult' not in r: print(r)" > /tmp/prune_list.$$
echo "deleting $(wc -l < /tmp/prune_list.$$) nodes"
while read r; do "$D/ct.sh" editor_toolset.toolsets.blueprint.BlueprintTools delete_node "{\"node\":{\"refPath\":\"$r\"}}" >/dev/null; done < /tmp/prune_list.$$
rm -f /tmp/prune_list.$$
