# Journal

One entry for each work session. Newest entry first.

## 9 October 2026, mock 4

- The owner decided: start mock 4 with scenarios 1, 3, 4 and 6 and the stricter rule B9 (decision 0066). No change to the difficulty of the questions.
- The plan of mock 4 was made (seed 445312). Before the run, the owner stopped and asked about the cost.
- The program did not use prompt caching. The owner agreed to decision 0067: the guide text, the 12 sample questions and the writer rules come first in each request, as cached blocks. No Message Batches API. The minimum cacheable size for Claude Opus 5.5 is 512 tokens, from the page "Prompt caching".
- A test on 10 questions of mock 3 measured the saving: $0.58 with caching against $1.72 without, about 66% on the check calls. 2 of 10 verdicts changed from pass to fail (M3-S31 on B9, M3-S49 on B8), both borderline. The causes are not separated. The owner named the stricter B9 as a third cause, but the test used the old text of B9, so the assistant recorded that it does not apply. Mock 3 stays accepted. 224 tests pass.

- The owner confirmed decision 0067 and gave the go. Mock 4 ran with seed 445312, scenarios 1, 3, 4 and 6, the stricter B9 and prompt caching. Run 1: 55 of 60 passed, $10.39. 5 slots opened, 4 of them on B9.
- Decision 0068: G074, G060, G059 and later G041 join the narrow list (24 groups), because their slots failed B9 three times on the same problem. M4-S23 got the new point 2.1-S1. After three runs, all 60 slots passed. Mock 4 cost $12.16 for 326 calls: 3.69 million input tokens came from the cache. The estimate with caching was $20 to $26.
- An independent agent checked all 95 point groups: 38 more groups are narrow (sure) and 11 are a judgment call. The narrow list does not change until the owner decides, before mock 5.
- An independent agent compared mock 4 with mocks 1 to 3: 1 copy (M4-S43 with M3-S19), 19 close, 40 same idea only, 0 new. 12 of the 40 are a cause question against an earlier fix question in nearly the same scene.

- Round 1 of mock 4: the marking file has 20 of 20 good. The owner states that they did not read the 20 questions. The second review in Cowork found 2 questions to fix: M4-S43 (a copy of M3-S19) and option C of M4-S09 (ruling 2). Both got a rewrite ($0.67) and passed. The owner did not mark round 2. The second review found both good, and the assistant typed the 2 marks on the instruction of the owner.
- The correct letters of mock 4 are not balanced: D 22 and B 8 of 52 (chance 13). In the 20 marked questions, B was never correct.
- Decision 0069: the known limits of mock 4 (M4-S43 is close to sample question 7, 19 close repeats, and the D2 and D3 findings), the D4 findings ignored, and the acceptance. Step 8 built mock 4. Mock 4 cost $12.83.
- Decision 0070: from mock 5 the plan sets balanced correct letters, and a note for the portal: show the options in a random order on each attempt. Decision 0071: the second review in Cowork marks mock 5, not the owner. 226 tests pass. Diagrams 02, 04 and 12 and the build guide sections of steps 1 and 2 show the changes.

- Decision 0072: the 38 sure narrow groups join the list (62 of 95). The 11 judgment calls keep the stricter rule. The build guide tells participants plainly that mocks 4 and 5 often test the same problem as mocks 1 to 3 in a new setting, that only copies are blocked, and that no person reads the questions of mocks 4 and 5.
- Fixes before the confirmation: 0069 (nobody read round 1, the second review found 2 questions to fix, 31 of 60 close), 0071 (no person reads mocks 4 and 5, the owner agreed to mark mocks 1 and 2 only), 0068 (the new point of an open slot is decision 0039, item 7, not 0045. The citation of 0045 in 0071 is right). The owner confirmed 0068 to 0072. The second review in Cowork checked them.

**Open**

- Mock 5 (scenarios 1, 2, 4 and 5): the second review marks it (decision 0071).
- (Done: the owner confirmed decision 0067 and gave the go for mock 4.)

## 9 October 2026, the stricter rule B9

- The owner confirmed decisions 0056 to 0065, one at a time, and the assistant pushed the commits.
- Decision 0066: a stricter rule B9 for mocks 4 and 5 (the same problem fails, also in another setting, and at most one wrong option may repeat). The owner asked to test it first.
- The test (`src/test_b9.py`, report `docs/reviews/test-b9-mock-3.md`) checked the 60 questions of mock 3: B9 fails 24. It agrees with the independent agent on 12, fails 12 more, and passes 14 that the agent named. It cost $6.33, not the $3 to $4 that the assistant estimated.
- The owner decided: the stricter B9 for mock 4, with an exception. Narrow ideas with almost only one problem keep the copy rule. The assistant drafted `data/narrow-ideas.json` (21 groups). The owner removed G078 and confirmed 20. The writer and call 4b get the copy rule for these ideas. 222 tests pass. Diagrams 06 and 11 and the build guide section of step 4 show it.
- New cost estimate of mock 4: about $32 to $40 (not measured).

**Open**

- (Done: the owner confirmed the list of narrow ideas without G078, 20 groups, and accepted the cost estimate of $32 to $40.)
- (Done: the owner confirmed decision 0066, with two additions: the rule is a judgment, and who proposed each part.)

## 9 October 2026, mock 3 accepted

- The owner marked round 1 of mock 3: 20 of 20 good (`marking/M3-round1.xlsx`, committed before anybody read it). The 2 copies, M3-S34 and M3-S49, got a rewrite with rule B9 ($0.70). Both passed steps 3 and 4 at the first new try.
- The owner marked round 2: 2 of 2 good (`marking/M3-round2.xlsx`, committed before anybody read it). The second review in Cowork also found 2 of 2 good, and no copy.
- Decision 0063: the known limits of mock 3 (47 close repeats across mocks, 7 pairs inside mock 3, and 4 findings of step 6 on repeated wrong ideas). Decision 0064: the 7 findings of rule D4 are ignored, and the 4 of rules D2 and D3 are known limits. Decision 0065: the owner accepted mock 3. Step 8 built `mocks/mock-03.questions.json` and `mocks/mock-03.answers.json`. Mock 3 cost $23.85.
- No step changed, so no new diagram and no build guide section changed. Diagram 12 shows mock 3 as built.

