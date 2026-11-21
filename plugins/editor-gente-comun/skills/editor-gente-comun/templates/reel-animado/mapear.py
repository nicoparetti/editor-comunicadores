# Mapea palabras del bruto al audio cortado
import json, sys
W = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2]))
off=[]; acc=0
for a,b in C: off.append((a,b,acc)); acc += b-a
out=[]
for w in W:
    cands=[(w['s']+w['e'])/2, w['s']+0.05, w['s'], w['e']-0.05]
    m=next((t for t in cands if any(a-0.05<=t<=b+0.05 for a,b,_ in off)), None)
    if m is None:
        m=min((abs(a-w['s']),a) for a,b,_ in off)[1]
    for a,b,o in off:
        if a-0.05<=m<=b+0.05:
            s=min(max(w['s'],a),b); e=min(max(w['e'],a),b)
            out.append({'w':w['w'],'s':round(s-a+o,3),'e':round(max(e-a+o, s-a+o+0.06),3)}); break
json.dump(out, open(sys.argv[3],'w'), ensure_ascii=False, indent=0)
print(len(W),'->',len(out),'palabras; dur',round(acc,3))
