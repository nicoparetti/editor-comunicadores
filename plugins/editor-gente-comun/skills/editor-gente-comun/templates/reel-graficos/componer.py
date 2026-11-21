import subprocess, sys
G=[('g1_v5',0.30,4.52),('g2_v5',4.52,7.93),('g3',7.93,10.55),('g4',17.54,19.29),('g5',25.01,29.62),('g13_v5',33.85,36.36),('g6_v3',36.95,41.87),
   ('g7_v5',41.93,45.77),('g8_v5',49.03,55.54),('g9_v5',55.54,62.10),('g10',62.10,65.24),('g11_v5',73.87,78.50)]
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i','base.mov','-i','mezcla.wav']
for g,a,b in G: cmd+=['-c:v','libvpx-vp9','-i',f'graf/{g}.webm']
fc=[];last='0:v'
for k,(g,a,b) in enumerate(G):
    fc.append(f'[{k+2}:v]format=yuva420p,setpts=PTS-STARTPTS+{a}/TB[o{k}]')
for k,(g,a,b) in enumerate(G):
    fc.append(f"[{last}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a},{b})'[x{k}]"); last=f'x{k}'
fc.append(f'[{last}]subtitles=subs.ass:fontsdir=../../../4_Recursos/fuentes,format=yuv420p[v]')
cmd+=['-filter_complex',';'.join(fc),'-map','[v]','-map','1:a','-r','30','-c:v','libx264','-preset',sys.argv[1],'-b:v','16M','-maxrate','20M','-bufsize','32M','-threads','4',
      '-c:a','pcm_s24le','-shortest','comp.mov']
subprocess.run(cmd,check=True); print('ok')
