#!/bin/bash
# usage: wire.sh <IA name> <function name> <y>
cd $(cd "$(dirname "$0")" && pwd)
BP=editor_toolset.toolsets.blueprint.BlueprintTools
M='/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
G="{\"refPath\":\"${M}:EventGraph\"}"
ref() { python3 -c "import sys,json;print(json.load(sys.stdin)['returnValue']['refPath'])"; }
IA=$(./ct.sh $BP create_node "{\"graph\":$G,\"type_id\":\"Input|EnhancedActionEvents|$1\",\"pos\":{\"x\":0,\"y\":$3}}" | ref)
CF=$(./ct.sh $BP create_node "{\"graph\":$G,\"type_id\":\"CallFunction|$2\",\"pos\":{\"x\":500,\"y\":$3}}" | ref)
echo $IA $CF
./ct.sh $BP connect_pins "{\"output_pin\":{\"direction\":\"EGPD_Output\",\"index_id\":1,\"node\":{\"refPath\":\"$IA\"}},\"input_pin\":{\"direction\":\"EGPD_Input\",\"index_id\":0,\"node\":{\"refPath\":\"$CF\"}}}"
