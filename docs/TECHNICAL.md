# HOLLOW KIN — Technical Document

Everything an engineer needs to build, run, change and ship the game from scratch. Companion docs:
[`GDD.md`](GDD.md) (design, as built) · [`HANDOFF.md`](HANDOFF.md) (start here, current status) ·
[`BUILDING.md`](BUILDING.md) (packaging) · [`PLATFORMS.md`](PLATFORMS.md) (iPad, controllers, consoles) ·
[`ROADMAP.md`](ROADMAP.md) (what is left) · [`CHANGELOG.md`](CHANGELOG.md) (history).

Last full update: 2026-11-28.

---

## 1. Project at a glance

| | |
|---|---|
| Engine | **Unreal Engine 5.8.4** (Epic launcher build, `/Users/Shared/Epic Games/UE_5.8`) |
| Project file | `HollowKin/HollowKin.uproject` (Blueprint-only; no game C++ module) |
| Repo | GitHub `RedZero13/Project-Stargate`, branch `claude/unity-game-roadmap-hpl2oh` (Git LFS for binaries) |
| Company | Terratales Media Entertainment Private Limited (CIN U59112DL2012PTC229544) |
| Target platforms | macOS (Apple Silicon) now; Windows next; iPad (M-series) set up; consoles planned (`PLATFORMS.md`) |
| Dev machine | Mac Studio M4 Max (primary), MacBook Pro 14" M3 Pro (tests) |
| Rendering | Deferred, Lumen GI + reflections on High/Epic, off on Medium/Low; Virtual Shadow Maps; no Nanite dependence |
| Character base | Epic **Game Animation Sample** (GASP) `SandboxCharacter_CMC` + motion matching (local-only, see §11) |

**Blueprint-only by design.** Every gameplay system is a Blueprint built and edited through Epic's Unreal MCP plugin
by Python scripts in `tools/unreal_mcp/`. The scripts are the source of truth for logic: re-running a script rebuilds
its graphs. Hand edits in the editor are fine but will be overwritten if the script that owns that graph is re-run.

---

## 2. Repository layout

```
Project-Stargate/
  HollowKin/                     the Unreal project
    HollowKin.uproject
    Config/                      Default*.ini (+ IOS/IOSInput.ini)
    Content/HollowKin/           all game-owned assets (see §4)
    Content/<Fab packs>/         third-party packs (git-ignored, local only; see §11)
    Fonts_src/                   source TTFs + OFL licences (Cinzel, Barlow, Patrick Hand)
    SourceArt/                   source PNGs (icons, logo, hurt vignette, item renders)
    Build/                       platform build config (Mac/iOS plists)
  tools/
    floors_layout.py             generator for the stacked hospital floors (JSON)
    draw_floorplans.py           draws docs/floorplans/*.png from the layout
    playtest_report.sh           collects the playtest log into a shareable file
    make_builds.sh               builds both Mac versions (regular + playtest)
    make_cursor.py, make_icons.py, make_logo_b.py, make_music.py, make_art.py   asset generators
    voice/                       Kokoro TTS (venv + models git-ignored), lines.py = every voiced line
    unreal_mcp/                  ~140 scripts that build the game through the editor's MCP server (§5)
  docs/                          design + technical docs, floor plans
  marketing/                     store/trailer material
```

---

## 3. Levels and game flow

| Level | Path | Content |
|-------|------|---------|
| Main menu | `Maps/Lvl_MainMenu` | `BP_MenuGameMode` + `BP_MenuPlayerController` -> `WBP_MainMenu` |
| Prologue | `Maps/City/Lvl_City` | Rainy Millbrook street (Assetsville Town demo map copy), phone call, prologue events, paramedic choice, clinic door |
| Chapter 1 | `Maps/Clinic/Lvl_Clinic` | St. Brigid's clinic: G (OPD/emergency) + F1 (maternity/NICU), stairs, twin lifts, F1 service lift down |
| Chapter 2 | `Maps/Containment/Lvl_ContainmentWing` | B1 hand-built vertical slice: fuses, drawings, Hollow Child, pistol, breaker, power door |
| Chapter 3 | `Maps/Wards/Lvl_Wards` | B2–B8 stacked floors (generated), one puzzle gate per floor |
| Chapter 4 | `Maps/Deep/Lvl_DeepLabs` | B9 hand-built labs/tunnels/generator + B10–B15 stacked floors, isolation cells, endings |
| Test | `Maps/Containment/Lvl_TestCorridor` | Old darkness/flashlight test corridor |

