"""Gameplay on the stacked floors (run after build_floors.py + floor_gameplay.py, with the level open).
usage: python3 place_floors.py wards     (deep for B10-B15)
Per floor: the lift (gate + transition to the next floor), its puzzle (keycard / 3 switches + the note giving the
order / generator), Hollows, dead staff and soldiers, pickups, hints and ambience. Tag FloorGP (re-runnable)."""
import json, sys, random, os
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
A = 'editor_toolset.toolsets.asset.AssetTools'
B = '/Game/HollowKin/Blueprints/'
F = B + 'Floors/'
m = sys.argv[1] if len(sys.argv) > 1 else 'wards'
floors = json.load(open(os.path.join(os.path.dirname(__file__), 'floors_%s.json' % m)))
random.seed(7 if m == 'wards' else 9)
for old in call(S, 'find_actors', {'name': '', 'tag': 'FloorGP', 'collision_channels': []})['returnValue']:
    call(S, 'remove_from_scene', {'actor': old})
def put(cls, label, x, y, z, yaw=0, scale=1.0, props=None, tags=(), folder='Gameplay'):
    a = call(S, 'add_to_scene_from_asset', {'asset_path': cls, 'name': label, 'xform': {'location': {'x': x, 'y': y, 'z': z},
         'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}, 'scale': {'x': scale, 'y': scale, 'z': scale}}})
    a = a.get('returnValue') if isinstance(a, dict) else None
    if not a: print('FAIL', label, cls); return None
    if props: call(O, 'set_properties', {'instance': a, 'values': json.dumps(props)})
    for t in ('FloorGP',) + tuple(tags): call(AT, 'add_tag', {'actor': a, 'tag': t})
    call(AT, 'set_label', {'actor': a, 'label': label}); call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Floors/' + label.split('_')[0] + '/' + folder})
    return a
DR = B + 'AI/BP_HollowDrone.BP_HollowDrone'; PU = B + 'Items/BP_Pickup.BP_Pickup'; HINT = B + 'Interactables/BP_Hint.BP_Hint'
SOL = B + 'Props/BP_DeadSoldier.BP_DeadSoldier'; AN = '/Game/DeadBodies_Poses_nikoff/Animations/'
POSES = ['AS_DeadBody_Pose_Lie_02', 'AS_DeadBody_Pose_Lie_05', 'AS_DeadBody_Pose_Sit_01', 'AS_DeadBody_Pose_Lie_09', 'AS_DeadBody_Pose_Sit_03', 'AS_DeadBody_Pose_Lie_12']
DEEP_NEXT = '/Game/HollowKin/Maps/Deep/Lvl_DeepLabs'
WING_NEXT = '/Game/HollowKin/Maps/Containment/Lvl_ContainmentWing'
INTRO = {
    'G': "St. Brigid's ground floor. It looks like a normal clinic: bright, clean, chairs in rows. Too clean. Nobody has sat here in days. The staff keycard for the lift will be behind reception or in the offices.",
    'F1': "First floor, the wards. The beds are made. The lights hum. A child's drawing is taped to the nurse station glass. The service lift at the east end is the only way down to the basements.",
    'B2': "Admissions. Halvorsen's front desk for children nobody would come looking for. The lift down is at the far end of the corridor.",
    'B3': "The paediatric ward. Tiny beds. Crayon on the walls. Something hums a nursery tune behind the curtains.",
    'B4': "Radiology. The X-ray machines still have films clipped to them: small ribcages, wrong in ways you can't name.",
    'B5': "Surgery. The power is out. Somewhere on this floor a generator is waiting.",
    'B6': "The pharmacy and blood lab. Racks of labelled blood bags. One label says HUNT, E.",
    'B7': "The morgue. The drawers are not all closed. The dead staff wear Halvorsen badges.",
    'B8': "Security and records. The cameras still watch the floors below. One monitor shows a cell with a girl in it.",
    'B10': "Specimen storage. Jars, tags, and a cold that gets into your teeth.",
    'B11': "Testing Lab A. The chairs have straps sized for children.",
    'B12': "Testing Lab B. Here the experiments stopped being human.",
    'B13': "Observation. Glass, microphones, and logbooks full of children's names.",
    'B14': "The sedation ward. The beds are warm. Whoever was in them was moved down very recently.",
    'B15': "The isolation chambers. Six glass cells. Six children. One of them is Emilia.",
}
for k, fl in enumerate(floors):
    L = fl['label']; z = fl['z']; rooms = fl['rooms']
    nxt = floors[k + 1] if k + 1 < len(floors) else None
    ax, ay, az = fl['arrival']
    put(HINT, '%s_HintIntro' % L, ax + 150, ay, z + 100, props={'Message': INTRO.get(L, fl['name'])})
    if fl['gate'] != 'ending':
        lx, ly, lz = fl['lift']
        gate = {'keycard': 1, 'switches': 2, 'power': 3}.get(fl['gate'], 0)
        props = {'Label': L, 'Gate': gate}
        OBJ = {'keycard': ": find this floor's KEYCARD (a glowing red card, usually in the far rooms), then take the lift at the east end.",
               'switches': ": read the drawing that gives the switch order, then step on floor switches I, II, III in that order. The lift is at the east end.",
               'power': ": the lift has no power. Find the dead generator in the plant room or store and restart it.",
               'ending': ": find Emilia's cell, L-03, in the middle of the north side."}
        if nxt:
            props['NextObjective'] = nxt['label'] + OBJ.get(nxt['gate'], '')
            props.update({'Target': {'x': nxt['arrival'][0], 'y': nxt['arrival'][1], 'z': nxt['arrival'][2]}, 'NextLabel': nxt['label'], 'NextName': nxt['name']})
        elif m == 'wards':
            props.update({'NextLevel': DEEP_NEXT, 'NextLabel': 'B9', 'NextName': 'DEEP LABS'})
        elif m == 'clinic':
            props.update({'NextLevel': WING_NEXT, 'NextLabel': 'B1', 'NextName': 'CONTAINMENT WING'})
        # switch puzzle: code is a permutation of 0,1,2; the note gives it as roman numerals
        if gate == 2:
            order = random.sample([0, 1, 2], 3); props['Code'] = ''.join(str(i) for i in order)
        put(F + 'BP_FloorLift.BP_FloorLift', '%s_Lift' % L, lx, ly, z + 100, props=props, tags=('Lift_' + L,))
        if gate == 1:   # keycard in the deepest room on the south side
            r = rooms[-1]; put(F + 'BP_Keycard.BP_Keycard', '%s_Keycard' % L, r['x'] + 150, r['y'] + r['side'] * 120, z + 95, props={'Label': L})
        elif gate == 2:
            spots = [rooms[0], rooms[-2], rooms[len(rooms) // 2]]
            for i, r in enumerate(spots):
                put(F + 'BP_SeqSwitch.BP_SeqSwitch', '%s_Switch%d' % L if False else '%s_Switch%d' % (L, i), r['x'] - 200, r['y'] - r['side'] * 150, z + 2, props={'Label': L, 'Idx': i}, tags=('Seq_' + L,))
            roman = ['I', 'II', 'III']
            note = "A child's drawing pinned to the wall: three stick figures holding hands, numbered %s, %s, %s.  Underneath, in crayon: 'THIS IS THE WAY HOME'." % tuple(roman[i] for i in order)
            r = rooms[1]; put(HINT, '%s_HintOrder' % L, r['x'], r['y'] - r['side'] * 200, z + 100, props={'Message': note})
        elif gate == 3:
            r = next((x for x in rooms if x['type'] in ('plant', 'store', 'storage')), rooms[-1])
            put(F + 'BP_FloorGenerator.BP_FloorGenerator', '%s_Generator' % L, r['x'] + 220, r['y'] + r['side'] * 60, z + 2, yaw=90, props={'Label': L})
    if fl['gate'] == 'ending':   # B15: Emilia in the middle north cell, the other five children in the rest
        for i, r in enumerate(rooms):
            if r['type'] != 'iso': continue
            cx, cy = r['x'], r['y'] - r['side'] * 40
            if r['id'] == 'N1':
                put(B + 'Props/BP_Emilia.BP_Emilia', '%s_Emilia' % L, cx, cy, z + 2, yaw=90 if r['side'] < 0 else 270, folder='Ending')
                put(B + 'Interactables/BP_EndingTrigger.BP_EndingTrigger', '%s_EndingTrigger' % L, r['x'] + 120, r['y'] + r['side'] * 60, z + 100, folder='Ending')   # beside Emilia, well past her cutscene at the door
            else:
                put(B + 'Props/BP_Child.BP_Child', '%s_Child%d' % (L, i), cx, cy, z + 2, yaw=90 if r['side'] < 0 else 270,
                    scale=random.choice([0.85, 0.9, 0.95]), folder='Ending')
        put(HINT, '%s_HintChildren' % L, rooms[0]['x'], 0, z + 100, props={'Message': "Five other children, L-01 to L-06 on the cell doors. They watch you without blinking. Emilia's cell is in the middle."})
    # enemies: 2 Hollows (3 on deep floors), the last deep floors get an Elite
    n_en = 0 if fl['gate'] == 'ending' else 0 if m == 'clinic' else 2 if m == 'wards' else 3
    for i in range(n_en):
        r = rooms[(k + 2 * i + 1) % len(rooms)]
        nurse = (i == 0) and (m == 'wards' or k % 2 == 0)
        put(DR, '%s_%s%d' % (L, 'UndeadNurse' if nurse else 'Hollow', i), r['x'], r['side'] * 330, z + 120, folder='Enemies', tags=(('Nurse',) if nurse else ()))
    if m == 'deep' and L in ('B12', 'B14'):
        r = rooms[1]; put(DR, '%s_Experiment' % L, r['x'], r['side'] * 340, z + 120, scale=1.25, tags=('Elite',), folder='Enemies')
    # dead staff / soldiers
    for i in range(3):
        r = rooms[(k + i * 2) % len(rooms)]
        put(B + 'Props/BP_DeadNurse.BP_DeadNurse' if i == 1 else SOL, '%s_Dead%s%d' % (L, 'Nurse' if i == 1 else '', i), r['x'] + random.randint(-200, 200), r['y'] + r['side'] * random.randint(-120, 60), z,
            yaw=random.randint(0, 359), props={'PoseAnim': {'refPath': AN + POSES[(k + i) % len(POSES)] + '.' + POSES[(k + i) % len(POSES)]}}, folder='Dressing')
    # pickups: ammo, gel/sedative, crafting parts
    loot = [(0, 6), (1 if k % 2 == 0 else 2, 40), (4, 1), (5, 1)]
    for i, (kind, amt) in enumerate(loot):
        r = rooms[(k + i) % len(rooms)]
        put(PU, '%s_Pickup%d' % (L, i), r['x'] + random.randint(-250, 250), r['y'] + r['side'] * random.randint(100, 220), z + 40, props={'PickupKind': kind, 'Amount': amt}, folder='Pickups')
print(call(A, 'save_assets', {'asset_paths': []}))
