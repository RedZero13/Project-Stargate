"""Places the BP_Cutscene vignettes in Lvl_DeepLabs (open it first): B9 arrival, B12 experiment reveal, B15 children,
Emilia reunion. Tag Cutscene (re-runnable)."""
import json
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
CS = '/Game/HollowKin/Blueprints/Interactables/BP_Cutscene.BP_Cutscene'
assert 'Lvl_DeepLabs' in str(call(S, 'get_current_level', {})['returnValue'])
for a in call(S, 'find_actors', {'name': '', 'tag': 'Cutscene', 'collision_channels': []})['returnValue']:
    call(S, 'remove_from_scene', {'actor': a})
fl = {f['label']: f for f in json.load(open('floors_deep.json'))}
def room(label, rid):
    return next(r for r in fl[label]['rooms'] if r['id'] == rid)
def put(label, x, y, z, props):
    a = call(S, 'add_to_scene_from_asset', {'asset_path': CS, 'name': label, 'xform': {'location': {'x': x, 'y': y, 'z': z}}})['returnValue']
    print(label, call(O, 'set_properties', {'instance': a, 'values': json.dumps(props)}))
    call(AT, 'add_tag', {'actor': a, 'tag': 'Cutscene'}); call(AT, 'set_label', {'actor': a, 'label': label})
    call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Cutscenes'})
V = lambda x, y, z: {'x': x, 'y': y, 'z': z}
VO = lambda i: {'refPath': '/Game/HollowKin/Audio/VO/VO_%s.VO_%s' % (i, i)}   # Kokoro voice lines (vo_hookup.py)
# 1) B9 arrival: the lift opens on the Deep Labs
put('CS_B9_Arrival', 450, 0, 100, {'Radius': 300.0, 'Hold': 4.5, 'CamOffset': V(-380, 260, 120), 'LookOffset': V(1600, 0, 40),
    'Line1': "B9. The lift doors grind open on warm, wet air. The emergency lights are the colour of old blood.",
    'Line2': "MAX:  Emilia... if you can hear me, I'm coming. I don't care how deep this goes.", 'Voice2': VO('max_b9'),
    'Line3': "Somewhere past the generator plant, a child is humming the lullaby your mother used to sing.",
    'Objective': "Cross the labs and tunnels to the old generator hall. Restart the generator to power the lift down."})
# 2) B12: the experiment reveal at the door of the room holding the Experiment
r = fl['B12']['rooms'][1]; z = fl['B12']['z']; side = r['side']   # the Experiment's room (place_floors: rooms[1])
put('CS_B12_Experiment', r['door'][0], r['door'][1] - side * 80, z + 100, {'Radius': 240.0, 'Hold': 4.5,
    'CamOffset': V(-260, side * 120, 140), 'LookOffset': V(100, side * 420, 60),
    'Line1': "TESTING LAB B. Through the observation glass: something that used to be a man, stitched to a machine.",
    'Line2': "A clipboard on the door: SUBJECT A-12. RESPONSE TO L-SERIES SERUM: TOTAL. CONTAINMENT: FAILED.",
    'Line3': "MAX:  This is what they were turning the children into.", 'Voice3': VO('max_b12'),
    'Objective': "Avoid the Experiment or bring it down with fuel barrels and shocks. Restart the floor generator."})
# 3) B15: the children in the isolation cells
z = fl['B15']['z']
put('CS_B15_Children', 1250, 0, z + 100, {'Radius': 300.0, 'Hold': 5.0,
    'CamOffset': V(250, 0, 230), 'LookOffset': V(1500, 0, -40),
    'Line1': "B15. ISOLATION. Six glass cells along a white corridor. Six beds. Six children.",
    'Line2': "They don't cry. They watch you. Their pupils are too wide, like the Hollows'.",
    'Line3': "MAX:  It's okay. I'm here to take you home. All of you.", 'Voice3': VO('max_b15'),
    'Objective': "Find Emilia's cell, L-03, in the middle of the north side."})
# 4) Emilia reunion: at her cell door
isos = [x for x in fl['B15']['rooms'] if x['type'] == 'iso']; r = isos[len(isos) // 2]; side = r['side']   # Emilia's cell (place_floors)
put('CS_B15_Emilia', r['door'][0], r['door'][1] - side * 80, z + 100, {'Radius': 230.0, 'Hold': 5.5,
    'CamOffset': V(160, side * 60, 120), 'LookOffset': V(0, side * 420, 70),
    'Line1': "EMILIA:  Max? You came. They told me you'd forgotten me.", 'Voice1': VO('emilia_1'), 'Voice2': VO('emilia_2'),
    'Line2': "EMILIA:  The others are like me now. The lantern in my head is so bright, Max. Don't let them put it out.",
    'Line3': "What you did to get here, and what you became on the way, will decide what happens next.",
    'Objective': "Go to Emilia."})
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
