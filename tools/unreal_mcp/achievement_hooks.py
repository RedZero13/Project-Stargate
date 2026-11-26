"""Hooks the achievement system (progress_system.py) into gameplay, plus collectibles and rewards.
- BP_Max: Drawings / Files per-run counters (carried between levels), Ach(Id, Title) -> GI Unlock.
- Collect: kind 7 drawing (wing drawings +20 Bond, floor drawings Amount 3 -> +3 Bond), every 5 drawings -> +1 health gel;
  kind 8 patient file (Amount = file number, shows its lore line), every 5 files -> +6 rounds.
- AchTick (run from the 2 s HKTrace): pistol, power, reached Wards / Deep Labs / B15, collectible counts.
- HKLog: "ENDING X" lines unlock that ending and record it (Every Door once all three are seen).
- DroneDie: kill counters, Elite kill. Craft functions: craft counter. Hollow Child: Mercy / Something Darkens."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
GI = '/Game/HollowKin/Blueprints/Systems/BP_HKGameInstance.BP_HKGameInstance'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
DR = '/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone'
HC = '/Game/HollowKin/Blueprints/AI/BP_HollowChild.BP_HollowChild'
from achievements_data import TOTAL_DRAWINGS, TOTAL_FILES
FILES = [  # file number -> lore line (shown when picked up)
    "PATIENT FILE 01 - 'Admitted for observation. Mother told the child is in quarantine. No visits.'",
    "PATIENT FILE 02 - 'Maternity referral: twins, healthy. Flag for the Halvorsen Programme. Inform family of stillbirth.'",
    "PATIENT FILE 03 - 'Subject 11 asks for her brother every night. Increase sedation.'",
    "PATIENT FILE 04 - 'Bed 6 transferred below. Paperwork to read: discharged to family.'",
    "PATIENT FILE 05 - 'X-ray shows bone density rising past adult levels. Subject is seven.'",
    "PATIENT FILE 06 - 'Surgery note: the graft took. The child no longer feels cold. Or pain.'",
    "PATIENT FILE 07 - 'Blood draw HUNT, E. - antibodies unlike anything on record. Priority sample.'",
    "PATIENT FILE 08 - 'Morgue intake: two orderlies. Bite marks. Do not report to the city.'",
    "PATIENT FILE 09 - 'Security memo: a man has been asking about his sister at the front desk. Name: Max Hunt.'",
    "PATIENT FILE 10 - 'Specimen jar 40 moved on its own last night. Night staff refuse B10.'",
    "PATIENT FILE 11 - 'Lab A: the children hum the same song together. None of them were taught it.'",
    "PATIENT FILE 12 - 'Lab B: the adults we changed do not stop. The children still answer to their names.'",
    "PATIENT FILE 13 - 'Observation log: L-03 drew a man with a torch again. She says he is coming.'",
    "PATIENT FILE 14 - 'Final order, Dr. Halvorsen: move L-01 to L-06 to isolation. Seal the lifts if anyone gets past B8.'",
]
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(bp, name, params, dsl):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt in params:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': True})
    w(bp + ':' + name, dsl)
def addvars(bp, vs):
    have = call(BT, 'list_variables', {'blueprint': {'refPath': bp}}).get('returnValue') or []
    for n, t in vs:
        if n not in have: call(BT, 'add_variable', {'blueprint': {'refPath': bp}, 'name': n, 'type_name': t})
    call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False})
addvars(MAX, [('Drawings', 'int'), ('Files', 'int')])
addvars(GI, [('CDrawings', 'int'), ('CFiles', 'int')])
GIC = '(Utilities|Casting|CastToBP_HKGameInstance (Game|GetGameInstance))'
fn(MAX, 'Ach', [('Id', 'string'), ('Title', 'string')], '''(fn Ach (Id Title)
  (bind gi %s
    (:then (Class|BPHKGameInstance|Unlock :self gi :Id Id :Title Title))
    (:CastFailed)))''' % GIC)
fn(MAX, 'AchCraft', [], '''(fn AchCraft ()
  (bind gi %s
    (:then (Class|BPHKGameInstance|AddCraft :self gi))
    (:CastFailed)))''' % GIC)
# ---- carry the per-run counters between levels (same pattern as deep_links.py) ----
F = [('Health', 'float'), ('Sanity', 'float'), ('Bond', 'float'), ('Taint', 'float'),
     ('Ammo', 'int'), ('ReserveAmmo', 'int'), ('Gels', 'int'), ('Sedatives', 'int'), ('Bottles', 'int'), ('Parts', 'int'), ('Chem', 'int'), ('Tapes', 'int'),
     ('Drawings', 'int'), ('Files', 'int')]
store = '\n      '.join('(Class|BPHKGameInstance|SetC%s :self gi :C%s (Variables|Default|Get%s))' % (n, n, n) for n, t in F)
restore = '\n        '.join('(Variables|Default|Set%s (Class|BPHKGameInstance|GetC%s :self gi))' % (n, n) for n, t in F)
w(MAX + ':StoreCarry', '''(fn StoreCarry ()
  (bind gi %s
    (:then
      %s
      (Class|BPHKGameInstance|SetCarryPistol :self gi :bCarryPistol (Variables|Default|GetHasPistol))
      (Class|BPHKGameInstance|SetCarry :self gi :bCarry true))
    (:CastFailed)))''' % (GIC, store))
w(MAX + ':RestoreCarry', '''(fn RestoreCarry ()
  (bind gi %s
    (:then
      (if (Class|BPHKGameInstance|GetCarry :self gi)
        %s
        (Variables|Default|SetHasPistol (Class|BPHKGameInstance|GetCarryPistol :self gi))))
    (:CastFailed)))''' % (GIC, restore))
# ---- Collect ----
N = lambda msg, s=3.0: '(CallFunction|Notify :Msg "%s" :Seconds %s)' % (msg.replace('"', "'"), s)
lore = '"PATIENT FILE"'
for i in range(len(FILES), 0, -1):
    lore = '(select (== Amount %d) "%s" %s)' % (i, FILES[i - 1].replace('"', "'"), lore)
w(MAX + ':Collect', '''(fn Collect (Kind Amount)
  (if (== Kind 0)
    (Variables|Default|SetReserveAmmo (select (> (+ (Variables|Default|GetReserveAmmo) (Math|Float|Round (* Amount (Variables|Default|GetLootMul)))) 40) 40 (+ (Variables|Default|GetReserveAmmo) (Math|Float|Round (* Amount (Variables|Default|GetLootMul))))))
    (elif (== Kind 1)
      (Variables|Default|SetGels (+ (Variables|Default|GetGels) 1))
      %s
      (elif (== Kind 2)
        (Variables|Default|SetSedatives (+ (Variables|Default|GetSedatives) 1))
        %s
        (elif (== Kind 3)
          (Variables|Default|SetFuses (+ (Variables|Default|GetFuses) 1))
          %s
          (elif (== Kind 4)
            (Variables|Default|SetParts (+ (Variables|Default|GetParts) 1))
            %s
            (elif (== Kind 5)
              (Variables|Default|SetChem (+ (Variables|Default|GetChem) 1))
              %s
              (elif (== Kind 6)
                (Variables|Default|SetBottles (+ (Variables|Default|GetBottles) 1))
                %s
                (elif (== Kind 7)
                  (Variables|Default|SetBond (Math|Float|Clamp(Float) (+ (Variables|Default|GetBond) (select (== Amount 3) 3.0 20.0)) 0.0 100.0))
                  (Variables|Default|SetDrawings (+ (Variables|Default|GetDrawings) 1))
                  (CallFunction|HKLog :Msg (Utilities|String|Append "COLLECT drawing " (Utilities|String|ToString(Integer) (Variables|Default|GetDrawings))))
                  (if (or (or (== (Variables|Default|GetDrawings) 5) (== (Variables|Default|GetDrawings) 10)) (== (Variables|Default|GetDrawings) 15))
                    (Variables|Default|SetGels (+ (Variables|Default|GetGels) 1))
                    (CallFunction|Notify :Msg (Utilities|String|Append (Utilities|String|Append "EMILIA'S DRAWING  " (Utilities|String|ToString(Integer) (Variables|Default|GetDrawings))) "/%d.   Tucked inside it: a HEALTH GEL  +1") :Seconds 6.0)
                    (else
                      (CallFunction|Notify :Msg (Utilities|String|Append (Utilities|String|Append "EMILIA'S DRAWING  " (Utilities|String|ToString(Integer) (Variables|Default|GetDrawings))) "/%d.   Crayon: two stick figures holding hands, 'MAX + EM'.") :Seconds 6.0)))
                  (CallFunction|RecordRun)
                  (elif (== Kind 8)
                    (Variables|Default|SetFiles (+ (Variables|Default|GetFiles) 1))
                    (CallFunction|HKLog :Msg (Utilities|String|Append "COLLECT file " (Utilities|String|ToString(Integer) (Variables|Default|GetFiles))))
                    (CallFunction|Notify :Msg %s :Seconds 8.0)
                    (if (or (== (Variables|Default|GetFiles) 5) (== (Variables|Default|GetFiles) 10))
                      (Variables|Default|SetReserveAmmo (+ (Variables|Default|GetReserveAmmo) 6))
                      (CallFunction|ShowNote :Msg (Utilities|String|Append (Utilities|String|Append "PATIENT FILES  " (Utilities|String|ToString(Integer) (Variables|Default|GetFiles))) "/%d.   A security locker code was clipped to them:  +6 ROUNDS") :Seconds 5.0))
                    (CallFunction|RecordRun)))))))))))''' % (
    N('HEALTH GEL  +1     (open your backpack with B to use it)'), N('SEDATIVE  +1     (open your backpack with B to use it)'),
    N('FUSE COLLECTED'), N('SCRAP PARTS  +1     (workbench: I)', 2.5), N('CHEMICALS  +1     (workbench: I)', 2.5),
    N('GLASS BOTTLE  +1     (G throws it to lure Hollows away)', 2.5), TOTAL_DRAWINGS, TOTAL_DRAWINGS, lore, TOTAL_FILES))
fn(MAX, 'RecordRun', [], '''(fn RecordRun ()
  (bind gi %s
    (:then (Class|BPHKGameInstance|RecordCollectibles :self gi :Drawings (Variables|Default|GetDrawings) :Files (Variables|Default|GetFiles)))
    (:CastFailed)))''' % GIC)
# ---- AchTick ----
fn(MAX, 'AchTick', [], '''(fn AchTick ()
  (bind lvl (Game|GetCurrentLevelName true))
  (if (Variables|Default|GetHasPistol) (CallFunction|Ach :Id "first_light" :Title "First Light"))
  (if (Variables|Default|GetPowerOn) (CallFunction|Ach :Id "lights_on" :Title "Lights On"))
  (if (Utilities|String|Contains lvl "Wards") (CallFunction|Ach :Id "going_down" :Title "Going Down"))
  (if (Utilities|String|Contains lvl "Deep") (CallFunction|Ach :Id "deep_labs" :Title "The Real Program"))
  (if (and (Utilities|String|Contains lvl "Deep") (Utilities|String|Contains (Variables|Default|GetLastObjective) "B15"))
    (CallFunction|Ach :Id "isolation" :Title "L-03"))
  (if (>= (Variables|Default|GetDrawings) 5) (CallFunction|Ach :Id "drawings_5" :Title "Crayon Trail"))
  (if (>= (Variables|Default|GetDrawings) %d) (CallFunction|Ach :Id "drawings_all" :Title "The Whole Gallery"))
  (if (>= (Variables|Default|GetFiles) 5) (CallFunction|Ach :Id "files_5" :Title "Paper Trail"))
  (if (>= (Variables|Default|GetFiles) %d) (CallFunction|Ach :Id "files_all" :Title "Archivist")))''' % (TOTAL_DRAWINGS, TOTAL_FILES))
# HKTrace: same state line as playtest_log.py, then AchTick
A_ = 'Utilities|String|Append'
def cat(*parts):
    e = parts[0]
    for p in parts[1:]: e = '(%s %s %s)' % (A_, e, p)
    return e
Fl = 'Utilities|String|ToString(Float)'
w(MAX + ':HKTrace', '''(fn HKTrace ()
  (CallFunction|HKLog :Msg %s)
  (CallFunction|AchTick))''' % cat(
    '"STATE hp="', '(%s (Variables|Default|GetHealth))' % Fl, '" san="', '(%s (Variables|Default|GetSanity))' % Fl,
    '" ammo="', '(Utilities|String|ToString(Integer) (Variables|Default|GetAmmo))', '" res="', '(Utilities|String|ToString(Integer) (Variables|Default|GetReserveAmmo))',
    '" gels="', '(Utilities|String|ToString(Integer) (Variables|Default|GetGels))', '" pistol="', '(Utilities|String|ToString(Boolean) (Variables|Default|GetHasPistol))',
    '" aim="', '(Utilities|String|ToString(Boolean) (Variables|Default|GetAiming))', '" torch="', '(Utilities|String|ToString(Boolean) (Variables|Default|GetFlashlightOn))',
    '" dead="', '(Utilities|String|ToString(Boolean) (Variables|Default|GetDead))',
    '" drawings="', '(Utilities|String|ToString(Integer) (Variables|Default|GetDrawings))', '" files="', '(Utilities|String|ToString(Integer) (Variables|Default|GetFiles))'))
# HKLog: print line + ending hook
w(MAX + ':HKLog', '''(fn HKLog (Msg)
  (Development|PrintString :InString %s :bPrintToScreen false :bPrintToLog true)
  (if (Utilities|String|Contains Msg "ENDING ")
    (bind gi %s
      (:then
        (if (Utilities|String|Contains Msg "ENDING HOMECOMING")
          (Class|BPHKGameInstance|Unlock :self gi :Id "end_home" :Title "Homecoming")
          (Class|BPHKGameInstance|AddEnding :self gi :Name "HOMECOMING"))
        (if (Utilities|String|Contains Msg "ENDING KIN")
          (Class|BPHKGameInstance|Unlock :self gi :Id "end_kin" :Title "Kin")
          (Class|BPHKGameInstance|AddEnding :self gi :Name "KIN"))
        (if (Utilities|String|Contains Msg "ENDING LANTERN")
          (Class|BPHKGameInstance|Unlock :self gi :Id "end_lantern" :Title "Lantern")
          (Class|BPHKGameInstance|AddEnding :self gi :Name "LANTERN")))
      (:CastFailed))))''' % (cat(
    '"HKLOG|"', '(%s (Utilities|Time|GetGameTimeinSeconds))' % Fl, '"|"', '(Game|GetCurrentLevelName true)', '"|"',
    '(Utilities|String|ToString(Vector) (Transformation|GetActorLocation))', '"|"', 'Msg'), GIC))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
# ---- crafting ----
SND = '(Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Flick_Switch_03.Flick_Switch_03" 0.8)'
w(MAX + ':CraftAmmo', '''(fn CraftAmmo ()
  (if (and (>= (Variables|Default|GetParts) 2) (>= (Variables|Default|GetChem) 1))
    (Variables|Default|SetParts (- (Variables|Default|GetParts) 2))
    (Variables|Default|SetChem (- (Variables|Default|GetChem) 1))
    (Variables|Default|SetReserveAmmo (+ (Variables|Default|GetReserveAmmo) 6))
    %s
    (CallFunction|AchCraft)))''' % SND)
w(MAX + ':CraftTonic', '''(fn CraftTonic ()
  (if (>= (Variables|Default|GetChem) 2)
    (Variables|Default|SetChem (- (Variables|Default|GetChem) 2))
    (Variables|Default|SetSedatives (+ (Variables|Default|GetSedatives) 1))
    %s
    (CallFunction|AchCraft)))''' % SND)
w(MAX + ':CraftGel', '''(fn CraftGel ()
  (if (and (>= (Variables|Default|GetParts) 1) (>= (Variables|Default|GetChem) 1))
    (Variables|Default|SetParts (- (Variables|Default|GetParts) 1))
    (Variables|Default|SetChem (- (Variables|Default|GetChem) 1))
    (Variables|Default|SetGels (+ (Variables|Default|GetGels) 1))
    %s
    (CallFunction|AchCraft)))''' % SND)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
# ---- kills ----
w(DR + ':DroneDie', '''(fn DroneDie ()
  (Variables|Default|SetDead true)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0)))
  (Class|BPMax|HKLog :self m :Msg (Utilities|String|Append "ENEMY killed " (Utilities|String|ToString(Vector) (Transformation|GetActorLocation))))
  (Collision|SetCollisionEnabled :self (Variables|Character|GetCapsuleComponent) :NewType "NoCollision")
  (Collision|SetCollisionProfileName :self (Variables|Character|GetMesh) :InCollisionProfileName "Ragdoll")
  (Physics|SetSimulatePhysics :self (Variables|Character|GetMesh) :bSimulate true)
  (Actor|SetLifeSpan :self self :InLifespan 15.0)
  (bind gi %s
    (:then (Class|BPHKGameInstance|AddKill :self gi :Elite (Actor|ActorHasTag :self self :Tag "Elite")))
    (:CastFailed)))''' % GIC)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DR}, 'warnings_as_errors': False}))
# ---- Hollow Child ----
w(HC + ':EventGraph', '''(event EventTick (DeltaSeconds)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then
      (if (and (< (Transformation|GetDistanceTo self m) 200.0) (not (Class|BPMax|GetAiming :self m)))
        (Class|BPMax|SetBond :self m :Bond (+ (Class|BPMax|GetBond :self m) 40.0))
        (Class|BPMax|ShowNote :self m :Msg "You lower the gun. The child stops shaking, touches your hand, and is gone. It trusted you." :Seconds 5.0)
        (Class|BPMax|Ach :self m :Id "mercy" :Title "Mercy")
        (Actor|DestroyActor self)))
    (:CastFailed)))''')
w(HC + ':EventGraph', '''(event Game|Damage|EventAnyDamage (Damage DamageType InstigatedBy DamageCauser)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then
      (Class|BPMax|SetTaint :self m :Taint (+ (Class|BPMax|GetTaint :self m) 40.0))
      (Class|BPMax|ShowNote :self m :Msg "It was only a child. Something inside you darkens." :Seconds 5.0)
      (Class|BPMax|Ach :self m :Id "darkened" :Title "Something Darkens")
      (Actor|DestroyActor self))
    (:CastFailed)))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': HC}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
