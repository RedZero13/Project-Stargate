"""Automated route test in Play-In-Editor for one stacked-floor map (open it in the editor first).
usage: python3 test_route.py clinic|wards|deep
For every floor: solve the gate like a player would (walk to the keycard / step the switches in the order written on
the note / walk up to the generator), walk into the lift and check Max arrives at the next floor's arrival room.
Prints PASS/FAIL per floor. Uses teleports instead of walking (navigation is tested separately)."""
import sys, json, time, os
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
m = sys.argv[1]
LV = {'clinic': 'Clinic/Lvl_Clinic', 'wards': 'Wards/Lvl_Wards', 'deep': 'Deep/Lvl_DeepLabs'}[m]
lvname = LV.split('/')[-1]
floors = json.load(open(os.path.join(os.path.dirname(__file__), 'floors_%s.json' % m)))
def find(name='', tag=''):
    return call(S, 'find_actors', {'name': name, 'tag': tag, 'collision_channels': []})['returnValue']
def loc(a): return call(AT, 'get_actor_transform', {'actor': a})['returnValue']['location']
def props(a, ps): return json.loads(call(O, 'get_properties', {'instance': a, 'properties': ps})['returnValue'])
def pie(a): return {'refPath': a['refPath'].replace('/%s.%s' % (lvname, lvname), '/UEDPIE_0_%s.%s' % (lvname, lvname))}
plan = []
for k, fl in enumerate(floors):
    L = fl['label']
    lifts = find(tag='Lift_' + L)
    step = {'label': L, 'gate': fl['gate'], 'lift': loc(lifts[0]) if lifts else None, 'lift_actor': lifts[0] if lifts else None, 'spots': []}
    if fl['gate'] == 'keycard':
        step['spots'] = [loc(a) for a in find(name=L + '_Keycard')]
    elif fl['gate'] == 'switches':
        code = props(lifts[0], ['Code'])['Code']
        sw = {props(a, ['Idx'])['Idx']: loc(a) for a in find(tag='Seq_' + L)}
        step['spots'] = [sw[int(c)] for c in code]
    elif fl['gate'] == 'power':
        step['spots'] = [loc(a) for a in find(name=L + '_Generator')]
    plan.append(step)
call('EditorToolset.EditorAppToolset', 'StartPIE', {'options': {}}); time.sleep(6)
M = {'refPath': '/Game/HollowKin/Maps/%s/UEDPIE_0_%s.%s:PersistentLevel.BP_Max_C_0' % (LV.split('/')[0], lvname, lvname)}
def tp(p, dz=100):
    call(AT, 'set_actor_transform', {'actor': M, 'xform': {'location': {'x': p['x'], 'y': p['y'], 'z': p['z'] + dz}, 'rotation': {'pitch': 0, 'yaw': 0, 'roll': 0}}, 'worldspace': True})
# god mode for the automated run (enemies are tested separately)
call(O, 'set_properties', {'instance': M, 'values': json.dumps({'DmgMul': 0.0})})
results = []
for k, st in enumerate(plan):
    if st['gate'] == 'ending' or not st['lift']:
        results.append((st['label'], 'skip (%s)' % st['gate'])); continue
    fl = floors[k]
    call(O, 'set_properties', {'instance': M, 'values': json.dumps({'DmgMul': 0.0, 'Sanity': 100.0, 'Health': 100.0})})
    tp({'x': fl['arrival'][0], 'y': fl['arrival'][1], 'z': fl['arrival'][2] - 100}); time.sleep(1.0)
    for p in st['spots']:
        if st['gate'] == 'power': p = dict(p, x=p['x'] - 180)
        tp(p, 95 if st['gate'] == 'switches' else 60); time.sleep(1.3)
        tp({'x': p['x'], 'y': 0, 'z': p['z']}, 100); time.sleep(0.4)
    unlocked = props(pie(st['lift_actor']), ['bUnlocked'])['bUnlocked']
    tp({'x': st['lift']['x'] - 160, 'y': 0, 'z': st['lift']['z']}, 10); time.sleep(7.5)
    after = loc(M)
    nxt = floors[k + 1]['arrival'] if k + 1 < len(floors) else None
    ok = (nxt is not None and abs(after['z'] - nxt[2]) < 150 and abs(after['x'] - nxt[0]) < 300)
    if nxt is None:
        ok = 'level travel'
    results.append((st['label'], 'unlocked=%s arrived=%s' % (unlocked, ok)))
    print(results[-1], flush=True)
    if nxt is None: break
try: call('EditorToolset.EditorAppToolset', 'StopPIE', {})
except Exception: pass
print(json.dumps(results, indent=1))
