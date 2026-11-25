# Paste this into a new Claude session

You are continuing work on **HOLLOW KIN**, a realistic third-person survival-horror game in **Unreal Engine 5.8** for Windows and macOS, built by a solo developer who is **new to Unreal: explain things simply**. The developer spends as little as possible.

**Repo:** `https://github.com/RedZero13/Project-Stargate`, branch `claude/unity-game-roadmap-hpl2oh` (PR #1). Local clone on the developer's Mac: `~/Documents/Unreal Projects/Project-Stargate` (the Unreal project is in `HollowKin/`). Run Claude in that folder. Commit and push to that branch after each working step, ending commit messages with a `Co-Authored-By:` line for the model you are.

**Do this first, in order:**
1. Read `docs/HANDOFF.md` (current state, how to work, known problems, **Lessons that cost time**, progress log), then `docs/ROADMAP.md`, `docs/GDD.md`, `docs/levels/CONTAINMENT_WING.md`, `docs/LOCAL_ASSETS.md` and `tools/unreal_mcp/README.md`.
2. Do not re-litigate the decisions listed in `docs/HANDOFF.md` (Unreal 5 realistic; title Hollow Kin; diegetic UI by default with the overlay HUD optional/off; Blueprint-first; Game Animation Sample and Fab packs stay local-only, git-ignored; only small files go to GitHub).
3. Make sure the editor is open on `HollowKin/HollowKin.uproject` (MCP server on `http://127.0.0.1:8000/mcp`). Without unreal-mcp tools, use `tools/unreal_mcp/*.sh` (`ct.sh`, `rdsl.sh`/`wdsl.sh` to read/write Blueprint graphs, `fnt.sh` to find node types).
4. New machine: Git LFS (`brew install git-lfs && git lfs install`), `export PATH=/opt/homebrew/bin:$PATH`, and the GitHub token for pushing.

**State:** NEW ADMISSION → `Maps/City/Lvl_City` (rainy night town, phone call from Jaz, walk to St. Brigid's Clinic) → clinic door → `Maps/Containment/Lvl_ContainmentWing` (hospital-textured rooms C1–C9, Whisper-skinned Hollows, guard, elite Brute in C4, explosive barrels + electric puddles, safe room that restores sanity, fuses → breaker → power door → ending → main menu). Max uses the Survival Character mesh; punch on V, aim toggle on T. The developer played the wing start to finish by hand and confirmed pistol kills. Read the Progress log in `docs/HANDOFF.md` for what is verified.

**Fab:** the editor's `FabToolset` reads the developer's Fab library and installs packs into the project (sign in once with `FabSignIn`). Downloads are slow and one at a time; **don't load another level while they run** (it cancels them). Check which packs from `docs/LOCAL_ASSETS.md` ("Queued") actually arrived under `HollowKin/Content/`, and re-queue any that are missing.

**Next, in order** (build → test in Play → commit/push → append to the Progress log in `docs/HANDOFF.md`):
1. Ask the developer for results from the new Mac build (city → wing) and fix what they report.
2. Follow **Next steps A–D** in `docs/HANDOFF.md` (guards in the Tactical Soldier outfit, Rampage mini-boss, new zones: recreation room, break area, reception/lobby, diagnostic labs, abandoned power plant).
3. Polish: swap the wing's box props (beds, desk, lockers, bed in C8) for Horror Hospital meshes, add grime/blood decals from the kit, more chalk drawings in C6/C8, a real explosion sound for barrels.
3. Guard cover / investigate-noise behaviour; footstep noise verification.
4. Inventory grid + examine view (data assets), keys.
5. Sanity audio / aim sway; Hollow Child flee/cower + spare/kill check.
6. Surface rooms S1–S4; settings menu (mouse sensitivity, overlay HUD toggle, flashing toggle).

**Working rules:** save in the editor before and after each batch (`save_assets` with an empty list saves level actors); stop Play before editing assets; never add Event BeginPlay to BP_Max; look up components by tag; give every Blueprint function a unique name; keep large binaries out of git; tell the developer plainly what is and is not verified.

Before you near your own usage limit, update `docs/HANDOFF.md` (Progress log + known problems), commit, push, and give the developer a fresh copy of this prompt.
