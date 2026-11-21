import numpy as np, subprocess, json
R='sfx/'; SR=48000; W=json.load(open('palabras_v7.json')); DUR=json.load(open('fin7.json'))['FIN']; GAIN=12.0  # estándar de SFX de todos los tipos (+12 sobre el nivel base)
T=lambda i: W[i]['s']; TE=lambda i: W[i]['e']
_c={}
def load(p):
    if p not in _c:
        raw=subprocess.run(['ffmpeg','-v','error','-i',R+p,'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True,check=True).stdout
        _c[p]=np.frombuffer(raw,dtype=np.float32).reshape(-1,2).copy()
    return _c[p].copy()
def norm(x,db): return x*(10**(db/20)/(np.abs(x).max()+1e-9))
mix=np.zeros((int(DUR*SR),2),np.float32); EV=[]
def put(f,t,peak,d,dur=None,fadein=0):
    x=load(f)
    if dur: x=x[:int(dur*SR)]; n=min(len(x),int(0.06*SR)); x[-n:]*=np.linspace(1,0,n)[:,None]
    if fadein: n=int(fadein*SR); x[:n]*=np.linspace(0,1,n)[:,None]
    x=norm(x,peak+GAIN); i=int(max(t,0)*SR); j=min(len(mix),i+len(x)); mix[i:j]+=x[:j-i]; EV.append((round(t,2),peak,f'{d} ({f})'))
TAP='tap_texture.mp3'; TXT='mouse05.mp3'; DEC='click_decision.mp3'; POP='pop.wav'; SW='swoosh.mp3'; SWI='swish.wav'; G='golpe_suave.wav'; PAP='paper.mp3'
# --- gancho ---
for k in range(11):                          # contador: clics mecánicos suaves que desaceleran
    u=k/10; put('px_key-press.mp3',0.2+1.5*(1-(1-u)**2),-6-k*0.25,'contador 2026→1727')
put(POP,1.72,-8,'llega a 1727')
put(TAP,T(4),-7,'aldea'); put(TXT,T(7),-10,'rótulo aldea')
put(SWI,T(11)-0.13,-10,'cambio a la tesis'); put(TXT,T(12),-8,'la idea')
put(TAP,T(15),-5,'figura orando'); put(TAP,T(22),-5,'figura martillando')
put('snap.mp3',T(23),-7,'línea quebrada'); put(G,T(26),-8,'sostenerlos')
# --- 100 años ---
put(SWI,T(27)-0.13,-10,'cambio a Herrnhut 1727'); put(TAP,T(27)+0.05,-10,'llama')
put('whoosh_grave.wav',T(35),-11,'el anillo se llena',dur=T(38)-T(35)+0.1,fadein=0.3)
put(G,T(38),-5,'+100 años'); put(DEC,T(38)+0.02,-10,'+100 años clic')
put(SW,T(43),-9,'salen del anillo')
# --- mapa Europa ---
put(SW,T(50),-7,'mapa: acercamiento'); put(TXT,T(52),-6,'Moravia')
put(G,T(57),-7,'tarjeta Jan Hus'); put(POP,T(65),-9,'pin Moravia'); put(POP,T(66),-7,'1722')
put(SW,T(67),-11,'ruta a Herrnhut'); put(POP,T(67)+1.5,-8,'pin Herrnhut'); put(TXT,T(69),-9,'Sajonia')
put(TAP,T(74),-6,'tarjeta Zinzendorf'); put(TAP,T(77),-6,'tarjeta Herrnhut')
put(SW,T(78),-9,'mapa: alejamiento a Europa'); put(TXT,T(79),-10,'Alemania')
# --- peleados → avivamiento (como v1) ---
put(SWI,T(90)-0.13,-10,'cambio a vecinos'); put('error.wav',T(93),-8,'vivían peleados')
put(TXT,T(98),-6,'13·08·1727'); put(TAP,T(101),-6,'santa cena')
put(G,T(109),-5,'avivamiento'); put(SW,T(110),-9,'se forma el círculo')
# --- reloj ---
put(SWI,T(114)-0.13,-10,'cambio a reloj'); put(TXT,T(117),-6,'24 + 24')
for k in range(12):
    u=k/11; put('tic.wav',T(123)+(T(125)+0.25-T(123))*u,-12,'se encienden las horas')
put(DEC,T(126),-5,'1 h'); put(TXT,T(132),-6,'¿y las otras 23?')
put('pop_boca.mp3',T(135),-6,'oficios')
# --- Roentgen / Kersten ---
put(SWI,T(137)-0.13,-10,'cambio a taller'); put(PAP,T(137),-8,'escritorio')
put(TXT,T(149),-6,'Versalles'); put(TXT,T(153),-6,'San Petersburgo')
put(SWI,T(156)-0.13,-10,'cambio a título'); put(TXT,T(156),-5,'no esperaron'); put(PAP,T(156)+0.35,-9,'foto Kersten')
put(DEC,T(165),-6,'los generaron')
# --- 1732 ---
put(SW,T(167)-0.13,-7,'entra el mapa 1732'); put(POP,T(168),-7,'1732'); put(POP,T(169)+0.9,-10,'pin Copenhague')
put(TAP,T(170),-6,'Dober'); put(TAP,T(173),-6,'Nitschmann'); put(SW,T(174),-8,'ruta del barco'); put(POP,T(176)+0.5,-7,'pin Santo Tomás')
put(SW,T(184)-0.13,-7,'entra la cita'); put(TXT,T(187),-9,'cita renglón 2'); put(TXT,T(190),-9,'cita renglón 3')
# --- reprise ---
put(SWI,T(193)-0.13,-10,'reprise'); put(TAP,T(198),-6,'el que trabaja'); put(TAP,T(200),-7,'tarima'); put(TAP,T(205),-6,'«la obra»')
put('snap.mp3',TE(208)+0.02,-6,'línea quebrada'); put(G,TE(208)+0.06,-8,'la tarima cede')
put(DEC,T(215),-4,'misión'); put(G,T(215)+0.02,-6,'misión golpe')
# --- oración + taller (como v1) ---
put(SWI,T(216)-0.13,-10,'cambio a íconos'); put(TAP,T(219),-6,'cuarto de oración'); put(TAP,T(222),-6,'taller')
put(SW,T(224),-8,'se funden'); put(G,T(226),-7,'mismo lugar')
# --- iglesia / frase ---
put(SWI,T(228)-0.13,-10,'cambio a iglesia'); put(TAP,T(228)+0.1,-8,'iglesia')
put('slide_metal.mp3',T(236),-6,'puertas se cierran'); put(G,T(236)+0.55,-8,'puertas cerradas')
put(SWI,T(245)-0.13,-10,'cambio a la frase')
put(DEC,T(251),-4,'adoración'); put(G,T(251)+0.02,-6,'adoración golpe')
# --- dos clases ---
put(SWI,T(252)-0.13,-10,'cambio a cierre'); put(TAP,T(253),-6,'orando'); put(TAP,T(254)+0.4,-6,'martillando')
put('snap.mp3',T(258),-7,'línea quebrada'); put(TXT,T(262),-9,'en la obra'); put(TXT,T(267),-9,'en el trabajo')
# --- oración · misión · vocación ---
put(TAP,T(271),-6,'la oración'); put(TAP,T(273),-6,'la misión'); put(TAP,T(276),-6,'la vocación')
put(SW,T(277),-8,'se forma el círculo')
put(G,T(283),-5,'el plan de Dios')
def pad(freqs,t,dur,peak,d,att=0.8,rel=1.2,bright=0.25):
    n=int(dur*SR); tt=np.arange(n)/SR; y=np.zeros(n)
    for k,f in enumerate(freqs):
        for det in (-0.6,0.6):
            ph=2*np.pi*(f+det)*tt+0.003*np.sin(2*np.pi*0.3*tt+k)*f
            y+=np.sin(ph)+bright*np.sin(2*ph)/2+bright*0.5*np.sin(3*ph)/3
    env=np.minimum(1,tt/att)*np.minimum(1,(dur-tt)/rel); y*=env
    a=np.exp(-2*np.pi*1800/SR); z=np.zeros_like(y); acc=0.0
    for i in range(n): acc=(1-a)*y[i]+a*acc; z[i]=acc
    x=np.stack([z,z],1).astype(np.float32); x=norm(x,peak+GAIN); i=int(t*SR); j=min(len(mix),i+len(x)); mix[i:j]+=x[:j-i]; EV.append((round(t,2),peak,f'{d} (pad sintetizado)'))
pad([65.41,98.0,130.81],T(31),T(38)-T(31)+1.6,-15,'pad solemne grave: anillo de oración',att=1.0,rel=1.4,bright=0.15)
pad([65.41,98.0,130.81,196.0],T(112),2.6,-14,'pad solemne: resplandor del avivamiento',att=0.5,rel=1.2,bright=0.2)
pad([146.83,220.0,293.66,440.0],T(224),2.4,-15,'resplandor sagrado: taller + oración',att=0.6,rel=1.2,bright=0.35)
pad([65.41,98.0,130.81,196.0],T(279),DUR-T(279),-15,'pad solemne de fondo hasta el final',att=1.2,rel=1.5,bright=0.2)
from collections import Counter
print('eventos',len(EV),'pico %.1f dBFS'%(20*np.log10(np.abs(mix).max())))
print(Counter(d.split('(')[-1][:-1] for _,_,d in EV).most_common())
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-af','alimiter=limit=0.89:attack=1:release=60:level=disabled','-c:a','pcm_s24le','sfx_v7.wav'],input=mix.tobytes(),check=True)
json.dump(sorted(EV),open('sfx_eventos_v7.json','w'),ensure_ascii=False,indent=0)
