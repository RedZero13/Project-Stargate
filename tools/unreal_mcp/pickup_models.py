"""World pickups use real item models (the same meshes rendered into the backpack icons, tools/../SourceArt/Items):
0 ammo = ammo case, 1 health gel = salve jar, 2 sedative = dropper bottle, 3 fuse = ceramic cylinder,
4 scrap parts = electronic junk, 5 chemicals = jerry can, 6 glass bottle = vial, 7 drawing = paper, 8 patient file = case folder, 9 L-7 serum = violet vial.
Each is scaled to a readable size, recentred, set on the floor (actor sits 40 cm up) and keeps its coloured glow."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
PU = '/Game/HollowKin/Blueprints/Items/BP_Pickup.BP_Pickup'
HH = '/Game/Horror_Hospital/Meshes/'
# kind: (mesh, scale, x off, y off, colour)
K = {0: ('/Game/Military_Radio/StaticMesh/SM_RadioBattary.SM_RadioBattary', 0.9, 0.0, 16.8, (1.0, 0.75, 0.25)),
     1: (HH + 'SM_Botlle_04_v01.SM_Botlle_04_v01', 2.4, -2.0, 3.7, (0.35, 1.0, 0.55)),
     2: (HH + 'SM_Botlle_02_v01.SM_Botlle_02_v01', 2.8, 0.0, 0.0, (0.45, 0.65, 1.0)),
     3: (HH + 'SM_Botlle_05_v01.SM_Botlle_05_v01', 3.0, 1.0, -1.0, (0.75, 1.0, 0.95)),
     4: (HH + 'SM_Small_Device_02_v01.SM_Small_Device_02_v01', 0.6, 0.0, 0.0, (0.85, 0.75, 0.6)),
     5: (HH + 'SM_Canister_01_v01.SM_Canister_01_v01', 0.55, 0.0, 0.0, (0.8, 0.45, 1.0)),
     6: (HH + 'SM_Botlle_01_v01.SM_Botlle_01_v01', 3.5, 0.3, 0.0, (0.6, 0.9, 0.85)),
     7: (HH + 'SM_Paper_01_v01.SM_Paper_01_v01', 1.3, 0.0, 0.0, (1.0, 0.9, 0.7)),
     8: (HH + 'SM_Book_01_v03.SM_Book_01_v03', 1.4, 0.0, 0.0, (0.55, 0.8, 1.0)),
     9: (HH + 'SM_Botlle_03_v01.SM_Botlle_03_v01', 3.0, 0.0, 0.0, (0.75, 0.2, 1.0))}
def branch(k):
    m, s, ox, oy, c = K[k]
    return '''(Components|StaticMesh|SetStaticMesh :self sm :NewMesh "%s")
      (Transformation|SetRelativeScale3D :self sm :NewScale3D (Math|Vector|MakeVector %s %s %s))
      (Transformation|SetRelativeLocation :self sm :NewLocation (Math|Vector|MakeVector %s %s -38.0))
      (Rendering|Components|Light|SetLightColor :self lt :NewLightColor (Math|Color|MakeColor %s %s %s 1.0))''' % (m, s, s, s, ox * s, oy * s, c[0], c[1], c[2])
body = ''
for k in sorted(K, reverse=True):
    body = '(%s (== kind %d)\n      %s%s)' % ('if' if k == 0 else 'elif', k, branch(k), ('\n      ' + body) if body else '')
dsl = '''(fn ApplyLook ()
  (bind lt (Utilities|Casting|CastToPointLightComponent (Actor|GetComponentByClass :ComponentClass "/Script/Engine.PointLightComponent")))
  (bind sm (Utilities|Casting|CastToStaticMeshComponent (Actor|GetComponentByClass :ComponentClass "/Script/Engine.StaticMeshComponent")))
  (bind kind (Variables|Default|GetPickupKind))
  %s)''' % body
r = call(BT, 'write_graph_dsl', {'graph': {'refPath': PU + ':ApplyLook'}, 'code': dsl})
print('ApplyLook', r)
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': PU}, 'warnings_as_errors': False}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
