# HOLLOW KIN — Game Design Document v5 (as built, 2026-11-28)

> v5 describes the game **as it is built today** and keeps the remaining design as clearly marked plans.
> v4 (the original Unreal design: Dr. Mán, Huckley boss, Nate, drugs, ink-ribbon modes) is in git history and its
> unbuilt parts are listed in §12. Companion docs: [`TECHNICAL.md`](TECHNICAL.md) (how it is built) ·
> [`ART_BIBLE.md`](ART_BIBLE.md) · [`UI_DESIGN.md`](UI_DESIGN.md) · [`EXPANSION_PLAN.md`](EXPANSION_PLAN.md) ·
> [`narrative/`](narrative/) · [`ROADMAP.md`](ROADMAP.md) · [`PLATFORMS.md`](PLATFORMS.md).

---

## 1. Overview

| | |
|---|---|
| **Title** | HOLLOW KIN (working title; trademark search still to do before a store page) |
| **Genre** | Third-person survival horror, story-first, with hidden-variable endings |
| **Camera** | Over-the-shoulder (RE2/RE4 Remake style), shoulder swap, tighter when aiming |
| **Engine** | Unreal Engine 5.8, realistic 3D, Lumen on High/Epic |
| **Platforms** | macOS now · Windows next · iPad (M-series) prepared · consoles planned (`PLATFORMS.md`) |
| **Requirements** | Mac: min Apple M1 / 8 GB / macOS 14, recommended M2 Pro–M3 Pro+ / 16 GB · iPad: min M1 / 8 GB, recommended M4 iPad Pro 16 GB (`PLATFORMS.md` §0) |
| **Length** | First clear about 2–2.5 h; 100% (all 7 endings, collectibles, achievements) about 6–7 h with chapter select and New Game+ |
| **Model** | Premium, single-player, offline |
| **Studio** | Terratales Media Entertainment Private Limited |

**Logline:** A broke 21-year-old breaks into a shut-down children's clinic to bring his little sister home, and finds
the hospital goes fifteen floors down, and what is waiting at the bottom is her.

### Pillars
1. **Dread over action.** Fighting always costs something: ammo, health, sanity, or a piece of who Max is.
2. **Every choice is remembered.** Small decisions change who you meet later and how the story ends — deterministic,
   but hidden on the first run.
3. **The monster is family.** Every system points back at Emilia and the five other children.

---

## 2. Story

### 2.1 Setting
Millbrook, a rainy small town. **St. Brigid's Clinic**, a bright, too-clean private clinic run by **Halvorsen
Biologics**, sits at the end of Main Street. Under it, fifteen basement floors: common wards, a paediatric ward,
radiology, surgery, pharmacy and blood lab, morgue, security, then the **Deep Labs** (B9) and below them the secret
government-contract levels (specimen storage, two testing labs, observation, sedation) and **B15, the isolation
chambers**, where six children are kept in glass cells: **L-01 Noor (8), L-02 Theo, L-03 Emilia Hunt, L-04 Mila,
L-05 Sofi Vargas (9), L-06 Ivy (6).** Project **LANTERN** gives these children an anomaly in the blood; the "lantern"
is the glow their nervous systems give off. The adults it was tried on became **Hollows**.

### 2.2 Backstory (canonical)
- Max Hunt (21) and Emilia (15) lost their parents; Emilia was taken into state care at six and never reached her
  foster home. Six days ago a letter told Max she never existed in the foster system.
- **Halvorsen Biologics** runs LANTERN under a government contract. Dr. Halvorsen's daughter **Jasmine ("Jaz")** wrote
  the dosing schedules, gave the children names because nobody else would, and is now trying to undo it.
- Tonight the clinic is being shut down and everything below it erased — including the children.

