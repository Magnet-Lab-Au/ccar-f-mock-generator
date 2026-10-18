# 0054: All page links point to a fixed tag, and the build reads the tag on GitHub

- Date: 16 October 2026
- Status: accepted
- Text confirmed by the owner: 16 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none

## Question

The build (`academy/build/lib.py`) reads each cited file from the local folder (`read()`). It links to the tag `mocks-v2` if the file has the same text at that tag, and else to `main` (`in_tag()`, `link()`). In the HTML and the script of the two pages, 800 links point to `main` (634 of them into `academy/`), and 1,261 point to the tag `mocks-v2` (counted on 19 October 2026). A line on `main` moves when its file changes, and a local file can differ from GitHub. Then a quote on a card and the line of its link do not agree, and nothing warns anybody. How do the quote and the link always agree?

## Decision

1. One new tag on this repository.
2. The build reads each cited file from GitHub, at the tag of its link (the new tag or `mocks-v2`), not from the local folder.
3. Each link that points to `main` today points to the new tag, also the 634 links into `academy/`. The links that point to the tag `mocks-v2` stay, because that tag is fixed too.
4. `check-pages.js` gets a check that each card's quote is on its linked line at the tag.
5. This work runs here, before the handoff to the portal.
6. The tag needs a push to GitHub, and the push needs a yes of the owner (working rule 32).

## Reason

A tag never moves, so a line at the tag stays the same line. The quote and the link then come from the same file. A file deleted from `main` later stays in the tag, so no link breaks.

Here, the build, `check-pages.js` and today's pages are in one place. A build before and after the change shows that the cards keep the same quotes and only the links change. The portal then gets pages that are already correct.

## How we decided

The owner asked why the build reads the local copy of this repository, and asked to see a real card. The assistant showed the card `teach-5-1-1-s3` of step 5 on tab 2, which quotes line 42 of `docs/build-guide/step-5-try-again.md` and links to `main`. The assistant explained, step by step, how one unpushed row in that table makes the link show another row. The owner said that the build should read GitHub. The owner asked when to do it, and agreed to do it here first, before the handoff. The owner asked whether it breaks anything. The assistant listed five risks, each checked. One of them said that the links to `mocks-v2` do not change, and the owner accepted the list. So item 3 keeps them: `mocks-v2` is a fixed tag too.

## Exam guide points

None.
