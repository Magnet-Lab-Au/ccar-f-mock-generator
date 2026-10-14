/* Check F1 (academy/check-plan.md): axe-core on both tabs in light and dark mode, with all parts open,
   and a walk with the Tab key through the page as it opens (parts closed).
   Run: AXE=<path to axe.min.js> node check-a11y.js <page.html> ...
   The contrast of the K and S letters (.lk, .ls) is a known exception (decisions 0009 and 0013). */
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');
(async () => {
  const axe = fs.readFileSync(process.env.AXE, 'utf8');
  const b = await chromium.launch({ executablePath: process.env.CHROME });
  for (const page of process.argv.slice(2)) {
    for (const scheme of ['light', 'dark']) {
      const ctx = await b.newContext({ colorScheme: scheme, viewport: { width: 1280, height: 900 }, bypassCSP: true, reducedMotion: 'reduce' });
      const p = await ctx.newPage();
      await p.goto('file://' + path.resolve(page));
      await p.evaluate(() => document.querySelectorAll('details').forEach((d) => { d.open = true; }));
      await p.addScriptTag({ content: axe });
      const r = await p.evaluate(async () => {
        const res = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } });
        return res.violations.map((v) => ({ id: v.id, impact: v.impact, help: v.help,
          nodes: v.nodes.map((n) => ({ target: n.target.join(' '), html: n.html.slice(0, 140), known: !!document.querySelector(n.target[0]) && document.querySelector(n.target[0]).matches('.lk, .ls, .lk *, .ls *') })) }));
      });
      console.log('\n## ' + path.basename(page) + ', ' + scheme + ' mode, axe-core');
      if (!r.length) console.log('No violations.');
      for (const v of r) {
        const real = v.nodes.filter((n) => !n.known), known = v.nodes.length - real.length;
        console.log('- ' + v.id + ' (' + v.impact + '): ' + v.help + '. ' + real.length + ' elements' + (known ? ', and ' + known + ' known exceptions' : ''));
        for (const n of real.slice(0, 6)) console.log('    ' + n.target + '  ' + n.html.replace(/\s+/g, ' '));
      }
      await ctx.close();
    }
    // The Tab key walk, light mode, page as it opens.
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    const p = await ctx.newPage();
    await p.goto('file://' + path.resolve(page));
    const seen = [], noring = [], hidden = [];
    let first = null;
    for (let i = 0; i < 3000; i++) {
      await p.keyboard.press('Tab');
      const f = await p.evaluate(() => {
        const e = document.activeElement;
        if (!e || e === document.body) return null;
        const cs = getComputedStyle(e), r = e.getBoundingClientRect();
        const sh = e.querySelector && e.querySelector('.sh');
        const shw = sh ? parseFloat(getComputedStyle(sh).strokeWidth) : 0;
        const ring = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || cs.boxShadow !== 'none' || shw >= 2.25;
        const key = e.tagName + '#' + (e.id || '') + '|' + (e.dataset.step || e.dataset.card || e.getAttribute('href') || e.textContent.trim().slice(0, 40));
        return { key, ring, visible: r.width > 0 && r.height > 0 };
      });
      if (!f) break;
      if (f.key === first) break;
      if (!first) first = f.key;
      seen.push(f.key);
      if (!f.ring) noring.push(f.key);
      if (!f.visible) hidden.push(f.key);
    }
    console.log('\n## ' + path.basename(page) + ', Tab key walk (light mode, parts closed)');
    console.log('Stops: ' + seen.length + '. Without a visible focus ring: ' + noring.length + '. Not visible on screen: ' + hidden.length + '.');
    for (const x of [...new Set(noring)].slice(0, 10)) console.log('    no ring: ' + x);
    for (const x of [...new Set(hidden)].slice(0, 10)) console.log('    hidden: ' + x);
    await ctx.close();
  }
  await b.close();
})();
