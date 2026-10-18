# 0050: The folder academy stays here, and the portal gets a copy of the built pages

- Date: 19 October 2026
- Status: accepted
- Text confirmed by the owner: 19 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none
- Changes: decision 0010, section "Where the pages are made" (the owner no longer moves the pages by hand), and decision 0017 (the move is a copy by a script)

## Question

Tab 1 and tab 2 must go into the portal (`~/magnetlab-academy`, a private repository). Where do the build, the sources, the facts and the records of `academy/` live after that, and how do the pages reach the portal?

## Decision

1. The folder `academy/` stays in this public repository: the build, the sources, the facts and the records. Working rule 34 stays.
2. The portal gets only a copy of the built pages, in its `frontend/` folder.
3. A copy script takes the built pages from this repository at a tag, puts them into the portal and writes the tag name into the portal.
4. Each copied file says at the top that this repository makes it. The copy script stops if the portal copy differs from the last copy, so that no change made in the portal is lost.
5. One build writes both forms of each page from the same cards: the page that opens alone here, and the form for the portal. `check-pages.js` checks both.
6. The folder `academy/` stays in the git history. Nobody rewrites the history.

## Reason

- The portal cannot use the pages here directly. Its security policy allows only its own scripts (`script-src 'self'`) and no frame from another site (`default-src 'self'`), in `frontend/public/_headers` line 23.
- The build reads the files of this repository to make each source card, and 315 links of the pages point into `academy/`. To keep `academy/` here is the simplest way to keep all of this correct.
- Nothing was built yet, so the change cost no work.
- The links will point to a fixed tag (decision 0054). So `academy/` can still leave this repository later, and no link breaks.
- `academy/` is public on `main` today already, so this makes nothing public that was private.

What the owner gives up: a repository that shows participants only the mock builder. `academy/` has 640 files and 50 MB, of which 30 MB are screenshots. The copies of Anthropic pages and of the official exam guide PDF in `academy/sources` stay public.

## How we decided

The owner first chose to move `academy/` into the portal, because the folder was meant to be temporary, and this public repository should hold only the mock builder for participants. The assistant then found that 315 links of the pages point into `academy/`, and that the build reads this repository for each quote. The owner and the assistant discussed six ramifications of the move, one at a time. The owner then asked: what if `academy/` stays in this public repository, because people can find it in an earlier commit anyway? The assistant agreed that this is simpler. On the request of the owner to think hard about the reversal, the assistant listed what it costs, what it gives up and two new risks, each with a safeguard (items 4 and 5). The owner agreed.

The assistant searched the repository for the personal files of working rule 19 (`git ls-files` and `git grep` over `academy/`). It found none. 12 files in `academy/` mention them only as an instruction to an agent not to open them, for example `academy/facts/step-0.md` line 10.

## Exam guide points

None.
