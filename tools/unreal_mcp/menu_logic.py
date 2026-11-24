import json,urllib.request,sys
BPT='editor_toolset.toolsets.blueprint.BlueprintTools'; UM='UMGToolSet.UMGToolSet'
def call(ts,tool,args):
    SID=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'sid')).read().strip()
    p={'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'call_tool','arguments':{'toolset_name':ts,'tool_name':tool,'arguments':args}}}
    r=urllib.request.Request('http://127.0.0.1:8000/mcp',json.dumps(p).encode(),{'Content-Type':'application/json','Accept':'application/json, text/event-stream','Mcp-Session-Id':SID})
    d=json.load(urllib.request.urlopen(r,timeout=120)); res=d['result']; t=''.join(c.get('text','') for c in res['content'])
    try: return json.loads(t)
    except: return t
def fn(bp,name,dsl,params=()):
    call(BPT,'add_function_graph',{'blueprint':{'refPath':bp},'graph_name':name})
    print(name,call(BPT,'write_graph_dsl',{'graph':{'refPath':f'{bp}:{name}'},'code':dsl}))
def wire(bp,button,fname,y):
    """bind Button.OnClicked to a call of function fname"""
    r=call(UM,'BindToEventProperty',{'widgetBlueprint':{'refPath':bp},'eventName':'OnClicked','propertyName':button,'propertyClass':{'refPath':'/Script/UMG.Button'}})
    ev=r['returnValue'] if isinstance(r,dict) else None
    print('bind',button,str(r)[:200])
    return ev
def connect_clicks(bp,mapping):
    g={'refPath':f'{bp}:EventGraph'}
    evs=call(BPT,'find_nodes',{'graph':g,'title':'Clicked'})['returnValue']
    infos=call(BPT,'get_node_infos',{'nodes':evs})['returnValue']
    y=0
    for n in infos:
        tid=n['type_id']
        for b,f in mapping.items():
            if f'({b})' in tid:
                node=n['node']
                cf=call(BPT,'create_node',{'graph':g,'type_id':f'CallFunction|{f}','pos':{'x':500,'y':y}})['returnValue']
                y+=250
                r=call(BPT,'connect_pins',{'output_pin':{'direction':'EGPD_Output','index_id':1,'node':node},'input_pin':{'direction':'EGPD_Input','index_id':0,'node':cf}})
                print(b,'->',f,r)
    print(call(BPT,'compile_blueprint',{'blueprint':{'refPath':bp},'warnings_as_errors':False}))