**Open**

- (See the entry above for the stricter rule B9.)
- (Done on 9 October 2026: the owner confirmed decisions 0056 to 0065, one at a time. Decision 0041 got a status line that names decision 0061. One error that stays in a confirmed text: decision 0061 says that diagram 06 does not change, but its B6 popup got one sentence on flags.)

## 8 October 2026, mock 2 accepted and mock 3

- The owner marked round 2 of mock 2: 14 of 14 good (`marking/M2-round2.xlsx`, committed before anybody read it). The owner decided: 4 close questions and 3 findings of step 6 are known limits (decision 0059), the 5 findings of rule D4 are ignored, and rule B9 does not change. Decision 0060: across mocks a copy is not allowed, a close repeat is a known limit. The owner accepted mock 2. Step 8 built `mocks/mock-02.questions.json` and `mocks/mock-02.answers.json`. Mock 2 cost $20.73.
- The assistant showed the 7 changes of decision 0046: 4 done, 2 partly done or done in the plan only, 1 not done by decision 0051. The owner said they are good enough.
- Mock 3 ran with seed 788092 and the fixed scenarios 1, 2, 4 and 6. Rule B9 failed many tries that repeated mock 2, mostly in scenario 6. 4 slots reached the limit of 3 tries.
- The assistant found a fault: rule B6 never found the flag "-p", which the guide names. The owner agreed to decision 0061: a flag is searched with its hyphens. The owner gave M3-S01 the new point 4.4-S4 and 3 more tries to M3-S07, M3-S48 and M3-S53. The command for an open slot could only select a new point at random. The assistant extended it to take the point of the owner, with the checks of decision 0045, and added a test.
- All 60 slots of mock 3 passed. Mock 3 cost $23.15. 219 tests pass.

- An independent agent compared mock 3 with mocks 1 and 2. 49 of 60 questions look like an earlier question: 2 copies (M3-S34 with M2-S13, M3-S49 with M1-S34) and 47 close repeats. About 26 have the same problem and the same answer in another setting, which rule B9 should fail. The owner decided (decision 0062): rewrite the 2 copies, the close repeats are known limits of mock 3, and B9 becomes stricter before mock 4.

**Open**

- (Done on 9 October 2026: see the entry above.)
- The design of the stricter rule B9, before mock 4.
- The owner confirms the texts of decisions 0056 to 0061.
- Mocks 4 and 5 wait for the owner.

## 8 October 2026, mock 2

- Mock 2 ran with seed 167622, scenarios 3, 4, 5 and 6: 60 slots passed, $16.27. The owner marked 20 of 20 good (`marking/M2-round1.xlsx`, committed before anybody read it, SHA-256 e39069af...).
- A second review and an independent agent compared mock 2 with mock 1: 13 strong repeats and 4 close repeats, and M2-S35 repeats M2-S31. The cause: the plan checks groups only inside one mock, step 1 did not prefer an unused point inside a group, and the writer did not know mock 1.
- The owner decided the rule against repeats across mocks (decision 0056): step 1 prefers an unused point inside a group, the writer sees the earlier questions on the same idea (a different scene and angle, never the same wrong options), and rule B9 in call 4b fails a repeat. The assistant suggested the check in step 4, not in step 6, and the owner agreed. 21 rules now.
- The owner fixed the scenarios of mocks 3 to 5: 1-2-4-6, 1-3-4-6, 1-2-4-5 (decision 0057). Each set is permitted by decision 0027. Plans work for 300 seeds of each.
- The 4 close repeats stay as known limits of mock 2 (decision 0058).
- The program read the marks of round 1 (no bad mark). The owner's 14 rewrites ran: the 13 strong repeats (M2-S35 among them, as a rewrite of finding M2-SC5-R1-F1) and M2-S41 (ruling 2, finding M2-SC5-R1-F6). Each passed steps 3 and 4. No try failed rule B9. Cost $4.46. Mock 2 so far: $20.73.
- New diagrams 11 (repeats across mocks) and 12 (scenarios of the 5 mocks) in the form of diagrams 09 and 10. Diagrams 02 and 04 to 07, the build guide sections of steps 1, 2 and 4, and the README files are updated. 216 tests pass.

**Open**

- The owner marks round 2 of mock 2 (`marking/M2-round2.xlsx`, 14 questions).
- The other step 6 findings of mock 2 wait for the owner after the marks.
- The owner confirms the texts of decisions 0056, 0057 and 0058.
- One reviewer checked decisions 0056 to 0058, diagrams 11 and 12 and the code of rule B9. The assistant fixed its findings. It judged that M2-S31-T2 and M2-S59-T2 are still close to M1-S34 and M1-S39, and that M2-S35-T3 shares an example with M2-S31-T2. The owner decides.

## 8 October 2026, later session

- The owner said to start the first change before mock 2. The assistant suggested a file of point groups and a rule of step 1, with changes 1 and 2 of decision 0046 as one decision. The owner agreed, and added a test against mock 1 and the form of the table for the confirmation (decision 0047).
- The assistant drafted `data/point-groups.json` from the 240 texts: 100 groups, 68 with two or more points. A script checks it (`src/point_groups.py check`), with tests in `tests/test_point_groups.py`.
- The test against mock 1: the rule rejects the plan of mock 1. It catches 9 of the 11 known pairs. It does not catch S53/S54 (decision 0046 says that 4.4-K1 and 4.4-K4 are not twins) or S33/S40 (two different correct answers). It also finds S12 with S20 and S22 (generic error messages), which no earlier review listed.
- An independent reviewer checked the groups. The assistant applied its low-cost findings: two merges, two splits and two idea texts. Its finding 1a waits for the owner: all of 4.2 and three points of 3.5 have the answer "give concrete examples".
- The rule of decision 0047 could not make a plan: task statement 3.3 is one group, and Domain 1 failed for each of 2000 seeds. The assistant suggested two changes, and the owner said yes (decision 0048): a task statement gets no more questions than its groups, and code selects so that a full plan stays possible.
- A second independent reviewer checked the final groups with the full exam guide. The owner agreed to its changes: one group for "give concrete examples" (all of 4.2, and 3.5-K1, 3.5-S1, 3.5-S4), the retry group joins the semantic errors (catches S53/S54), 3.1-K1 joins the path rules of 3.3 (catches S33/S40), two small merges and two idea texts. The file now has 95 groups, 65 with two or more points. Each known pair of mock 1 is caught. 15 points never get a slot.
- Step 1 has the rule. Over 2000 seeds each seed gives a plan with no two slots in one group. With the first draft of the groups, 11 points never got a slot, because a tighter task statement always takes their group. Diagram 02 and the build guide section of step 1 show the rule.

