"""Chains the levels for the 15-floor descent (docs/EXPANSION_PLAN.md):
- Wing (B1) ending with power on -> Lvl_Wards (B2..B8) instead of the Deep Labs (TravelDeep now opens the Wards
  with the "CHAPTER 2 - THE WARDS" card; the Wards' B8 lift opens the Deep Labs).
- BP_Child: Emilia's look and idle, smaller, silent: the other kidnapped children in the B15 isolation cells.
Run with no Fab import in progress (compiles)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
L = '/Game/HollowKin/UI/Menus/WBP_Loading.WBP_Loading_C'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
w(MAX + ':OpenDeepLabs', '(fn OpenDeepLabs ()\n  (Game|OpenLevel(byName) "/Game/HollowKin/Maps/Wards/Lvl_Wards"))')
w(MAX + ':TravelDeep', '''(fn TravelDeep ()
  (bind pc (Game|GetPlayerController 0))
  (CallFunction|StoreCarry)
  (Input|DisableInput :self self :PlayerController pc)
  (CameraFades|StartCameraFade :self (Game|GetPlayerCameraManager 0) :FromAlpha 0.0 :ToAlpha 1.0 :Duration 1.0 :bHoldWhenFinished true)
  (bind card (Utilities|Casting|CastToWBP_Loading (UserInterface|CreateWidget "%s" pc)))
  (Class|WBPLoading|SetupCard :self card :Chapter "CHAPTER 2" :TitleText "THE WARDS" :BodyText "Behind L-03 there is no bed and no girl, only a service lift going down. Seven floors of wards, labs and a morgue, and under them the deep labs. Emilia is at the bottom.")
  (UserInterface|Viewport|AddToViewport card 90)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "OpenDeepLabs" :Time 6.5 :bLooping false))''' % L)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
# BP_Child: copy of BP_Emilia without her lines
CH = '/Game/HollowKin/Blueprints/Props/BP_Child'
if not call(A, 'exists', {'path': CH}).get('returnValue'):
    print(call(A, 'duplicate', {'path': '/Game/HollowKin/Blueprints/Props/BP_Emilia', 'new_path': CH}))
w(CH + '.BP_Child:EventGraph', '(event EventTick (DeltaSeconds))')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': CH + '.BP_Child'}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
