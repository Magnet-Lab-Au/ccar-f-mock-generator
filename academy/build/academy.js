/* The shared behavior of the academy pages: the light and dark button, popups and preview cards, linked
   highlighting, steppers, and the closed parts that a link opens (decisions 0010, 0017 and 0033).
   The page script puts window.ACADEMY = {pop: {...}, card: {...}} in front of this code, so each tab
   has one script file and no inline script. */
(function () {
  try { var t = localStorage.getItem('academy-theme'); if (t === 'dark' || t === 'light') document.documentElement.classList.add(t); } catch (e) {}
})();
document.addEventListener('DOMContentLoaded', function () {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const POP = (window.ACADEMY && window.ACADEMY.pop) || {}, CARD = (window.ACADEMY && window.ACADEMY.card) || {};

  /* the light and dark button */
  (() => {
    const root = document.documentElement, btn = document.getElementById('theme-btn');
    if (!btn) return;
    const device = matchMedia('(prefers-color-scheme: dark)');
    const dark = () => root.classList.contains('dark') || (!root.classList.contains('light') && device.matches);
    const label = () => { btn.textContent = dark() ? 'Light mode' : 'Dark mode'; };
    btn.addEventListener('click', () => {
      const next = dark() ? 'light' : 'dark';
      root.classList.remove('light', 'dark'); root.classList.add(next);
      try { localStorage.setItem('academy-theme', next); } catch (e) {}
      label();
    });
    device.addEventListener('change', label);
    label();
  })();

  /* a link opens its part: the closed details that hold the target open, then the page scrolls to it */
  const openTo = (id, scroll) => {
    const t = id && document.getElementById(id);
    if (!t) return;
    for (let d = t; d; d = d.parentElement) if (d.tagName === 'DETAILS') d.open = true;
    if (scroll) t.scrollIntoView({ block: 'start', behavior: still ? 'auto' : 'smooth' });
  };
  const fromHash = () => { try { openTo(decodeURIComponent(location.hash.slice(1)), true); } catch (e) {} };
  addEventListener('hashchange', fromHash);
  fromHash();
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (a && a.getAttribute('href') === location.hash) openTo(a.getAttribute('href').slice(1), true);
  });

  /* popups (data-step) and preview cards (data-card) */
  const pop = document.getElementById('pop');
  const OPEN_DELAY = 300, CLOSE_DELAY = 350, GAP = 10, EDGE = 8;
  let current = null, pinned = false, openTimer = null, closeTimer = null;
  const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
  function fillStep(d) {
    const who = document.getElementById('popwho'); who.className = 'tag t-' + d.cls; who.textContent = d.who;
    document.getElementById('poptitle').textContent = d.title;
    const s = document.getElementById('popbody'); s.textContent = '';
    d.sent.forEach((t) => s.appendChild(el('p', null, t)));
    if (d.example) { s.appendChild(el('h3', null, d.examplehead)); s.appendChild(el('pre', null, d.example)); if (d.examplenote) s.appendChild(el('p', 'exnote', d.examplenote)); }
    if (d.points && d.points.length) {
      s.appendChild(el('h3', null, 'The exam guide says')); const key = el('p', 'key');
      if (d.points.some((p) => p.id.includes('-K'))) key.appendChild(el('span', 'tag-k', 'K = Knowledge of'));
      if (d.points.some((p) => p.id.includes('-S'))) key.appendChild(el('span', 'tag-s', 'S = Skills in'));
      s.appendChild(key); const ul = el('ul');
      d.points.forEach((p) => { const li = el('li'); const b = el('b'), m = p.id.match(/^(.*-)([KS])(.*)$/); if (m) b.append(m[1], el('span', m[2] === 'K' ? 'lk' : 'ls', m[2]), m[3] + ' '); else b.textContent = p.id + ' '; li.appendChild(b); li.appendChild(document.createTextNode(p.text)); li.appendChild(el('span', 'pctx', p.ctx)); ul.appendChild(li); });
      s.appendChild(ul);
    }
  }
  const KIND = { excerpt: 'Source', code: 'Code', guide: 'Exam guide', docs: 'Anthropic docs', count: 'Run records' };
  function fillCard(c) {
    const who = document.getElementById('popwho'); who.className = 'tag ' + (c.kind === 'code' ? 't-code' : c.kind === 'guide' ? 't-model' : '');
    who.textContent = KIND[c.kind] || 'Source';
    document.getElementById('poptitle').textContent = c.title;
    const s = document.getElementById('popbody'); s.textContent = '';
    if (c.kind === 'code') s.appendChild(el('pre', null, c.text)); else { const q = el('blockquote'); q.textContent = c.text; s.appendChild(q); }
    s.appendChild(el('p', 'csrc', c.src));
    if (c.href) { const a = el('a', 'open', c.kind === 'docs' ? 'Open the page' : 'Open in the repository'); a.href = c.href; a.target = '_blank'; a.rel = 'noopener'; s.appendChild(a); }
  }
  function place() {
    if (!current) return;
    const b = current.getBoundingClientRect(), vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
    const pw = pop.offsetWidth, ph = pop.offsetHeight; let left, top;
    if (current.classList.contains('fact')) { left = b.left; top = b.bottom + 6; if (top + ph > vh - EDGE) top = b.top - 6 - ph; }
    else if (b.right + GAP + pw <= vw - EDGE) { left = b.right + GAP; top = b.top; }
    else if (b.left - GAP - pw >= EDGE) { left = b.left - GAP - pw; top = b.top; }
    else if (b.bottom + GAP + ph <= vh - EDGE) { left = b.left; top = b.bottom + GAP; }
    else { left = b.left; top = b.top - GAP - ph; }
    pop.style.left = Math.max(EDGE, Math.min(left, vw - pw - EDGE)) + 'px';
    pop.style.top = Math.max(EDGE, Math.min(top, vh - ph - EDGE)) + 'px';
  }
  const setPinned = (v) => { pinned = v; document.getElementById('poppin').textContent = v ? 'kept open' : ''; };
  function open(t, pin) {
    clearTimeout(openTimer); clearTimeout(closeTimer);
    if (current && current !== t) current.setAttribute('aria-expanded', 'false');
    current = t;
    if (t.dataset.step) fillStep(POP[t.dataset.step]); else fillCard(CARD[t.dataset.card]);
    pop.hidden = false; pop.scrollTop = 0; t.setAttribute('aria-expanded', 'true'); setPinned(pin); place();
  }
  function close(returnFocus) {
    clearTimeout(openTimer); clearTimeout(closeTimer);
    if (!current) return;
    const t = current; t.setAttribute('aria-expanded', 'false'); pop.hidden = true; current = null; setPinned(false);
    if (returnFocus) t.focus({ preventScroll: true });
  }
  function scheduleClose() {
    clearTimeout(closeTimer); if (pinned) return;
    closeTimer = setTimeout(() => {
      if (pinned) return;
      if (current && (current.matches(':hover') || pop.matches(':hover'))) return;
      if (current && (document.activeElement === current || pop.contains(document.activeElement))) return;
      close(false);
    }, CLOSE_DELAY);
  }
  if (pop) {
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && current) { e.preventDefault(); close(true); } });
    document.querySelectorAll('[data-step],[data-card]').forEach((t) => {
      t.addEventListener('mouseenter', () => { clearTimeout(closeTimer); if (pinned || current === t) return; clearTimeout(openTimer); openTimer = setTimeout(() => { if (!pinned) open(t, false); }, OPEN_DELAY); });
      t.addEventListener('mouseleave', () => { clearTimeout(openTimer); scheduleClose(); });
      t.addEventListener('click', (e) => { e.stopPropagation(); e.preventDefault(); if (current === t && pinned) close(false); else open(t, true); });
      t.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (current === t && pinned) close(true); else open(t, true); } });
      t.addEventListener('blur', () => { if (!pinned) scheduleClose(); });
    });
    document.addEventListener('click', (e) => { if (current && !pop.contains(e.target)) close(false); });
    pop.addEventListener('mouseenter', () => clearTimeout(closeTimer));
    pop.addEventListener('mouseleave', scheduleClose);
    document.getElementById('popclose').addEventListener('click', (e) => { e.stopPropagation(); close(true); });
    addEventListener('scroll', place, true); addEventListener('resize', place);
  }

  /* linked highlighting */
  const linked = [...document.querySelectorAll('[data-ref]')], refs = (x) => x.dataset.ref.split(' ');
  let hovered = null, focused = null;
  const paint = () => {
    const keys = (hovered || focused)?.dataset.ref.split(' ') ?? [];
    for (const t of linked) t.classList.toggle('is-lit', refs(t).some((k) => keys.includes(k)));
    for (const svg of document.querySelectorAll('svg')) svg.classList.toggle('has-lit', !!svg.querySelector('.is-lit'));
  };
  for (const x of document.querySelectorAll('.ve-ref')) {
    x.addEventListener('pointerenter', () => { hovered = x; paint(); }); x.addEventListener('pointerleave', () => { hovered = null; paint(); });
    x.addEventListener('focus', () => { focused = x; paint(); }); x.addEventListener('blur', () => { focused = null; paint(); });
  }

  /* stepper: opens on the full picture (k = 0); the arrows go one step at a time; nothing plays by itself */
  for (const root of document.querySelectorAll('.ve-steps')) {
    const parts = [...root.querySelectorAll('[data-a]')], lines = [...root.querySelectorAll('[data-s]')], caps = [...root.querySelectorAll('.ve-cap li')];
    const n = caps.length; let i = 0;
    const show = (k) => {
      i = Math.max(0, Math.min(n - 1, k));
      const full = i === 0;
      for (const p of parts) p.classList.toggle('now', !full && p.dataset.a.split(' ').includes(String(i)));
      for (const l of lines) { l.classList.toggle('on', full || +l.dataset.s <= i); l.classList.toggle('now', !full && +l.dataset.s === i); }
      caps.forEach((c, j) => c.hidden = j !== i);
      root.classList.toggle('is-full', full); root.classList.toggle('is-step', !full);
      root.dispatchEvent(new Event('ve:step'));
    };
    root.addEventListener('click', (e) => { const b = e.target.closest('[data-go]'); if (b) show(i + +b.dataset.go); });
    show(0);
  }

  /* the glossary panel at the side (owner, 15 October 2026): a fixed button opens and closes it */
  const gBtn = document.querySelector('.glossary-btn'), gPan = document.getElementById('top-words');
  if (gBtn && gPan) {
    const gSet = (on) => { gPan.hidden = !on; gBtn.setAttribute('aria-expanded', String(on)); if (on) gPan.querySelector('.gp-close').focus(); };
    gBtn.addEventListener('click', () => gSet(gPan.hidden));
    gPan.querySelector('.gp-close').addEventListener('click', () => { gSet(false); gBtn.focus(); });
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && !gPan.hidden) { gSet(false); gBtn.focus(); } });
    const gHash = () => { if (location.hash === '#top-words') gSet(true); };
    addEventListener('hashchange', gHash);
    gHash();
  }

  /* before / after (decision 0037): with no script both panels show, and the script shows one panel and two buttons */
  for (const fig of document.querySelectorAll('.ve-ba')) {
    const panels = [...fig.querySelectorAll('.ba-panel')];
    if (panels.length !== 2) continue;
    const bar = document.createElement('div');
    bar.className = 've-toggle'; bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', 'Show before or after');
    panels.forEach((p, i) => { const b = document.createElement('button'); b.type = 'button'; b.dataset.i = i; b.textContent = p.dataset.label; bar.append(b); });
    const show = (k) => { panels.forEach((p, i) => { p.hidden = i !== k; }); [...bar.children].forEach((b, i) => b.setAttribute('aria-pressed', String(i === k))); };
    bar.addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) show(+b.dataset.i); });
    fig.insertBefore(bar, fig.firstChild);
    show(1);   // the answer first: the after panel
  }

  /* live figure (decision 0037): with no script the full picture shows, and the script adds one button for each example,
     and a choice lights that example and says what happens to it */
  for (const fig of document.querySelectorAll('.ve-live')) {
    const every = [...fig.querySelectorAll('[data-pick]')], targets = [...fig.querySelectorAll('[data-target]')], say = fig.querySelector('.ve-say');
    const items = every.filter((it, i) => every.findIndex((x) => x.dataset.pick === it.dataset.pick) === i);   // a phone drawing repeats each example (academy decision 0043)
    const target = targets.length > 0;
    if (!items.length || !say) continue;
    const bar = document.createElement('div');
    bar.className = 've-toggle'; bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', fig.dataset.controls || 'Choose an example');
    items.forEach((it, i) => { const b = document.createElement('button'); b.type = 'button'; b.dataset.i = i; b.textContent = it.dataset.pick; bar.append(b); });
    const all = document.createElement('button'); all.type = 'button'; all.dataset.i = -1; all.textContent = fig.dataset.allLabel || 'All'; bar.append(all);
    const show = (k) => {
      const pick = k >= 0 ? items[k].dataset.pick : null;
      every.forEach((it) => { it.classList.toggle('sel', it.dataset.pick === pick); it.classList.toggle('dim', k >= 0 && it.dataset.pick !== pick); });
      targets.forEach((t) => { t.classList.toggle('on', k >= 0 && items[k].dataset.match === 'yes'); t.classList.toggle('dim', k >= 0 && items[k].dataset.match !== 'yes'); });
      say.textContent = k >= 0 ? items[k].dataset.say : say.dataset.all;
      [...bar.children].forEach((b) => b.setAttribute('aria-pressed', String(+b.dataset.i === k)));
    };
    bar.addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) show(+b.dataset.i); });
    fig.insertBefore(bar, fig.firstChild);
    show(-1);   // the full picture first
  }

  if (!still) {
    /* charts grow and whole numbers count up once, when the chart comes on the screen (decision 0037) */
    const grow = new IntersectionObserver((entries) => {
      for (const en of entries) {
        if (!en.isIntersecting) continue;
        grow.unobserve(en.target); en.target.classList.add('grown');
        for (const t of en.target.querySelectorAll('text.hv')) {
          const end = t.textContent.trim(); if (!/^\d+$/.test(end) || +end === 0) continue;
          const t0 = performance.now(), n = +end;
          const step = (now) => { const k = Math.min(1, (now - t0) / 900); t.textContent = String(Math.round(n * (1 - Math.pow(1 - k, 3)))); if (k < 1) requestAnimationFrame(step); else t.textContent = end; };
          requestAnimationFrame(step);
        }
      }
    }, { threshold: 0.4 });
    for (const c of document.querySelectorAll('svg.ve-bars, svg.ve-grow')) grow.observe(c);

    /* flow dots (the sample, decision 0008): dots move along the route while the figure is on the screen and shows its full picture */
    for (const svg of document.querySelectorAll('svg:has([data-flow])')) {
      const layer = svg.querySelector('.ve-dots'), steps = svg.closest('.ve-steps');
      const routes = [...svg.querySelectorAll('[data-flow]')].map((p) => ({ p, len: 0, every: +p.dataset.every, delay: +(p.dataset.delay || 0), next: null }));
      let dots = [], visible = false, running = false;
      const live = () => visible && (!steps || steps.classList.contains('is-full'));
      const tick = (t) => {
        if (!live()) { running = false; for (const d of dots) d.c.remove(); dots = []; for (const r of routes) r.next = null; return; }
        for (const r of routes) { if (!r.len) r.len = r.p.getTotalLength(); if (r.next === null) r.next = t + r.delay; }   // lengths now, when the figure is open; a delay orders the routes
        for (const r of routes) if (t >= r.next) { r.next = t + r.every; const c = document.createElementNS(svg.namespaceURI, 'circle'); c.setAttribute('r', 5); layer.append(c); dots.push({ c, r, t0: t }); }
        dots = dots.filter((d) => { const s = (t - d.t0) * .3; /* 0.3 units per ms: slower than the sample (.45), on the wish of the owner */ if (s > d.r.len) { d.c.remove(); return false; } const pt = d.r.p.getPointAtLength(s); d.c.setAttribute('cx', pt.x); d.c.setAttribute('cy', pt.y); return true; });
        requestAnimationFrame(tick);
      };
      const start = () => { if (!running && live()) { running = true; requestAnimationFrame(tick); } };
      if (steps) steps.addEventListener('ve:step', start);
      new IntersectionObserver(([en]) => { visible = en.isIntersecting; start(); }).observe(svg);
    }
    document.documentElement.classList.add('js-motion');
    const io = new IntersectionObserver((entries) => { for (const en of entries) if (en.isIntersecting) { io.unobserve(en.target); en.target.classList.add('in'); } }, { rootMargin: '0px 0px -10% 0px' });
    for (const x of document.querySelectorAll('main > *')) io.observe(x);
  }
});
