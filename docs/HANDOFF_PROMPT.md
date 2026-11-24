# Paste this into a new Claude session (another account)

You are continuing work on **HOLLOW KIN**, a realistic third-person survival-horror game in **Unreal Engine 5.8** for Windows and macOS, built by a solo developer who is **new to Unreal: explain things simply**. The developer spends as little as possible.

**Repo:** `https://github.com/RedZero13/Project-Stargate`, branch `claude/unity-game-roadmap-hpl2oh` (PR #1). Local clone on the developer's Mac: `~/Documents/Unreal Projects/Project-Stargate` (the Unreal project is in `HollowKin/`). Run Claude in that folder. Commit and push to that branch after each working step, ending commit messages with a `Co-Authored-By:` line for the model you are.

**Do this first, in order:**
1. Read `docs/HANDOFF.md` (current state, patterns, known problems, progress log), then `docs/ROADMAP.md`, `docs/GDD.md`, `docs/ART_BIBLE.md`, `docs/UI_DESIGN.md`, `docs/levels/CONTAINMENT_WING.md`, `docs/narrative/PROLOGUE.md`, `docs/LOCAL_ASSETS.md` and `tools/unreal_mcp/README.md`.
2. Do not re-litigate the decisions listed in `docs/HANDOFF.md` (Unreal 5 realistic; title *Hollow Kin*; diegetic UI by default with the overlay HUD optional/off; Blueprint-first; Game Animation Sample assets stay **local-only, git-ignored**; only small files go to GitHub).
3. Make sure the editor is open on `HollowKin/HollowKin.uproject` (the editor's MCP server listens on `http://127.0.0.1:8000/mcp`). If your session has no `unreal-mcp` tools, drive it with `tools/unreal_mcp/*.sh` (see its README for the many gotchas: LFS file locks, vector formats, the `Windows close` hang, Blueprint DSL limits).
4. Setup needed on a new machine: Git LFS (`brew install git-lfs && git lfs install`), `export PATH=/opt/homebrew/bin:$PATH`, and the git credential for pushing (GitHub token).

**Then continue the mechanics backlog from the docs, one step at a time (build → test in Play → commit/push → append to the "Progress log" in `docs/HANDOFF.md`):**
Already done (see Progress log): death/respawn, Hollow Drone, gunshot noise, pickups, safe-room checkpoint save/load, low-sanity hallucinations, fuse/breaker/power-door puzzle, a ranged Guard, footstep noise, Mac build (`docs/BUILDING.md`). **Next, in order:** verify by hand what the log marks unverified (pistol killing a drone, stagger/ragdoll, hearing) → Guard cover/alert behaviour → footstep noise → inventory grid + examine view (data assets), doors, keys, fuse/breaker puzzle (see `docs/levels/CONTAINMENT_WING.md`) → sanity audio / aim sway / breakdown at 0 → Bond/Taint and the Hollow Child spare/kill choice → greybox the Containment Wing rooms C1–C9 and S1–S4 → main-menu `CONTINUE` using the save slot → settings menu (mouse sensitivity, overlay HUD toggle, flashing-effects toggle).

**Working rules:** save in the editor before and after each batch; stop Play before editing assets; never add `Event BeginPlay` to `BP_Max`; look up components by tag; keep large binaries out of git; tell the developer plainly what is and is not verified.

Before you near your own usage limit, update `docs/HANDOFF.md` (Progress log + known problems), commit, push, and give the developer a fresh copy of this prompt.
