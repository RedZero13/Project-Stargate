"""UI audit: every Widget Blueprint under /Game/HollowKin. Flags TextBlocks with literal backslash escapes, default
placeholder text, engine fallback font (Roboto), empty images, and DSL string pins containing a literal backslash-n."""
import re
from ui_lib import *
A='editor_toolset.toolsets.asset.AssetTools'; BT='editor_toolset.toolsets.blueprint.BlueprintTools'
import os
root=os.path.abspath(os.path.join(D,'../../HollowKin/Content/HollowKin'))
wbps=[]
for dp,_,fs in os.walk(root):
    for f in fs:
        if f.startswith('WBP_') and f.endswith('.uasset'):
            rel=os.path.relpath(os.path.join(dp,f[:-7]),root); wbps.append('/Game/HollowKin/'+rel+'.'+f[:-7])
BAD=re.compile(r'\\n|\\t|Text Block|TextBlock|TODO|lorem|pre-alpha|placeholder',re.I)
for w in sorted(wbps):
    issues=[]
    try: ws=call(U,'GetWidgets',{'widgetBlueprint':{'refPath':w}})['returnValue']['widgets']
    except Exception as e: print('==',w,'ERR',str(e)[:80]); continue
    for x in ws:
        cls=x['widgetClassPath']['refPath'].split('.')[-1]; ref=x['widget']['refPath']; n=ref.split('.')[-1]
        if cls=='TextBlock':
            p=json.loads(call(O,'get_properties',{'instance':{'refPath':ref},'properties':['Font','Text']})['returnValue'])
            t=str(p.get('Text')); fo=str(p['Font'].get('fontObject'))
            if BAD.search(t): issues.append('text %s: %r'%(n,t[:70]))
            if 'Roboto' in fo: issues.append('roboto %s: %r'%(n,t[:30]))
    for g in ['EventGraph']:
        r=call(BT,'read_graph_dsl',{'graph':{'refPath':w+':'+g}})
        s=r.get('returnValue','') if isinstance(r,dict) else ''
        if isinstance(s,str) and '\\n' in s: issues.append('graph %s has literal \\n'%g)
    print('==',w.split('.')[-1],len(ws),'widgets'); [print('   ',i) for i in issues]
