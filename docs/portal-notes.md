# Notes for the portal

These notes are for the people who put the mocks on the portal. The format of the portal is not known yet (decision 0036).

1. **Random order of the options.** Show the options of each question in a random order on each attempt. The correct letters in mocks 1 to 4 are not balanced (decision 0070). The converter must keep the link between each option and its reason.
2. **Mock 5 is a review mock.** It mostly revisits problems of mocks 1 to 4 in new settings. 46 of its 60 questions are close to a question of an earlier mock (decision 0076). In the comparison of an independent agent, only 1 question has no earlier question on its idea (`docs/reviews/mock-5-comparison.md`). Tell participants this before they start it.
3. **No person reads the questions of mocks 4 and 5.** The writer, the checkers and the second review are all Claude models (decision 0071).
4. **Mocks 2 to 5 repeat earlier problems.** The guide has 95 ideas and 5 mocks have 300 questions, so ideas come back. For most ideas, a later mock tests the same problem in a new setting. Only copies are blocked (decisions 0060, 0066, 0068, 0072 and 0075).
5. **The files.** Each mock is two JSON files in `mocks/`: `mock-0N.questions.json` (the questions, in 4 groups by scenario, with no answers) and `mock-0N.answers.json` (the correct letters and the reason of each option). A converter to the format of the portal comes later (decision 0036).