- The owner decided: the program makes 5 mocks (decision 0049). With 95 ideas and 300 slots, each idea comes in about 3 mocks.

- The owner asked for a simple way to spread similar questions over the mocks. The assistant suggested one rule in step 1, in code only, and the owner said yes (decision 0050): the groups that earlier mocks used least come first. In a simulation of 20 series of mocks 2 to 5 (`python3 src/point_groups.py series 20`), no idea is left out, 82 of 95 ideas come in 2 to 4 mocks, and about 11 ideas are in all 5. The assistant had first said "3 or 4 mocks", which was too exact.
- Diagrams 01 and 02 and the build guide section of step 1 show decisions 0047, 0048 and 0050. A reviewer checked the records, and the assistant fixed its findings. 192 tests pass.

- The owner confirmed the groups file `data/point-groups.json` and the texts of decisions 0047 to 0050. The text of decision 0045 was not confirmed yet. The owner confirmed it too.
- Change 3 of decision 0046 (12 questions of Domain 4 in one scenario): the owner agreed to no new rule (decision 0051). Any limit below 12 leaves 2 of the 11 sets of scenarios or none. The point groups already prevent the repeat that it caused in mock 1.
- Change 4 of decision 0046 (step 6 compares one scenario only): the owner agreed to a change in code only (decision 0052). Rule C3 now compares the text of each question with all 60 questions of the mock. A finding of C3 can name a question of another scenario. 196 tests pass. Diagram 08 and the build guide section of step 6 show the change.
- Change 5 of decision 0046 (the longest option): the owner agreed to a field of the slot, an instruction to the writer and rule A12 of step 3 (decision 0053). In the built mock 1, the correct option is the longest in 37 of 52 questions with 1 answer (chance 13). The plan now lets the longest option be correct on 13 of 52 and 3 of 8 slots. 199 tests pass. Diagrams 02, 04, 05 and 06 and the build guide sections of steps 1 and 3 show the change.
- Change 6 of decision 0046 ("Select 2." on a point with one idea): the owner agreed to a list of two-answer points, a rule of step 1 and an instruction to the writer (decision 0054). The assistant drafted `data/two-answer-points.json` with 85 points. A reviewer checked it against the guide. The owner agreed to remove the points that list the fields of one structure. The list now has 78 points, and 2000 of 2000 seeds give a plan. 203 tests pass.
- Change 7 of decision 0046 (copies of the sample questions): a word count of code does not separate a copy, so the owner agreed to rule B8 in call 4b, with the 12 sample questions (decision 0055). The list of rules now has 20 rules. 203 tests pass. Diagrams 04, 05 and 06 and the build guide section of step 4 show the change.
- All 7 changes before mock 2 of decision 0046 are done.
- The owner confirmed decisions 0051 to 0055.
- One reviewer checked changes 4 to 7 (decisions 0052 to 0055) against the code and the records. It found no bug in the code. The assistant fixed its findings: old rule numbers in diagram 07 and `src/README.md`, two missing tests (the enum of B8 in the form, rule A12 with 2 correct options), the wording of B8 ("scene is different or correct action is different"), the status lines of decisions 0027, 0030, 0032, 0034 and 0053, the README files, and the build guide section of step 2. 205 tests pass. Not changed: a C3 copy across two scenarios can show as two findings, one in each scenario.

**Open**

- Mock 2.
- How the program prevents the same scene in two mocks, and selects the scenarios across mocks.

## 8 October 2026

This entry continues the second session of 7 October. The work went on after midnight.

- Mock 1 ran: 60 questions passed steps 3 and 4, and step 6 checked the 4 scenarios. One slot (M1-S47) failed 3 tries. The owner selected `more_tries` (decision D001 in `runs/mock-01/owner-decisions.json`), and it passed on its fourth try. The command line did not accept `--mock` before the action. The assistant fixed it and added a test. Mock 1 cost $14.60.
- The owner marked all 60 questions blind. The blind result: 60 good.
- After the blind marking, a second review by a Claude model in Cowork (not a person) marked the questions blind too, and then compared. By the four checks it also found 60 good. It found 7 problems of the mock as a set, and the owner asked it to write them into the marking file as 7 bad marks with reasons. So the 7 bad marks are not blind marks of the owner. The notes of the second review: `docs/reviews/M1-round1-second-review-notes.md`.
- 7 bad marks reach the stop limit of decision 0035. The assistant said that the program applies that limit, and suggested that the 7 do not count, because they are not blind marks and steps 3 and 4 did not fail. The owner agreed.
- The blind file was not in git: only the empty file of the program was committed. The owner had sent the blind file to the Cowork session before the second review, and it came back from there unchanged: SHA-256 a30c0145b79a727ae34c7a4feafec362e8dd6b59cc483cb8ceb85fe19cd7b0e5. The assistant checked the fingerprint, 60 marks, all good, no reasons, and the same 60 question IDs as round 1 of the program. It did not open and save the file. Five columns are hidden in it. The owner hid them while marking. The blind file is now `marking/M1-round1.xlsx`. The file with the 7 bad marks is `marking/M1-round1-second-review.xlsx`.
- A new line in the check at the end of a session in `CLAUDE.md`: a marking file that the owner filled is committed before anybody else reads it.
- The assistant checked the six probable causes of the second review against the plan and the code. True: twin points (two points of one task statement), scenario 5 with 12 of 15 questions from Domain 4, step 6 inside one scenario, no rule on the longest option in the set (29 of 52 by words, 34 of 52 by characters, chance about 13), and multiple-response slots on a point with one idea. False as written: the writer of S30 did not get sample question 1 as an example. The probable cause is the point 1.4-K2 itself.

