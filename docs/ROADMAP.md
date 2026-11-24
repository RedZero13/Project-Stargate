# HOLLOW KIN — Development Roadmap (Unreal Engine 5 edition)

> Engine: **Unreal Engine 5**, realistic 3D, over-the-shoulder. Claude drives the live editor through Epic's **Model Context Protocol (MCP) plugin**.
> Status: **pre-production.** Design docs are written; no Unreal project exists yet.
> Companion docs: [`GDD.md`](GDD.md) · [`ART_BIBLE.md`](ART_BIBLE.md) · [`levels/CONTAINMENT_WING.md`](levels/CONTAINMENT_WING.md) · [`narrative/PROLOGUE.md`](narrative/PROLOGUE.md)

## Decisions locked

| Topic | Decision |
|-------|----------|
| Team / budget | Solo, spending as little as possible |
| Scope | 3 launch endings, 6-character core cast, sanity as a resource, Ironman opt-in, Chapter 1 first |
| Title | ***HOLLOW KIN***: in-world Project LANTERN; enemies are Hollows; villain Dr. Sebastian Mán |
| **Engine & look** | **Unreal Engine 5, realistic 3D, over-the-shoulder** (replaces Unity and the pixel-art plan) |
| Assets | Fab (free + some paid) + Megascans + MetaHuman + self-made Blender + AI-assisted concepts |
| Voice | ElevenLabs, all story dialogue; lip-sync via MetaHuman Animator |
| Cutscenes | In-engine (Sequencer) + 2D storybook panels for flashbacks |
| Platforms | Windows (Steam, Steam Deck) + macOS |
| Hardware | M4 Max Mac Studio, 64 GB (development). **A Windows machine is needed for Windows builds** (§2.3) |

---

## 1. Is Unreal better than Unity for this game?

**For a realistic horror game, yes.** Most of what made the realistic version too big for one developer in Unity comes free and built in with Unreal.

| Need | Unreal Engine 5 | Unity 6 |
|------|-----------------|---------|
| Realistic lighting in dark interiors | **Lumen** dynamic GI built in; the flashlight lights the room realistically with no baking | URP needs baked lighting plus tricks; HDRP is closer but heavier and has less Mac support |
| Realistic humans | **MetaHuman**: free, film-quality faces and bodies, built in | Buy or commission characters (the biggest cost in the old plan) |
| Environment art | **Fab** (free assets every two weeks, plus a large catalogue) + **Megascans**, Nanite for dense detail | Asset Store kits, usually less realistic |
| Third-person movement | **Game Animation Sample** (free, motion matching) | Buy an animation pack and controller |
| Facial animation / lip-sync | **MetaHuman Animator** generates it from audio, which pairs perfectly with ElevenLabs | Third-party tools |
| Cutscenes | Sequencer (film-grade) | Timeline (good) |
| Enemy AI | Behavior Trees / StateTree + AI Perception (sight + hearing) built in | NavMesh + write your own perception |
| AI editor control | Epic's **MCP plugin**: hundreds of tools (actors, Blueprints, materials, Niagara, Sequencer…) | Unity MCP: smaller toolset |
| Cost | Free; **5% royalty only on gross revenue above $1M** per product | Free under $200k revenue |

### The trade-offs (the honest part)
1. **Building for Windows from a Mac isn't possible in Unreal.** You can *develop* on the Mac Studio, but Windows builds need a Windows PC. Windows is about 95% of Steam, so this is required (see §2.3).
2. **Mac is a second-class dev platform for Unreal.** Most of it works well on Apple Silicon, but Live Coding (hot-reloading C++) is Windows-only, some Fab plugins ship without Mac binaries, and C++ needs Xcode. **Mitigation:** build the game mostly in **Blueprints** (which Claude can create and edit through the MCP), with a small C++ module only where needed.
3. **Steeper learning curve and heavier projects.** Expect 100–300 GB of disk space for the engine, project and caches, and longer shader compiles.
4. **A realistic game is bigger than the pixel version.** Unreal makes realism *feasible* solo, not quick: about **2 years to Chapter 1** (§3), against about 14 months for pixel art.

### Feasibility
**Solo, 25–30 hrs/week:**
- **Playable prototype:** about 2–3 months.
- **Vertical slice / Steam demo:** about 8 months.
- **Chapter 1 on Steam:** about 20–24 months.

