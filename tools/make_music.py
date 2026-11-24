"""Synthesizes placeholder base music (original, no samples): ambient drone loop, tension loop, music-box lullaby. Needs numpy."""
import numpy as np, wave, os
OUT=os.path.join(os.path.dirname(__file__),'..','HollowKin','SourceAudio'); SR=44100
rng=np.random.default_rng(7)
def save(name,x):
    x=x/ (np.abs(x).max()+1e-9)*0.8; st=np.stack([x[0],x[1]],1) if x.ndim==2 else np.stack([x,x],1)
    with wave.open(os.path.join(OUT,name+'.wav'),'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
def t(sec): return np.arange(int(sec*SR))/SR
def lp(x,k): 
    c=np.cumsum(np.insert(x,0,0)); y=(c[k:]-c[:-k])/k; return np.pad(y,(0,len(x)-len(y)),mode='edge')
def loopfade(x,n): # crossfade tail into head for seamless loop
    f=np.linspace(0,1,n); y=x[:-n].copy(); y[:n]=y[:n]*f+x[-n:]*(1-f); return y
# ---- ambient drone (A minor-ish, cold)
D=100; tt=t(D+4)
def sine(f,ph=0): return np.sin(2*np.pi*f*tt+ph)
amb=0.5*sine(55)+0.35*sine(55.4)+0.25*sine(82.4,1)+0.18*sine(110.3)
swell=0.6+0.4*np.sin(2*np.pi*tt/25)
amb*=swell
noise=lp(rng.standard_normal(len(tt)),60); noise=lp(noise,40); amb+=noise*6*(0.5+0.5*np.sin(2*np.pi*tt/17+2))
sub=0.4*np.sin(2*np.pi*36.7*tt)*(0.5+0.5*np.sin(2*np.pi*tt/9))
amb+=sub
L=loopfade(amb,SR*4); R=loopfade(np.roll(amb,3000),SR*4); save('MUS_Ambient_Containment',np.stack([L,R]))
# ---- tension: pulsing heartbeat-like low pulse + dissonant high bed
D=60; tt=t(D+4)
pulse=np.zeros(len(tt)); bpm=70
for b in np.arange(0,D+4,60/bpm):
    for off,amp in((0,1.0),(0.28,0.6)):
        i=int((b+off)*SR); n=int(0.25*SR)
        if i+n<len(pulse): pulse[i:i+n]+=amp*np.sin(2*np.pi*48*t(0.25))*np.exp(-t(0.25)*14)
bed=0.25*np.sin(2*np.pi*466*tt)+0.25*np.sin(2*np.pi*493.9*tt)
bed*=(0.3+0.3*np.sin(2*np.pi*tt/11)); bed+=lp(rng.standard_normal(len(tt)),8)*3*(0.5+0.5*np.sin(2*np.pi*tt/7))
ten=pulse*1.4+bed*0.5+0.35*np.sin(2*np.pi*55*tt)
save('MUS_Tension',np.stack([loopfade(ten,SR*3),loopfade(np.roll(ten,2000),SR*3)]))
# ---- Emilia's lullaby (music box, safe rooms). 3/4, slow, A minor.
notes={'A4':440,'B4':493.88,'C5':523.25,'D5':587.33,'E5':659.25,'F5':698.46,'G5':783.99,'A5':880,'E4':329.63,'C4':261.63}
mel=[('E5',1),('D5',1),('C5',1),('B4',2),('C5',1),('D5',1),('E5',2),('A4',1),('A4',3),
     ('C5',1),('D5',1),('E5',1),('G5',2),('F5',1),('E5',1),('D5',2),('B4',1),('C5',3),
     ('E5',1),('D5',1),('C5',1),('B4',2),('A4',1),('C5',1),('B4',1),('A4',1),('E4',1),('A4',3)]
beat=0.62; total=sum(d for _,d in mel)*beat+4; y=np.zeros(int(total*SR)); pos=0
for n,d in mel:
    f=notes[n]; tn=t(2.2); env=np.exp(-tn*2.6)
    tone=(np.sin(2*np.pi*f*tn)+0.4*np.sin(2*np.pi*f*2.76*tn)*np.exp(-tn*9)+0.2*np.sin(2*np.pi*f*5.4*tn)*np.exp(-tn*18))*env
    i=int(pos*SR); y[i:i+len(tone)]+=tone[:len(y)-i]; pos+=d*beat
y*=1; # slight detune pad for unease
pad=0.06*np.sin(2*np.pi*110*t(total))+0.05*np.sin(2*np.pi*164.8*t(total)*1.004); y=y[:len(pad)]+pad[:len(y)]
save('MUS_Lullaby_MusicBox',np.stack([y,np.roll(y,400)]))
print(sorted(os.listdir(OUT)))
