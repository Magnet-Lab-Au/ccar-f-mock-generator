# The list for the owner: results of the reader checks

The checks of `academy/check-plan.md` ran on 14 October 2026, evening. Each check has its own result file in this folder. This file gives the items that need the owner, most important first. The assistant changed only clear errors: they are in `changes.md` (41 lines), and the version that the owner reads has the tag `owner-review-2026-10-14`. A review agent checked all fixes and found 7 problems, 1 high (a new card reused an ID, so the caption of Fig. 2.3-1 opened the wrong card). All 7 are fixed, and the build now stops when two different cards have one ID. Three fixes add a reading or a fact rather than correct an error. `changes.md` names them, and the owner can take them back.

## In short

- **The facts hold.** 822 URLs: 819 links, 0 broken, and 3 URLs in code examples (A1). 246 numbers of tab 2, all equal to their sources (A2). The second fact check of the 5 hardest parts found 17 problems (1 high): 14 are fixed, one of them only in part (the Explanation of 4.3 is fixed, Fig. 4.3-1 is on this list), and 3 are on this list (A4). The two tabs disagreed in 6 places, and 4 are fixed (A3).
- **The page teaches the facts that the exam asks for.** Agents that read only the page answered 293 mock questions, and each answer was correct with a quote of the page (B1). 4 answers used the agent's own knowledge. The score cannot separate the page from what the model already knows, so the notes of the agents matter more.
- **The main weakness: guide against product.** In about 22 places, the page states a product fact that goes against a point of the guide (for example: four current models reject `tool_choice` any). The label "Guide only" marks most of them, but no line says which answer the exam expects. Five checks found this (B1, B2, B3, B4, C1).
- **A beginner of domain 1 needs a primer** of the products and a glossary (C1, E2).
- **On a phone, the sideways scroll hides the point of about 25 of the 67 figure pictures** (C4).
- **Tab 2 convinces about the process, less about the quality of the questions** (C5).

## 1. Cross-cutting items (each touches many parts)

1. **Say which answer the exam expects.** Where a product fact goes against the guide, add one line such as "For the exam: answer as the guide says." Places: 1.3 (the Agent tool runs even when allowedTools does not name it), 2.3 and 4.3 (four models reject any and a forced tool, also in the Overview and in Fig. 4.3-1), 2.4 (tool search defers MCP tools, resources by tool calls), 2.5 (Grep and Glob not in the default tools on macOS, Linux and WSL, in a caption), 2.3 (30 to 50 tools against "18 instead of 4-5"), 3.1 (/memory and /context), 3.2 (allowed-tools, argument-hint), 3.3 (a Read also loads a rule), 3.4 (Plan subagent, not Explore), 3.5 and 4.2 (3 to 5 examples), 3.6 (`--bare` skips CLAUDE.md), 4.6 (extended thinking deprecated). B1 found 10 mock questions where this tension can confuse: 6 on tool_choice, 2 on allowed-tools and 2 on argument-hint. Sources: B1, B2, B3, B4, C1.
2. **Move product caveats down a level.** B3 found that 20 of 30 Explanations are "mixed": the caveat and the exam point compete in the 3-minute level. The agents name about 14 facts for the Depth, and 3 facts that should go up (1.5: a PostToolUse hook cannot undo an action, 3.1: CLAUDE.md does not enforce, 4.1-S2: disable a noisy category). Source: B3.
3. **A primer before domain 1.** One map of the products (Claude API, Claude Code, Agent SDK, MCP, Managed Agents: what each is, and who runs the tools), one tool definition with one tool_use and tool_result exchange in JSON, and a glossary (tool, built-in tool, hook, session, fork, permission mode, MCP, slash command, CLAUDE.md, skill). Tab 1 never explains Agent SDK, scenario, session or the terms of tab 2 that its "In the mock builder" blocks use. Tab 2 never explains "the assistant", "scenario" or "design review". Sources: C1, E2.
4. **The phone layout.** The wide drawings scroll sideways on a phone, as accepted on 14 October 2026. The agent recommends a vertical layout for the before/after figures and the live figure (2.1-1, 3.3-1, 4.1-1, 3.2-1), and bar charts that shrink to the width (tab 2, Fig. 4-2, 6-2, 4-3). Captions of 9 to 14 lines on a phone: 5.6-1, 2.5-1, 5.4-1, 4.6-1. Source: C4.
5. **Screen readers do not reach the popups inside the figures.** Each drawing has `role="img"`, which the plugin asks for, so a screen reader treats it as one item. The fix is `role="group"` on each drawing that has popups. Nothing visible changes. Source: F1.
6. **The weak and missing popups.** Tab 1: 20 weak (5 of them the step popups of Fig. 1.1-1 from the sample, which repeat the step captions) and 9 missing (a tenth was fixed by A4). Tab 2: 7 weak and 9 missing, the strongest gap is Fig. 4-2 (rules B2 to B5 are not explained anywhere). Source: D2.
7. **Labels and legends of the figures.** Tab 2, Fig. 1-3, 3-2 and 6-2 have no label that says what is counted. Fig. 5-2 has no legend. Fig. 4-2 does not say what B9 is. Tab 1, Fig. 5.5-1 shows only the 97% total, not a weak segment. Source: D1.
8. **Headings that help a search.** The headings of 3.6, 4.6, 5.1, 5.6 and 2.4 do not name some of their points. Two links go one way only (5.5 to 4.6-S3, 3.1 to 3.6-K3). Source: E1.
9. **Plain English.** 85 sentences on tab 1 and 50 on tab 2 have more than 25 words. 17 rewrites, most harmful first, are in C3. The top paragraph of tab 2 is not in Simplified Technical English. The owner wrote it, so the assistant did not change it. Source: C3.

