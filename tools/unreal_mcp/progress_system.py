"""Achievements, collectibles and rewards (2026-11-26).
- BP_ProgressSave (slot "HollowKinProgress", kept across runs and endings): AchList "|id|id|" (not "Unlocked": clashes with BP_FloorLift.bUnlocked in the DSL), Endings "|LANTERN|KIN|",
  Kills, Crafts, BestDrawings, BestFiles.
- BP_HKGameInstance: LoadProgress, Unlock(Id, Title) (saves + "ACHIEVEMENT UNLOCKED" toast + sound), AddKill(Elite),
  AddCraft, AddEnding(Name), Count(Id) helpers.
- BP_Max: Drawings / Files counters (per run), Collect rewritten: kind 7 drawing (+Amount Bond, every 5 -> +1 health gel),
  kind 8 patient file (lore note, every 5 -> +6 rounds); AchTick (from the 2 s trace) unlocks location/state achievements.
See ACH below for the list (also shown on the main-menu ACHIEVEMENTS screen)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
GI = '/Game/HollowKin/Blueprints/Systems/BP_HKGameInstance.BP_HKGameInstance'
PS = '/Game/HollowKin/Blueprints/Systems/BP_ProgressSave.BP_ProgressSave'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
from achievements_data import ACH, TOTAL_DRAWINGS, TOTAL_FILES
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split('.')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
def fn(bp, name, params, dsl):
    call(BT, 'add_function_graph', {'blueprint': {'refPath': bp}, 'graph_name': name})
    for pn, pt, inp in params:
        call(BT, 'add_function_param', {'graph': {'refPath': bp + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': inp})
    w(bp + ':' + name, dsl)
def addvars(bp, vs):
    have = call(BT, 'list_variables', {'blueprint': {'refPath': bp}}).get('returnValue') or []
    for n, t in vs:
        if n not in have: call(BT, 'add_variable', {'blueprint': {'refPath': bp}, 'name': n, 'type_name': t})
    call(BT, 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False})
if not call(A, 'exists', {'path': PS.split('.')[0]}).get('returnValue'):
    print(call(BT, 'create', {'folder_path': '/Game/HollowKin/Blueprints/Systems', 'asset_name': 'BP_ProgressSave', 'asset_type': {'refPath': '/Script/Engine.SaveGame'}}))
call(BT, 'remove_variable', {'blueprint': {'refPath': PS}, 'name': 'Unlocked'})
addvars(PS, [('AchList', 'string'), ('Endings', 'string'), ('Kills', 'int'), ('Crafts', 'int'), ('BestDrawings', 'int'), ('BestFiles', 'int')])
have = call(BT, 'list_variables', {'blueprint': {'refPath': GI}}).get('returnValue') or []
if 'Progress' not in have:
    call(BT, 'add_object_variable', {'blueprint': {'refPath': GI}, 'name': 'Progress', 'object_class': {'refPath': PS.replace('.BP_ProgressSave', '.BP_ProgressSave_C')}})
call(BT, 'compile_blueprint', {'blueprint': {'refPath': GI}, 'warnings_as_errors': False})
PSC = '/Game/HollowKin/Blueprints/Systems/BP_ProgressSave.BP_ProgressSave_C'
fn(GI, 'LoadProgress', [], '''(fn LoadProgress ()
  (Utilities|IsValid (Variables|Default|GetProgress)
    (:"Is Not Valid"
     (if (SaveGame|DoesSaveGameExist "HollowKinProgress" 0)
      (Variables|Default|SetProgress (Utilities|Casting|CastToBP_ProgressSave (SaveGame|LoadGameFromSlot "HollowKinProgress" 0)))
      (else (Variables|Default|SetProgress (Utilities|Casting|CastToBP_ProgressSave (SaveGame|CreateSaveGameObject "%s"))))))))''' % PSC)
fn(GI, 'SaveProgress', [], '''(fn SaveProgress ()
  (SaveGame|SaveGameToSlot (Variables|Default|GetProgress) "HollowKinProgress" 0))''')
fn(GI, 'Unlock', [('Id', 'string', True), ('Title', 'string', True)], '''(fn Unlock (Id Title)
  (CallFunction|LoadProgress)
  (bind p (Variables|Default|GetProgress))
  (bind key (Utilities|String|Append (Utilities|String|Append "|" Id) "|"))
  (if (not (Utilities|String|Contains (Class|BPProgressSave|GetAchList :self p) key))
    (Class|BPProgressSave|SetAchList :self p :AchList (Utilities|String|Append (Class|BPProgressSave|GetAchList :self p) key))
    (CallFunction|SaveProgress)
    (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Special_Powerup_03.Special_Powerup_03" 0.8)
    (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
      (:then
        (Class|BPMax|Notify :self m :Msg (Utilities|String|Append "ACHIEVEMENT UNLOCKED   //   " Title) :Seconds 4.0)
        (Class|BPMax|HKLog :self m :Msg (Utilities|String|Append "ACHIEVEMENT " Id)))
      (:CastFailed))))''')
fn(GI, 'AddKill', [('Elite', 'bool', True)], '''(fn AddKill (Elite)
  (CallFunction|LoadProgress)
  (bind p (Variables|Default|GetProgress))
  (Class|BPProgressSave|SetKills :self p :Kills (+ (Class|BPProgressSave|GetKills :self p) 1))
  (CallFunction|SaveProgress)
  (if (>= (Class|BPProgressSave|GetKills :self p) 10) (CallFunction|Unlock :Id "kills_10" :Title "Orderly"))
  (if (>= (Class|BPProgressSave|GetKills :self p) 50) (CallFunction|Unlock :Id "kills_50" :Title "Exterminator"))
  (if Elite (CallFunction|Unlock :Id "elite" :Title "The Bigger They Are")))''')
fn(GI, 'AddCraft', [], '''(fn AddCraft ()
  (CallFunction|LoadProgress)
  (bind p (Variables|Default|GetProgress))
  (Class|BPProgressSave|SetCrafts :self p :Crafts (+ (Class|BPProgressSave|GetCrafts :self p) 1))
  (CallFunction|SaveProgress)
  (if (>= (Class|BPProgressSave|GetCrafts :self p) 5) (CallFunction|Unlock :Id "crafter" :Title "Field Medic")))''')
fn(GI, 'AddEnding', [('Name', 'string', True)], '''(fn AddEnding (Name)
  (CallFunction|LoadProgress)
  (bind p (Variables|Default|GetProgress))
  (bind key (Utilities|String|Append (Utilities|String|Append "|" Name) "|"))
  (if (not (Utilities|String|Contains (Class|BPProgressSave|GetEndings :self p) key))
    (Class|BPProgressSave|SetEndings :self p :Endings (Utilities|String|Append (Class|BPProgressSave|GetEndings :self p) key))
    (CallFunction|SaveProgress))
  (bind e (Class|BPProgressSave|GetEndings :self p))
  (if (and (and (and (Utilities|String|Contains e "|LANTERN|") (Utilities|String|Contains e "|KIN|")) (and (Utilities|String|Contains e "|HOMECOMING|") (Utilities|String|Contains e "|HOLLOW|"))) (and (Utilities|String|Contains e "|SIXDOORS|") (Utilities|String|Contains e "|LULLABY|")))
    (CallFunction|Unlock :Id "all_endings" :Title "Every Door")))''')
fn(GI, 'RecordCollectibles', [('Drawings', 'int', True), ('Files', 'int', True)], '''(fn RecordCollectibles (Drawings Files)
  (CallFunction|LoadProgress)
  (bind p (Variables|Default|GetProgress))
  (if (> Drawings (Class|BPProgressSave|GetBestDrawings :self p)) (Class|BPProgressSave|SetBestDrawings :self p :BestDrawings Drawings))
  (if (> Files (Class|BPProgressSave|GetBestFiles :self p)) (Class|BPProgressSave|SetBestFiles :self p :BestFiles Files))
  (CallFunction|SaveProgress))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': GI}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))
