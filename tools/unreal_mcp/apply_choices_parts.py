"""Re-applies selected parts of choices.py without re-running all of it (Interact, SetObjectiveNote, StartNG).
Refuses to run while Play-In-Editor is active (recompiling BP_Max with a live PIE world crashed the editor)."""
from ui_lib import call
if call('EditorToolset.EditorAppToolset', 'IsPIERunning', {}).get('returnValue'):
    raise SystemExit('PIE is running - stop it first')
s = open('choices.py').read(); lines = s.split('\n')
i = next(k for k, l in enumerate(lines) if l.startswith('def vars_('))
j = i + 1
while lines[j].startswith(' '): j += 1
g = {}; exec('\n'.join(lines[:j]), g)
def block(start, end):
    a = s.index(start); b = s.index(end, a) + len(end); return s[a:b]
exec(block("vars_(MAX, [('IntDist'", "print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))"), g)
exec(block("w(MAX + ':SetObjectiveNote', r", ".replace('\\\\n', '\\n'))"), g)
exec(block("fn(GI, 'StartNG', r", ".replace('\\\\n', '\\n'))"), g)
for bp in (g['MAX'], g['GI']):
    print(bp.split('.')[-1], call(g['BT'], 'compile_blueprint', {'blueprint': {'refPath': bp}, 'warnings_as_errors': False}))
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': [g['MAX'].split('.')[0], g['GI'].split('.')[0]]}))
