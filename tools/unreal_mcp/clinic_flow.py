"""Clinic flow (2026-11-27): the G lift is out of order, so Max takes the west stairs up to F1, sees that something is
wrong there (cutscene at the top of the stairs), solves the switch puzzle and takes the F1 service lift down to the
basements. Updates WBP_ScreenFX.WingIntro (clinic objective) and the lift locked message for gate 6 (out of order)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
SFX = '/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX'
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': SFX + ':WingIntro'}, 'code': '''(fn WingIntro ()
  (bind lvl (Game|GetCurrentLevelName true))
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0)))
  (if (Utilities|String|Contains lvl "Containment")
    (Class|BPMax|ShowNote m "ST. BRIGID'S  //  B1  //  CONTAINMENT WING.   The service lift brought you down. Somewhere below: Emilia." 7.0)
    (Class|BPMax|RefreshObjective m))
  (if (Utilities|String|Contains lvl "DeepLabs")
    (Class|BPMax|SetObjectiveNote m "B9 DEEP LABS: cross the labs and tunnels to the generator hall. Restart the old generator to power the lift down."))
  (if (Utilities|String|Contains lvl "Wards")
    (Class|BPMax|SetObjectiveNote m "Each floor's lift down is at the east end of the corridor. Find what powers it on this floor."))
  (if (Utilities|String|Contains lvl "Clinic")
    (Class|BPMax|SetObjectiveNote m "Find a way down to the basements. The lift is at the east end of the corridor.")))'''})
print('WingIntro', r)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': SFX}, 'warnings_as_errors': False}))