Flow: Main menu -> NEW ADMISSION -> difficulty -> PROLOGUE card -> City -> clinic door (`BP_LevelDoor`) -> Clinic G ->
stairs to F1 -> F1 service lift (`BP_FloorLift.NextLevel`) -> Containment Wing -> wing exit (`BP_EndingTrigger` in
the wing travels on) -> Wards B2..B8 (lifts) -> B8 lift -> Deep Labs B9 -> B9 generator lift -> B10..B15 -> B15
ending trigger beside Emilia -> ending screen -> 14 s -> `EndRun` deletes the checkpoint and returns to the menu.
`MapsToCook` in `Config/DefaultGame.ini` lists exactly these maps (never use `-allmaps`: it cooks every Fab demo map).

### Stacked floors
Floors live in one map, stacked vertically: `FLOOR_DZ = 1500` cm apart (`BASE_Z`: wards 0, deep −2000; clinic goes
UP with `FLOOR_DZ_MAP['clinic'] = 470` so G and F1 form a real two-storey building joined by stairs). A lift ride is
a teleport between floors hidden behind closed doors (§6.4). `floors_<map>.json` (written by `build_floors.py`) holds
every floor's rooms, doors, corridors, cores, lift positions and arrival points; all placement scripts read it.

---

## 4. Content layout (`Content/HollowKin/`)

| Folder | Assets |
|--------|--------|
| `Blueprints/Player` | `BP_Max` (child of GASP `SandboxCharacter_CMC`) |
| `Blueprints/AI` | `BP_HollowDrone` (melee Hollow, ranged guard, undead nurse, Elite variants via tags/vars), `BP_Guard`, `BP_HollowChild`, `BP_Hallucination` |
| `Blueprints/Floors` | `BP_FloorLift`, `BP_Door`, `BP_Keycard`, `BP_SeqSwitch`, `BP_FloorGenerator`, `BP_Breaker`, `BP_Dial`, `BP_CellConsole`, `BP_MapBoard` |
| `Blueprints/Interactables` | `BP_Choice`, `BP_FlagGate`, `BP_Cutscene`, `BP_StreetEvent`, `BP_PhoneCall`, `BP_LevelDoor`, `BP_EndingTrigger`, `BP_Hint`, `BP_GunPickup`, `BP_BreakerPanel`, `BP_PowerDoor`, `BP_HazardBarrel`, `BP_HazardShock`, `BP_SafeZone`, `BP_SaveTerminal` |
| `Blueprints/Items` | `BP_Pickup` (one class, `PickupKind` 0–9) + legacy subclasses |
| `Blueprints/Props` | `BP_Emilia`, `BP_Child`, `BP_DeadSoldier`, `BP_DeadNurse` |
| `Blueprints/Systems` | `BP_HKGameInstance`, `BP_HollowSave` (checkpoint), `BP_SettingsSave`, `BP_ProgressSave`, game modes, `BP_MenuPlayerController` |
| `UI/Menus` | `WBP_MainMenu`, `WBP_Difficulty`, `WBP_PauseMenu`, `WBP_Settings` (Protocols), `WBP_Backpack`, `WBP_Credits`, `WBP_Achievements`, `WBP_Chapters`, `WBP_Journal`, `WBP_Choice`, `WBP_Loading` |
| `UI/Diegetic` | `WBP_ScreenFX` (objective, messages, HUD ring, overlays), `WBP_DeathScreen` (also endings), `WBP_WristMonitor`, `WBP_GunDisplay` |
| `UI/HUD` | `WBP_HUD` (optional overlay HUD, off by default), `WBP_TouchHUD` (iPad) |
| `UI/Maps` | `T_Plan_<floor>` (floor plans shown on the map screen) |
| `UI/Fonts` | Cinzel (titles), Barlow Semi Condensed (UI), Patrick Hand (journal) |
| `Audio/VO` | 32 Kokoro voice lines `VO_<id>` (source wavs beside them, git-ignored) |
| `Audio/Music` | Lullaby music box, ambient, tension loops |
| `Materials` | world-tile master `M_HK_WorldTile` + instances, `Materials/Clean/*` for the bright clinic, LED panel materials |
| `Input` (project root `/Game/Input`) | `IMC_Combat`, `IA_*` actions; GASP `IMC_Sandbox`; `HollowKin/Input/Look/IMC_Look_*` sensitivity contexts |

