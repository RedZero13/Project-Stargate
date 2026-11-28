# HOLLOW KIN — Platforms: iPad, controllers, consoles

Status 2026-11-28. Mac builds ship today; Windows needs a Windows PC (`BUILDING.md`).

---

## 0. System requirements (estimates, 2026-11-28)
Measured so far: install size about 2.1 GB (download 1.8 GB zip); memory use 5.7 GB on the main menu and up to
~7.7 GB in heavy areas on High (measured with the editor also open, so in-game use alone is lower). Tested on a Mac
Studio M4 Max and a MacBook Pro 14" M3 Pro. Everything else is an estimate until more devices are tested.

### macOS (Apple Silicon only; Intel Macs are not supported)
| | Minimum | Recommended |
|---|---|---|
| Chip | Apple M1 | Apple M2 Pro / M3 Pro or newer (M4 for 60 fps on High) |
| Memory | 8 GB unified memory | 16 GB or more |
| OS | macOS 14 Sonoma | macOS 15 Sequoia or newer |
| Storage | 5 GB free (SSD) | 10 GB free |
| Settings | LOW / MEDIUM preset (Lumen off), 70% render scale, 1080p, ~30 fps | HIGH / EPIC (Lumen on), 100% render scale, 1440p+, 60 fps |
| Input | Keyboard + mouse | Keyboard + mouse, or Xbox / PlayStation controller |

### iPad (M-series only)
| | Minimum | Recommended |
|---|---|---|
| Device | iPad Air or iPad Pro with M1 (8 GB) | iPad Pro with M4 (16 GB models: 1 TB / 2 TB storage) |
| OS | iPadOS 17 | iPadOS 18 or newer |
| Storage | 5 GB free | 10 GB free |
| Settings | iOS profile at 70% render scale, 30 fps | iOS profile at 80–100% render scale, 60 fps |
| Input | Touch (on-screen sticks + buttons) | Bluetooth Xbox / PlayStation / MFi controller |
Lumen is off on every iPad (screen-space lighting instead). A-series iPads and iPhones are not targeted.

---

## 1. Controllers (done)
Xbox, PlayStation (DualSense / DualShock 4) and MFi pads work on Mac and iPad through Enhanced Input.
Layout (Xbox names): left stick move · right stick look · LB sprint · A jump/climb · B crouch · LT aim · RT fire ·
X reload · RB melee · Y interact · D-pad up torch · D-pad down throw · D-pad left map/journal · D-pad right workbench ·
View backpack · Menu pause · R3 swap shoulder. Menus: the first button gets focus on the first pad press, D-pad moves,
A presses, B / Menu / View go back. Built by `tools/unreal_mcp/controller.py`.
Still to do for a polished pad experience: button glyphs in prompts (currently "E / (Y)"), rebinding UI, aim assist
(slight magnetism on Easy/Normal), rumble on hits and gunshots.

---

## 2. iPad (M4 iPad Pro) — set up, needs your Apple ID to build

### What is already configured
- `Config/DefaultEngine.ini` `[/Script/IOSRuntimeSettings.IOSRuntimeSettings]`: iPad only, landscape, bundle id
  `com.terratales.hollowkin`, **Metal SM5 (desktop-class) renderer**, 60 fps cap with high refresh, controllers on,
  automatic signing (team id empty until you add one).
- `Config/DefaultDeviceProfiles.ini` `[IOS DeviceProfile]`: no Lumen / hardware RT (screen-space + baked-style
  lighting), medium shadows/effects/view distance, 80% render scale, 1.5 GB texture pool.
- `Config/IOS/IOSInput.ini`: on-screen move/look sticks; `WBP_TouchHUD` adds FIRE, AIM, USE, RELOAD, TORCH, BAG, MAP,
  PAUSE buttons (only on iOS). A Bluetooth controller is the recommended way to play.

### What you need to do (one time, ~10 minutes)
1. **Xcode -> Settings -> Accounts -> +** -> sign in with your Apple ID. A free account works for testing on your own
   iPad (apps expire after 7 days; reinstall to renew). The paid Apple Developer Program ($99/yr) removes the limit
   and enables TestFlight.
2. Plug the iPad in with USB-C, unlock it, **Trust This Computer**.
3. On the iPad: **Settings -> Privacy & Security -> Developer Mode -> On** (restarts the iPad).
4. Tell Claude when done: it reads your Team ID from Xcode, writes it into the project, and runs the build.

