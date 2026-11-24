"""Generates HOLLOW KIN logo + item icons into HollowKin/SourceArt (own art, no AI imagery). Run with Pillow."""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT=os.path.join(os.path.dirname(__file__),'..','HollowKin','SourceArt'); os.makedirs(OUT,exist_ok=True)
TEAL=(95,163,154); AMB=(224,165,71); RED=(184,50,58); BLUE=(143,211,255); WHITE=(232,238,236); DARK=(8,12,13)
F=lambda n,s: ImageFont.truetype('/System/Library/Fonts/Supplemental/'+n,s)
def glow(img,blur,strength=1.0):
    a=img.split()[3].filter(ImageFilter.GaussianBlur(blur)); g=Image.new('RGBA',img.size,TEAL+(0,)); g.putalpha(a.point(lambda v:int(v*0.8)))
    return Image.alpha_composite(g,img)
def tracked(d,xy,text,font,fill,track):
    x,y=xy
    for ch in text:
        d.text((x,y),ch,font=font,fill=fill); x+=d.textlength(ch,font=font)+track
    return x
def width(d,text,font,track): return sum(d.textlength(c,font=font)+track for c in text)-track
# ---- logo
W,H=2048,900
logo=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(logo)
cx,cy,r=W//2,185,150
# hollow ring with a gap (the "hollow"), small lantern dot inside
for a0,a1 in((-60,230),):
    d.arc((cx-r,cy-r,cx+r,cy+r),a0,a1,fill=TEAL+(255,),width=14)
