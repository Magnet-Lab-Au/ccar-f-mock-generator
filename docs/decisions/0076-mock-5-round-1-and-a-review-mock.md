# 0076: Mock 5: round 1, and a review mock

- Date: 9 October 2026
- Status: accepted
- Text confirmed by the owner: 9 October 2026
- Diagram: none. No step changes.

## Question

The second review in Cowork marked all 60 questions of mock 5 (decisions 0071 and 0073): 58 good, 2 bad. An independent agent found that 46 of the 60 questions are close to a question of an earlier mock (`docs/reviews/mock-5-comparison.md`). What happens to the 2 bad questions, and how are participants told about the close questions?

## Options

1. Rewrite the 2 bad questions, keep M5-S41, record the close questions as a known limit, and call mock 5 a review mock in the build guide and in the notes for the portal.
2. Rewrite more questions.

## Decision

Option 1.

1. **The marks of round 1** are marks of the second review, not of the owner. On the instruction of the owner, the assistant typed them into `marking/M5-round1.xlsx` and committed the file.
2. **M5-S33, bad:** a copy of M2-S34 (a CI skill runs Bash and deletes a fixture directory, the answer allowed-tools, the same three wrong options). The rewrite keeps point 3.2-K2 with a different frontmatter field as the answer, for example context: fork or argument-hint.
3. **M5-S45, bad:** a repeat of M5-S41 in the same scenario (both answers: "the same session keeps its reasoning"), and it misses its point 4.6-S3. The rewrite keeps the point. Its answer is the verification pass that reports confidence, so that findings can be routed for review. No same-session idea, and no wrong option on self-reported confidence, because scenario 5 already has one in M5-S40.
4. **M5-S41 stays** as it is.
5. **Known limit:** 46 of the 60 questions of mock 5 are close to a question of an earlier mock. 14 of them are near copies: the same scene and answer, with other wrong options.
6. **Mock 5 is a review mock.** It mostly revisits earlier problems in new settings. The build guide and `docs/portal-notes.md` say so.

2 bad marks of 60 are below the stop limit of decision 0073 (more than 6).

## Reason

Plain reason: the copy breaks decision 0060, and the repeat inside the mock and the missed point are errors of the question. The close questions follow from the narrow list (63 of the 95 ideas, decisions 0066 to 0075). A participant must know that mock 5 repeats problems, so that the mock is used as review and not as a new test.

## How we decided

The owner gave the marks of the second review and the reasons, decided that M5-S41 stays, and asked for the known limit and the note on the review mock.

The second review in Cowork checked this file. The owner confirmed the text of this file on 9 October 2026.

## Exam guide points

none