### Lean budget
| Item | Cost |
|------|------|
| Unreal Engine, MetaHuman, Game Animation Sample, Megascans/Fab freebies | $0 |
| Paid Fab packs (modular lab/hospital kit, weapon animations, horror SFX), bought on sale | $150–400 |
| **Windows build machine** (a used PC with an RTX 3060-class GPU) **or** a cloud Windows PC by the hour | $500–800 once, **or** ~$10–30 per month while building |
| ElevenLabs paid plan (voice-production months only) | ~$100–200 |
| Git LFS storage (Unreal projects are large) | ~$5–10 per month |
| Steam Direct fee | $100 |
| **Total** | **≈ $900–1,600** with a PC, or ≈ $500–900 with cloud Windows |

Optional: an iPhone (any recent model) for MetaHuman facial capture of hero cutscenes.

---

## 2. Tooling setup

### 2.1 On your Mac Studio (one-time)
1. **Xcode** from the App Store (needed by Unreal on Mac, even for Blueprint projects that later add C++).
2. **Epic Games Launcher** → Unreal Engine tab → install the **latest Unreal Engine 5.x** (pick one version and stay on it). Include the **Windows** target platform in the install options for when you build on the PC.
3. Create the project: **Games → Third Person** template, **Blueprint**, Desktop, **Maximum quality**, Starter Content off. Name it `HollowKin` and save it into this repo.
4. **Enable the Unreal MCP** (Epic's experimental plugin), so Claude can drive the editor:
   - **Edit → Plugins:** enable **Model Context Protocol** and **All Toolsets**, then restart the editor. (Or add both to the `.uproject` `Plugins` list.)
   - Auto-start the server: add this to `HollowKin/Saved/Config/MacEditor/EditorPerProjectUserSettings.ini`:
     ```ini
     [/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
     bAutoStartServer=True
     ```
   - In the editor console (the `` ` `` key), run `ModelContextProtocol.GenerateClientConfig ClaudeCode`. This writes `.mcp.json` next to `HollowKin.uproject`, pointing Claude Code at `http://127.0.0.1:8000/mcp`.
5. **Run Claude on the Mac**, inside the project folder (Claude Desktop, or `claude` in a terminal), so it can reach the local MCP server. Alternatively, keep using a cloud session and connect your Mac folder through **Remote Control** (Claude Desktop → Settings → Claude Code → Remote Control).
6. Free downloads from Fab / the Launcher: **Game Animation Sample**, **MetaHuman** plugin, and any free horror/lab packs. Claim Fab's free assets every two weeks.

### 2.2 Source control
- Git + **Git LFS**, with a `.gitattributes` tracking `*.uasset *.umap *.fbx *.wav *.png *.exr *.psd`. Turn on LFS **file locking** for `.uasset`/`.umap` (binary files can't be merged).
- `.gitignore`: `Binaries/ DerivedDataCache/ Intermediate/ Saved/ .vs/ *.xcworkspace`.
- If the repo outgrows GitHub LFS, alternatives are Anchorpoint or Diversion (both Unreal-friendly with free tiers) or Perforce (free for small teams).

### 2.3 Windows builds
Unreal can't cross-compile a Windows game from macOS. Options, cheapest first:
1. **Cloud Windows PC by the hour** (a GPU cloud desktop, roughly $0.50–1.50/hr): pull the repo, package, upload to Steam. Fine for monthly builds.
2. **A used Windows PC** (RTX 3060 or better), which also becomes your **min-spec performance test machine** and Steam Deck-like baseline. **Recommended by the vertical-slice milestone.**
3. Later: a CI build machine (GitHub Actions self-hosted runner on that PC) → SteamPipe upload.

### 2.4 What Claude can do through the Unreal MCP
Spawn and arrange actors, greybox levels, create and edit Blueprints and widgets, materials and material instances, Niagara effects, Sequencer cinematics, Behavior Trees/StateTree, data assets, and run automation tests. Workflow rules: **save before every batch change**, keep Play-In-Editor stopped during asset edits, and commit after each working step.

### 2.5 Asset pipeline
1. **Concept:** AI-assisted mood boards → lock the direction in `ART_BIBLE.md`.
2. **Characters:** MetaHuman Creator → clothing (Fab / Blender) → Hollow variants sculpted in Blender → import.
3. **Environment:** Fab modular kit + Megascans → material instances per sector → hero props from Blender (FBX, cm scale, +Z up).
4. **Animation:** Game Animation Sample retargeted to MetaHumans + Fab packs + MetaHuman Animator for faces.
5. **Log every asset** in `docs/ASSET_LOG.md` (source, license, AI involvement); Steam requires AI-content disclosure.

### 2.6 Voice (ElevenLabs)
- A **paid plan** is required for commercial use. Use only designed voices or library voices licensed for commercial use. Never clone a real person without written consent.
- Script sheet: `character, line_id, line, direction` → batch-generate → `VO_<char>_<scene>_<id>.wav` (48 kHz) → MetaHuman Animator audio-to-face → Sequencer.
- Subtitles from the same sheet (Unreal String Tables), so localization comes cheap later.

---

## 3. Phased roadmap

### Phase 1 — Planning ✅ mostly done
- ✅ Concept, pillars, scope cuts, title, canonical story (`GDD.md`)
- ✅ Art direction for realistic UE5 (`ART_BIBLE.md`)
- ✅ Vertical-slice level design (`levels/CONTAINMENT_WING.md`)
- ✅ Prologue and letter (`narrative/PROLOGUE.md`)
- ⬜ Mood board in `docs/reference/` (**you**: AI concepts + references)
- ⬜ First MetaHuman pass of Max and Emilia (**you**, ~1 evening; Claude can't operate MetaHuman Creator's sculpting UI)

### Phase 2 — Prototype: "is it tense and fun?" (2–3 months)
Placeholder art only (Third Person template mannequins, grey boxes, a free Fab kit).
1. **Weeks 1–2: setup.** Project, plugins, MCP, Git LFS, folder structure (`ART_BIBLE.md` §8), Enhanced Input actions (keyboard/mouse + gamepad).
2. **Weeks 2–4: Max.** Game Animation Sample locomotion, over-the-shoulder camera with a shoulder swap, aim mode, pistol (hitscan), knife, health and hit reactions, flashlight (spot light + Lumen).
3. **Weeks 4–6: enemies.** Hollow Drone (Behavior Tree: wander → chase → lunge → stagger), Guard (patrol → investigate noise → alert → shoot) with **AI Perception** sight + hearing; noise events from footsteps, gunshots and thrown bottles.
4. **Weeks 6–8: systems.** Inventory grid (data assets), examine-item view, doors/keys/pickups, safe room with save/load (`SaveGame`), item box, sanity with one hallucination effect (post-process + a fake enemy).
5. **Weeks 8–10: greybox the Containment Wing** from the level doc; playtest with 5+ people.

**Gate 1:** testers report tension and want to keep going. If not, iterate before any art spend.

### Phase 3 — Production
**3a. Vertical slice / Steam demo (months 3–8)**
- St. Brigid's + the Containment Wing at final quality: modular kit dressed, lighting pass, post-processing and fog, Emilia's room.
- MetaHumans: Max, Emilia (human + Hollow), Huckley (diary voice and a photo), a guard. Hollows: Drone and Child.
- All slice systems from the level doc, plus the Hollow Child spare/kill choice tracking Bond/Taint.
- Audio: ambience, footsteps per surface, weapons, the heartbeat layer, adaptive music (MetaSounds), Emilia's lullaby; ElevenLabs VO for the prologue, Jaz and Emilia.
- Prologue cutscene (Sequencer + storybook panels); main, pause and settings menus (CommonUI).
- **Output:** Steam "Coming Soon" page, a 60–90 s trailer, and the **demo build (Windows + Mac)**. Wishlists start here.

**3b. Pre-alpha (months 9–13):** greybox the Research Labs, Maintenance Tunnels and Security Hub; the Huckley boss; Nate; the Screamer; all 4 drugs; the map.

**3c. Alpha (months 14–18):** feature complete. The Dr. Mán boss, the 3 endings, all puzzles, difficulty modes + dynamic difficulty, every cutscene in rough form, accessibility (subtitles, rebinding, aim assist, flashing toggle).

**3d. Beta (months 19–21):** content complete. Final art everywhere, all VO and facial animation, balancing, performance on Steam Deck and the min-spec PC, localization strings extracted.

### Phase 4 — Testing & QA (focused months 18–22)
- **Automated:** Unreal Automation tests (inventory, save/load, Bond/Taint maths, the lock-and-key graph has no dead ends), run headless on the Windows build machine.
- **Manual:** a softlock checklist per key item; save in every room, then reload; GPU-crash checks across Lumen scalability presets.
- **Performance:** Unreal Insights per sector, a shader-compile stutter check (PSO cache), memory on Steam Deck.
- **Playtests:** Steam Playtest, with a short survey and recorded sessions.

### Phase 5 — Pre-launch (alongside 3c–4)
- Devlog every 2 weeks: lighting before/after, the Hollow Child encounter and MetaHuman close-ups do well on X, Reddit r/survivalhorror, r/unrealengine, r/IndieDev and TikTok.
- Discord; **Steam Next Fest** with the demo; keys for horror streamers.
- Polish: PSO precaching, load times, age rating (IARC), store assets, launch trailer.

### Phase 6 — Launch (month ~22–24)
- Steam (Windows + macOS). Watch crash reports (Unreal's crash reporter / Sentry) and reviews; keep a hotfix branch ready.

### Phase 7 — Post-launch
- Patches, Steam Deck Verified.
- **Content:** the 4 remaining endings, New Game+ / Ironman, the Vicky/Jasper/Jade backstory chapter, then **Chapter 2**.

---

## 4. Vertical-slice backlog

| # | Task | Owner | Unreal tech |
|---|------|-------|-------------|
| 1 | Install UE5 + Xcode, create the project, enable the MCP plugins | **You** (≈1 hour) | Epic Launcher |
| 2 | Git LFS, `.gitattributes`, `.gitignore`, folder structure | Claude | — |
| 3 | Enhanced Input actions + over-the-shoulder camera + aim mode | Claude (via MCP) | Enhanced Input, Spring Arm |
| 4 | Game Animation Sample locomotion on Max | Claude + you (download) | Motion Matching |
| 5 | Flashlight + Lumen setup + per-area post-process | Claude | Spot light, PPV |
| 6 | Pistol/knife, health, hit reactions, weak points | Claude | Blueprints, line traces |
| 7 | Hollow Drone + Guard AI | Claude | Behavior Tree / StateTree, AI Perception |
| 8 | Noise system (footsteps, gunshots, bottle lure) | Claude | `ReportNoiseEvent` |
| 9 | Inventory grid, examine view, items as data assets | Claude | CommonUI, UMG |
| 10 | Doors, keys, pickups, fuse/breaker puzzle | Claude | Blueprint interfaces |
| 11 | Safe room: save/load, item box | Claude | `SaveGame` |
| 12 | Sanity system + hallucination effects | Claude | Post-process materials, Niagara |
| 13 | Bond/Taint + the Hollow Child choice | Claude | Game Instance subsystem |
| 14 | Greybox S1–C9 from the level doc | Claude | Modeling Mode, blockout |
| 15 | Mood board + AI concepts for Max, Emilia, Hollows | **You** | — |
| 16 | MetaHumans: Max, Emilia (both forms), Huckley, guard | **You** (Creator) + Claude (setup in engine) | MetaHuman |
| 17 | Buy and import the modular kit; dress the slice | You (buy) + Claude (dress) | Fab, Nanite |
| 18 | Audio: ambience, SFX, music, lullaby, heartbeat | You (source) + Claude (wire) | MetaSounds, Sound Classes |
| 19 | ElevenLabs VO + lip-sync | You (generate) + Claude (import, sequences) | MetaHuman Animator |
| 20 | Prologue cinematic, storybook panels, menus | Claude (Sequencer, UI) + you (panel art) | Sequencer, CommonUI |
| 21 | Windows build machine + demo builds + Steam page | **You** (machine) + Claude (packaging config) | Project Launcher / BuildGraph |

---

## 5. Next steps

**You, now:**
1. **Review and merge the PR** (or comment on anything you want changed).
2. Do §2.1 on the Mac: Xcode, Unreal Engine 5, the `HollowKin` Third Person Blueprint project in this repo, and the MCP plugins with the server auto-starting.
3. Then either run Claude on the Mac in the project folder, or connect the folder to a cloud session through Remote Control.
4. Decide on Windows builds: a cloud PC now, or a used PC before the demo (§2.3).

**Claude, in the first editor session (backlog 2–5):**
1. Set up Git LFS, ignores and the folder structure; commit the empty project.
2. Over-the-shoulder camera, aim mode and input on the template character.
3. A test corridor greybox with the flashlight and Lumen darkness tuned, so we can judge the horror feel on day one.
4. Commit, then work down the backlog toward Gate 1.
