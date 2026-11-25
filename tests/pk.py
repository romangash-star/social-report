import asyncio,json
from playwright.async_api import async_playwright
GJ={"type":"FeatureCollection","features":[
 {"type":"Feature","properties":{"MisparProject":8001853,"ShemMitcham":"ההסתדרות 197-207","Yeshuv":"חולון","plan_name":"505-1398999","TeurSugMaslul":"רשויות","codeStatusHarashut":1,"yachadKayamRashut":"146","yachadMutzaRashut":"596","YachadTosafti":450},
  "geometry":{"type":"Polygon","coordinates":[[[34.7890,32.0133],[34.7918,32.0118],[34.7912,32.0110],[34.7885,32.0126],[34.7890,32.0133]]]}},
 {"type":"Feature","properties":{"MisparProject":4342,"ShemMitcham":"פיכמן","Yeshuv":"חולון","plan_name":"505-0548057","TeurSugMaslul":"מיסוי","codeStatusHarashut":3,"yachadKayamRashut":"116","yachadMutzaRashut":"235","YachadTosafti":119},
  "geometry":{"type":"Polygon","coordinates":[[[34.78,32.02],[34.781,32.02],[34.781,32.021],[34.78,32.021],[34.78,32.02]]]}}]}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']);pg=await b.new_page(viewport={'width':1300,'height':1000});errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        async def route(r):
            u=r.request.url
            if 'leaflet.min.js' in u: await r.fulfill(path='/home/claude/test/lf/package/dist/leaflet.js',content_type='application/javascript')
            elif 'leaflet.min.css' in u: await r.fulfill(path='/home/claude/test/lf/package/dist/leaflet.css',content_type='text/css')
            elif 'GIS_UrbanRenewal' in u: await r.fulfill(body=json.dumps(GJ,ensure_ascii=False),content_type='application/json')
            elif 'nominatim' in u and 'reverse' in u: await r.fulfill(body=json.dumps({"display_name":"x","address":{"road":"ההסתדרות","house_number":"209","city":"חולון"}}),content_type='application/json')
            elif 'tile.openstreetmap' in u: await r.fulfill(status=204)
            elif u.startswith('file:'): await r.continue_()
            else: await r.abort()
        await pg.route('**/*',route)
        await pg.goto('file://{ROOT}/index.html');await pg.wait_for_timeout(1500)
        await pg.fill('#urSearch','חולון ההסתדרות');await pg.wait_for_timeout(200)
        print('list:',await pg.inner_text('#urList'))
        await pg.click('[data-urfocus="8001853"]');await pg.wait_for_timeout(600)
        await pg.screenshot(path='/home/claude/test/pk1.png')
        await pg.click('.leaflet-popup [data-pickur="8001853"]');await pg.wait_for_timeout(1200)
        print('meta:',await pg.evaluate("JSON.stringify([S.meta.name,S.meta.city,S.meta.track,S.meta.compoundId,S.buildings.map(b=>b.num).join(','),!!S.compound.geo])"))
        print('selbox:',await pg.inner_text('.selbox'))
        # click on map center to reverse geocode
        box=await pg.query_selector('#pmap');bb=await box.bounding_box()
        await pg.mouse.click(bb['x']+bb['width']/2,bb['y']+bb['height']/2);await pg.wait_for_timeout(800)
        print('popup:',await pg.inner_text('.leaflet-popup-content'))
        btn=await pg.query_selector('.leaflet-popup [data-addrev]')
        if btn: await btn.click();await pg.wait_for_timeout(600)
        print('n buildings:',await pg.evaluate("S.buildings.length"))
        await pg.screenshot(path='/home/claude/test/pk2.png')
        await pg.evaluate("go('compound')");await pg.wait_for_timeout(600);await pg.screenshot(path='/home/claude/test/pk3.png')
        print('ERR',errs)
        await b.close()
asyncio.run(main())
