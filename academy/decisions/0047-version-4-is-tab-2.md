# 0047: Version 4 is tab 2, and the other versions are old

- Date: 15 October 2026
- Status: accepted. Built on the branch `behind-mocks-v3`. Not merged into main yet.
- Text confirmed by the owner: not yet. An independent agent checks it (working rule 35).
- Diagram: none
- Changes: decision 0046 (the file names of version 4)

## Question

The owner checked version 4 of tab 2 (decision 0046) and tab 1 with its last changes. Which version is tab 2 now, and what happens to the other versions?

## Decision

1. Version 4 is tab 2. Its builder is now `academy/build/make-behind-the-mocks.py`, and it writes `academy/pages/behind-the-mocks.html` and `behind-the-mocks.js`, the files that tab 1 links to.
2. The three other versions stay for comparison, with new names:
   - The original tab 2: `make-behind-the-mocks-v1-old.py` writes `behind-the-mocks-v1-old.html`.
   - Version 2: `make-behind-the-mocks-v2-old.py` writes `behind-the-mocks-v2-old.html`.
   - Version 3: `make-behind-the-mocks-v3-old.py` writes `behind-the-mocks-v3-old.html`.
3. Each old page has a banner at the top: "Old version. The current tab 2 is Behind the mocks", with a link. Each old builder has a note "OLD" at the top.
4. Nothing is deleted. `git mv` keeps the history of each file.
5. The merge of the branch into main is a separate step. The assistant asks the owner before it, because the main session works in that checkout.

## Reason

The owner said that version 4 and the last changes of tab 1 are the main version. Tab 1 links to `behind-the-mocks.html`, so version 4 must have that name. The old versions show how the page changed, so the owner can still compare them.

## How we decided

The owner said: "Okay this is now the main version so we can mark all the other as old." The assistant recommended the new names, a banner on each old page, no deletion, and a separate step for the merge. The owner said: "yes, go ahead with that plan".

## Exam guide points

None.