### 2.3 Chapters (as built)
| Chapter | Where | What happens |
|---------|-------|--------------|
| **Prologue — Millbrook** | Main Street, night, rain | Jaz's call ("your sister is alive"), an abandoned police car with quarantine chatter, a fence of MISSING posters (all state-care children), a child in a hospital gown under a streetlight who vanishes, Jaz calling back, a crashed ambulance and **Leo Vargas**, the dying paramedic who drove Emilia in. **Choice 1.** |
| **1 — St. Brigid's Clinic** | G (OPD, emergency, cafeteria) and F1 (maternity, NICU) | The passenger lift is out of order and its neighbour's doors have been forced open on an empty shaft. Max climbs the stairs; on F1 every bed is made and every drip still runs into an empty bed; a small figure watches from the NICU. Nurse **Okafor** knocks from a locked office (**choice 2**). Three floor switches in the order shown by a child's drawing power the service lift to the basements. |
| **2 — Containment Wing (B1)** | Hand-built slice | Fuses, Emilia's first drawings, the **Hollow Child** (spare or hurt), the pistol from a dead guard, the breaker, the power door. |
| **3 — The Wards (B2–B8)** | Seven generated floors | One lift puzzle per floor (keycard, switches, counters, generator, breakers). Okafor again (B5, confession) or her Hollow (B3). Paediatric medicine (B4, **choice 3**). Sgt. **Hale**, a bitten guard (B8, **choice 4**). Jaz confesses she wrote the dosing schedules. |
| **4 — The Deep Labs (B9–B15)** | Hand-built B9 + six generated floors | Hale's cache or his squad (B9). The research archive (B11, **choice 5**). Hale turning (B12, mercy or last stand). Sedated patients (B14, **choice 6**). The six children, Emilia's cell, the release console, the ending. |

### 2.4 Characters
| Character | Role | Arc |
|-----------|------|-----|
| **Max Hunt** (21) | Protagonist (voice: Kokoro `am_echo`) | Dry humour over guilt; how far he goes decides what he becomes (Bond vs Taint). |
| **Emilia Hunt** (15) | Sister, subject L-03 | Draws "the man with a torch" coming for her. Speaks in the B15 reunion; in New Game+ her whispers guide Max. |
| **Jaz (Jasmine Halvorsen)** | Voice on the phone | Calls in the prologue, at the Wards and at the Deep Labs, more honest each time; in New Game+ she admits Dr. Halvorsen is her father. |
| **Leo Vargas** | Paramedic | Dying beside his ambulance; drove Emilia in; asks Max to tell his daughter Sofi (L-05) he's sorry he was late. |
| **Nurse Adaeze Okafor** | Staff, complicit | Sedated the children to pay for her son's treatment. Freed: confesses on B5 (forgive / condemn). Left: becomes a Hollow on B3. Forgiven: carries the last child out in the good endings. |
| **Sgt. Elias Hale** | Halvorsen guard | Bitten on B8. Spared: his squad holds fire, and on B12 he either gets a merciful end or holds the corridor with one bullet (and kills the Experiment). Robbed: his squad hunts Max on B9. |
| **The children** | Noor, Theo, Mila, Sofi, Ivy | Told through patient files, drawings and the B15 cells; whether they leave depends on Max. |
| **Dr. Halvorsen** | Unseen antagonist | Present in files, orders and Jaz's confession. |

---

## 3. Core loop
Explore a floor -> read notes and drawings (they hold the puzzle answers, all saved in the journal) -> find the
floor's evacuation plan (map) -> solve the lift puzzle while avoiding or fighting Hollows -> make the floor's choice if
there is one -> ride the lift down. Resources (ammo, gels, sedatives, parts, chemicals, bottles) are always scarce;
the workbench turns parts and chemicals into what you need.

---

## 4. Systems (as built)

### 4.1 Movement and camera
Motion-matched locomotion (walk, run, crouch, jump, vault), over-the-shoulder camera, shoulder swap, aim zoom.

### 4.2 Combat
- **Pistol** (M1911): hitscan, 6-round magazine, auto-reload, reserve capped at 40. Aim with RMB/Q (T toggles).
- **Melee** punch; **glass bottles** thrown as a noise lure (Hollows walk to the sound).
- **Enemies:** Hollow (melee, red eye glow, alert stinger), **guard** (rifle, warning shot first), **undead nurse**,
  **brute / Experiment** (Elite, 60% damage taken), **Hollow Child** (spare or hurt), hazards (shock floors,
  explosive barrels). Hollows open doors they reach.