---

## 5. Tooling: how the game is built

### 5.1 The MCP connection
Epic's Unreal MCP plugin serves tools at `http://127.0.0.1:8000/mcp` while the editor runs. `tools/unreal_mcp/ui_lib.py`
wraps it: `call(toolset, tool, args)`. The session id lives in `tools/unreal_mcp/sid`; if the editor restarts, run
`: > sid; bash mcp.sh` to create a new session. `HK_TIMEOUT` (env, default 600 s) sets the per-call timeout.

Toolsets used most: `editor_toolset.toolsets.blueprint.BlueprintTools` (graphs as a Lisp-like DSL via
`write_graph_dsl` / `read_graph_dsl`, variables, functions, compile), `UMGToolSet.UMGToolSet` (widget trees),
`editor_toolset.toolsets.scene.SceneTools` (spawn/find/remove actors, load level), `ActorTools`, `ObjectTools`
(`get_properties` / `set_properties` as JSON), `AssetTools` (save, duplicate, find), `TextureTools.import_file`,
`StaticMeshTools` (bounds, convex collision), `ProgrammaticToolset.execute_tool_script` (batched calls in-editor),
`EditorAppToolset` (PIE start/stop, captures).

### 5.2 Blueprint DSL rules learned the hard way
- Bool variables drop the `b`: `bAiming` -> `GetAiming` / `SetAiming` (but function *pins* keep it: `:bAiming`).
- A variable named like another class's bool (e.g. `Unlocked` vs `BP_FloorLift.bUnlocked`) resolves to the wrong
  class. Rename (`AchList`).
- `(bind x (Cast...) (:then ...) (:CastFailed))` and `IsValid` with `(:"Is Valid" ...)` are branches: any statement
  after them in the same block is "unreachable". Put them last or restructure.
- `select` cannot output asset objects or enums; use `if` branches. Enum pins need literal strings in `if` arms.
- Use keyword pins for class literals: `:ComponentClass`, `:Tag`, `:InPlayRate`; positional class pins can be lost.
- Functions with underscores are called without them in the DSL (`HK_God` -> `CallFunction|HKGod`).
- `add_variable` twice creates `Name_0`; always check `list_variables` first. `set_variable_instance_editable`
  takes `variable_name`.
- `ObjectTools.set_properties` does not work on PIE actors.
- IMC `DefaultKeyMappings`: change elements and change size in separate calls (re-key first, then append).
- Some node names: `Appearance|SetBrushfromTexture` (Border, not Image), `Rendering|SetBoundsScale`,
  `Widget|HasAnyUserFocusedDescendants`, `Game|GetPlatformName`, `Math|Vector|DotProduct`.
- `read_graph_dsl` output is not always round-trippable; write fresh DSL from the scripts.
- **Newlines in DSL string literals must be real newline characters** (`"\n"` in a normal Python string). `"\\n"` is
  stored as a backslash + n and shows on screen as `\n` (this broke the Achievements screen and the journal).

### 5.3 Operational rules
- **Never send other MCP calls while `build_floors.py` runs** (it stalls past the timeout). Alone: ~1 min per floor.
- Never compile Blueprints while a Fab/Interchange import runs (editor deadlock).
- `load_level` fails if the current level has unsaved changes: `save_assets([])` first, then assert
  `get_current_level` before any destructive placement.
- Importing audio/fonts: there is no MCP import tool for them. Copy the file into `Content/...`, then accept the
  editor's "source files detected — Import" prompt (or Content Browser -> Import). **Keep the source file there**:
  deleting it makes the editor delete the asset.

