# Building and testing HOLLOW KIN (Mac)

> The Game Animation Sample assets are local-only (`LOCAL_ASSETS.md`), so a build can only be made on a machine that has them.

## Make a Mac test build (proof of concept)
From the repo folder, in a terminal:

```bash
"/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun \
  -project="$PWD/HollowKin/HollowKin.uproject" -noP4 -platform=Mac -clientconfig=Shipping \
  -build -cook -stage -pak -compressed -utf8output
```
- Cooks only the maps in `MapsToCook` (`Config/DefaultGame.ini`: main menu, city, wing, test corridor). Do **not** use `-allmaps` (it would cook every Fab demo map).
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

## Fixes after first human test (2026-11-24)
- **Crash at launch** (`FICUInternationalization::Initialize` fatal): the build had no `Engine/Content/Internationalization` (ICU data). Fixed by `InternationalizationPreset=English` + `CulturesToStage=en` in `DefaultGame.ini`. Rebuild required.
- **Menu not clickable on a 32:9 5120x1440 monitor:** cause not confirmed. Default window is now 1920x1080 windowed (`DefaultGameUserSettings.ini`). If clicks still miss, report the window size and whether hover highlights appear.
- Config staging alone did not copy the ICU data. **Manual step after each build:** `cp -R "/Users/Shared/Epic Games/UE_5.8/Engine/Content/Internationalization/English/." <build>/Engine/Content/Internationalization/` (mkdir first). Launch then runs without the crash. A `DirectoriesToAlwaysStageAsNonUFS` entry was added to try to automate this; unverified.

## Sending the build to another Mac (2026-11-25)
1. After the build, copy the ICU data (manual step above) into the staged folder.
2. Zip the **whole** staged folder `HollowKin/Saved/StagedBuilds/Mac/` (right-click → Compress, or `ditto -c -k --keepParent <folder> HollowKinMac.zip`).
3. On the other Mac: unzip, then because the app is unsigned run `xattr -cr <folder>/HollowKin.app` once in Terminal (or right-click → Open → Open). Apple Silicon or Intel Mac with Metal SM6 support.
4. Trackpad play: two-finger click held = aim, or press **T** to toggle aim; click / **E** = fire, **V** punch, **R** reload, **F** flashlight, **Tab** swap shoulder, **P/Esc** pause.
5. The game starts borderless full screen at the monitor's resolution (works on 16:9, 21:9 and 32:9). Alt+Enter / F11 switches to a window.

## Smaller builds (2026-11-25)
The first test build was 4.3 GB. Why, and what changed:
- **Result (2026-11-25):** app 1.4 GB, zip 0.97 GB. Copy the ICU data into `HollowKin-Mac-Shipping.app/Contents/UE/Engine/Content/Internationalization/`, rename the app to `HollowKin.app`, zip it alone with `ditto -c -k --keepParent`.
- **Half of it was a duplicate.** The staged folder holds the game twice: inside `HollowKin.app/Contents/UE/` and again in the loose `HollowKin/` + `Engine/` folders next to it. The app only reads the copy inside itself, so **send only `HollowKin.app`** (zip it alone).
- **Shipping instead of Development:** the executable drops from 433 MB to a fraction of that, with no debug console (`-clientconfig=Shipping`, `BuildConfiguration=PPBC_Shipping`).
- **Compressed paks** (`-compressed`, `bCompressed=True`): Oodle compression of the game data.
- **Textures capped at 2048** on Mac (`Config/DefaultDeviceProfiles.ini`): Fab packs ship 4K textures; the cook now drops the top mip. Raise `MaxLODSize` back to 16384 for a high-quality build.
- Biggest remaining item: the Game Animation Sample animation set (about 1.2 GB raw). Trimming unused animations is a later step.

## Windows build (needs a Windows PC)
Unreal cannot build a Windows game from a Mac. To make one:
1. On a Windows 10/11 PC (or a cloud Windows machine such as AWS/Azure/Shadow with a GPU), install the Epic Games Launcher, then **Unreal Engine 5.8**. In the engine's install options, tick the Windows target.
2. Install **Visual Studio 2022** (Community is free) with the workloads "Game development with C++" and "Desktop development with C++", plus a Windows 10/11 SDK.
3. Install **Git** and **Git LFS**, then clone: `git clone https://github.com/RedZero13/Project-Stargate.git`, check out `claude/unity-game-roadmap-hpl2oh`, and run `git lfs pull`.
4. Copy the Fab packs across. They are not in git. Either re-install each pack from Fab inside the editor (list in `docs/LOCAL_ASSETS.md`), or copy the `HollowKin/Content/<PackName>` folders from the Mac.
5. Open `HollowKin/HollowKin.uproject` once so shaders compile. Then, in a Command Prompt at the repo folder:
   ```
   "C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="%CD%\HollowKin\HollowKin.uproject" -noP4 -platform=Win64 -clientconfig=Shipping -build -cook -stage -pak -compressed -utf8output
   ```
6. The game is in `HollowKin\Saved\StagedBuilds\Windows\`. Zip that whole folder. The app icon comes from `HollowKin/Build/Windows/Application.ico`.
On Windows, the ICU copy step is usually not needed; if the game crashes at start with an ICU/Internationalization error, copy `Engine\Content\Internationalization\English` the same way as on the Mac.
