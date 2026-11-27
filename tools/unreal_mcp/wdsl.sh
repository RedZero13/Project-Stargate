#!/bin/bash
# usage: wdsl.sh <graph refPath> <dsl file>   -> writes the DSL into that graph (and compiles)
D="$(cd "$(dirname "$0")" && pwd)"
ARGS=$(python3 -c "import json,sys;print(json.dumps({'graph':{'refPath':sys.argv[1]},'code':open(sys.argv[2]).read()}))" "$1" "$2")
"$D/ct.sh" editor_toolset.toolsets.blueprint.BlueprintTools write_graph_dsl "$ARGS"
