# 0061: The tab bar of the portal form in the owner's order

- Date: 20 October 2026
- Status: accepted
- Text confirmed by the owner: 20 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none
- Changes: decision 0059, item 1, and decision 0060, item 1 (the place of the tabs that the portal makes). The rest of 0059 and 0060 stays.

## Question

The owner reordered the portal sidebar and the Academy tab bars. Every tab bar must use one order: Start here, Exam guide breakdown, Study with Claude, Exam traps, Behind the mocks. In the portal form of decisions 0059 and 0060, "Behind the mocks" comes third, directly after "Exam guide breakdown". How does the tab bar of the portal form change?

## Decision

1. `academy/build/portal_form.py` writes the whole tab bar of the portal form from one list, `PORTAL_TAB_BAR`, in this order: Start here (`/start-here`), Exam guide breakdown, Study with Claude (`/study-with-claude`), Exam traps (`/exam-traps`), Behind the mocks. The current tab is a `span` with `aria-current="page"`, as before. The list replaces `PORTAL_TABS_FIRST` and `PORTAL_TABS`.
2. The pages that open alone keep their two tabs, as in decision 0059.
3. The change goes to the portal as the tag `pages-v7`.

## Reason

1. A reader sees one order on every tab bar and in the sidebar of the portal.
2. One list gives the order in one place, so a later change of the order is a change of one line.

## How we decided

The owner gave the portal session the new order of the sidebar and the tab bars. The assistant showed the old and the new tab bar of both tabs (working rule 37). The owner said "yes, go ahead", also for the push of `main` and the tag `pages-v7` after the checks and the review.

In the portal, the tabs that the portal makes got the same order in portal PR #63 (merged into `staging` of the portal).

## Exam guide points

None.
