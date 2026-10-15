# 0046: Tab 2 tells a story before the steps

- Date: 15 October 2026
- Status: accepted. Built as version 3, `academy/pages/behind-the-mocks-v3.html`, and version 4, `academy/pages/behind-the-mocks-v4.html`. The original tab 2 and version 2 do not change.
- Text confirmed by the owner: not yet. An independent agent checks it (working rule 35).
- Diagram: none
- Changes: decision 0010, tab 2, item 1 (what comes under the title and the paragraph of the owner). In version 4, decision 0010, tab 2, items 3 and 4 (the closed state of each step and of each part of the build in Claude Code).

## Question

The owner said that the introduction of tab 2 is weak. What is the purpose of tab 2, and what does a reader see first?

## Decision

Purpose:
1. Tab 2 has three purposes, in this order. First, it teaches the exam through a real build. Second, it shows a senior leader at a glance that the build was designed with care. Third, it gives trust in the mocks.
2. The page shows this through evidence, not through claims about the build.

Order of the top of tab 2, top down:
3. The title and the paragraph of the owner stay as they are.
4. "First, we settled what is true": how the guide became the one source of truth.
5. "Next, we used only what the job needed": three choices, and a map of the 30 task statements. (The overview changed "Then" to "Next".)
6. Then Fig. A and the 9 steps.
7. In version 4, a copy of version 3 (owner, 15 October 2026: "I think this is where we need a v4"): each step heading becomes a principle with its task statement. The owner wants to see it before a decision on the words.

Tone:
8. The new sections tell the story as it happened, with "we" and the past tense, for example "we observed that the guide differed from the product". The facts stay exact and come from the records.

The truth section:
9. Three stages in one figure (Fig. S): mock v1 used the guide, the documentation and the CCAR-F course as sources. The present builder uses the guide only (mock decision 0008). The academy pages check the documentation of a fixed date and mark each difference that could change an exam answer (academy decision 0042). The form shows the role of each source. Each stage opens a popup.
10. Why the guide: this is an exam, the exam tests the guide, and the only sample questions of the exam are the 12 in the guide. They became the benchmark. The guide alone answers 4 that the assistant checked (mock decision 0008). Call 4a answered all 12 right before mock 1. Rule B8 stops a close copy of one of them. The owner gave this reason after seeing version 3: "it is because this is an exam and the only sample questions we have is from the guide."
11. One difference side by side (1.3-K1: the Task tool, now called Agent), the count of 23 boxes in 15 parts on tab 1, and a link to them.
12. The source of stage 1 is the document "How These Mocks Were Made" of mock v1, 30 September 2026. The owner said that it may be inaccurate. It is not in this repository, and the page says so on the stage and in its popup. The page does not quote the course.
13. Long-term goal of the owner: a separate tab collects the differences between the guide and the products, and later checks by itself how they drift apart. We did not build it yet.

The tools section:
14. Three choices tell how we decided: no subagents (mock decision 0012), no MCP, hooks or sessions (mock decision 0026), and no Message Batches API but prompt caching (mock decision 0067).
15. A map of the 30 task statements in 5 domain columns (Fig. M). Each tile shows by its form if the build used it, used it in part (or in another way than the guide names), or did not need it, and where: the mock builder or the build in Claude Code. Each tile opens a popup with what we did or why the job did not need it.
16. One agent drafted the map from the records (`academy/facts/task-statement-use-draft.json`), and an independent agent reviewed it (`academy/facts/task-statement-use-review.md`). The page reads `academy/facts/task-statement-use.json`, and the build stops if a quote is not on its stated line.

## Built (15 October 2026)

Version 3 has items 3 to 6 and 8 to 16. Item 7 goes into version 4. The review of the map changed 13 entries and made 8 claims weaker. The map now shows 10 task statements used, 11 as an idea only, and 9 not used. `check-pages.js` printed "All checks passed." for `behind-the-mocks-v3.html`.

The owner decided 1.2 and 1.3: "yes, make 1.3 used and keep 1.2 idea". 1.3 is used at the level of the build in Claude Code, because each subagent got a written brief with its context. 1.2 stays "idea only", because the main session started agents one at a time, with no coordinator that splits, routes and joins the work. Choice 1 of the tools section now says that the pipeline uses no subagents, but the build in Claude Code did. The map now shows 11 used, 10 idea only and 9 not used.

The owner asked what "idea only" means. It covered two cases: done in another way than the guide names (for example 4.3), and done in part (for example 2.5 and 3.2). The owner said: "yes, rename it to in part". The label on the page is now "In part", with the key "in part, or in another way than the guide names". The value in `academy/facts/task-statement-use.json` stays "idea". The caption of Fig. M now says: "Of the 30 task statements, the build used 11, used 10 in part, and did not use 9."

