# Inserta silencios en la voz cortada: pausa mínima entre oraciones + respiros en momentos clave
import json, numpy as np, subprocess
W=json.load(open('palabras_editadas.json')); C=json.load(open('cortes.json'))
SR=48000
juncs=[]; acc=0
for a,b in C: acc+=b-a; juncs.append(acc)
HOLD={26:0.5, 39:0.9, 113:1.0, 166:0.45, 192:0.6, 208:0.7, 215:0.25, 227:0.4, 251:0.45, 269:0.6, 276:0.4}
NOMIN={136}
MINGAP=0.45
raw0=subprocess.run(['ffmpeg','-v','error','-i','voz_tratada.wav','-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True,check=True).stdout
x0=np.frombuffer(raw0,np.float32); H=480
def emin(a,b):
    ks=range(int(a*100),max(int(a*100)+1,int(b*100)))
    e=[(np.sqrt((x0[k*H:(k+1)*H]**2).mean()),k) for k in ks]
    return (min(e)[1]+0.5)/100
ins=[]
for i in range(len(W)-1):
    w,n=W[i],W[i+1]
    end_sent = w['w'][-1] in '.?!'
    extra = HOLD.get(i,0)
    gap = n['s']-w['e']
    if end_sent and gap < MINGAP and i not in NOMIN: extra = max(extra, MINGAP-max(gap,0))
    if extra<=0: continue
    # punto de inserción: unión de cortes más cercana antes del inicio de la palabra siguiente
    pt = {166: emin(60.80, 60.98)}.get(i) or emin(w['s']+0.15, n['s']+0.03)
    ins.append((round(pt,3), round(extra,2), i, w['w']))
raw=subprocess.run(['ffmpeg','-v','error','-i','voz_tratada.wav','-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True,check=True).stdout
x=np.frombuffer(raw,np.float32)
parts=[];prev=0
for pt,ex,i,ww in ins:
    k=int(pt*SR); parts.append(x[prev:k]); parts.append(np.zeros(int(ex*SR),np.float32)); prev=k
parts.append(x[prev:]); parts.append(np.zeros(int(1.6*SR),np.float32))   # cola final
y=np.concatenate(parts)
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s24le','voz_v6.wav'],input=y.tobytes(),check=True)
def mp(t,tol=0.0):
    return t+sum(ex for pt,ex,_,_ in ins if pt<=t+tol)
W2=[{'w':w['w'],'s':round(mp(w['s'],0.06),3),'e':round(mp(w['e']),3)} for w in W]
# fijar: inicio en el desplazamiento correcto aunque la palabra cruce el punto
for w,o in zip(W2,W):
    if w['e']<w['s']+0.06: w['e']=w['s']+0.06
W4=json.load(open('palabras_v4.json'))
CORR={136:{'e':54.81},137:{'s':55.24},165:{'s':64.75},166:{'s':64.95,'e':65.56},208:{'e':81.49},209:{'s':82.98},212:{'s':84.30},213:{'s':84.51},214:{'s':84.62},215:{'s':84.76,'e':85.27},
      249:{'s':96.97},250:{'s':97.28},251:{'s':97.56,'e':98.34},268:{'s':103.72},269:{'s':104.0,'e':104.43}}
for i,fs in CORR.items():
    d=W2[i]['s']-W4[i]['s']
    for f,v in fs.items(): W2[i][f]=round(v+d,3)
json.dump(W2,open('palabras_v6.json','w'),ensure_ascii=False,indent=0)
json.dump(ins,open('silencios_v6.json','w'),ensure_ascii=False)
print(len(ins),'inserciones', round(sum(e for _,e,_,_ in ins),2),'s extra · duración', round(len(y)/SR,2))
for pt,ex,i,ww in ins: print(pt,ex,i,ww)
