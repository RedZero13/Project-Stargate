#!/bin/bash
# usage: desc.sh <toolset> <tool>   -> prints that tool's description and input schema
D="$(cd "$(dirname "$0")" && pwd)"
"$D/mcp.sh" describe_toolset "{\"toolset_name\":\"$1\"}" | python3 -c "
import sys,json;d=json.load(sys.stdin);t=json.loads(d['result']['content'][0]['text'])
for x in t['tools']:
  if x['name'].endswith('.$2'): print(x['description']); print(json.dumps(x['inputSchema'])[:900])"
