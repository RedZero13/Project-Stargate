# HOLLOW KIN (formerly Project Stargate) — Assessment & Development Roadmap

> Source: *Project Stargate – The Following Saga* (GDD draft).
> Engine target: **Unity 6 LTS**, driven via the **Unity CLI** + **Unity MCP** so Claude can work inside the live Editor.
> Status: **planning only — nothing has been built yet.** The repo has just a README.
> Companion docs: [`GDD.md`](GDD.md) (design v2, which applies every fix in §1) · [`narrative/PROLOGUE.md`](narrative/PROLOGUE.md)

### Decisions locked (review round 1)
| Topic | Decision |
|-------|----------|
| Team / budget | Solo; spend as little as possible (the **Lean** column in §1) |
| Scope cuts in §1 | **Approved**: 3 launch endings, 6-character core cast, sanity as a resource, Ironman opt-in, PC first |
| Title | **Renamed** to *HOLLOW KIN* (working title). In-world project: **Project LANTERN**. Enemies: **Hollows** |
| Assets | Stock + self-made Blender + AI-assisted concepts |
| Voice | ElevenLabs |
| Cutscenes | In-engine animation where possible, with 2D storybook panels elsewhere |
| Hardware | M4 Max Mac Studio, 64 GB RAM. Unity MCP connected locally |

---

## 1. Concept assessment

### What's strong
- **Clear emotional core.** Brother rescues his sister, and she might be the monster. That's a good horror hook because the "boss" is the person you came to save.
- **Proven formula.** RE2-Remake-style semi-open facility, an over-the-shoulder camera, resource scarcity, and backtracking puzzles. Players already understand this loop, and you can study a lot of reference material.
- **One contained setting.** A single underground facility with four sectors keeps environment art bounded and reusable (modular kits).
- **Systemic hooks that set it apart.** A sanity meter, drugs with trade-offs, and choice-driven endings give it an identity beyond "RE clone".

### Risks and issues found in the GDD

| # | Issue | Why it matters | Recommendation |
|---|-------|----------------|----------------|
| 1 | **Scope is AAA-sized for a solo dev.** Semi-open world, stealth, melee + ranged, upgrades, sanity, dynamic difficulty, permadeath mode, 7 endings, ~13 named characters, voice acting, 2D cutscenes, 3 platforms. | The 19–28 month estimate assumes all of it works out. Realistically this is 4–6+ years solo. | Ship in **slices**: a vertical slice first (one wing, ~45 min), then an episodic or "Chapter 1" release. |
| 2 | **The "MVP" table is from a different game.** It lists *spikes and holes*, *dust particles*, *level select*, *itch page*, and marks everything "Finished". | It's a 2D platformer template. None of it applies, and none of it exists. | Replace it with the vertical-slice backlog in §4. |
| 3 | **Sanity as a 100→0 level timer** fights the RE2-style exploration and backtracking. | A timer punishes exactly what the genre rewards: careful exploring, reading notes, solving puzzles. | Make sanity a **resource** drained by darkness, remnant psychic attacks, gore and drugs, and restored by light, safe rooms and rare items. Low sanity brings hallucinations, aim sway and fake enemies. Keep a hard timer only for set-piece escapes. |
| 4 | **Souls-like "restart the entire run" difficulty.** | In a 6–10 hr narrative game this is brutal and costly to balance. | Make it an opt-in **Ironman** mode unlocked after the first clear. Balance only Normal at first; derive the others from multipliers. |
| 5 | **7 endings.** | Each ending needs a cutscene, choice tracking and QA of every path. | Launch with **3 endings** (Human / Remnant / Sacrifice). Add the rest in post-launch DLC or New Game+. |
| 6 | **Overlapping characters.** Huckley and Marlowe (both psych), Kline / Thompson / Jaz (all "insider who feeds Max info"), and Nate (an ally). | Every NPC costs models, rigs, VO and scripting. | Merge to about 6 core characters: Max, Emilia, Huckley (mentor who falls), Dr. Man (villain), one insider ally (merge Kline + Jaz + Thompson), Nate (combat ally). Vicky, Jasper and Jade appear as remnants or in notes and 2D art. |
| 7 | **Story contradictions.** Max is "adopted by an elderly couple" but also "went through every foster home until kicked out at 18". He has a dead-end receptionist job, but the prologue has him offered a security-guard job. | Players and testers notice. | Lock one canonical backstory in the narrative bible (Phase 2). |
| 8 | **The "Stargate" name.** It's a well-known MGM trademark (and a real CIA program). "Remnant" is also taken (*Remnant: From the Ashes*). | A trademark risk on Steam or the App Store, and it's hard to search for. | ✅ Fixed: *HOLLOW KIN* / Project LANTERN / Hollows. Still run a trademark search before the store page goes up. |
| 9 | **Emilia's design references Eveline (RE7)** directly. | It could feel derivative. | Use it as a mood reference only, and develop a unique silhouette: telekinetic "halo" debris, a nervous-system glow, a hospital gown with ID tags. |
| 10 | **iPadOS plus realistic 3D horror.** | Mobile GPU, touch controls and memory limits add a whole port project. | **PC first (Windows + macOS)**, with an iPad port after launch. Choose **URP** now so the port stays possible. |

