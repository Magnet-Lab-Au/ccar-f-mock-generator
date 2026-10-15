# Review of `academy/facts/task-statement-use-draft.json`

- Reviewer: a new agent that did not make the file. Date: 15 October 2026.
- What I checked: each of the 30 entries against the task statement and its K and S points (`reference/task-statements-and-points.md`), the decisions in `docs/decisions/` and `academy/decisions/`, the fact sheets `academy/facts/ts-*.md` and `academy/facts/claude-code.md`, the build guide tables, and `src/`.
- A script checked each evidence quote: all 61 quotes are on their cited lines. The script also counted the words of each "what": all have 25 words or fewer, and none has a semicolon.
- What I did not check: the Anthropic documentation (I made no claim about a product). The marking files (`marking/*.xlsx`), which the brief forbids. I changed no file except this one.

## Changes

| ID | Field | Old | New | Reason (path:line) |
|---|---|---|---|---|
| 1.1 | evidence | 3 items, with `src/model_call.py` 130 (`stop = getattr(response, "stop_reason", None)`) | Remove the `src/model_call.py` 130 item | The code reads `stop_reason` only to reject a refusal or `max_tokens` (`src/model_call.py` 131-135). It does not stop a loop, so it does not support the claim. |
| 1.2 | state | used | idea | `academy/facts/ts-1-2.md` 147 (C7): "To cite it as an example of 1.2 needs a decision by the owner." Academy decision 0023 links no entry to 1.2, and decision 0012 lists "Exam guide points: none". No later decision of the owner cites 1.2. The owner can change this to "used" with a decision. |
| 1.2 | evidence | 3 items, with mock decision 0026 line 19 | Remove the 0026 line 19 item ("The pipeline uses none.") | It is about the builder, not the build in Claude Code. It does not support the claim. |
| 1.3 | state | used | idea | Academy decision 0023 line 19 chose "4.6 (not 1.3)" for the review agents. `academy/facts/claude-code.md` 164: 1.3-K2 "holds in part" and "can be a secondary point". The fact agents are the same agents as in 1.2, so the same owner decision applies (`academy/facts/ts-1-2.md` 147). |
| 1.3 | levels | builder, claude-code | claude-code | `academy/facts/ts-1-3.md` 192 (C7): "No agent passes context in step 0 ... A page must not say that the build passes context between agents." |
| 1.3 | what | "The assistant gave each fact agent a written brief as its context. Step 0 kept the ID of each guide record for later steps." | "The assistant gave each fact agent a written brief, because a subagent does not get the conversation. The builder passed no context between agents." | Same reason as levels. The new text follows `academy/facts/claude-code.md` 164. |
| 1.3 | where, evidence | "step 0 and the build in Claude Code". 3 items. | "the build in Claude Code". Remove the step 0 item (`docs/build-guide/step-0-prepare-the-guide-records.md` 29). | The step 0 item supports only the removed builder claim. |
| 1.4 | evidence | 3 items | Add `docs/decisions/0029-the-design-of-step-2-the-writer-call.md` 131: "code controls the sequence, so each question always gets each check" | The old items show checks by code, but no item shows the order of the steps in code. This line does. |
| 1.6 | what | "Step 1 fixed the plan of a mock before the writing started, because the work of a mock was known in advance." | "Code fixed the plan of a mock in advance, and the checks ran as a fixed chain: each question first, then the whole mock." | The step 1 link alone is weak: `academy/facts/ts-1-6.md` 152 (C4), "agrees in part", and `docs/build-guide/step-1-plan-the-mock.md` 63, "only one idea is used". The step 6 table now has 1.6-K2 (`docs/build-guide/step-6-check-the-complete-mock.md` 40, added under academy decision 0039, item 24). That is a direct use, so "used" stays. |
| 1.6 | where, evidence | "step 1". 2 items. | "steps 1 and 6". Add `docs/build-guide/step-6-check-the-complete-mock.md` 40: "Here: the checks are a fixed chain." | As above. |
| 1.7 | what | "Each new session started fresh from HANDOFF.md and the journal, not from a resumed or forked session." | "HANDOFF.md and the journal gave a new session a summary of the state and the next step. No record shows resume or fork." | The old text says that no session was resumed. `academy/facts/claude-code.md` 138 (C2.1): probably one Claude Code session continued over several days, and "A page must not say that each journal entry was a new Claude Code session." The link holds on 1.7-K4 only (`academy/facts/claude-code.md` 105). |
| 1.7 | evidence | 3 items, with mock decision 0026 line 10 | Replace the 0026 line 10 item with `academy/facts/claude-code.md` 105: "Verdict: the link holds on 1.7-K4 (the structured summary for a new session)." | The 0026 line is about the pipeline, not the build in Claude Code. |
| 2.1 | what | "... The schema description went into the request text." | "The model steps sent no tools, so no tool needed a description. The description of each form went into the request text." | Decision 0040 line 22: the `description` of the draft tool goes into the request text, not a description of the schema. |
| 2.5 | state | used | idea | Academy decision 0035 line 17, accepted by the owner (academy decision 0039, item 2): "2.5: the link does not hold on the records. No record in the repository says which tool did what." The draft text itself says that no record shows which tool did what. "not-used" is false, because the build used the tools. |
| 2.5 | what | "The assistant made every edit and commit with the built-in tools of Claude Code, but no record shows which tool did what." | "The assistant worked with the built-in tools of Claude Code, but no record shows how it chose between them." | 2.5 is about the choice of a tool (2.5-S1, S2, S3). The new text says what the records do not show. |
| 2.5 | evidence | 1 item | Add `academy/decisions/0035-tab-2-leaves-out-the-entries-of-3-2-and-2-5.md` 17: "2.5: the link does not hold on the records." | The decision of the owner. |
| 3.6 | evidence | 2 items | Remove `academy/decisions/0002-...md` 10 ("It uses no task statement of domain 2 or domain 3. This is a deliberate choice.") | The line is about the build guide tables. It does not say why the build needed no CI/CD. |
| 4.5 | what | "The owner rejected the Message Batches API, because each round of the pipeline waited for the round before it." | "The owner rejected the Message Batches API, because the rounds of the pipeline would wait for each batch." | `docs/decisions/0067-prompt-caching-of-the-guide-text.md` 15 gives this reason. The old text gave a different reason. |
| 5.3 | state | used | idea | 5.3 is error propagation "across multi-agent systems". The builder has no agents (mock decision 0026 line 10). The step tables use only 5.3-K4, and say "Written for errors between agents" (`docs/build-guide/step-3-check-by-code.md` 34, `step-6-check-the-complete-mock.md` 42). The build also stops the run on one failure of rule C2, the other half of 5.3-K4 (`academy/facts/ts-5-3.md`, C4). |
| 5.3 | what | "A failed call or an answer that was not valid never counted as a pass, and the control wrote an error record." | "A failed call or an answer that was not valid never counted as a pass. The builder had no agents to pass errors between." | As above. |
| 5.3 | evidence | 2 items | Add `docs/decisions/0026-...md` 10: "The pipeline uses no MCP, no subagent, no hook and no session." | Supports the new second sentence. |
| 5.4 | state | used | idea | 5.4 is "large codebase exploration". This repository is small, and no build guide table names 5.4 (`academy/facts/ts-5-4.md` 137, C4: "The owner decides."). The owner accepted only one line on the 1.7 entry: "the same files also show 5.4-K2" (academy decision 0039, item 9). |
| 5.4 | what | "The decision files, the journal and HANDOFF.md kept key findings across sessions as scratchpad files." | "The decision files, the journal and HANDOFF.md kept key findings across sessions, as scratchpad files do. The repository was small." | As above. |
| 5.5 | what | "The owner marked all 60 questions of mock 1, then a stratified sample of 20 questions of each later mock." | "The owner marked all 60 questions of mock 1, and a sample of 20 questions, 5 from each scenario, of mocks 2 and 3." | Overclaim. Mock 4: "the owner states that they did not read the 20 questions of round 1" (`docs/decisions/0069-...md` 24). Mock 5: "The second review in Cowork marked all 60 questions" (`docs/decisions/0076-...md` 10). Mocks 2 and 3: `docs/decisions/0056-...md` 10, `docs/decisions/0063-...md` 10. Mock 1: `docs/decisions/0045-...md` 10. |
| 5.5 | evidence | 2 items | Add `docs/decisions/0069-mock-4-round-2-known-limits-findings-and-acceptance.md` 24 and `docs/decisions/0063-mock-3-its-known-limits.md` 10: "The owner marked round 1 (20 of 20 good)" | To show the limit and the mocks that the owner marked. |

