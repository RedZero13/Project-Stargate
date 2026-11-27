# HOLLOW KIN — Asset plan: what you can do while Claude builds mechanics

> Rules of the road (from `ART_BIBLE.md` and `ROADMAP.md`): one modular kit for all interiors; MetaHuman for every human; Game Animation Sample for locomotion; AI concepts are reference only; log every asset in `docs/ASSET_LOG.md` (source, licence, AI involvement; Steam needs AI disclosure).
> **Prices change.** Search results below were not price-verified. Check each Fab page, use the "Fab Limited-Time Free" collection, and buy on sale.
> **Repo cost rule:** keep big binaries out of GitHub (see `LOCAL_ASSETS.md`). Put purchased packs in the project on your Mac; only small files are committed.

## How to hand assets to Claude
1. Add the pack in the editor (Fab → Add to Project, UE 5.8). It lands in `Content/<PackName>/`.
2. Add one line to `docs/ASSET_LOG.md`: name, URL, licence, price, date, "AI involved: yes/no".
3. Tell Claude "pack X is in the project". Claude then wires it (materials, blueprints, animations) and moves the pieces into the `Content/HollowKin/...` folders from the Art Bible.

## Priority order (do these first → later)
| # | Task | Why now | Who | Notes |
|---|------|---------|-----|-------|
| 1 | **Modular lab/hospital kit** | Unblocks greyboxing → real rooms (Containment Wing) | You (choose, buy) + Claude (dress) | Candidates found: *Sci-Fi Research Facility* modular pack (horror sci-fi, ~69 meshes, UE 5.7 tag), *Low Poly Sci-Fi Laboratory 1* (stylised, 84 meshes), *Sci-Fi Facility Kit 2* (clean/white — weaker for horror), *Medical Props Vol1* (~$10), hospital modular sets (~$33), a free *Wall Ceiling Floor Module*. Sources: [Fab medical buildings](https://www.fab.com/category/3d-model/buildings-architecture--medical-buildings?lang=en), [forum: stcn Modular Sci-Fi Research Facility](https://forums.unrealengine.com/t/stcn-modular-sci-fi-research-facility/2714474), [Digital Production](https://digitalproduction.com/2026/06/11/free-sci-fi-station-lands-on-fab/). Pick **one** kit and stay on it. |
| 2 | **Pistol/shotgun/knife animations + meshes** | Combat currently has a cube for a gun and no reload/fire animation | You (find), Claude (wire) | Need third-person weapon sets for the **UE5 mannequin skeleton** (the Game Animation Sample has no weapons). Search Fab for "pistol animation UE5 third person", "shotgun", "knife melee". Also weapon meshes with PBR textures and muzzle-flash VFX. |
| 3 | **Enemy animations (Hollows)** | Drone currently uses the unarmed mannequin | You | Fab has zombie mocap sets that fit the UE5 skeleton, e.g. *Gamma Studio Zombie Animation* (89 anims), *Zombie Performance Pack Vol. 1* (172 anims), *Undead Horde Animation Pack*. See [Gamma Studio](https://forums.unrealengine.com/t/gamma-studio-zombie-animation-vicon-mocap/2856638.md), [Undead Horde](https://forums.unrealengine.com/t/undead-horde-animation-pack/2747510). Free alternative: Mixamo (check licence). Need: shamble, run, lunge, stagger, hit reactions, death, grab. |
| 4 | **MetaHumans** | All human characters | **You only** (MetaHuman Creator UI cannot be driven by Claude) | Max, Emilia (human + Hollow), Dr. Huckley, Dr. Mán, Jaz, Nate, 2–3 guards. ~1 evening for Max and Emilia first. Export to the project; Claude sets them up in Blueprints. |
| 5 | **Audio** | Currently silent apart from the sample's foley | You (source), Claude (wire in MetaSounds) | Needs: HVAC/ambience loops, emergency alarm, heartbeat, whispers, gunshots, weapon handling, Hollow vocals, door/locker sounds, UI clicks, **Emilia's lullaby** (music box). Free/cheap sources: Fab sound packs, Sonniss GDC bundles, freesound (CC0 only), or compose/commission the lullaby. Voices: ElevenLabs paid plan (see `ROADMAP.md` §2.6). |
| 6 | **Fonts and UI art** | Menus use engine Roboto | You | IBM Plex Sans / Plex Mono (open licence) per Art Bible §7; barcode/stencil label graphics; subject-photo style frames; icons for items. |
| 7 | **Emilia's drawings and storybook panels** | Core collectible + flashback cutscenes | You (draw / AI-assist then paint over) | ~12 child drawings for puzzles and collectibles; 6–8 storybook panels (crash, the children, the letter). Log any AI use. |
| 8 | **Mood board + concept art** | Locks the look before final dressing | You | Put images in `docs/reference/`. Reference only. |
| 9 | **Props and decals** | Dressing and storytelling | You + Claude | Hospital beds, observation tank (Blender hero prop), lockers, breaker panel, fuse tiles, injectors, files/notes. Megascans decals (blood, grime, water damage) are free in Fab. |
| 10 | **Vehicles/surface: St. Brigid's clinic exterior** | Slice start area | later | A small exterior kit or a few Megascans buildings. |

## Plugins and engine features (mostly built in)
| Item | Cost | Use | Status |
|------|------|-----|--------|
| **CommonUI** | free (UE plugin) | Gamepad-friendly menus, input prompts, settings screens | Not enabled yet; move menus onto it before the demo |
| **Enhanced Input** | built in | Inputs and rebinding | In use |
| **MetaSounds** | built in | Adaptive music (calm/tension/combat/chase), ambience, sanity audio | Not used yet |
| **Niagara** | built in | Muzzle flash, impacts, blood, Emilia's debris halo, dust | Not used yet |
| **Chooser / PoseSearch / Mover** | built in | Used by the Game Animation Sample | Enabled |
| **StateTree / Behavior Tree + AI Perception** | built in | Guard AI and replacing hand-rolled drone perception later | Enabled (StateTree) |
| **Sequencer + MetaHuman Animator** | built in / free | Cutscenes, lip-sync from ElevenLabs lines | Later |
| **Steam (Online Subsystem Steam / Steamworks)** | free | Achievements, cloud saves, Steam Deck | Needs Windows build machine anyway |
| **DLSS / FSR plugins** | free | Upscaling on Windows | Later |
| **Sentry or Unreal Crash Reporter** | free tier | Crash reports after launch | Phase 6 |
| **Wwise / FMOD** | free for small indies | Only if MetaSounds proves limiting; avoid unless needed | Skip for now |

## Parallel work split
**You (assets):** pick/buy the kit (#1), pistol + shotgun anims/meshes (#2), zombie anims (#3), MetaHuman Max & Emilia (#4), start sourcing audio (#5), fonts (#6).
**Claude (mechanics, in order):** doors/keys/breaker puzzle → Guard enemy → weapon data assets + shotgun/knife → inventory + examine view → sanity audio/aim sway/breakdown → Bond/Taint + Hollow Child choice → rebuild the Containment Wing from your kit → settings/accessibility menu → CommonUI move → Mac demo builds.
**Both:** playtest the 10-minute opening and note where it drags or confuses.

## Decisions needed from you
1. Which modular kit (#1) — then Claude plans material instances per sector (teal labs, rust-red wing, etc.).
2. Windows build machine: cloud PC vs used PC (needed for Steam demo and Windows testers).
3. Whether to buy a paid weapon-animation pack or keep the cube gun until the shotgun is built.