### Feasibility verdict
**Feasible, but only if you cut scope.** As written, the GDD is a studio project. With the cuts above, plus heavy use of Asset Store / marketplace assets, Mixamo-style animation and stock audio, a solo dev or a team of 2–3 can reach a polished **vertical slice in about 6–9 months** and a **Chapter 1 commercial release in about 18–24 months**.

### Rough budget (indie, solo + contractors)

| Item | Low | Comfortable |
|------|-----|-------------|
| Unity Personal (free under $200k revenue) / Pro | $0 | ~$2,200/yr |
| Asset Store: modular sci-fi lab kit, characters, FX, audio packs, tools | $300 | $1,500 |
| Character art/rigging (Max, Emilia + Hollow form) — contractor or Character Creator–style tool | $0 (stock + tweak) | $3,000–8,000 |
| Music + SFX (composer or licensed) | $100 | $2,000–5,000 |
| Voice acting (6 characters, Chapter 1) | $0 (text only) | $2,000–6,000 |
| 2D cutscene / storybook art | $0 (self) | $1,500–4,000 |
| Steam Direct fee / Apple Developer | $100 / $99 per yr | same |
| Trademark search, capsule art, trailer | $0 | $1,000–3,000 |
| **Total** | **≈ $600** | **≈ $15k–30k** |

**Your lean plan (chosen):** Unity Personal $0 · Asset Store/Fab packs on sale ≈ $200–400 · ElevenLabs Creator plan ≈ $22/mo only during voice-production months (≈ $100–150 total) · stock music/SFX (free CC0 + one paid pack) ≈ $50 · Steam fee $100 · **total ≈ $450–700**. The Apple Developer fee ($99/yr) is only needed for the iPad port.

---

## 2. Tooling: Unity CLI + Unity MCP (how Claude works in your Editor)

This cloud session has **no Unity Editor** and no GPU or display, and the Editor needs your Unity license. So the Editor and the MCP bridge must run **on your M4 Max Mac Studio**, and Claude must be running **on that Mac** (Claude Desktop app, or `claude` in a terminal in this repo) to use the MCP tools. A cloud session can't reach your local MCP.

Mac notes: install the **Apple Silicon** Editor. Mac builds use IL2CPP (native arm64 + x86_64 universal). Windows builds from a Mac use the **Mono** backend; IL2CPP for Windows needs a Windows machine or CI runner, which is fine for the demo.

One-time setup on your machine:

