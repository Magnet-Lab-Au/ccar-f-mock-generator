# 0011: The order of trust, and four checks for each page

- Date: 13 October 2026
- Status: accepted. Decision 0014 adds the Anthropic documentation as the source for product facts.
- Text confirmed by the owner: 13 October 2026
- Diagram: none

## Question

The build produced many documents, and some of them disagree. How do the pages show the most accurate facts?

## Decision

### The order of trust

If two sources disagree, the page uses the higher one, and the reviewer reports the conflict.

1. The code (`src/`, `tests/`) and the run files (`runs/`, `mocks/`, `data/`): what the builder does and what happened.
2. The decisions (`docs/decisions/`, `academy/decisions/`). A later decision wins. The status line of a decision names the decisions that change it.
3. The build guide (`docs/build-guide/`) and the diagrams (`docs/diagrams/`).
4. The journal, the lessons, the reviews, `HANDOFF.md` and `docs/portal-notes.md`. They give the stories, not the final facts.

The facts of the exam come from `reference/exam-guide.md` and `reference/guide-records.json`.

### The four checks

1. A fact sheet before each part is written. One agent reads the sources of the part and lists each fact, with its file and line and its place in the order of trust. It also lists each conflict. The owner decides the conflicts.
2. Numbers come from a script. The page script reads each count from the run files. Nobody types a number by hand.
3. Each fact has its source card (decision 0005). The page says only what the fact sheet holds.
4. An independent review after the part is written. A new agent, which did not write the part, checks each sentence against its source. It lists each sentence that the source does not support. The owner reads that list, plus 3 or 4 sentences at random.

## Reason

The build made about 1,600 run files, 94 decisions and about 60 written accounts. 24 of the 84 mock decisions were changed later by other decisions. The written accounts were written at one point in time, so they can be out of date. A check must not depend on the memory or the judgment of one agent (working rule 14).

## How we decided

The owner asked which documents exist, because the pages must get all details right and documents can conflict. The assistant listed the documents in five groups and recommended the order of trust. The owner asked how the most accurate facts reach the page. The assistant recommended the four checks. The owner accepted both.

## Known limits

- The owner's marks (`marking/*.xlsx`, `docs/coverage/*.xlsx`) are not in the order of trust. A page that uses them names them as its source.

## Exam guide points

none.
