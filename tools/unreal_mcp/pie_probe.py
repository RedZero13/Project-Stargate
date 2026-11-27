"""Small PIE probe for manual tests in Lvl_DeepLabs (or another level via HK_LEVEL=Folder/Lvl_X).
usage: pie_probe.py start | stop | tp <label> [dy] | get <Prop,Prop> <label>..."""
import sys, os, time
from ui_lib import call
S='editor_toolset.toolsets.scene.SceneTools'; AT='editor_toolset.toolsets.actor.ActorTools'; O='editor_toolset.toolsets.object.ObjectTools'; E='EditorToolset.EditorAppToolset'
folder, lvl = os.environ.get('HK_LEVEL', 'Deep/Lvl_DeepLabs').split('/')
LV='/Game/HollowKin/Maps/%s/UEDPIE_0_%s.%s:PersistentLevel.' % (folder, lvl, lvl)
M={'refPath':LV+'BP_Max_C_0'}
def find(label):
    for a in call(S,'find_actors',{'name':label,'tag':'','collision_channels':[]})['returnValue']:
        if a['refPath'].split('.')[-1] and True: return a
def pie(a): return {'refPath':a['refPath'].replace('/%s.%s' % (lvl, lvl),'/UEDPIE_0_%s.%s' % (lvl, lvl))}
cmd=sys.argv[1]
if cmd=='start': call(E,'StartPIE',{'options':{}}); time.sleep(8); print('started')
elif cmd=='stop': call(E,'StopPIE',{})
elif cmd=='tp':
    t=call(AT,'get_actor_transform',{'actor':find(sys.argv[2])})['returnValue']['location']
    dy=float(sys.argv[3]) if len(sys.argv)>3 else 0
    call(AT,'set_actor_transform',{'actor':M,'xform':{'location':{'x':t['x'],'y':t['y']+dy,'z':t['z']+40},'rotation':{'pitch':0,'yaw':0,'roll':0}},'worldspace':True}); print('at',t)
elif cmd=='get':
    for lab in sys.argv[3:]:
        ref = M if lab == 'Max' else pie(find(lab))
        print(lab, call(O,'get_properties',{'instance':ref,'properties':sys.argv[2].split(',')}).get('returnValue'))
