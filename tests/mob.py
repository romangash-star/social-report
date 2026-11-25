import asyncio,json
from playwright.async_api import async_playwright
exec(open('pk.py').read().split('async def main')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':390,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=await ctx.new_page();errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        async def route(r):
            u=r.request.url
            if 'leaflet.min.js' in u: await r.fulfill(path='/home/claude/test/lf/package/dist/leaflet.js',content_type='application/javascript')
            elif 'leaflet.min.css' in u: await r.fulfill(path='/home/claude/test/lf/package/dist/leaflet.css',content_type='text/css')
            elif 'GIS_UrbanRenewal' in u: await r.fulfill(body=json.dumps(GJ,ensure_ascii=False),content_type='application/json')
            elif u.startswith('file:'): await r.continue_()
            else: await r.abort()
        await pg.route('**/*',route)
        await pg.goto('file://{ROOT}/index.html');await pg.wait_for_timeout(1200)
        await pg.click('#bDemo');await pg.wait_for_timeout(500)
        res={}
        for s in ['project','compound','housing','org','survey','concl','gantt','report']:
            await pg.evaluate(f"go('{s}')");await pg.wait_for_timeout(300)
            ov=await pg.evaluate("({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,wide:[...document.querySelectorAll('main *')].filter(e=>e.getBoundingClientRect().width>document.documentElement.clientWidth+2&&!e.closest('.scroll')&&!e.closest('.leaflet-container')).slice(0,5).map(e=>e.tagName+'.'+e.className+':'+Math.round(e.getBoundingClientRect().width))})")
            res[s]=ov
            if s in('project','compound','report','gantt'): await pg.screenshot(path=f'/home/claude/test/m_{s}.png')
        hh=await pg.evaluate("document.querySelector('header.top').getBoundingClientRect().height")
        print(json.dumps(res,ensure_ascii=False));print('header h',hh,'ERR',errs)
        await b.close()
asyncio.run(main())
