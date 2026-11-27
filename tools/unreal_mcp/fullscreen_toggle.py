"""Own fullscreen toggle (2026-11-26). The engine's F11/Alt+Enter toggle kept the small window resolution inside
the macOS fullscreen space, so the picture went black and the window slid off the bottom of the screen (clicks
missed). Now F11 (menu and game) calls BP_HKGameInstance.ToggleFullscreen: borderless fullscreen at the DESKTOP
resolution, or back to a window that fits (80% of the desktop height, 16:9)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
GI = '/Game/HollowKin/Blueprints/Systems/BP_HKGameInstance.BP_HKGameInstance'
PC = '/Game/HollowKin/Blueprints/Systems/BP_MenuPlayerController.BP_MenuPlayerController'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], r)
call(BT, 'add_function_graph', {'blueprint': {'refPath': GI}, 'graph_name': 'ToggleFullscreen'})
w(GI + ':ToggleFullscreen', '''(fn ToggleFullscreen ()
  (bind gus (Settings|GetGameUserSettings))
  (bind desk (Settings|GetDesktopResolution :self gus))
  (bind (dwi dhi) (Utilities|Struct|BreakIntPoint desk))
  (bind h (* dhi 0.8))
  (bind wd (Math|Float|Min(Float) (* h 1.7778) (* dwi 0.9)))
  (switch Utilities|FlowControl|Switch|SwitchonEWindowMode (Settings|GetFullscreenMode :self gus)
    (:Windowed
      (Settings|SetFullscreenMode :self gus :InFullscreenMode "WindowedFullscreen")
      (Settings|SetScreenResolution :self gus :Resolution desk)
      (Settings|ApplySettings :self gus :bCheckForCommandLineOverrides false))
    (:Default
      (Settings|SetFullscreenMode :self gus :InFullscreenMode "Windowed")
      (Settings|SetScreenResolution :self gus :Resolution (Utilities|Struct|MakeIntPoint (Math|Float|Truncate wd) (Math|Float|Truncate h)))
      (Settings|ApplySettings :self gus :bCheckForCommandLineOverrides false))))''')
GICALL = '(Class|BPHKGameInstance|ToggleFullscreen :self (Utilities|Casting|CastToBP_HKGameInstance (Game|GetGameInstance)))'
w(PC + ':EventGraph', '(event Input|KeyboardEvents|F11 (Key)\n  %s)' % GICALL)
w(MAX + ':EventGraph', '(event Input|KeyboardEvents|F11 (Key)\n  %s)' % GICALL)
# menus must let the controller see F11: Game+UI input (mouse still locked to the window)
w(PC + ':EventGraph', '''(event EventBeginPlay
  (CallFunction|FitWindow)
  (bind wm (UserInterface|CreateWidget "/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu_C" self))
  (UserInterface|Viewport|AddToViewport wm)
  (Variables|MouseInterface|SetShowMouseCursor true)
  (Input|SetInputModeGameAndUIEx :PlayerController self :InWidgetToFocus wm :InMouseLockMode "LockAlways" :bHideCursorDuringCapture false))''')
