#!/bin/bash
# usage: rdsl.sh <graph refPath>   -> prints the graph as DSL
D="$(cd "$(dirname "$0")" && pwd)"
"$D/ct.sh" editor_toolset.toolsets.blueprint.BlueprintTools read_graph_dsl "{\"graph\":{\"refPath\":\"$1\"}}" | python3 -c "import sys,json;t=sys.stdin.read();
try: print(json.loads(t)['returnValue'])
except Exception: print(t)"
