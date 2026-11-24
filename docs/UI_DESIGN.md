# HOLLOW KIN — HUD & Menu Design

> Source of truth for the in-game HUD and menus. Extends `ART_BIBLE.md` §7 (UI).
> Survival horror set in a decommissioned government lab: the UI is **clinical equipment** (patient monitors, intake forms, specimen labels), not game chrome.

## Principles
1. **It belongs to the world.** Everything looks like hospital / lab hardware: thin hairlines, corner brackets, stencil labels, subject IDs, barcodes. No glossy fantasy panels.
2. **No progression UI.** No XP bar, no skill tree, no levels. Power comes from found weapons, parts and pouches (Resident Evil style): the HUD only shows *state* (health, sanity, ammo).
3. **Quiet until it matters.** Panels sit at low opacity in the corners. They brighten and shift colour when something is wrong (low HP, fraying sanity, low ammo). Nothing pulses when the player is fine.
4. **Colour carries meaning** (from the Art Bible):
   - **Clinic teal** `#5fa39a` — normal / stable
   - **Sodium amber** `#e0a547` — caution
   - **Alarm red** `#b8323a` — danger only (low HP, damage hits)
   - **Lantern blue** `#6fb7ff` — psychic: the **sanity** meter and anything to do with Emilia / Hollows
   - **Monitor white** `#dfe9e6` — primary text · **Dim** `#3b4f4c` — secondary text and lines
   - Panel fill: near-black `#0b0f10` at ~70% opacity
5. **Type:** Condensed uppercase sans with wide letter-spacing for labels; large bold numerals for values. (Engine Roboto for now; swap to IBM Plex Sans/Mono per the Art Bible when fonts are imported.)

## In-game HUD (1920×1080 reference)

| Element | Where | Content |
|---------|-------|---------|
| **Vitals panel** | Bottom-left | Header `VITALS` + subject tag `L-04 / HUNT, M.` · **HP bar** (segmented, number at right) with status word · **Sanity bar** (lantern blue) with cognition word |
| **Weapon panel** | Bottom-right | `SIDEARM` caption · weapon name · loaded rounds (big) / reserve (small) · turns amber when low, red when empty |
| **Reticle** | Centre | Only while aiming. Four hairline ticks and a dot; no fill |
| **Damage flash** | Full screen | Red edge flash when hit; strength fades out |
| **Sanity haze** | Full screen | Blue-grey edge tint that grows as sanity falls |
| **Location tag** | Top-left | `LANTERN FACILITY // CONTAINMENT WING` in dim text |
| **Prompt line** | Bottom-centre | Context prompts (`[E] EXAMINE`), hidden by default |

### Status words
- **HP:** `STABLE` (>66%) · `CAUTION` (33–66%) · `CRITICAL` (<33%, bar turns red and the panel flickers)
- **Sanity (cognition):** `LUCID` (>70%) · `UNSTABLE` (40–70%) · `FRAYING` (15–40%) · `BREAKING` (<15%)

### Sanity rules wired up so far
- Drains slowly while the **flashlight is off** (darkness); stops when it is on. Floor at 0.
- Not yet connected: set-piece drains, drawings (+25), sedatives (+40), safe-room refill (to a 60 cap) — see GDD §5.4.
- The GDD originally hid the meter on Normal and above. Decision: the meter is **visible by default** and can be turned off in Protocols (settings) later.

## Accessibility and platform notes (from the Art Bible)
- **Flashing / pulsing effects** (damage flash, critical flicker) get a settings toggle; reduced mode shows a steady tint instead.
- **Gamepad from day one:** the first menus are plain UMG. Move them to **CommonUI** (navigation, input-aware prompts) before the vertical-slice menus are finished, as the roadmap plans.
- **Easy mode** adds a subtle HUD pulse when enemies hear the player (GDD §5.3).
- **Later diegetic layer:** health on a wrist monitor and posture, inventory as a medical tray with a 6–10 slot grid, files as photographed paper, the map as a clinical facility plan.

## Menus
Presented as an **intake / patient-file system**. Dark background, a file-folder tab in the top-left, hairline frame with corner brackets, barcode strip and `LANTERN // PROJECT FILE` footer.

### Main menu
| Item | Meaning |
|------|---------|
| `NEW ADMISSION` | New game |
| `CONTINUE` | Load the latest save (greyed out until saves exist) |
| `PROTOCOLS` | Settings (not built yet) |
| `DISCHARGE` | Quit |

Title treatment: **HOLLOW KIN** in wide-spaced capitals; sub-line `PROJECT LANTERN — SUBJECT FILE L-03 / L-04`. A file card on the right shows `HUNT, EMILIA — L-03 — [REDACTED]` and `HUNT, MAX — L-04 — PENDING INTAKE` (his intake file, GDD §3). The menu theme is Emilia's lullaby (GDD §9), not added yet.

### Pause menu
Opens with `P` (or Start on a gamepad). Game is paused, scene dims, panel header reads `SUSPENDED`.
| Item | Meaning |
|------|---------|
| `RESUME` | Close the menu |
| `EXAMINE` | Inventory tray (later) |
| `PROTOCOLS` | Settings (later) |
| `RETURN TO INTAKE` | Back to the main menu |
| `DISCHARGE` | Quit |

## Bigger weapons (planned)
The weapon panel is data-driven: it reads a weapon name and loaded/reserve rounds from the player. When the shotgun, nail-gun-style tool and others arrive, the same panel shows them; no layout change needed. Upgrades (pouches, weapon parts) appear in the inventory tray, never as an XP screen.