## Items for the owner

1. 1.2 and 1.3: the records show that the assistant started fact agents and review agents with a written brief. `academy/facts/ts-1-2.md` 147 says that to cite this as 1.2 needs a decision of the owner. I set "idea" until the owner decides.
2. 2.5 and 3.2: academy decision 0035 removed both entries from tab 2. If this map goes on tab 2, it shows them again, as "idea". The owner decides if the map shows them.

## Entries that I checked and kept

- 1.1 (state, levels, what). The step 5 table cites 1.1-S3 (`docs/build-guide/step-5-try-again.md` 42).
- 1.4 (state, levels, what). The tables cite 1.4-K1 and 1.4-K2. Decision 0013 line 26 records the open slot that goes to a person.
- 1.5. The builder uses the plain API (`docs/decisions/0029-...md` 110). No Agent SDK import in `src/`.
- 2.2. `src/model_call.py` 45-54: a retryable error or an error that stops the run.
- 2.3, 2.4. Supported by decisions 0040 and 0026 and academy decision 0002.
- 3.1. Academy decision 0023 and `academy/facts/claude-code.md` 50.
- 3.2 (idea). Decision 0040 line 72 records the use of the Claude API skill. See item 2 for the owner.
- 3.3, 3.6 (state and what).
- 3.4 (idea). Academy decision 0023: "3.4: no example". The journal (`docs/journal.md` 339) agrees.
- 3.5 (idea). No record of tests first or of the interview pattern in the build.
- 4.1. The tables of steps 2, 4 and 6 cite 4.1-K1.
- 4.2. `src/step2_*.py` 70-124 sends 3 sample questions as examples.
- 4.3 (idea). Decision 0040 calls structured outputs "A deviation from the exam guide" (line 33), with "a newer way with the same purpose" (line 64). The named method, tool use, is not used. The schema points 4.3-S4, S5 and K3 are used, but the title names tool use. "idea" agrees with the owner's own words.
- 4.4. `src/control.py` 31: `TRIES = 3`. The step 5 table cites 4.4-K1 and S1.
- 4.6. Academy decision 0023 accepted the 4.6 entry. The step 4 and step 6 tables cite 4.6-K1, K2, K3 and S2.
- 5.1. No step keeps a long conversation (`academy/facts/ts-5-1.md`, "Not found").
- 5.2 (idea). `src/control.py` 32 and 222-223 send a slot with 2 "cannot decide" verdicts to the owner.
- 5.6. The step 0 table cites 5.6-K1 and K2. `src/step0_prepare_guide_records.py` 216 checks the exact text.

## Counts per state after the changes

| State | Draft | After review |
|---|---|---|
| used | 15 | 10 (1.4, 1.6, 1.7, 3.1, 4.1, 4.2, 4.4, 4.6, 5.5, 5.6) |
| idea | 6 | 11 (1.1, 1.2, 1.3, 2.5, 3.2, 3.4, 3.5, 4.3, 5.2, 5.3, 5.4) |
| not-used | 9 | 9 (1.5, 2.1, 2.2, 2.3, 2.4, 3.3, 3.6, 4.5, 5.1) |
| Total | 30 | 30 |
