"""Clicks the first Slate widget whose snapshot line contains the given text (editor UI automation)."""
import sys, json, re
from ui_lib import call
S = 'SlateInspectorToolset.SlateInspectorToolset'
t = call(S, 'Snapshot', {'ref': '', 'maxDepth': 40})['returnValue']
for l in t.split('\n'):
    if sys.argv[1] in l and 'ref=' in l:
        r = re.search(r'ref=(\w+)', l).group(1)
        print(l.strip()[:120], call(S, 'Click', {'ref': r}))
        break
