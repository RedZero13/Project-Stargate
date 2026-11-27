#!/bin/bash
# usage: cap2.sh out.png   -> screenshot of the whole editor (shows Play-In-Editor too)
D="$(cd "$(dirname "$0")" && pwd)"
PAY='{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"call_tool","arguments":{"toolset_name":"EditorToolset.EditorAppToolset","tool_name":"CaptureEditorImage","arguments":{}}}}'
curl -s -m 60 -X POST http://127.0.0.1:8000/mcp -H "Mcp-Session-Id: $(cat "$D/sid")" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d "$PAY" | python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
for c in d['result']['content']:
    t=c.get('text','')
    try:
        j=json.loads(t); rv=j['returnValue']; im=rv.get('image',rv); open('$1','wb').write(base64.b64decode(im['data'])); print('saved')
    except Exception as e: print(t[:200])"
