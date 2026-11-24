from ui_lib import *
TEAL='5fa39a';DIM='3b4f4c';WHITE='dfe9e6';PANEL='0b0f10';BLUE='6fb7ff';RED='b8323a';AMBER='e0a547'
def mk(w):
    def brush(): return {'drawAs':'Image','imageType':'FullColor','tintColor':{'specifiedColor':{'r':1,'g':1,'b':1,'a':1},'colorUseRule':'UseColor_Specified'}}
    def txt(name,parent,text,size=14,color=WHITE,bold=False,spacing=0,just='Left',a=1.0):
        wref,slot=w.add('TextBlock',name,parent)
        setp(wref,{'text':text,'colorAndOpacity':{'specifiedColor':col(color,a),'colorUseRule':'UseColor_Specified'},'justification':just,'font':{'size':size,'typefaceFontName':'Bold' if bold else 'Regular','letterSpacing':spacing}})
        return wref,slot
    def box(name,parent,color,a,**kw):
        wref,slot=w.add('Border',name,parent); v={'background':brush(),'brushColor':col(color,a)}; v.update(kw); setp(wref,v); return wref,slot
    def cslot(slot,ax,ay,l,t,r,b,alx=0,aly=0):
        f=lambda v:(v[0],v[1]) if isinstance(v,tuple) else (v,v)
        setp(slot,{'layoutData':{'offsets':{'left':l,'top':t,'right':r,'bottom':b},'anchors':{'minimum':{'x':f(ax)[0],'y':f(ay)[0]},'maximum':{'x':f(ax)[1],'y':f(ay)[1]}},'alignment':{'x':alx,'y':aly}}})
    def bslot(slot,pad=None,fill=None,h=None,v=None):
        d={}
        if pad is not None: d['padding']={'left':pad[0],'top':pad[1],'right':pad[2],'bottom':pad[3]}
        if fill is not None: d['size']={'sizeRule':'Fill','value':fill}
        if h: d['horizontalAlignment']=h
        if v: d['verticalAlignment']=v
        if d: setp(slot,d)
    def rule(name,parent,color=TEAL,a=0.35,pad=(0,8,0,12)):
        sb,s=w.add('SizeBox','Sz'+name,parent); setp(sb,{'heightOverride':1,'bOverride_HeightOverride':True}); bslot(s,pad=pad)
        box(name,'Sz'+name,color,a)
    def button(name,parent,label,enabled=True,pad=(0,4,0,4)):
        def img(c,a): return {'drawAs':'Image','imageType':'FullColor','tintColor':{'specifiedColor':col(c,a),'colorUseRule':'UseColor_Specified'},'resourceName':'None','outlineSettings':{'width':0,'cornerRadii':{'x':0,'y':0,'z':0,'w':0},'color':{'specifiedColor':{'r':0,'g':0,'b':0,'a':0},'colorUseRule':'UseColor_Specified'},'roundingType':'FixedRadius','bUseBrushTransparency':False}}
        b,s=w.add('Button',name,parent)
        setp(b,{'widgetStyle':{'normal':img(TEAL,0.0),'hovered':img(TEAL,0.20),'pressed':img(TEAL,0.35),'disabled':img(TEAL,0.0)},'bIsEnabled':enabled})
        bslot(s,pad=pad)
        hb,_=w.add('HorizontalBox',name+'Row',name)
        sz,s2=w.add('SizeBox',name+'Tick',name+'Row'); setp(sz,{'widthOverride':3,'bOverride_WidthOverride':True}); bslot(s2,v='VAlign_Fill')
        box(name+'TickBar',name+'Tick',TEAL if enabled else DIM,0.8 if enabled else 0.3)
        t,s3=txt(name+'Label',name+'Row',label,20,WHITE if enabled else DIM,True,500); bslot(s3,pad=(16,10,16,10),v='VAlign_Center')
        return b
    return brush,txt,box,cslot,bslot,rule,button
