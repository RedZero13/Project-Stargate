# Handoff — context for a new Claude session

Read this first, then `docs/ROADMAP.md`, `docs/GDD.md`, `docs/ART_BIBLE.md`, `docs/UI_DESIGN.md`, `docs/levels/CONTAINMENT_WING.md`, `docs/narrative/PROLOGUE.md`, `docs/LOCAL_ASSETS.md`, and `tools/unreal_mcp/README.md`.

## The project
- **HOLLOW KIN**: realistic third-person over-the-shoulder sci-fi survival horror in **Unreal Engine 5.8.4**, Windows + macOS. Solo developer, spending as little as possible, M4 Max Mac Studio. **New to Unreal: explain things simply.**
- Story: Max Hunt (21) breaks into a shut-down lab (Project LANTERN) to rescue his sister Emilia (15), turned into a "Hollow" by the L-7 serum. Cast: Max, Emilia, Dr. Huckley, Dr. Mán (villain), Jaz (radio), Nate.
- Repo: `RedZero13/Project-Stargate`, branch `claude/unity-game-roadmap-hpl2oh`, PR #1. Commit + push to that branch after each working step.

## Decisions already made (don't re-litigate)
Unreal 5 realistic 3D; title *Hollow Kin*; Chapter 1 first, 3 launch endings (hidden Bond/Taint); sanity is a resource; Ironman opt-in; Blueprint-first; Fab/MetaHuman/Game Animation Sample assets; ElevenLabs voices.
**UI decision (latest):** *diegetic by default* (monitor on Max, display on the pistol, screen tint/flash). The flat overlay HUD is built but **off by default** (`bShowOverlayHUD` on `BP_Max`) and will be finished later once the art style is final. No XP bar or skill tree.
**Storage decision:** only small files go to GitHub. The Game Animation Sample (~1.2 GB) is **git-ignored and local-only** (see `docs/LOCAL_ASSETS.md`).

## How to work
- Editor: open `HollowKin/HollowKin.uproject`. Claude may not have the `unreal-mcp` tools; use `tools/unreal_mcp/*.sh` (HTTP to the editor's MCP server on port 8000). Read its README (gotchas listed there).
- Save in the editor before/after every batch; stop Play-In-Editor before editing assets.
- LFS: `export PATH=/opt/homebrew/bin:$PATH`; lock a tracked `.uasset` (`git lfs lock <path>`) before the editor can save it. New files are writable.
- Commit trailer: `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.

## What exists (all under `HollowKin/Content/`)
- **Max:** `HollowKin/Blueprints/Player/BP_Max` is a child of the sample's `SandboxCharacter_CMC` (walk/run/crouch/jump/aim animations + camera). I added: flashlight (F; spot light on left hand, aimed with Max's facing), pistol (hold RMB to aim, LMB fire, R reload; 6-round mag, 16 reserve; hitscan from the camera; amber tracer + muzzle flash), health (100) / sanity (100, drains with flashlight off), hurt flash, `ReceiveAnyDamage` → `ApplyHurt`.
  - **Pattern:** my code lives in Blueprint functions called each frame from `Event Tick → UpdateCamera → EnsureCombatInput / AimFlashlight / TickVitals(TickFX, TickOverlay, TickDiegetic)`. Do **not** add an `Event BeginPlay` to `BP_Max` (it replaces the sample's BeginPlay and breaks movement). Components are found by **tag** (`Pistol`, `Muzzle`, `Flashlight`, `Wrist`, `Gun`).
  - Inputs: `Content/Input/Actions/IA_*` (mine: Aim, Fire, Reload, Flashlight, SwapShoulder (unused), Pause) mapped in `Input/IMC_Combat`; the sample's `IMC_Sandbox` (local-only) maps movement. Mouse sensitivity = `InputModifierScalar_1` in `IMC_Sandbox` (0.3).
- **UI:** `HollowKin/UI/` — `HUD/WBP_HUD` (overlay), `Diegetic/WBP_WristMonitor`, `WBP_GunDisplay`, `WBP_ScreenFX`, `Menus/WBP_MainMenu`, `WBP_PauseMenu` (P key, `OpenPause` on `BP_Max`). Game starts on `Maps/Lvl_MainMenu` (`BP_MenuGameMode`, `BP_MenuPlayerController`). `Lvl_TestCorridor` (greybox 20 m corridor + side room, dark post-process, manual exposure) is the playable test map; game mode `ThirdPerson/Blueprints/BP_ThirdPersonGameMode` uses `BP_Max` + the sample's `PC_Sandbox`.
- **Config:** sample plugins in `.uproject`, gameplay tags in `Config/DefaultGameplayTags.ini`, console vars/collision channels in `DefaultEngine.ini`.

## Known problems / unfinished
1. The diegetic displays (`WristMonitor` on Max's back via `spine_03`, `GunDisplay` on the pistol) now use **screen-space** widget components (they track the body and show live data). True 3D world-space widget planes never drew in Play (cause unknown; tried blend modes, rotations, offsets) — revisit only if a real 3D look is needed.
2. Shooting, pause key `P`, and menu button clicks are wired but only partly verified by hand.
3. Posture (limping at low HP), shoulder swap (removed with my old camera), settings menu, CommonUI/gamepad navigation: not built.
4. Messages like "AC_SmartObjectAnimation not available" are harmless (a sample component I left out).

## Next steps (roadmap Phase 2 / backlog items 6–14), in order
Health/damage/death → Hollow Drone (Behavior Tree + AI Perception) and Guard → noise events → inventory/pickups/doors/keys → safe room save/load → sanity effects + hallucination → Bond/Taint + Hollow Child choice → greybox the Containment Wing from `levels/CONTAINMENT_WING.md`.
(See the "Progress log" below for what was finished since this was written.)

## Progress log
- Diegetic displays working via screen-space widget components.
- Death/respawn: `Die` on `BP_Max` (HP 0 → `WBP_DeathScreen`, level restarts after 3.5 s). Built, not yet tested by hand.
- Hollow Drone: `Blueprints/AI/BP_HollowDrone` (custom sight/hearing/patrol/chase/attack/stagger/ragdoll logic in `Think`, `UpdateSight`, `HearNoise`, `TakeHit`, `DroneDie`); Max emits gunshot noise via `EmitNoise`. Navmesh volume + 2 drones placed in `Lvl_TestCorridor`. **Untested in Play** (editor froze while starting the test — see tools README).
- (update this list after every finished step)
