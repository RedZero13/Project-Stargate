# Local-only assets (not in git)

To keep GitHub storage small, the **Game Animation Sample** files live only on the developer's Mac.
They are ignored via `.gitignore`; the exact list is in [`gasp_local_files.txt`](gasp_local_files.txt) (1,378 files, about 1.2 GB).

## What is in git vs not
- **In git:** docs, config (`Config/*.ini`, including the sample's gameplay tags and settings), `HollowKin.uproject` (with the sample's plugins), and our own small assets (`BP_Max`, input actions, `IMC_Combat`, the test corridor level).
- **Not in git:** `Content/Blueprints/`, `Content/Characters/UEFN_Mannequin/`, `Content/Audio/`, `Content/Levels/`, `Content/Misc/` and the sample's `IA_*`/`IMC_Sandbox` input files.
  `BP_Max` is a child of the sample's `SandboxCharacter_CMC`, so it will not load without them.

## Restoring on another machine
1. In the Epic Games Launcher, get **Game Animation Sample** (free, Fab, by Epic Games) and create the project for UE 5.8.
2. Copy the files named in `gasp_local_files.txt` from that project's `Content/` into `HollowKin/Content/`, keeping the same relative paths:
   ```bash
   cd <GameAnimationSample>/Content
   sed 's#^HollowKin/Content/##' <repo>/docs/gasp_local_files.txt | rsync -a --files-from=- . <repo>/HollowKin/Content/
   ```
3. Restart the editor so the plugins and gameplay tags load.

## Back-ups
Anything not in git exists only on this Mac. Keep a Time Machine (or similar) back-up.

## Fab packs (local-only, from the developer's Fab library)
Installed into `HollowKin/Content/<PackFolder>/` from inside the editor (`FabToolset` → `InstallFabListing`, or Window → Fab → Add to Project). They are ignored by the Content allow-list in `.gitignore`.
Used by the slice right now: **Horror Ambient Sound Effects Pack_01** (`HorrorAmbientSFX`, room ambience), **Horror Music - Free Starter Kit** (music bed + menu theme), **Interface & Item Sounds Pack** (pickup/breaker/hint sounds). The sound waves listed in `tools/unreal_mcp/build_slice.py`-era scripts were set to *Looping* locally; re-set `bLooping` after reinstalling.
Also used now: **M1911 (FREE)** (`M1911`, pistol mesh), **Modern Pistols SFX** (`MW_Pistol_SK`, fire/reload), **Essential Footsteps SFX** (`Essential_Foosteps_SK`), **NEON WEX Free Muzzle Flash** (`NW_MuzzleFX`), **Save Room (Music Pack)** (`Save_Room_Music`, C3), **Realistic Starter VFX Vol 2** (impacts, drips, steam, sparks), **Table Lamp**, **Military Radio** (props), **Dead Bodies Sitting & Lying Poses** (`DeadBodies_Poses_nikoff`), **Warning signs decals Vol. 1** (`FD_WarningSigns_V1`). Installed, not used yet: Free Interaction Animation (lever/door anims), FREE Dramatic Death, Misc Props UB (`UnrealBucket`, swords only).
Also used now: **Horror Hospital** (`Horror_Hospital`, wall/floor/ceiling textures via `MI_HK_*`), **Kid Chalk Drawing** (`Kid_Chalk_Drawing`). Queued (may still be downloading): Sun/Cloud Chalk Drawing, Fog Area. Not re-queued yet: Survival Character, Car Chalk Drawing, Drip Streak + Dust Smudge Alpha, CCTV camera, flat icons, Glitch Noises, InfinitelyCloseNightmare, LAMENT, Essential Ambience SFX.

## Added 2026-11-25
- **Tactical Soldier Outfit for MetaHuman (UE 5.6+)** (Fab, FBX format) → `Content/Fab/Tactical_Soldier_Outfit_for_MetaHuman__UE_5_6+_/` (outfit + helmet) and `Content/Fab/Tactical_Soldier_Outfit/` (helmet, belt, sniper). Used by `BP_DeadSoldier`. **Import with the classic FBX importer**: type `Interchange.FeatureFlags.Import.FBX 0` in the editor's Cmd box first — the Interchange importer stalls for 15+ minutes on its bind poses and freezes the editor.
- **Sci-Fi Military Character** (free, Fab) → `Content/SciFiCharacter/`. Fallback soldier look; not used yet.
