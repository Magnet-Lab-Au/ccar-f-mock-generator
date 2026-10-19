/* Check the academy pages in a headless browser (decisions 0013, 0015, 0017, 0026 and 0033).

   For each page, in light and in dark mode, at 1280 and 390 pixels wide, with every part open:
   - no console error, no page error and no breach of the security policy
   - no sideways overflow of the page
   - each ID once only
   - each link to an anchor finds its target, and a link to a part opens that part
   - each step of the 9-step diagram has its part
   - each popup and preview card opens, has a title and stays inside the window
   - text contrast at least 4.5 to 1 (3 to 1 for large text), with the known exceptions of decisions 0009 and 0013
   - the same text checks in both panels of each before / after figure, for each choice of each live figure, and at each step of each stepper, with the opacity of each part and its parents, and each step shows only its own caption
   - each text at least 12 pixels high as rendered, also in the figures
   - the word limits of decision 0026: Overview at most 100 words, Explanation at most 500 words, figures not counted
   - each card that quotes a file of this repository: the quote is on the linked lines at the tag of the link (decision 0054)
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
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.ts': 'text/javascript', '.woff2': 'font/woff2', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml' };

function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      let u = decodeURIComponent(req.url.split('?')[0].split('#')[0]);
      if (u.startsWith('/academy/')) u = '/portal/public' + u;   // the images of the portal form, at /academy/ as in the portal
      const f = path.join(PAGES, u);
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
    // with the popups of Fig. A (owner, 15 October 2026) the link to the step is inside the popup of the box
    const pops = (window.ACADEMY && window.ACADEMY.pop) || {};
    const inPop = [...map.querySelectorAll('[data-step]')].some((n) => ((pops[n.dataset.step] || {}).links || []).some((l) => l.href === '#step-' + s));
    if (!a && !inPop) out.fail.push('The 9-step diagram has no link to step ' + s);
    else if (!document.getElementById('step-' + s)) out.fail.push('Step ' + s + ' has no part');
  }
  // text: contrast and size, HTML and SVG
  const checkText = (rootNode, pre) => {
  const fail0 = out.fail.length, known0 = out.known.length;
  const walker = document.createTreeWalker(rootNode, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const t = walker.currentNode; if (!t.textContent.trim()) continue;
    const n = t.parentElement; if (!n || seen.has(n) || n.closest('#pop[hidden],script,style,[hidden],title')) continue; seen.add(n);
    if (!visible(n)) continue;
    let op = 1; for (let x = n; x && x.nodeType === 1; x = x.parentElement) op *= +getComputedStyle(x).opacity;   // a faded part fades its text too
    if (op < 0.01) continue;
    const s = getComputedStyle(n);
    const svgText = n.closest('svg') && n.tagName.toLowerCase() !== 'svg';
    let size = parseFloat(s.fontSize);
    if (svgText) { const ctm = n.getScreenCTM && n.getScreenCTM(); if (ctm) size *= Math.hypot(ctm.a, ctm.b); }
    const where = (n.id ? '#' + n.id : n.tagName.toLowerCase() + (n.className && n.className.baseVal == null ? '.' + String(n.className).split(' ').join('.') : '')) + ' "' + t.textContent.trim().slice(0, 30) + '"';
    if (size < 11.9) out.fail.push('Text below 12 px (' + size.toFixed(1) + '): ' + where);
    const fg0 = rgb(svgText ? s.fill : s.color); if (!fg0) continue;
    const fg = [fg0[0], fg0[1], fg0[2], fg0[3] * op];
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
  if (pre) { for (let i = fail0; i < out.fail.length; i++) out.fail[i] = pre + out.fail[i]; for (let i = known0; i < out.known.length; i++) out.known[i] = pre + out.known[i]; }
  };
  checkText(document.body, '');
  // each step of each stepper (figure plan, plan review item 2): the check above sees only the full picture
  for (const root of document.querySelectorAll('.ve-steps')) {
    const caps = [...root.querySelectorAll('.ve-cap li')], next = root.querySelector('[data-go="1"]'), prev = root.querySelector('[data-go="-1"]');
    const name = root.id || (root.querySelector('.fig-n') || {}).textContent || 'a stepper';
    if (!caps.length || !next || !prev) { out.fail.push('Stepper without captions or arrows: ' + name); continue; }
    for (let k = 1; k < caps.length; k++) {
      next.click();
      const shown = caps.filter((c) => !c.hidden);
      if (shown.length !== 1 || shown[0] !== caps[k]) out.fail.push('Stepper ' + name + ': step ' + k + ' does not show only its own caption');
      checkText(root, 'Stepper ' + name + ', step ' + k + ': ');
    }
    for (let k = 1; k < caps.length; k++) prev.click();
    out.info.push('STEPPER ' + name + ': ' + (caps.length - 1) + ' steps checked');
    if (caps[0].hidden) out.fail.push('Stepper ' + name + ' does not go back to the full picture');
  }
  // each panel of each before / after figure (plan review item 2)
  for (const fig of document.querySelectorAll('.ve-ba')) {
    const name = (fig.querySelector('.fig-n') || {}).textContent || 'a before / after figure';
    const buttons = [...fig.querySelectorAll('.ve-toggle button')], panels = [...fig.querySelectorAll('.ba-panel')];
    if (buttons.length !== 2 || panels.length !== 2) { out.fail.push('Before / after without two buttons and two panels: ' + name); continue; }
    buttons.forEach((b, i) => {
      b.click();
      if (panels[i].hidden || !panels[1 - i].hidden) out.fail.push(name + ': button ' + (i + 1) + ' does not show only its panel');
      checkText(fig, name + ', panel ' + (i + 1) + ': ');
    });
    buttons[1].click();
    out.info.push('TOGGLE ' + name + ': 2 panels checked');
  }
  // each choice of each live figure (plan review item 2)
  for (const fig of document.querySelectorAll('.ve-live')) {
    const name = (fig.querySelector('.fig-n') || {}).textContent || 'a live figure';
    const buttons = [...fig.querySelectorAll('.ve-toggle button')], say = fig.querySelector('.ve-say');
    if (!buttons.length || !say) { out.fail.push('Live figure without buttons or a sentence: ' + name); continue; }
    const items = [...fig.querySelectorAll('[data-pick]')];
    buttons.forEach((b, i) => {
      b.click();
      const k = +b.dataset.i, want = k >= 0 ? items[k].dataset.say : say.dataset.all;
      if (say.textContent !== want) out.fail.push(name + ': choice ' + (i + 1) + ' shows the wrong sentence');
      if (k >= 0 && !items[k].classList.contains('sel')) out.fail.push(name + ': choice ' + (i + 1) + ' does not light its part');
      if (k < 0 && fig.querySelector('.sel, .dim')) out.fail.push(name + ': the choice for all does not reset the figure');
      checkText(fig, name + ', choice ' + (i + 1) + ': ');
    });
    (buttons.find((b) => +b.dataset.i < 0) || buttons[buttons.length - 1]).click();
    out.info.push('LIVE ' + name + ': ' + buttons.length + ' choices checked');
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

/* Decision 0054: each card that quotes a file of this repository links to the lines of its quote at a tag.
   Read each linked file at its tag (from GitHub, or from the local git with ACADEMY_SOURCE=git) and confirm that the quote
   is on the linked lines. A card of the kind "count" states a result, not a quote, so it is not checked here. */
