import asyncio, subprocess, sys, time
from playwright.async_api import async_playwright
# Uso: python3 render.py <cuadro_ini> <cuadro_fin> salida.mp4 graficos.html <duración_s>
FPS=30; a=int(sys.argv[1]); out=sys.argv[3]; HTML=sys.argv[4]; FIN=float(sys.argv[5]); N=int(round(FIN*FPS)); b=min(N,int(sys.argv[2]))
async def main():
    ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
        '-c:v','libx264','-preset','medium','-crf','12','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',out],stdin=subprocess.PIPE)
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox","--allow-file-access-from-files"])
        pg=await br.new_page(viewport={"width":1080,"height":1920})
        await pg.goto("file://"+__import__("os").path.abspath(HTML)); await pg.wait_for_timeout(1500)
        t0=time.time()
        for i in range(a,b):
            await pg.evaluate(f"render({i/FPS})")
            ff.stdin.write(await pg.screenshot(type="jpeg",quality=95))
            if i%150==0: print(i, round(time.time()-t0), flush=True)
        await br.close()
    ff.stdin.close(); ff.wait(); print('LISTO', out)
asyncio.run(main())
