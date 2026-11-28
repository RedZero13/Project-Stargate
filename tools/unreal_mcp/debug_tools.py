"""Developer / debug tools (playtest = Development build; the console does not exist in the Shipping build).
Open the console with the ` key (left of 1; ~ on some layouts) and type   ke * <command> [value]
  HK_Help            list of commands on screen
  HK_God             god mode on/off (no damage, health and sanity stay full)
  HK_Dev             developer mode on/off: god mode + all lifts unlocked + live debug overlay
  HK_Overlay         debug overlay on/off (floor, position, health, sanity, Bond, Taint, flags, run kills)
  HK_Heal            full health and sanity
  HK_GiveAll         pistol, 12 + 40 rounds, 5 gels, 3 sedatives, 5 parts, 5 chemicals, 3 bottles
  HK_UnlockLifts     power every lift on this level
  HK_KillAll         kill every Hollow on this level
  HK_Bond 80         set Bond      HK_Taint 10    set Taint
  HK_Flag nurse_freed  add a story flag (see docs/TECHNICAL.md for the list)
  HK_Chapter 3       start chapter 0-4 (0 Prologue, 1 Clinic, 2 Wing, 3 Wards, 4 Deep Labs)
  HK_Ending          trigger the ending now (uses the current Bond / Taint / flags)
Unreal's own cheats also work after typing  EnableCheats :  God, Fly, Ghost, Walk, Slomo 0.5, Teleport, ViewMode Unlit, Stat FPS."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
GIC = '(Utilities|Casting|CastToBP_HKGameInstance (Game|GetGameInstance))'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(name, dsl, params=()):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': MAX}, 'graph_name': name})
    for pn, pt in params: call(BT, 'add_function_param', {'graph': {'refPath': MAX + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': True})
    w(MAX + ':' + name, dsl)
have = call(BT, 'list_variables', {'blueprint': {'refPath': MAX}}).get('returnValue') or []
for n in ('GodMode', 'DevOverlay'):
    if n not in have: call(BT, 'add_variable', {'blueprint': {'refPath': MAX}, 'name': n, 'type_name': 'bool'})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False})
SAY = lambda t: '(CallFunction|Notify :Msg "%s" :Seconds 4.0)' % t
fn('HK_Help', '''(fn HK_Help ()
  (CallFunction|Notify :Msg "DEBUG (console, ke * ...):  HK_God  HK_Dev  HK_Overlay  HK_Heal  HK_GiveAll  HK_UnlockLifts  HK_KillAll  HK_Bond n  HK_Taint n  HK_Flag name  HK_Chapter 0-4  HK_Ending" :Seconds 12.0))''')
fn('HK_God', '''(fn HK_God ()
  (Variables|Default|SetGodMode (not (Variables|Default|GetGodMode)))
  (Variables|Default|SetDmgMul (select (Variables|Default|GetGodMode) 0.0 1.0))
  (Variables|Default|SetHealth 100.0) (Variables|Default|SetSanity 100.0)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "OverlayTick" :Time 0.5 :bLooping true)
  (CallFunction|HKLog :Msg (Utilities|String|Append "DEBUG god " (Utilities|String|ToString(Boolean) (Variables|Default|GetGodMode))))
  (CallFunction|Notify :Msg (select (Variables|Default|GetGodMode) "GOD MODE ON" "GOD MODE OFF") :Seconds 3.0))''')
fn('HK_Heal', '''(fn HK_Heal ()
  (Variables|Default|SetHealth 100.0) (Variables|Default|SetSanity 100.0)
  %s)''' % SAY('HEALED'))
fn('HK_GiveAll', '''(fn HK_GiveAll ()
  (Variables|Default|SetHasPistol true)
  (Variables|Default|SetAmmo 12) (Variables|Default|SetReserveAmmo 40) (Variables|Default|SetGels 5) (Variables|Default|SetSedatives 3)
  (Variables|Default|SetParts 5) (Variables|Default|SetChem 5) (Variables|Default|SetBottles 3)
  (CallFunction|HKLog :Msg "DEBUG giveall")
  %s)''' % SAY('ALL ITEMS GIVEN'))
fn('HK_UnlockLifts', '''(fn HK_UnlockLifts ()
  (for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/Floors/BP_FloorLift.BP_FloorLift_C")
    (Class|BPFloorLift|PowerLift :self (Utilities|Casting|CastToBP_FloorLift x)))
  (CallFunction|HKLog :Msg "DEBUG unlocklifts")
  %s)''' % SAY('ALL LIFTS POWERED'))
fn('HK_KillAll', '''(fn HK_KillAll ()
  (for x (Actor|GetAllActorsOfClass "/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone_C")
    (Class|BPHollowDrone|DroneDie :self (Utilities|Casting|CastToBP_HollowDrone x)))
  (CallFunction|HKLog :Msg "DEBUG killall")
  %s)''' % SAY('ALL HOLLOWS DOWN'))
fn('HK_Bond', '''(fn HK_Bond (Value)
  (Variables|Default|SetBond Value)
  (CallFunction|Notify :Msg (Utilities|String|Append "BOND " (Utilities|String|ToString(Float) Value)) :Seconds 3.0))''', params=[('Value', 'float')])
fn('HK_Taint', '''(fn HK_Taint (Value)
  (Variables|Default|SetTaint Value)
  (CallFunction|Notify :Msg (Utilities|String|Append "TAINT " (Utilities|String|ToString(Float) Value)) :Seconds 3.0))''', params=[('Value', 'float')])
fn('HK_Flag', '''(fn HK_Flag (Name)
  (CallFunction|AddFlag :F Name)
  (CallFunction|Notify :Msg (Utilities|String|Append "FLAG ADDED  " Name) :Seconds 3.0))''', params=[('Name', 'string')])
fn('HK_Ending', '(fn HK_Ending ()\n  (CallFunction|ShowEnding))')
LV = ['/Game/HollowKin/Maps/City/Lvl_City', '/Game/HollowKin/Maps/Clinic/Lvl_Clinic', '/Game/HollowKin/Maps/Containment/Lvl_ContainmentWing',
      '/Game/HollowKin/Maps/Wards/Lvl_Wards', '/Game/HollowKin/Maps/Deep/Lvl_DeepLabs']
fn('HK_Chapter', '''(fn HK_Chapter (Index)
  (bind gi %s
    (:then
      (Class|BPHKGameInstance|SetChapterKit :self gi :Index Index)
      %s)
    (:CastFailed)))''' % (GIC, '\n      '.join('(if (== Index %d) (Game|OpenLevel(byName) "%s"))' % (i, l) for i, l in enumerate(LV))), params=[('Index', 'int')])
fn('OverlayTick', '''(fn OverlayTick ()
  (if (Variables|Default|GetGodMode) (Variables|Default|SetHealth 100.0) (Variables|Default|SetSanity 100.0))
  (if (Variables|Default|GetDevOverlay)
    (Development|PrintString :InString (Utilities|String|Append (Utilities|String|Append (Utilities|String|Append (Utilities|String|Append (Utilities|String|Append "DEV  " (CallFunction|FloorLabel))
        (Utilities|String|Append "   pos " (Utilities|String|ToString(Vector) (Transformation|GetActorLocation))))
        (Utilities|String|Append (Utilities|String|Append "   hp " (Utilities|String|ToString(Float) (Variables|Default|GetHealth))) (Utilities|String|Append "  san " (Utilities|String|ToString(Float) (Variables|Default|GetSanity)))))
        (Utilities|String|Append (Utilities|String|Append "   bond " (Utilities|String|ToString(Float) (Variables|Default|GetBond))) (Utilities|String|Append "  taint " (Utilities|String|ToString(Float) (Variables|Default|GetTaint)))))
        (Utilities|String|Append (Utilities|String|Append "   kills " (Utilities|String|ToString(Integer) (Variables|Default|GetRunKills))) (Utilities|String|Append "   flags " (Variables|Default|GetFlags))))
      :bPrintToScreen true :bPrintToLog false :TextColor (Math|Color|MakeColor 0.3 1.0 0.5 1.0) :Duration 0.55)))''')
fn('HK_Overlay', '''(fn HK_Overlay ()
  (Variables|Default|SetDevOverlay (not (Variables|Default|GetDevOverlay)))
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "OverlayTick" :Time 0.5 :bLooping true))''')
fn('HK_Dev', '''(fn HK_Dev ()
  (CallFunction|HKGod)
  (CallFunction|HKUnlockLifts)
  (Variables|Default|SetDevOverlay (Variables|Default|GetGodMode))
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "OverlayTick" :Time 0.5 :bLooping true)
  (CallFunction|Notify :Msg (select (Variables|Default|GetGodMode) "DEVELOPER MODE ON  (ke * HK_Help for commands)" "DEVELOPER MODE OFF") :Seconds 4.0))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
