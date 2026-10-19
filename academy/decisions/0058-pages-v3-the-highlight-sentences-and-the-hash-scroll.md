# 0058: pages-v3: the two highlight sentences and the scroll to a part

- Date: 19 October 2026
- Status: accepted
- Text confirmed by the owner: 19 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none
- Changes: none. It adds to decisions 0050 and 0051 (the portal form of the pages).

## Question

The portal session gave two items for the next update of the pages. First, on tab 1, part 1.1, the two sentences "tool_use" and "end_turn" (`<b class="ve-ref">`) have the dotted underline of a card. A reader expects a popup, and the owner reported them as "preview cards that don't work". They only light up a part of the figure. Second, a link to a part (`#id`) lands too far down in the portal. How do the sentences look, and when does the fix of the scroll go in?

## Decision

1. The two sentences have no dotted underline. They have a faint tint at all times, and a stronger tint on hover or focus, as before. No new text.
2. The next update of the pages is `pages-v3`, now. It has the new style of the two sentences and the fix of the scroll. The script scrolls to the hash at the end of `academyStart()`, when all content is in its final state.

## Reason

1. The tint looks like a highlight that matches the figure, not like a card. The cards keep their dotted underline, so the dotted underline still means "a popup".
2. The fix is small and agreed. With it, the portal can later drop its own fix (`stop.open(id)` after `start()`).

## How we decided

The portal session reported both items in its handoff, with a measurement: at `/exam-guide-breakdown#ts-2-5` the part ended 1,730 px above the top of the window. The assistant confirmed both in the code and recommended `pages-v3` now. The owner said "yes start pages-v3". The assistant recommended the faint tint without the underline, with the old and the new style rule. The owner said "yes".

The work found two more causes of the wrong scroll. The fonts finish loading after the scroll and make the text above the part taller (146 px at `#ts-2-5`), so the script scrolls again then, unless the reader or a link moved the page in the meantime. With motion on, a block that is not on the screen yet sits 1rem lower, so the script shows the block of the target at once before it scrolls. These are fixes of the same agreed item, not new decisions.

## Exam guide points

None.