## 2. Tab 2: how it presents its evidence (C5, C2)

1. The title promise holds for steps 1 to 5, partly for step 6, and only as a label for steps 0 and 7. In a skim, only Fig. 1-2 ties a step to a task statement.
2. Call 4a agreed with the answer key 477 times in 477, and no test gives it a wrong key on purpose. (Correction of 15 October 2026: a test before mock 1, `runs/test-0024/part3.json`, gave step 4 two questions with a wrong key on purpose, and step 4 failed both.) Rule B9 let a repeat pass twice (M5-S38 try 5, M5-S33). The page shows the records but not the conclusion.
3. Missing for a sceptic: a comparison with the real exam, a check of the answer keys of mocks 4 and 5 by someone other than a model, the error rate that remains, the known limits of each mock for the candidate, the 10 ideas that are in all 5 mocks, and the total cost (about 86 dollars).
4. Claims stronger than their evidence: "a working example of the exam's principles in action" (the owner's paragraph), "a reader marks the questions, to show if those checks are right" (a model for mocks 4 and 5), and "84 of the 95 ideas are in 2 to 4 mocks" shown as a good spread.
5. The four parts of the build in Claude Code have no group heading that says why they come after step 8. Fig. 5-3 (the design review) stands in the part of the loop of a slot. The 57 D4 findings are ignored with no reason given.

## 3. By part (items not in section 1)

Tab 1:

- **Top, How we broke it down:** the sentence that explains "Guide only" is hard to read (C3, C1). CCAR-F is never expanded, "scored questions" and "primary" are not explained (C1).
- **1.1:** content blocks and why a tool result has the role "user" (C1). 1.1-K3 is thin (B4).
- **1.2:** the code popup is Managed Agents, which the text does not introduce (C1, decision 0039 item 15 chose it). Four popups of Fig. 1.2-1 use one template and repeat the text (D2). 1.2-K3, S1, S2 are thin (B4).
- **1.3:** the hardest part for a beginner (C1): Task tool, allowedTools, AgentDefinition, fork and session at once. "fork" has three meanings. Fig. 1.3-1: "findings + sources" sits under the dashed arrow (D1).
- **1.4:** "hook" is used before 1.5 defines it (C1). 1.4-S2 is thin (B4).
- **1.5:** the code popup quotes a hook of Claude Code, while the text is about the Agent SDK. Not wrong, but an Agent SDK example fits better (C1). "defer" in a popup is not explained (D2).
- **1.6:** the Depth is three facts that do not connect (B3).
- **1.7:** one of the 8 points was not rated by B4 (its count of 1.7 was 7). "results stale": no test for where "tell it which files changed" ends (D2).
- **2.1:** sample question 2, options A and C (few-shot routing, a keyword layer) are not warned against (B2). 2.1-K4, S3, S4 thin (B4). Two weak popups (D2).
- **2.2:** sample question 8, option C (a timeout returned as an empty success) is warned only weakly (B2). The permission panel ends in "no action named in the guide" (D1, D2, B1).
- **2.3:** 5 thin points (B4).
- **2.4:** 5 thin points (B4). Resources: how they differ from tools.
- **3.2:** the heading is about sharing skills, the figure is about `context: fork` (C2). context: fork is not in the Overview prose (B3).
- **3.4:** sample question 5, option D (start direct, switch later) is warned only weakly (B2). The exception of bypass permissions reads oddly (C1, B4). Fig. 3.4-1: the box "Explore subagent" has no arrows (D1).
- **3.5:** "more prose does not fix mixed results" is not said (B2). The box "interacting / independent" floats in Fig. 3.5-1 (D1).
- **3.6:** sample question 10 (CLAUDE_HEADLESS, a redirect of stdin, `--batch`) is not warned against (B2). Who posts the PR comments (D2).
- **4.1:** two weak popups (D2). 4.1-S2 is only in the figure (B3, B4).
- **4.3:** Fig. 4.3-1 does not name manual extended thinking (A4). A skimmer reads that two of the three settings are broken (C2).
- **4.6:** "The exam tests" leaves out the appendix item on prompt chaining (A4). A larger context window and a vote of 3 runs are warned only weakly (B2).
- **5.2:** "In the reading of this page, the limit is on a confidence that nobody calibrated" (B4, C3). "mood" and "sentiment" name one thing, and "mood" is in the heading (C3). Fig. 5.2-1 leaves out the two conditions of 5.2-S3 (A4).
- **5.4:** "a larger context window does not stop degradation" is not said (B2).
- **5.5:** "stratified" is not explained (B1, D2). The heading says calibration, the first sentence says segments (B3).
- **5.6:** a choice by date or by credibility is not rejected (B2). "also in 5.3-S4" in the figure (D1).

Tab 2:

- **Step 0:** the popup on "steps" does not say why steps 3 and 6 do not read the records (D2).
- **Step 1:** "A new point of the owner does not change it" against the caption of Fig. 5-1 (D2).
- **Step 2:** "the narrow list" and "a narrow idea" are not defined (D2).
- **Step 4:** Fig. 4-2 counts 148 failed checks and 156 findings: one check can have more than one finding, but the figure does not say so (C2).
- **Step 5:** the sentence on the branch of the code needed three reads (C3). "the slot is open" (C3).
- **Step 6:** why the owner ignored D4 (D2, C5).
- **Step 7:** "The owner filled the 20 marks of round 1 without reading the questions" alarms a skimmer (C2).
- **The build in Claude Code, 3.4:** plan mode without the exception that tab 1 gives (A3).
- **The build in Claude Code, 4.6:** why the owner stopped with 20 fixes that nobody checked (D2). "Working rule 26" is not explained (D2, C3).
- **Cards:** tab 2 cites `HANDOFF.md` by line on the branch `main`, so a later change of `HANDOFF.md` moves the line (A2).

## 4. Layout and load (for the move into the portal)

- Tab 1 loads in 65 ms from disk, and 329 KB of its 407 KB of page data are the 706 preview cards (F3). The portal can load the cards of a part only when the reader opens it.
- A link to the largest copy of the documentation (structured outputs, 103 KB) gave the error 504 once on GitHub (A1).

- The move itself: G1 found three ways (copy the files, a React page around the built HTML, or a rewrite in React). A copy needs no login, against the portal rule "everything sits behind auth". The owner decides 7 points first, see `G1.md`.

## 5. Checks done and skipped

All 23 checks ran. No check was skipped. The plan and its result files are in this folder.
