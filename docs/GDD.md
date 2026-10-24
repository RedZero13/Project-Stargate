# HOLLOW KIN — Game Design Document v2

> Supersedes *Project Stargate – The Following Saga* (GDD v1).
> Status: **draft for review**. Everything marked ❓ needs a decision from you.

## 0. Change log vs. v1

| v1 | v2 | Why |
|----|----|-----|
| Title *Project Stargate: Remnants* | **HOLLOW KIN** (working title) | "Stargate" is an MGM trademark, and *Remnant* is an existing game franchise (*Remnant: From the Ashes*). |
| In-world *Project Stargate* | **Project LANTERN** | Avoids the trademark. A "lantern" is also the faint glow the subjects' nervous systems give off. |
| Enemies called *Remnants* | **Hollows** | Same franchise conflict. "Hollow" ties into the title: people emptied of themselves. |
| ~13 named characters | **6 core characters** + 3 children told through notes and enemy encounters | Cuts modelling, rigging and voice work roughly in half. |
| Sanity = 100→0 level timer | **Sanity = resource** that drains and refills | A timer punishes the exploration the genre is built on. |
| Souls-like "restart the whole run" | **Ironman** mode, unlocked after the first clear | Optional for players who want it, and not something to balance around. |
| 7 endings | **3 at launch**, 4 saved for post-launch | Cuts cutscene and QA cost. |
| Contradictory backstory (adopted vs. "every foster home"; receptionist vs. security-guard job; 1st vs. 3rd person prose) | One canonical timeline (§3) | Consistency. |
| Platform: Mac, Windows, iPad | **macOS + Windows** at launch, iPad later | One developer working on an M4 Max Mac Studio. |
| 2D-platformer MVP table | Vertical-slice backlog (`ROADMAP.md` §4) | The old table was for a different game. |

❓ **Alternative titles** if you don't like *Hollow Kin*: *Below the Lantern*, *Sister Signal*, *The Quiet Ward*. Whatever you pick needs a USPTO/EUIPO and Steam search before the store page goes up.

---

## 1. Overview

| | |
|---|---|
| **Genre** | Third-person survival horror / sci-fi thriller |
| **Camera** | Over-the-shoulder (RE2 Remake / RE4 Remake style) |
| **Inspirations** | Resident Evil 2 & 7, Silent Hill 2, *Venom* (2018), *Stranger Things* (the Lab) |
| **Audience** | 20–45, story-first and casual-to-core horror players |
| **Platforms** | macOS (Apple Silicon) + Windows via Steam; iPadOS later |
| **Engine** | Unity 6 LTS, URP |
| **Length (Chapter 1)** | 5–7 hours for a first clear |
| **Business model** | Premium, single-player, no live service |

**Logline:** A broke 21-year-old breaks into a shut-down government lab to bring his little sister home, and finds the thing hunting him through its corridors *is* her.

### Design pillars
1. **Dread over action.** Combat is always a cost, never a reward.
2. **Every resource is a choice.** Ammo, health, sanity and drugs all compete for the same eight inventory slots.
3. **The monster is family.** Every system eventually points back at Emilia.

---

## 2. Core loop

```
Explore ──► find key items / notes / Emilia's drawings
   ▲                     │
   │                     ▼
Safe room ◄── fight or evade ◄── solve puzzle → unlock shortcut / new sector
(save, item box,           (spend ammo, health, sanity)
 craft, recover sanity)
```

The game is semi-open in the RE2 style: one central sector (Containment) with locked shortcuts into the other three. You backtrack once you've found new keys or tools.

---

## 3. Story: canonical version

