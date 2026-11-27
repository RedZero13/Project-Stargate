"""Capture the editor viewport from a given camera pose. usage: capview.py out.png x y z yaw [pitch]"""
import json, urllib.request, base64, sys, os
SID = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sid')).read().strip()
out, x, y, z, yaw = sys.argv[1], *map(float, sys.argv[2:6]); pitch = float(sys.argv[6]) if len(sys.argv) > 6 else -8
args = {'captureTransform': {'location': {'x': x, 'y': y, 'z': z}, 'rotation': {'pitch': pitch, 'yaw': yaw, 'roll': 0}, 'scale': {'x': 1, 'y': 1, 'z': 1}},
        'annotations': {'gridSpacing': 0, 'gridExtent': 0, 'showActorLabels': False}}
p = {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'call_tool', 'arguments': {'toolset_name': 'EditorToolset.EditorAppToolset', 'tool_name': 'CaptureViewport', 'arguments': args}}}
r = urllib.request.Request('http://127.0.0.1:8000/mcp', json.dumps(p).encode(), {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'Mcp-Session-Id': SID})
d = json.load(urllib.request.urlopen(r, timeout=120))
txt = ''.join(c.get('text', '') for c in d['result']['content'])
img = json.loads(txt)['returnValue']['image']['data']
open(out, 'wb').write(base64.b64decode(img)); print('saved', out)
