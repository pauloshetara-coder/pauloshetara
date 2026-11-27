const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); 
  const cfg = [
    ['thumbnail_youtube.png', 1280, 720, {'--u':'10px','--pad':'60px','--bot':'50px','--tr':'470px','--sr':'60px','--st':'60px','--sw':'380px','--sh':'600px','--grad':'linear-gradient(90deg,rgba(0,0,0,.85) 0%,rgba(0,0,0,.4) 60%,rgba(0,0,0,.2) 100%)'}],
    ['capa_vertical.png', 1080, 1920, {'--u':'13px','--pad':'70px','--bot':'120px','--tr':'70px','--sr':'190px','--st':'150px','--sw':'700px','--sh':'900px','--grad':'linear-gradient(180deg,rgba(0,0,0,.2) 0%,rgba(0,0,0,.5) 50%,rgba(0,0,0,.92) 100%)'}]];
  for (const [f, w, h, v] of cfg) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('file://' + path.join(__dirname, 'capa.html'));
    await p.evaluate(([w,h,v]) => { const s=document.body.style; s.setProperty('--w',w+'px'); s.setProperty('--h',h+'px'); for (const k in v) s.setProperty(k,v[k]); }, [w,h,v]);
    await p.waitForTimeout(500); await p.screenshot({ path: path.join(__dirname, f) }); await p.close();
  }
  await b.close();
})();
