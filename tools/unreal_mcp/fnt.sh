#!/bin/bash
# usage: fnt.sh <graph refPath> <type_id substring>   -> lists matching node type ids
D="$(cd "$(dirname "$0")" && pwd)"
"$D/ct.sh" editor_toolset.toolsets.blueprint.BlueprintTools find_node_types "{\"graph\":{\"refPath\":\"$1\"},\"type_id_filter\":\"$2\",\"context_pins\":[]}" | python3 -c "
import sys,json;t=sys.stdin.read()
try:
  d=json.loads(t)['returnValue']
  for x in d[:40]: print(x if isinstance(x,str) else x.get('type_id',x))
except Exception: print(t[:1500])"
