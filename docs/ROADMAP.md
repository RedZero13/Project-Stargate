# HOLLOW KIN — Development Roadmap (pixel art edition)

> Engine: **Unity 6 LTS, URP 2D Renderer**, driven through the **Unity CLI + Unity MCP** on your Mac.
> Status: **pre-production.** Design docs are written; no Unity project exists yet.
> Companion docs: [`GDD.md`](GDD.md) · [`ART_BIBLE.md`](ART_BIBLE.md) · [`levels/CONTAINMENT_WING.md`](levels/CONTAINMENT_WING.md) · [`narrative/PROLOGUE.md`](narrative/PROLOGUE.md)

## Decisions locked

| Topic | Decision |
|-------|----------|
| Team / budget | Solo, spending as little as possible |
| Scope | 3 launch endings, 6-character core cast, sanity as a resource, Ironman opt-in, Chapter 1 first |
| Title | ***HOLLOW KIN***: in-world Project LANTERN; enemies are Hollows; villain Dr. Sebastian Mán |
| **Visual format** | **2D top-down pixel art**, ¾ view (Stardew-style perspective, *Signalis* / *Darkwood* tone) |
| Assets | Stock pixel packs re-coloured to the palette + Aseprite + Blender (optional) + AI-assisted concepts |
| Voice | ElevenLabs, for key lines only (cutscenes, radio, Emilia, bosses) |
| Cutscenes | In-engine sprite scenes + portraits + storybook panels |
| Platforms | macOS + Windows (Steam) at launch; Steam Deck and iPad soon after |
| Hardware | M4 Max Mac Studio, 64 GB. Unity MCP connected locally |

---

## 1. Assessment (pixel edition)

### Why the pixel switch is right
- **It halves the art load.** A ~32-px character is about 400 hand-drawn frames, against a rigged, textured, animated 3D model. Environments are tilesets instead of modular 3D kits.
- **It's proven for this genre.** *Signalis* (pixel survival horror, RE-style), *Darkwood* (top-down, line-of-sight horror) and *Faith* show that dread comes from lighting, sound and framing, not polygons.
- **Every system in the GDD still works.** Lock-and-key, safe rooms, stealth, sanity, drugs, the endings. Stealth actually gets *better*: top-down line of sight is easy to read.
- **More platforms for free.** 2D runs on Steam Deck and iPad with little extra work.

### New risks to manage
| Risk | Mitigation |
|------|------------|
| Pixel art reads as "cosy" (the Stardew association) | The palette rules in `ART_BIBLE.md` §2: 60% darkness, red only for danger, warmth only in safe rooms |
| Mixed stock packs look inconsistent | Lock the 16-px grid and 32-colour palette first; re-colour every pack to it |
| Small sprites can't carry emotion | 96-px dialogue portraits + storybook panels for the big moments |
| AI pixel art is messy | Use AI for concepts and mood only; draw the final pixels |
| The pixel-art market is crowded | The hook (*your sister is the monster*) and a *Signalis*-quality atmosphere are the differentiators. Show them in the first 10 seconds of the trailer |

### Feasibility
**Solo, about 25–30 hrs/week:** a **vertical slice/demo in 4–5 months**, and **Chapter 1 on Steam in about 12–15 months** from when the Unity project is created.

### Lean budget
| Item | Cost |
|------|------|
| Unity Personal | $0 |
| Aseprite | ~$20 (or compile the source yourself for free) |
| Stock pixel tilesets, props, FX (itch.io / Asset Store, bought on sale) | $50–150 |
| Pixel font | $0 (free licensed fonts) |
| Music + SFX (CC0 + one paid horror pack) | $0–60 |
| ElevenLabs (paid plan, only during voice months) | ~$50–100 |
| Steam Direct fee | $100 |
| **Total** | **≈ $220–430** |

Later and optional: Apple Developer ($99/yr) for the iPad port, and a trademark filing.

---

## 2. Tooling setup (on your Mac)

The Unity Editor and the MCP bridge run **on your Mac**, so Claude has to run there too: the Claude Desktop app, or `claude` in a terminal in this repo. **A cloud session like this one can't reach your local MCP.**

```bash
# 1. Unity CLI (beta)
curl -fsSL https://public-cdn.cloud.unity3d.com/hub/prod/cli/install.sh | UNITY_CLI_CHANNEL=beta bash
unity --version
unity auth login && unity license activate

# 2. Unity 6 LTS (Apple Silicon) + Windows build support
unity install lts --architecture arm64 --module mac-il2cpp --module windows-mono --yes --accept-eula
#    (check module ids with: unity install-modules --help)

# 3. Create the project from the URP 2D template, inside this repo
unity templates list --editor lts --format json        # find the 2D URP template id
unity projects create "HollowKin" --path . --editor-version lts --template <2d-urp-template-id>

# 4. Let the CLI/MCP drive the live Editor
cd HollowKin && unity pipeline install
unity mcp configure claude-code --project-path "$(pwd)"
unity status                                            # expect state "ready"
```

