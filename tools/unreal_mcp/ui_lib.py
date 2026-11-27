import json,urllib.request
import os
D=os.path.dirname(os.path.abspath(__file__))
SID=open(D+'/sid').read().strip()
def call(toolset,tool,args):
    p={'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'call_tool','arguments':{'toolset_name':toolset,'tool_name':tool,'arguments':args}}}
    r=urllib.request.Request('http://127.0.0.1:8000/mcp',json.dumps(p).encode(),{'Content-Type':'application/json','Accept':'application/json, text/event-stream','Mcp-Session-Id':SID})
    d=json.load(urllib.request.urlopen(r,timeout=120))
    res=d.get('result',d)
    txt=''.join(c.get('text','') for c in res.get('content',[])) if isinstance(res,dict) and 'content' in res else json.dumps(res)
    try: return json.loads(txt)
    except: return txt
U='UMGToolSet.UMGToolSet'; O='editor_toolset.toolsets.object.ObjectTools'
def hexc(h,a=1.0):
    h=h.lstrip('#'); return {'r':int(h[0:2],16)/255,'g':int(h[2:4],16)/255,'b':int(h[4:6],16)/255,'a':a}
# srgb->linear is applied by engine for FLinearColor? values are linear: convert
def lin(c):
    f=lambda v:(v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4)
    return {'r':f(c['r']),'g':f(c['g']),'b':f(c['b']),'a':c['a']}
def col(h,a=1.0): return lin(hexc(h,a))
def setp(ref,vals):
    r=call(O,'set_properties',{'instance':{'refPath':ref},'values':json.dumps(vals)})
    return r
class Wbp:
    def __init__(self,path):
        self.path=path; self.ref={'refPath':path}; self.tree=path+':WidgetTree'; self.count={}
    def add(self,cls,name,parent=None,**props):
        pr={'refPath':self.tree+'.'+parent} if parent else None
        idx=self.count.get(parent,0); self.count[parent]=idx+1
        r=call(U,'AddWidget',{'widgetBlueprint':self.ref,'widgetClass':{'refPath':'/Script/UMG.'+cls},'widgetDisplayName':name,'parentWidget':pr,'childIndex':idx})
        if not isinstance(r,dict) or 'widget' not in r.get('returnValue',{}) if isinstance(r,dict) else True: print('ADD FAIL',name,str(r)[:200]); return None
        w=r['returnValue']; slot=w['slot']['refPath'] if isinstance(w['slot'],dict) else None
        wref=w['widget']['refPath']
        if props: setp(wref,props)
        return wref,slot
    def widget(self,name): return self.tree+'.'+name
