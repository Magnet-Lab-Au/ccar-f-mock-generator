/* Made by academy/build/ from its sources. Do not edit by hand. */
window.ACADEMY = {"pop": {"ts-1-1-check": {"who": "Your code", "cls": "code", "title": "Your code checks stop_reason", "sent": ["\"tool_use\": the loop continues. \"end_turn\": the loop stops. Your code decides on this field, not on the text of the answer."], "points": [{"id": "1.1-K1", "text": "The agentic loop lifecycle: sending requests to Claude, inspecting stop_reason (\"tool_use\" vs \"end_turn\"), executing requested tools, and returning results for the next iteration", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}, {"id": "1.1-S1", "text": "Implementing agentic loop control flow that continues when stop_reason is \"tool_use\" and terminates when stop_reason is \"end_turn\"", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}, {"id": "1.1-S3", "text": "Avoiding anti-patterns such as parsing natural language signals to determine loop termination, setting arbitrary iteration caps as the primary stopping mechanism, or checking for assistant text content as a completion indicator", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}], "example": null, "examplehead": "", "examplenote": ""}, "ts-1-1-convo": {"who": "The conversation", "cls": "io", "title": "The conversation grows", "sent": ["Each iteration adds the tool result to the conversation history, so that Claude can reason about the next action."], "points": [{"id": "1.1-K2", "text": "How tool results are appended to conversation history so the model can reason about the next action", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}, {"id": "1.1-S2", "text": "Adding tool results to conversation context between iterations so the model can incorporate new information into its reasoning", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}], "example": null, "examplehead": "", "examplenote": ""}, "ts-1-1-resp": {"who": "Claude", "cls": "model", "title": "Claude responds", "sent": ["Claude reasons about which tool to call next, from the context."], "points": [{"id": "1.1-K3", "text": "The distinction between model-driven decision-making (Claude reasons about which tool to call next based on context) and pre-configured decision trees or tool sequences", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}], "example": null, "examplehead": "", "examplenote": ""}, "ts-1-1-run": {"who": "Your code", "cls": "code", "title": "Your code runs the tool and adds the result", "sent": ["Your code runs the tool that Claude asked for. Then it adds the result to the conversation, so that Claude can use the new information in its next step."], "points": [{"id": "1.1-K2", "text": "How tool results are appended to conversation history so the model can reason about the next action", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}, {"id": "1.1-S2", "text": "Adding tool results to conversation context between iterations so the model can incorporate new information into its reasoning", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}], "example": null, "examplehead": "", "examplenote": ""}, "ts-1-1-done": {"who": "Your code", "cls": "owner", "title": "The loop stops", "sent": ["stop_reason is \"end_turn\", so your code stops the loop."], "points": [{"id": "1.1-S1", "text": "Implementing agentic loop control flow that continues when stop_reason is \"tool_use\" and terminates when stop_reason is \"end_turn\"", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}, {"id": "1.1-S3", "text": "Avoiding anti-patterns such as parsing natural language signals to determine loop termination, setting arbitrary iteration caps as the primary stopping mechanism, or checking for assistant text content as a completion indicator", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}], "example": null, "examplehead": "", "examplenote": ""}, "ts-1-1-send": {"who": "Your code", "cls": "code", "title": "Your code sends the request", "sent": ["The request carries the conversation history, with each tool result."], "examplehead": "The loop in Python", "example": "messages = [{\"role\": \"user\", \"content\": task}]\nwhile True:\n    response = client.messages.create(\n        model=\"claude-opus-5-5\", max_tokens=16000,\n        tools=tools, messages=messages)\n    messages.append({\"role\": \"assistant\", \"content\": response.content})\n    if response.stop_reason != \"tool_use\":\n        break                     # \"end_turn\", or another reason to handle\n    # stop_reason is \"tool_use\": run each tool that Claude asked for\n    results = [{\"type\": \"tool_result\", \"tool_use_id\": block.id,\n                \"content\": run_tool(block.name, block.input)}\n               for block in response.content if block.type == \"tool_use\"]\n    messages.append({\"role\": \"user\", \"content\": results})", "examplenote": "Based on the Anthropic documentation, page \"How tool use works\", section \"The agentic loop (client tools)\" (https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works), read on 13 October 2026. The exam guide has no code.", "points": [{"id": "1.1-K1", "text": "The agentic loop lifecycle: sending requests to Claude, inspecting stop_reason (\"tool_use\" vs \"end_turn\"), executing requested tools, and returning results for the next iteration", "ctx": "Task statement 1.1: Design and implement agentic loops for autonomous task execution"}]}}, "card": {"ts-1-1-title": {"title": "Exam guide, task statement 1.1", "kind": "guide", "text": "### **Task Statement 1.1: Design and implement agentic loops for autonomous task execution**", "src": "reference/exam-guide.md, line 115", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L115"}, "ts-1-1-g-scope": {"title": "In-Scope Topics, Section 17 (Appendix)", "kind": "guide", "text": "Agentic loop implementation: control flow based on stop_reason, tool result handling, loop termination conditions", "src": "reference/exam-guide.md, line 1021", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L1021"}, "ts-1-1-g-tech": {"title": "Technologies and Concepts, Section 17 (Appendix)", "kind": "guide", "text": "Claude API — tool_use with JSON schemas, tool_choice options (\"auto\", \"any\", forced tool selection), stop_reason values (\"tool_use\", \"end_turn\"), max_tokens, system prompts", "src": "reference/exam-guide.md, line 1006", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L1006"}, "ts-1-1-count": {"title": "The questions of the 5 mocks", "kind": "count", "text": "Questions whose point starts with 1.1, in mocks/mock-01.questions.json to mock-05.questions.json: 10 of 300. The script of this page counted them.", "src": "mocks/mock-01.questions.json to mocks/mock-05.questions.json", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/tree/mocks-v2/mocks"}, "ts-1-1-guide": {"title": "Exam guide, task statement 1.1", "kind": "guide", "text": "1.1: Design and implement agentic loops for autonomous task execution. 6 points: The agentic loop lifecycle: sending requests to Claude, inspecting stop_reason (\"tool_use\" vs \"end_turn\"), executing requested tools, and returning results for the next iteration / How tool results are appended to conversation history so the model can reason about the next action / The distinction between model-driven decision-making (Claude reasons about which tool to call next based on context) and pre-configured decision trees or tool sequences / Implementing agentic loop control flow that continues when stop_reason is \"tool_use\" and terminates when stop_reason is \"end_turn\" / Adding tool results to conversation context between iterations so the model can incorporate new information into its reasoning / Avoiding anti-patterns such as parsing natural language signals to determine loop termination, setting arbitrary iteration caps as the primary stopping mechanism, or checking for assistant text content as a completion indicator", "src": "reference/exam-guide.md, lines 115 to 127", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L115-L127"}, "ts-1-1-d-stop": {"title": "Anthropic documentation: Handling stop reasons", "kind": "docs", "text": "The page names seven stop_reason values: end_turn, max_tokens, stop_sequence, tool_use, pause_turn, refusal and model_context_window_exceeded. For tool_use it says: \"Claude is calling a tool and expects you to run it.\"", "src": "platform.claude.com, read on 13 October 2026", "href": "https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons"}, "m-what": {"title": "Exam guide, section 1", "kind": "guide", "text": "This guide is the authoritative reference for candidates preparing to sit the exam. It describes the exam content, lists the domains and task statements tested, provides sample questions, and recommends preparation strategies.", "src": "reference/exam-guide.md, line 15", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L15"}, "m-items": {"title": "Exam guide, section 3", "kind": "guide", "text": "| Number of items | 60 |", "src": "reference/exam-guide.md, line 40", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L40"}, "m-format": {"title": "Exam guide, section 3", "kind": "guide", "text": "| Item format | Multiple-choice and multiple-response items; each item states how many responses to select |", "src": "reference/exam-guide.md, line 41", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L41"}, "m-struct": {"title": "Exam guide, section 3", "kind": "guide", "text": "| Exam structure | 4 scenarios drawn from a bank of 6 |", "src": "reference/exam-guide.md, line 42", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L42"}, "m-weights": {"title": "Exam guide, section 4", "kind": "guide", "text": "The percentages indicate the approximate proportion of scored items drawn from each domain.", "src": "reference/exam-guide.md, line 54", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L54"}, "m-d1": {"title": "Exam guide, section 4, domain 1", "kind": "guide", "text": "| 1 | Agentic Architecture & Orchestration | 27% |", "src": "reference/exam-guide.md, line 58", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L58"}, "m-d2": {"title": "Exam guide, section 4, domain 2", "kind": "guide", "text": "| 2 | Tool Design & MCP Integration | 18% |", "src": "reference/exam-guide.md, line 59", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L59"}, "m-d3": {"title": "Exam guide, section 4, domain 3", "kind": "guide", "text": "| 3 | Claude Code Configuration & Workflows | 20% |", "src": "reference/exam-guide.md, line 60", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L60"}, "m-d4": {"title": "Exam guide, section 4, domain 4", "kind": "guide", "text": "| 4 | Prompt Engineering & Structured Output | 20% |", "src": "reference/exam-guide.md, line 61", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L61"}, "m-d5": {"title": "Exam guide, section 4, domain 5", "kind": "guide", "text": "| 5 | Context Management & Reliability | 15% |", "src": "reference/exam-guide.md, line 62", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L62"}, "m-s1": {"title": "Exam guide, section 5, scenario 1", "kind": "guide", "text": "### Scenario 1: Customer Support Resolution Agent", "src": "reference/exam-guide.md, line 69", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L69"}, "m-s2": {"title": "Exam guide, section 5, scenario 2", "kind": "guide", "text": "### Scenario 2: Code Generation with Claude Code", "src": "reference/exam-guide.md, line 75", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L75"}, "m-s3": {"title": "Exam guide, section 5, scenario 3", "kind": "guide", "text": "### Scenario 3: Multi-Agent Research System", "src": "reference/exam-guide.md, line 83", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L83"}, "m-s4": {"title": "Exam guide, section 5, scenario 4", "kind": "guide", "text": "### Scenario 4: Developer Productivity with Claude", "src": "reference/exam-guide.md, line 89", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L89"}, "m-s5": {"title": "Exam guide, section 5, scenario 5", "kind": "guide", "text": "### Scenario 5: Claude Code for Continuous Integration", "src": "reference/exam-guide.md, line 95", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L95"}, "m-s6": {"title": "Exam guide, section 5, scenario 6", "kind": "guide", "text": "### Scenario 6: Structured Data Extraction", "src": "reference/exam-guide.md, line 101", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/exam-guide.md?plain=1#L101"}, "m-count": {"title": "The exam guide as records", "kind": "count", "text": "reference/guide-records.json has 30 task statements and 240 points: 113 of kind knowledge and 127 of kind skill. The script of this page counted them.", "src": "reference/guide-records.json", "href": "https://github.com/Magnet-Lab-Au/ccar-f-mock-generator/blob/mocks-v2/reference/guide-records.json"}}};
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