**Packages:** 2D Sprite, 2D Tilemap + Tilemap Extras (Rule Tiles), 2D Aseprite Importer, 2D Pixel Perfect (built into URP), Input System, Cinemachine (with its Pixel Perfect extension), Timeline, TextMeshPro, Addressables (later), Localization (later).

**Repo hygiene:** a Unity `.gitignore`; **Git LFS** for `*.png *.aseprite *.psd *.wav *.ogg *.mp3`.

**Build notes:** Mac builds use IL2CPP (universal arm64 + x86_64). Windows builds from a Mac use Mono, which is fine for the demo; add a Windows CI runner for IL2CPP later.

### 2.1 Asset pipeline
1. **Concept:** AI-assisted mood boards → pick a direction → lock it in `ART_BIBLE.md`.
2. **Stock:** buy packs that match the 16-px grid → re-colour to the 32-colour palette → slice in Unity (Unity's `sprite-editor` skill).
3. **Draw:** characters, portraits and hero props in **Aseprite** → import `.aseprite` directly.
4. **Blender (optional):** render tricky rotating objects to frames → paint over them.
5. **Log every asset** in `docs/ASSET_LOG.md` (source, license, AI involvement). Steam requires AI-content disclosure.

### 2.2 Voice (ElevenLabs)
- A **paid plan** is required for commercial use. Only use designed voices, or library voices licensed for commercial use. No cloning of real people without written consent.
- Script sheet: `character, line_id, line, direction` → batch-generate → `VO_<char>_<scene>_<id>.wav`.
- Import settings: mono, Vorbis; *Compressed In Memory* for lines, *Streaming* for long cutscenes.

---

## 3. Phased roadmap

Durations assume one developer at about 25–30 hrs/week.

### Phase 1 — Planning ✅ mostly done
- ✅ Concept, pillars, scope cuts, title, canonical story (`GDD.md`)
- ✅ Pixel art spec and palette (`ART_BIBLE.md`)
- ✅ Vertical-slice level design (`levels/CONTAINMENT_WING.md`)
- ✅ Prologue and letter (`narrative/PROLOGUE.md`)
- ⬜ Mood board in `docs/reference/` (**you**: AI concepts + references)
- ⬜ Market check: wishlist and review counts for *Signalis*, *Faith*, *Darkwood*, *Mouthwashing*, *World of Horror* (Claude can draft this)

### Phase 2 — Pre-production: the "fun" prototype (6–8 weeks)
Built with **placeholder art** (coloured squares and a free test tileset). The only question it answers is *is this tense and fun?*
1. **Week 1: project setup** (§2): folders, import presets, Pixel Perfect Camera, sorting layers, the Input System action map.
2. **Weeks 2–3: core feel.** Top-down movement, the flashlight cone with **2D shadow casters**, aim and shoot, the knife, health.
3. **Weeks 3–4: enemies.** Hollow Drone (chase, lunge, stagger) and Guard (patrol, hear, see, alert). Pathfinding on a tile grid (A* on the Tilemap; NavMesh isn't needed in 2D).
4. **Weeks 5–6: systems.** Inventory grid, examine, pickups, doors and keys, one safe room with save/load, and sanity with one hallucination effect.
5. **Weeks 7–8: greybox the Containment Wing** from the level doc with placeholder tiles, then **playtest with 5+ people**.

**Gate 1:** testers report tension and want to keep playing. If not, iterate here before drawing anything final.

### Phase 3 — Production

**3a. Vertical slice / demo (months 3–5)**
- Final art for St. Brigid's and the Containment Wing: tilesets, Max, Emilia (both forms), Drone, Child, Guard, portraits, 2 storybook panels.
- Lighting pass (emergency beacons, fluorescent flicker), post effects (vignette, palette shift, scanline jitter).
- Audio: ambience, footsteps, weapons, the heartbeat layer, adaptive music, Emilia's lullaby; ElevenLabs lines for the prologue, Jaz and Emilia.
- Menus: main, pause, settings (rebinding, subtitles, flashing-effects toggle).
- **Output:** a Steam "Coming Soon" page, a 60-second trailer, and the **demo build**. Wishlists start counting from here.

**3b. Pre-alpha (months 6–8):** greybox the Research Labs, Maintenance Tunnels and Security Hub; the Huckley boss prototype; Nate; the Screamer enemy; all 4 drugs; the map.

**3c. Alpha (months 9–11):** feature complete. The Dr. Mán boss, Bond/Taint and the 3 endings, all puzzles, difficulty modes + dynamic difficulty, every cutscene in rough form.

**3d. Beta (months 12–13):** content complete. Final art for every sector, all VO, balancing, performance on Steam Deck, localization strings extracted.

### Phase 4 — Testing & QA (overlapping, focused months 11–14)
- **Automated:** EditMode/PlayMode tests (inventory, save/load, Bond/Taint maths, the lock-and-key graph has no dead ends), run with `unity test` in GitHub Actions.
- **Manual:** a softlock checklist for every key item; a save in every room, then reload.
- **Balance:** a spreadsheet of the ammo/health economy per sector (see the level doc §5), deaths per room.
- **Playtests:** Steam Playtest, with a short survey and recorded sessions.

### Phase 5 — Pre-launch (alongside 3c–4)
- Devlog every 2 weeks (GIFs of the lighting and the Hollow Child encounter work well on X, Reddit r/survivalhorror, r/PixelArt, r/IndieDev, TikTok).
- Discord; **Steam Next Fest** with the demo; streamer keys (horror streamers love short demos).
- Final polish, age rating (IARC), store assets, launch trailer.

### Phase 6 — Launch (month ~14–15)
- Steam for Windows and macOS; itch.io optionally.
- Watch crash reports and reviews; a hotfix branch ready (`unity build` → SteamPipe).

### Phase 7 — Post-launch
- Patches, Steam Deck Verified, the iPad port.
- **Content:** the 4 remaining endings, New Game+ / Ironman, the Vicky/Jasper/Jade backstory chapter, then **Chapter 2**.

---

## 4. Vertical-slice backlog

| # | Task | Owner | Unity tech / skill |
|---|------|-------|-------------------|
| 1 | Create the project, packages, Git LFS, folder structure, import presets | Claude (on your Mac) | Unity CLI, `unity-package-management` |
| 2 | Pixel-perfect setup: PPU 16, 480×270, sorting layers | Claude | `2d-pixel-perfect` |
| 3 | Input actions (keyboard + mouse, gamepad) | Claude | Input System |
| 4 | Top-down controller + camera that leans toward the aim | Claude | Cinemachine + Pixel Perfect |
| 5 | Flashlight cone + shadow casters + player vision darkness | Claude | URP 2D Lights |
| 6 | Aim/shoot/knife + health/damage | Claude | Physics2D raycasts |
| 7 | Hollow Drone AI + Guard AI (sight cone, noise events) | Claude | Grid A*, ScriptableObjects |
| 8 | Inventory grid, examine, items as ScriptableObjects | Claude | UI Toolkit |
| 9 | Doors, keys, pickups, the fuse puzzle | Claude | — |
| 10 | Safe room: save/load (JSON), item box | Claude | — |
| 11 | Sanity system + post effects | Claude | URP 2D, shaders |
| 12 | Bond/Taint tracking + the Hollow Child spare/kill choice | Claude | — |
| 13 | Placeholder tiles, then greybox S1–C9 from the level doc | Claude | Tilemap, Rule Tiles (`tilemap-*` skills) |
| 14 | Mood board + AI concept pass for Max, Emilia, Hollows | **You** | — |
| 15 | Palette file + stock pack purchase and re-colour | **You** (Claude helps slice) | `sprite-editor`, `manage-sprite-atlas` |
| 16 | Max, Emilia, Drone, Child, Guard sprites + portraits | **You** | Aseprite Importer |
| 17 | Ambience, SFX, music, lullaby | **You** (stock) + Claude wiring | Audio Mixer (`audio-setup-mixers`) |
| 18 | ElevenLabs VO: prologue, Jaz, Emilia | **You** (generate) + Claude (script sheet, import) | `optimize-audio` |
| 19 | Prologue cutscene + storybook panels + menus | Claude (scenes) + **you** (panel art) | Timeline |
| 20 | Demo build (Mac + Win), Steam page, trailer capture | Both | `unity build` |

---

## 5. Next steps

**You, now:**
1. **Review and merge the PR** (or comment on anything you want changed).
2. **Start Claude on your Mac**: open the repo in the Claude Desktop app, or run `claude` in a terminal there. Check `unity status` reports "ready".
3. Put any reference images or AI concepts in `docs/reference/`.

**Claude, in the first Mac session (backlog 1–5, about one sitting):**
1. Create the `HollowKin` Unity project in the repo with the 2D URP template, packages, Git LFS and `.gitignore`.
2. Apply the pixel-perfect spec from `ART_BIBLE.md` §1.
3. Build a test room with a free placeholder tileset: Max as a coloured capsule, a working **flashlight with real shadows**, and top-down movement.
4. Commit, then continue down the backlog toward Gate 1.
