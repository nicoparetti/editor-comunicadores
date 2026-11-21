import sys, subprocess, time
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE = Path(__file__).resolve().parent
FPS = 30
def frames(times, outdir):
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = br.new_page(viewport={'width': 1080, 'height': 1920}); pg.on('pageerror', lambda e: print('pageerror:', e))
        pg.goto(f'file://{HERE}/reel.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        for t in times:
            pg.evaluate(f'render({t})'); pg.screenshot(path=f'{outdir}/f_{t:07.2f}.png')
        br.close()
def video(f0, f1, out):
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
                           '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', out], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = br.new_page(viewport={'width': 1080, 'height': 1920}); pg.on('pageerror', lambda e: print('pageerror:', e))
        pg.goto(f'file://{HERE}/reel.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        t0 = time.time()
        for i in range(f0, f1):
            pg.evaluate(f'render({i / FPS})'); ff.stdin.write(pg.screenshot(type='jpeg', quality=94))
            if (i - f0) % 300 == 0: print(out, i, round(time.time() - t0), 's', flush=True)
        br.close()
    ff.stdin.close(); ff.wait()
if __name__ == '__main__':
    if sys.argv[1] == 'frames':
        Path(sys.argv[2]).mkdir(exist_ok=True); frames([float(x) for x in sys.argv[3:]], sys.argv[2])
    else:
        video(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
