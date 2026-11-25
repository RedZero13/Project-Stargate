# HOLLOW KIN: 15-floor expansion plan (2026-11-26)

Asked for: at least 15 floors, puzzles, Emilia in the deepest isolation chambers (after the testing labs) with
4-5 other kidnapped children, cutscenes, rooms full of medical props (beds, IVs, diagnostics, X-ray, MRI),
dead nurses/doctors, undead people and failed experiments, then a gameplay trailer.

## Floor map (all underground, Halvorsen Biologics)
| Floor | Name | Map | Gate to the next floor |
|---|---|---|---|
| B1 | Containment Wing (existing) | Lvl_ContainmentWing | 2 fuses → breaker (existing) |
| B2 | Admissions | Lvl_Wards | keycard |
| B3 | Paediatric Ward | Lvl_Wards | switch sequence (order drawn on a child's picture) |
| B4 | Radiology (X-ray, angiography "MRI") | Lvl_Wards | keycard |
| B5 | Surgery | Lvl_Wards | power: restart the floor generator |
| B6 | Pharmacy & Blood Lab | Lvl_Wards | switch sequence |
| B7 | Morgue | Lvl_Wards | keycard |
| B8 | Security & Records | Lvl_Wards | power |
| B9 | Deep Labs (existing: labs, tunnels, generator hall) | Lvl_DeepLabs | brute + generator |
| B10 | Specimen Storage | Lvl_DeepLabs | keycard |
| B11 | Testing Lab A | Lvl_DeepLabs | switch sequence |
| B12 | Testing Lab B (experiments) | Lvl_DeepLabs | power |
| B13 | Observation | Lvl_DeepLabs | keycard |
| B14 | Sedation Ward | Lvl_DeepLabs | switch sequence |
| B15 | Isolation Chambers: Emilia + 5 children, finale | Lvl_DeepLabs | ending |

Floors in one map are stacked 1500 cm apart. A **lift** at the end of each floor runs a short cutscene
(fade, floor title card "B4 — RADIOLOGY") and moves Max to the next floor. Two maps instead of 15 keeps memory and
load times down.

## Systems to build
- `tools/floors_layout.py`: generates each floor's rooms and corridor from themed templates (one data file per map).
- `tools/unreal_mcp/build_floors.py`: greybox walls/floors/lights (same pipeline as `build_slice.py`) plus
  **furnishing by theme** with Horror Hospital props: beds, IV stands, stretchers, treatment tables, wheelchairs,
  the fluorograph (X-ray), angiography scanner + monitors (MRI room), anaesthesia machine, blood test machine,
  fume cupboards, microscope, fridges, racks, medical waste bins, curtains, signs (Radiology, Surgery, Nursery…).
- `BP_FloorLift`: the gate and lift: locked until its floor puzzle is solved, then plays the transition.
- Puzzles: `BP_Keycard` (pickup → unlocks that floor's lift), `BP_SeqSwitch` (3 floor switches stepped in
  order; the order is on a note/drawing; a wrong order resets with a buzz), power (`BP_FloorGenerator`).
- People: dead nurses/doctors (Zombie Nurse + Survival Character in dead poses), undead patients (Hollows),
  failed experiments (Zombie Mutant as a tougher Hollow variant), 5 children + Emilia in glass isolation cells.
- Cutscenes: camera-blend vignettes like the gun pickup: arrival at B9, the experiment reveal on B12, the
  children on B15, the Emilia reunion (all three endings branch here).
- Trailer: recorded from the packaged build when everything is in, cut with title cards and music (ffmpeg).

## Assets
Already installed: Horror Hospital (2,400+ props), Dead Bodies poses, Survival Character, civilian girl, Whisper.
Added for this: Zombie Female Nurse (free), Zombie Mutant (free, UE 5.5 package).
