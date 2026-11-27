# HOLLOW KIN — Art Bible (Unreal Engine 5, realistic)

> The source of truth for characters, environments, lighting and UI. If an asset breaks a rule here, either the asset changes or this document does, on purpose.

## 1. Technical baseline

| Setting | Value | Notes |
|---------|-------|-------|
| Engine | Unreal Engine 5 (latest 5.x) | Pin one version for the whole project; upgrade only between milestones |
| Global illumination | **Lumen** (software ray tracing) | Works on the M4 Max and on mid-range Windows GPUs. Hardware RT is optional on Windows |
| Geometry | **Nanite** for static environment meshes | Not for characters or foliage cards |
| Shadows | Virtual Shadow Maps | The flashlight's shadows are the most important horror feature |
| Anti-aliasing / upscaling | TSR (Temporal Super Resolution) | Plus DLSS/FSR plugins on Windows later |
| Units | 1 Unreal unit = 1 cm | Max is about 178 cm. Doors 100×210 cm, corridors 240–300 cm wide |
| Performance target | 60 fps at 1080p on an RTX 3060 / M-series Mac; 30–40 fps on Steam Deck (Low preset) | Budget with `stat unit` and Unreal Insights each milestone |
| Scalability | Low / Medium / High / Epic presets | Lumen and fog quality drop first on Low |

## 2. Look & mood

**Grounded realism with a gritty sci-fi edge.** References: *RE2 Remake* (material realism), *Silent Hill 2 Remake* (fog, decay), *Alan Wake 2* (the flashlight as a character), *The Callisto Protocol* (facility scale).

| Rule | Why |
|------|-----|
| About **60% of every frame is near-black** | Dread lives in what the player can't see |
| **Red only signals danger** (emergency beacons, blood, alarms) | Players learn to fear it |
| **Warm sodium light only in safe rooms and the surface clinic** | Relief should be *felt* |
| **Lantern blue belongs to Emilia and the Hollows** | If something glows blue, it's psychic |
| Exposure is fixed per area (no auto-exposure in gameplay) | Stops dark rooms from brightening up, which would kill tension |

### Colour per sector
| Sector | Key colour | Light sources |
|--------|-----------|---------------|
| St. Brigid's Clinic | Sodium orange `#e0a547` | Street lamps through windows, flashlight |
| Containment Wing | Rust red `#b8323a` | Rotating emergency beacons, flashlight |
| Research Labs | Clinic teal `#5fa39a` | Flickering fluorescents (light functions / animated intensity) |
| Maintenance Tunnels | None (void) | **Flashlight only**, plus wet reflections |
| Security Hub | Monitor blue `#8fd3ff` | Wall of CRT monitors (emissive + rect lights) |

**Post-processing** (one global Post Process Volume plus per-area volumes): film grain, a slight vignette, chromatic aberration only at low sanity, LUT colour grading per sector, and volumetric fog in every space.

## 3. Characters (MetaHuman)

| Character | Notes |
|-----------|-------|
| **Max** | Early 20s, brunette, thin, tired eyes. Worn hoodie under a cheap work jacket, ripped sneakers. Clothes get dirtier and bloodier per act (3 material variants) |
| **Emilia (human)** | 15 but small for her age. Brunette, hospital gown with laminated subject tags (`L-03 / HUNT, E.`) and children's drawings taped to her arms |
| **Emilia (Hollow)** | The same MetaHuman with: a nervous-system glow through the skin (an emissive material mask that pulses with her mood), a slow orbit of debris (Niagara: pens, syringes, toys), bare feet a few centimetres off the floor. **No creepy-girl clichés**: no hair over the face, no crab-walking. Heartbreaking first, frightening second |
| **Dr. Huckley** | Mid-30s, blonde, lab coat. Her Hollow (boss) form is the MetaHuman with a sculpted overlay: cracked skin with light bleeding through |
| **Dr. Mán** | 50s, Chinese-born. Immaculate suit under a lab coat. Boss rig: a psychic-dampening harness (Blender model) |
| **Jaz** | Late 20s. Technician's overalls, a headset, a homemade radio rig |
| **Nate** | Early 30s, ex-soldier. A subject's gown under scavenged tactical gear |
| **Guards** | 2–3 MetaHuman variants sharing one uniform |

**Hollows (enemies):** MetaHuman bodies with heavy sculpted damage made in Blender, plus shared "lantern node" glow materials. Each has a readable silhouette:
- **Drone:** hunched, one oversized arm.
- **Screamer:** an elongated jaw.
- **Child:** small, fast, crouched.

**Workflow:** create in MetaHuman Creator → assemble in Unreal → add clothing (Fab, or Marvelous Designer / Blender) → set up LODs for gameplay.

## 4. Environments
- **One modular kit** (sci-fi lab/hospital, from Fab) for every interior, varied per sector by lighting, decals and **material instances**, never by new meshes.
- **Megascans surfaces and decals** for grime, water damage, blood, paper debris.
- **Hero props** in Blender: the cracked observation tank, Emilia's bolted bed, L-7 injectors, the breaker panel, the lift.
- **Emilia's drawings** are the only deliberately "childish" art: scanned crayon drawings (draw them yourself or AI-assist, then clean up) on decals and paper meshes.
- Level workflow: **greybox** with Modeling Mode / simple blocks → playtest → dress with the kit → lighting pass.

## 5. Animation
| Source | Used for |
|--------|----------|
| **Game Animation Sample** (Epic, free) | Max's motion-matched locomotion, traversal |
| Fab / marketplace packs | Pistol, shotgun and knife sets; zombie-style locomotion for Hollows; hit reactions |
| **MetaHuman Animator** | Facial animation from audio (ElevenLabs lines) or iPhone capture |
| Control Rig in Sequencer | Hand-keyed fixes for cutscenes |
| Physics (ragdoll / physical animation) | Deaths, stagger blending |

## 6. Storybook panels & key art
- 2D painted panels for flashbacks (the crash, the children, Huckley's letters), shown with a slow parallax pan.
- **This is where AI-assisted concepts help most:** generate the composition and mood, then paint over it. Never ship raw AI output, and record every use in `ASSET_LOG.md` for Steam's AI disclosure.

## 7. UI
> Detailed HUD and menu spec: [`UI_DESIGN.md`](UI_DESIGN.md). Where the two differ, `UI_DESIGN.md` is newer.

- RE-style diegetic and clinical: the inventory is a medical tray with a grid of 6–10 slots, files open as photographed paper, the map is a clinical facility plan.
- Font: a licensed clinical sans plus a monospace for terminals (free options such as *IBM Plex Sans / Mono*).
- Built with **CommonUI + UMG**, so it supports gamepad from day one.
- Damage: a red edge pulse. Low sanity: vignette, grain and grading. Flashing effects can be switched off in settings.

## 8. Content folder & naming
```
Content/HollowKin/
  Characters/{Max,Emilia,Huckley,Man,Jaz,Nate,Guards,Hollows}/
  Environments/{Kit,Props,Decals,Materials}/
  Maps/{Prologue,Clinic,Containment,Labs,Tunnels,Security}/
  Blueprints/{Player,AI,Items,Interactables,Systems}/
  Audio/{Music,SFX,VO,Ambience}/
  UI/  Cinematics/  FX/
```
Prefixes: `BP_` Blueprint, `SK_` skeletal mesh, `SM_` static mesh, `M_` / `MI_` material / instance, `T_` texture, `NS_` Niagara, `ABP_` anim blueprint, `WBP_` widget, `LS_` level sequence, `DA_` data asset, `SW_`/`SC_` sound wave / cue.
