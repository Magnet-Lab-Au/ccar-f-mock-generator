/* Check F3 (academy/check-plan.md): the load time of each tab from the local disk, and the size of its parts.
   Run: node measure-load.js <page.html> ... Each page loads 3 times, and the script prints the median. */
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME });
  for (const page of process.argv.slice(2)) {
    const t = [];
    for (let i = 0; i < 3; i++) {
      const p = await b.newPage();
      await p.goto('file://' + path.resolve(page), { waitUntil: 'load' });
      t.push(await p.evaluate(() => { const n = performance.getEntriesByType('navigation')[0]; return { dcl: n.domContentLoadedEventEnd, load: n.loadEventEnd }; }));
      await p.close();
    }
    t.sort((a, b) => a.load - b.load);
    const m = t[1];
    const html = fs.readFileSync(page, 'utf8');
    const svg = (html.match(/<svg[\s\S]*?<\/svg>/g) || []).join('').length;
    const js = fs.statSync(page.replace(/\.html$/, '.js')).size;
    console.log(path.basename(page) + ': DOMContentLoaded ' + Math.round(m.dcl) + ' ms, load ' + Math.round(m.load) + ' ms (median of 3, local disk). HTML ' + Math.round(html.length / 1024) + ' KB, of it SVG ' + Math.round(svg / 1024) + ' KB. Page data JS ' + Math.round(js / 1024) + ' KB.');
  }
  await b.close();
})();
