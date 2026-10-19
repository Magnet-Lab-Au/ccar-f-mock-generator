# 0059: The portal form names the two tabs that the portal makes

- Date: 19 October 2026
- Status: accepted
- Text confirmed by the owner: 19 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none
- Changes: none. It adds to decisions 0050 and 0051 (the portal form of the pages).

## Question

The portal now has four Academy tabs: "Exam guide breakdown", "Behind the mocks", "Study with Claude" and "Exam traps". The portal session builds the last two in the portal repository, from files of the owner. They are not in this repository. The owner's brief for "Exam traps" asks that all four tabs show the same tab bar, in this order: Exam guide breakdown, Behind the mocks, Study with Claude, Exam traps. The first two tabs come from this repository. Which tab bars change here?

## Decision

1. The tab bar of the portal form (`academy/pages/portal/`) of the first two tabs ends with two links: "Study with Claude" to `/study-with-claude` and "Exam traps" to `/exam-traps`. `academy/build/portal_form.py` adds them (`PORTAL_TABS`).
2. The pages that open alone (`academy/pages/exam-guide-breakdown.html` and `academy/pages/behind-the-mocks.html`) keep their two tabs.
3. `academy/build/check-pages.js` accepts the two routes in the portal form, and does not follow them, because only the portal has these pages.
4. The change goes to the portal as the tag `pages-v5`.

## Reason

1. A reader of the portal sees one Academy with four tabs. Each tab bar must show all four.
2. In this repository, `study-with-claude.html` and `exam-traps.html` do not exist. A link to them from a page that opens alone would go to a missing page.

## How we decided

The owner gave the portal session a brief for the fourth tab, "Exam traps". The brief describes the form of the pages that open alone, so the portal session asked where the tab goes. The owner chose the portal, as for "Study with Claude", and the tab bars of the first two tabs through this repository and a new tag. The portal session then asked which tab bars change here, and recommended the portal form only. The owner chose the portal form only. The assistant showed the old and the new tab bar of both tabs (working rule 37), and the owner said "yes".

The portal's plan (`PLAN.md` of `~/magnetlab-academy`, "Post-MVP 3") records the same choice. In the portal, `AcademyPage.tsx` routes the two new links, so they open with no reload (portal PR #50, on `staging` of the portal on 19 October 2026).

## Exam guide points

None.
