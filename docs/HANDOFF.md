# Handoff — context for a new Claude session

Read this first, then `docs/ROADMAP.md`, `docs/GDD.md`, `docs/ART_BIBLE.md`, `docs/levels/CONTAINMENT_WING.md` and `docs/narrative/PROLOGUE.md`.

## The project
- **HOLLOW KIN** (formerly "Project Stargate"): a realistic, third-person, over-the-shoulder sci-fi survival horror game in **Unreal Engine 5.8.4**, for Windows + macOS.
- **Developer:** solo, spending as little as possible, on an **M4 Max Mac Studio (64 GB)**.
- **Story:** Max Hunt (21) breaks into a shut-down government lab (Project LANTERN) to rescue his sister Emilia (15). The L-7 serum has turned her into a "Hollow" with telekinesis.
- **Core cast:** Max, Emilia, Dr. Lorraine Huckley, Dr. Sebastian Mán (villain), Jaz Hawkins (radio ally), Nate Carter (combat ally).

## Decisions already made (don't re-litigate)
- **Engine:** Unreal Engine 5, realistic 3D. Unity and a 2D pixel-art version were both considered and dropped.
- **Title:** *Hollow Kin*. Enemies are called Hollows, and the villain's surname is spelled "Mán".
- **Scope:**
  - Chapter 1 first, with 3 launch endings (driven by hidden Bond/Taint values).
  - Sanity is a resource that drains and refills, not a timer.
  - Ironman mode is opt-in.
- **Story hook:** Max sold blood to a mobile donation van that is secretly a LANTERN front. (This replaced a security-job offer, which was too close to the FNAF movie.)
- **Assets:** Fab/Megascans, MetaHuman, the Game Animation Sample, Blender for hero props, AI concepts for reference only. Voices from ElevenLabs on a paid plan, with lip-sync via MetaHuman Animator.
- **Build approach:**
  - **Blueprint-first** (Live Coding is Windows-only); a small C++ module only if needed.
  - Windows builds need a Windows machine or a cloud Windows PC; the developer hasn't chosen which yet.

## Where things stand
- All design docs are on branch `claude/unity-game-roadmap-hpl2oh`, PR: https://github.com/RedZero13/Project-Stargate/pull/1 (open, docs only). Work continues on this branch.
- Unreal Engine 5.8.4 is installed. The first launch failed with *"cannot execute tool 'metal' due to missing Metal Toolchain"*. The fix given was:
  `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer && sudo xcodebuild -license accept && xcodebuild -runFirstLaunch && xcodebuild -downloadComponent MetalToolchain`, then `xcrun -sdk macosx metal --version` to verify.
  **Confirm first whether the editor now opens.**
- **No Unreal project exists yet.**

## Next steps (ROADMAP §2.1 and §5)
1. Make sure the editor launches (the Metal Toolchain fix above).
2. Create a **Games → Third Person**, **Blueprint**, Desktop, Maximum quality project named `HollowKin` (no Starter Content) inside this repo.
3. Enable the **Model Context Protocol** and **All Toolsets** plugins, and set `bAutoStartServer=True` in `HollowKin/Saved/Config/MacEditor/EditorPerProjectUserSettings.ini` under `[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]`.
4. Run `ModelContextProtocol.GenerateClientConfig ClaudeCode` in the editor console, then restart Claude in the project folder so the `unreal-mcp` tools load.
5. Then work through backlog items 2–5:
   - Git LFS + `.gitattributes` (uasset/umap/fbx/wav/png/exr/psd, with locking) + an Unreal `.gitignore`.
   - The folder structure from `ART_BIBLE.md` §8.
   - Enhanced Input + over-the-shoulder camera + aim mode.
   - A greybox test corridor with the flashlight and Lumen darkness tuned.

   Commit and push after each working step.

## Working rules
- Save in the editor before and after every batch of MCP changes. Stop Play-In-Editor before editing assets.
- Commit only to `claude/unity-game-roadmap-hpl2oh` (or a new branch if the PR has been merged).
- Explain things simply: the developer is new to Unreal.
