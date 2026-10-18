# 0053: The portal gets the package of IBM Plex Mono

- Date: 16 October 2026
- Status: accepted
- Text confirmed by the owner: 16 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none
- Changes: decision 0017, sentence "The owner adds the IBM Plex Mono font files to the portal when the owner moves the pages."

## Question

The pages use Sora and IBM Plex Mono, from copies in `academy/pages/fonts/`. The portal loads Sora from the package `@fontsource/sora` and has no mono font. How does the portal get IBM Plex Mono?

## Decision

The portal gets the package `@fontsource/ibm-plex-mono`, loaded in the same way as Sora (`frontend/src/main.tsx`). The copied font files of `academy/pages/fonts/` do not go to the portal. The plan section of the portal flags the new package, as the portal rule "Stack discipline" asks.

## Reason

It is the way the portal already loads its fonts.

## How we decided

The assistant recommended it. The owner agreed.

## Exam guide points

None.