const REPO_BLOB = 'https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/';
const RAW = 'https://raw.githubusercontent.com/Magnet-Lab-Au/ccar-f-mock-generator/';
const CACHE = path.join(__dirname, '.cache');
const ROOT = path.join(__dirname, '..', '..');
const tagText = {};
async function atTag(ref, file) {
  const key = ref + ':' + file;
  if (!(key in tagText)) {
    let data = null;
    const local = path.join(CACHE, ref, file);
    if (process.env.ACADEMY_SOURCE === 'git') {
      try { data = require('child_process').execFileSync('git', ['-C', ROOT, 'show', ref + ':' + file], { maxBuffer: 1 << 28 }); } catch (e) { data = null; }
    } else if (fs.existsSync(local)) {
      data = fs.readFileSync(local);
    } else {
      const r = await fetch(RAW + ref + '/' + file.split('/').map(encodeURIComponent).join('/'));
      if (r.ok) { data = Buffer.from(await r.arrayBuffer()); fs.mkdirSync(path.dirname(local), { recursive: true }); fs.writeFileSync(local, data); }
      else if (r.status !== 404) throw new Error('GitHub ' + r.status + ' for ' + key);
    }
    tagText[key] = data === null ? null : data.toString('utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  }
  return tagText[key];
}
// the form that the portal relies on (the portal session, 19 October 2026). If a change of the form is intended,
// write it in academy/portal-plan.md, "The portal form as built", change this check, and tell the portal session,
// so that it changes its React page in the same round.
const TABS = ['exam-guide-breakdown', 'behind-the-mocks'];
function checkForm() {
  const fail = [], dir = path.join(PAGES, 'portal'), read = (f) => fs.readFileSync(path.join(dir, f), 'utf8');
  const want = ['src/academy.ts', ...TABS.flatMap((t) => ['.body.html', '.data.ts', '.css'].map((x) => 'src/' + t + x))];
  for (const f of want) if (!fs.existsSync(path.join(dir, f))) fail.push('Missing file: ' + f);
  for (const f of fs.readdirSync(path.join(dir, 'src'))) if (!want.includes('src/' + f)) fail.push('A file that the portal does not know: src/' + f);
  if (!fs.existsSync(path.join(dir, 'public', 'academy'))) fail.push('Missing folder: public/academy/');
  for (const f of fs.readdirSync(path.join(dir, 'public'))) if (f !== 'academy') fail.push('A file outside public/academy/: public/' + f);
  if (fail.length) return fail;
  const ts = read('src/academy.ts');
  for (const [what, re] of [
    ['export { academyStart as start }', /^export \{ academyStart as start \};$/m],
    ['function academyStart(root, data)', /^function academyStart\(root, data\) \{$/m],
    ['start returns stop', /^  return stop;$/m],
    ['stop.open(id)', /^  stop\.open = \(id\) => /m],
  ]) if (!re.test(ts)) fail.push('academy.ts lacks ' + what);
  if ((ts.match(/^export /gm) || []).length !== 1) fail.push('academy.ts has more than one export');
  for (const t of TABS) {
    const data = read('src/' + t + '.data.ts'), css = read('src/' + t + '.css'), body = read('src/' + t + '.body.html');
    if (!/^export default data;$/m.test(data) || (data.match(/^export /gm) || []).length !== 1) fail.push(t + '.data.ts: the only export must be export default data');
    if (/@font-face/.test(css)) fail.push(t + '.css has @font-face rules: the portal loads the fonts');
    // each style rule is scoped to the root classes academy-page ap-<tab>
    const scope = '.academy-page.ap-' + t;
    const flat = css.replace(/\/\*[\s\S]*?\*\//g, '').replace(/@keyframes[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}/g, '');
    for (const m of flat.matchAll(/([^{}@;]+)\{[^{}]*\}/g)) {
      const sel = m[1].trim();
      if (!sel || /^(from|to|\d+%)/.test(sel)) continue;
      // split at the top-level commas only, not the commas inside :is(...) or :not(...)
      const parts = []; let depth = 0, cur = '';
      for (const ch of sel) { if (ch === '(') depth++; if (ch === ')') depth--; if (ch === ',' && !depth) { parts.push(cur); cur = ''; } else cur += ch; }
      parts.push(cur);
      for (const one of parts) if (!one.includes(scope)) { fail.push(t + '.css: a rule outside ' + scope + ': ' + one.trim().slice(0, 80)); break; }
    }
    // links to the other tab go through the routes of the portal, and images live under /academy/
    for (const [f, text] of [[t + '.body.html', body], [t + '.data.ts', data]]) {
      // in the data, "src" names the source of a card, so only "href" is a link there
      const urls = [...text.matchAll(/(?:href|src)=\\?"([^"\\]*)|"href": ?"([^"\\]*)/g)].map((m) => m[1] ?? m[2]);
      for (const u of new Set(urls)) {
        if (/^(#|https:\/\/|mailto:|data:)/.test(u)) continue;
        if (/^\/(exam-guide-breakdown|behind-the-mocks)(#[\w.-]+)?$/.test(u)) continue;
        if (/^\/(start-here|study-with-claude|exam-traps)$/.test(u)) continue;   // the tabs that the portal makes itself (decisions 0059 and 0060)
        if (/^\/academy\/[\w./-]+$/.test(u)) { if (!fs.existsSync(path.join(dir, 'public', u))) fail.push(f + ': missing image ' + u); continue; }
        fail.push(f + ': a link or image in a form that the portal does not know: ' + u);
      }
    }
  }
  return fail;
}

async function checkQuotes(name) {
  const fail = [], summary = [];
  let checked = 0;
  if (name.startsWith('portal/')) {
    // the portal form: the same cards and popups as the page that opens alone, apart from the routes between the tabs
    const tab = path.basename(name, '.html');
    const load = (code, key) => { const c = { window: {} }; require('vm').runInNewContext(code, c); return c.window[key]; };
    const alone = fs.readFileSync(path.join(PAGES, tab + '.js'), 'utf8'), k = alone.indexOf('window.ACADEMY =');
    const a = load(alone.slice(k, alone.indexOf('\n', k)), 'ACADEMY');
    const ts = fs.readFileSync(path.join(PAGES, 'portal', 'src', tab + '.data.ts'), 'utf8'), m = ts.indexOf('const data = ');
    const b = load('window.D = ' + ts.slice(m + 13, ts.lastIndexOf('export default')), 'D');
    const route = (s) => s.replace(/(exam-guide-breakdown|behind-the-mocks)\.html/g, '/$1');
    for (const part of ['card', 'pop']) for (const id of new Set([...Object.keys(a[part]), ...Object.keys(b[part] || {})])) {
      if (route(JSON.stringify(a[part][id])) !== JSON.stringify((b[part] || {})[id])) fail.push('The portal form differs in ' + part + ' ' + id); else checked++;
    }
    return { fail, checked, summary, same: true };
  }
  const src = fs.readFileSync(path.join(PAGES, name.replace('.html', '.js')), 'utf8');
  const i = src.indexOf('window.ACADEMY =');
  const ctx = { window: {} };
  require('vm').runInNewContext(src.slice(i, src.indexOf('\n', i)), ctx);
  for (const [id, c] of Object.entries(ctx.window.ACADEMY.card)) {
    if (c.kind === 'count' || !c.href || !c.href.startsWith(REPO_BLOB)) continue;
    const m = c.href.slice(REPO_BLOB.length).match(/^([^/]+)\/([^?#]+)(?:\?plain=1)?#L(\d+)(?:-L(\d+))?$/);
    if (!m) continue;
    const [, ref, file, a, b] = m;
    if (ref !== 'mocks-v2' && !/^pages-/.test(ref)) { fail.push('Card ' + id + ' links to ' + ref + ', not to a tag'); continue; }
    const text = await atTag(ref, decodeURIComponent(file));
    if (text === null) { fail.push('Card ' + id + ': ' + file + ' is not at the tag ' + ref); continue; }
    const lines = text.split('\n').slice(+a - 1, +(b || a));
    const block = lines.join('\n');
    // the forms of a quote: word for word; inside a JSON string; code with its indent removed; the points of a task statement
    const asJson = JSON.stringify(c.text).slice(1, -1);
    const indent = Math.min(...lines.filter((l) => l.trim()).map((l) => l.length - l.trimStart().length));
    let ok = block.includes(c.text) || block.includes(asJson) || lines.map((l) => l.slice(indent)).join('\n') === c.text;
    if (!ok && c.kind === 'guide' && c.text.includes(' points: ')) ok = c.text.split(' points: ')[1].split(' / ').every((p) => block.includes(p));
    // a summary card names a record by its ID, and its link goes to the line of that ID
    if (!ok && (c.text.match(/\b[A-Z0-9]+(?:-[A-Z0-9]+){2,}\b/g) || []).some((x) => block.includes('"' + x + '"'))) { summary.push(id); checked++; continue; }
    if (!ok) fail.push('Card ' + id + ': the quote is not on ' + file + ' lines ' + a + (b ? ' to ' + b : '') + ' at ' + ref);
    checked++;
  }
  return { fail, checked, summary };
}

// a link lands on its part: when the scroll has stopped, the top of the part is at its scroll margin, or the page is at its end
async function landing(q, id) {
  return q.evaluate(async (i) => {
    await document.fonts.ready;
    let last = -1;
    for (let n = 0; n < 60 && scrollY !== last; n++) { last = scrollY; await new Promise((ok) => setTimeout(ok, 100)); }
    const t = document.getElementById(i), top = t.getBoundingClientRect().top, margin = parseFloat(getComputedStyle(t).scrollMarginTop) || 0;
    const end = scrollY >= document.documentElement.scrollHeight - innerHeight - 2;
    return Math.abs(top - margin) <= 2 || (end && top >= margin - 2 && top < innerHeight) ? null : 'The link #' + i + ' lands ' + Math.round(top - margin) + ' px from its part';
  }, id);
}

(async () => {
  const pages = process.argv.slice(2);
  let quoteFailures = 0;
  for (const name of pages) {
    const q = await checkQuotes(name);
    if (q.same) console.log(name + ': ' + q.checked + ' cards and popups the same as in the page that opens alone, ' + q.fail.length + ' failures');
    else console.log(name + ' quotes: ' + q.checked + ' cards checked at their tag, ' + q.fail.length + ' failures. ' + q.summary.length + ' of the checked cards are summaries, found at the line of their ID' + (q.summary.length ? ': ' + q.summary.join(', ') : '') + '.');
    for (const x of q.fail) console.log('  FAIL ' + x);
    quoteFailures += q.fail.length;
  }
  if (pages.some((n) => n.startsWith('portal/'))) {
    const form = checkForm();
    console.log('The form for the portal: ' + form.length + ' failures');
    for (const x of form) console.log('  FAIL ' + x + ' (a change of the form needs a note for the portal session)');
    quoteFailures += form.length;
  }
  const srv = await serve();
  const base = 'http://127.0.0.1:' + srv.address().port + '/';
  const browser = await chromium.launch({ executablePath: process.env.CHROME });
  fs.mkdirSync(SHOTS, { recursive: true });
  let failures = quoteFailures;
  for (const name of pages) {
    const portal = name.startsWith('portal/');
    if (portal && !fs.existsSync(path.join(PAGES, 'portal', 'preview', 'preflight.css'))) { console.log('  FAIL ' + name + ': no preflight.css, so the test page lacks the base styles of the portal'); failures++; }
    // the portal form also at 1024 px, where the side bar of the portal leaves the page least room, and once with motion on
    const runs = [];
    for (const scheme of ['light', 'dark']) for (const width of portal ? [1280, 1024, 390] : [1280, 390]) runs.push({ scheme, width, motion: false });
    if (portal) runs.push({ scheme: 'light', width: 1280, motion: true });
    for (const { scheme, width, motion } of runs) {
      {
        const ctx = await browser.newContext({ colorScheme: scheme, viewport: { width, height: 900 }, reducedMotion: motion ? 'no-preference' : 'reduce' });
        const p = await ctx.newPage();
        const errors = [];
        p.on('console', (m) => { if (m.type() === 'error') errors.push('Console: ' + m.text()); });
        p.on('pageerror', (e) => errors.push('Page error: ' + e.message));
        await p.goto(base + name, { waitUntil: 'networkidle' });
        const tag = name.replace('.html', '') + ' ' + scheme + ' ' + width + (motion ? ' motion' : '');
        if (width === 1280) await p.screenshot({ path: path.join(SHOTS, tag.replace(/ /g, '-') + '-top.png') });
        // open every part and level
        await p.evaluate(() => document.querySelectorAll('details').forEach((d) => { d.open = true; }));
        let r = await p.evaluate(inPage);
        // with motion on, a part that has not come on the screen is still hidden, so only the errors and the overflow count
        if (motion) r = { fail: [], known: [], pending: [], info: [] };
        const overflow = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        if (overflow > 1) r.fail.push('Sideways overflow of ' + overflow + ' px');
        if (portal) {
          // nothing may reach out of the page element into the padding of the portal, except inside a scroll box or a fixed box
          let out = await p.evaluate(() => {
            const ap = document.getElementById('ap'), edge = ap.getBoundingClientRect().right + 1, res = [], tilted = [];
            for (const n of ap.querySelectorAll('*')) {
              const b = n.getBoundingClientRect();
              if (b.width === 0 || b.right <= edge) continue;
              let skip = false, turn = false;
              for (let q = n; q && q !== ap; q = q.parentElement) { const s = getComputedStyle(q); if (s.position === 'fixed' || s.overflowX !== 'visible') { skip = true; break; } if (s.transform !== 'none') turn = true; }
              // a tilted mark, such as the notepad of tab 1, has a turned box whose corner may pass the edge by a few pixels
              if (!skip) (turn && b.right - edge < 8 ? tilted : res).push((n.id ? '#' + n.id : n.tagName.toLowerCase() + (n.className && n.className.baseVal === undefined ? '.' + String(n.className).split(' ')[0] : '')) + ' by ' + Math.round(b.right - edge + 1) + ' px');
            }
            return { res, tilted };
          });
          for (const x of new Set(out.tilted)) r.known.push('A tilted mark passes the page edge: ' + x);
          out = out.res;
          for (const x of [...new Set(out)].slice(0, 10)) r.fail.push('Reaches out of the page element: ' + x);
          if (out.length > 10) r.fail.push('Reaches out of the page element: ' + (out.length - 10) + ' more');
        }
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
        if (width === 1280 && scheme === 'light' && !motion) {
          const anchors = await p.evaluate(() => [...document.querySelectorAll('details.part[id]')].map((d) => d.id));
          for (const id of anchors) {
            const q = await ctx.newPage();
            await q.goto(base + name + '#' + id, { waitUntil: 'networkidle' });
            const open = await q.evaluate((i) => document.getElementById(i).open, id);
            if (!open) r.fail.push('The link #' + id + ' does not open its part');
            const land = await landing(q, id); if (land) r.fail.push(land);
            await q.close();
          }
          const local = r.info.filter((x) => x.startsWith('LOCAL ')).map((x) => x.slice(6));
          for (const h of [...new Set(local)]) {
            let [file, hash] = h.split('#');
            if (/^\/(start-here|study-with-claude|exam-traps)$/.test(file)) continue;   // a tab that only the portal has (decisions 0059 and 0060)
            if (/^\/(exam-guide-breakdown|behind-the-mocks)$/.test(file)) file = 'portal/preview' + file + '.html';   // a route of the portal form
            else if (name.includes('/')) file = path.posix.join(path.posix.dirname(name), file);
            if (!fs.existsSync(path.join(PAGES, file))) { r.pending.push('Link to a page that is not built yet: ' + h); continue; }
            if (hash) {
              const q = await ctx.newPage(); await q.goto(base + file + '#' + hash, { waitUntil: 'networkidle' });
              if (!(await q.evaluate((i) => !!document.getElementById(i), hash))) r.fail.push('Link to a missing anchor: ' + h);
              await q.close();
            }
          }
          for (const x of r.info.filter((x) => x.startsWith('WORDS '))) console.log('  ' + x.slice(6));
          for (const x of r.info.filter((x) => x.startsWith('STEPPER ') || x.startsWith('TOGGLE ') || x.startsWith('LIVE '))) console.log('  ' + x);
        }
        // with motion on, the scroll is smooth: the first, a middle and the last part must still land on their part,
        // also when the fonts arrive 2 seconds late, in a new context with the scheme and motion of this run
        if (motion || (portal && width === 1280 && scheme === 'light')) {
          const anchors = await p.evaluate(() => [...document.querySelectorAll('details.part[id]')].map((d) => d.id));
          for (const slow of [false, true]) {
            const c2 = await browser.newContext({ colorScheme: scheme, viewport: { width, height: 900 }, reducedMotion: motion ? 'no-preference' : 'reduce' });
            if (slow) await c2.route('**/*.woff2', async (rt) => { await new Promise((ok) => setTimeout(ok, 2000)); await rt.continue(); });
            for (const id of new Set([anchors[0], anchors[anchors.length >> 1], anchors[anchors.length - 1]].filter(Boolean))) {
              const q = await c2.newPage();
              await q.goto(base + name + '#' + id, { waitUntil: 'networkidle' });
              const land = await landing(q, id); if (land) r.fail.push(land + (motion ? ' (motion on' : ' (motion off') + (slow ? ', fonts 2 s late)' : ')'));
              await q.close();
            }
            await c2.close();
          }
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