- The owner agreed that the 7 do not count as bad marks, and that they become rewrites (decision 0045). A rewrite can now have no finding of step 6, and it can get a new point that the owner gives. Code checks three conditions for that point. The assistant checked the four points of the owner: none is a twin of a point in use. For S25, no point of task statement 1.6 was free of twins, so S25 kept its point 1.6-S3, with a reason that tells the writer to test exactly that point. S38 got 3.4-K4.
- The owner set a rule for the 19 findings of step 6: ignore a finding that the 7 cover, rewrite the newer question of a D1 finding that the 7 do not cover, ignore the rest. The result: 9 rewrites and 17 ignore (decisions D002 to D027 in `runs/mock-01/owner-decisions.json`).
- The round of 9 rewrites ran ($2.57). Step 6 ran again. Mock 1 cost $17.17 in total.
- The owner marked round 2 blind: 9 of 9 good. The file was committed before anybody read it (SHA-256 07c3d5fde864c733f012e87e09fd68ec7f6bd67e1efe5bec950a4a8d9e8eeacb). The second review also found 9 of 9 good, and three weak questions. The owner decided: no more rewrites. The three are known limits of mock 1 (decision 0046), and three more causes go to the list of changes before mock 2.

- The owner decided: each of the 16 findings of the second run of step 6 is ignore. The 3 of rule D1 became known limits in decision 0046. The owner accepted mock 1. Step 8 checked the 6 conditions and built `mocks/mock-01.questions.json` and `mocks/mock-01.answers.json`: 60 questions in 4 groups, 120 minutes. Mock 1 cost $17.17 for 265 model calls.
- The build guide sections of steps 5 and 8 exist. Diagrams 01, 07 and 10 show that steps 5 and 8 ran.

**Open**

- The list of 7 changes before mock 2 (decision 0046).

## 7 October 2026, second session

The first session in Claude Code.

- The assistant listed the 30 working rules, and gave the state of the work in 5 lines.
- The folder is in WSL at `/home/triggger/ccar-f-mock-generator`. It is a git repository with a private remote on GitHub. The assistant checked this with `git` and `gh`.
- The new name of the folder is `ccar-f-mock-generator`. With the yes of the owner, the assistant changed the old name `mock-builder-v3` in `CLAUDE.md`, `README.md`, `HANDOFF.md`, the two scripts of step 0, and diagram scripts 02, 03 and 04. The three diagram scripts now find the folder from their own location. The assistant ran them, and diagrams 02, 03 and 04 did not change. Decision 0001 keeps the old name (rule 26).
- The assistant showed a plan for the control before it read all files that `HANDOFF.md` names. The owner asked if it had read them. It had not. It read them, and changed six points of the plan. The owner said yes to the plan.
- The plan said that the assistant stops at each of items 6 to 10. It wrote the code for all five in one pass, and told the owner.
- Decided: the answers to items 6 to 10 of the second review, and four more choices of the code (decision 0039). The owner said yes to each answer. The owner asked if the values of `state` were already decided. The names were decided in decision 0037. The meanings were open.
- The owner asked for shorter questions and answers: 1 to 3 sentences for each item. The owner also asked that each mention of a decision gives the text of that decision. A new rule 31 in `WORKING-RULES.md` records both.
- New code: `src/control.py`, `tests/fakes.py` and `tests/test_control.py`. The tests use `unittest`. No test makes a model call.
- Two independent reviewers checked the code, the tests and decision 0039. The first found 4 serious and 6 minor bugs. The second found 1 serious and 3 minor bugs in the fixes. The owner said yes before each round of fixes. 53 tests pass. For each fix, the assistant removed the fix in a copy of the code and saw a test fail. No reviewer checked the last round of fixes. The owner and the assistant agreed to stop the reviews of the control there.
- `HANDOFF.md`, `README.md`, `src/README.md`, `WORKING-RULES.md` and a new `.gitignore` have the state of the end of this session. The owner said yes to these changes before the assistant made them. The assistant committed and pushed them, with the yes of the owner.
- The owner asked if "auto mode" also means no yes before a change. The assistant recommended that it covers only the tool permissions. The owner agreed.
- The assistant made a list of 63 changes for decisions 0024 and 0027 to 0036, so that they describe the control and correct the findings of the second review. The owner said yes, and the assistant made them. It checked two product facts in the Anthropic documentation: only `strict: true` guarantees the schema of a tool input (page "Structured outputs"), and the Messages API is stateless (page "Messages"). The draft forms do not set `strict`. That is now an open item of decision 0029.
- The owner said that the assistant asks for a yes too often. A new rule 32 in `WORKING-RULES.md` says when the assistant acts without a yes.
- An independent reviewer checked the 10 changed decisions. It found 2 serious and 5 minor items, and some smaller points. The assistant fixed them.
- The owner let the assistant select the diagrams to make again. The assistant made diagrams 07 (step 5) and 08 (step 6) again, in the visual form of diagrams 09 and 10, because decision 0038 changed those steps the most. A browser test opened each popup: 22 in diagram 07 and 17 in diagram 08. An independent reviewer checked their text and found 2 serious and 7 minor items. The assistant fixed them. It also corrected the false sentence of rule B4 in diagram 06, and an unclear example in decision 0033, item 8.

- The owner confirmed the text of decisions 0019 to 0036 and 0039. The assistant first asked if the yes covered the full text, and recommended that the owner read the files. The owner asked for one line for each file, and then confirmed. Rule 26 now applies to all decisions.

- The owner asked when the building starts. The assistant said that nothing blocks it, and that the workbook check need not come first. The owner agreed to start with step 1.
- Step 1 is built: `src/step1_plan.py`, with 20 tests. An independent reviewer found 1 serious and 7 minor items, and the assistant fixed them. The step now uses only `random()` of Python: the Python documentation (page "random", "Notes on Reproducibility", read on 7 October 2026) guarantees the same sequence only for `random()`.
- With the yes of the owner, step 1 made the real plan of mock 1: `runs/mock-01/plan.json`, seed 366341, scenarios 3, 1, 2 and 5. Scenario 5 gets all 12 questions of Domain 4, as decision 0027 expects for this set.
- The first section of the build guide exists: `docs/build-guide/step-1-plan-the-mock.md`. A script makes it from the records file and the plan. Diagram 02 is corrected: the step is built, and the old items are gone.

