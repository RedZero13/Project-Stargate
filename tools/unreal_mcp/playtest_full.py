"""Full-game automated playtest in Play-In-Editor, one continuous session across level travel:
City (phone call -> clinic door) -> Clinic G/F1 (keycard, switch order) -> Containment Wing B1 (fuses, drawings,
Hollow Child, pistol, breaker, power door, exit) -> Wards B2-B8 (each floor's gate) -> Deep Labs B9 (generator) ->
B10-B14 -> B15 (cutscenes, Emilia, ending). Teleports stand in for walking; damage is off so the route itself is tested.
Writes a PASS/FAIL report to playtest_report.json and screenshots to the scratchpad. Open Lvl_City in the editor first.
usage: python3 playtest_full.py"""
import json, time, subprocess, os, re
from ui_lib import call
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
E = 'EditorToolset.EditorAppToolset'
SP = os.environ.get('HK_SHOTS', '/tmp/hk_playtest/')
os.makedirs(SP, exist_ok=True)
POS = json.load(open('route_positions.json'))
FOLDER = {'Lvl_City': 'City', 'Lvl_Clinic': 'Clinic', 'Lvl_ContainmentWing': 'Containment', 'Lvl_Wards': 'Wards', 'Lvl_DeepLabs': 'Deep'}
report = []
def log(step, ok, info=''):
    report.append({'step': step, 'ok': ok, 'info': info}); print(('PASS ' if ok else 'FAIL ') + step, info, flush=True)
def pie(ref, lv): return {'refPath': ref.replace('/%s.%s' % (lv, lv), '/UEDPIE_0_%s.%s' % (lv, lv))}
def maxref(lv): return {'refPath': '/Game/HollowKin/Maps/%s/UEDPIE_0_%s.%s:PersistentLevel.BP_Max_C_0' % (FOLDER[lv], lv, lv)}
def current_level():
    for lv in FOLDER:
        r = call(AT, 'get_actor_transform', {'actor': maxref(lv)})
        if isinstance(r, dict) and isinstance(r.get('returnValue'), dict): return lv
    return None
def wait_level(lv, timeout=25):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if current_level() == lv: time.sleep(2.5); return True
        time.sleep(1)
    return False
def prop(ref, names):
    r = call(O, 'get_properties', {'instance': ref, 'properties': names})
    try: return json.loads(r['returnValue'])
    except Exception: return {}
def setp(ref, vals): call(O, 'set_properties', {'instance': ref, 'values': json.dumps(vals)})
def where(lv):
    r = call(AT, 'get_actor_transform', {'actor': maxref(lv)})
    return r['returnValue']['location'] if isinstance(r, dict) and isinstance(r.get('returnValue'), dict) else {'x': 0, 'y': 0, 'z': 0}
