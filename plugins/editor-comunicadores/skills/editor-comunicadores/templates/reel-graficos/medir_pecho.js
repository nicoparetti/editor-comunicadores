const {chromium}=require('playwright');
const T={g1:3,g2:7.4,g7:45.2,g8:55.0,g9:61.7,g11:76,g13:36.2};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/graficos.html');await p.waitForTimeout(800);
for(const [g,t] of Object.entries(T)){await p.evaluate(([g,t])=>window.render(g,t),[g,t]);
 const r=await p.evaluate(g=>{const c=document.querySelector('#'+g+' .card');const b=c.getBoundingClientRect();return [Math.round(b.top),Math.round(b.bottom),Math.round(b.height)]},g);
 console.log(g,'top',r[0],'bottom',r[1],'alto',r[2],'aire mentón',r[0]-700,'aire subtítulo',1242-r[1]);}
await b.close();})();
