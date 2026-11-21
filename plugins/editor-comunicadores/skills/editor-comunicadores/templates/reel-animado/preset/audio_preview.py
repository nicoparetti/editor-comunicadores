import numpy as np, subprocess, json, sys
SR=48000; DUR=7.8
def load(p, mono=False):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True,check=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
def db(x): return 20*np.log10(x+1e-12)
# voz: pasa altos 80 Hz + compresión suave (umbral −22 dB, 2,5:1, 10/120 ms)
subprocess.run(['ffmpeg','-v','error','-y','-i','voz_v1.wav','-t',str(DUR),'-af','highpass=f=80,acompressor=threshold=0.0794:ratio=2.5:attack=10:release=120:makeup=1','-ac','2','-ar',str(SR),'voz_pv.wav'],check=True)
v=load('voz_pv.wav'); n=int(DUR*SR); v=np.pad(v,((0,max(0,n-len(v))),(0,0)))[:n]
v*=10**(-1/20)/np.abs(v).max()
vrms=np.sqrt(np.mean(v[np.abs(v).max(1)>0.02]**2))
mix=np.zeros_like(v); EV=[]
def put(f,t,peak,d):
    x=load('sfx/'+f); x*=10**(peak/20)/(np.abs(x).max()+1e-9); i=int(t*SR); j=min(n,i+len(x)); mix[i:j]+=x[:j-i]; EV.append((round(t,2),peak,d,f))
W=json.load(open('voz_v1_palabras.json'))
CORR={12:4.02,13:4.63,14:4.77,15:5.04,16:5.35,17:6.18,18:6.31,19:6.57,20:6.70,21:7.16}
T=lambda i: CORR.get(i,W[i]['s'])
G=3.0   # +3 dB: lleva los SFX al estándar común (nivel base +12)
P0=T(4)-0.12; P1=T(9)-0.08
put('tap_texture.mp3',0.05,-8+G,'entra el que trabaja')
put('whoosh-short.mp3',P0-0.13+0.05,-9+G,'cámara: taller → plataforma')
put('5_mouse_click.mp3',P0+0.4,-7+G,'se enciende el círculo de luz')
put('mouse05.mp3',T(8),-9+G,'rótulo «ministerio»')
put('whoosh-short.mp3',P1-0.13+0.05,-9+G,'cámara: plataforma → taller')
put('click_decision.mp3',T(15),-5+G,'2ª clase')
# contador continuo: muchos clics que se van espaciando (desaceleración), sin huecos
c0,c1=T(17),T(21)+0.35; t=c0; k=0; import random; random.seed(3)
while t<c1-0.01:
    u=(t-c0)/(c1-c0); put('key-press.mp3',t,-7+G-1.5*u+random.uniform(-0.6,0.6),'contador 2026→1600'); k+=1
    t+=0.028+0.16*u**2.2
put('pop.wav',c1,-9+G,'el contador llega a 1600')
# cama sonora: pad grave con octavas altas, ≈ 12 dB bajo la voz, todo el video
tt=np.arange(n)/SR; y=np.zeros(n)
for k,f in enumerate((65.41,98.0,130.81,261.63,392.0)):
    for det in (-0.6,0.6):
        ph=2*np.pi*(f+det)*tt+0.003*np.sin(2*np.pi*0.3*tt+k)*f
        y+=np.sin(ph)+0.15*np.sin(2*ph)/2
env=np.minimum(1,tt/1.0)*np.minimum(1,(DUR-tt)/0.5); y*=env
a=np.exp(-2*np.pi*1800/SR); from scipy.signal import lfilter
y=lfilter([1-a],[1,-a],y)
y*=vrms*10**(-12/20)/np.sqrt(np.mean(y[int(SR):-int(SR)]**2))
mix+=np.stack([y,y],1).astype(np.float32)
out=v+mix
fo=int(0.12*SR); out[-fo:]*=np.linspace(1,0,fo)[:,None]
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-af','alimiter=limit=0.89:attack=1:release=60:level=disabled','-c:a','pcm_s24le','mezcla_pv.wav'],input=out.astype(np.float32).tobytes(),check=True)
print(len(EV),'efectos;', sum('contador' in e[2] for e in EV),'clics del contador'); [print(e) for e in EV if 'contador' not in e[2]]
