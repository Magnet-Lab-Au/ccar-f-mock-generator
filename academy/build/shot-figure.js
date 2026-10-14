/* Screenshots of one figure of an academy page, and of each step of a stepper (decisions 0013 and 0037).
   Run from the folder ccar-f-mock-generator:
       NODE_PATH=<folder with playwright-core> CHROME=<path of chrome-headless-shell> node academy/build/shot-figure.js <absolute path of page.html> <figure ID or number> <out prefix> [light|dark] [width] [all|full] [nocap]
   nocap hides the caption, the step captions, the panel captions and the sentence of a live figure (check D1). */
const { chromium } = require('playwright-core');
(async () => {
  const [page, fig, out, scheme = 'light', width = '1280', mode = 'all', cap = ''] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: process.env.CHROME });
  const p = await b.newPage({ viewport: { width: +width, height: 1000 }, colorScheme: scheme, reducedMotion: 'reduce' });
  const errs = []; p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + page);
  await p.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
  const h = await p.evaluateHandle((f) => document.getElementById(f) || [...document.querySelectorAll('figure')].find(x => (x.querySelector('.fig-n') || {}).textContent === 'Fig. ' + f), fig);
  const el = h.asElement(); if (!el) { console.log('no figure', fig); process.exit(1); }
  if (cap === 'nocap') await el.evaluate(x => x.querySelectorAll('figcaption, .ve-cap, p.cap, .ve-say').forEach(c => { c.style.display = 'none'; }));
  await el.scrollIntoViewIfNeeded();
  const n = await el.evaluate(x => x.querySelectorAll('.ve-cap li').length);
  await el.screenshot({ path: `${out}-0.png` });
  const nb = await el.evaluate(x => x.querySelectorAll('.ve-toggle button').length);
  for (let k = 0; k < nb; k++) { await el.evaluate((x, i) => x.querySelectorAll('.ve-toggle button')[i].click(), k); await el.screenshot({ path: `${out}-panel${k + 1}.png` }); }
  if (nb) await el.evaluate(x => x.querySelectorAll('.ve-toggle button')[1].click());
  if (mode === 'all') for (let k = 1; k < n; k++) { await el.evaluate(x => x.querySelector('[data-go="1"]').click()); await el.screenshot({ path: `${out}-${k}.png` }); }
  console.log(fig, 'steps', Math.max(0, n - 1), 'errors', errs.length, errs.slice(0, 3).join(' | '));
  await b.close();
})();
