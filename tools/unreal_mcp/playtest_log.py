"""Playtest logging (2026-11-26). Every line starts with "HKLOG|" so it can be pulled out of the game log:
  HKLOG|<game time>|<level>|<x,y,z>|<event>
Written with PrintString (log only, not on screen). Shipping builds strip it; the PLAYTEST build is a Development
build, whose log file is the shareable bug report (see docs/BUILDING.md "Playtest build").
Logged: 2-second state trace (position, health, sanity, ammo, reserve, gels, aiming, torch, objective), every
on-screen message, objective changes, damage, death (+cause: sanity breakdown or health), checkpoints, pause,
lifts, keycards, switch steps (right/wrong), generators, cutscenes, enemies alerting/dying, level starts."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
DR = '/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(bp, name, params, dsl):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt in params:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': True})
    w(bp + ':' + name, dsl)
have = call(BT, 'list_variables', {'blueprint': {'refPath': MAX}}).get('returnValue') or []
for n, t in (('bTraceOn', 'bool'), ('LastObjective', 'string')):
    if n not in have: call(BT, 'add_variable', {'blueprint': {'refPath': MAX}, 'name': n, 'type_name': t})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False})
A = 'Utilities|String|Append'
def cat(*parts):
    """nested Append of DSL string expressions"""
    e = parts[0]
    for p in parts[1:]: e = '(%s %s %s)' % (A, e, p)
    return e
F = 'Utilities|String|ToString(Float)'
fn(MAX, 'HKLog', [('Msg', 'string')], '''(fn HKLog (Msg)
  (Development|PrintString :InString %s :bPrintToScreen false :bPrintToLog true))''' % cat(
    '"HKLOG|"', '(%s (Utilities|Time|GetGameTimeinSeconds))' % F, '"|"', '(Game|GetCurrentLevelName true)', '"|"',
    '(Utilities|String|ToString(Vector) (Transformation|GetActorLocation))', '"|"', 'Msg'))
fn(MAX, 'HKTrace', [], '''(fn HKTrace ()
  (CallFunction|HKLog :Msg %s))''' % cat(
    '"STATE hp="', '(%s (Variables|Default|GetHealth))' % F, '" san="', '(%s (Variables|Default|GetSanity))' % F,
    '" ammo="', '(Utilities|String|ToString(Integer) (Variables|Default|GetAmmo))', '" res="', '(Utilities|String|ToString(Integer) (Variables|Default|GetReserveAmmo))',
    '" gels="', '(Utilities|String|ToString(Integer) (Variables|Default|GetGels))', '" pistol="', '(Utilities|String|ToString(Boolean) (Variables|Default|GetHasPistol))',
    '" aim="', '(Utilities|String|ToString(Boolean) (Variables|Default|GetAiming))', '" torch="', '(Utilities|String|ToString(Boolean) (Variables|Default|GetFlashlightOn))',
    '" dead="', '(Utilities|String|ToString(Boolean) (Variables|Default|GetDead))'))
# objective: log + start the trace once per level
w(MAX + ':SetObjectiveNote', '''(fn SetObjectiveNote (Msg)
  (if (not (Variables|Default|GetTraceOn))
    (Variables|Default|SetTraceOn true)
    (CallFunction|HKLog :Msg "LEVEL START")
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "HKTrace" :Time 2.0 :bLooping true))
  (if (not (Utilities|String|EqualExactly(String) Msg (Variables|Default|GetLastObjective)))
    (Variables|Default|SetLastObjective Msg)
    (CallFunction|HKLog :Msg (Utilities|String|Append "OBJECTIVE " Msg)))
  (Utilities|IsValid (Variables|Default|GetScreenFXRef)
    (:"Is Valid"
      (Class|WBPScreenFX|SetObjective :self (Variables|Default|GetScreenFXRef) :Msg Msg))))''')
w(MAX + ':Notify', '''(fn Notify (Msg Seconds)
  (CallFunction|HKLog :Msg (Utilities|String|Append "MESSAGE " Msg))
  (Utilities|IsValid (Variables|Default|GetScreenFXRef)
    (:"Is Valid"
      (Class|WBPScreenFX|ShowMessage :self (Variables|Default|GetScreenFXRef) :Msg Msg :Seconds Seconds))))''')
w(MAX + ':ApplyHurt', '''(fn ApplyHurt (Amount)
  (if (not (Variables|Default|GetDead))
    (CallFunction|HKLog :Msg %s)
    (Variables|Default|SetHealth (Math|Float|Clamp(Float) (- (Variables|Default|GetHealth) (* Amount (Variables|Default|GetDmgMul))) 0.0 100.0))
    (Variables|Default|SetSanity (Math|Float|Clamp(Float) (- (Variables|Default|GetSanity) (* Amount 0.3)) 0.0 100.0))
    (Variables|Default|SetHurtFlash 1.0)
    (if (<= (Variables|Default|GetHealth) 0.0)
      (CallFunction|Die))))''' % cat('"HURT amount="', '(%s Amount)' % F, '" hp_before="', '(%s (Variables|Default|GetHealth))' % F))
w(MAX + ':Die', '''(fn Die ()
  (bind pc (Game|GetPlayerController 0))
  (if (not (Variables|Default|GetDead))
    (CallFunction|HKLog :Msg (select (Variables|Default|GetBreakdown) "DEATH cause=sanity_breakdown" "DEATH cause=health"))
    (Variables|Default|SetDead true)
    (Input|DisableInput :self self :PlayerController pc)
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "RestartLevel" :Time 3.5 :bLooping false)
    (bind ds (UserInterface|CreateWidget "/Game/HollowKin/UI/Diegetic/WBP_DeathScreen.WBP_DeathScreen_C" pc))
    (UserInterface|Viewport|AddToViewport ds 30)
    (if (Variables|Default|GetBreakdown)
      (Class|WBPDeathScreen|SetBreakdown :self (Utilities|Casting|CastToWBP_DeathScreen ds)))))''')
w(MAX + ':OpenPause', '''(fn OpenPause ()
  (CallFunction|HKLog :Msg "PAUSE open")
  (bind pc (Game|GetPlayerController 0))
  (bind pm (UserInterface|CreateWidget "/Game/HollowKin/UI/Menus/WBP_PauseMenu.WBP_PauseMenu_C" pc))
  (UserInterface|Viewport|AddToViewport pm 20)
  (Game|SetGamePaused true)
  (Input|SetInputModeUIOnly :PlayerController pc :InWidgetToFocus pm :InMouseLockMode "LockAlways")
  (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor true)
  (Class|WBPPauseMenu|SetVitals :self (Utilities|Casting|CastToWBP_PauseMenu pm) :Health (Variables|Default|GetHealth) :Sanity (Variables|Default|GetSanity)))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
# enemies
w(DR + ':DroneDie', '''(fn DroneDie ()
  (Variables|Default|SetDead true)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0)))
  (Class|BPMax|HKLog :self m :Msg (Utilities|String|Append "ENEMY killed " (Utilities|String|ToString(Vector) (Transformation|GetActorLocation))))
  (Collision|SetCollisionEnabled :self (Variables|Character|GetCapsuleComponent) :NewType "NoCollision")
  (Collision|SetCollisionProfileName :self (Variables|Character|GetMesh) :InCollisionProfileName "Ragdoll")
  (Physics|SetSimulatePhysics :self (Variables|Character|GetMesh) :bSimulate true)
  (Actor|SetLifeSpan :self self :InLifespan 15.0))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DR}, 'warnings_as_errors': False}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
