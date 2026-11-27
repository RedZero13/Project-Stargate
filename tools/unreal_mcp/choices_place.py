"""Places the choices, their consequences and the New Game+ echoes in every level (run after the floors are built).
usage: python3 choices_place.py      (loads each level in turn; tag Choices, re-runnable)
  City      paramedic: give your gel (Bond, he explains F1) / search him (supplies, Taint; a Hollow paramedic waits on G)
  Clinic F1 nurse Okafor in a locked office: free her (Bond; med cache on B2) / leave her (Taint; she is an undead nurse on B3)
  Wards B4  paediatric medicine: take it (2 gels + sedative) / leave it for the children (Bond; needed for LANTERN LIT)
  Wards B8  wounded guard Hale: bandage him (-1 gel, Bond; ammo cache on B9, his squad holds fire) / take his ammo
            (+12 rounds, Taint; two of his squad hunt you on B9)
  Deep B11  research terminal: send everything to Jaz (alarm: 2 Hollows; endings mention it) / wipe it (Taint -10)
  Deep B14  sedated patients: wake them (Bond; 2 of them have already turned) / let them sleep (Taint)
  NG+ only  Emilia's echoes near F1's nurse, B4's medicine and B11's terminal."""
import json, os
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
B = '/Game/HollowKin/Blueprints/'
CHO = B + 'Interactables/BP_Choice.BP_Choice'; GATE = B + 'Interactables/BP_FlagGate.BP_FlagGate'; EV = B + 'Interactables/BP_StreetEvent.BP_StreetEvent'
PU = B + 'Items/BP_Pickup.BP_Pickup'; DR = B + 'AI/BP_HollowDrone.BP_HollowDrone'
VO = lambda i: {'refPath': '/Game/HollowKin/Audio/VO/VO_%s.VO_%s' % (i, i)}
HERE = os.path.dirname(os.path.abspath(__file__))
FL = {m: {f['label']: f for f in json.load(open(os.path.join(HERE, 'floors_%s.json' % m)))} for m in ('clinic', 'wards', 'deep')}
def room(m, L, *types):
    for t in types:
        for r in FL[m][L]['rooms']:
            if r['type'] == t: return r
    return FL[m][L]['rooms'][1]
def load(path):
    call(A, 'save_assets', {'asset_paths': []})
    call(S, 'load_level', {'level_path': '/Game/HollowKin/Maps/' + path})
    cur = str(call(S, 'get_current_level', {})['returnValue']); assert cur.endswith(path.split('/')[1]), cur
    for a in call(S, 'find_actors', {'name': '', 'tag': 'Choices', 'collision_channels': []})['returnValue']:
        call(S, 'remove_from_scene', {'actor': a})
