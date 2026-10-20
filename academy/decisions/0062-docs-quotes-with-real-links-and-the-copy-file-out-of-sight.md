# 0062: Docs quotes with real links, and the file of the copy out of sight

- Date: 20 October 2026
- Status: accepted
- Text confirmed by the owner: 20 October 2026. Items 1.1, 2 and 3 come from the owner's brief "Portal fixes from the review of 20 October 2026", items 1 and 10. The owner then approved item 1.2 (the `#heading` links), the code popups of item 2, and item 5 (tab 2).
- Diagram: none
- Changes: none. It adds to decisions 0014 and 0030 (the dated copies of the documentation) and 0044 (the source lists).

## Question

The owner reviewed tab 1 in the portal. In the cards that quote the Anthropic documentation, some quotes show raw Markdown links, such as "[fork](/docs/en/sub-agents#fork-the-current-conversation)", and each card shows the file and the line of its dated copy, such as "academy/sources/2026-10-14-claude-code-docs-memory.md, line 39". On tab 2, one sentence says that the notes of mock v1 are "not in this repository". How do these change?

## Decision

1. In a docs quote, a Markdown link becomes a real link. It opens in a new tab with `rel="noopener"`.
   - A `/docs/` path goes to the live site of its documentation: `https://code.claude.com` for Claude Code and `https://platform.claude.com` for the Claude API.
   - A `#heading` goes to that heading of the live page of the copy. One heading moved since the copy: `code-review#review-md` goes to `code-review-customize#use-review-md-for-review-only-rules`.
   - The quote text in the data does not change, so the check of each quote on its linked lines still reads it. The card gets a second field, `html`, which the script shows in place of the text.
2. The file and the line of a dated copy leave the visible source line of the card, the source lists of the parts and the note under the code popups. They stay in the page source, as `data-source` on the card trigger, the source list item, the quote and the note. The note of a code popup says "Copy of 14 October 2026". The title of the card, such as "Claude Code documentation, Memory (copy of 14 October 2026)", and the link "Open the page" do not change.
3. On tab 2, "Source: the notes of mock v1, not in this repository." becomes "Source: the notes of mock v1."
4. Tab 2 gets the same clean-up: its 10 docs cards keep the file of their copy in `data-source` only, and the one raw Markdown link (card `cc-doc-fresh`) becomes a real link.
5. The change goes to the portal as the tag `pages-v8`.

## Reason

1. A reader can follow a link in a quote, and does not see Markdown syntax.
2. A reader does not need the file name of a copy. The title and "Open the page" say where the quote comes from. The file stays in the page source for the checks and for a reviewer.
3. The owner asked for the shorter sentence.

## How we decided

The owner gave the portal session a brief of ten fixes after a review of the portal. Items 1 and 10 change the pages of this repository. The brief gave the counts before the change: 36 cards with raw Markdown links (19 with relative `/docs/` paths) and 294 cards with file paths. The brief says what to do for `/docs/` paths and is silent on `#heading` links. Nine links in eight cards are of that kind, all on Claude Code pages. The assistant made them links to the heading on the live page, and checked that the six live pages answer. An independent review found that one of these headings moved to another page, and that 30 code popups still showed the file of their copy in their note. Both are fixed. The owner approved both, confirmed the moved heading, and asked for the same clean-up on tab 2. The code moved into `academy/build/lib.py` (`docs_cards_tidy`, `source_item`), so both tabs use one copy. Tab 1 stayed byte for byte the same after the move. One sentence of a tab 2 popup still names the folder `academy/sources/` in words. It is page text, so it did not change.

## Exam guide points

None.
