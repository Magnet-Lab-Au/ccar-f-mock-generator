# 0046: Tab 2 tells a story before the steps

- Date: 15 October 2026
- Status: accepted. Built as version 3, `academy/pages/behind-the-mocks-v3.html`. The original tab 2 and version 2 do not change.
- Text confirmed by the owner: not yet. An independent agent checks it (working rule 35).
- Diagram: none
- Changes: decision 0010, tab 2, item 1 (what comes under the title and the paragraph of the owner)

## Question

The owner said that the introduction of tab 2 is weak. What is the purpose of tab 2, and what does a reader see first?

## Decision

Purpose:
1. Tab 2 has three purposes, in this order. First, it teaches the exam through a real build. Second, it shows a senior leader at a glance that the build was designed with care. Third, it gives trust in the mocks.
2. The page shows this through evidence, not through claims about the build.

Order of the top of tab 2, top down:
3. The title and the paragraph of the owner stay as they are.
4. "First, we settled what is true": how the guide became the one source of truth.
5. "Then, we used only what the job needed": three choices, and a map of the 30 task statements.
6. Then Fig. A and the 9 steps.
7. Later in version 3: each step heading becomes a principle with its task statement. The owner wants to see it before a decision on the words.

Tone:
8. The new sections tell the story as it happened, with "we" and the past tense, for example "we observed that the guide differed from the product". The facts stay exact and come from the records.

The truth section:
9. Three stages in one figure (Fig. S): mock v1 used the guide, the documentation and the CCAR-F course as sources. The present builder uses the guide only (mock decision 0008). The academy pages check the documentation of a fixed date and mark each difference that could change an exam answer (academy decision 0042). The form shows the role of each source. Each stage opens a popup.
10. One difference side by side (1.3-K1: the Task tool, now called Agent), the count of 23 boxes in 15 parts on tab 1, and a link to them.
11. The source of stage 1 is the document "How These Mocks Were Made" of mock v1, 30 September 2026. The owner said that it may be inaccurate. It is not in this repository, and the page says so on the stage and in its popup. The page does not quote the course.
12. Long-term goal of the owner: a separate tab collects the differences between the guide and the products, and later checks by itself how they drift apart. It is not built yet.

The tools section:
13. Three choices tell how we decided: no subagents (mock decision 0012), no MCP, hooks or sessions (mock decision 0026), and no Message Batches API but prompt caching (mock decision 0067).
14. A map of the 30 task statements in 5 domain columns (Fig. M). Each tile shows by its form if the build used it, used the idea only, or did not need it, and where: the mock builder or the build in Claude Code. Each tile opens a popup with what we did or why the job did not need it.
15. One agent drafted the map from the records (`academy/facts/task-statement-use-draft.json`), and an independent agent reviewed it (`academy/facts/task-statement-use-review.md`). The page reads `academy/facts/task-statement-use.json`, and the build stops if a quote is not on its stated line.

## Built (15 October 2026)

Version 3 has items 3 to 6 and 8 to 15. Item 7 is not built yet. The review of the map changed 13 entries and made 8 claims weaker. The map now shows 10 task statements used, 11 as an idea only, and 9 not used. `check-pages.js` printed "All checks passed." for `behind-the-mocks-v3.html`.

Open for the owner, from the review:
- 1.2 and 1.3 show "idea only". The fact sheet of 1.2 says that a decision of the owner is necessary to cite the fact agents and review agents as 1.2.
- The map shows 2.5 and 3.2 as "idea only", but academy decision 0035 removed their entries from tab 2.

## Reason

The old introduction made a claim ("more than practice") and then showed a process. The owner and the assistant agreed that both a learner and a leader need the reasons first: why the build is made this way. A leader trusts choices with evidence, such as a cheaper option that we rejected for a reason, more than a statement that the build is good. An empty tile on the map shows judgment, not a gap.

## How we decided

The owner asked: "what is the purpose of this page?" The assistant recommended teaching as the first purpose. The owner said: "I think that the primary purpose should be to teach but the secondary purpose would to to show competence for senior leaders ... And the lowere priority should be trust". The assistant proposed that the first screen serves the leader and the rest serves the learner. The owner said that it is not so simple, and that the structure of overview first and then detail already serves both. The assistant then said that the problem is what the overview says, not the structure. The owner agreed: "We want to fist show things like what principals were used and why."

The owner shared a prototype from mock v1, "How These Mocks Were Made" (30 September 2026), and said that it may be inaccurate. The owner then gave the order: first how we settled the truth, then "a good engineer doesn't use all the tools they were given but what fits best", with the map, then the overview. The assistant suggested principles as step headings, and the owner said: "It sounds like a good idea but we would need to see."

The assistant suggested a short lead of two sentences in place of the paragraph of the owner. The owner said: "The current paragraph we have ... is good Ithought we we buildign after that". The paragraph stays. The owner rejected a label "Read this first" as "tacky and not fit for senior leaders".

On the truth section, the owner said that it "wasn't just from Anthropic's live documentation because we got the course notes" and that "it isn't as simpel as you think". The assistant found three stages in the records, and the owner accepted them and the form of one figure. On the tools section, the owner said: "the story about we meticuliocy choose thigns must be there". The assistant said that the page must show the choices, not claim them, and found the three choices in the mock decisions. The owner said "yes, those three work" and asked to build version 3: "start the v3 build".

## Exam guide points

1.3-K1 (the example of the truth section). The map names all 30 task statements, but this decision does not depend on a point.
