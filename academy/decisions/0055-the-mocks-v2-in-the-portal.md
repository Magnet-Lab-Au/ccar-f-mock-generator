# 0055: The mocks of version 2 in the portal

- Date: 19 October 2026
- Status: accepted
- Text confirmed by the owner: 19 October 2026 (accepted in the discussion, one item at a time, working rule 35)
- Diagram: none
- Changes: mock decision 0036 ("A converter comes later"): the format of the portal is now known, and this decision sets the converter. Mock decision 0070, item 4 ("the portal shows the options in a random order on each attempt"): item 5 below mixes the options once, and the order on each attempt becomes later work

## Question

The portal holds version 1 of the 5 mocks (`backend/content/ccar-f/mock-N.v1.json`). Our version 2 is two files for each mock in `mocks/`. The strict schema of the portal (`backend/src/content/schema.ts` lines 9 to 49) refuses them: 40 questions have 5 options, the two-answer questions do not end with "Select TWO.", we give a reason for each option, and fields such as `difficulty` are missing. How does version 2 go into the portal?

## Decision

1. **The source.** The mocks of version 2 stay in `mocks/` as the source. The portal gets a converted copy, `mock-N.v2.json`, next to the files of version 1.
2. **The fifth option.** The portal accepts 4 or 5 options (A to E) for a question. The schema, the answer check, the question screen (`ItemBody.tsx`) and the answer review (`Explanation.tsx`, its list `LETTERS`) change. No question of version 1 changes.
3. **"Select TWO."** The converter adds " Select TWO." at the end of the text of each of the 40 two-answer questions (`select: 2`). The check of the portal stays.
4. **The reasons.** `explanation` gets the reason of the correct option, word for word. For a two-answer question, it gets both reasons, each with its letter first ("B: … C: …"). `distractor_explanations` gets the reason of each wrong option, word for word.
5. **The order of the options.** The converter mixes the options of each question once, with a fixed seed, so that each letter is correct about equally often. The reasons move with their options. A map file records the old and the new letter of each option. A new random order on each attempt is a later feature of the portal. Before the converter runs, a check confirms that no page of `academy/pages/` quotes a mock question with its option letter.
6. **Version 2 is the default.** It loads as version 2. The rule of the portal "newest version" (`learning-service.ts` line 282) makes it the default. No announcement and no page for version 1.
7. **The missing fields.** `difficulty`: "Full mock" for mocks 1 to 4, and "Review mock" for mock 5. `timing_note`: empty for mocks 1 to 4. For mock 5: "Most questions revisit a problem of mocks 1 to 4 in a new setting, so take it after them." `trap`: empty (null) for each question.
8. **`point` and `question_id`.** Both stay: two new optional columns on `MockItem`, by a migration that only adds. With `question_id`, a report in the portal leads to the question in `mocks/` and to its letter map. With `point`, the answer review links each question to its part of tab 1, for example `/exam-guide-breakdown#ts-2-5`, next to the "Task 2.5" that `ItemMeta.tsx` already shows. The strict schema of the portal changes to accept the two fields.
9. **The converter.** It lives in the portal, as a path for version 2 in `backend/scripts/prepare-content.ts`, which today writes only version 1 (line 50). It reads our files from GitHub at the tag `mocks-v2`, applies items 3 to 7, fills the two fields of item 8, and writes `mock-N.v2.json` and the letter map. The schema and the tests of the portal check the result.

## Reason

- Item 2: we cannot cut an option without changing a question that passed all its checks.
- Item 3: the exam guide says "each item states how many responses to select" (`reference/exam-guide.md` line 41), and version 1 does the same.
- Item 4: no reason is lost or reworded.
- Item 5: in the 260 one-answer questions, the correct letter is D 76 times, C 67, B 63 and A 54 (counted from `mocks/mock-0N.answers.json` on 19 October 2026). Mock decision 0070 balances the letters only from mock 5. A check found no question and no reason that names another option by its letter, so a new order breaks no text. A new order on each attempt needs much work in the portal: each attempt must store its order.
- Item 6: the portal was never open to participants, and nobody attempted version 1.
- Item 7: the values of version 1 ("Standard" to "Final, with multiple-response items", and notes on the length of the questions) were measures, and we did not measure version 2. A role is true. Mock 5 mostly revisits problems of mocks 1 to 4 (`docs/portal-notes.md` item 2).
- Item 9: the portal already has a script for this job, and its schema is in the portal.

## How we decided

The owner asked whether the mocks stay here or go to the portal, and what happens to version 1. The assistant answered from the code of the portal. Then the assistant brought the 7 questions (a) to (g) and the place of the converter one at a time, each with one recommendation. The owner agreed to each. For item 6, the owner said that nobody attempted version 1. The owner first wanted a page for version 1, which is hard to reach, and then said that it is unnecessary. During item 4, the assistant found that `Explanation.tsx` lists only A to D, and added it to item 2.

## Exam guide points

None.
