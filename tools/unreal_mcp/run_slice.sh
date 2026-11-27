#!/bin/bash
# usage: run_slice.sh <layout.py> <LevelName> <level path>   -> loads the level, rebuilds its greybox (tag Slice), saves
D="$(cd "$(dirname "$0")" && pwd)"; T=$(mktemp -d)
python3 "$D/../$1" > "$T/l.json" && python3 "$D/build_slice.py" "$T/l.json" "$2" > "$T/s.py" && cd "$D" && python3 - "$T/s.py" "$3" <<'PY'
import sys
from ui_lib import call
print(call('editor_toolset.toolsets.scene.SceneTools','load_level',{'level_path':sys.argv[2]}))
r=call('editor_toolset.toolsets.programmatic.ProgrammaticToolset','execute_tool_script',{'script':open(sys.argv[1]).read()})
print(str(r)[:400])
print(call('editor_toolset.toolsets.asset.AssetTools','save_assets',{'asset_paths':[]}))
PY