def put(asset, label, x, y, z, yaw=0, props=None, tags=()):
    a = call(S, 'add_to_scene_from_asset', {'asset_path': asset, 'name': label, 'xform': {'location': {'x': x, 'y': y, 'z': z}, 'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}}})
    a = a.get('returnValue') if isinstance(a, dict) else None
    if not a: print('FAIL', label); return None
    if props: call(O, 'set_properties', {'instance': a, 'values': json.dumps(props)})
    for t in ('Choices',) + tuple(tags): call(AT, 'add_tag', {'actor': a, 'tag': t})
    call(AT, 'set_label', {'actor': a, 'label': label}); call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Choices'})
    return a
def gate(label, x, y, z, tag, need='', forbid=''):
    put(GATE, label, x, y, z, props={'GateTag': tag, 'NeedFlag': need, 'ForbidFlag': forbid})
def echo(label, x, y, z, vo, text):
    put(EV, label, x, y, z, props={'Radius': 380.0, 'Seconds': 5.0, 'Voice': VO(vo), 'Msg': "(A girl's whisper, right beside your ear)  " + text}, tags=('NGEcho_' + label,))
    gate(label + '_Gate', x, y, z, 'NGEcho_' + label, need='NG+')
POSE = lambda p: {'PoseAnim': {'refPath': '/Game/DeadBodies_Poses_nikoff/Animations/%s.%s' % (p, p)}}
# ------------------------------------------------------------ City
load('City/Lvl_City')
put(CHO, 'CH_Paramedic', 7120, -560, 0, props={'Prompt': 'kneel by the paramedic', 'Question': "LEO VARGAS, the badge says. Still breathing. 'I drove her in. Your sister. Three weeks ago... If you see a little girl called Sofi... tell her Daddy's sorry he was late.'  His eyes find the health gel in your hand.",
    'OptA': 'Give him your health gel', 'OptB': 'Search his pockets',
    'ResA': "PARAMEDIC:  'Service lift... first floor. The drawing on the nurse glass... tells you the order.'  He points at the clinic, then he is gone.",
    'ResB': "Gauze, a lighter, a crumpled photo of a little girl. He stops breathing while you look at it.",
    'FlagA': 'paramedic_saved', 'FlagB': 'paramedic_robbed', 'BondA': 10.0, 'TaintB': 8.0, 'GelsA': -1, 'GelsB': 1, 'VoiceA': VO('paramedic'), 'VoiceQ': VO('leo_2')})
# ------------------------------------------------------------ Clinic
load('Clinic/Lvl_Clinic')
g = FL['clinic']['G']; r = room('clinic', 'G', 'cafeteria')
put(DR, 'C_HollowParamedic', r['x'], r['y'], g['z'] + 120, props={}, tags=('C_paramedic', 'Nurse'))
gate('C_HollowParamedic_Gate', r['x'], r['y'], g['z'] + 50, 'C_paramedic', need='paramedic_robbed')
f1 = FL['clinic']['F1']; r = room('clinic', 'F1', 'office', 'suite')
put(CHO, 'CH_Nurse', r['x'], r['y'], f1['z'], props={'Prompt': 'answer the knocking', 'Question': "Knocking from inside the locked office. A woman's voice: 'Please. They locked me in when it started. I'm not one of them. Please.'",
    'OptA': 'Unlock the door', 'OptB': 'Leave her. It could be a trap.',
    'ResA': "NURSE OKAFOR:  'Thank God. There's a med kit in the B2 nurse station, take it. And whatever you do, don't trust the quiet floors.'",
    'ResB': "The knocking follows you down the corridor. Then it stops, all at once.",
    'FlagA': 'nurse_freed', 'FlagB': 'nurse_left', 'BondA': 10.0, 'TaintB': 6.0, 'VoiceA': VO('nurse_okafor')})
echo('Echo_F1', r['x'] - 250, r['y'], f1['z'], 'echo_2', "'The nurse knows the way out. Let her go.'")
# ------------------------------------------------------------ Wards
load('Wards/Lvl_Wards')
b2 = FL['wards']['B2']; r = room('wards', 'B2', 'nurse')
for i, (kind, amt) in enumerate(((1, 1), (1, 1), (0, 12))):
    put(PU, 'C_NurseCache%d' % i, r['x'] - 60 + i * 60, r['y'], b2['z'] + 40, props={'PickupKind': kind, 'Amount': amt}, tags=('C_nursecache',))
gate('C_NurseCache_Gate', r['x'], r['y'], b2['z'], 'C_nursecache', need='nurse_freed')
b3 = FL['wards']['B3']; r = room('wards', 'B3', 'nurse', 'store')
put(DR, 'C_Okafor', r['x'], r['y'], b3['z'] + 120, tags=('C_okafor', 'Nurse'))
gate('C_Okafor_Gate', r['x'], r['y'], b3['z'], 'C_okafor', need='nurse_left')
# Okafor again on B5 (only if she was freed): her confession
b5 = FL['wards']['B5']; r = room('wards', 'B5', 'recovery', 'plant')
put(B + 'Props/BP_DeadNurse.BP_DeadNurse', 'C_OkaforB5', r['x'] + 70, r['y'], b5['z'], yaw=180, props=POSE('AS_DeadBody_Pose_Sit_03'), tags=('C_okaforB5',))
put(CHO, 'CH_OkaforB5', r['x'] - 30, r['y'], b5['z'], props={'Prompt': 'talk to Nurse Okafor', 'VoiceQ': VO('okafor_b5'),
    'Question': "NURSE OKAFOR, hiding behind the recovery beds:  'You came back down. I owe you the truth. I sedated them. Every night, the little ones. They paid for my boy's treatment, and I told myself they were just sick children. Can you forgive that?'",
    'OptA': 'Forgive her', 'OptB': "Tell her you can't",
    'ResA': "OKAFOR:  'Then I'll help you carry them out. Every one of them. I'll be at the bottom when you need me.'",
    'ResB': "OKAFOR:  'No. You're right. I don't deserve it.'  When you look back, she is gone.",
    'FlagA': 'forgave_okafor', 'FlagB': 'condemned_okafor', 'BondA': 10.0, 'TaintB': 5.0, 'VoiceA': VO('okafor_forgive'), 'VoiceB': VO('okafor_condemn')}, tags=('C_okaforB5',))
gate('C_OkaforB5_Gate', r['x'], r['y'], b5['z'], 'C_okaforB5', need='nurse_freed')
# Jaz calls when the Wards begin
put(EV, 'C_JazWards', 400, 0, b2['z'], props={'Radius': 350.0, 'Seconds': 8.0, 'Voice': VO('jaz_wards'),
    'Msg': "JAZ:  'Max, you're in the wards. I wrote the dosing schedules for those children. I need you to know that before you trust anything else I say.'"})
b4 = FL['wards']['B4']; r = room('wards', 'B4', 'records', 'nurse', 'store')
put(CHO, 'CH_Medicine', r['x'], r['y'], b4['z'], props={'Prompt': 'open the medicine cabinet', 'Question': "A cabinet labelled PAEDIATRIC - L-SERIES. Gels, sedatives, small doses. Six names on the shelf tags. One of them is EMILIA.",
    'OptA': 'Take the medicine', 'OptB': 'Leave it for the children',
    'ResA': "You fill your pockets. Two health gels and a sedative. The empty shelf looks wrong.",
    'ResB': "You close the cabinet. Whoever gets them out of here will need it more than you.",
    'FlagA': 'took_meds', 'FlagB': 'left_meds', 'GelsA': 2, 'BondB': 15.0})
echo('Echo_B4', r['x'] - 250, r['y'], b4['z'], 'echo_1', "'Max... the medicine on this floor. Leave it. It's for us.'")
b8 = FL['wards']['B8']; r = room('wards', 'B8', 'security', 'control')
put(B + 'Props/BP_DeadSoldier.BP_DeadSoldier', 'C_GuardHale', r['x'] + 60, r['y'], b8['z'], yaw=90, props=POSE('AS_DeadBody_Pose_Sit_01'))
put(CHO, 'CH_Guard', r['x'] - 40, r['y'], b8['z'], props={'Prompt': 'check the wounded guard', 'Question': "A Halvorsen guard, bleeding from a bite on his arm. SGT. HALE on the badge. He raises his hands. 'You're not one of them. Help me. Please.'",
    'OptA': 'Bandage him (one health gel)', 'OptB': 'Take his ammunition',
    'ResA': "SGT. HALE:  'You're not one of them. Okay. My squad's on B9. I'll tell them to hold fire. Ammo cache by the lift. Go.'",
    'ResB': "You strip his magazines. He swears at you, then reaches for his radio.",
    'FlagA': 'guard_spared', 'FlagB': 'guard_robbed', 'BondA': 5.0, 'GelsA': -1, 'AmmoB': 12, 'TaintB': 10.0, 'VoiceA': VO('guard_hale')})
# ------------------------------------------------------------ Deep Labs
load('Deep/Lvl_DeepLabs')
for i, (kind, amt) in enumerate(((0, 12), (0, 12), (1, 1))):
    put(PU, 'C_HaleCache%d' % i, 700 + i * 60, -250, 140, props={'PickupKind': kind, 'Amount': amt}, tags=('C_halecache',))
gate('C_HaleCache_Gate', 700, -250, 100, 'C_halecache', need='guard_spared')
for i in range(2):
    put(DR, 'C_HaleSquad%d' % i, 1600 + i * 300, 150 - i * 300, 220, props={'Ranged': True}, tags=('C_squad',))
gate('C_HaleSquad_Gate', 1600, 0, 100, 'C_squad', need='guard_robbed')
put(EV, 'C_JazDeep', 600, 0, 0, props={'Radius': 400.0, 'Seconds': 8.0, 'Voice': VO('jaz_deep'),
    'Msg': "JAZ:  'Emilia's cell is L-03. The others are Noor, Theo, Mila, Sofi and Ivy. I gave them names, because nobody else would.'"})
# Hale again on B12 (only if he was spared): turning
b12 = FL['deep']['B12']; r = room('deep', 'B12', 'plant', 'lab', 'testing')
put(B + 'Props/BP_DeadSoldier.BP_DeadSoldier', 'C_HaleB12', r['x'] + 70, r['y'], b12['z'], yaw=270, props=POSE('AS_DeadBody_Pose_Sit_01'), tags=('C_haleB12',))
put(CHO, 'CH_HaleB12', r['x'] - 30, r['y'], b12['z'], props={'Prompt': 'go to Sgt. Hale', 'VoiceQ': VO('hale_b12'),
    'Question': "SGT. HALE, slumped against the wall, grey-lipped:  'Hey. Hunt. Told you I'd hold them off... the bite's spreading. I can feel it in my teeth. I don't want to become one of those things.'",
    'OptA': 'End it quickly', 'OptB': 'Leave him one bullet',
    'ResA': "HALE:  'Thank you. Find your sister.'  One shot. The corridor is very quiet afterwards.",
    'ResB': "HALE:  'One bullet's enough. Go. Whatever's coming down that corridor goes through me first.'  Later, far behind you: a burst of gunfire, a roar, then nothing.",
    'FlagA': 'hale_mercy', 'FlagB': 'hale_stand', 'TaintA': 5.0, 'BondB': 5.0, 'AmmoB': -1, 'KillTagB': 'B12Exp',
    'VoiceA': VO('hale_mercy'), 'VoiceB': VO('hale_stand')}, tags=('C_haleB12',))
gate('C_HaleB12_Gate', r['x'], r['y'], b12['z'], 'C_haleB12', need='guard_spared')
# NG+ only: Jaz tells the truth on B15
b15 = FL['deep']['B15']
put(EV, 'C_JazReveal', 900, 0, b15['z'], props={'Radius': 350.0, 'Seconds': 9.0, 'Voice': VO('jaz_reveal'),
    'Msg': "JAZ:  'My name is Jasmine Halvorsen. Doctor Halvorsen is my father. Every door you've opened tonight... I should have opened years ago.'"}, tags=('C_reveal',))
gate('C_JazReveal_Gate', 900, 0, b15['z'], 'C_reveal', need='NG+')
b11 = FL['deep']['B11']; r = room('deep', 'B11', 'control', 'observe')
put(CHO, 'CH_Terminal', r['x'], r['y'], b11['z'], props={'Prompt': 'use the research terminal', 'Question': "PROJECT LANTERN - FULL ARCHIVE. Names, doses, deaths. Jaz's number is still in your phone.",
    'OptA': 'Send everything to Jaz', 'OptB': 'Wipe it all',
    'ResA': "UPLOAD COMPLETE.  Somewhere above you an alarm starts to scream, and something answers it.",
    'ResB': "The archive is gone. Nobody can ever do this again from these notes. Nobody will ever know, either.",
    'FlagA': 'evidence', 'FlagB': 'wiped', 'SpawnA': 2, 'TaintB': -10.0})
echo('Echo_B11', r['x'] - 250, r['y'], b11['z'], 'echo_3', "'Tell everyone, Max. Send them everything.'")
b14 = FL['deep']['B14']; r = room('deep', 'B14', 'icu', 'isoward')
put(CHO, 'CH_Sedated', r['x'], r['y'], b14['z'], props={'Prompt': 'look at the sedated patients', 'Question': "Adults strapped to the beds, drips still running. Some of them are still people. Some of them are not, any more.",
    'OptA': 'Wake them up', 'OptB': 'Let them sleep',
    'ResA': "You pull the drips. Three of them gasp awake, crying. Two of them sit up without breathing.",
    'ResB': "You leave the drips running. The monitors keep beeping behind you.",
    'FlagA': 'woke', 'FlagB': 'let_sleep', 'BondA': 10.0, 'SpawnA': 2, 'TaintB': 5.0})
print(call(A, 'save_assets', {'asset_paths': []}))