- Steps 3 and 8 have code and tests: `src/step3_check_code.py` and `src/step8_build_files.py`. An independent reviewer found 4 serious and 6 minor items. The assistant fixed them. Two were real faults: the control crashed when it saved the verdict of a question with an incomplete option, and step 8 built files from a record that did not agree with its slot. 116 tests pass. For each fix, a test fails without it.
- Steps 3 and 8 did not run on a real question, so they have no build guide section yet.

- Step 7 has code and tests: `src/step7_marking.py`. An independent reviewer found 3 serious and 6 minor items. The assistant fixed them. The main one: an owner who sorts only the column "Mark" moves marks to the wrong questions, and code cannot see it later. The sheet is now protected with no password, so only the two columns of the owner can change and sorting is off. This is not checked in real Excel. 132 tests pass.

- The model steps need a fixed form. Decisions 0029, 0032 and 0034 force a tool call, but the current models reject it. The assistant checked this on the page "Define tools". The owner asked if a model that supports it is better. The assistant recommended against it. Decided: structured outputs (decision 0040). The owner asked that this deviation from the exam guide is shown openly. The two pages are saved in `docs/sources/` and quoted word for word. The owner confirmed the text of decision 0040.
- Steps 2, 4, 5 and 6, the adapter `src/steps.py` and the command line `src/run.py` have code and tests. A test runs the whole pipeline with a fake client, from the plan to the two files. An independent reviewer found 3 serious items: call 4a had no guide text, the B6 search found names inside other words, and each API error was retried. The assistant fixed them and the minor items. Decision 0041 records each change beyond the confirmed decisions, and the owner confirmed its text. 161 tests pass. No real call to the API has run.

- The owner put the API key into `~/.bashrc`, outside the repository. The owner asked about a `.env` file and about identity federation. The assistant recommended `~/.bashrc` and an API key, because of the rule in `CLAUDE.md`. The package `anthropic` 1.11.0 is installed. The assistant checked the price page: Claude Opus 5.5 costs $4 per million input tokens and $20 per million output tokens.
- Decided: the plan of the test before the first full run (decision 0042). The owner said that the assistant does not need a yes for each small thing. Rule 33 records it.
- The test ran with real calls. Part 1: the writer made 10 questions, and all 10 passed step 3 at the first try. The owner marked 9 good and 1 bad (T-M1-S05: confusing, two names for one actor, long sentences). The owner asked the assistant not to look at the marking file before the owner said so. Part 2: call 4a answered 12 of 12 sample questions right. Part 3: call 4b passed the 9 good questions, and failed each of the 9 damaged copies on its rule. The assistant wrote the damages by hand in `runs/test-0024/damaged.json`. The test cost $2.64 in total.
- The bad mark of T-M1-S05 had no rule. The assistant first recommended an instruction to the writer only. The owner asked if that is enough. It is not (1.4-K2). A script measured the sentences: length did not cause the bad mark, so a code rule for length would not help. Decided: a writer instruction and a new rule B7 in call 4b (decision 0043).
- A check of B7 ran ($0.82): T-M1-S05 failed on B7, as expected. 3 of the 9 good questions also failed on B7, with true findings: two names for one actor. The owner said that cost is not a concern and asked what is best. Agreed: B7 stays strict for mock 1. The owner confirmed the text of decisions 0042 and 0043, after three corrections.

- Part 4 of the test ran ($0.40): the writer made 7 more questions of scenario 3, and the assistant wrote one copy with the same scene as T-M1-S06. Call 6a found the copy (D1). Step 6 also found real problems of the writer: one more pair with the same scene, and four pairs that give away an answer (D4). It also found one wrong idea in three questions (D2), but one of the three was the copy of the test, so the writer had it in only 2 questions, the limit. The assistant first reported it as a problem of the writer. A reviewer found that error. The whole test cost $3.86.
- The owner asked if everything is documented, with the diagrams. A script showed four gaps: only step 1 had a build guide section, diagrams 01 and 04 to 10 had old statements, six rows of `HANDOFF.md` were old, and no reviewer had checked decisions 0040 to 0043. The assistant closed all four before mock 1, with the yes of the owner.
- The diagrams 01 and 04 to 10 now describe the built steps. Diagram 04 shows the deviation of decision 0040 with its page and section. New build guide sections: steps 2, 3, 4, 6 and 7. Each popup of the ten diagrams opens and closes in a browser test.
- Two reviewers checked the work. The first found one serious item in the code (the prompt of call 4b said "six rules") and 10 minor items in decisions 0040 to 0043. The second found one error (a wrong claim about step 6 in a section and in this journal), 3 serious items in diagram 01 and the code, and 14 minor items. The assistant fixed each one. Decision 0044 records the corrections to the confirmed decisions 0040 to 0043, and the owner confirmed its text.

**Open**

- Rule B7 is stricter than the marks of the owner. In mock 1, the report shows how often it fails.
- The protection of the marking file is not checked in real Excel.
- Rule A11 passes "cannot" and "doesn't" (see `HANDOFF.md`).
- Diagrams 01 to 06 and 09 to 10 do not show decisions 0038 and 0039 yet.
- No reviewer checked the last fixes of the decisions and of diagrams 07 and 08.
- The real steps do not exist. Each step is a fake in the tests.
- The owner has no command line yet. The control has the functions.

Next: see "The next steps" in `HANDOFF.md`.

## 7 October 2026

This entry continues the third session of 6 October. The work went on after midnight.

