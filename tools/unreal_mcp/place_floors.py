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
    'G': "St. Brigid's ground floor. It looks like a normal clinic: bright, clean, chairs in rows. Too clean. Nobody has sat here in days. The lift at the east end is out of order; the stairs are at the west end of the corridor.",
    'F1': "First floor, maternity and the NICU. The beds are made. Every IV drip is still running into empty beds. A child's drawing is taped to the nurse station glass. The service lift at the east end goes down to the basements.",
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
GATE_OVERRIDE = {'G': 'blocked', 'B4': 'dial', 'B6': 'breakers', 'B8': 'dial', 'B11': 'breakers', 'B13': 'dial'}   # puzzles2.py
for f_ in floors: f_['gate'] = GATE_OVERRIDE.get(f_['label'], f_['gate'])
BRK = F + 'BP_Breaker.BP_Breaker'; DIAL = F + 'BP_Dial.BP_Dial'
def inside(r, x, y, m=70):
    return min(max(x, r['x0'] + m), r['x1'] - m), min(max(y, r['y0'] + m), r['y1'] - m)
def breaker_start(rng):   # 4 breakers in a row, a press flips itself and its neighbours; pick a start needing >= 2 presses
    import itertools
    while True:
        s = [rng.random() < 0.5 for _ in range(4)]
        if all(s): continue
        best = min(sum(c) for c in itertools.product([0, 1], repeat=4)
                   if all(s[i] ^ (sum(c[j] for j in range(4) if abs(i - j) <= 1) % 2 == 1) for i in range(4)))
        if best >= 2: return s
