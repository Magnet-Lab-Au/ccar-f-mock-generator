# 0051: The tabs fit into the portal by way B

- Date: 16 October 2026
- Status: accepted
- Text confirmed by the owner: 16 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none
- Changes: decision 0008 (the light and dark button of the pages: in the portal, the button of the portal decides), and decision 0017 ("If a prototype runs here, it runs in the portal": way B adds a React page, scoped CSS and a page body)

## Question

The survey of the portal (`academy/checks/G1.md`) found three ways to fit the two tabs into the portal. Way A copies the built files into `frontend/public/`. Way B is a React page that shows the built page. Way C rewrites the tabs in React. Which way?

## Decision

Way B:

1. A React page in the portal shows the body of the built page, behind the login, in the section `learning`, and starts the page script on it.
2. The CSS of the pages is scoped, so that it does not clash with the styles of the portal.
3. One dark mode stays: the one of the portal, with its key `theme`.
4. The portal gets a scroll to a `#hash`, for the links to an anchor, between the tabs and inside a tab.

## Reason

- Way B keeps the checked pages exactly, with the login, the sidebar and the tests of the portal.
- Way A has no login. The portal says "Everything sits behind auth by design" (`EXTENDING.md` line 168).
- Way C rebuilds about 1,000 source cards and 143 drawings by hand. Each of them passed independent reviews, and a rewrite puts each of them at risk.

## How we decided

The assistant first recommended way B and wrote "about 2,000 popups" for way C. That number was not counted. The assistant counted and corrected it: 726 source cards and 89 drawings on tab 1, and 287 source cards and 54 drawings on tab 2. The owner asked what the right way is. The assistant recommended way B, with its costs. The owner agreed.

## Exam guide points

None.