### Timeline
| When | Event |
|------|-------|
| **−5 yrs** | The Hunts' car crash. The parents die. Max is **16** and Emilia is **10**. Paramedics' bloodwork flags an anomaly in Emilia's blood. Within days she is taken into state custody, and from there quietly transferred to Project LANTERN. Max is told she was "placed with a specialist medical foster program". |
| −5 yrs | Max is placed with **Walter and June Hale**, an elderly couple, as his only foster placement. They are warm and decent. |
| −3 yrs | Max falls in with the wrong crowd. When a dealer the Hales owe money to threatens them, Max takes a **felony possession-with-intent charge** that wasn't his, to keep them out of it. |
| −1 yr | The Hales turn cold and then openly hostile. (Late-game reveal: LANTERN had been paying them a monthly stipend to report on Max, who may share Emilia's anomaly. When the project began shutting down, the payments stopped and the pressure began.) Max moves into a studio apartment he can barely afford. |
| −1 yr → now | **Dr. Lorraine Huckley** begins smuggling letters from Emilia to Max. |
| −1 month | A well-dressed stranger offers Max an absurdly well-paid "night escort" job at a private medical site. Max turns it down. (The stranger was a LANTERN recruiter sizing Max up as a replacement subject.) |
| **Day 0** | Huckley's last letter: *Emilia is being released. Meet at the old St. Brigid's clinic on the 14th.* |
| Day 0 + 6 | Nobody comes, and Huckley stops answering. Max goes to St. Brigid's himself. |

**Max's current life (canonical):** receptionist at Dell's Hardware, a family-run shop that is slowly going under. Job applications bounce because of his record and his lack of qualifications.

**What happened inside:** LANTERN was ordered to shut down. The night before Emilia's release, **Dr. Sebastian Man** injected her with **L-7**, an unstable serum, to recover his life's work before the shutdown. It worked too well. Emilia became a **Hollow** with telekinesis and mind control. In a single night she broke the facility, and broke Huckley's mind. She is still down there, still ten years old inside, waiting for her brother.

### Act structure (Chapter 1)

| Act | Location | Beats |
|-----|----------|-------|
| **Prologue** | Max's walk to work → his apartment → the letter | Tone, poverty, loneliness. Emilia's letter (see `narrative/PROLOGUE.md`). |
| **Act 1** | St. Brigid's clinic (surface front) → lift to the **Containment Wing** | Tutorial. First Hollow. Meet **Jaz** over the radio. Find the children's dormitory and drawings. |
| **Act 2** | **Research Labs** + **Maintenance Tunnels** | Meet **Nate**. Learn what L-7 is. Huckley's audio logs grow more and more broken. Boss: **Huckley Hollow**. |
| **Act 3** | **Security Hub** → Emilia's test chamber | Dr. Man's reveal. Dr. Man boss (a human with a psychic-dampening rig). Emilia confrontation. The ending is decided. |

---

## 4. Characters

### Core cast (modelled, voiced)

| Character | Age | Role | Notes |
|-----------|-----|------|-------|
| **Max Hunt** | 21 | Protagonist | Brunette, thin, a worn hoodie and work jacket. Dry humour that hides guilt for not finding her sooner. |
| **Emilia Hunt** | 15 (10 inside) | Sister / Hollow | Two models: **human** and **Hollow**. Naive, optimistic, with a twisted streak. Talks to Max through intercoms, PA systems and *in his head*. |
| **Dr. Lorraine Huckley** | mid-30s | Fallen mentor → boss | Blonde, a prodigy psychiatrist. She was kind to Emilia and smuggled the letters. Emilia's power broke her mind; she's now a Hollow boss. Her audio logs trace her decline. |
| **Dr. Sebastian Man** | 50s | Antagonist | Chinese-born biochemist, a near-Nobel laureate believed dead. Holds that the ends justify any means. Also absorbs Dr. Marlowe's role (the cruel conditioning programme). ❓ "Dr. Man" can read oddly in English dialogue. Consider writing it "Dr. Mán" or giving him a different surname. |
| **Jasmine "Jaz" Hawkins** | late 20s | Insider ally (radio) | A former LANTERN technician hiding in the Maintenance Tunnels. **Merged from three v1 characters:** Jaz (layout and security knowledge), Dr. Kline (the saboteur who leaves clues) and Agent Thompson (gathering evidence). Mostly a voice on the radio, so cheap to produce. |
| **Nathaniel "Nate" Carter** | early 30s | Combat ally | An ex-soldier turned subject who escaped containment. Joins for a few set pieces. His fate depends on your choices. |

### Told through notes, drawings and encounters (not full characters)
- **Vicky (9), Jasper (7), Jade (11):** the other children. Their drawings and diaries are the key collectible. **Two of them are met as Hollows**, and whether you spare them feeds the ending.

### Cut (possible DLC or sequel)
- **Dr. Edward Kline** and **Dr. Eliza Marlowe**: folded into Jaz and Dr. Man.
- **Agent Sarah Thompson**: her agency becomes the "unknown force" behind a post-launch ending.

### Emilia: art direction note
v1 pointed straight at Eveline (RE7). Keep her as a *mood* reference only. Emilia's own silhouette:
- A hospital gown with laminated subject tags (`L-03 / HUNT, E.`) and child's drawings taped to her arms.
- Telekinetic **halo**: a slow orbit of debris (pens, syringes, toys) around her.
- Her nervous system glows through her skin (the "lantern"), and the glow pulses with her mood.
- No "creepy-girl" tropes such as hair over the face or crab-walking. She should be heartbreaking first and frightening second.

---

## 5. Systems

### 5.1 Exploration & puzzles
- RE-style lock-and-key progression, with cross-sector shortcuts.
- Puzzle types: logic (circuit routing), observation (clues hidden in notes and drawings), and skill (timed valve or cooling sequences).
- **Narrative puzzles:** the solutions come from Emilia's letters and the children's drawings, so the lore *is* the key.
- Hidden rooms are opened by examining items closely (rotate, find a seam), which supports replays.
- "Time-waster" puzzles (from v1) appear only as optional side rooms, never on the critical path.

### 5.2 Combat
- **Ranged:** pistol, shotgun, and a nail-gun-style lab tool (sci-fi flavour). Ammo is scarce.
- **Melee:** a knife that breaks, used for defensive counters and escaping grabs.
- **Psychic push** (late game, from the L-7 serum): staggers enemies but raises **Taint** (§5.6).
- **Enemies (Chapter 1):**
  - **Hollow Drone:** shambling, hits hard, weak to headshots.
  - **Hollow Screamer:** a psychic shriek that drains sanity, and it calls in other enemies.
  - **Hollow Child:** fast and evasive. Can be *spared*, which affects the ending.
  - **Guard:** human, uses cover, investigates noise.
  - **Bosses:** Huckley Hollow, Dr. Man.

### 5.3 Stealth
- **Noise:** each action has a sound radius (walk 2 m, run 8 m, gunshot 25 m, thrown bottle as a lure). Guards and Hollows investigate the last noise they heard.
- **Sight:** a vision cone, reduced by darkness. Turning your flashlight off cuts detection but costs sanity over time.
- **Hiding:** lockers, under beds, vents. Some Hollows can sense you; hold your breath (a stamina meter) to stay hidden.

### 5.4 Sanity (redesigned)
**0–100, a resource rather than a timer.**

| Drains | Restores |
|--------|----------|
| Time in darkness (flashlight off) | Safe rooms (slow refill, up to a 60 cap) |
| Hollow psychic attacks and shrieks | Bright, lit areas (stops the drain) |
| Witnessing set-piece horrors | **Emilia's drawings** (rare, +25, also raise Bond) |
| Drug come-downs | **Sedative** item (+40, slows aim) |

| Band | Effects |
|------|---------|
| 100–70 | Normal |
| 70–40 | Whispers, edge vignette, occasional footsteps that aren't real |
| 40–15 | **Hallucinated enemies** that vanish when shot, aim sway, a distorted map |
| 15–1 | Fast heartbeat, the screen darkens (as in v1), Emilia's voice gives false directions |
| 0 | **Breakdown:** a cutscene, then reload from the last save |

v1's countdown survives only in **set-piece escapes** (for example, the Security Hub lockdown), where a hard timer is the right tool.

### 5.5 Drugs & boosts (temporary, with trade-offs)
| Item | Upside | Downside | Duration |
|------|--------|----------|----------|
| **Adrenal** | +30% move speed | −25% damage resistance | 60 s |
| **Stonewall** | +40% damage resistance | −30% move speed | 60 s |
| **Clarity** | Stops sanity drain | Heavy aim sway when it wears off | 90 s |
| **L-7 trace** | Unlocks / charges the psychic push | +Taint (affects the ending), −10 max sanity | permanent |

**Permanent upgrades:** inventory pouches (6 → 8 → 10 slots), weapon parts found in the world, and holster speed. No XP or skill tree; upgrades are found by exploring, which fits the genre.

### 5.6 Hidden ending variables
- **Bond (0–100):** raised by collecting Emilia's drawings, sparing Hollow Children, answering her intercom calls kindly, and keeping her letters in your inventory.
- **Taint (0–100):** raised by using L-7 and by killing Hollow Children.

### 5.7 Difficulty
| Mode | Notes |
|------|-------|
| Easy | More ammo, slower sanity drain, aim assist |
| **Normal** (default) | **Dynamic difficulty** on by default (can be turned off). Loot and sanity drain adapt to recent deaths, how much ammo you carry, and accuracy |
| Hard | Fixed scarcity, smarter guards |
| Nightmare | Hard, plus limited saves (ink-ribbon style) and extra Hollows |
| **Ironman** | Unlocks after a first clear. One life; death ends the run (the "souls-like" mode from v1) |

Balancing is done on **Normal**. The other modes are multipliers on top of it.

### 5.8 Map & save
- An auto-filling map that colours rooms once they're fully looted (RE2 style), with player pins.
- Saving happens only at safe-room terminals, plus autosaves at chapter boundaries.

---

## 6. Endings

### Launch (3)
| Ending | Condition |
|--------|-----------|
| **Homecoming:** Emilia is restored to human | Bond ≥ 70 **and** Taint < 40 |
| **Kin:** Emilia survives as a Hollow and leaves with Max | Bond ≥ 40 (and the Homecoming condition not met) |
| **Lantern:** Max sacrifices himself so she can live | Bond < 40, *or* the player chooses it in the final scene |

### Post-launch (4)
Emilia is killed · Emilia sacrifices herself · Emilia keeps walking the corridors · **an unknown force** (Thompson's agency) takes them both, which sets up a sequel.

---

## 7. Facility: Chapter 1 sectors

| Sector | Mood / palette | Function |
|--------|---------------|----------|
| **St. Brigid's Clinic** (surface) | Decaying 1970s clinic, sodium-orange light | Tutorial and the front for the facility |
| **Containment Wing** (hub) | Rust-red emergency light, padded cells, the children's dorm | Central hub with locked shortcuts |
| **Research Labs** | Sterile teal and white, flickering fluorescents | Puzzles, L-7 lore, Huckley boss |
| **Maintenance Tunnels** | Black, wet, flashlight only | Stealth, Jaz's hideout, shortcuts |
| **Security Hub** | Cold blue monitor glow | Timed lockdown escape, Dr. Man |

All sectors are built from one **modular sci-fi lab kit** (stock), re-textured per sector, with hero props modelled in Blender.

---

## 8. Art
- **Style:** grounded realism with gritty sci-fi touches. Lighting does most of the horror work: volumetric fog, the flashlight as the main light source, emergency strobes.
- **Sources:** stock (Asset Store / Fab) for the modular kit and generic props; **Blender** for hero props, the Emilia Hollow form, and kit-bashed variants; **AI-assisted** concept art and mood boards (concepts only, then repainted or modelled). Characters come from a stock base mesh, customised in Blender, then given humanoid rigs and Mixamo plus marketplace animation.
- **Cutscenes:** in-engine (Timeline + Cinemachine) wherever possible. Backstory flashbacks are **2D storybook panels** with a slow parallax pan, which is cheap and stylish.
- **UI:** mostly diegetic. Health shows in Max's posture and a wrist monitor; sanity shows on screen as vignette and audio rather than a visible meter on Normal and above.

## 9. Audio
- **Voice:** ElevenLabs, one consistent voice per character, recorded with direction notes per line (see `ROADMAP.md` §2.2 for licensing).
- **Music:** adaptive states (calm / tension / combat / chase) driven by Audio Mixer snapshots. Emilia has her own melodic motif: a music-box lullaby that slowly distorts.
- **SFX:** HVAC hum, surface-specific footsteps, Hollow vocals, and the heartbeat layer at low sanity (from v1).
- **Main menu theme:** short and loopable, built on Emilia's lullaby.
