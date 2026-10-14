/* Writes the text of each part of a tab as plain Markdown, for the reader checks (academy/check-plan.md).
   Run: node extract-text.js <page.html> <out-dir>
   For each part (the top, each domain summary and each closed part) it writes:
     <part>.md        the full text: headings, text of all levels, figure captions and step captions,
                      the labels inside each figure, and the popups of the boxes of the figures
     <part>.skim.md   only the headings, the figure labels and the captions (check C2)
     <part>.cards.md  the preview cards that the part links to (titles and texts)
   Hidden text (steps that are not current, closed levels) is included: it is text that a reader can open. */
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');
(async () => {
  const [page, out] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ executablePath: process.env.CHROME });
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(page));
  const parts = await p.evaluate(() => {
    const A = window.ACADEMY || { pop: {}, card: {} };
    const BLOCK = /^(P|LI|H[1-6]|FIGCAPTION|DIV|TD|TH|TR|DT|DD|BR|PRE|SUMMARY|SECTION|DETAILS|FIGURE|UL|OL|TABLE|BLOCKQUOTE|HEADER)$/;
    function text(node) {
      let s = '';
      node.childNodes.forEach((c) => {
        if (c.nodeType === 3) { s += c.textContent; return; }
        if (c.nodeType !== 1) return;
        const t = c.tagName;
        if (t === 'SCRIPT' || t === 'STYLE' || t === 'svg' || t === 'SVG' || t === 'BUTTON') return;
        if (c.classList.contains('sources')) return;
        let pre = '', post = '';
        if (/^H[1-6]$/.test(t)) { pre = '\n\n' + '#'.repeat(+t[1]) + ' '; post = '\n'; }
        else if (t === 'SUMMARY') { pre = '\n\n## '; post = '\n'; }
        else if (t === 'LI' && c.parentElement.classList.contains('ve-cap')) { pre = '\n[Step caption] '; }
        else if (t === 'LI') { pre = '\n- '; }
        else if (t === 'FIGCAPTION') { pre = '\n[Caption] '; post = '\n'; }
        else if (t === 'TD' || t === 'TH') { pre = ' | '; }
        else if (BLOCK.test(t)) { pre = '\n'; post = '\n'; }
        s += pre + text(c) + post;
      });
      return s;
    }
    function labels(fig) {
      const out = [];
      fig.querySelectorAll('svg').forEach((svg) => {
        const l = [];
        svg.querySelectorAll('text').forEach((x) => { const v = x.textContent.trim(); if (v) l.push(v); });
        if (l.length) out.push(l.join(' · '));
      });
      return out.join('\n');
    }
    const clean = (s) => s.replace(/[ \t]+/g, ' ').replace(/\n /g, '\n').replace(/\n{3,}/g, '\n\n').trim();
    const roots = [...document.querySelectorAll('header#top, section.parts, details.part')];
    return roots.map((r0) => {
      const id = r0.id || 'part';
      let r = r0;
      if (r0.matches('section.parts')) { r = r0.cloneNode(true); r.querySelectorAll('details.part').forEach((x) => x.remove()); }
      let full = text(r);
      const figs = [...r.querySelectorAll('figure')];
      let figtext = '';
      figs.forEach((f) => {
        const cap = f.querySelector('figcaption');
        figtext += '\n\n### Figure labels: ' + (cap ? cap.textContent.trim().slice(0, 80) : '(no caption)') + '\n' + labels(f);
      });
      const pops = [...r.querySelectorAll('[data-step]')].map((x) => {
        const d = A.pop[x.dataset.step]; if (!d) return '';
        const ex = d.example ? '\n  ' + (d.examplehead || 'Example') + ':\n```\n' + (typeof d.example === 'string' ? d.example : JSON.stringify(d.example, null, 1)) + '\n```' + (d.examplenote ? '\n  ' + d.examplenote : '') : '';
        return '\n- Popup on "' + (d.who || '') + '": ' + (d.title || '') + '. ' + (d.sent || []).join(' ') + ex;
      }).join('');
      const cards = [...new Set([...r.querySelectorAll('[data-card]')].map((x) => x.dataset.card))].map((k) => {
        const d = A.card[k]; if (!d) return '';
        return '\n\n## Card ' + k + ': ' + d.title + '\n' + (d.text || '');
      }).join('');
      let skim = '';
      r.querySelectorAll('h1,h2,h3,h4,figcaption,ol.ve-cap li,p.cap').forEach((h) => {
        const t = h.tagName === 'FIGCAPTION' ? '[Caption] ' : (h.tagName === 'LI' ? '[Step caption] ' : (h.tagName === 'P' ? '[Panel caption] ' : '# '));
        skim += '\n' + t + h.textContent.trim();
      });
      skim += figtext;
      return { id, full: clean(full) + '\n\n## Figure labels' + figtext + (pops ? '\n\n## Popups on the figures' + pops : ''), skim: clean(skim), cards: clean(cards) };
    });
  });
  for (const x of parts) {
    fs.writeFileSync(path.join(out, x.id + '.md'), x.full + '\n');
    fs.writeFileSync(path.join(out, x.id + '.skim.md'), x.skim + '\n');
    if (x.cards) fs.writeFileSync(path.join(out, x.id + '.cards.md'), x.cards + '\n');
  }
  console.log('Wrote ' + parts.length + ' parts to ' + out);
  await b.close();
})();
