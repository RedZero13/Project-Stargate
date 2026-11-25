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

- **Do not call `SlateInspectorToolset Windows close` repeatedly right after starting Play**: once it hung the editor's game thread (had to wait/restart). Prefer leaving the Message Log popup alone, or fix the cause of the load-error message.
- Naming: do not name a Blueprint function the same as a native one (e.g. `MakeNoise`); use `EmitNoise`.
- **Saving placed level actors:** this level uses one-file-per-actor. `save_assets` on the level and `save_actor` do NOT write newly added actors. Use `SlateInspectorToolset Snapshot` to find the "Save Current Level" button ref (e.g. `b5`) then `Click {"ref":"b5","button":"left"}`; confirm new files appear under `Content/__ExternalActors__/`. Lock the `.umap` first (`git lfs lock`).

- **Saving new actors in one-file-per-actor levels (works reliably):** `AssetTools.save_assets` with an **empty list** saves every dirty package, including new external actors. (`save_actor` fails for actors that were never saved; the toolbar/File-menu clicks are unreliable.)
- **Ambiguous node names in the DSL** (e.g. `GetDynamicMaterial`, `SetScalarParameterValue`, functions called `Setup`/`UpdateHUD`/`ApplySavedVolumes` that exist on several classes): create the node with `create_node` + `declaring_class`, or give our functions unique names.