The overview (owner, 15 October 2026): the three headings are one sequence, "First, we settled what is true", "Next, we used only what the job needed" and "Then, we built it in 9 steps". The new heading stands above Fig. A, with a bridge in the story tone: "With the truth settled and the tools chosen, we built the pipeline. It makes a mock in 9 steps. Code moves each try through the steps, a Claude model writes and checks, and the owner decides where judgment is needed. In Fig. A, the form of each box shows who does the step." The owner accepted the bridge with "Code runs most of them". The assistant changed it, because code runs only 4 of the 9 steps alone. In version 3, Fig. A, its caption and the section "The 9 steps" stay as they are. Version 4 changes the closed steps (see below).

Version 4 (owner, 15 October 2026) is built by `academy/build/make-behind-the-mocks-v4.py` as `academy/pages/behind-the-mocks-v4.html`. Each closed step shows its principle and the task statements of that principle, taken from the table of the step in the build guide. Step 8 has none. Under the principle, a short line of at most 10 words says what the step does. The last line gives the name of the step and who does it. The takeaway of each step leaves the page. The owner asked "I wonder if we can have both somehow" for the principle and the old heading, and said "yes, build it in v4". The owner approved the 9 principles after seeing version 4: "Yes much cleaner than before".

The build in Claude Code, version 4 (owner, 15 October 2026): no new map. Fig. M is the map of this section, because its 4 parts (3.1, 1.7, 4.6, 3.4) are tiles marked "Claude Code". The section opens with a bridge: "We built the pipeline itself with Claude Code, under the same discipline. These 4 parts are tiles marked "Claude Code" in Fig. M." Each part has the form of the 9 steps: a principle, a short teal line, and its name. In place of who does it, the part gives its state on the map. The 4 principles: "Write the rules once, and load them into every session" (3.1), "Each new session starts from a written summary" (1.7), "A file that others rely on gets an independent reviewer" (4.6), "Discuss first, then act" (3.4, in part). The tiles of these 4 task statements in Fig. M link to their part. The owner asked to think first about a second map, and then said "yes, build it in v4". The owner approved the 4 principles: "yes, approve them".

The last section, version 4 (owner, 15 October 2026): the heading "Finally, what we can claim and what we cannot" ends the sequence of the story. Its bridge: "A careful build still has limits. Here is what the records prove, and what they do not." The old lead follows, and the two boxes stay as they are. We did not add the concept "Where the process failed" of the document of mock v1, because the Depth of each step holds its failures.

Sections that open and close, version 4 (owner, 15 October 2026): "First, we settled what is true" and "Next, we used only what the job needed" open and close like the other big sections, and start open. The overview and "The 9 steps" are one section, "Then, we built it in 9 steps", with the stairs icon. It holds the bridge, Fig. A and the 9 steps. The page has 5 big sections in one form. The owner said: "yes, merge them and build it in v4 but put the icon in the new merged heading".

Settled from the review:
- 2.5 and 3.2: academy decision 0035 removed their entries from the section "The build in Claude Code", because their examples are weak. The map must show all 30, so they stay as "in part", and their popups say what the records show and do not show.

## Reason

The old introduction made a claim ("more than practice") and then showed a process. The owner and the assistant agreed that both a learner and a leader need the reasons first: why the build is made this way. A leader trusts choices with evidence, such as a cheaper option that we rejected for a reason, more than a statement that the build is good. An empty tile on the map shows judgment, not a gap.

## How we decided

The owner asked: "what is the purpose of this page?" The assistant recommended teaching as the first purpose. The owner said: "I think that the primary purpose should be to teach but the secondary purpose would to to show competence for senior leaders ... And the lowere priority should be trust". The assistant proposed that the first screen serves the leader and the rest serves the learner. The owner said that it is not so simple, and that the structure of overview first and then detail already serves both. The assistant then said that the problem is what the overview says, not the structure. The owner agreed: "We want to fist show things like what principals were used and why."

The owner shared a prototype from mock v1, "How These Mocks Were Made" (30 September 2026), and said that it may be inaccurate. The owner then gave the order: first how we settled the truth, then "a good engineer doesn't use all the tools they were given but what fits best", with the map, then the overview. The assistant suggested principles as step headings, and the owner said: "It sounds like a good idea but we would need to see."

The assistant suggested a short lead of two sentences in place of the paragraph of the owner. The owner said: "The current paragraph we have ... is good Ithought we we buildign after that". The paragraph stays. The owner rejected a label "Read this first" as "tacky and not fit for senior leaders".

On the truth section, the owner said that it "wasn't just from Anthropic's live documentation because we got the course notes" and that "it isn't as simpel as you think". The assistant found three stages in the records, and the owner accepted them and the form of one figure. On the tools section, the owner said: "the story about we meticuliocy choose thigns must be there". The assistant said that the page must show the choices, not claim them, and found the three choices in the mock decisions. The owner said "yes, those three work" and asked to build version 3: "start the v3 build".

## Exam guide points

1.3-K1 (the example of the truth section). The map names all 30 task statements, but this decision does not depend on a point.