- **Difficulty:** EASY (less damage, more supplies) / NORMAL / BRUTAL (harder hits, fewer supplies). New Game+ adds
  +30% Hollow health.

### 4.3 Sanity
0–100. Drops in darkness and when hurt; sedatives restore 35. Low sanity tints and distorts the screen; at 0 Max
breaks down (death screen, reload). Hallucinated enemies exist (`BP_Hallucination`).

### 4.4 Inventory and crafting
RE4-style backpack (B): items with real models. Workbench (I): **6 rounds** = 2 parts + 1 chemical; **sedative** =
2 chemicals; **health gel** = 1 part + 1 chemical. Health gel +40 HP.

### 4.5 Exploration aids
- **Map (M):** each floor's plan once its **EVACUATION PLAN** board in the lift lobby is photographed (clinic plans
  are always known).
- **Journal (J):** every note, clue, file and choice outcome, newest first, in Max's handwriting — including the
  mission-critical ones (switch order, counter digits, breaker instructions).
- **Objectives** tab: current goal plus the history.

### 4.6 Puzzles
Keycard search · three floor switches in a drawn order · **breaker panel** (four breakers wired in a chain: each flips
its neighbours; all green powers the lift) · **counter lock** (3-digit code, one digit on each of three notes) ·
generator restart · B1 fuses + breaker · B15 cell release (needs 5 patient files).

### 4.7 Floors and layouts
Every basement floor has its own plan: straight spine, ring (two corridors around a block of rooms), jog (offset
corridors with a central hub) or hall (corridor with an open hall). Always present: two washrooms (toilets, sinks,
shower), a break room, two stair cores, the lift lobby and the lift room. G adds a cafeteria. Real doors on every
room. Above ground is bright and clean; the basements are cold, desaturated and clinical, full of machinery, dead
staff and — from the Wards down — dead guards. A separate basement stairwell is collapsed on most floors (open to a
landing on B3, B6, B11).

### 4.8 Lifts
Real lifts: doors open as you approach a working lift, close once you are inside, the cabin hums for a few seconds,
and you step out of the next floor's lift. No loading screen between floors.

### 4.9 Collectibles and rewards
17 of Emilia's drawings (Bond; every 5 hides a health gel) and 14 patient files (lore, the children's names; every 5
gives rounds). L-7 serum vials heal fully but add Taint.

### 4.10 Achievements
30, including all endings, the hidden ending, NPC arcs (Absolution, Last Stand, Whistleblower), collectibles, kills,
crafting and puzzles. Kept across runs; shown on the main menu.

---

## 5. Choices
Each choice is a two-option prompt (E / Y). Consequences are **deterministic** but not shown; most surface floors
later or only in the ending.

| # | Where | Option A | Option B |
|---|-------|----------|----------|
| 1 | City — Leo Vargas | Give him your gel: +Bond, he explains the F1 lift | Search his pockets: supplies, +Taint; a Hollow paramedic waits on G |
| 2 | F1 — Okafor | Free her: +Bond, med cache on B2, her confession on B5 | Leave her: +Taint, she is a Hollow on B3 |
| 2b | B5 — Okafor's confession | Forgive: +Bond, she helps carry the children out | Condemn: +Taint, she disappears |
| 3 | B4 — paediatric medicine | Take it: 2 gels + sedative | Leave it for the children: +15 Bond (needed for LANTERN LIT) |
| 4 | B8 — Sgt. Hale | Bandage him (1 gel): +Bond, ammo cache on B9, his squad holds fire | Take his ammo: +12 rounds, +Taint, two of his squad hunt you on B9 |
| 4b | B12 — Hale turning | End it quickly: +Taint | Leave him one bullet: +Bond, he kills the B12 Experiment for you |
| 5 | B11 — the archive | Send it to Jaz: an alarm brings two Hollows; endings expose Halvorsen | Wipe it: −10 Taint; Halvorsen reopens under a new name |
| 6 | B14 — sedated patients | Wake them: +Bond, but two have already turned | Let them sleep: +Taint |
Plus: sparing or hurting the Hollow Children (B1, B3, B7, B11, B13), taking L-7 serums, killing at all (Lullaby).

