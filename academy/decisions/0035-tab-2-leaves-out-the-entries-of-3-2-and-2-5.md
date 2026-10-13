# 0035: Tab 2 leaves out the entries of 3.2 and 2.5

- Date: 14 October 2026
- Status: accepted (decision 0039, item 2)
- Text confirmed by the owner: 14 October 2026, in the discussion (working rule 35)
- Diagram: none
- Changes: decision 0023, the rows of 3.2 and 2.5

## Question

Decision 0023 names six entries for the build in Claude Code. The fact agent of slice 3 checked each link against the K and S points (`academy/facts/claude-code.md`, entries 4 and 5). Does tab 2 show the entries of 3.2 (skills) and 2.5 (built-in tools)?

## Decision

Tab 2 leaves out both entries. The section "The build in Claude Code" has four parts: 3.1, 1.7, 4.6, and 3.4 with no example.

- 2.5: the link does not hold on the records. No record in the repository says which tool did what. Decision 0010 line 47 says: "A link that does not hold after the check is removed."
- 3.2: the link holds only weakly. The two skills that decision 0023 names have no frontmatter option of 3.2. No record shows that the build used them. They are outside the repository, in `~/.claude/skills/synced/`.

## Reason

Neither entry has an example in the records that shows its points. A weak example teaches the point badly. For 3.2, whether a weak link stays is a choice of the owner, so this file records it as a proposal.

## Options for the owner

The repository records two other uses with a real effect: the Claude API skill, before the code of the model steps (mock decision 0040, line 72), and the plugin visual-explainer, for the figures of the academy (academy decision 0013). Step 2 of tab 2 already shows the result of the check that the Claude API skill caused: the build sends its form as structured outputs. It does not name the skill. The assistant recommends no 3.2 entry. If the owner wants a 3.2 entry, the entry can use one of these instead of the two skills that decision 0023 names.

## How we decided

The fact agent of slice 3 found the two weak links (conflict C4.1 and the verdict of entry 5). The review agent of slice 3 found that the reason in the journal was too strong for 3.2. The owner was asleep, so the assistant chose under working rule 36.

## Exam guide points

3.2, 2.5.