d.arc((cx-r+34,cy-r+34,cx+r-34,cy+r-34),110,400,fill=TEAL+(120,),width=5)
d.ellipse((cx-9,cy-9,cx+9,cy+9),fill=AMB+(255,))
d.line((cx,cy+9,cx,cy+r+20),fill=TEAL+(160,),width=3)
f=F('DIN Condensed Bold.ttf',330)
t1='HOLLOW'; t2='KIN'
w1=width(d,t1,f,34); 
y=cy+r+40
tracked(d,((W-w1)//2,y),t1,f,WHITE+(255,),34)
f2=F('DIN Alternate Bold.ttf',70); sub='SURVIVAL HORROR  //  PROJECT LANTERN'
ws=width(d,sub,f2,18)
tracked(d,((W-ws)//2,y+330),sub,f2,TEAL+(230,),18)
# KIN is replaced by hollow-outline treatment appended after HOLLOW? keep single line title 'HOLLOW KIN'
logo=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(logo)
d.arc((cx-r,cy-r,cx+r,cy+r),-60,230,fill=TEAL+(255,),width=14)
d.arc((cx-r+34,cy-r+34,cx+r-34,cy+r-34),110,400,fill=TEAL+(120,),width=5)
d.ellipse((cx-9,cy-9,cx+9,cy+9),fill=AMB+(255,))
title='HOLLOW KIN'; f=F('DIN Condensed Bold.ttf',300); wt=width(d,title,f,40)
tracked(d,((W-wt)//2,y-30),title,f,WHITE+(255,),40)
tracked(d,((W-ws)//2,y+300),sub,f2,TEAL+(230,),18)
glow(logo,18).save(os.path.join(OUT,'T_Logo_HollowKin.png'))
# ---- icons 256
def icon(name,draw_fn,col):
    im=Image.new('RGBA',(256,256),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((6,6,250,250),18,outline=col+(200,),width=4,fill=(10,16,17,200))
    draw_fn(d,col); glow(im,5).save(os.path.join(OUT,name+'.png'))
def ammo(d,c):
    for i in range(3):
        x=70+i*48; d.rounded_rectangle((x,70,x+30,190),6,fill=c+(255,)); d.rectangle((x,70,x+30,100),fill=WHITE+(255,))
def gel(d,c):
    d.rounded_rectangle((88,60,168,200),16,outline=c+(255,),width=7); d.rectangle((88,120,168,200),fill=c+(200,))
    d.rectangle((108,40,148,62),fill=WHITE+(255,)); d.line((128,95,128,145),fill=WHITE+(255,),width=8); d.line((103,120,153,120),fill=WHITE+(255,),width=8)
def sed(d,c):
    d.rounded_rectangle((60,110,190,146),14,outline=c+(255,),width=6); d.rectangle((100,112,186,144),fill=c+(180,))
    d.line((190,128,225,128),fill=WHITE+(255,),width=5); d.rectangle((40,100,62,156),fill=WHITE+(255,))
def fuse(d,c):
    d.rounded_rectangle((90,50,166,206),10,outline=c+(255,),width=6); d.rectangle((110,50,146,76),fill=c+(255,))
    d.line((128,90,128,170),fill=AMB+(255,),width=6); d.rectangle((104,196,152,214),fill=c+(255,))
def key(d,c):
    d.ellipse((60,80,130,150),outline=c+(255,),width=9); d.line((130,115,210,115),fill=c+(255,),width=9)
    d.line((185,115,185,150),fill=c+(255,),width=9); d.line((158,115,158,140),fill=c+(255,),width=9)
def drawing(d,c):
    d.rectangle((54,54,202,202),outline=c+(255,),width=5)
    d.ellipse((100,80,156,136),outline=c+(255,),width=5); d.line((128,136,128,180),fill=c+(255,),width=5)
    d.line((128,150,100,170),fill=c+(255,),width=5); d.line((128,150,156,170),fill=c+(255,),width=5)
for n,fn,c in(('T_Icon_Ammo',ammo,AMB),('T_Icon_Gel',gel,(110,220,150)),('T_Icon_Sedative',sed,BLUE),('T_Icon_Fuse',fuse,WHITE),('T_Icon_Keycard',key,RED),('T_Icon_Drawing',drawing,TEAL)): icon(n,fn,c)
print(sorted(os.listdir(OUT)))
# ---- blood overlay (RE7-style): organic edge-weighted blood splatter, transparent centre
import random
random.seed(11)
S=1024; m=Image.new('L',(S,S),0); d=ImageDraw.Draw(m)
for _ in range(900):
    a=random.random()*6.283; rr=(random.random()**0.45)*S*0.62+S*0.18   # weighted to the edges
    x=S/2+math.cos(a)*rr; y=S/2+math.sin(a)*rr*0.8
    r=random.choice([2,3,4,6,8,12,18,28,45]); d.ellipse((x-r,y-r,x+r,y+r),fill=255)
    if random.random()<0.18: d.line((x,y,x+random.randint(-6,6),y+random.randint(30,170)),fill=255,width=random.randint(2,6))
m=m.filter(ImageFilter.GaussianBlur(7)).point(lambda v:255 if v>110 else 0).filter(ImageFilter.GaussianBlur(1.4))
tone=Image.effect_noise((S,S),40).point(lambda v:v//3)
bl=Image.new('RGBA',(S,S),(115,0,6,0)); bl.putalpha(m.point(lambda v:int(v*0.92)))
shade=Image.merge('RGBA',(tone.point(lambda v:90+v//2),Image.new('L',(S,S),0),Image.new('L',(S,S),4),Image.new('L',(S,S),0)))
shade.putalpha(m); bl=Image.alpha_composite(bl,shade)
vig=Image.new('L',(S,S),0); vd=ImageDraw.Draw(vig)
for i in range(60): vd.ellipse((i*4,i*4,S-i*4,S-i*4),outline=int(255*(1-i/60)**2),width=6)
vig=vig.filter(ImageFilter.GaussianBlur(25))
red=Image.new('RGBA',(S,S),(90,0,3,0)); red.putalpha(vig.point(lambda v:int(v*0.7)))
bl=Image.alpha_composite(red,bl); bl.save(os.path.join(OUT,'T_BloodOverlay.png'))
# ---- wristwatch panel for the pause menu (strap + case + dark face)
W2,H2=700,520; wt=Image.new('RGBA',(W2,H2),(0,0,0,0)); d=ImageDraw.Draw(wt)
d.rounded_rectangle((250,0,450,H2),24,fill=(28,32,31,255),outline=(60,68,66,255),width=4)     # strap
for y in range(20,H2,36): d.line((262,y,438,y),fill=(40,46,44,255),width=2)
d.rounded_rectangle((90,110,610,410),44,fill=(52,58,57,255),outline=(110,122,120,255),width=8)    # case
d.rounded_rectangle((122,140,578,380),26,fill=(6,12,12,255),outline=(30,60,58,255),width=4)       # face
for i in range(4): d.line((160+i*0,170+i*60,540,170+i*60),fill=(14,26,25,255),width=1)           # faint scan lines
d.ellipse((600,230,630,260),fill=(90,100,98,255))                                                 # crown
wt=glow(wt,6); wt.save(os.path.join(OUT,'T_Watch.png'))