---

## 6. Endings (7)
| Ending | Condition (checked in this order) | What happens |
|--------|-----------------------------------|--------------|
| **HOLLOW** | Taint ≥ 80 | The serum finishes what it started; Emilia holds her brother's hand as his eyes go dark. |
| **LANTERN LIT** (hidden) | New Game+ and cells opened and archive sent and medicine left and Okafor freed and Taint < 20 | Max, Emilia and the five children walk out into the dawn. |
| **SIX DOORS** | Cells opened, Bond ≥ 70, Taint < 40 | Six children walk out; the city finally hears their names. |
| **LULLABY** | No kills this run, Bond ≥ 40, Taint < 40 | Emilia sings and every Hollow lies down to sleep. |
| **HOMECOMING** | Bond ≥ 70, Taint < 40 | Emilia is human again; they walk out into the morning. |
| **KIN** | Bond ≥ 40 | She survives as what she is, and leaves with him. |
| **LANTERN** | otherwise | Max stays behind so she can live. |
Epilogue lines change with the archive choice, Okafor's fate and Hale's last stand.

---

## 7. Replay design
- **Chapter select** (unlocked as chapters are reached) with a fixed kit per chapter; collectibles and Bond/Taint
  start fresh so every ending is reachable from Chapters 3–4.
- **New Game+** after any ending: pistol and 32 rounds from the start, last run's journal carried over as "memories",
  tougher Hollows, Emilia's whispered hints (F1, B4, B11), Jaz's final confession (B15), and the only route to
  LANTERN LIT.
- Hidden, deterministic tallies in the Silent Hill 2 tradition: the game judges how you played rather than asking.

---

## 8. Art direction (as built)
Realistic UE5 with Fab packs (Horror Hospital interiors, Assetsville town, Survival Character for Max, Whisper for
Hollows, tactical outfit for guards, Zombie Nurse). Clean white/teal/yellow above ground; grime, decals, blood, dead
LED panels and cold light below. Lights sit under LED ceiling panels. Full spec: `ART_BIBLE.md`. MetaHumans for Max
and Emilia are still planned.

## 9. UI (as built)
Diegetic-first: objective top-left, message panel, ammo/health ring bottom-right; RE4-style backpack; 007-style
Options page (Protocols); chapter cards; achievements; journal/map. Fonts: Cinzel, Barlow Semi Condensed, Patrick
Hand. Controller and touch supported. Spec: `UI_DESIGN.md`.

## 10. Audio (as built)
Kokoro (offline TTS) voices for all spoken lines (32 lines: Max, Jaz, Emilia, Leo, Okafor, Hale, police radio);
horror ambience, music-box lullaby, tension loops, interface sounds. Planned: final actor or ElevenLabs voices,
lip-sync, adaptive music states.

---

## 11. Content warning
Child endangerment and medical experiments on children (implied, never shown graphically), violence, gore, suicide
implication (Hale). Shown at startup.

---

## 12. Not built yet (from v4 and later ideas)
- Bosses (Huckley Hollow, Dr. Mán / Dr. Halvorsen confrontation); ally Nate.
- Shotgun / nail gun, breakable knife, weak points, psychic push.
- Drugs (Adrenal, Stonewall, Clarity), inventory pouch upgrades.
- Hiding spots, stealth noise radii beyond the bottle lure, dynamic difficulty, Nightmare / Ironman modes.
- Map auto-colouring and player pins; safe-room item box.
- MetaHumans for Max and Emilia, facial animation and lip-sync, storybook prologue panels.
- Localisation, subtitles options beyond text size, full accessibility pass.
