#!/bin/bash
# usage: ct.sh <toolset> <tool> '<json args>'
D="$(cd "$(dirname "$0")" && pwd)"
[ -s "$D/sid" ] || "$D/mcp.sh" list_toolsets '{}' >/dev/null
ARGS=${3:-{\}}
PAY=$(python3 -c "import json,sys;print(json.dumps({'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'call_tool','arguments':{'toolset_name':sys.argv[1],'tool_name':sys.argv[2],'arguments':json.loads(sys.argv[3])}}}))" "$1" "$2" "$ARGS")
curl -s -m 600 -X POST http://127.0.0.1:8000/mcp -H "Mcp-Session-Id: $(cat "$D/sid")" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d "$PAY" | python3 -c "
import sys,json
d=json.load(sys.stdin)
r=d.get('result',d)
if isinstance(r,dict) and 'content' in r:
    for c in r['content']: print(c.get('text',c))
else: print(json.dumps(r,indent=1))"