```bash
# 1. Install the Unity CLI (beta)
# macOS / Linux:
curl -fsSL https://public-cdn.cloud.unity3d.com/hub/prod/cli/install.sh | UNITY_CLI_CHANNEL=beta bash
# Windows (PowerShell):
#   $env:UNITY_CLI_CHANNEL='beta'; irm https://public-cdn.cloud.unity3d.com/hub/prod/cli/install.ps1 | iex
unity --version

# 2. Sign in + license (Unity Personal is fine to start)
unity auth login
unity license activate

# 3. Install Unity 6 LTS with the platform modules we target
unity install lts --architecture arm64 --module mac-il2cpp --module windows-mono --yes --accept-eula
#   (run `unity install-modules --help` for exact module ids on your OS)

# 4. Create the project inside this repo (URP 3D template — list ids first)
unity templates list --editor lts --format json
unity projects create "HollowKin" --path . --editor-version lts --template <urp-3d-template-id>

# 5. Install the Pipeline package so the CLI/MCP can drive the live Editor
cd HollowKin && unity pipeline install

# 6. Register the Unity MCP server with Claude Code
unity mcp configure claude-code --project-path "$(pwd)"
unity status        # should report a connected Editor in state "ready"
```

Repository hygiene, done at project creation:
- A Unity `.gitignore` (excludes `Library/`, `Temp/`, `Obj/`, `Build/`, `Logs/`, `UserSettings/`).
- **Git LFS** for `*.fbx *.psd *.png *.tga *.exr *.wav *.mp3 *.ogg *.mp4`. Alternatively, Unity Version Control (UVCS) if the art gets heavy.
- Packages: Input System, Cinemachine, AI Navigation, TextMeshPro, Timeline, Addressables, Localization (later), URP post-processing.

### 2.1 Asset pipeline (stock + Blender + AI)
1. **Concept:** AI-assisted mood boards and character sheets → paint over or pick a direction → lock it in the art bible. Use them as *reference only*; don't ship raw AI images.
2. **Model:** stock base meshes and the modular kit → customise and kit-bash in **Blender** → export FBX (Apply Transforms, +Y up, scale 1.0) into `Assets/Art/<Category>/`.
3. **Rig and animate:** humanoid rig → Mixamo / marketplace clips → retarget in Unity.
4. **Texture:** reuse PBR texture sets, with a per-sector trim sheet to keep draw calls low.
5. **Ship:** Steam requires an **AI content disclosure** on the store page for AI-generated content. Keep a provenance log (`docs/ASSET_LOG.md`, started in Phase 2): source, license and AI involvement for every asset.

### 2.2 Voice (ElevenLabs)
- Use a **paid plan** for commercial rights. Free-tier output can't be used commercially. Use only voices you have rights to (designed voices, or library voices that allow commercial use). Never clone a real person without written consent.
- Keep a script spreadsheet (`character, line_id, line, direction`) and batch-generate. Name files `VO_<char>_<scene>_<id>.wav`.
- Import settings: mono, Vorbis, *Compressed In Memory* for lines and *Streaming* for long cutscenes.

Once that's connected, Claude can create scenes, place the modular kit, wire NavMesh, set up the URP volumes for the horror lighting, and write and run C# directly in your Editor.

---

## 3. Phased roadmap

Durations assume **one dev at about 25–30 hrs/week**. Halve them roughly for full-time work or a team of 2–3.

