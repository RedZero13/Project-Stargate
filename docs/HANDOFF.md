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
Health/damage/death → footstep-noise check → Guard cover/alert → inventory grid/examine, doors, keys, fuse puzzle → sanity audio/aim sway/breakdown → Bond/Taint + Hollow Child choice → greybox the Containment Wing from `levels/CONTAINMENT_WING.md`.
(See the "Progress log" below for what was finished since this was written.)

## Progress log
- Diegetic displays working via screen-space widget components.
- Death/respawn: `Die` on `BP_Max` (HP 0 → `WBP_DeathScreen`, level restarts after 3.5 s). Verified in Play.
- Hollow Drone: `Blueprints/AI/BP_HollowDrone` (custom sight/hearing/patrol/chase/attack/stagger/ragdoll logic in `Think`, `UpdateSight`, `HearNoise`, `TakeHit`, `DroneDie`); Max emits gunshot noise via `EmitNoise`. Navmesh volume + 2 drones placed in `Lvl_TestCorridor`. **Verified in Play:** drones patrol, see Max (sight range shrinks if his flashlight is off), chase, hit for 20 every 1.6 s, wrist monitor HP drops; at 0 HP the `TERMINATED` screen shows and the level restarts. Not yet verified by hand: pistol killing a drone (3 shots), stagger, ragdoll, hearing gunshots.
- Pickups: `Blueprints/Items/BP_Pickup` (+ `_Ammo` +6 reserve, `_Gel` +50 HP, `_Sedative` +40 sanity); walking into one calls `BP_Max.Collect`. Verified in Play; 4 placed in `Lvl_TestCorridor`.
- Safe-room save/load: `Interactables/BP_SaveTerminal` (walk in → `BP_Max.SaveCheckpoint`: saves HP/sanity/ammo/position to slot `HollowKinSlot1`, lifts sanity to 60); `LoadCheckpoint` runs once at start (from `EnsureCombatInput`); `NEW ADMISSION` deletes the slot. Verified (died → reloaded at the terminal). Main menu `CONTINUE` still greyed out.
- Hallucinations: `AI/BP_Hallucination` (blue-lit mannequin; vanishes when shot, approached within 2.6 m, or after 7 s). `BP_Max.TickHallucination` spawns one every 15–35 s while sanity < 40. Verified in Play. Still to do for sanity (GDD §5.4): whispers/audio, aim sway, heartbeat, breakdown at 0, restore from drawings / bright rooms.
- Footstep noise: `TickFootsteps` (running > 380 cm/s emits noise radius 8 m, sprint 12 m). Main-menu CONTINUE enabled when a save exists (`SetupContinue`, `DoContinue`). Compiles and runs without errors; footstep-triggered drone reactions not yet verified by hand.
- Fuse/breaker/door puzzle: `Items/BP_Pickup_Fuse` (kind 3, `BP_Max.Fuses`), `Interactables/BP_BreakerPanel` (needs 2 fuses → `BP_Max.bPowerOn`), `Interactables/BP_PowerDoor` (slides up when power is on). Verified in Play. **These pieces are spawned by `BP_ThirdPersonGameMode.SpawnTestLayout`, not placed in the level**, because the editor stopped writing newly placed actors to disk (one-file-per-actor level): placing + `Save Current Level` worked earlier but not later in the session. Move them into the level (place, save, confirm new files in `__ExternalActors__`) when that is fixed, then delete `SpawnTestLayout`.
- Mac build: `docs/BUILDING.md`. Packaged and launched OK (main menu loads); full playthrough of the packaged build still to be verified by a human. Fixed cook error by adding the `GameFeatureData` Asset Manager entry.
- Guard: `AI/BP_Guard` is a child of `BP_HollowDrone` with `bRanged=true` (stops at up to 14 m with line of sight, faces Max, shoots every 1.4 s, 70% hit, 12 dmg, blue tracer). Spawned by `SpawnTestLayout`. Verified in Play. Same mannequin look as drones (child components can't be restyled via the tools; set a different mesh in the editor). Not done: cover use, investigating noise before sight, alerting other enemies.
- Settings ("Protocols"): `UI/Menus/WBP_Settings` (overlay HUD on/off, reduce flashing on/off), saved to slot `HollowKinSettings` (`Systems/BP_SettingsSave`); opened from PROTOCOLS on the main and pause menus; `BP_Max.ApplySettings` reads them at start. Compiles clean. **Button clicks cannot be verified with the automation tools (simulated clicks only hover); a human must click through** main menu → PROTOCOLS, pause (P) → PROTOCOLS, and the two toggles. Still to add: mouse sensitivity, volume sliders, rebinding, subtitles.
- (update this list after every finished step)
