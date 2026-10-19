/* Compare each page that opens alone with its portal form (academy decisions 0050 and 0051).

   For each tab, in light and in dark mode, at 1280 and 390 pixels wide, with every part open, it takes a full-page
   screenshot of the page that opens alone (without its theme button, which the portal does not have) and of the test
   page of the portal form with ?shell=0 (no side bar, no padding). The two must match pixel for pixel, or the scoped
   styles, the sizes in pixels or the dark mode of the portal form differ from the page. compare-shots.py counts the pixels.

   Run from the folder ccar-f-mock-generator, after the build:
       NODE_PATH=<folder with playwright-core> CHROME=<path of chrome-headless-shell> OUT=<folder> node academy/build/compare-portal-form.js
       python3 academy/build/compare-shots.py <folder> */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const PAGES = path.join(__dirname, '..', 'pages');
const OUT = process.env.OUT;
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.ts': 'text/javascript', '.woff2': 'font/woff2', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml' };

const srv = http.createServer((req, res) => {
  let u = decodeURIComponent(req.url.split('?')[0].split('#')[0]);
  if (u.startsWith('/academy/')) u = '/portal/public' + u;
  const f = path.join(PAGES, u);
  if (!f.startsWith(PAGES) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

async function shot(browser, url, scheme, width, file) {
  const ctx = await browser.newContext({ colorScheme: scheme, viewport: { width, height: 900 }, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.waitForFunction(() => !!document.getElementById('pop'));
  await p.evaluate(async () => { document.querySelectorAll('details').forEach((d) => { d.open = true; }); await document.fonts.ready; });
  await p.addStyleTag({ content: '#theme-btn { display: none !important; }' });
  await p.waitForTimeout(300);
  await p.screenshot({ path: file, fullPage: true });
  await ctx.close();
}

srv.listen(0, '127.0.0.1', async () => {
  const base = 'http://127.0.0.1:' + srv.address().port + '/';
  const browser = await chromium.launch({ executablePath: process.env.CHROME });
  fs.mkdirSync(OUT, { recursive: true });
  for (const tab of ['exam-guide-breakdown', 'behind-the-mocks']) {
    for (const scheme of ['light', 'dark']) {
      for (const width of [1280, 390]) {
        const tag = tab + '-' + scheme + '-' + width;
        await shot(browser, base + tab + '.html', scheme, width, path.join(OUT, tag + '-alone.png'));
        await shot(browser, base + 'portal/preview/' + tab + '.html?shell=0', scheme, width, path.join(OUT, tag + '-portal.png'));
        console.log('shot ' + tag);
      }
    }
  }
  await browser.close(); srv.close();
});
