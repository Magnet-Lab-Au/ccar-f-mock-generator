# 0017: The prototypes obey the security policy of the portal

- Date: 13 October 2026
- Status: proposed
- Text confirmed by the owner: not yet
- Diagram: none

## Question

The security policy of the portal (`magnetlab-academy/frontend/public/_headers`) has `script-src 'self'` and `font-src 'self' data:`. So the portal blocks inline scripts and fonts from other sites. The fifth sample and the two split pages each have 3 inline scripts (and 2 blocks of JSON data), and they load Sora and IBM Plex Mono from Google Fonts. The portal has Sora and Norwester, not IBM Plex Mono. How do the prototypes move into the portal?

## Decision

The prototypes obey the security policy of the portal from the start:

- Each tab has one separate script file. A page has no inline script.
- The font files are stored in the `academy/` folder and loaded from there.
- Each page sets the policy of the portal, so that the browser blocks the same things as the portal does.

If a prototype runs here, it runs in the portal. The owner adds the IBM Plex Mono font files to the portal when the owner moves the pages.

## Reason

Decision 0010 said only that the move "needs some work for each page". The independent review of the plan found the exact limits. A prototype that obeys them makes the move a copy.

## How we decided

The independent review of the plan raised it. The assistant recommended the three rules. The owner accepted them ("Yes I suppose so").

## Exam guide points

none.
