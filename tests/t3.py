import asyncio
from playwright.async_api import async_playwright
STEPS=['project','sources','urban','compound','housing','pop','org','svc','survey','concl','alts','gantt','summary','report']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1300,'height':900})
        errs=[]
        pg.on('pageerror',lambda e:errs.append('PAGE:'+str(e)))
        await pg.goto('file://{ROOT}/index.html',wait_until='domcontentloaded')
        await pg.wait_for_timeout(500)
        await pg.click('#bDemo'); await pg.wait_for_timeout(200)
        for s in STEPS:
            await pg.evaluate(f"go('{s}')"); await pg.wait_for_timeout(120)
            if s=='urban': await pg.click('#fillCmp')
            if s=='pop': await pg.click('[data-autopop]')
            if s=='concl':
                await pg.click('#conclAuto')
                for i in range(4):
                    btn=await pg.query_selector('[data-addsug]')
                    if btn: await btn.click(); await pg.wait_for_timeout(80)
            if s=='alts': await pg.click('#altDef')
            if s=='gantt':
                for c in ['0.0','0.1','1.2','4.3','4.4']: await pg.click(f'[data-gc="{c}"]')
            if s=='summary': await pg.click('#sumAuto')
            await pg.screenshot(path=f'/home/claude/test/v3_{s}.png')
        for rt in ['מצב קיים','הערכת חלופות','מלא']:
            await pg.evaluate("go('report')")
            await pg.select_option('#repType',rt); await pg.wait_for_timeout(200)
            txt=await pg.inner_text('#paper'); open(f'/home/claude/test/rep_{rt}.txt','w').write(txt)
            await pg.screenshot(path=f'/home/claude/test/v3_rep_{rt}.png',full_page=True)
        async with pg.expect_download() as d: await pg.click('#expWord')
        await (await d.value).save_as('/home/claude/test/v3.doc')
        print('recs',await pg.evaluate('S.recs.length'),'concl',await pg.evaluate('S.concl.length'))
        print('ERRORS',errs)
        await b.close()
asyncio.run(main())
