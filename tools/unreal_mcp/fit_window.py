"""Window fits the screen (2026-11-26): on every launch the menu controller checks the window; in windowed mode a
window taller/wider than the desktop (or smaller than half its height, e.g. 1280x720 pixels on a Retina screen) (e.g. the 14" MacBook Pro, notch + menu bar) is shrunk to 80% of the desktop
height at 16:9 and re-applied. The menu keeps the mouse locked inside the window (LockAlways)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
PC = '/Game/HollowKin/Blueprints/Systems/BP_MenuPlayerController.BP_MenuPlayerController'
call(BT, 'add_function_graph', {'blueprint': {'refPath': PC}, 'graph_name': 'FitWindow'})
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], r)
w(PC + ':FitWindow', '''(fn FitWindow ()
  (bind gus (Settings|GetGameUserSettings))
  (bind desk (Settings|GetDesktopResolution :self gus))
  (bind cur (Settings|GetScreenResolution :self gus))
  (bind (dwi dhi) (Utilities|Struct|BreakIntPoint desk))
  (bind (cwi chi) (Utilities|Struct|BreakIntPoint cur))
  (bind dh (* dhi 1.0))
  (bind dw (* dwi 1.0))
  (switch Utilities|FlowControl|Switch|SwitchonEWindowMode (Settings|GetFullscreenMode :self gus)
    (:Windowed
      (if (or (or (> (* chi 1.0) (* dh 0.88)) (> (* cwi 1.0) (* dw 0.95))) (< (* chi 1.0) (* dh 0.5)))
        (bind h (* dh 0.8))
        (bind wd (Math|Float|Min(Float) (* h 1.7778) (* dw 0.9)))
        (Settings|SetScreenResolution :self gus :Resolution (Utilities|Struct|MakeIntPoint (Math|Float|Truncate wd) (Math|Float|Truncate h)))
        (Settings|ApplyResolutionSettings :self gus :bCheckForCommandLineOverrides false)
        (Settings|SaveSettings :self gus)))))''')
w(PC + ':EventGraph', '''(event EventBeginPlay
  (CallFunction|FitWindow)
  (bind wm (UserInterface|CreateWidget "/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu_C" self))
  (UserInterface|Viewport|AddToViewport wm)
  (Variables|MouseInterface|SetShowMouseCursor true)
  (Input|SetInputModeUIOnly :PlayerController self :InWidgetToFocus wm :InMouseLockMode "LockAlways"))''')
