#!/bin/bash
# usage: fabget.sh "<keywords>" [install]   search the Fab library; with "install", install the first match (unreal-engine format)
D="$(cd "$(dirname "$0")" && pwd)"
OUT=$("$D/ct.sh" FabToolset.FabToolset SearchFabMyLibrary "$(python3 -c 'import json,sys;print(json.dumps({"Keywords":sys.argv[1]}))' "$1")")
ARGS=$(python3 -c '
import sys,json
d=json.loads(json.loads(sys.argv[1])["returnValue"])
rs=d.get("results",[])
for r in rs[:3]: print("#",r["title"],r["listingId"],[o["assetFormat"] for o in r.get("installOptions",[])],file=sys.stderr)
if not rs: sys.exit()
r=rs[0]; opts=r.get("installOptions",[])
o=next((o for o in opts if o["assetFormat"]=="unreal-engine"),opts[0] if opts else None)
if o: print(json.dumps(dict(listingId=r["listingId"],title=r["title"],**o)))
' "$OUT")
[ "$2" = install ] && [ -n "$ARGS" ] && { echo "install $ARGS"; "$D/ct.sh" FabToolset.FabToolset InstallFabListing "$ARGS"; }
