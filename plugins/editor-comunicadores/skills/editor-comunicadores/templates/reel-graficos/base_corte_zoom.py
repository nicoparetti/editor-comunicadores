import json, subprocess, sys
K=json.load(open('cortes.json'))
SRC=__import__('os').environ.get('BRUTO','../../../1_Videos sin editar/<proyecto>/bruto.mp4')   # ruta del bruto (variable BRUTO)
i0,i1,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
ed=[];acc=0
for s,e in K: ed.append(acc); acc+=e-s
FACE={4:(544,492),13:(550,514),26:(549,467),27:(549,467),28:(549,467)}
A0,A1=70.15,73.55
def zexpr(i):
    T0=ed[i]
    if i in (4,13): return "1+0.3*(1-pow(1-min(1,on/6),3))"
    if i in (26,27): return f"1+0.4*min(1,max(0,({T0:.3f}+on/30-{A0})/{A1-A0:.3f}))"
    if i==28: return "1.4-0.4*(1-pow(1-min(1,on/7),3))"
    return None
fv=[];fa=[]
for k,i in enumerate(range(i0,i1)):
    s,e=K[i]; z=zexpr(i)
    v=f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS"
    if z:
        fx,fy=FACE[i]; X=fx*2; Y=fy*2
        v+=f",scale=2160:3840:flags=lanczos,zoompan=z='{z}':x='{X}*(1-1/zoom)':y='{Y}*(1-1/zoom)':d=1:s=1080x1920:fps=30"
    else:
        v+=",scale=1080:1920:flags=lanczos"
    if i==len(K)-1: v+=",tpad=stop_mode=clone:stop_duration=0.6"
    v+=f",setsar=1,format=yuv420p[v{k}]"
    a=f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.006,afade=t=out:st={e-s-0.006:.3f}:d=0.006"
    if i==len(K)-1: a+=",apad=pad_dur=0.6"
    a+=f"[a{k}]"
    fv.append(v); fa.append(a)
n=i1-i0
fc=';'.join(fv+fa)+';'+''.join(f'[v{k}][a{k}]' for k in range(n))+f'concat=n={n}:v=1:a=1[v][a]'
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',SRC,'-filter_complex',fc,'-map','[v]','-map','[a]',
     '-r','30','-c:v','libx264','-preset','veryfast','-crf','15','-threads','4','-c:a','pcm_s16le','-ar','48000',out]
subprocess.run(cmd,check=True); print('ok',out)
