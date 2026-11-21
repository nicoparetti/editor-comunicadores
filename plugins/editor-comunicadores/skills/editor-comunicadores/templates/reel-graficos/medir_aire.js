const {chromium}=require('playwright');const {PNG}=require('pngjs');
const C={c2:['g2',7.4],c13:['g13',36.2],c7:['g7',45.2],c8:['g8',55.0],c9:['g9',61.7]};
function ink(a,b){const A=PNG.sync.read(a),B=PNG.sync.read(b);let x0=1e9,y0=1e9,x1=-1,y1=-1;
for(let y=0;y<A.height;y++)for(let x=0;x<A.width;x++){const i=(y*A.width+x)*4;if(Math.abs(A.data[i]-B.data[i])+Math.abs(A.data[i+1]-B.data[i+1])+Math.abs(A.data[i+2]-B.data[i+2])>60){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}}
return [y0,A.height-1-y1,x0,A.width-1-x1];}
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/graficos.html');await p.waitForTimeout(800);
for(const [c,[g,t]] of Object.entries(C)){await p.evaluate(([g,t])=>window.render(g,t),[g,t]);const el=await p.$('#'+c);
await p.evaluate(c=>document.getElementById(c).style.transform='none',c);
const a=await el.screenshot();await p.evaluate(c=>[...document.getElementById(c).children].forEach(e=>e.style.visibility='hidden'),c);const bb=await el.screenshot();
await p.evaluate(c=>[...document.getElementById(c).children].forEach(e=>e.style.visibility=''),c);
console.log(c,'arriba/abajo/izq/der',ink(a,bb).join(' / '));}
await b.close();})();
