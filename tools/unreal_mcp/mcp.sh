#!/bin/bash
# usage: mcp.sh <top-level tool> '<json args>'   (e.g. list_toolsets '{}', describe_toolset '{"toolset_name":"..."}')
D="$(cd "$(dirname "$0")" && pwd)"
if [ ! -s "$D/sid" ]; then
 curl -s -m 10 -D - -o /dev/null -X POST http://127.0.0.1:8000/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"claude","version":"0"}}}' | grep -i mcp-session-id | awk '{print $2}' | tr -d '\r' > "$D/sid"
fi
S=$(cat "$D/sid")
curl -s -m 120 -X POST http://127.0.0.1:8000/mcp -H "Mcp-Session-Id: $S" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"$1\",\"arguments\":$2}}"
