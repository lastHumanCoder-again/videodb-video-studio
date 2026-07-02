// Render slides.html -> a 16:9 PDF (one slide per page) using system Chrome.
//   node render.js [input.html] [output.pdf]
const { chromium } = require('playwright');
const path = require('path');

const IN  = path.resolve(process.argv[2] || 'slides.html');
const OUT = path.resolve(process.argv[3] || 'out/videodb-deck.pdf');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage();
  await page.goto('file://' + IN, { waitUntil: 'networkidle' });
  // wait for the hand-drawn doodles to finish painting
  await page.waitForSelector('body[data-doodles-ready="1"]', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(400);
  await page.emulateMedia({ media: 'screen' });
  // auto-detect slide size from the first .slide so any dimension works
  const dim = await page.evaluate(() => {
    const s = document.querySelector('.slide');
    if (!s) return { w: 1280, h: 720 };
    const r = s.getBoundingClientRect();
    return { w: Math.round(r.width), h: Math.round(r.height) };
  });
  await page.pdf({
    path: OUT,
    width: dim.w + 'px',
    height: dim.h + 'px',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });
  await browser.close();
  console.log(`PDF -> ${OUT}  (${dim.w}×${dim.h})`);
})();
