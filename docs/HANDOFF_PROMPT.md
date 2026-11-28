# Paste this into a new Claude session (or give it to a new developer)

You are continuing **HOLLOW KIN**, a realistic third-person survival horror game in **Unreal Engine 5.8** by
Terratales Media Entertainment, built by a solo owner who wants plain language and low cost.

**Repo:** `https://github.com/RedZero13/Project-Stargate`, branch `claude/unity-game-roadmap-hpl2oh`. Local clone:
`~/Documents/Unreal Projects/Project-Stargate` (Unreal project in `HollowKin/`). Commit and push after each working
step; end commit messages with `Co-Authored-By: <the model you are> <noreply@anthropic.com>`.

**Read first, in order:** `docs/HANDOFF.md` (state, setup, conventions, next steps) -> `docs/TECHNICAL.md` (every
system, the Blueprint DSL rules, the script catalogue, saves, input, debug, builds) -> `docs/GDD.md` (design as
built) -> `docs/ROADMAP.md` (status table) -> `docs/PLATFORMS.md` -> `docs/CHANGELOG.md` (history, only as needed).

**Before touching the editor:** open `HollowKin/HollowKin.uproject` (MCP on `http://127.0.0.1:8000/mcp`), then
`cd tools/unreal_mcp; : > sid; bash mcp.sh`. All game logic is in `tools/unreal_mcp/*.py` scripts: change a script
and re-run it rather than hand-editing graphs. Never run other editor calls while `build_floors.py` runs. Never
compile while a Fab import runs. Save before `load_level` and check the current level before placing actors.

**Then:** ask the owner for their latest playtest results (`~/Desktop/HollowKin_Playtest_<date>.txt`, screenshots),
fix what they report, rebuild with `bash tools/make_builds.sh`, and keep `docs/HANDOFF.md` and `docs/CHANGELOG.md`
current before you stop.
