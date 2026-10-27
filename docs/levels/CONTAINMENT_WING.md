# Level design: St. Brigid's + Containment Wing (vertical slice)

> Target: **~45 minutes** for a first playthrough. This is the content of the Steam demo.
> Scale: rooms are given in 16-px tiles (W×H). The screen shows about 30×17 tiles.

## 1. Flow at a glance

```
                     ┌──────────────────────── SURFACE ───────────────────────┐
                     │ S1 Loading Bay ─► S2 Clinic Lobby ─► S3 Records Office │
                     │                         │                    (Huckley's │
                     │                         ▼                     desk/key) │
                     │                    S4 Service Lift ◄──────────────┘    │
                     └─────────────────────────┬──────────────────────────────┘
                                               ▼  (one-way: the lift dies)
 ┌──────────────────────────────── CONTAINMENT WING (hub) ──────────────────────────────┐
 │                                                                                       │
 │  C2 Decon Corridor ──► C3 Nurses' Station ──► C4 Observation Ring ──► C9 Lab Door ▣    │
 │       ▲                     │   ★SAFE ROOM          │      (loop)        (Act 2, locked)│
 │       │                     ▼                       ▼                                 │
 │  C1 Lift Landing       C5 Cell Block A ◄──────► C6 Children's Dorm                    │
 │                             │  (drone patrol)       │  (drawings, Hollow Child)       │
 │                             ▼                       ▼                                 │
 │                        C7 Isolation Cells ──► C8 Emilia's Room ──► END OF SLICE       │
 │                           (guard, stealth)      (L-03 tag door)                       │
 └───────────────────────────────────────────────────────────────────────────────────────┘
```

## 2. Rooms

| ID | Room | Size | Content | Purpose |
|----|------|------|---------|---------|
| S1 | Loading Bay | 24×16 | Child's drawing taped to the door (end of the prologue). Flashlight pickup. | Teaches **movement + flashlight**. Pitch black except for a sodium lamp |
| S2 | Clinic Lobby | 30×20 | Overturned chairs, dead reception PC, a note about "the Halvorsen van". **First scare:** a shadow passes the window | Teaches **examine**; plants the blood-van subplot |
| S3 | Records Office | 18×14 | Huckley's desk (her last diary entry, the **Lift Keycard**), a locked filing cabinet (code puzzle, optional) | First **key item**; optional puzzle for **handgun ammo ×10** |
| S4 | Service Lift | 8×8 | Lift ride cutscene: Emilia's voice over the PA (*"Big brother? Is that you?"*). The lift drops the last metre and dies | Point of no return; Emilia's first line |
| C1 | Lift Landing | 16×12 | Dead guard with the **pistol + 6 rounds**. Radio crackles: **Jaz's first call** | Teaches **pick up weapon**; meet Jaz |
| C2 | Decon Corridor | 40×8 | Long and narrow. **First Hollow Drone** shambles out of a decon shower at the far end | Teaches **aim + shoot**. Enough ammo to kill it; tension comes from having to spend it |
| C3 | Nurses' Station ★ | 16×12 | **Safe room:** warm lamp, save terminal, item box, typewriter-style log. Sedative ×1 | First relief beat. Teaches **save + item box** |
| C4 | Observation Ring | 36×24 | A circular corridor around a glass observation tank (empty, cracked from the inside). Doors to C5, C6, C9. Hollow Screamer behind the glass on revisit | The **hub loop**. The player passes it 3–4 times |
| C5 | Cell Block A | 30×18 | 6 cells, 2 open. **Drone patrol** (2 Drones). Cell 4 holds **Fuse A** | Choose: fight (ammo) or sneak round the patrol (stealth) |
| C6 | Children's Dorm | 24×16 | 4 beds, toys, **3 of Emilia's drawings** (Bond +, sanity +). Under Jade's bed: **Fuse B**. **Hollow Child** encounter: it hides, flees, then cowers. **Spare** or **kill** | The game's **heart**: lore, the first moral choice, Bond/Taint |
| C7 | Isolation Cells | 28×16 | Dark (flashlight only). **Guard** patrolling with a torch. Lockers for hiding. Breaker panel (**puzzle 2**) | Teaches **stealth, hiding and noise**. The guard is very dangerous here |
| C8 | Emilia's Room | 16×12 | Door tagged `L-03 / HUNT, E.`. Inside: a bed bolted to the floor, a hundred drawings on the walls, floating debris that stops when Max enters. Emilia isn't there. Final drawing: Max and Emilia at the lake | **Slice ending**: Emilia appears in the glass and whispers *"You came."* The lights die. Title card: **"WISHLIST HOLLOW KIN"** |
| C9 | Lab Door | — | Sealed blast door, panel reads `RESEARCH LABS — LOCKDOWN` | Teases Act 2; locked in the slice |

