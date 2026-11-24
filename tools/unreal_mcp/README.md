# Driving the Unreal editor from the shell (Epic's MCP server)

The editor (with the *Model Context Protocol* + *All Toolsets* plugins) serves MCP over HTTP at `http://127.0.0.1:8000/mcp`.
If your Claude session does not have the `unreal-mcp` tools loaded, these scripts talk to it directly.

```bash
cd tools/unreal_mcp
./mcp.sh list_toolsets '{}'            # opens a session, writes ./sid
./mcp.sh describe_toolset '{"toolset_name":"editor_toolset.toolsets.blueprint.BlueprintTools"}'
./ct.sh <toolset> <tool> '<json args>' # call one tool, e.g.
./ct.sh EditorToolset.EditorAppToolset StartPIE '{"options":{}}'
./cap2.sh out.png                      # screenshot the whole editor (works during Play)
```
- Blueprint logic is written with `BlueprintTools.write_graph_dsl` (S-expression DSL, see `get_graph_dsl_docs`).
  Enhanced Input event nodes cannot be written in the DSL: create them with `create_node` and connect with `connect_pins` (see `wire.sh`).
- `ui_lib.py` / `menu_common.py` / `menu_logic.py` build UMG widgets; `gen.py` shows the tag-based component lookup pattern used by `BP_Max`.
- Gotchas learned: `set_properties` values must be a JSON *string*; on live PIE objects write vectors as `"(X=1,Y=2,Z=3)"` (a JSON dict only sets X);
  LFS-tracked `.uasset` files are read-only until `git lfs lock <file>`; run `export PATH=/opt/homebrew/bin:$PATH` so git finds git-lfs;
  a Message Log window may pop over Play - close it with `SlateInspectorToolset Windows {"action":"close","index":1}`.
