# HOLLOW KIN — Genre research and "make sure the game has this" checklist

> Purpose: look at comparable survival-horror games, then list what our game should add or guarantee. Status column refers to the current prototype (see `HANDOFF.md`).
> Evidence quality: the web searches below were short; where a point comes from general genre knowledge rather than a source, it is marked *(general)*. Check Fab prices and availability yourself before buying.

## What comparable games teach us

| Game | Lessons for Hollow Kin | Sources |
|------|------------------------|---------|
| **Resident Evil 2 (2019)** | Scarcity (ammo, healing, inventory slots) is the core tension. The inventory is real-time (no pausing to heal), which raises tension. Save rooms are a relief beat: music change, item box, safe feeling. Enemies follow you between rooms (not only when in sight), but never into save rooms. Varied threat types sustain fear; heavy scripting of spawns is a common criticism, so mix scripted and systemic encounters. Items can break grabs (knife, grenade). Replays use shuffled enemy/item placement and harder modes. | [Game Developer: design examination](https://www.gamedeveloper.com/design/a-design-examination-on-resident-evil-2-remake), [difficulty modes](https://www.gamedeveloper.com/design/evolving-difficulty-modes-in-survival-horror-resident-evil-2) |
| **Dead Space (2023)** | Diegetic UI done well (health on the suit, ammo on the gun) — our chosen direction. Strong accessibility menu: difficulty, aim assist, single-press instead of button-mash events, menu narration, subtitle size/colour, colour-blind filters, separate dialogue/effects/music volume, optional content warnings (off by default). | [EA: accessibility and player choice](https://ea.com/able/news/accessibility-and-player-choice-in-dead-space), [GameRant summary](https://gamerant.com/dead-space-remake-accessibility-options-audio-gameplay/) |
| **Alan Wake 2** | Flashlight as a character (our flashlight). Three difficulty presets; bass-reduction and mono audio options; separate mixer sliders; "hold" vs "toggle" for aim. Some effects (horror flashes) are hard to disable without breaking level flow, so design flashing effects with a safe alternative from day one. | [Alan Wake: gameplay assists](https://www.alanwake.com/story/gameplay-assist-alan-wake-2/), [accessibility settings](https://sportskeeda.com/esports/alan-wake-2-accessibility-settings-explored) |
| **Silent Hill 2 remake, Callisto Protocol, Signalis, Crow Country, Amnesia, Outlast** | *(general)* Sound and sight limitation do most of the scaring (fog, darkness, radio static). Fixed-ish camera angles or cramped corridors for dread. Melee that costs durability. Environmental storytelling via notes. Hiding/stealth verbs (lockers, holding breath). Short, readable puzzles tied to story. Not researched in detail here. | — |

## Checklist: what Hollow Kin has, and what to add

Legend: ✅ built · 🟡 partly · ⬜ not yet · 📄 designed in a doc only

### Core loop and combat
| Aspect | Status | Notes |
|--------|--------|-------|
| Over-the-shoulder movement + aim | ✅ | Game Animation Sample character; shoulder swap removed (sample camera) |
| Pistol (hitscan), ammo, reload | ✅/🟡 | Needs real animations, sounds, hit effects, reload time |
| Shotgun, nail-gun lab tool, knife (breaks) | ⬜📄 | GDD §5.2. Weapon data-asset system needed first |
| Weak points, limb stagger, grabs + escape items | ⬜📄 | RE2 lesson: items (knife/flashbang) break grabs |
| Enemy types: Drone ✅, Guard ⬜, Screamer ⬜, Child ⬜, bosses ⬜ | 🟡 | Drone patrols, hears, chases, attacks, ragdolls |
| Enemies track across rooms but never enter save rooms | 🟡 | Drone follows noise/sight; add "safe room" rule |
| Mix scripted set-pieces with systemic AI | ⬜ | Avoid pure scripting (RE2 critique) |
| Stealth: noise, light, hiding | 🟡 | Gunshot/footstep noise ✅, flashlight affects sight ✅; hiding spots, hold-breath ⬜ |

### Resources, items, progression
| Aspect | Status | Notes |
|--------|--------|-------|
| Pickups (ammo, health gel, sedative) | ✅ | Placed by hand for now |
| Inventory grid (6→10 slots), examine view, item box | ⬜📄 | Real-time (no pause), per RE2 |
| Doors, keys, fuse/breaker puzzle, lock-and-key graph | 🟡 | Being built next |
| Permanent upgrades found in world (pouches, weapon parts) — no XP | ⬜📄 | Matches "no skill tree" decision |
| Crafting (simple: combine items) | ⬜ | Optional; keep tiny |
| Item and ammo placement that adapts (dynamic difficulty) | ⬜📄 | GDD §5.7 |

### Sanity (our signature system)
| Aspect | Status | Notes |
|--------|--------|-------|
| Drain in dark / flashlight off | ✅ | |
| Hallucinated enemies at low sanity | ✅ | One type; add fake footsteps, moving objects |
| Screen tint, heartbeat, whispers, false directions from Emilia | 🟡/⬜ | Tint ✅; audio ⬜ |
| Restore: drawings (+25), sedative ✅, safe room (to 60) ✅ | 🟡 | Drawings ⬜ |
| Breakdown at 0 | ⬜ | Cutscene then reload |
| Bond/Taint hidden values + 3 endings | ⬜📄 | Drives the Hollow Child choice |

### Saving, menus, flow
| Aspect | Status | Notes |
|--------|--------|-------|
| Checkpoint save at safe-room terminals, continue from menu | ✅ | One slot; add 3 slots, autosave at chapter boundaries |
| Limited-save mode (ink-ribbon style) on Nightmare | ⬜📄 | RE lesson: saving costing something adds tension |
| Main menu, pause menu | ✅ | Settings ("Protocols") ⬜ |
| Map that fills in as rooms are cleared | ⬜📄 | Clinical facility plan |
| Death → retry quickly | ✅ | Add "hint" tips on death screen *(general)* |
| New Game+, difficulty presets, Ironman | ⬜📄 | |

### Accessibility and comfort (do not leave until the end)
Taken from Dead Space / Alan Wake 2 practice plus Art Bible §7:
- Subtitles on by default, **size and colour options**, speaker names
- Separate **volume sliders** (music / effects / dialogue / voice-over), **mono audio**, bass reduction
- **Flashing/pulsing effects toggle** with a steady alternative (design effects so the game works without them)
- **Aim toggle vs hold**, adjustable aim assist, single-press instead of button-mash prompts
- **Full key/button rebinding**, mouse sensitivity and invert, controller dead zones
- Colour-blind modes, UI scale, optional content warnings (off by default)
- Menu narration (later), gamepad navigation in all menus (move to CommonUI)
- Camera shake / motion blur / head-bob sliders *(general)*

### Technical and shipping
| Aspect | Notes |
|--------|-------|
| Performance targets in Art Bible §1 (60 fps RTX 3060 / M-series, 30–40 Steam Deck) | Profile each milestone |
| Shader-compile stutter (PSO cache), load times | Before Next Fest demo |
| Controller-first input (Steam Deck), Steam Input | |
| Steam page, trailer, achievements, cloud saves, crash reporting | Roadmap Phase 5–6 |
| Localization from String Tables | All UI text should go through String Tables soon |
| Photo mode, spectate/replays | *(general, optional)* |
| Windows build machine | Decision pending (cloud PC vs used PC) |

## Suggested additions to the design (new ideas to consider)
1. **Safe-room rule for AI:** enemies lose interest at the safe-room door; the music changes to the lullaby. Makes saving feel like relief.
2. **Item that breaks a grab** (knife, flashbang) so melee has a reason to exist.
3. **Radio ally (Jaz) as a hint system:** optional hints through the radio on difficult puzzles, so we need fewer pop-up hints.
4. **Flashlight battery or heat** *(general)*: only if it does not fight the sanity rule (flashlight off already costs sanity).
5. **Examine-to-solve puzzles using Emilia's drawings** (already in the GDD) — keep puzzle solutions in notes, not guesswork.
6. **Optional "hold breath" stamina meter** when hiding (GDD §5.3).
7. **Ambient dread audio layer** driven by sanity (whispers, false footsteps), not only the screen tint.
8. **A short, strict first 10 minutes**: movement, flashlight, aim, one fight, one save, one scare, then the lift. Players judge the game in that window.