### Phase 1 — Planning: concept & research (3–4 weeks)
- **Lock the pillars:** *Dread over action · Every resource is a choice · The monster is family.*
- **Genre and comps:** RE2R, RE7, Silent Hill 2R, The Callisto Protocol, Signalis. Play their opening hours and log their pacing.
- **Audience and platform:** 20–45-year-old story-first players. PC first (Steam), Mac via Steam, iPad later.
- **Core loop:** *Explore → find key items/notes → solve puzzle → unlock a shortcut or new sector → fight or evade → manage ammo, health and sanity → safe room (save, store, craft) → repeat.*
- **Scope cut decisions** from §1 (endings, cast, sanity model, difficulty).
- **Feasibility:** the budget sheet, your skill map (what you'll make vs buy vs commission), and a market check (wishlist counts of comparable indie horror titles).
- **Proof of concept:** a one-page pitch, a mood board, a paper map of the Containment Wing, and a 60-second "greybox" walkthrough video (see Phase 2).

**Deliverables:** pitch one-pager, pillars, a revised feature list (Must/Should/Could/Won't), and the budget.

### Phase 2 — Pre-production (3–4 months)
1. **GDD v2.** Rewrite the GDD into living docs in `docs/`:
   - Narrative bible: canonical backstory, timeline, cast sheets, and the choice → ending matrix.
   - Systems specs: combat, inventory grid, sanity, drugs/boosts, stealth (sound radius + line of sight), dynamic difficulty, save system.
   - Level design doc: sector maps, lock-and-key graph, puzzle list, enemy placement.
   - Tech design: Unity 6 + URP, Input System, Cinemachine 3rd-person rig, NavMesh AI, ScriptableObject data, Addressables, save format.
2. **Greybox prototype.** One sector in blockout (ProBuilder):
   - Over-the-shoulder controller, aim, one pistol and one melee weapon.
   - One Hollow enemy (chase/attack/stagger) and one human guard (patrol/investigate/alert).
   - Inventory, one lock-and-key puzzle, and the sanity meter with one hallucination effect.
   - **The test:** is 10 minutes of it tense and fun? If not, iterate before making any art.
3. **Art direction.** A style guide covering palette (sterile teal/white labs vs rust-red containment), lighting rules (volumetric fog, flashlight as primary light, emergency strobes), character turnarounds for Max and Emilia (human + Hollow), the Hollow design language, and a UI style (diegetic where possible).
4. **Audio direction.** Reference tracks, an ambience palette (HVAC hum, distant screams, Emilia's psychic "whisper" motif), the heartbeat/low-sanity layer, and the dynamic music states (calm / tension / combat).

**Exit criteria (Gate 1):** greybox playtested by 5+ people, core loop confirmed fun, art and audio bibles approved.

### Phase 3 — Production (12–18 months, in milestones)

**3a. Vertical slice (months 1–5)**: the Containment Wing at final quality, about 45 minutes long.
- **Assets:** a modular sci-fi lab kit (bought, then re-textured), Max, Emilia (human), two Hollow types, one guard. Animations via Mixamo / marketplace, plus a few custom ones.
- **Environment:** lighting pass, post-processing (film grain, chromatic aberration at low sanity), reflection probes, baked + realtime mix, occlusion culling.
- **Systems:** full combat, inventory, safe room and save, map, notes/lore viewer, sanity, two drugs, the first puzzle chain, and Nate's first encounter.
- **Audio:** ambience, footsteps per surface, weapons, enemy VO, and adaptive music via an Audio Mixer.
- **Output:** a **Steam "Coming Soon" page + trailer + demo build**.

**3b. Pre-alpha (months 6–9)**: all Chapter 1 sectors greyboxed (Containment, Research Labs, Security Hub, Maintenance Tunnels), all core systems in, and story beats in placeholder form.

**3c. Alpha (months 10–13)**: feature complete. All enemies, puzzles, upgrades, 3 endings, cutscenes (Timeline plus 2D storybook panels), difficulty modes, settings and accessibility (subtitles, rebinding, aim assist, photosensitivity toggle).

**3d. Beta (months 14–18)**: content complete. Final art, VO, music, balancing, optimization (target 60 fps on a GTX 1060 / M1-class GPU), and localization strings extracted.

### Phase 4 — Testing & QA (overlaps the 3c/3d milestones, about 3 months focused)
- **Bug hunting:** automated EditMode/PlayMode tests via `unity test` in CI (GitHub Actions); softlock checks on every lock-and-key path; save/load fuzzing.
- **Performance:** Profiler and Memory Profiler passes per sector, plus frame-time budgets.
- **Balancing:** ammo and health economy spreadsheets, dynamic difficulty telemetry (deaths, ammo on hand, time per room), and the sanity drain curve.
- **Playtesting:** closed tests through Steam Playtest, a feedback form, and recorded sessions (watch where people get lost and where they stop being scared).

### Phase 5 — Pre-launch (2–3 months)
- **Marketing:** devlogs (TikTok / YouTube Shorts / X / Reddit r/survivalhorror, r/IndieDev), a Discord, the Steam Next Fest demo, press/streamer keys, and a launch trailer.
- **Final polish:** load times (Addressables), crash reporting, a day-one patch branch, store assets and age rating (IARC).

### Phase 6 — Launch
- **Distribution:** Steam (Windows + macOS) first. Optionally itch.io and GOG. iPad / App Store as a later port.
- **Monitoring:** crash dashboards, review sentiment, a hotfix pipeline (`unity build` in CI → SteamPipe upload).

### Phase 7 — Post-launch & LiveOps
- Patches, balance updates, and performance passes.
- **New content:** the remaining 4 endings, a "Vicky / Jasper / Jade" backstory DLC (the playable stealth flashbacks from the GDD), New Game+ / Ironman mode, the iPad port, and localization.
- Live-service features are **not** recommended for this genre; keep it premium, single-player.

---

## 4. Vertical-slice backlog (replaces the old MVP table)

| # | Task | Type | Unity tech |
|---|------|------|-----------|
| 1 | Project setup: Unity 6 LTS URP, Git LFS, packages, CI | Tech | Unity CLI, GitHub Actions |
| 2 | 3rd-person controller + OTS camera + aim | Code | Input System, Cinemachine |
| 3 | Interaction system (doors, pickups, examine item) | Code | — |
| 4 | Inventory grid + item combine | Code/UI | UI Toolkit, ScriptableObjects |
| 5 | Health, damage, hit reactions | Code | Animator |
| 6 | Pistol + knife combat | Code/Art | Raycast, VFX Graph |
| 7 | Hollow AI (chase/attack/stagger/psychic) | Code | AI Navigation |
| 8 | Guard AI (patrol/hear/see/alert) + stealth | Code | AI Navigation, sensors |
| 9 | Sanity system + hallucination FX | Code/Art | URP Volumes, post-processing |
| 10 | Drugs / boosts (2 items with trade-offs) | Code | — |
| 11 | Safe room: save/load + item box | Code | JSON save |
| 12 | Map + notes/lore viewer | UI | UI Toolkit |
| 13 | Containment Wing greybox → art pass | Level | ProBuilder, modular kit |
| 14 | Lighting & atmosphere pass | Art | URP, volumetric fog, light probes |
| 15 | First puzzle chain (3 puzzles, 1 hidden room) | Design | — |
| 16 | Max, Emilia, 2 Hollows, guard: models + anims | Art | Humanoid rig, Mixamo |
| 17 | Ambience, SFX, adaptive music, heartbeat layer | Audio | Audio Mixer, snapshots |
| 18 | Opening cutscene (Emilia's letter) + 2D storybook panel | Narrative | Timeline |
| 19 | Main / pause / settings menus | UI | UI Toolkit |
| 20 | Demo build (Win + macOS) + Steam page | Release | `unity build` |

---

## 5. What I still need from you

1. **Review this PR**: the GDD v2 changes, the cast merge, and the prologue/letter rewrite. Mark up anything that's wrong for your vision.
2. **The ❓ items in `GDD.md`**: confirm the title (or pick an alternative), and decide what to do about Dr. Man's surname.
3. **Run Claude on your Mac** (Desktop app, or `claude` in a terminal in this repo) so the Unity MCP tools are available. Then we start the §2 project setup and the Phase 2 greybox.
4. **Concept images** you already have (Max, Emilia, the facility), dropped into `docs/reference/`.
