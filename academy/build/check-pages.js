/* Check the academy pages in a headless browser (decisions 0013, 0015, 0017, 0026 and 0033).

   For each page, in light and in dark mode, at 1280 and 390 pixels wide, with every part open:
   - no console error, no page error and no breach of the security policy
   - no sideways overflow of the page
   - each ID once only
   - each link to an anchor finds its target, and a link to a part opens that part
   - each step of the 9-step diagram has its part
   - each popup and preview card opens, has a title and stays inside the window
   - text contrast at least 4.5 to 1 (3 to 1 for large text), with the known exceptions of decisions 0009 and 0013
   - each text at least 12 pixels high as rendered, also in the figures
   - the word limits of decision 0026: Overview at most 100 words, Explanation at most 500 words, figures not counted
   It also saves screenshots for the owner.

   Needs playwright-core and the headless shell of Chromium. Run from the folder ccar-f-mock-generator:
       NODE_PATH=<folder with playwright-core> CHROME=<path of chrome-headless-shell> node academy/build/check-pages.js <page.html> ...
   Exit code 0 means no failure. Known exceptions and pending links are listed, not failed. */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const PAGES = path.join(__dirname, '..', 'pages');
const SHOTS = path.join(__dirname, '..', 'screenshots');
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.woff2': 'font/woff2', '.png': 'image/png' };

function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const f = path.join(PAGES, decodeURIComponent(req.url.split('?')[0].split('#')[0]));
      if (!f.startsWith(PAGES) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
      res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(res);
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

/* runs in the page: every check that needs the rendered page */
function inPage() {
  const out = { fail: [], known: [], pending: [], info: [] };
  const rgb = (s) => {
    let m = s.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);
    if (m) return [+m[1], +m[2], +m[3], m[4] == null ? 1 : +m[4]];
    m = s.match(/color\(srgb ([\d.e-]+) ([\d.e-]+) ([\d.e-]+)(?: \/ ([\d.e-]+))?\)/);
    if (m) return [m[1] * 255, m[2] * 255, m[3] * 255, m[4] == null ? 1 : +m[4]];
    return null;
  };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const over = (top, bot) => [0, 1, 2].map((i) => top[i] * top[3] + bot[i] * (1 - top[3])).concat(1);
  const bgOf = (node) => {
    const layers = [];
    for (let n = node; n && n.nodeType === 1; n = n.parentElement) {
      const c = rgb(getComputedStyle(n).backgroundColor);
      if (c && c[3] > 0) { layers.push(c); if (c[3] >= 1) break; }
    }
    let base = [255, 255, 255, 1];
    for (let i = layers.length - 1; i >= 0; i--) base = over(layers[i], base);
    return base;
  };
  const visible = (n) => { const r = n.getBoundingClientRect(); const s = getComputedStyle(n); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity !== 0; };

  // IDs
  const ids = {}; for (const n of document.querySelectorAll('[id]')) ids[n.id] = (ids[n.id] || 0) + 1;
  for (const [k, v] of Object.entries(ids)) if (v > 1) out.fail.push('ID used ' + v + ' times: ' + k);
  // anchors on this page and to other pages
  for (const a of document.querySelectorAll('a[href]')) {
    const h = a.getAttribute('href');
    if (h.startsWith('#')) { if (!document.getElementById(h.slice(1))) out.fail.push('Link to a missing anchor: ' + h); }
    else if (!/^https?:/.test(h)) out.info.push('LOCAL ' + h);
  }
  // the 9-step diagram
  const map = document.querySelector('[data-figure="builder"]');
  if (map) for (let s = 0; s <= 8; s++) {
    const a = map.querySelector('a[href="#step-' + s + '"]');
    if (!a) out.fail.push('The 9-step diagram has no link to step ' + s);
    else if (!document.getElementById('step-' + s)) out.fail.push('Step ' + s + ' has no part');
  }
  // text: contrast and size, HTML and SVG
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const t = walker.currentNode; if (!t.textContent.trim()) continue;
    const n = t.parentElement; if (!n || seen.has(n) || n.closest('#pop[hidden],script,style,[hidden],title')) continue; seen.add(n);
    if (!visible(n)) continue;
    const s = getComputedStyle(n);
    const svgText = n.closest('svg') && n.tagName.toLowerCase() !== 'svg';
    let size = parseFloat(s.fontSize);
    if (svgText) { const ctm = n.getScreenCTM && n.getScreenCTM(); if (ctm) size *= Math.hypot(ctm.a, ctm.b); }
    const where = (n.id ? '#' + n.id : n.tagName.toLowerCase() + (n.className && n.className.baseVal == null ? '.' + String(n.className).split(' ').join('.') : '')) + ' "' + t.textContent.trim().slice(0, 30) + '"';
    if (size < 11.9) out.fail.push('Text below 12 px (' + size.toFixed(1) + '): ' + where);
    const fg = rgb(svgText ? s.fill : s.color); if (!fg) continue;
    let bg = bgOf(svgText ? n.closest('figure, .frame, .case, main, body') : n);
    if (svgText) {   // a text drawn on a filled shape: the shape is its background
      const kids = n.parentElement && n.parentElement.tagName.toLowerCase() === 'g' ? [...n.parentElement.children].filter((c) => /^(rect|path|circle)$/.test(c.tagName)) : [];
      const main = kids.find((c) => c.classList.contains('sh')) || kids[0];
      const shape = main && rgb(getComputedStyle(main).fill) ? main : null;
      if (shape) { const c = rgb(getComputedStyle(shape).fill); bg = c[3] < 1 ? over(c, bg) : c; }
    }
    const f2 = fg[3] < 1 ? over(fg, bg) : fg;
    const L1 = lum(f2), L2 = lum(bg), ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const large = size >= 24 || (size >= 18.66 && +s.fontWeight >= 700);
    const need = large ? 3 : 4.5;
    if (ratio < need) {
      const known = n.matches('.lk, .ls');
      (known ? out.known : out.fail).push('Contrast ' + ratio.toFixed(2) + ' < ' + need + ': ' + where);
    }
  }
  // word limits (decision 0026): figures and popups are not counted
  const words = (n) => { const c = n.cloneNode(true); c.querySelectorAll('figure, details, .sources, svg').forEach((x) => x.remove()); return (c.textContent.match(/\S+/g) || []).length; };
  for (const n of document.querySelectorAll('[data-level]')) {
    const lim = { overview: 100, explanation: 500 }[n.dataset.level]; if (!lim) continue;
    const w = words(n); const part = n.closest('[id]') ? n.closest('[id]').id : '?';
    out.info.push('WORDS ' + part + ' ' + n.dataset.level + ' ' + w + '/' + lim);
    if (w > lim) out.fail.push('Over the word limit: ' + part + ' ' + n.dataset.level + ' has ' + w + ' words, the limit is ' + lim);
  }
  return out;
}

