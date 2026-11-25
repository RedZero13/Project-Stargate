"""Puts every music loop (Horror Music kit, Save Room music, HollowKin/Audio/Music) in the engine Music sound class
so the MUSIC volume setting controls it. Saves the assets (Fab packs are local-only)."""
from ui_lib import call
A = 'editor_toolset.toolsets.asset.AssetTools'
paths = []
for folder in ['/Game/Horror_Music_Free_Starter_Kit', '/Game/Save_Room_Music', '/Game/HollowKin/Audio/Music', '/Game/InfinitelyCloseNightmareMusicPack', '/Game/LAMENTSTARTER', '/Game/FreeAtmosGameMusic']:
    for t in ('SoundWave', 'SoundCue'):
        paths += call(A, 'find_assets', {'folder_path': folder, 'name': '', 'asset_type': {'refPath': '/Script/Engine.' + t}})['returnValue']
n = 0
for p in paths:
    obj = p if '.' in p.split('/')[-1] else p + '.' + p.split('/')[-1]
    r = call('editor_toolset.toolsets.object.ObjectTools', 'set_properties', {'instance': {'refPath': obj}, 'values': '{"SoundClassObject": {"refPath": "/Engine/EngineSounds/Music.Music"}, "bLooping": true}' if obj.split('.')[0].endswith(tuple(['Cue'])) is False else '{"SoundClassObject": {"refPath": "/Engine/EngineSounds/Music.Music"}}'})
    n += 1 if r.get('returnValue') else 0
print('music class set on', n, 'of', len(paths))
print(call(A, 'save_assets', {'asset_paths': paths}))