def tp(lv, x, y, z, yaw=0):
    call(AT, 'set_actor_transform', {'actor': maxref(lv), 'xform': {'location': {'x': x, 'y': y, 'z': z}, 'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}}, 'worldspace': True})
def god(lv): setp(maxref(lv), {'DmgMul': 0.0, 'Sanity': 100.0, 'Health': 100.0})
def shot(name): subprocess.run(['./cap2.sh', SP + name + '.png'], capture_output=True)
def items(lv, cls, label_prefix=None):
    return [i for i in POS[lv] if i['cls'] == cls and (label_prefix is None or i['label'].startswith(label_prefix))]
SI = 'SlateInspectorToolset.SlateInspectorToolset'
def press_e(n=1):
    for _ in range(n): call(SI, 'PressKey', {'key': 'E'}); time.sleep(0.35)
def solve_breakers(lv, L):
    bs = sorted(items(lv, 'BP_Breaker', L + '_'), key=lambda b: b['label'])
    on = [bool(prop(pie(b['ref'], lv), ['On']).get('On')) for b in bs]
    n = len(bs)
    for mask in range(1 << n):
        st = list(on)
        for i in range(n):
            if mask >> i & 1:
                for j in (i - 1, i, i + 1):
                    if 0 <= j < n: st[j] = not st[j]
        if all(st): break
    else: return 'no solution from %s' % on
    for i, b in enumerate(bs):
        if mask >> i & 1: tp(lv, b['x'], b['y'] + 90, b['z'] - 30); time.sleep(0.6); press_e()
    return 'start %s presses %s' % (on, [i for i in range(n) if mask >> i & 1])
def solve_dials(lv, L, code):
    ds = sorted(items(lv, 'BP_Dial', L + '_'), key=lambda d: d['label'])
    info = []
    for i, d in enumerate(ds):
        dig = int(prop(pie(d['ref'], lv), ['Digit']).get('Digit', 0))
        k = (int(code[i]) - dig) % 10
        tp(lv, d['x'], d['y'] + 90, d['z'] - 30); time.sleep(0.6); press_e(k)
        info.append(int(prop(pie(d['ref'], lv), ['Digit']).get('Digit', -1)))
    return 'code %s dials now %s' % (code, info)
def objective(lv): return prop(maxref(lv), ['LastObjective']).get('LastObjective', '')

call(E, 'StartPIE', {'options': {}}); time.sleep(6)
try:
  exec(compile(r'''
lv = 'Lvl_City'
log('City loads', current_level() == lv)
god(lv); shot('01_city_start')
# phone call -> objective to walk to the clinic
t0 = time.time(); ok = False
while time.time() - t0 < 75:
    o = objective(lv)
    if 'Clinic' in o or 'clinic' in o: ok = True; break
    time.sleep(3)
log('Phone call finishes and sets clinic objective', ok, objective(lv)[:90]); shot('02_city_after_call')
door = items(lv, 'BP_LevelDoor')[0]
tp(lv, door['x'] - 120, door['y'], door['z'] + 20, 0)
log('Clinic door -> Lvl_Clinic', wait_level('Lvl_Clinic', 30))
# ---------- stacked-floor maps ----------
def run_floors(lv, labels):
    god(lv)
    for L in labels:
        lift = next((i for i in POS[lv] if i['cls'] == 'BP_FloorLift' and i['label'] == L + '_Lift'), None)
        if not lift: log('%s lift exists' % L, False); continue
        lp = pie(lift['ref'], lv); gate = prop(lp, ['Gate', 'Code', 'NextLevel'])
        # arrival: Max should be on this floor now (except the first floor of a map, reached by level start)
        god(lv)
        if gate.get('Gate') == 1:
            k = items(lv, 'BP_Keycard', L + '_')
            if k: tp(lv, k[0]['x'], k[0]['y'], k[0]['z'] + 20); time.sleep(1.5)
        elif gate.get('Gate') == 2:
            sw = {}
            for s in items(lv, 'BP_SeqSwitch', L + '_'):
                sw[prop(pie(s['ref'], lv), ['Idx']).get('Idx')] = s
            for c in gate.get('Code', ''):
                s = sw.get(int(c))
                if s: tp(lv, s['x'], s['y'], s['z'] + 95); time.sleep(1.3); tp(lv, s['x'], 0, s['z'] + 100); time.sleep(0.5)
        elif gate.get('Gate') == 3:
            g = items(lv, 'BP_FloorGenerator', L + '_')
            if g: tp(lv, g[0]['x'] - 180, g[0]['y'], g[0]['z'] + 100); time.sleep(1.5)
        info = ''
        if gate.get('Gate') == 4: info = solve_breakers(lv, L); time.sleep(1)
        elif gate.get('Gate') == 5: info = solve_dials(lv, L, gate.get('Code', '000')); time.sleep(1)
        unlocked = prop(lp, ['bUnlocked']).get('bUnlocked')
        if gate.get('Gate') == 6:   # clinic G lift is out of order by design; the stairs lead to F1
            log('%s lift out of order (by design)' % L, not unlocked); continue
        log('%s gate solved (gate %s)' % (L, gate.get('Gate')), bool(unlocked), (info or objective(lv))[:110])
        shot('f_%s' % L)
        tp(lv, lift['x'] - 200, lift['y'], lift['z'] + 90); time.sleep(2.0)    # walk up: doors open
        tp(lv, lift['x'] + 170, lift['y'], lift['z'] + 90)                      # step into the cabin
        if gate.get('NextLevel'):
            return True
        time.sleep(9)
        here = where(lv)
        log('%s lift ride' % L, here['z'] < lift['z'] - 500 or here['z'] > lift['z'] + 500, 'z %.0f' % here['z'])
    return False
lv = 'Lvl_Clinic'
run_floors(lv, ['G', 'F1'])
log('F1 lift -> Containment Wing', wait_level('Lvl_ContainmentWing', 30))
# ---------- Containment Wing ----------
lv = 'Lvl_ContainmentWing'; god(lv); shot('10_wing_start')
m = maxref(lv)
b0 = prop(m, ['Bond', 'Taint'])
for p in items(lv, 'BP_Pickup'):
    if p.get('PickupKind') in (3, 7):
        tp(lv, p['x'], p['y'], p['z'] + 30); time.sleep(1.2)
st = prop(m, ['Fuses', 'Bond'])
log('Wing: both fuses collected', st.get('Fuses', 0) >= 2, str(st))
log('Wing: drawings raise Bond', st.get('Bond', 0) > b0.get('Bond', 0), 'bond %s -> %s' % (b0.get('Bond'), st.get('Bond')))
g = items(lv, 'BP_GunPickup')
if g:
    tp(lv, g[0]['x'] - 100, g[0]['y'], g[0]['z'] + 100); time.sleep(6)
    log('Wing: pistol picked up', bool(prop(m, ['bHasPistol']).get('bHasPistol')))
hc = items(lv, 'BP_HollowChild')
if hc:
    setp(m, {'Bond': 0.0}); bb = prop(m, ['Bond']).get('Bond', 0)
    tp(lv, hc[0]['x'] - 150, hc[0]['y'], hc[0]['z'] + 100); time.sleep(2)
    ba = prop(m, ['Bond']).get('Bond', 0)
    log('Wing: sparing the Hollow Child adds Bond (+40)', ba >= bb + 39, 'bond %s -> %s' % (bb, ba))
br = items(lv, 'BP_BreakerPanel')
if br:
    tp(lv, br[0]['x'] - 80, br[0]['y'], br[0]['z'] + 50); time.sleep(2)
    log('Wing: breaker restores power', bool(prop(m, ['bPowerOn']).get('bPowerOn')))
shot('11_wing_power')
et = items(lv, 'BP_EndingTrigger')
if et:
    tp(lv, et[0]['x'] - 60, et[0]['y'], et[0]['z']); time.sleep(1)
log('Wing exit -> Lvl_Wards', wait_level('Lvl_Wards', 30))
lv = 'Lvl_Wards'
log('Carry-over keeps pistol into Wards', bool(prop(maxref(lv), ['bHasPistol']).get('bHasPistol')))
run_floors(lv, ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'])
log('B8 lift -> Deep Labs', wait_level('Lvl_DeepLabs', 30))
lv = 'Lvl_DeepLabs'; god(lv); time.sleep(16)        # B9 arrival cutscene
shot('20_deep_start')
gen = next(i for i in POS[lv] if i['label'] == 'B9_Generator')
tp(lv, gen['x'] - 180, gen['y'], gen['z'] + 100); time.sleep(1.5)
lift9 = next(i for i in POS[lv] if i['label'] == 'B9_Lift')
log('B9 generator powers lift', bool(prop(pie(lift9['ref'], lv), ['bUnlocked']).get('bUnlocked')))
tp(lv, lift9['x'] - 200, 0, lift9['z'] + 10); time.sleep(7.5)
log('B9 lift -> B10', where(lv)['z'] < -1500, 'z %.0f' % where(lv)['z'])
run_floors(lv, ['B10', 'B11', 'B12', 'B13', 'B14'])
god(lv); bond = prop(maxref(lv), ['Bond', 'Taint'])
cs = next(i for i in POS[lv] if i['label'] == 'CS_B15_Children')
tp(lv, cs['x'], 0, cs['z'] + 10, 0); time.sleep(20); shot('30_b15_children')
em = next(i for i in POS[lv] if i['label'] == 'CS_B15_Emilia')
tp(lv, em['x'], em['y'], em['z'] + 10, 90 if em['y'] < 0 else -90); time.sleep(22); shot('31_emilia')
etr = next(i for i in POS[lv] if i['label'] == 'B15_EndingTrigger')
tp(lv, etr['x'], etr['y'], etr['z']); time.sleep(4); shot('32_ending')
exp = 'Homecoming' if bond.get('Bond', 0) >= 70 and bond.get('Taint', 0) < 40 else ('Kin' if bond.get('Bond', 0) >= 40 else 'Lantern')
log('Ending reached at B15', bool(prop(maxref(lv), ['bDead']).get('bDead')), 'bond %s taint %s -> expected %s' % (bond.get('Bond'), bond.get('Taint'), exp))
''', 'route', 'exec'))
except Exception as e:
    import traceback; traceback.print_exc(); log('script error', False, repr(e)[:200])
finally:
    call(E, 'StopPIE', {})
json.dump(report, open('playtest_report.json', 'w'), indent=1)
print('PASSED %d / %d' % (sum(1 for r in report if r['ok']), len(report)))