## 3. Lock-and-key chain

```
Flashlight (S1) ─► Lift Keycard (S3) ─► Lift (S4) ─► Pistol (C1)
                                                        │
                    ┌───────────────────────────────────┘
                    ▼
        Fuse A (C5) + Fuse B (C6) ─► Breaker panel (C7) ─► power to the C8 door ─► END
```
Both fuses can be collected in either order, which gives the player a small taste of non-linear routing.

## 4. Puzzles

| # | Location | Type | Solution |
|---|----------|------|----------|
| P1 (optional) | S3 filing cabinet | Observation | The 4-digit code is Emilia's birthday (`0611`). It's circled on Huckley's desk calendar ("Em turns 15 🎂") and mentioned in her diary entry |
| P2 | C7 breaker panel | Logic | Route power through a 3×3 grid of rotatable fuse tiles. The wiring diagram is drawn on the back of a child's drawing in C6, so **the lore is the key** |
| P3 (hidden) | C6 Jade's bed | Examine | Rotating the toy rabbit reveals a seam with a **Clarity** drug and a note from Jade inside. Optional, for replays |

## 5. Resource economy (Normal)

| Resource | Placed | Needed to fight everything | Intent |
|----------|--------|----------------------------|--------|
| Handgun ammo | 6 (C1) + 10 (S3, optional) + 6 (C5) = **22** | ~26 | It's slightly impossible to kill everything; sneaking is rewarded |
| Health (first-aid gel) | 2 | — | One mistake is survivable, two is risky |
| Sedative | 1 (C3) | — | Introduces sanity recovery |
| Clarity | 1 (hidden, P3) | — | A reward for curiosity |
| Emilia's drawings | 3 (C6) + 1 (C8) | — | Bond + sanity |

## 6. Encounters

| Where | Enemy | Behaviour | Ideal answer |
|-------|-------|-----------|--------------|
| C2 | Hollow Drone ×1 | Scripted: shambles straight down the corridor | Shoot it (tutorial) |
| C5 | Hollow Drone ×2 | Patrol loop through the cell rows | Sneak through the open cells (stealth) or spend about 10 rounds |
| C6 | Hollow Child ×1 | Hides, darts between beds, cowers when cornered | **Spare it** (Bond +10) or kill it (Taint +15) |
| C7 | Guard ×1 | Patrol, investigates noise, shoots on sight | Hide in lockers; throw a bottle to lure him away |
| C4 (revisit) | Hollow Screamer (behind glass) | Shrieks when the flashlight hits it: sanity −15 | Lesson: turn the flashlight off near the tank |

## 7. Sanity beats (designed)
- S2: shadow at the window (−5).
- C4: the first time Max sees the cracked tank (−10).
- C6: the drawings restore it (+25 total).
- C7: darkness drains it slowly; the guard's torch is both a threat and relief.
- C8: on purpose, the player should reach the ending at around **40–60 sanity**, so the hallucination effects are in view for the trailer.
