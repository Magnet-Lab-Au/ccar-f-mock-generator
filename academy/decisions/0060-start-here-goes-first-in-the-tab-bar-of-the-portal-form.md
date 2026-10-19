# 0060: "Start here" goes first in the tab bar of the portal form

- Date: 20 October 2026
- Status: accepted
- Text confirmed by the owner: 20 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none
- Changes: none. It adds to decision 0059 (the portal form names the two tabs that the portal makes).

## Question

The portal gets a fifth Academy tab, "Start here". The portal session builds it in the portal repository, from files of the owner, as "Study with Claude" and "Exam traps". The owner's brief asks that "Start here" is the first tab in every tab bar, in this order: Start here, Exam guide breakdown, Behind the mocks, Study with Claude, Exam traps. The first two tabs come from this repository. How does their tab bar change?

## Decision

1. The tab bar of the portal form (`academy/pages/portal/`) of the first two tabs starts with "Start here", a link to `/start-here`. `academy/build/portal_form.py` adds it (`PORTAL_TABS_FIRST`). The two links of decision 0059 stay at the end.
2. The pages that open alone keep their two tabs, as in decision 0059.
3. `academy/build/check-pages.js` accepts the route `/start-here` in the portal form, and does not follow it.
4. The change goes to the portal as the tag `pages-v6`.

## Reason

1. "Start here" shows a new participant where to begin, so it comes first in each tab bar.
2. `start-here.html` is not in this repository, so the pages that open alone cannot link to it (decision 0059, reason 2).

## How we decided

The owner gave the portal session a brief for "Start here". The portal's plan (`PLAN.md` of `~/magnetlab-academy`, "Post-MVP 4", merged with the yes of the owner) follows the choices for "Exam traps": the page is made in the portal, and the first two tabs get the new tab through the portal form of this repository and a new tag. The assistant showed the old and the new tab bar of both tabs (working rule 37), and the owner said "yes".

In the portal, `AcademyPage.tsx` routes `/start-here`, so the link opens with no reload (portal PR #57, to `staging` of the portal).

## Exam guide points

None.
