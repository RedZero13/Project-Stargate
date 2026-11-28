"""Replaces the grey greybox stand-ins left on early interactables (found by scan_runtime.py, 2026-11-28).
At BeginPlay (placed copies keep their own saved component values, so template edits do not reach them):
- BP_SaveTerminal: grey 40x40x110 pillar (mostly sunk in the floor) -> anesthesia machine with screens, ~1 m tall
- BP_BreakerPanel / BP_PowerDoor: plain engine-cube slab -> MI_HK_Metal (metal cabinet / security shutter)
- BP_EndingTrigger: the pillar is hidden (the glow stays as the marker)
Only the (empty) BeginPlay event is written; the other events stay as they are. Refuses to run during PIE."""
from ui_lib import call
if call('EditorToolset.EditorAppToolset', 'IsPIERunning', {}).get('returnValue'): raise SystemExit('stop PIE first')
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
I = '/Game/HollowKin/Blueprints/Interactables/'
SMC = '(bind sm (Utilities|Casting|CastToStaticMeshComponent (Actor|GetComponentByClass :ComponentClass "/Script/Engine.StaticMeshComponent")))'
METAL = '(Rendering|Material|SetMaterial :self sm :ElementIndex 0 :Material "/Game/HollowKin/Materials/MI_HK_Metal.MI_HK_Metal")'
LOOK = {
    'BP_SaveTerminal': '''(Components|StaticMesh|SetStaticMesh :self sm :NewMesh "/Game/Horror_Hospital/Meshes/SM_Anesthesia_Machine_01_v01.SM_Anesthesia_Machine_01_v01")
  (Transformation|SetRelativeScale3D :self sm :NewScale3D (Math|Vector|MakeVector 0.6 0.6 0.6))
  (Transformation|SetRelativeLocation :self sm :NewLocation (Math|Vector|MakeVector 0.0 0.0 0.0))''',
    'BP_BreakerPanel': METAL,
    'BP_PowerDoor': METAL,
    'BP_EndingTrigger': '(Rendering|SetVisibility :self sm :bNewVisibility false)',
}
EVENTS = {   # existing events, kept unchanged
    'BP_SaveTerminal': '(event Collision|EventActorBeginOverlap (OtherActor)\n  (CallFunction|TerminalTouched OtherActor))',
    'BP_BreakerPanel': '(event Collision|EventActorBeginOverlap (OtherActor)\n  (CallFunction|BreakerTouched OtherActor))',
    'BP_EndingTrigger': '(event Collision|EventActorBeginOverlap (OtherActor)\n  (CallFunction|EndingTouched OtherActor))',
    'BP_PowerDoor': '(event EventTick (DeltaSeconds)\n  (CallFunction|DoorThink DeltaSeconds))',
}
FN = {'BP_SaveTerminal': 'TerminalLook', 'BP_BreakerPanel': 'BreakerLook', 'BP_PowerDoor': 'ShutterLook', 'BP_EndingTrigger': 'HideMarker'}   # unique names: a shared name resolves to another class
for bp, look in LOOK.items():
    path = I + bp + '.' + bp; fn = FN[bp]
    call(BT, 'add_function_graph', {'blueprint': {'refPath': path}, 'graph_name': fn})
    print(bp, fn, call(BT, 'write_graph_dsl', {'graph': {'refPath': path + ':' + fn}, 'code': '(fn ' + fn + ' ()\n  %s\n  %s)' % (SMC, look)}))
    print(bp, 'events', call(BT, 'write_graph_dsl', {'graph': {'refPath': path + ':EventGraph'}, 'code': '(event EventBeginPlay\n  (CallFunction|%s))' % fn}))
    print('  compile', call(BT, 'compile_blueprint', {'blueprint': {'refPath': path}, 'warnings_as_errors': False}))
    print('  graph:', str(call(BT, 'read_graph_dsl', {'graph': {'refPath': path + ':EventGraph'}}).get('returnValue'))[:400].replace('\n', ' | '))
print(call(A, 'save_assets', {'asset_paths': [I + b for b in LOOK]}))
