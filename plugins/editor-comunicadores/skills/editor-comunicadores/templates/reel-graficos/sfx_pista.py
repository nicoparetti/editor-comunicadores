import numpy as np, subprocess, json
import sys
R='../../../4_Recursos/'; SR=48000; DUR=float(sys.argv[1]) if len(sys.argv)>1 else 86.9   # duración del video cortado
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True,check=True).stdout
    return np.frombuffer(raw,dtype=np.float32).reshape(-1,2).copy()
def norm(x,peak_db):
    p=np.abs(x).max()+1e-9; return x*(10**(peak_db/20)/p)
def quill(seed,dur=0.32):
    rng=np.random.default_rng(seed); n=int(dur*SR); t=np.arange(n)/SR
    noise=rng.standard_normal(n)
    # banda 2.5–7 kHz con granos (rasgueo)
    f=np.fft.rfft(noise); fr=np.fft.rfftfreq(n,1/SR); f*=((fr>2500)&(fr<7000)); s=np.fft.irfft(f,n)
    grains=(0.55+0.45*np.sin(2*np.pi*(38+12*rng.random())*t)**8)
    env=np.minimum(1,t/0.015)*np.exp(-t/0.16)
    s=s*grains*env; return np.stack([s,s],1).astype(np.float32)
def ticks(start,end,n,decel=True,tic=None):
    out=[]
    for k in range(n):
        u=k/(n-1)
        tt=start+(end-start)*(1-(1-u)**2 if decel else u**2)
        out.append(tt)
    return out
mix=np.zeros((int(DUR*SR),2),np.float32)
GAIN=12.0   # estándar de SFX de todos los tipos de reel (+3 dB sobre la primera referencia)
def sh(t): return t   # si se quita un tramo después de armar la lista, desplaza aquí los tiempos posteriores
def put(x,t,peak):
    t=sh(t); x=norm(x,peak+GAIN); i=int(t*SR); j=min(len(mix),i+len(x)); mix[i:j]+=x[:j-i]
pop=load(R+'sfx/pop.wav'); tap=load(R+'sfx/tap_texture.mp3'); dec=load(R+'sfx/click_decision.mp3')
tic=load(R+'sfx/tic.wav'); golpe=load(R+'sfx/golpe_suave.wav'); paper=load(R+'sfx/paper.mp3')
swoosh=load(R+'sfx/swoosh.mp3'); swish=load(R+'sfx/swish.wav'); wg=load(R+'sfx/whoosh_grave.wav')
# Un evento por cosa que aparece o cambia en pantalla: (sonido, segundo, nivel base, descripción).
# El segundo sale de las marcas por palabra del video ya cortado; el nivel base, de la tabla de estilo-por-defecto.md → 7.
ev=[]
ev.append((pop,0.40,-7,'pin en el mapa'))
ev.append((tap,4.55,-5,'aparece la tarjeta'))
ev.append((dec,5.80,-5,'tilde en la lista'))
ev.append((swoosh,14.90,-7,'whoosh 0,13 s antes del golpe de zoom'))
ev.append((golpe,17.55,-5,'golpe: retrato'))
ev.append((paper,25.85,-8,'papel: entra el mapa'))
for k,tt in enumerate(ticks(30.0,31.2,9)): ev.append((tic,tt,-9-k*0.6,'reloj que corre'))
for x,t,p,d in ev: put(x,t,p)

pk=np.abs(mix).max(); print('eventos',len(ev),'pico pista sfx %.1f dBFS'%(20*np.log10(pk)))
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-af','alimiter=limit=0.89:attack=1:release=60:level=disabled','-c:a','pcm_s24le','sfx.wav'],input=mix.tobytes(),check=True)
json.dump([(round(sh(t),2),p,d) for x,t,p,d in ev],open('sfx_eventos.json','w'),ensure_ascii=False,indent=0)
