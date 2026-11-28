# HOLLOW KIN — Handoff (start here)

For a new Claude account/session **or a human developer**. Read this page, then:
1. [`GDD.md`](GDD.md) — what the game is (as built) and what is still planned.
2. [`TECHNICAL.md`](TECHNICAL.md) — how everything is built: levels, Blueprints, systems, saves, input, tools, rules.
3. [`BUILDING.md`](BUILDING.md) — packaging Mac (and Windows) builds; [`PLATFORMS.md`](PLATFORMS.md) — iPad, controllers, consoles.
4. [`ROADMAP.md`](ROADMAP.md) — status and what is left. [`CHANGELOG.md`](CHANGELOG.md) — full history of every session.
Reference: `ART_BIBLE.md`, `UI_DESIGN.md`, `UI_REFERENCES.md`, `EXPANSION_PLAN.md`, `GENRE_RESEARCH.md`,
`LOCAL_ASSETS.md`, `ASSET_PLAN.md`, `levels/CONTAINMENT_WING.md`, `narrative/PROLOGUE.md`, `narrative/DIALOGUE_CH1.md`,
`floorplans/*.png`.

Updated 2026-11-28.

---

## 1. The project in one paragraph
HOLLOW KIN is a realistic third-person survival horror game in **Unreal Engine 5.8** by **Terratales Media
Entertainment Private Limited** (CIN U59112DL2012PTC229544). Max Hunt goes down fifteen floors under St. Brigid's
Clinic to find his sister Emilia. It is playable start to finish: prologue street, two-storey clinic, a hand-built
Containment Wing, seven generated ward floors, the Deep Labs and six more floors to the isolation cells, with puzzles,
enemies, crafting, six story choices with NPC arcs, seven endings, 30 achievements, chapter select and New Game+. The
whole game is Blueprint-only and is built by Python scripts that drive the editor through Epic's Unreal MCP plugin.

## 2. Current state
- **Playable:** full route City -> B15, all seven endings reachable (LANTERN LIT only in New Game+).
- **Latest builds:** `~/Documents/Unreal Projects/Builds/HollowKin-Mac.zip` (regular, Shipping) and
  `HollowKin-Playtest-Mac.zip` (Development: console, debug commands, playtest log).
- **Verified recently (PIE):** lift ride between floors, map boards, journal capture, ending logic (earlier runs).
- **Not yet verified by hand:** every choice's consequence chain, New Game+ start, chapter select, the prologue
  events, controller menus, the iPad build (needs your Apple ID). The automated full-route test
  (`playtest_full.py`) has not been re-run since the layout-v2 rebuild.
- Owner playtest feedback comes in as screenshots/videos and the playtest log
  (`bash tools/playtest_report.sh` -> `~/Desktop/HollowKin_Playtest_<date>.txt`).

## 3. Setting up a new machine
1. **Mac with Apple Silicon**, Xcode (latest), Epic Games Launcher -> **Unreal Engine 5.8**.
2. `git clone` the repo, `git lfs install && git lfs pull` (binaries are LFS). Branch `claude/unity-game-roadmap-hpl2oh`.
3. **Install the local-only content** (git-ignored, see `LOCAL_ASSETS.md` and TECHNICAL §11): the Game Animation
   Sample and the Fab packs from the owner's Fab library (Epic launcher Fab tab, or the editor's FabToolset
   `install_fab_listing`). Without them the maps open with missing meshes and the player has no animation.
4. Enable the **Unreal MCP** plugin (already in the .uproject) and open `HollowKin/HollowKin.uproject`. The MCP server
   starts on `http://127.0.0.1:8000/mcp`.
5. Tools: `cd tools/unreal_mcp; : > sid; bash mcp.sh` creates an MCP session; then `python3 <script>.py`.
   Voice: `cd tools/voice && python3 -m venv .venv && .venv/bin/pip install kokoro-onnx soundfile` and download the
   two Kokoro model files into `tools/voice/models/` (TECHNICAL §10).
6. Builds: `bash tools/make_builds.sh`.

## 4. How work is done (conventions)
- **Scripts are the source of truth** for Blueprint logic (`tools/unreal_mcp/*.py`, catalogue in TECHNICAL §5.4).
  Change the script, re-run it; avoid hand edits to graphs that a script owns.
- **Levels:** the stacked floors are regenerated: `python3 rebuild_map.py <clinic|wards|deep>` (build -> dress ->
  gameplay -> anti-clip), then `python3 choices_place.py` (choices/NPCs) and, for the Deep Labs, `place_cutscenes.py`.
  Layout/program changes go in `tools/floors_layout.py`; redraw plans with `tools/draw_floorplans.py`.
- **Rules:** never send other editor calls while `build_floors.py` runs; never compile during a Fab import; save
  before `load_level` and assert the current level before placing; keep voice wavs next to their assets.
- **Commits:** after each working step, push to the branch. Commit trailer:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` (use the model you are). No secrets in commits.
- **Owner preferences:** plain language, low cost, confirm before quitting the editor or deleting anything big,
  privacy for personal details.

## 5. Debug / developer mode (playtest build or editor)
Press ` in the playtest build, then `ke * HK_Dev` (god mode + lifts powered + overlay) or `ke * HK_Help` for the list.
Full table in TECHNICAL §7.

## 6. What to do next (priority order)
1. Owner playtest of the latest builds; fix what comes back (log + screenshots).
2. Re-run `collect_positions.py` + `playtest_full.py` for the new layouts; extend it to choices, NG+ and chapter select.
3. iPad build once the Apple ID is in Xcode (PLATFORMS §2).
4. Windows build (needs a PC) -> Steam page, demo, trailer (ROADMAP status).
5. Remaining content from GDD §12 (bosses, MetaHumans, lip-sync, accessibility, localisation).
