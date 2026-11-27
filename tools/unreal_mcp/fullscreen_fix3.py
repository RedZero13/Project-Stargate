"""Fullscreen fixes (2026-11-27, from the playtest video):
1) The cursor is no longer locked inside the window in menus (main menu, pause, backpack): DoNotLock, so the mouse
   can reach the window's green fullscreen button / other screens. In play the camera still captures the mouse.
2) "Fullscreen" in OPTIONS now applies at launch: FitWindow reads the saved setting first and switches to
   fullscreen the same way the OPTIONS toggle does (before, the window was resized and the setting ignored until
   you toggled it off and on again)."""
import re
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
PC = '/Game/HollowKin/Blueprints/Systems/BP_MenuPlayerController.BP_MenuPlayerController'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
BPK = '/Game/HollowKin/UI/Menus/WBP_Backpack.WBP_Backpack'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
w(PC + ':FitWindow', '''(fn FitWindow ()
  (bind gus (Settings|GetGameUserSettings))
  (bind desk (Settings|GetDesktopResolution :self gus))
  (bind cur (Settings|GetScreenResolution :self gus))
  (bind (dwi dhi) (Utilities|Struct|BreakIntPoint desk))
  (bind (cwi chi) (Utilities|Struct|BreakIntPoint cur))
  (bind dh (* dhi 1.0))
  (bind dw (* dwi 1.0))
  (bind wantfull (and (SaveGame|DoesSaveGameExist "HollowKinSettings" 0)
                      (not (Class|BPSettingsSave|GetWindowed :self (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))))))
  (if wantfull
    (Settings|SetFullscreenMode :self gus :InFullscreenMode "WindowedFullscreen")
    (Settings|SetScreenResolution :self gus :Resolution desk)
    (Settings|ApplySettings :self gus :bCheckForCommandLineOverrides false)
    (else
      (Settings|SetFullscreenMode :self gus :InFullscreenMode "Windowed")
      (if (or (or (> (* chi 1.0) (* dh 0.88)) (> (* cwi 1.0) (* dw 0.95))) (< (* chi 1.0) (* dh 0.5)))
        (bind h (* dh 0.8))
        (bind wd (Math|Float|Min(Float) (* h 1.7778) (* dw 0.9)))
        (Settings|SetScreenResolution :self gus :Resolution (Utilities|Struct|MakeIntPoint (Math|Float|Truncate wd) (Math|Float|Truncate h))))
      (Settings|ApplySettings :self gus :bCheckForCommandLineOverrides false)))
  (Settings|SaveSettings :self gus))''')
w(PC + ':EventGraph', '''(event EventBeginPlay
  (CallFunction|FitWindow)
  (bind wm (UserInterface|CreateWidget "/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu_C" self))
  (UserInterface|Viewport|AddToViewport wm)
  (Class|WBPMainMenu|RefreshNG :self (Utilities|Casting|CastToWBP_MainMenu wm))
  (Variables|MouseInterface|SetShowMouseCursor true)
  (Input|SetInputModeGameAndUI :PlayerController self :InWidgetToFocus wm :InMouseLockMode "DoNotLock" :bHideCursorDuringCapture false))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': PC}, 'warnings_as_errors': False}))
# pause menu and backpack close: same graphs as before (playtest_log.py, build_backpack_logic.py) with the mouse free
w(MAX + ':OpenPause', '''(fn OpenPause ()
  (CallFunction|HKLog :Msg "PAUSE open")
  (bind pc (Game|GetPlayerController 0))
  (bind pm (UserInterface|CreateWidget "/Game/HollowKin/UI/Menus/WBP_PauseMenu.WBP_PauseMenu_C" pc))
  (UserInterface|Viewport|AddToViewport pm 20)
  (Game|SetGamePaused true)
  (Input|SetInputModeUIOnly :PlayerController pc :InWidgetToFocus pm :InMouseLockMode "DoNotLock")
  (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor true)
  (Class|WBPPauseMenu|SetVitals :self (Utilities|Casting|CastToWBP_PauseMenu pm) :Health (Variables|Default|GetHealth) :Sanity (Variables|Default|GetSanity)))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
w(BPK + ':CloseCase', '''(fn CloseCase ()
  (bind pc (Game|GetPlayerController 0))
  (Widget|RemoveFromParent self)
  (bind pm (Widget|GetAllWidgetsOfClass :WidgetClass "/Game/HollowKin/UI/Menus/WBP_PauseMenu.WBP_PauseMenu_C" :TopLevelOnly true))
  (if (> (Utilities|Array|Length pm) 0)
    (Input|SetInputModeUIOnly :PlayerController pc :InWidgetToFocus (Utilities|Array|Get(acopy) pm 0) :InMouseLockMode "DoNotLock")
    (else
      (Game|SetGamePaused false)
      (Input|SetInputModeGameOnly pc false)
      (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor false))))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': BPK}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
