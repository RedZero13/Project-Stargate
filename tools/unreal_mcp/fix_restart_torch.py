"""Death restart reloads the CURRENT level (was hard-coded to the wing, so dying in the City/Deep Labs sent you back
to the start). Torch attaches to the spotlight found by class (the 'Flashlight' tag isn't set yet when ApplyMaxLook runs)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl})
    print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
w(MAX + ':RestartLevel', '''(fn RestartLevel ()
  (Game|OpenLevel(byName) :LevelName (Game|GetCurrentLevelName true)))''')
src = open('torch_and_gun.py').read()
dsl = src.split("w(MAX + ':ApplyMaxLook', '''")[1].split("''')")[0]
dsl = dsl.replace('''(Utilities|Array|Get(acopy) (Actor|GetComponentsByTag "/Script/Engine.ActorComponent" "Flashlight") 0)''',
                  '''(Actor|GetComponentByClass "/Script/Engine.SpotLightComponent")''')
w(MAX + ':ApplyMaxLook', dsl)
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'assets': []}) if False else '')