for k, fl in enumerate(floors):
    L = fl['label']; z = fl['z']; rooms = fl['rooms']
    nxt = floors[k + 1] if k + 1 < len(floors) else None
    ax, ay, az = fl['arrival']
    if fl.get('lift_w'):
        wx, wy, wz = fl['lift_w']
        put(F + 'BP_FloorLift.BP_FloorLift', '%s_ArrivalLift' % L, wx, wy, wz, yaw=180, props={'Label': L + 'W', 'Arrival': True, 'Gate': 0})
    if m == 'clinic' and L == 'F1':
        st = next(c for c in fl['cores'] if c['id'] == 'StairW')
        put(HINT, '%s_HintIntro' % L, st['x1'] - 60, st['y1'] - 120, z + 100, props={'Message': INTRO['F1']})
        a = put(B + 'Interactables/BP_Cutscene.BP_Cutscene', 'CS_F1_Wrong', st['x1'] - 60, -100, z + 100, folder='Story', props={
            'Radius': 200.0, 'Hold': 4.5, 'CamOffset': {'x': -300, 'y': -200, 'z': 120}, 'LookOffset': {'x': 1500, 'y': 0, 'z': 60},
            'Line1': "The first floor. Every light is on. Every bed is made. Every IV drip is still running into an empty bed.",
            'Line2': "MAX:  Where is everyone? ...Emilia was brought here. I saw the ambulance.", 'Voice2': {'refPath': '/Game/HollowKin/Audio/VO/VO_max_f1.VO_max_f1'},
            'Line3': "Far down the corridor, a small figure stands in the dark doorway of the NICU. When you blink, it is gone.",
            'Objective': "F1: the service lift at the east end goes down to the basements. Find the switch order and step on the three floor switches."})
        call(AT, 'add_tag', {'actor': a, 'tag': 'Cutscene'}) if a else None
    else:
        put(HINT, '%s_HintIntro' % L, (ax + 150) if m == 'clinic' else 420, ay, z + 100, props={'Message': INTRO.get(L, fl['name'])})
    if fl['gate'] != 'ending':
        lx, ly, lz = fl['lift']
        gate = {'keycard': 1, 'switches': 2, 'power': 3, 'breakers': 4, 'dial': 5, 'blocked': 6}.get(fl['gate'], 0)
        props = {'Label': L, 'Gate': gate}
        OBJ = {'keycard': ": find this floor's KEYCARD (a glowing red card, usually in the far rooms), then take the lift at the east end.",
               'switches': ": read the drawing that gives the switch order, then step on floor switches I, II, III in that order. The lift is at the east end.",
               'power': ": the lift has no power. Find the dead generator in the plant room or store and restart it.",
               'breakers': ": the breakers have tripped. Find the breaker panel and get all four green (E flips one and its neighbours).",
               'dial': ": the lift needs a 3-digit code on the counters by the lift. Three notes on this floor each give one digit.",
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
        rng2 = random.Random(sum(map(ord, L)) + 17)     # separate RNG so the old floors keep their layouts
        if gate == 5:
            code = str(rng2.randint(1, 9)) + str(rng2.randint(0, 9)) + str(rng2.randint(0, 9)); props['Code'] = code
        put(F + 'BP_FloorLift.BP_FloorLift', '%s_Lift' % L, lx, ly, z, props=props, tags=('Lift_' + L,))
        if gate == 1:   # keycard in the deepest room on the south side
            r = rooms[-1]; kx, ky = inside(r, r['x'] + 150, r['y'] + r['side'] * 120)
            put(F + 'BP_Keycard.BP_Keycard', '%s_Keycard' % L, kx, ky, z + 95, props={'Label': L})
        elif gate == 2:
            spots = [rooms[0], rooms[-2], rooms[len(rooms) // 2]]
            for i, r in enumerate(spots):
                sx, sy = inside(r, r['x'] - 200, r['y'] - r['side'] * 150, 90)     # B3 bug: a switch used to land inside a wall
                put(F + 'BP_SeqSwitch.BP_SeqSwitch', '%s_Switch%d' % (L, i), sx, sy, z + 2, props={'Label': L, 'Idx': i}, tags=('Seq_' + L,))
            roman = ['I', 'II', 'III']
            note = "A child's drawing pinned to the wall: three stick figures holding hands, numbered %s, %s, %s.  Underneath, in crayon: 'THIS IS THE WAY HOME'." % tuple(roman[i] for i in order)
            r = rooms[1]; put(HINT, '%s_HintOrder' % L, r['x'], r['y'] - r['side'] * 200, z + 100, props={'Message': note})
        elif gate == 4:
            r = next((x for x in rooms if x['type'] in ('plant', 'store', 'storage', 'nurse')), rooms[len(rooms) // 2])
            back = r['y1'] if r['side'] > 0 else r['y0']
            st = breaker_start(rng2)
            for i in range(4):
                put(BRK, '%s_Breaker%d' % (L, i), r['x'] - 105 + i * 70, back - r['side'] * 10, z + 120, yaw=0 if r['side'] > 0 else 180,
                    props={'Label': L, 'Idx': i, 'On': st[i]}, tags=('Brk_' + L,))
            put(HINT, '%s_HintBreakers' % L, r['x'], r['y'], z + 100, props={'Message': "Maintenance tag on the panel: 'Breakers A-D are wired in a chain. Flipping one kicks its neighbours too. All four green = lift power.'  (E flips a breaker.)"})
        elif gate == 5:
            for i in range(3):
                put(DIAL, '%s_Dial%d' % (L, i), lx - 400 + i * 75, -388, z + 110, yaw=180, props={'Label': L, 'Idx': i, 'Digit': 0})   # lift room, north wall
            words = ['FIRST', 'SECOND', 'THIRD']
            for i, r in enumerate([rooms[1], rooms[len(rooms) // 2], rooms[-2]]):
                put(HINT, '%s_HintDigit%d' % (L, i), r['x'] + 60, r['y'], z + 100, props={'Message': "A bed chart with one number circled in red marker:  '%s DIGIT  -  %s'.  Someone wanted the lift code remembered." % (words[i], code[i])})
        elif gate == 3:
            r = next((x for x in rooms if x['type'] in ('plant', 'store', 'storage')), rooms[-1])
            gx, gy = inside(r, r['x'] + 220, r['y'] + r['side'] * 60, 110)
            put(F + 'BP_FloorGenerator.BP_FloorGenerator', '%s_Generator' % L, gx, gy, z + 2, yaw=90, props={'Label': L})
    if fl['gate'] == 'ending':   # B15: Emilia in the middle north cell, the other five children in the rest
        isos = [r for r in rooms if r['type'] == 'iso']
        em_id = isos[len(isos) // 2]['id'] if isos else None
        for i, r in enumerate(rooms):
            if r['type'] != 'iso': continue
            cx, cy = r['x'], r['y'] - r['side'] * 40
            if r['id'] == em_id:
                put(B + 'Props/BP_Emilia.BP_Emilia', '%s_Emilia' % L, cx, cy, z + 2, yaw=90 if r['side'] < 0 else 270, folder='Ending')
                put(B + 'Interactables/BP_EndingTrigger.BP_EndingTrigger', '%s_EndingTrigger' % L, r['x'] + 120, r['y'] + r['side'] * 60, z + 100, folder='Ending')   # beside Emilia, well past her cutscene at the door
            else:
                put(B + 'Props/BP_Child.BP_Child', '%s_Child%d' % (L, i), cx, cy, z + 2, yaw=90 if r['side'] < 0 else 270,
                    scale=random.choice([0.85, 0.9, 0.95]), folder='Ending')
        put(HINT, '%s_HintChildren' % L, rooms[0]['x'], 0, z + 100, props={'Message': "Five other children, L-01 to L-06 on the cell doors. They watch you without blinking. Emilia's cell is in the middle."})
    # enemies: 2 Hollows (3 on deep floors), the last deep floors get an Elite
    n_en = 0 if fl['gate'] == 'ending' else 0 if m == 'clinic' else 3
    for i in range(n_en):
        r = rooms[(k + 2 * i + 1) % len(rooms)]
        nurse = (i == 0) and (m == 'wards' or k % 2 == 0)
        dx, dy = r.get('door', (r['x'], r['y']))
        put(DR, '%s_%s%d' % (L, 'UndeadNurse' if nurse else 'Hollow', i), dx, dy + r['side'] * 130, z + 120, folder='Enemies', tags=(('Nurse',) if nurse else ()))
    if m == 'deep' and L in ('B12', 'B14'):
        r = rooms[1]; dx, dy = r.get('door', (r['x'], r['y']))
        put(DR, '%s_Experiment' % L, dx, dy + r['side'] * 160, z + 120, scale=1.25, tags=('Elite', L + 'Exp'), folder='Enemies')
    # dead staff / soldiers: the clinic only has one dead nurse; the basements are where the guards fell
    nb = 1 if m == 'clinic' else 5 if m == 'wards' else 6
    for i in range(nb):
        r = rooms[(k + i * 2) % len(rooms)]
        guard = m != 'clinic' and i % 2 == 0
        cls = SOL if guard else B + 'Props/BP_DeadNurse.BP_DeadNurse'
        put(cls, '%s_Dead%s%d' % (L, 'Guard' if guard else 'Nurse', i), r['x'] + random.randint(-150, 150), r['y'] + r['side'] * random.randint(-100, 60), z,
            yaw=random.randint(0, 359), props={'PoseAnim': {'refPath': AN + POSES[(k + i) % len(POSES)] + '.' + POSES[(k + i) % len(POSES)]}}, folder='Dressing')
    # pickups: ammo, gel/sedative, crafting parts
    loot = [(0, 6), (1 if k % 2 == 0 else 2, 40), (4, 1), (5, 1)]
    for i, (kind, amt) in enumerate(loot):
        r = rooms[(k + i) % len(rooms)]
        put(PU, '%s_Pickup%d' % (L, i), r['x'] + random.randint(-250, 250), r['y'] + r['side'] * random.randint(100, 220), z + 40, props={'PickupKind': kind, 'Amount': amt}, folder='Pickups')
    if L in ('B3', 'B7', 'B11', 'B13'):   # another Hollow Child: lower the gun (+Bond) or hurt it (+Taint)
        r = rooms[(k + 4) % len(rooms)]
        put(B + 'AI/BP_HollowChild.BP_HollowChild', '%s_HollowChild' % L, r['x'], r['y'], z + 100, folder='Enemies')
    if m != 'clinic' and k % 2 == 0 and fl['gate'] != 'ending':   # L-7 serum: full heal, +15 Taint
        r = rooms[(k + 6) % len(rooms)]
        put(PU, '%s_Serum' % L, r['x'] + 90, r['y'] - r['side'] * 60, z + 40, props={'PickupKind': 9, 'Amount': 1}, folder='Pickups')
    if fl['gate'] == 'ending':
        put(F + 'BP_CellConsole.BP_CellConsole', '%s_CellConsole' % L, rooms[0]['x'] + 250, -165, z, yaw=180, folder='Ending')
        put(HINT, '%s_HintConsole' % L, rooms[0]['x'] + 250, 0, z + 100, props={'Message': "CELL RELEASE CONSOLE.  Every lock needs its patient's release code. Halvorsen's staff kept them in the patient files."})
    if m != 'clinic':   # evacuation plan in the lift lobby: walking up to it adds this floor to the map (M)
        put(F + 'BP_MapBoard.BP_MapBoard', '%s_MapBoard' % L, 420, -390, z + 110, yaw=180, props={'Label': L}, folder='Story')
    # a real door on every room and washroom (E opens it; Hollows open the doors they reach)
    for r in rooms + fl.get('wcs', []):
        d = fl.get('doors', {}).get(r['id'])
        if not d: continue
        put(F + 'BP_Door.BP_Door', '%s_Door_%s' % (L, r['id']), (d[0] + d[2]) / 2, (d[1] + d[3]) / 2, z, folder='Doors',
            props={'Width': float(d[2] - d[0]), 'OpenYaw': 95.0 if r['side'] < 0 else -95.0})
    # collectibles (achievement_hooks.py): one of Emilia's drawings (Amount 3 = +3 Bond) and one numbered patient file per floor
    if fl['gate'] != 'ending':
        fileno = {'clinic': 1, 'wards': 3, 'deep': 10}[m] + k
        r = rooms[(k + 5) % len(rooms)]
        put(PU, '%s_Drawing' % L, r['x'] - 120, r['y'] + r['side'] * 160, z + 40, props={'PickupKind': 7, 'Amount': 3}, folder='Collectibles', tags=('Collectible',))
        r = rooms[(k + 3) % len(rooms)]
        put(PU, '%s_PatientFile' % L, r['x'] + 180, r['y'] + r['side'] * 40, z + 40, props={'PickupKind': 8, 'Amount': fileno}, folder='Collectibles', tags=('Collectible',))
print(call(A, 'save_assets', {'asset_paths': []}))