- The owner and the assistant started to close the 10 new serious items one at a time. The owner agreed to item 1 (rule A11) and saw a suggestion for item 2.
- The owner then said: "I suspect that if we fix these new 10 issues and review we will keep finding more and the cycle will continue." The assistant agreed: the first review found 14 items, and the fixes made 10 new ones.
- The owner asked what the theme of the problems is. The answer: too much automatic repair, designed before one real run. The rules for a question are stable. The 9 steps stay.
- Decided: a simple control for mock 1, written as code with tests (decision 0038). The owner confirmed its text. It closes 3 of the 10 items, removes 2, and gives 5 to the code and its tests. It also corrects one sentence of decision 0037.
- A correction: the assistant said first that the simple control removes most of the 10 items. It removes 2.
- Decided: the work moves to Claude Code now. The folder moves out of OneDrive, to a folder in WSL with a private repository on GitHub. The owner makes the repository and copies the folder.
- The assistant read the Anthropic documentation on 7 October 2026 (code.claude.com/docs/en/memory): Claude Code reads `CLAUDE.md` in the project folder at the start of each session, and that file can import other files with `@`. It does not read `HANDOFF.md` automatically. The product treats these files as context and does not enforce them.
- A new file, `CLAUDE.md`, imports `WORKING-RULES.md` and says to read `HANDOFF.md` first. It has two more rules: no API key in the repository, and a test of the control makes no model call.
- The owner asked how many API credits the project needs. The assistant read the Anthropic price page on 7 October 2026 and estimated 50 to 100 US dollars for 5 mocks: 8 to 12 dollars for one mock with Claude Opus 5.5, 4 to 6 with Claude Sonnet 5.5. The token numbers are an estimate from word counts. The model and the number of mocks are not decided.
- `HANDOFF.md`, `README.md` and this journal have the state of the end of this session. The owner said yes to these changes before the assistant made them.

**Open**

- The control program and its tests do not exist.
- Items 6 to 10 of the second review have no answer yet.
- Decisions 0027 to 0036 and diagrams 02 to 10 do not agree with decision 0038.
- The other findings of the second review are not corrected.
- No independent reviewer checked decisions 0037 and 0038 after decision 0038.

Next: see "The next steps" in `HANDOFF.md`.

## 6 October 2026, third session

- The assistant read `HANDOFF.md` and the files that it names. It did not read diagrams 02 to 08.
- The assistant showed one proposal with an answer for each of the 14 serious items of the review. The owner asked to discuss them one at a time, and said yes to each one.
- The owner asked for a more simple explanation of items 8, 10, 12 and 14. The first explanations were too long.
- Item 8: the owner asked if code or a model must do the search for rule B6. Agreed: code.
- Item 12: the owner asked how the properties of the sample questions stay in the new questions. A script measured the 12 sample questions. Agreed: four new code rules, A8 to A11.
- A correction: the assistant said that 6 of the 11 sets have a scenario with 12 questions of one domain. The correct number is 9.
- Decision 0037 has the 14 answers. The owner confirmed its text.
- Two scripts are in `docs/decisions/`: `0037-check-scenario-tables.py` and `0037-check-sample-properties.py`. The assistant ran both in the folder. The results agree with decision 0037.
- The assistant showed the owner a list of the changes for decisions 0024, 0027 and 0029 to 0036, and five details that were new. The owner said yes. The assistant changed the 10 files. A script took each guide text from the records file.
- Six things were not in the list. The assistant told the owner after the change: the file `docs/diagrams/06-forms-draft.json` got the fields `letter` and `features`, each changed file got a line "Changed", rule A11 got an exact method in decision 0031, a failed count against the plan (rule C2) stops step 6 with an error, the record of step 6 got field names, and two items went into "Not decided yet".
- Two independent agents reviewed decisions 0024 and 0027 to 0037. The owner said yes to the 2 agents before they started. Result: each of the 26 guide quotes is exact, and each list "Exam guide points" agrees with its Reason. Of the 14 serious items, 8 are closed and 6 are closed in part. The reviewers found 3 new errors and 10 new serious items. The report is `docs/reviews/review-decisions-0024-to-0037.md`.
- One of the new serious items is an error of the assistant: it wrote a more exact method for rule A11 in decision 0031, and did not make decisions 0030 and 0037 agree.
- `HANDOFF.md`, `README.md` and this journal have the state of the end of this session. The owner said yes to these changes before the assistant made them.

**Open**

- The 10 new serious items of the second review are open. The other findings of that review are not corrected.
- Decision 0037 has one sentence that is too strong (point 1.4-K2). The owner confirmed its text, so the correction needs a new file (rule 26).
- Diagrams 02 to 10 show the design before decision 0037.
- The owner has not confirmed the full text of decisions 0019 to 0036.
- The list of open items is in `HANDOFF.md`.

Next: see "The next steps" in `HANDOFF.md`.

## 6 October 2026, second session

