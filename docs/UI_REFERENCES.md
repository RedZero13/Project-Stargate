# UI references

Site: https://gameuidatabase.com (Game UI Database, ~80,000 screenshots from ~2,000 games, browsable by game and by screen category). It blocks automated fetching (HTTP 403) but loads in a normal browser. **Use it for reference only; do not copy art.** Check its terms before reusing anything.

## Horror titles listed on its front page (good matches for Hollow Kin)
Resident Evil 7, Crow Country, Still Wakes the Deep, Reanimal, Clive Barker's Hellraiser: Revival, Silent Pines (Silver Pines), plus the references the developer shared: The Sinking City 2 (main menu, difficulty, saves, item inspect), Alan Wake 2-style / Marastan game (settings, save select, dialogue).

## Screens to restyle, with the target reference
| Screen | Current | Target (from developer's references) |
|--------|---------|--------------------------------------|
| Main menu | Left column, teal text | Keep clinical look; large logo, one highlighted row with accent bar, controller prompt on the right |
| Difficulty (`WBP_Difficulty`) | Copy of pause menu | Centered title banner, one button per level, description text under the list (hover updates it), BACK prompt bottom-right |
| Settings | Two toggles | Tabs (Gameplay / Sound / Video / Language / Controls / Accessibility), left list, right description panel, DEFAULT / BACK prompts |
| Item inspect | none | Rotatable 3D item on the right, name + description + a short quote on the left, ROTATE / TAKE prompts |
| Dialogue | none (text only in docs) | Name in accent colour above a thin line, subtitle-style text box at the bottom, CONTINUE prompt; optional topic list top-left |
| Save select | one slot | 3 to 6 slots, each with location, time, difficulty, empty-slot state; DELETE / BACK |

Order of work suggestion: settings tabs + sliders (needed for sensitivity/volume/accessibility) → save slots → item inspect → dialogue.

---

## Second batch (2026-11-25): 007 First Light, Control, Resident Evil 4 remake

Reference screenshots and screen recordings stay local (not in git): `~/Downloads/Control07252024-063732-17658.mp4`,
`Control07252024-063732-25506.mp4` (menu + game-start animation), `Resident-Evil-4-202307292024-125019-5960.mp4`,
`Resident-Evil-4-202307292024-125019-3173.mp4`, plus chat screenshots. These are **style references only**: we copy
layout ideas and feel, never art, logos, fonts or text.

### What each reference asks for

| Reference | Screen | What to take for HOLLOW KIN |
|---|---|---|
| 007 First Light options | Options | Full-screen page: small "OPTIONS /" caption, left category list (GAMEPLAY, CONTROLS, GRAPHICS, AUDIO, ACCESSIBILITY, EXIT), centre rows with label left and toggle / slider / value right, thin separators, highlighted row with a warm underline glow, right column = description of the focused row + "Default value". Bottom-right button hints, bottom-left build version. Blurred game scene behind. |
| 007 audio page | Audio | Master / Effects / Music / Dialogue volume **sliders** with numbers. |
| 007 subtitles page | Accessibility | Subtitle size, background opacity, background colour, text colour, speaker name in colour, with a live preview. |
| Control fast travel / missions | Map, objectives | Left list + big right panel; mission list with a TRACK marker and a description card. |
| Control videos | Menu animation | Menu and game-start transition animations (fades, slides) — to be studied frame by frame. |
| RE4 load game | Main menu | Left vertical menu (CONTINUE, LOAD GAME, NEW GAME, EXTRAS), right list of save slots with thumbnail, date, chapter, location / objective; one-line help text + button hints at the bottom. |
| RE4 chapter card | Loading | Black left half with chapter title + 2-3 line story recap, scene image on the right, page dots and a thin progress bar. |
| RE4 tutorial modal | Tutorials | Dimmed blurred game, right card with picture, title, 2-3 lines, "Next". |
| RE4 examine | Item pickup | Item shown large on the right with its name, game blurred behind, "Close". |
| RE4 Mission Failed | Death | Large spaced title over smoke, CONTINUE / LOAD GAME / QUIT, help line at the bottom. |
| RE4 typewriter | Save point | Left small menu (Save Game, Storage...), object on the right. Ours: tape recorder. |
| RE4 attaché case | Inventory | Grid case, objective top-left with a marker icon, item name + description under the case, weapon ring bottom-right. |
| RE4 treasure / files / challenges / gallery / totals / area map | Extras | Later milestones. |
| RE4 HUD | In game | Circular weapon + ammo ring bottom-right, small objective notification, contextual button prompts on objects, QTE prompt. |
| Text with background (developer note) | All in-game text | Every message / subtitle / objective sits on a solid dark plate. |

### Build order (agreed direction, newest first)
1. In-game text on solid plates; objective panel top-left (done 2026-11-25).
2. Full-screen Options page in the 007 layout (categories, sliders, description column) replacing the Protocols popup.
3. Main menu in the RE4 layout (left list, save-slot list on the right), chapter loading card between levels.
4. Death screen in the Mission Failed layout; tutorial modal cards for first-time controls.
5. Weapon/ammo ring HUD; contextual prompts; examine view for pickups.
6. Inventory case, map, files, extras.
