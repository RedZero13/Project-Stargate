"""BP_PhoneCall: opening sequence in Lvl_City (title, controls, Jaz's call) + objective panel set at start and after the call."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
BP = '/Game/HollowKin/Blueprints/Interactables/BP_PhoneCall.BP_PhoneCall'
OBJ1 = 'Answer your phone. Stay on Main Street.'
OBJ2 = "Walk north up Main Street to St. Brigid's Clinic. Its door is under the green light."
DSL = '''(event EventBeginPlay
  (Utilities|FlowControl|Delay 0.5)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0)))
  (if (not (Variables|Default|GetShown))
    (Variables|Default|SetShown true)
    (Class|BPMax|SetObjectiveNote m "%(o1)s")
    (Utilities|FlowControl|Delay 1.0)
    (Class|BPMax|ShowNote m "MILLBROOK  //  11:47 PM  //  SIX DAYS AFTER THE LETTER" 5.0)
    (Utilities|FlowControl|Delay 5.0)
    (Class|BPMax|ShowNote m "WASD  move     Mouse  look     Shift  run     F  flashlight     RMB / Q  aim  (T toggles)     LMB / E  fire     V  punch     P / Esc  pause" 9.0)
    (Utilities|FlowControl|Delay 9.0)
    (Audio|SpawnSound2D "/Game/Interface_And_Item_Sounds/WAV/Ringtone_01.Ringtone_01" 0.7)
    (Class|BPMax|ShowNote m "*  Your phone buzzes.  UNKNOWN NUMBER  *" 3.5)
    (Utilities|FlowControl|Delay 3.5)
    (Class|BPMax|ShowNote m "JAZ:  Max Hunt? Don't hang up. My name is Jaz. I used to work for Project LANTERN." 6.0)
    (Utilities|FlowControl|Delay 6.0)
    (Class|BPMax|ShowNote m "JAZ:  Your sister is alive. Emilia. They never put her in foster care. She's under St. Brigid's clinic, at the end of this street." 8.0)
    (Utilities|FlowControl|Delay 8.0)
    (Class|BPMax|ShowNote m "JAZ:  They're shutting the place down tonight, and they'll erase everything down there. Her too. The front door is open. Go. Now." 8.0)
    (Utilities|FlowControl|Delay 8.0)
    (Class|BPMax|ShowNote m "MAX:  ...Em?   (The line goes dead.)" 4.5)
    (Utilities|FlowControl|Delay 4.5)
    (Class|BPMax|SetObjectiveNote m "%(o2)s")
    (Class|BPMax|ShowNote m "NEW OBJECTIVE  -  top left of the screen. Press E at the clinic door to go inside." 8.0)))''' % {'o1': OBJ1, 'o2': OBJ2}
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': BP + ':EventGraph'}, 'code': DSL}))
