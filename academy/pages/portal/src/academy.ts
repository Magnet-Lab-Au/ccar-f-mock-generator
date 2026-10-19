// @ts-nocheck
/* eslint-disable */
/* Made by academy/build/portal_form.py in ccar-f-mock-generator. Do not edit here: change the source there and copy again. */
/* The shared behavior of the academy pages: the light and dark button, popups and preview cards, linked
   highlighting, steppers, and the closed parts that a link opens (decisions 0010, 0017 and 0033).
   academyStart(root, data) binds everything inside root and returns a function that removes it again, so that the
   portal can start and stop a page on one element (academy decisions 0050 and 0051). That function also has
   open(id): it opens the part with that id and scrolls to it, for a router that changes the hash without a
   hashchange event. The page that opens alone puts
   window.ACADEMY = {pop: {...}, card: {...}} in front of this code and starts it on the body (the end of this file),
   so each tab has one script file and no inline script. */
function academyStart(root, data) {
  const ac = new AbortController(), on = { signal: ac.signal }, observers = [], added = [], timers = new Set();
  let stopped = false;
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const POP = (data && data.pop) || {}, CARD = (data && data.card) || {};
  const $ = (sel) => root.querySelector(sel), $$ = (sel) => [...root.querySelectorAll(sel)];

  /* the light and dark button (only on the page that opens alone; the portal has its own) */
  (() => {
    const html = document.documentElement, btn = $('#theme-btn');
    if (!btn) return;
    const device = matchMedia('(prefers-color-scheme: dark)');
    const dark = () => html.classList.contains('dark') || (!html.classList.contains('light') && device.matches);
    const label = () => { btn.textContent = dark() ? 'Light mode' : 'Dark mode'; };
    btn.addEventListener('click', () => {
      const next = dark() ? 'light' : 'dark';
      html.classList.remove('light', 'dark'); html.classList.add(next);
      try { localStorage.setItem('academy-theme', next); } catch (e) {}
      label();
    }, on);
    device.addEventListener('change', label, on);
    label();
  })();

  /* a link opens its part: the closed details that hold the target open, then the page scrolls to it */
  let opens = 0;   // counts the scrolls of openTo, so that the late scroll after the fonts load does not undo a later one
  const openTo = (id, scroll) => {
    const t = id && document.getElementById(id);
    if (!t || !root.contains(t)) return;
    for (let d = t; d && d !== root; d = d.parentElement) if (d.tagName === 'DETAILS') d.open = true;
    if (!scroll) return;
    opens++;
    /* with motion on, a block that has not come on the screen sits 1rem lower (academy.css, .js-motion): show it at once, so that the scroll measures its final place */
    const box = t.closest('main > *, .ap-main > *');
    if (box && root.classList.contains('js-motion') && !box.classList.contains('in')) { box.style.transition = 'none'; box.classList.add('in'); box.getBoundingClientRect(); box.style.transition = ''; }
    t.scrollIntoView({ block: 'start', behavior: still ? 'auto' : 'smooth' });
  };
  const fromHash = () => { try { openTo(decodeURIComponent(location.hash.slice(1)), true); } catch (e) {} };
  addEventListener('hashchange', fromHash, on);
  root.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (a && a.getAttribute('href') === location.hash) openTo(a.getAttribute('href').slice(1), true);
  }, on);

  /* popups (data-step) and preview cards (data-card) */
  const pop = $('#pop');
  const OPEN_DELAY = 300, CLOSE_DELAY = 350, GAP = 10, EDGE = 8;
  let current = null, pinned = false, openTimer = null, closeTimer = null;
  const later = (f, ms) => { const t = setTimeout(() => { timers.delete(t); f(); }, ms); timers.add(t); return t; };
  const cancel = (t) => { clearTimeout(t); timers.delete(t); };
  const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
  function fillStep(d) {
    const who = $('#popwho'); who.className = 'tag t-' + d.cls; who.textContent = d.who;
    $('#poptitle').textContent = d.title;
    const s = $('#popbody'); s.textContent = '';
    d.sent.forEach((t) => s.appendChild(el('p', null, t)));
    if (d.links && d.links.length) { const lp = el('p', 'poplinks'); d.links.forEach((l) => { const a = el('a'); a.innerHTML = l.text; a.href = l.href; lp.appendChild(a); }); s.appendChild(lp); }   /* links of a popup, such as the popups of Fig. A of tab 2 */
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
    const who = $('#popwho'); who.className = 'tag ' + (c.kind === 'code' ? 't-code' : c.kind === 'guide' ? 't-model' : '');
    who.textContent = KIND[c.kind] || 'Source';
    $('#poptitle').textContent = c.title;
    const s = $('#popbody'); s.textContent = '';
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
  const setPinned = (v) => { pinned = v; $('#poppin').textContent = v ? 'kept open' : ''; };
  function open(t, pin) {
    cancel(openTimer); cancel(closeTimer);
    if (current && current !== t) current.setAttribute('aria-expanded', 'false');
    current = t;
    if (t.dataset.step) fillStep(POP[t.dataset.step]); else fillCard(CARD[t.dataset.card]);
    pop.hidden = false; pop.scrollTop = 0; t.setAttribute('aria-expanded', 'true'); setPinned(pin); place();
  }
  function close(returnFocus) {
    cancel(openTimer); cancel(closeTimer);
    if (!current) return;
    const t = current; t.setAttribute('aria-expanded', 'false'); pop.hidden = true; current = null; setPinned(false);
    if (returnFocus) t.focus({ preventScroll: true });
  }
  function scheduleClose() {
    cancel(closeTimer); if (pinned) return;
    closeTimer = later(() => {
      if (pinned) return;
      if (current && (current.matches(':hover') || pop.matches(':hover'))) return;
      if (current && (document.activeElement === current || pop.contains(document.activeElement))) return;
      close(false);
    }, CLOSE_DELAY);
  }
  if (pop) {
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && current) { e.preventDefault(); close(true); } }, on);
    $$('[data-step],[data-card]').forEach((t) => {
      t.addEventListener('mouseenter', () => { cancel(closeTimer); if (pinned || current === t) return; cancel(openTimer); openTimer = later(() => { if (!pinned) open(t, false); }, OPEN_DELAY); }, on);
      t.addEventListener('mouseleave', () => { cancel(openTimer); scheduleClose(); }, on);
      t.addEventListener('click', (e) => { e.stopPropagation(); e.preventDefault(); if (current === t && pinned) close(false); else open(t, true); }, on);
      t.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (current === t && pinned) close(true); else open(t, true); } }, on);
      t.addEventListener('blur', () => { if (!pinned) scheduleClose(); }, on);
    });
    document.addEventListener('click', (e) => { if (current && !pop.contains(e.target)) close(false); }, on);
    pop.addEventListener('mouseenter', () => cancel(closeTimer), on);
    pop.addEventListener('mouseleave', scheduleClose, on);
    $('#popclose').addEventListener('click', (e) => { e.stopPropagation(); close(true); }, on);
    addEventListener('scroll', place, { capture: true, signal: ac.signal }); addEventListener('resize', place, on);
  }

  /* linked highlighting */
  const linked = $$('[data-ref]'), refs = (x) => x.dataset.ref.split(' ');
  let hovered = null, focused = null;
  const paint = () => {
    const keys = (hovered || focused)?.dataset.ref.split(' ') ?? [];
    for (const t of linked) t.classList.toggle('is-lit', refs(t).some((k) => keys.includes(k)));
    for (const svg of $$('svg')) svg.classList.toggle('has-lit', !!svg.querySelector('.is-lit'));
  };
  for (const x of $$('.ve-ref')) {
    x.addEventListener('pointerenter', () => { hovered = x; paint(); }, on); x.addEventListener('pointerleave', () => { hovered = null; paint(); }, on);
    x.addEventListener('focus', () => { focused = x; paint(); }, on); x.addEventListener('blur', () => { focused = null; paint(); }, on);
  }

  /* stepper: opens on the full picture (k = 0); the arrows go one step at a time; nothing plays by itself */
  for (const st of $$('.ve-steps')) {
    const parts = [...st.querySelectorAll('[data-a]')], lines = [...st.querySelectorAll('[data-s]')], caps = [...st.querySelectorAll('.ve-cap li')];
    const n = caps.length; let i = 0;
    const show = (k) => {
      i = Math.max(0, Math.min(n - 1, k));
      const full = i === 0;
      for (const p of parts) p.classList.toggle('now', !full && p.dataset.a.split(' ').includes(String(i)));
      for (const l of lines) { l.classList.toggle('on', full || +l.dataset.s <= i); l.classList.toggle('now', !full && +l.dataset.s === i); }
      caps.forEach((c, j) => c.hidden = j !== i);
      st.classList.toggle('is-full', full); st.classList.toggle('is-step', !full);
      st.dispatchEvent(new Event('ve:step'));
    };
    st.addEventListener('click', (e) => { const b = e.target.closest('[data-go]'); if (b) show(i + +b.dataset.go); }, on);
    show(0);
  }

  /* the scenarios of tab 1: the name opens the text of the guide under its row (owner, 15 October 2026) */
  for (const b of $$('.scen-toggle')) {
    const row = document.getElementById(b.getAttribute('aria-controls'));
    if (!row || !root.contains(row)) continue;
    row.hidden = b.getAttribute('aria-expanded') !== 'true';
    b.addEventListener('click', () => { const v = b.getAttribute('aria-expanded') !== 'true'; b.setAttribute('aria-expanded', String(v)); row.hidden = !v; }, on);
  }

  /* the glossary panel at the side (owner, 15 October 2026): a fixed button opens and closes it */
  const gBtn = $('.glossary-btn'), gPan = $('#top-words');
  let gHash = () => {};
  if (gBtn && gPan) {
    const gSet = (v) => { gPan.hidden = !v; gBtn.setAttribute('aria-expanded', String(v)); if (v) gPan.querySelector('.gp-close').focus(); };
    gBtn.addEventListener('click', () => gSet(gPan.hidden), on);
    gPan.querySelector('.gp-close').addEventListener('click', () => { gSet(false); gBtn.focus(); }, on);
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && !gPan.hidden) { gSet(false); gBtn.focus(); } }, on);
    gHash = () => { if (location.hash === '#top-words') gSet(true); };
    addEventListener('hashchange', gHash, on);
  }

  /* before / after (decision 0037): with no script both panels show, and the script shows one panel and two buttons */
  for (const fig of $$('.ve-ba')) {
    const panels = [...fig.querySelectorAll('.ba-panel')];
    if (panels.length !== 2) continue;
    const bar = document.createElement('div');
    bar.className = 've-toggle'; bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', 'Show before or after');
    panels.forEach((p, i) => { const b = document.createElement('button'); b.type = 'button'; b.dataset.i = i; b.textContent = p.dataset.label; bar.append(b); });
    const show = (k) => { panels.forEach((p, i) => { p.hidden = i !== k; }); [...bar.children].forEach((b, i) => b.setAttribute('aria-pressed', String(i === k))); };
    bar.addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) show(+b.dataset.i); }, on);
    fig.insertBefore(bar, fig.firstChild); added.push(bar);
    show(1);   // the answer first: the after panel
  }

  /* live figure (decision 0037): with no script the full picture shows, and the script adds one button for each example,
     and a choice lights that example and says what happens to it */
  for (const fig of $$('.ve-live')) {
    const every = [...fig.querySelectorAll('[data-pick]')], targets = [...fig.querySelectorAll('[data-target]')], say = fig.querySelector('.ve-say');
    const items = every.filter((it, i) => every.findIndex((x) => x.dataset.pick === it.dataset.pick) === i);   // a phone drawing repeats each example (academy decision 0043)
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
    bar.addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) show(+b.dataset.i); }, on);
    fig.insertBefore(bar, fig.firstChild); added.push(bar);
    show(-1);   // the full picture first
  }

  const watch = (cb, opts) => { const o = new IntersectionObserver(cb, opts); observers.push(o); return o; };
  const dotLayers = [];
  if (!still) {
    /* charts grow and whole numbers count up once, when the chart comes on the screen (decision 0037) */
    const grow = watch((entries) => {
      for (const en of entries) {
        if (!en.isIntersecting) continue;
        grow.unobserve(en.target); en.target.classList.add('grown');
        for (const t of en.target.querySelectorAll('text.hv')) {
          const end = t.textContent.trim(); if (!/^\d+$/.test(end) || +end === 0) continue;
          const t0 = performance.now(), n = +end;
          const step = (now) => { if (stopped) { t.textContent = end; return; } const k = Math.min(1, (now - t0) / 900); t.textContent = String(Math.round(n * (1 - Math.pow(1 - k, 3)))); if (k < 1) requestAnimationFrame(step); else t.textContent = end; };
          requestAnimationFrame(step);
        }
      }
    }, { threshold: 0.4 });
    for (const c of $$('svg.ve-bars, svg.ve-grow')) grow.observe(c);

    /* flow dots (the sample, decision 0008): dots move along the route while the figure is on the screen and shows its full picture */
    for (const svg of $$('svg:has([data-flow])')) {
      const layer = svg.querySelector('.ve-dots'), steps = svg.closest('.ve-steps');
      dotLayers.push(layer);
      const routes = [...svg.querySelectorAll('[data-flow]')].map((p) => ({ p, len: 0, every: +p.dataset.every, delay: +(p.dataset.delay || 0), next: null }));
      let dots = [], visible = false, running = false;
      const live = () => !stopped && visible && (!steps || steps.classList.contains('is-full'));
      const tick = (t) => {
        if (!live()) { running = false; for (const d of dots) d.c.remove(); dots = []; for (const r of routes) r.next = null; return; }
        for (const r of routes) { if (!r.len) r.len = r.p.getTotalLength(); if (r.next === null) r.next = t + r.delay; }   // lengths now, when the figure is open; a delay orders the routes
        for (const r of routes) if (t >= r.next) { r.next = t + r.every; const c = document.createElementNS(svg.namespaceURI, 'circle'); c.setAttribute('r', 5); layer.append(c); dots.push({ c, r, t0: t }); }
        dots = dots.filter((d) => { const s = (t - d.t0) * .3; /* 0.3 units per ms: slower than the sample (.45), on the wish of the owner */ if (s > d.r.len) { d.c.remove(); return false; } const pt = d.r.p.getPointAtLength(s); d.c.setAttribute('cx', pt.x); d.c.setAttribute('cy', pt.y); return true; });
        requestAnimationFrame(tick);
      };
      const start = () => { if (!running && live()) { running = true; requestAnimationFrame(tick); } };
      if (steps) steps.addEventListener('ve:step', start, on);
      watch(([en]) => { visible = en.isIntersecting; start(); }).observe(svg);
    }
    root.classList.add('js-motion');
    const io = watch((entries) => { for (const en of entries) if (en.isIntersecting) { io.unobserve(en.target); en.target.classList.add('in'); } }, { rootMargin: '0px 0px -10% 0px' });
    for (const x of $$('main > *, .ap-main > *')) io.observe(x);
  }

  /* the hash last, when the steppers, the before and after panels and the scenario rows are in their final state:
     an earlier scroll lands too far down, because the content above the part gets shorter after it (the portal session, 19 October 2026).
     If the fonts still load, the text above the part gets taller when they arrive, so the page scrolls again then. */
  fromHash();
  gHash();
  if (document.fonts && document.fonts.status !== 'loaded') {
    /* not if the reader moved the page, or if a link or stop.open scrolled again in the meantime */
    let moved = false; const n = opens;
    for (const ev of ['wheel', 'touchstart', 'keydown', 'pointerdown']) addEventListener(ev, () => { moved = true; }, { once: true, passive: true, signal: ac.signal });
    document.fonts.ready.then(() => { if (!stopped && !moved && opens === n) fromHash(); });
  }

  /* stop: remove what start added, so that a page can start again on the same element */
  const stop = () => {
    stopped = true;
    ac.abort();
    if (current) current.setAttribute('aria-expanded', 'false');
    if (gBtn && gPan) { gPan.hidden = true; gBtn.setAttribute('aria-expanded', 'false'); }
    for (const o of observers) o.disconnect();
    for (const t of timers) clearTimeout(t);
    for (const n of added) n.remove();
    for (const l of dotLayers) if (l) l.textContent = '';
    if (pop) pop.hidden = true;
    root.classList.remove('js-motion');
  };
  stop.open = (id) => openTo(id, true);
  return stop;
}

export { academyStart as start };
