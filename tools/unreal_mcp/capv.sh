#!/bin/bash
# usage: capv.sh out.png x y z pitch yaw   -> renders the editor viewport from that camera
D="$(cd "$(dirname "$0")" && pwd)"
PAY=$(python3 -c "import json,sys;x,y,z,p,w=map(float,sys.argv[1:6]);print(json.dumps({'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'call_tool','arguments':{'toolset_name':'EditorToolset.EditorAppToolset','tool_name':'CaptureViewport','arguments':{'captureTransform':{'location':{'x':x,'y':y,'z':z},'rotation':{'pitch':p,'yaw':w,'roll':0}},'annotations':[],'bShowUI':False}}}}))" "$2" "$3" "$4" "$5" "$6")
curl -s -m 60 -X POST http://127.0.0.1:8000/mcp -H "Mcp-Session-Id: $(cat "$D/sid")" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d "$PAY" | python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
for c in d['result']['content']:
  j=json.loads(c.get('text','{}')); im=j['returnValue']; im=im.get('image',im); open(sys.argv[1],'wb').write(base64.b64decode(im['data'])); print('saved')" "$1"
