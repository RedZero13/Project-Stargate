"""Second half of fullscreen_toggle.py: GI ToggleFullscreen (switch on all 3 modes), DoToggleFS in BP_Max and the
menu controller, and an F11 key event node wired to it (the DSL can't create key events directly)."""
from ui_lib import call
import json
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
GI = '/Game/HollowKin/Blueprints/Systems/BP_HKGameInstance.BP_HKGameInstance'
PC = '/Game/HollowKin/Blueprints/Systems/BP_MenuPlayerController.BP_MenuPlayerController'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], r)
TOFS = '''      (Settings|SetFullscreenMode :self gus :InFullscreenMode "WindowedFullscreen")
      (Settings|SetScreenResolution :self gus :Resolution desk)
      (Settings|ApplySettings :self gus :bCheckForCommandLineOverrides false)'''
TOWIN = '''      (Settings|SetFullscreenMode :self gus :InFullscreenMode "Windowed")
      (Settings|SetScreenResolution :self gus :Resolution (Utilities|Struct|MakeIntPoint (Math|Float|Truncate wd) (Math|Float|Truncate h)))
      (Settings|ApplySettings :self gus :bCheckForCommandLineOverrides false)'''
w(GI + ':ToggleFullscreen', '''(fn ToggleFullscreen ()
  (if (Utilities|String|EqualExactly(String) (Game|GetPlatformName) "Mac") (return))
  (bind gus (Settings|GetGameUserSettings))
  (bind desk (Settings|GetDesktopResolution :self gus))
  (bind (dwi dhi) (Utilities|Struct|BreakIntPoint desk))
  (bind h (* dhi 0.8))
  (bind wd (Math|Float|Min(Float) (* h 1.7778) (* dwi 0.9)))
  (switch Utilities|FlowControl|Switch|SwitchonEWindowMode (Settings|GetFullscreenMode :self gus)
    (:Windowed
%s)
    (:WindowedFullscreen
%s)
    (:Fullscreen
%s)))''' % (TOFS, TOWIN, TOWIN))
for bp in (PC, MAX):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': 'DoToggleFS'})
    w(bp + ':DoToggleFS', '(fn DoToggleFS ()\n  (Class|BPHKGameInstance|ToggleFullscreen :self (Utilities|Casting|CastToBP_HKGameInstance (Game|GetGameInstance))))')
    g = {'refPath': bp + ':EventGraph'}
    for old in call(BT, 'find_nodes', {'graph': g, 'title': 'F11'}).get('returnValue') or []:
        call(BT, 'delete_node', {'node': old})
    k = call(BT, 'create_node', {'graph': g, 'type_id': 'Input|KeyboardEvents|F11', 'pos': {'x': -400, 'y': 2400}})
    c = call(BT, 'create_node', {'graph': g, 'type_id': 'CallFunction|DoToggleFS', 'pos': {'x': 0, 'y': 2400}})
    print(str(k)[:200], str(c)[:200])
    kn = k['returnValue']; cn = c['returnValue']
    print(call(BT, 'connect_pins', {'output_pin': {'direction': 'EGPD_Output', 'index_id': 0, 'node': kn}, 'input_pin': {'direction': 'EGPD_Input', 'index_id': 0, 'node': cn}}))
    print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False}))
w(PC + ':EventGraph', '''(event EventBeginPlay
  (CallFunction|FitWindow)
  (bind wm (UserInterface|CreateWidget "/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu_C" self))
  (UserInterface|Viewport|AddToViewport wm)
  (Variables|MouseInterface|SetShowMouseCursor true)
  (Input|SetInputModeGameAndUI :PlayerController self :InWidgetToFocus wm :InMouseLockMode "LockAlways" :bHideCursorDuringCapture false))''')
