# HOLLOW KIN — Pixel Art Bible

> The source of truth for every sprite, tile and UI element. If an asset breaks a rule here, either the asset changes or this document does, on purpose.

## 1. Technical spec (locked: changing these later means redrawing everything)

| Setting | Value | Notes |
|---------|-------|-------|
| Perspective | Top-down ¾ (as in Stardew Valley) | Walls show their front face; floors are seen from above |
| Tile size | **16×16 px** | Unity *Pixels Per Unit* = **16** |
| Character height | **~32 px** (2 tiles) | Children ~24 px; bosses up to 64 px |
| Internal resolution | **480×270** | Scales cleanly: ×4 = 1920×1080, ×8 = 3840×2160 |
| Visible area | ~30×17 tiles | Tight framing makes the game scarier |
| Camera | Unity **Pixel Perfect Camera**, *Upscale Render Texture* on | Keeps 2D lights and post effects pixelated too, so they match the art |
| Texture import | Filter **Point**, Compression **None**, Mip Maps **off** | Set by an import preset in `Assets/Art/` |
| Sprite pivot | Bottom-centre (feet) | Correct Y-sorting for the ¾ view |
| Sorting | Transparency Sort Axis **(0, 1, 0)**, sorting layers `Floor → Decals → Props → Characters → Overhead → FX → UI` | |
| Sub-pixel motion | Off; positions snapped to the pixel grid | Unity's `2d-pixel-perfect` skill audits this |
| Lighting material | `Sprite-Lit-Default` (URP 2D) | Normal maps are optional; skip them for the slice |

## 2. Palette

One master palette of **32 colours** (stored as an Aseprite `.gpl` file in `Assets/Art/Palette/`). Every stock asset is re-coloured to it, which is what makes mixed sources look like one game.

| Group | Hex (dark → light) | Used for |
|-------|--------------------|----------|
| Void | `#07080c` `#0e1118` `#171b25` `#232937` | Darkness, outlines, shadows: about 60% of any screen |
| Steel | `#343c4d` `#4a5468` `#6b768c` `#98a2b5` | Walls, machinery, metal props |
| Clinic teal | `#12302f` `#1d4a47` `#2f6e68` `#5fa39a` | Research Labs, monitors, scrubs |
| Sodium | `#3a2410` `#6b4419` `#a86b22` `#e0a547` | St. Brigid's, warm lamps, safe rooms |
| Rust / blood | `#2a0d0f` `#4f1418` `#7f1d22` `#b8323a` | Containment, danger, damage. **Red only ever signals danger.** |
| Skin | `#3b2620` `#6e4a3a` `#a8786a` `#d9b39f` | Characters |
| Lantern | `#1a2a4a` `#3d6fd1` `#8fd3ff` `#e8fbff` | Hollow glow, Emilia, psychic effects: the only saturated cool tone |
| Paper | `#5a5650` `#a39d92` `#e3ddd0` `#ffffff` | Notes, drawings, UI text |

Rules:
- **Fight the cosy look.** No warm, saturated greens or yellows outside safe rooms.
- **Safe rooms are the only warm, sodium-lit spaces.** Players should *feel* relief in them.
- The lantern blue belongs to Emilia and the Hollows. If something glows blue, it's psychic.

## 3. Character sprite budget (vertical slice)

Bodies face 4 directions (down, up, side, and side mirrored), so **3 are drawn**. The weapon arm is a separate sprite with **8 pre-drawn aim angles**. Rotating pixel art at runtime breaks the pixel grid, so it isn't used.

| Character | Animations (frames) | Total frames ≈ |
|-----------|---------------------|---------------|
| **Max** | idle 4 · walk 6 · run 6 · aim-walk 6 · hurt 2 · death 6 · interact 3 · knife 4 · hide 3 · examine 2 | ~130 (×3 directions) + 8 aim arms × 3 weapons |
| **Emilia (human)** | idle 4 · walk 6 · cutscene poses 6 | ~40 |
| **Emilia (Hollow)** | float idle 6 · drift 6 · psychic cast 8 · scream 6 · halo debris (separate loop) 12 | ~70 |
| **Hollow Drone** | idle 4 · shamble 8 · lunge 5 · grab 4 · stagger 3 · death 6 | ~90 |
| **Hollow Child** | idle 4 · scurry 6 · pounce 5 · cower (spare) 4 · death 5 | ~70 |
| **Guard** | idle 4 · walk 6 · aim 2 · shoot 3 · alert 2 · death 6 | ~70 |
| **Jaz / Nate / Huckley / Dr. Mán** | Phase 3: idle 4 · walk 6 + cutscene poses | ~40 each |

**Dialogue portraits:** 96×96 px bust, 3–4 expressions per character. These carry the emotion that 32-px sprites can't.

**Production shortcut:** Max's 3 directions can be roughed in from a stock 32-px base character, then repainted. Re-colour the guard from Max's base so their proportions match.

## 4. Environment

| Sector | Tileset base | Palette weight | Light sources |
|--------|-------------|----------------|---------------|
| St. Brigid's Clinic | Stock "abandoned hospital" set | Sodium + Steel | Orange street lamps through windows, flashlight |
| Containment Wing | Sci-fi lab set, re-coloured | Rust + Void | Rotating red emergency beacons, flashlight |
| Research Labs | Same lab set | Clinic teal + Steel | Flickering fluorescents (animated light intensity) |
| Maintenance Tunnels | Sewer/industrial set | Void (90%) | **Flashlight only** |
| Security Hub | Lab set + monitors | Steel + Lantern | Wall of CRT monitors (animated sprites + lights) |

- Use **Rule Tiles** for walls and floors (Unity's `tilemap-ruletile-createfromsegment` skill), with a **Tile Palette** per sector.
- Every wall tile gets a **2D shadow caster**, so the flashlight casts real shadows. This is the single most important horror feature in the engine.
- Decals (blood, papers, children's drawings) go on their own tilemap layer, so one set of floor tiles yields many variations.

## 5. Storybook panels & key art
- 480×270 (the full screen) or larger, painted at 2× pixel density, with a slow parallax pan.
- **This is where AI-assisted concepts help:** generate the composition and mood, then redraw it in palette. Never ship raw AI output; record every use in `ASSET_LOG.md` for Steam's AI disclosure.
- Emilia's in-world drawings are deliberately "child-drawn": crayon textures, paper palette, the only intentionally messy art in the game.

## 6. UI
- *Signalis*-inspired clinical UI: a monospace pixel font (for example *m5x7* or *Pixel Operator*, both free), thin steel frames, a paper palette for documents.
- Inventory: a grid of 6–10 slots shown as a medical tray. Items drawn at 24×24.
- Screen effects (shaders on the upscale render texture): vignette, palette shift toward a sickly tone at low sanity, scanline jitter on hallucinations, red edge pulse on damage. Flashing effects can be switched off in settings.

## 7. Tools & file layout
- **Aseprite** (~$20) for sprites and tiles. Export sprite sheets and JSON, or import `.aseprite` files directly with Unity's `2D Aseprite Importer` package.
- **Blender** (optional): render 3D blockouts to 32-px frames for awkward rotations (machinery, the debris halo), then paint over them.
- Folders: `Assets/Art/{Characters,Tiles,Props,FX,UI,Portraits,Storybook,Palette}/`
- Naming: `chr_max_walk_down.aseprite`, `tile_containment_wall.png`, `prop_locker_01.png`, `fx_lantern_glow.png`.
