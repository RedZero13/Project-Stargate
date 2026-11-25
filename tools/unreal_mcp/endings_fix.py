"""Makes all three endings reachable in the slice (GDD 6): sparing the Hollow Child +40 Bond, hurting it +40 Taint;
Emilia's drawings (pickup kind 7) +20 Bond each, three hidden in the wing (tag SliceDrawings).
Homecoming = Bond >= 70 and Taint < 40; Kin = Bond >= 40; Lantern otherwise."""
from ui_lib import call
import json, re
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
HC = '/Game/HollowKin/Blueprints/AI/BP_HollowChild.BP_HollowChild'
print('child', call(BT, 'write_graph_dsl', {'graph': {'refPath': HC + ':EventGraph'}, 'code': '''(event EventTick (DeltaSeconds)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then
      (if (and (< (Transformation|GetDistanceTo self m) 200.0) (not (Class|BPMax|GetAiming :self m)))
        (Class|BPMax|SetBond :self m :Bond (+ (Class|BPMax|GetBond :self m) 40.0))
        (Class|BPMax|ShowNote :self m :Msg "You lower the gun. The child stops shaking, touches your hand, and is gone. It trusted you." :Seconds 5.0)
        (Actor|DestroyActor self)))
    (:CastFailed)))'''}))
print('child dmg', call(BT, 'write_graph_dsl', {'graph': {'refPath': HC + ':EventGraph'}, 'code': '''(event Game|Damage|EventAnyDamage (Damage DamageType InstigatedBy DamageCauser)
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then
      (Class|BPMax|SetTaint :self m :Taint (+ (Class|BPMax|GetTaint :self m) 40.0))
      (Class|BPMax|ShowNote :self m :Msg "It was only a child. Something inside you darkens." :Seconds 5.0)
      (Actor|DestroyActor self))
    (:CastFailed)))'''}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': HC}, 'warnings_as_errors': False}))
# Collect: add kind 7 (drawing)
s = open('inventory_logic.py').read()
s = s.replace("""              (elif (== Kind 6)
                (Variables|Default|SetBottles (+ (Variables|Default|GetBottles) 1))
                %s))))))))''' % (""", """              (elif (== Kind 6)
                (Variables|Default|SetBottles (+ (Variables|Default|GetBottles) 1))
                %s
                (elif (== Kind 7)
                  (Variables|Default|SetBond (+ (Variables|Default|GetBond) 20.0))
                  %s)))))))))''' % (""")
s = s.replace("""    N('GLASS BOTTLE  +1     (G throws it to lure Hollows away)', 2.5)))""", """    N('GLASS BOTTLE  +1     (G throws it to lure Hollows away)', 2.5),
    N("EMILIA'S DRAWING.  Crayon: two stick figures holding hands, 'MAX + EM'. You fold it into your jacket.", 6.0)))""")
open('inventory_logic.py', 'w').write(s)
ns = {}
exec(s[s.index("N = lambda"):s.index("fn('Collect'")], ns)
m = re.search(r"fn\('Collect', '''(.*?)''' % \((.*?)\)\)\nfn\('UseGel'", s, re.S)
print('Collect', call(BT, 'write_graph_dsl', {'graph': {'refPath': '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max:Collect'}, 'code': m.group(1) % eval('(' + m.group(2) + ')', ns)}))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'}, 'warnings_as_errors': False}))
# place drawings
S = 'editor_toolset.toolsets.scene.SceneTools'; AT = 'editor_toolset.toolsets.actor.ActorTools'; O = 'editor_toolset.toolsets.object.ObjectTools'
for old in call(S, 'find_actors', {'name': '', 'tag': 'SliceDrawings', 'collision_channels': []})['returnValue']:
    call(S, 'remove_from_scene', {'actor': old})
for label, x, y in (('PU_Drawing_C3', 3350, 220), ('PU_Drawing_C6', 4350, 1150), ('PU_Drawing_C7', 6150, -1400)):
    a = call(S, 'add_to_scene_from_asset', {'asset_path': '/Game/HollowKin/Blueprints/Items/BP_Pickup.BP_Pickup', 'name': label, 'xform': {'location': {'x': x, 'y': y, 'z': 40}}})['returnValue']
    call(O, 'set_properties', {'instance': a, 'values': json.dumps({'PickupKind': 7, 'Amount': 20})})
    call(AT, 'add_tag', {'actor': a, 'tag': 'SliceDrawings'}); call(AT, 'set_label', {'actor': a, 'label': label})
    call(S, 'set_actor_folder', {'actor': a, 'folder_path': 'Slice/Gameplay'})
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