- The assistant read `HANDOFF.md` and the files that it names. It changed no file before the owner said so.
- The owner asked for short answers in the chat.
- Decided: the build guide does not show MCP, subagents, hooks or sessions at work (decision 0026). The owner accepted MCP and subagents first, and hooks and sessions after a second question. The assistant changed the new file of decision 0026 for the second answer before it told the owner. It told the owner after.
- The owner asked how long the work needs. The assistant estimated 6 to 10 sessions. The owner asked if the design needs that long. The answer was no: the time comes from one question for each detail.
- Agreed: a faster method for the design of the steps. One proposal for each step, and the owner accepts or changes it. This changes rule 1 (rule 30 in `WORKING-RULES.md`).
- Decided the design of step 1, the plan of a mock (decision 0027). The owner looked at each detail and said yes to each one. The assistant found one weak point after the proposal and told the owner: a task statement can be a bad fit for a scenario.
- Diagram 02 (step 1). The owner said that the first version was hard to read and asked for the hover popups of diagram 01. The assistant made it again with popups. The owner said: "It is better".
- The assistant showed a proposal for step 2. The owner said that it was not specific: no source for the story of the scenario, no records for code, no output format, no fields. The owner was right. Agreed: step 0 is designed before step 2, and each design names the exact file format and the exact fields.
- Decided the design of step 0 (decision 0028). The owner asked why all records are in one file, and what a point is.
- Step 0 ran. `src/step0_prepare_guide_records.py` made `reference/guide-records.json`: 5 domains, 6 scenarios, 30 task statements, 240 points, 12 sample questions and the 3 lists of Section 17.
- The checks of the records file. Check 2: `src/check_guide_records.py` passed 41 of 41 checks. Check 3: one independent agent found no errors, and listed 7 observations (`docs/reviews/review-guide-records.md`). Check 1, the comparison of our copy of the guide with the original, is not done. The assistant can read the original only as text in the chat.
- Diagram 03 (step 0). The owner said that the first version was a copy of the form of diagram 02 and had elements that are not necessary. The assistant made it again with a different idea: a document for people becomes records for code. The owner accepted it. Diagrams 04 to 07 have this form.
- Decided the design of step 2, the writer call (decision 0029). The owner did not understand the second proposal. The assistant told it as the story of one question. The owner asked to see the JSON schema and accepted it.
- The owner asked three questions on the architecture: why no subagent reviews the output in the same call, if the API can have subagents, and why the build does not use the SDK. The assistant read the Anthropic documentation: the Messages API is stateless and has no subagents. The owner said: "keep the simple api". The answers are in decision 0029.
- Diagram 04 (step 2).
- Decided the 13 rules for a good question (decision 0030).
- Decided the design of step 3, the code check (decision 0031). A script measured the 12 sample questions for the limits of rules A6 and A7: `docs/decisions/0031-check-sample-lengths.py`.
- The assistant wanted to make the diagram of step 3 later, together with the diagram of step 4. The owner asked for it. The assistant made diagram 05. Rule 13 says to make each diagram when its decision is made.
- Decided the design of step 4 (decision 0032): two calls for each question, a blind answer and then a rule check. The owner did not understand the first proposal. The assistant told it as a story. The owner asked what happens when the blind call is wrong. The answer is in the Reason of decision 0032. The owner also decided that call 4b always runs.
- A correction: the assistant said that the checker gets about 8000 words of guide text. A script counted about 5300 words. Decision 0032 has the correct number.
- Diagram 06 (step 4).
- Decided the design of step 5, the new try (decision 0033): the request of step 2 plus the failed question and its findings, at most 3 tries, then an open slot in the report. The owner asked if the answer is structured output. The answer was yes: the same form as in step 2.
- Diagram 07 (step 5).
- For each diagram from 02 to 07, a browser test in Chromium checked that each box opens its popup, that the popup stays in the window and that it closes. The tests passed. The test scripts are not in this folder.
- After that update, the session went on.
- Decided the design of step 6 (decision 0034). The owner asked if one API call is good enough for so many questions. The assistant said that it is 4 calls with 15 questions each, and changed the proposal to two calls for each scenario, each with one job.
- Diagram 08 (step 6).
- Decided the design of step 7 (decision 0035): the Excel marking file, the marks record, and the bad marks that stop a mock. The assistant added the folder `marking/` when it wrote the file, and told the owner after.
- The first diagram 09 (step 7) had the form of diagrams 03 to 08. The owner said: "the visuals could be better". The assistant made diagram 09 again as a sample in a new visual form: the thing itself, not a box with its name. The owner said: "much better". The owner said that the older diagrams do not have to be made again.
- Decided the design of step 8 (decision 0036): two JSON files for each mock, groups by scenario, and a fingerprint that stops the build when a record changed after its check.
- Diagram 10 (step 8), in the new visual form.
- Each of the 9 steps now has a design decision and a diagram. The assistant told the owner that the design of all 9 steps is complete. That was too early.
- Two independent agents reviewed decisions 0026 to 0036, the text of diagrams 02 to 10 and `HANDOFF.md`. The owner said yes to the 2 agents before they started. Result: each quoted guide text is exact and each number about the guide is true. But the reviewers found 4 serious contradictions, 10 serious gaps, 4 serious diagram errors and 2 serious handoff errors, and 13 of 47 uses of a guide point are not fair or do not state their context. The report is `docs/reviews/review-decisions-0026-to-0036.md`.
- The assistant corrected `HANDOFF.md`, `README.md` and this journal, with the yes of the owner: the design is not complete, and the 14 serious items are the next step. No decision file and no diagram is changed yet.
- `HANDOFF.md`, `README.md` and this journal were updated a second time, with the yes of the owner.
- (First update:) `HANDOFF.md`, `README.md`, `src/README.md` and `WORKING-RULES.md` have the state of the end of this session. The owner said yes to these changes before the assistant made them. The change of `src/README.md` was not in the list that the owner saw.

**Open**

- The 14 serious items of the review are open. The other findings of the review are not corrected.
- The owner has not confirmed the full text of decisions 0019 to 0036.
- A decision on the Agent SDK is not written: no step uses it.
- Check 1 of the records file is not done. The assistant asked the owner if the original guide file is on the computer. The owner did not answer yet.
- The folder is not a git repository.
- The list of open items is in `HANDOFF.md`.

Next: see "The next steps" in `HANDOFF.md`.

## 6 October 2026, first session

- The owner confirmed Part B of `WORKING-RULES.md`, with one change: rule 26 permits a change to the status line of a decision file.
- The owner confirmed the text of decision 0001, with one change: 3.4-K1 is not in the list of exam guide points, because the decision does not use plan mode.
- The owner confirmed the text of decision 0002, with three changes. Option 3 now says: the Claude API for a step that is one request with a fixed output format, the Agent SDK for a step in which the model works in a loop with tools. The last line of the Reason now says "the Agent SDK". The note on Scenario 6 now says "JSON schemas", because the guide does not name the API there. The assistant checked the product facts in the Anthropic documentation (platform.claude.com and code.claude.com).
- A diff checked each of the three files. No independent reviewer checked them.
- Decided that a mock has the same form as the exam (decision 0003).
- Decided that the build does not use the questions of the first build (decision 0004). The owner asked about bias, and the assistant changed its recommendation from option 1 to option 2.
- Decided that ruling 1 of 29 September applies: a question depends only on features that the exam guide names (decision 0005).
- Decided that ruling 2 of 29 September applies, with two limits from the original text (decision 0006). The assistant read the original briefs in `CCAR-F Mocks v2/reference/first-build/rubric/`. The owner gave read access to `CCAR-F Mocks v2` and `CCAR-F Portal Mocks` for that.
- Decided that ruling 1 covers each text that a participant sees, also the explanation (decision 0007, adds to 0005).
- Decided that the exam guide is the only source of facts in the first version (decision 0008). The owner asked how a documentation source would work, and the assistant suggested a form that is recorded in 0008 and not decided.
- Decided step 1 of the pipeline: code makes the plan of a mock, a list of 60 slots (decision 0009).
- Decided step 2 of the pipeline: a model writes one question for one slot, in one API call (decision 0010).
- Decided step 3 of the pipeline: code checks each question against the rules that have an exact answer (decision 0011).
- Decided step 4 of the pipeline: an independent model call checks each question, as a plain API call (decision 0012). The owner asked if the pipeline needs subagents. The answer is in 0012: not for independence, and no agreed step needs the Agent SDK.
- Decided step 5 of the pipeline: a failed question goes back to the writer with the findings, up to a limit of tries (decision 0013).
- Decided step 6 of the pipeline: the program checks the complete mock, with a code count and one model call for each scenario (decision 0014).
- Decided step 7 of the pipeline: the owner marks a random sample of each mock, with no verdict in view (decision 0015).
- Decided step 8 of the pipeline: code builds the mock files from the question records, and nobody edits an output file by hand (decision 0016).
- Decided step 0 of the pipeline: prepare the guide records, one time for each version of the guide (decision 0017). The owner corrected the assistant two times: the 240 points exist already, and the work must be documented as a step.