(async () => {
  const pages = process.argv.slice(2);
  const srv = await serve();
  const base = 'http://127.0.0.1:' + srv.address().port + '/';
  const browser = await chromium.launch({ executablePath: process.env.CHROME });
  fs.mkdirSync(SHOTS, { recursive: true });
  let failures = 0;
  for (const name of pages) {
    for (const scheme of ['light', 'dark']) {
      for (const width of [1280, 390]) {
        const ctx = await browser.newContext({ colorScheme: scheme, viewport: { width, height: 900 }, reducedMotion: 'reduce' });
        const p = await ctx.newPage();
        const errors = [];
        p.on('console', (m) => { if (m.type() === 'error') errors.push('Console: ' + m.text()); });
        p.on('pageerror', (e) => errors.push('Page error: ' + e.message));
        await p.goto(base + name, { waitUntil: 'networkidle' });
        const tag = name.replace('.html', '') + ' ' + scheme + ' ' + width;
        if (width === 1280) await p.screenshot({ path: path.join(SHOTS, tag.replace(/ /g, '-') + '-top.png') });
        // open every part and level
        await p.evaluate(() => document.querySelectorAll('details').forEach((d) => { d.open = true; }));
        const r = await p.evaluate(inPage);
        const overflow = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        if (overflow > 1) r.fail.push('Sideways overflow of ' + overflow + ' px');
        // popups and preview cards
        const pops = await p.evaluate(async () => {
          const res = []; const pop = document.getElementById('pop'); if (!pop) return res;
          for (const el of document.querySelectorAll('[data-step],[data-card]')) {
            el.scrollIntoView({ block: 'center' }); el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
            await new Promise((ok) => requestAnimationFrame(ok));
            const b = pop.getBoundingClientRect(), id = el.dataset.step || el.dataset.card;
            if (pop.hidden || !document.getElementById('poptitle').textContent) res.push('Popup does not open: ' + id);
            else if (b.left < -1 || b.top < -1 || b.right > innerWidth + 1 || b.bottom > innerHeight + 1) res.push('Popup outside the window: ' + id);
            document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
          }
          return res;
        });
        r.fail.push(...pops, ...errors);
        // a link opens its part: load the page at each part anchor with all parts closed
        if (width === 1280 && scheme === 'light') {
          const anchors = await p.evaluate(() => [...document.querySelectorAll('details.part[id]')].map((d) => d.id));
          for (const id of anchors) {
            const q = await ctx.newPage();
            await q.goto(base + name + '#' + id, { waitUntil: 'networkidle' });
            const open = await q.evaluate((i) => document.getElementById(i).open, id);
            if (!open) r.fail.push('The link #' + id + ' does not open its part');
            await q.close();
          }
          const local = r.info.filter((x) => x.startsWith('LOCAL ')).map((x) => x.slice(6));
          for (const h of [...new Set(local)]) {
            const [file, hash] = h.split('#');
            if (!fs.existsSync(path.join(PAGES, file))) { r.pending.push('Link to a page that is not built yet: ' + h); continue; }
            if (hash) {
              const q = await ctx.newPage(); await q.goto(base + h, { waitUntil: 'networkidle' });
              if (!(await q.evaluate((i) => !!document.getElementById(i), hash))) r.fail.push('Link to a missing anchor: ' + h);
              await q.close();
            }
          }
          for (const x of r.info.filter((x) => x.startsWith('WORDS '))) console.log('  ' + x.slice(6));
        }
        console.log(tag + ': ' + r.fail.length + ' failures, ' + r.known.length + ' known exceptions, ' + r.pending.length + ' pending');
        for (const x of r.fail) console.log('  FAIL ' + x);
        for (const x of [...new Set(r.known)]) console.log('  known ' + x);
        for (const x of [...new Set(r.pending)]) console.log('  pending ' + x);
        failures += r.fail.length;
        await ctx.close();
      }
    }
  }
  await browser.close(); srv.close();
  console.log(failures ? 'FAILED: ' + failures : 'All checks passed.');
  process.exit(failures ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
