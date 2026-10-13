/* Made by academy/build/ from its sources. Do not edit by hand. */
window.ACADEMY = {"pop": {"ts-44": {"who": "Task statement 4.4", "cls": "model", "title": "Implement validation, retry, and feedback loops for extraction quality", "sent": ["How step 5 uses it: Written for the extraction of data. Here: the findings of the checks go back to the writer with the failed question.", "The same context. Here: the \"document\" is the request of step 2, the \"failed extraction\" is the failed question, and the \"validation errors\" are the findings.", "The same context. Here: the writer can answer \"cannot write\" for a slot that does not fit its scenario. The design expects that such a slot does not improve with a new try. That is an assumption, not checked."], "points": [{"id": "4.4-K1", "text": "Retry-with-error-feedback: appending specific validation errors to the prompt on retry to guide the model toward correction", "ctx": "Task statement 4.4: Implement validation, retry, and feedback loops for extraction quality"}, {"id": "4.4-S1", "text": "Implementing follow-up requests that include the original document, the failed extraction, and specific validation errors for model self-correction", "ctx": "Task statement 4.4: Implement validation, retry, and feedback loops for extraction quality"}, {"id": "4.4-K2", "text": "The limits of retry: retries are ineffective when the required information is simply absent from the source document (vs format or structural errors)", "ctx": "Task statement 4.4: Implement validation, retry, and feedback loops for extraction quality"}], "example": null}, "ts-11": {"who": "Task statement 1.1", "cls": "model", "title": "Design and implement agentic loops for autonomous task execution", "sent": ["How step 5 uses it: Written for agent loops. Here: the limit of 3 tries is a guard, not the main way to stop. The main way to stop is a question that passes."], "points": [{"id": "1.1-S3", "text": "Avoiding anti-patterns such as parsing natural language signals to determine loop termination, setting arbitrary iteration caps as the primary stopping mechanism, or checking for assistant text content as a completion indicator", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}], "example": null}, "ts-43": {"who": "Task statement 4.3", "cls": "model", "title": "Enforce structured output using tool use and JSON schemas", "sent": ["How step 5 uses it: Written for the extraction of data. The new try answers in the same fixed form as step 2, sent as structured outputs (see the deviation above).", "Written for the extraction of data. The guide teaches a forced tool call. This build does not use it (see the deviation above)."], "points": [{"id": "4.3-K1", "text": "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors", "ctx": "Task statement 4.3: Enforce structured output using tool use and JSON schemas"}, {"id": "4.3-S3", "text": "Forcing a specific tool with tool_choice: {\"type\": \"tool\", \"name\": \"extract_metadata\"} to ensure a particular extraction runs before enrichment steps", "ctx": "Task statement 4.3: Enforce structured output using tool use and JSON schemas"}], "example": null}}, "card": {"c-auto": {"title": "Mock decision 0038, Decision", "kind": "excerpt", "text": "1. **One automatic loop.** A question that fails step 3 or step 4 goes to step 5.", "src": "docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md, line 21", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md?plain=1#L21"}, "c-wait": {"title": "Mock decision 0038, Decision", "kind": "excerpt", "text": "2. **Each other failure waits for the owner.** A slot that is `open`, a finding of step 6, a bad mark, and a call that fails 3 times. The program does no automatic repair for them.", "src": "docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md, line 22", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md?plain=1#L22"}, "s5-what": {"title": "Build guide, step 5", "kind": "excerpt", "text": "A question that fails step 3 or step 4 goes back to the writer. The writer gets the request of step 2, plus the failed question with the letters that the checker saw, and the exact findings.", "src": "docs/build-guide/step-5-try-again.md, line 9", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/build-guide/step-5-try-again.md?plain=1#L9"}, "s5-again": {"title": "Build guide, step 5", "kind": "excerpt", "text": "The new try goes through steps 3 and 4 again, as a new question.", "src": "docs/build-guide/step-5-try-again.md, line 9", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/build-guide/step-5-try-again.md?plain=1#L9"}, "s5-short": {"title": "Build guide, step 5", "kind": "excerpt", "text": "The writer does not see older tries, so the request stays short.", "src": "docs/build-guide/step-5-try-again.md, line 9", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/build-guide/step-5-try-again.md?plain=1#L9"}, "s5-three": {"title": "Mock decision 0033, Reason", "kind": "excerpt", "text": "The guide names three parts for a new try: the original, the failed result and the errors (4.4-S1). It does not name the complete history.", "src": "docs/decisions/0033-the-design-of-step-5-the-new-try.md, line 113", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/decisions/0033-the-design-of-step-5-the-new-try.md?plain=1#L113"}, "s5-pass": {"title": "Build guide, step 5", "kind": "excerpt", "text": "The limit is not the main way to stop. The main way to stop is a question that passes.", "src": "docs/build-guide/step-5-try-again.md, line 13", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/build-guide/step-5-try-again.md?plain=1#L13"}, "s5-open": {"title": "Build guide, step 5", "kind": "excerpt", "text": "A slot that stops is open, and the owner decides: more tries, a new point, or a new plan.", "src": "docs/build-guide/step-5-try-again.md, line 13", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/build-guide/step-5-try-again.md?plain=1#L13"}, "s5-file": {"title": "Build guide, step 5", "kind": "excerpt", "text": "Each try is a new file. No file is written over, so the history of each question stays.", "src": "docs/build-guide/step-5-try-again.md, line 15", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/build-guide/step-5-try-again.md?plain=1#L15"}, "s5-guard": {"title": "The two limits in the code", "kind": "code", "text": "TRIES = 3              # tries for one slot (decision 0033). A guess.\nCANNOT_DECIDE = 2      # \"cannot decide\" results that stop a slot (decision 0023)", "src": "src/control.py, lines 31 to 32", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/src/control.py#L31-L32"}, "s5-counts": {"title": "The run records of mocks 1 to 5", "kind": "count", "text": "Tries for 60 slots, counted from the question files: mock 1 83, mock 2 92, mock 3 101, mock 4 111, mock 5 101. Slots with more than one try: 18, 27, 28, 29, 21. Slots that opened at the limit and waited for the owner: 1, 0, 4, 6, 6. Results \"cannot decide\" and answers \"cannot write\": 0 in all. The script of this page counted the files.", "src": "runs/mock-01/ to runs/mock-05/: questions/, checks/ and owner-decisions.json", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/tree/mocks-v2/runs"}, "a-reviews": {"title": "Mock decision 0038, Question", "kind": "excerpt", "text": "The first review found 14 serious items. Decision 0037 answered them. The second review found 10 new serious items, and most of them come from the rules of decision 0037.", "src": "docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md, line 10", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md?plain=1#L10"}, "a-quote": {"title": "Mock decision 0038, How we decided", "kind": "excerpt", "text": "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue.", "src": "docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md, line 62", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md?plain=1#L62"}, "a-code": {"title": "Mock decision 0038, Decision", "kind": "excerpt", "text": "6. **The control is code.** It is one part of the program, with tests that make no model call.", "src": "docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md, line 26", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md?plain=1#L26"}, "a-limit": {"title": "Mock decision 0038, Reason", "kind": "excerpt", "text": "A test shows that a case has a path. It does not show that the path is good. The owner decides that.", "src": "docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md, line 52", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/decisions/0038-a-simple-control-for-mock-1-written-as-code-with-tests.md?plain=1#L52"}, "a-passfirst": {"title": "The code: a pass stops the loop first", "kind": "code", "text": "if v3[\"verdict\"] == \"pass\" and v4[\"verdict\"] == \"pass\":\n    state[\"status\"] = \"passed\"\n    return state\n# The current try failed. Check the two limits (decision 0037, item 6).\ncannot_decide = 0\nfor t in in_round:\n    v = self.verdict(t[\"question_id\"], 4)\n    if v is not None and v[\"verdict\"] == \"cannot_decide\":\n        cannot_decide += 1\nif len(in_round) >= TRIES:\n    state[\"open_reasons\"].append(\"three_tries\")\nif cannot_decide >= CANNOT_DECIDE:\n    state[\"open_reasons\"].append(\"cannot_decide_twice\")\nstate[\"status\"] = \"open\" if state[\"open_reasons\"] else \"to_write\"", "src": "src/control.py, lines 211 to 224", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/src/control.py#L211-L224"}, "a-tests": {"title": "The tests of the program", "kind": "count", "text": "The folder tests/ has 228 tests (each line that starts with \"def test\"). No test makes a model call. The script of this page counted them.", "src": "tests/", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/tree/main/tests"}, "b-q": {"title": "Mock decision 0074, Question", "kind": "excerpt", "text": "The program sent the writer the last failed try and its findings, but not the reason of the owner (decision 0039).", "src": "docs/decisions/0074-the-writer-gets-the-reason-of-more-tries.md, line 10", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/decisions/0074-the-writer-gets-the-reason-of-more-tries.md?plain=1#L10"}, "b-reason": {"title": "The decision of the owner on M5-S38", "kind": "excerpt", "text": "B9 failed three times on the problem of resubmitting failed requests. Use the second problem of the point instead: custom_id to match each answer to its request, because batch results do not come back in the order of the requests.", "src": "runs/mock-05/owner-decisions.json, line 33", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/runs/mock-05/owner-decisions.json#L33"}, "b-fix": {"title": "The fix of decision 0074", "kind": "code", "text": "# more_tries: the last try before the decision. Since decision 0074 the\n# writer also gets the reason of the owner, as an instruction.\ntries = self.tries(slot[\"slot_id\"])\nlast = tries[-1]\nowner = []\nif event.get(\"decision\", {}).get(\"reason\"):\n    owner = [{\"step\": 7, \"rule\": \"owner\", \"detail\": event[\"decision\"][\"reason\"],\n              \"letter\": None, \"point\": None, \"other_questions\": []}]\nif last[\"status\"] == \"cannot_write\":\n    request[\"findings\"] = owner\n    return request\nreturn self._step5(request, last, self._check_findings(last) + owner)", "src": "src/control.py, lines 270 to 281", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/src/control.py#L270-L281"}, "b-first": {"title": "The branch that runs first: a failed try of this start", "kind": "code", "text": "if in_round:\n    # A try of this start failed: step 5 shows that try (decision 0033, item 4).\n    failed = in_round[-1]\n    return self._step5(request, failed, self._check_findings(failed))", "src": "src/control.py, lines 236 to 239", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/src/control.py#L236-L239"}, "b-test": {"title": "The test of decision 0074", "kind": "code", "text": "def test_more_tries_gives_the_reason_of_the_owner_to_the_writer(self):", "src": "tests/test_control.py, line 114", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/tests/test_control.py#L114"}, "b-t4": {"title": "M5-S38, try 4, option A (correct)", "kind": "excerpt", "text": "Select the files to resubmit by reading the custom_id of each failed result, which maps directly to the source file path.", "src": "runs/mock-05/questions/M5-S38-T4.json, line 16", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/runs/mock-05/questions/M5-S38-T4.json#L16"}, "b-m1": {"title": "M1-S46, try 1, the correct option (mock 1)", "kind": "excerpt", "text": "Assign each request a custom_id derived from its source file path, then match each returned result to its file by that custom_id.", "src": "runs/mock-01/questions/M1-S46-T1.json, line 22", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/runs/mock-01/questions/M1-S46-T1.json#L22"}, "b-t5": {"title": "M5-S38, try 5, option A (correct), in the built mock 5", "kind": "excerpt", "text": "The retry step resubmits every request instead of only the failed ones identified by their custom_id, so successful reviews are paid for twice.", "src": "runs/mock-05/questions/M5-S38-T5.json, line 16", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/runs/mock-05/questions/M5-S38-T5.json#L16"}, "b-said": {"title": "Mock decision 0074, Decision", "kind": "excerpt", "text": "The instruction reached the writer, but the question did not follow it.", "src": "docs/decisions/0074-the-writer-gets-the-reason-of-more-tries.md, line 23", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/docs/decisions/0074-the-writer-gets-the-reason-of-more-tries.md?plain=1#L23"}}};
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
    };
    root.addEventListener('click', (e) => { const b = e.target.closest('[data-go]'); if (b) show(i + +b.dataset.go); });
    show(0);
  }

  if (!still) {
    document.documentElement.classList.add('js-motion');
    const io = new IntersectionObserver((entries) => { for (const en of entries) if (en.isIntersecting) { io.unobserve(en.target); en.target.classList.add('in'); } }, { rootMargin: '0px 0px -10% 0px' });
    for (const x of document.querySelectorAll('main > *')) io.observe(x);
  }
});