**After the decisions**

- The owner did not confirm that the list of steps 0 to 8 is complete. The owner asked if everything is covered.
- The assistant compared the steps with the 22 lessons in `docs/lessons.md`. The owner then asked where the lessons come from, and if the assistant had used them for the design. The answer was yes, for most reasons and for the sequence of the steps.
- The owner decided: `docs/lessons.md` is private history of the first build. It is not a source for the design. The file stays in the folder.
- The assistant made a table that compares the reason of each step with the exam guide: 3 steps full, 5 in part, 1 none. The owner accepted the table.
- The Reason section of decisions 0003 to 0017 is new. The rule: the reason is an exam guide point with its ID, or a section of the guide, or a ruling of the owner, or one plain sentence. A Reason has no lesson number and no F number. Decisions 0010 and 0016 have a plain reason and no exam guide point.
- Each decision from 0003 to 0017 has a new section "How we decided", below the Reason.
- Decision 0004 no longer says that `docs/lessons.md` stays in use.
- Decisions 0001 and 0002 did not change. Each names the first build in its reason.
- Decided: for each step we decide what it receives, what it returns and what can fail, and the final script also checks that each answer in the workbook names a step that exists (decision 0018).
- A script compared each quoted exam guide text in decisions 0001 to 0017 with `reference/task-statements-and-points.md`: 20 quotes, 0 differ. The same check for the three quotes in decision 0018: 0 differ.

**Other files**

- `HANDOFF.md`: the lesson is out of the list "Read these files first". The sections "Where we are", "What a finished mock is", "The next steps" and "Things that are open" have the state of 6 October. A new section describes the build guide. The table "Words" has "the exam guide" and "the build guide".
- `README.md` and `docs/lessons.md`: the label "Private history of the first build. Not a source for the design." `docs/lessons.md` also says that lesson 3 leaves out the two limits of ruling 2.
- New folder `docs/build-guide/` with a README. The build guide "How the Mocks Are Built" is a product of this work, with the same weight as the program. No section exists.
- New diagram `docs/diagrams/01-pipeline-overview.html`: the 9 steps on one page, with the path of a question that fails. Each box opens a popup with the exam guide points of its step. A script took each exam guide text from the points file. A test in Chromium passed 26 of 26 checks. The assistant wrote the sentences "receives, does, returns" and "Why here" in the popups.
- `docs/diagrams/README.md` lists diagram 01. Its rule is now: a diagram for participants uses plain words and no decision numbers, and the decision file names its diagram. Decisions 0009 to 0017 name diagram 01 in the line "Diagram".
- The owner confirmed the text of decisions 0003 to 0018. Each of the 16 files has the line "Text confirmed by the owner: 6 October 2026". Rule 26 applies to them.
- One independent agent reviewed decisions 0003 to 0018 against the exam guide: 41 uses, 14 agree, 26 agree in part, 1 does not agree. Each quote was exact. The report is `docs/reviews/review-decisions-0003-to-0018.md`.
- Decided: one file corrects the errors that the review found (decision 0019). The 26 "in part" results stay, and the build guide and the popups will name the context of each point. The owner approved a short form of the text of 0019. The owner did not confirm its full text.
- Decided: a question from step 5 goes through the checks again (decision 0020).
- Decided: a bad mark of the owner sends the question to step 5, and too many bad marks stop the mock (decision 0021).
- Decided: the owner reads all 60 questions of mock 1, then 20 of each later mock (decision 0022).
- Decided: the checker has a third verdict, "cannot decide" (decision 0023).
- Decided: a test of the writer and of the checker comes before the first full run (decision 0024).
- The owner confirmed that the list of steps 0 to 8 is complete for one mock (decision 0025). The design of each step can start.
- Diagram 01 has decisions 0019 to 0025: the new question is checked again, "cannot decide", the bad mark, the size of the sample and the test before the first full run. Each point in a popup names its task statement. The browser test passed 26 of 26 checks.
- `HANDOFF.md` and `README.md` have the state of the end of 6 October. `README.md` lists `docs/build-guide/` and `docs/reviews/`.

**Open**

- No independent reviewer checked decisions 0001, 0002 and 0019 to 0025, `HANDOFF.md`, or diagram 01 and the sentences in its popups.
- Not decided: how the program prevents the same scene in two different mocks, and how many mocks the program makes.
- The owner has not confirmed the text of decisions 0019 to 0025.
- The folder is not a git repository.
- The owner has not decided if the build guide must also show MCP and subagents at work. The pipeline uses none.

Next: see "The next steps" in `HANDOFF.md`.

## 5 October 2026

- Decided to start clean in this folder (decision 0001).
- Decided that the build is a program with the Claude API and the Agent SDK (decision 0002).
- Made the file `reference/task-statements-and-points.md`. An independent reviewer confirmed all 240 points against the exam guide copy.
- Made the workbook `docs/coverage/task-statement-decisions.xlsx`. No decision is filled in yet.
- Started a discussion of task statement 1.1 and stopped it. The assistant had assumed a pipeline sequence that nobody had agreed on.
- Wrote `HANDOFF.md`, `WORKING-RULES.md` and `docs/lessons.md` for a new session. Two independent reviewers checked the first version, and a third reviewer checked the second version. The assistant applied the corrections of the third reviewer. Nobody reviewed that last version.
- Not done: version control. The folder is not a git repository yet.

Next: see "The next steps" in `HANDOFF.md`.
