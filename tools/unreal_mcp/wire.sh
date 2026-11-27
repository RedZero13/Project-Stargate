#!/bin/bash
# usage: wire.sh <BP asset path> <IA name> <function name> <y>  -> Enhanced-Input "Started" event calls a BP function
D="$(cd "$(dirname "$0")" && pwd)"
M="$1"; BP=editor_toolset.toolsets.blueprint.BlueprintTools
G="{\"refPath\":\"${M}:EventGraph\"}"
ref() { python3 -c "import sys,json;print(json.load(sys.stdin)['returnValue']['refPath'])"; }
IA=$("$D/ct.sh" $BP create_node "{\"graph\":$G,\"type_id\":\"Input|EnhancedActionEvents|$2\",\"pos\":{\"x\":0,\"y\":$4}}" | ref)
CF=$("$D/ct.sh" $BP create_node "{\"graph\":$G,\"type_id\":\"CallFunction|$3\",\"pos\":{\"x\":500,\"y\":$4}}" | ref)
"$D/ct.sh" $BP connect_pins "{\"output_pin\":{\"direction\":\"EGPD_Output\",\"index_id\":1,\"node\":{\"refPath\":\"$IA\"}},\"input_pin\":{\"direction\":\"EGPD_Input\",\"index_id\":0,\"node\":{\"refPath\":\"$CF\"}}}"
