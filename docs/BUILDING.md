# Building and testing HOLLOW KIN (Mac)

> The Game Animation Sample assets are local-only (`LOCAL_ASSETS.md`), so a build can only be made on a machine that has them.

## Make a Mac test build (proof of concept)
From the repo folder, in a terminal:

```bash
"/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun \
  -project="$PWD/HollowKin/HollowKin.uproject" -noP4 -platform=Mac -clientconfig=Development \
  -build -cook -allmaps -stage -pak -archive \
  -archivedirectory="$HOME/Documents/Unreal Projects/Builds/HollowKinMac" -utf8output
```
- Takes roughly 15–40 minutes the first time (shaders and the 1.2 GB animation set are cooked).
- **The runnable build is the staged folder** `HollowKin/Saved/StagedBuilds/Mac/` (contains `HollowKin.app`, `HollowKin/Content/Paks`, `Engine/`; about 1.8 GB). Copy the **whole folder** somewhere (e.g. `~/Documents/Unreal Projects/Builds/HollowKinMac_Test`) and open `HollowKin.app` inside it. The `-archive` output only contains the bare executable and will not start (missing libraries and content) — ignore it.
- First launch may need right-click → Open because it is unsigned.
- Builds are **not** committed to git.
- Needs Xcode and the Metal toolchain (see the first handoff notes).

## What to test in the build
1. Main menu appears (NEW ADMISSION; CONTINUE is greyed until a save exists).
2. WASD, mouse look (sensitivity was lowered), Shift run, C crouch, Space jump.
3. `F` flashlight; hold right mouse to aim, left mouse fire, `R` reload.
4. The monitor on Max's back shows HP and sanity; ammo shows by the pistol while aiming.
5. Two Hollow Drones patrol the corridor. Gunshots and running draw them.
6. Pick up glowing items (amber ammo, green gel, blue sedative, white fuse).
7. Collect both fuses (one near the start, one at the far end), walk into the breaker panel (red glow) in the corridor: the side-room door slides open.
8. Amber save terminal in the corridor saves a checkpoint. Dying reloads from it.
9. `P` opens the pause menu.
10. Keep the flashlight off for a while: sanity drains; below 40 blue ghosts appear.

## Status
Built successfully on 2026-11-24 (took about 1.5 minutes after the first compile). Launched from a terminal: the game started and loaded `Lvl_MainMenu`. A required project setting (Asset Manager entry for `GameFeatureData` in `Config/DefaultGame.ini`) was missing and had made the first cook fail; it is fixed. Not yet checked by hand: clicking through the menu into the test corridor in the packaged build.

## Known limits of this build
Placeholder art (grey blocks, mannequin characters, cube pistol), almost no audio, no settings menu, Development build (not optimised, console available), Windows build not possible from a Mac (see `ROADMAP.md` §2.3).
