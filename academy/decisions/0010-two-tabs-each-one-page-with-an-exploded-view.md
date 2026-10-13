# 0010: Two tabs, each one page with an exploded view

- Date: 13 October 2026
- Status: accepted
- Text confirmed by the owner: 13 October 2026
- Diagram: none
- Changes: decision 0002 (one entry for each task statement), decision 0004 (the levels of "Behind the mocks", and one visual in each Overview)

## Question

How are "Exam guide breakdown" and "Behind the mocks" laid out, and what does each part show?

## Decision

Each section is one tab of the portal. Each tab is one long page, like an exploded view: the reader sees the whole picture first and opens each part deeper. Each part starts closed. Each part has an anchor, such as `#ts-1-1` or `#step-5`, so a link can open it.

### Tab 1: Exam guide breakdown

1. The exam guide: 5 domains and 30 task statements, as one map.
2. How we broke it down: the labels such as 1.1-K2, and the three levels.
3. Each domain opens into its task statements. A closed task statement shows only its takeaway heading, such as "The loop runs while Claude asks for tools". When the reader opens it, it shows the three levels of the 1.1 sample (`sample/1-1-split-exam-guide.html`): Overview, Explanation and Depth.

A task statement gets a figure or an animation only when it has a mechanism to show. The other task statements are text only, in the same three levels.

### Tab 2: Behind the mocks

1. At the top, in big letters, the title "Mocks Built with the Same Principles They Test". Under it, the owner's paragraph:

   > The mock builder is itself an application of the principles the exam tests. The same patterns you are expected to recognise and apply are built into the system that generates the questions. So the mocks are more than practice. They are a working example of the exam's principles in action. Each step below traces those principles back to the relevant task statements, while showing where the design failed, what we learned, and how the system improved.

2. The mock builder: one diagram of the 9 steps (steps 0 to 8 of the build guide).
3. Each step, with four states:
   - Closed: the step name and its place in the 9-step diagram.
   - Overview: what the step does, in one or two sentences.
   - Explanation: how it works, its diagram (diagrams 01 to 12 are the base), and the task statements it uses, with links to tab 1.
   - Depth: what went wrong and how we fixed it. If the step has no story yet, the Depth says so.
4. The build in Claude Code, with the same four states. The entries, each to be checked against the K and S points of the guide before the pages are written:

| Entry | Task statement |
|---|---|
| CLAUDE.md, which imports WORKING-RULES.md | 3.1 |
| Skills, such as ste-writing and discussion-and-brainstorming | 3.2 |
| "Discuss first", before any code | 3.4 |
| A new agent reviews each file. Story: the 26 document gaps | 1.3 |
| HANDOFF.md, the journal and the decision files carry the work from one session to the next | 1.7 |

A link that does not hold after the check is removed.

### Where the five stories of the brief go

| Story | Place |
|---|---|
| The review loop that ended when the control became code (in the 1.1 sample) | Step 5, try again |
| The owner's reason did not reach the writer (mock decision 0074) | Step 5, try again |
| Prompt caching, missed and then added (mock decision 0067) | Step 4, check by a model |
| The limit on confidence options | Step 6, check the complete mock |
| The 26 document gaps that an independent agent found | The build in Claude Code |

### Links between the tabs

- In tab 1, the Depth of each task statement links to each step in tab 2 that uses it. If no step uses it, the Depth says so, and says why the build did not need it (decision 0002).
- In tab 2, the Explanation of each step links to its task statements in tab 1.
- A link opens the target part and scrolls to it.

### Where the pages are made

The pages are HTML prototypes in this folder. The owner moves them into the portal from the portal's own repository. They hold only text, diagrams and animations.

## Changes to earlier decisions

- Decision 0002: "Behind the mocks" has one entry for each step and for each part of the build in Claude Code, not one entry for each task statement. The source labels and the "why the build did not need it" rule stay.
- Decision 0004, "Behind the mocks" column: the Overview says what the step does, the Explanation says how it works, and the Depth has what went wrong and the fix.
- Decision 0004, "one visual" in each Overview: a visual only when there is a mechanism to show.

## Reason

The owner wants an exploded view: the reader sees the overall picture and goes deeper as far as they like. The audience has little time, so there are not 30 separate pages. The mock builder has 9 steps, so "Behind the mocks" follows the steps, not the 30 task statements. The title and paragraph at the top are the hook.

## How we decided

1. The owner asked what happened to the plan for the pipeline. The assistant showed that no page explained the mock builder as a whole, and recommended one overview page.
2. The owner described the exploded view, and said that one page for each tab is better than many pages. The assistant had counted 29 more pages and had forgotten the limit of the audience. The assistant corrected the step count: 9 steps, steps 0 to 8, not 8. The owner said that the pages are HTML prototypes here, which the owner moves into the portal.
3. The assistant proposed a one-page outline. The owner asked for it across the two tabs of decision 0001.
4. The owner gave the title of the "Behind the mocks" tab. The assistant suggested a paragraph. The owner wrote their own. The assistant pointed out a second name ("mock engine"), a semicolon and a repeated sentence. The owner rewrote it, and the assistant accepted it as it is.
5. The assistant moved to the build too soon. The owner stopped it: the outline was not finished. The assistant listed the four open items, and the owner decided them one at a time.
6. For the levels of a task statement, the assistant first proposed new levels. The owner asked if that is how the 1.1 sample shows them. It is not, so the assistant recommended the sample's levels as they are.

## Known limits

- One page with 30 task statements and 9 steps is long. It works only if each part starts closed.
- The animations use JavaScript, and the portal allows only its own scripts and fonts. The move into the portal needs some work for each page.
- The task statement of each entry of the build in Claude Code is not yet checked.

## Exam guide points

none.