### How the build runs
```bash
"/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun \
  -project="$PWD/HollowKin/HollowKin.uproject" -noP4 -platform=IOS -clientconfig=Development \
  -build -cook -stage -pak -compressed -package -deploy -utf8output
```
`-deploy` installs onto the connected iPad. First cook for iOS takes a while (shaders for Metal SM5).

### Risks and things to check on the device
- **Memory:** the M4 iPad Pro has 8 or 16 GB; the Mac build uses ~6–8 GB. If it runs out, lower texture pool and
  view distance in the iOS profile.
- **Lighting:** without Lumen the basements may look flatter or darker; may need extra fill lights or a per-level
  exposure bias for iOS.
- **Thermals:** cap at 30 fps if it throttles (`FrameRateLock=PUFRL_30`).
- **Game Animation Sample** content must be present locally (it is, on this Mac).
- Shipping on the App Store additionally needs: paid developer account, App Store Connect listing, privacy labels,
  age rating, icons/launch screen, and Apple review.

---

## 3. Consoles — plan

### 3.1 Which consoles and what it takes
| Platform | Access | SDK / devkits | Cost (approx.) | Notes |
|----------|--------|---------------|----------------|-------|
| **Xbox Series X\|S** | ID@Xbox application (free) | GDK + Xbox devkits (or "Dev Mode" on a retail console for early tests) | Devkit loan/purchase; dev mode $19 one-off | Easiest entry for indies; Game Pass is a funding route |
| **PlayStation 5** | PlayStation Partners application (company registration, NDA) | PS5 SDK + devkit/testkit | Devkit purchase (~$2.5k) | Needs a registered company (Terratales qualifies) |
| **Nintendo Switch 2** | Nintendo Developer Portal application | NintendoSDK + devkit | Devkit purchase | UE5 realistic lighting needs heavy scaling (no Lumen); last priority |
| **Steam Deck** | none (Steam) | Proton or native Linux | free | Effectively a PC target; verify controller + 800p performance |

Unreal provides the console platform code only after approval, through Epic's console developer portal (UDN). Our
project is Blueprint-only, which keeps porting simpler: no engine changes, no game C++.

### 3.2 Work needed (in order)
1. **Windows build first** (consoles are closer to Windows than to Mac): Windows PC, D3D12, PSO cache, shader stutter pass.
2. **Controller-first UI** (mostly done): glyphs per platform (Xbox / PlayStation / Switch), no mouse-only screens,
  safe-zone margins (TV overscan), text size options, rebinding.
3. **Performance targets:** 30 fps locked minimum, 60 fps mode on PS5/Series X; Series S at reduced resolution.
  Tools: Unreal Insights, `stat unit`, GPU profiler. Expect: Lumen on PS5/Series X (software or hardware RT), off on
  Series S/Switch; TSR upscaling; texture streaming budgets; level streaming for the 15-floor maps (split Wards/Deep
  into streamed sub-levels per floor so memory stays bounded).
4. **Platform services:** achievements/trophies (map our 30 achievements; PS5 needs a Platinum and trophy grades),
  user sign-in and profile switching, cloud-safe saves via the platform save API (our three SaveGame slots map
  cleanly), Activities (PS5) / Hero Stats optional, rich presence.
5. **Certification requirements** (TRC for PlayStation, XR for Xbox, Lotcheck for Nintendo): suspend/resume, sign-out
  handling, controller disconnect pause, save-data error handling, no hangs over N seconds without a spinner, age
  rating screens, mandatory platform terminology ("Wireless Controller", etc.), accessibility basics.
6. **Ratings:** IARC (digital) covers most stores; ESRB/PEGI/USK/CERO for physical or as platforms require. Expect
  M / PEGI 18 (gore, child-endangerment themes).
7. **Store assets and builds:** platform packaging (PKG / XVC / NSP), patches, day-one notes, store pages, trailers.

### 3.3 Suggested timeline (after the Steam PC release)
| Month | Milestone |
|-------|-----------|
| 0 | Apply to ID@Xbox and PlayStation Partners (in parallel with PC beta) |
| 1–2 | Approval, devkits, platform SDK installed in UE5.8; first boot on devkit |
| 2–4 | Performance pass, streamed floors, platform services (achievements, saves, sign-in) |
| 4–5 | Certification pre-checks, ratings, store setup |
| 5–6 | Submission, fixes, release (Xbox and PS5 together; Switch 2 later if at all) |

### 3.4 Budget rough order (solo/indie)
Devkits $3–6k total, ratings mostly free via IARC (physical ratings extra), optional QA/cert-prep contractor
$5–15k, console porting house alternative (full port) $40–100k+. Xbox via ID@Xbox is the cheapest first console.