### 5.4 Script catalogue (tools/unreal_mcp)
Run with `python3 <script>` from `tools/unreal_mcp`, editor open. Grouped by area (each file's docstring explains it).

| Area | Scripts |
|------|---------|
| Floors (generate/rebuild) | `floors_layout.py` (in `tools/`), `build_floors.py <map> <Lvl>`, `dress_floors.py <map>`, `place_floors.py <map>`, `declip.py <map>`, `rebuild_map.py <map>`, `rebuild_all.sh` (`MAPS="wards deep"`), `solid_props.py`, `solid_props2.py`, `clean_materials.py` |
| Floor gameplay | `floor_gameplay.py`, `lift_doors.py`, `puzzles2.py`, `floors_links.py`, `deep_relink.py`, `clinic_flow.py` |
| Story | `cutscenes.py`, `place_cutscenes.py`, `phone_call.py`, `prologue_events.py`, `choices.py`, `choices_place.py`, `endings6.py`, `vo_hookup.py` |
| Player | `inventory_logic.py`, `fire_fix.py`, `gameplay_fixes2.py`, `torch_and_gun.py`, `apply_settings_max.py`, `tickfx.py`, `wing_objectives.py`, `fix_restart_torch.py`, `deep_links.py` (carry), `debug_tools.py` |
| AI | `enemy_anims.py`, `guards.py`, `nurses.py`, `hazard_fix.py`, `fix_looks.py`, `child_look.py`, `soldier_fix.py` |
| Progress | `progress_system.py`, `achievements_data.py`, `achievement_hooks.py`, `chapter_select.py`, `journal_map.py` |
| UI | `build_title*.py`, `build_options*.py`, `build_backpack*.py`, `build_credits.py`, `build_achievements.py` (+ `../make_trophies.py`, `import_trophies.py`), `fix_menu_fonts.py`, `audit_ui.py`, `build_loading.py`, `build_hud_ring.py`, `build_objective.py`, `build_msg.py`, `menu_fit.py`, `menu_dedupe.py`, `bigger_buttons.py`, `controller.py`, `touch_hud.py` |
| Window / input | `fit_window.py`, `fullscreen_fix3.py`, `input_prefs.py`, `build_look_imcs.py`, `backpack_hooks.py` |
| Levels (hand-built) | `build_slice.py`, `dress_slice.py`, `place_*.py`, `build_city.py`, `city_night.py`, `city_colliders.py`, `lighting_pass.py`, `light_south.py` |
| Testing | `playtest_full.py`, `test_route.py`, `collect_positions.py`, `pie_probe.py`, `capview.py`, `playtest_log.py` |

---

## 6. Gameplay systems

### 6.1 Max (`BP_Max`)
Child of GASP `SandboxCharacter_CMC` (walk/run/crouch/jump/traverse via motion matching). Additions:
- **Look**: Survival Character mesh layered by leader pose on the hidden GASP mesh (`ApplyMaxLook`).
- **Torch** (`ToggleFlashlight`, spotlight tagged `Flashlight` in the left hand), **pistol** (M1911; hitscan
  `FirePistol` traced from Max along the aim line so walls near the camera don't eat shots; 6-round magazine,
  auto-reload, reserve cap 40), **melee** punch, **bottle throw** (noise lure).
- **Vitals**: Health 0–100, Sanity 0–100 (drops in darkness and when hurt; sedatives restore), `DmgMul` (difficulty /
  god mode), `LootMul`.
- **Story state**: `Bond`, `Taint` (0–100), `Flags` (`|flag|flag|`), `FreedChildren`, `RunKills`, `Drawings`, `Files`,
  `Journal`, `ObjLog`, `MapsFound`, `LastObjective`.
- **Interact** (E / Y): presses the nearest `BP_Door`, `BP_Breaker`, `BP_Dial`, `BP_CellConsole`, `BP_Choice` within 2 m.
- Functions worth knowing: `Notify`, `ShowNote` (also writes the journal), `SetObjectiveNote` (objective panel +
  log + level-start hooks), `Collect(Kind, Amount)`, `StoreCarry` / `RestoreCarry`, `SaveCheckpoint` /
  `LoadCheckpoint`, `ShowEnding`, `EndRun`, `OpenPause`, `OpenCase(Tab)`, `OpenJournal(Tab)`, `HKLog` (playtest log),
  `AchTick`, `HasFlag` / `AddFlag`, `FloorLabel`, `HK_*` debug commands.

### 6.2 Input
Enhanced Input: GASP `IMC_Sandbox` (movement, look, sprint, crouch, jump/traverse) + `IMC_Combat` (everything else).

| Action | Keyboard / mouse | Controller (Xbox names) |
|--------|------------------|-------------------------|
| Move / look | WASD / mouse | Left / right stick |
| Sprint / crouch / jump | Shift / C / Space | LB / B / A |
| Aim (hold) / aim toggle | RMB or Q / T | LT |
| Fire / reload / melee | LMB or Enter / R / V | RT / X / RB |
| Interact | E | Y |
| Torch / throw | F / G | D-pad up / D-pad down |
| Map / journal | M / J | D-pad left (map; tabs inside) |
| Backpack / workbench | B / I | View / D-pad right |
| Pause | P / Esc | Menu |
| Swap shoulder | Tab | R3 |

Menus: the first button takes focus on the first pad press; D-pad/stick navigates, A presses, B/Menu/View close
(`controller.py`). Sensitivity / invert-Y swap in one of ten small `IMC_Look_*` contexts (`build_look_imcs.py`).
iPad: on-screen sticks (`Config/IOS/IOSInput.ini`) + `WBP_TouchHUD` buttons, or any Bluetooth controller.

### 6.3 Enemies (`BP_HollowDrone`)
One class with variants: melee Hollow (Whisper mesh), **guard** (`Ranged`: Survival body + tactical outfit + AK,
warning shot first), **undead nurse** (tag `Nurse`), **Elite** (tag `Elite`, scale 1.25–1.3, 60% damage taken; the
brute and the Experiments). `Think` / `AlertCheck` / `AttackAnim` on Tick; navmesh movement with acceleration for
paths (no floating). `DroneHealth` (+30% in NG+). `DroneDie` ragdolls, counts kills. Hollows open doors they reach.
`BP_HollowChild`: walk up without aiming = spare (+40 Bond), damage it = +40 Taint.

### 6.4 Lifts (`BP_FloorLift`)
Placed at the lift door plane facing the lobby; builds frame + two sliding leaves + cabin light + floor indicator at
BeginPlay. `Gate` decides how it unlocks: 0 open, 1 keycard, 2 three switches in order (`Code`), 3 generator,
4 breakers, 5 3-digit counters (`Code`), 6 out of order (clinic G). `PowerLift()` unlocks. `DoorTick`: doors open when
Max is near and the lift works; standing in the cabin 1 s closes them; `StartRide` (4 s hum, notice) -> `EndRide`
teleports Max to `Target` (the next floor's arrival cabin) or opens `NextLevel` after `StoreCarry`. `Arrival = true`
lifts only open/close. `NoDoors = true` keeps the old fade-and-teleport (B9).

### 6.5 Puzzles
Keycard (`BP_Keycard`), three floor switches in an order given by a drawing (`BP_SeqSwitch` + lift `SeqHit`),
generator (`BP_FloorGenerator`), breaker panel "lights out" with 4 breakers (`BP_Breaker`, lift `BreakerHit`; start
states guaranteed solvable), 3-digit counter lock with digits on three notes (`BP_Dial`, lift `DialCheck`), B15 cell
release console (`BP_CellConsole`, needs 5 patient files), Containment Wing fuses + breaker + power door.
Gate per floor: `floors_layout.py` `MAPS` + overrides `GATE_OVERRIDE` in `place_floors.py`.

### 6.6 Items, crafting, collectibles (`BP_Pickup.PickupKind`)
0 ammo · 1 health gel (+40 HP) · 2 sedative (+35 sanity) · 3 fuse · 4 scrap parts · 5 chemicals · 6 glass bottle ·
7 Emilia's drawing (+20 Bond in the wing, +3 on floors; every 5 -> +1 gel) · 8 patient file (lore line by `Amount`;
every 5 -> +6 rounds) · 9 L-7 serum (full heal, +15 Taint). Workbench recipes: 6 rounds = 2 parts + 1 chem; sedative
= 2 chem; health gel = 1 part + 1 chem. Totals: 17 drawings, 14 files.

### 6.7 Choices and consequences
`BP_Choice` (E -> `WBP_Choice`, pauses): two options, each with Bond/Taint/gels/rounds deltas, a flag, a voice line,
optional spawns (Hollows) and `KillTag` (destroy actors with that tag). `VoiceQ` plays when the prompt opens.
`BP_FlagGate`: 1.5 s after a level starts, destroys actors tagged `GateTag` unless `NeedFlag` is set and `ForbidFlag`
isn't. Consequences are pre-placed actors with gate tags (`choices_place.py`).

Flags: `paramedic_saved` / `paramedic_robbed`, `nurse_freed` / `nurse_left`, `forgave_okafor` / `condemned_okafor`,
`took_meds` / `left_meds`, `guard_spared` / `guard_robbed`, `hale_mercy` / `hale_stand`, `evidence` / `wiped`,
`woke` / `let_sleep`, `NG+`.

### 6.8 Endings (`BP_Max.ShowEnding`, `endings6.py`)
Checked in order: **HOLLOW** (Taint ≥ 80) · **LANTERN LIT** (NG+ and cells opened and `evidence` and `left_meds`
and `nurse_freed` and Taint < 20) · **SIX DOORS** (cells opened, Bond ≥ 70, Taint < 40) · **LULLABY** (no kills this
run, Bond ≥ 40, Taint < 40) · **HOMECOMING** (Bond ≥ 70, Taint < 40) · **KIN** (Bond ≥ 40) · **LANTERN**. Epilogue
lines append for `evidence` / `wiped`, `forgave_okafor`, `hale_stand`. Logs `ENDING <NAME>`; unlocks NG+.

### 6.9 Saving and progress
| Save slot | Class | Contents |
|-----------|-------|----------|
| `HollowKinSlot1` | `BP_HollowSave` | checkpoint (level, position, vitals, items); written by lifts/save terminals; deleted on NEW ADMISSION / chapter / ending |
| `HollowKinSettings` | `BP_SettingsSave` | options: quality, window mode, volumes, sensitivity, invert Y, text size, overlay HUD |
| `HollowKinProgress` | `BP_ProgressSave` | achievements (`AchList`), endings seen, kills, crafts, best collectibles, chapters reached, `NGUnlocked`, `LastJournal` |
Level-to-level carry: `BP_HKGameInstance` `C*` fields (health, sanity, Bond, Taint, ammo, items, drawings, files,
run kills, flags, journal, objective log, maps found, pistol) via `StoreCarry` / `RestoreCarry`.
`SetChapterKit(Index)` resets the carry for chapter select / NEW ADMISSION; `StartNG` for New Game+.

### 6.10 Achievements (30)
List in `tools/unreal_mcp/achievements_data.py`; unlocked through `BP_HKGameInstance.Unlock(Id, Title)` (toast +
sound + save). Sources: `AchTick` (every 2 s: pistol, power, reached Wards / Deep Labs / B15, collectibles), `HKLog`
lines (`ENDING …`, `FLAG …`), `DroneDie` (kills, elite), craft functions, Hollow Child, choices, breakers, dials.
Screen: `WBP_Achievements` = summary + 3-column grid of trophy cards (badge, title, description, UNLOCKED/LOCKED;
locked cards dimmed). Badges are own art: `tools/make_trophies.py` (bronze/silver/gold/red by tier, glyph by category)
-> `HollowKin/SourceArt/Trophies/` -> `import_trophies.py` -> `/Game/HollowKin/UI/Trophies/T_Trophy_<id>`.

### 6.11 UI
Diegetic-first: objective panel top-left, message panel, RE4-style ammo/health ring bottom-right (`WBP_ScreenFX`).
Main menu: company logo -> splash -> content warning -> title -> menu (NEW ADMISSION, CONTINUE, NEW GAME + (after an
ending), CHAPTERS, PROTOCOLS, ACHIEVEMENTS, CREDITS, DISCHARGE). Menus are resolution independent
(ScaleBox -> 1920×1080 canvas). Journal screen: MAP (current floor plan once its evacuation board is found; clinic
always), JOURNAL (handwritten, every note/clue, newest first), OBJECTIVES (current + log).

### 6.12 Audio
Music classes via `SM_HKVolume`; volumes in settings. Ambience: HorrorAmbientSFX cues. Voice: Kokoro (§10).

### 6.13 Window and display (Mac)
`BP_MenuPlayerController.FitWindow`: if the saved setting is fullscreen -> WindowedFullscreen at desktop resolution;
else a 16:9 window at 80% of desktop height. Cursor is free in menus (`DoNotLock`), captured in play.
`Info.Template.plist` has `NSHighResolutionCapable`; `bAllowHighDPIInGameMode`. Lumen on High/Epic only
(`DefaultScalability.ini`); textures capped at 2048 on Mac (`DefaultDeviceProfiles.ini`).

---

## 7. Debug and developer tools (playtest build and editor only)
Console: press the ` key (left of 1) in the **Playtest** (Development) build or in PIE. Type `ke * <command>`:

| Command | Effect |
|---------|--------|
| `ke * HK_Help` | list commands on screen |
| `ke * HK_Dev` | developer mode on/off: god mode + all lifts powered + live overlay |
| `ke * HK_God` | god mode on/off |
| `ke * HK_Overlay` | overlay: floor, position, health, sanity, Bond, Taint, kills, flags |
| `ke * HK_Heal` · `ke * HK_GiveAll` | full vitals · pistol + ammo + items |
| `ke * HK_UnlockLifts` · `ke * HK_KillAll` | power every lift · kill every Hollow on the level |
| `ke * HK_Bond 80` · `ke * HK_Taint 10` | set Bond / Taint |
| `ke * HK_Flag nurse_freed` | add a story flag (§6.7) |
| `ke * HK_Chapter 3` | jump to chapter 0–4 |
| `ke * HK_Ending` | trigger the ending now |
Engine cheats after `EnableCheats`: `God`, `Fly`, `Ghost`, `Walk`, `Slomo 0.5`, `Teleport`, `ViewMode Unlit`, `Stat FPS`, `Stat Unit`.
Playtest log: every `HKLOG|time|level|position|event` line; `bash tools/playtest_report.sh` writes
`~/Desktop/HollowKin_Playtest_<date>.txt`. Raw: `~/Library/Containers/com.YourCompany.HollowKin/Data/Library/Logs/HollowKin/HollowKin.log`.

---

## 8. Building and packaging
See [`BUILDING.md`](BUILDING.md). Short version: `bash tools/make_builds.sh` (both), `… regular` or `… playtest`.
Shipping = regular (no console, no logs); Development = playtest. ICU data is copied into each app (the cook misses
it). Output: `~/Documents/Unreal Projects/Builds/HollowKin(.app|-Mac.zip)`, `HollowKin-Playtest(.app|-Mac.zip)`.
Windows needs a Windows PC (steps in BUILDING.md); iPad needs an Apple ID in Xcode (PLATFORMS.md).

---

## 9. Testing
- `playtest_full.py`: one continuous PIE run City -> B15 with PASS/FAIL per step (teleports stand in for walking;
  `route_positions.json` from `collect_positions.py`). Last full pass: 39/41 before layout v2; re-run after layout v2
  is still to do (positions changed).
- `test_route.py <map>`: per-map gate/lift route test. `pie_probe.py`: manual probes. Endings verified via HKLOG.
- Lift ride B10 -> B11, map board and journal verified in PIE on 2026-11-28.

---

## 10. Voice (Kokoro, offline)
`tools/voice/`: venv with `kokoro-onnx` + models (`kokoro-v1.0.onnx`, `voices-v1.0.bin`, git-ignored; Apache-2.0).
`lines.py` holds every line `id -> (voice, speed, text)`; `.venv/bin/python lines.py` renders `out/vo/VO_<id>.wav`.
Voices: Max `am_echo`, Jaz `af_sarah`, Emilia `af_sky`, Okafor `af_bella`, Hale `am_adam`, Leo `bm_george`, radio
`am_onyx`. Import: copy into `Content/HollowKin/Audio/VO/`, accept the import prompt, keep the wavs there.
`say.py "<text>" out/x.wav <voice>` for quick tests.

---

## 11. Third-party content and licences
Local-only packs (git-ignored, see `LOCAL_ASSETS.md`): Game Animation Sample (Epic), Horror Hospital, Survival
Character, Whisper, Tactical Soldier Outfit for MetaHuman, Zombie Nurse, Assetsville Town, Mega Street Props, Abandoned
Power Plant, Restaurant Scene, M1911, Modern Pistols SFX, NEON WEX muzzle flash, Realistic Starter VFX 2, Dead Bodies
poses, Warning Signs Decals, Blood Decals, Kid Chalk Drawing, Table Lamp, Military Radio, Horror Music Free Starter Kit,
Save Room Music, Horror Ambient SFX 01, Interface & Item Sounds, Essential Footsteps, Thunder Sounds, Free City
Ambiences, FP Flashlight — all Fab Standard License (credited in `WBP_Credits`). Fonts: SIL OFL (Cinzel, Barlow,
Patrick Hand). Voices: Kokoro (Apache-2.0). A new machine must install the same Fab packs from the owner's Fab
library (FabToolset can install them) before the project opens cleanly.

---

## 12. Known issues and limits
- The editor viewport captures are dark; judge lighting in PIE or a build.
- Floating/clipping props: `declip.py` handles most; report leftovers with screenshots.
- `read_graph_dsl` loses some literal pins (e.g. Notify messages) — keep scripts as the source of truth.
- Placeholder pieces still in: storybook prologue art, MetaHumans (Max/Emilia use pack characters), facial animation,
  lip-sync, full adaptive music. See ROADMAP status.
