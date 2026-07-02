// Export each .slide as its own PNG at native size (x2 for crispness).
//   node shots.js <input.html> <outDir> [prefix]
// e.g. node shots.js slides.html out/slides slide
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const IN = path.resolve(process.argv[2] || 'slides.html');
const OUTDIR = path.resolve(process.argv[3] || 'out/shots');
const PREFIX = process.argv[4] || 'slide';

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.goto('file://' + IN, { waitUntil: 'networkidle' });
  await page.waitForSelector('body[data-doodles-ready="1"]', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(400);
  const slides = await page.$$('.slide');
  let i = 0;
  for (const s of slides) {
    i++;
    const file = path.join(OUTDIR, `${PREFIX}-${String(i).padStart(2, '0')}.png`);
    await s.screenshot({ path: file });
    console.log('OK', file);
  }
  await browser.close();
  console.log(`\n${i} slides -> ${OUTDIR}`);
})();
