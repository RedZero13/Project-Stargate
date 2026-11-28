"""Imports the trophy badges (tools/make_trophies.py) as /Game/HollowKin/UI/Trophies/T_Trophy_<id> (UI texture group)."""
import os
from ui_lib import *
from achievements_data import ACH
TT = 'editor_toolset.toolsets.texture.TextureTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
SRC = os.path.abspath(os.path.join(D, '../../HollowKin/SourceArt/Trophies'))
F = '/Game/HollowKin/UI/Trophies'
paths = []
for i, t, _ in ACH:
    n = 'T_Trophy_' + i; p = F + '/' + n
    if call(A, 'exists', {'path': p}).get('returnValue'): call(A, 'delete', {'path': p})
    r = call(TT, 'import_file', {'folder_path': F, 'asset_name': n, 'source_file': os.path.join(SRC, n + '.png')})
    ok = isinstance(r, dict) and r.get('returnValue') is not None
    if ok:
        setp(p + '.' + n, {'LODGroup': 'TEXTUREGROUP_UI', 'CompressionSettings': 'TC_EditorIcon', 'NeverStream': True, 'MipGenSettings': 'TMGS_NoMipmaps'})
        paths.append(p)
    print(n, ok if ok else str(r)[:200])
print(call(A, 'save_assets', {'asset_paths': paths}))
