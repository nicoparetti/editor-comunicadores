const {chromium}=require('playwright');const fs=require('fs');
const gs=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/graficos.html');await p.waitForTimeout(1000);
const Gt=await p.evaluate(()=>Object.fromEntries(Object.entries(G).map(([k,v])=>[k,[v[0],v[1]]])));
for(const g of gs){const [a,e]=Gt[g];const n=Math.ceil((e-a)*30);fs.mkdirSync(`fr/${g}`,{recursive:true});
 for(let i=0;i<n;i++){await p.evaluate(([g,t])=>window.render(g,t),[g,a+i/30]);await p.screenshot({path:`fr/${g}/${String(i).padStart(4,'0')}.png`,omitBackground:true});}
 console.log(g,a,e,n);}
await b.close();})();
