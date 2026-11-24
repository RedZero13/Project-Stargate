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
