# Independent review of decisions 0003 to 0018
Date: 6 October 2026. Reviewer: one independent agent. It did not write the files and did not see the design discussion.
Sources that the reviewer read: the 16 decision files, `reference/task-statements-and-points.md` and `reference/exam-guide.md`. It changed no file.
The reviewer was told to be strict about context: a point from a different context counts as "agrees in part".

Review of the 16 decision files (0003 to 0018) is complete, read only. All IDs in every "Reason" resolve to real points and every ID-tagged quote is an exact substring. The weak spot is context transfer: 26 of 41 rows are "agrees in part" and 1 is "does not agree".

## 1. Table

| File | ID or section | Verdict | Why |
|---|---|---|---|
| 0003 | Section 3 | agrees | 60 items, 120 minutes, "4 scenarios drawn from a bank of 6", and "each item states how many responses to select" are all there; the 6 scenarios themselves are in Section 5, which 0003 does not cite. |
| 0003 | Section 4 | agrees | Weights 27/18/20/20/15 and the word "approximate" are there; the guide says "approximate proportion of scored items", and 0003 drops "scored". |
| 0004 | 5.5-K3 | agrees in part | Point: "Field-level confidence scores calibrated using labeled validation sets for routing review attention" (task 5.5, extraction review). What is calibrated is field-level confidence scores, not "a checker", and the point does not say that a person makes the labels. |
| 0005 | Section 17 | agrees in part | The three quoted phrases are exact, but Section 17 nowhere says that a feature it does not name is not tested. "might appear" is not an exhaustive list, and "will not appear" covers only the listed out-of-scope topics. |
| 0006 | 5.2-K3 | agrees in part | Point: "Why sentiment-based escalation and self-reported confidence scores are unreliable proxies for actual case complexity" (task 5.2, customer-support escalation). The Reason concludes "a fair wrong option" for every scenario without naming that context. |
| 0006 | Section 9, sample question 3 | agrees | Option B is the self-reported confidence score with a threshold, and the explanation calls it wrong ("poorly calibrated"). |
| 0006 | 5.5-K3 | agrees | Full exact quote, and the first limit matches it (field-level, calibrated, routing to review). |
| 0007 | Section 9, sample question 10 | agrees | Options B and D contain `CLAUDE_HEADLESS` and `--batch`; the guide calls both "non-existent features". |
| 0007 | task statement 1.1 | agrees in part | "iteration caps" exists only in 1.1-S3, as an anti-pattern: "setting arbitrary iteration caps as the primary stopping mechanism". The guide never mentions "maxTurns", so it cannot confirm that the two are the same thing. |
| 0008 | sample questions 1, 2, 3, 10 (no section number given) | agrees in part | "Twelve" is correct, and the correct answers follow from 1.4-S1, 2.1-K2, 5.2-S1 and 3.6-K1/S1. For question 10, the only place the guide says options B and D are wrong is the explanation of question 10 itself. |
| 0009 | 1.4-K2 | agrees | Full exact quote; task 1.4 is workflow enforcement, and the general principle transfers to "counts must hold each time". |
| 0009 | 1.6-S1 | agrees in part | Point is about "predictable multi-aspect reviews" and prompt chaining, which is a sequence of model prompts. A list of 60 slots made by code for a generation task is neither a review nor a prompt chain. |
| 0009 | 1.6-K1 | agrees in part | Point: "When to use fixed sequential pipelines (prompt chaining) versus dynamic adaptive decomposition based on intermediate findings". It names the choice but not the rule, and has the same context gap as 1.6-S1. |
| 0009 | Sections 3 to 5 | agrees | Form, weights, scenarios and primary domains are in Sections 3, 4 and 5; but "(decision 0003)" cites only Sections 3 and 4. |
| 0011 | 1.4-K1 | agrees in part | Point: "The difference between programmatic enforcement (hooks, prerequisite gates) and prompt-based guidance for workflow ordering". The quote stops before "for workflow ordering"; the point is about the order of steps, not about checking the content of a record. |
| 0011 | 1.4-K2 | agrees | The paraphrase drops the condition "When deterministic compliance is required", but the sentence before it supplies that condition. |
| 0011 | 4.3-K3 | agrees | Exact quote; task 4.3 is structured output in general. |
| 0011 | 4.4-K4 | agrees | The point states the same split between semantic and syntax errors; its task statement is "for extraction quality". |
| 0011 | 5.3-K4 | agrees in part | Point is in task 5.3, "error propagation strategies across multi-agent systems": an agent hides its own failure. The Reason applies it to a code check that rejects an empty writer output, without naming the context. |
| 0012 | 4.6-K1 | agrees | Exact quote; general review context. |
| 0012 | 4.6-K2 | agrees | Full exact quote. |
| 0012 | 4.6-S1 | agrees in part | Point: "Using a second independent Claude instance to review generated code without the generator's reasoning context". The context is generated code. |
| 0012 | 3.6-K4 | agrees in part | Point is about "the same Claude session that generated code" in task 3.6 (Claude Code in CI/CD). |
| 0012 | 5.2-K3 | does not agree | The middle sentence restates the point correctly, but the claim it carries is "The doubt of the checker is not proof". The point is about confidence scores as a proxy for "case complexity" in escalation; the checker in this Decision gives verdicts, not confidence scores. If you judge only the middle sentence, this row is "agrees in part". |
| 0013 | 4.4-K1 | agrees | Exact quote with generic wording; its task statement is "for extraction quality". |
| 0013 | 4.4-S1 | agrees in part | Point: "the original document, the failed extraction, and specific validation errors for model self-correction". It is an extraction context, and the mapping of document to slot and extraction to question is not stated. |
| 0013 | 4.4-K2 | agrees in part | Point: "The limits of retry: retries are ineffective when the required information is simply absent from the source document (vs format or structural errors)". It names a kind of failure that a retry cannot repair, not a maximum number of tries, so "So the tries have a limit" does not follow from it. |
| 0013 | 4.4-S2 | agrees in part | Point: "Identifying when retries will be ineffective (...) versus when they will succeed (...)". It classifies failures; it gives no count limit and no hand-over to a person. |
| 0014 | 4.6-K3 | agrees in part | The mapping to questions is stated, but the point is a review of files and its integration pass is for cross-file issues, not for duplicates. Its stated purpose is "to avoid attention dilution", and step 6 reads all questions of a scenario in one call. |
| 0014 | 4.6-S2 | agrees in part | Point: "integration passes for cross-file data flow analysis"; multi-file code review, not a duplicate search. |
| 0014 | 1.6-K2 | agrees in part | Point: "analyze each file individually, then run a cross-file integration pass"; review of files. |
| 0015 | 5.5-K2 | agrees in part | Point is about "high-confidence extractions" (data extraction). The step has no confidence scores, and the transfer to questions is not stated. |
| 0015 | 5.5-S1 | agrees in part | Same extraction context: "stratified random sampling of high-confidence extractions for ongoing error rate measurement". |
| 0015 | 5.5-K1 | agrees in part | Point names "specific document types or fields"; the Reason maps these to scenario and domain without saying so. |
| 0015 | 5.5-S2 | agrees in part | Full point: "Analyzing accuracy by document type and field to verify consistent performance across all segments before reducing human review". The quote leaves out the words that carry the extraction context. |
| 0017 | 1.3-S2 | agrees in part | Point is about "passing context between agents" (task 1.3, subagents). The Decision is a one-time preparation of record files, and decision 0012 says the pipeline call "is not a subagent". |
| 0017 | 5.6-K1 | agrees in part | Point names loss of attribution "during summarization steps" (task 5.6, multi-source synthesis). The Decision has no summarization step; the risk it guards is a model that copies guide text wrongly. |
| 0017 | 5.6-K2 | agrees in part | Point: "structured claim-source mappings that the synthesis agent must preserve and merge when combining findings"; synthesis agent context. |
| 0018 | 1.3-K2 | agrees | Exact quote, and the Reason itself says "The guide says this for subagents". |
| 0018 | 5.3-K1 | agrees in part | Point is about "coordinator recovery decisions" in multi-agent systems. Unlike the 1.3-K2 sentence, the Reason does not name that context. |
| 0018 | 5.3-K4 | agrees in part | Same multi-agent context, not named. |

Files 0010 and 0016 have no ID and no section reference in the Reason. The "ruling of the owner" claims in 0005, 0006 and 0007 cannot be checked from the three permitted sources.

## 2. Quote problems

No quote with an ID fails the exact-substring test (checked by code against the points file). The section quotes in 0005 ("might appear on the exam", "explicitly tested", "will not appear") are exact in Section 17.

Partial quotes where the words left out change or narrow the meaning:
- **0004, 5.5-K3:** only "labeled validation sets" is quoted. Left out: "Field-level confidence scores calibrated using" and "for routing review attention". The subject becomes "a checker", which the point does not say.
- **0006 and 0012, 5.2-K3:** left out "Why sentiment-based escalation and". This removes the only word that shows the point is about escalation.
- **0011, 1.4-K1:** left out "for workflow ordering". The point is limited to the order of steps.
- **0013, 4.4-K2:** left out the label "The limits of retry:" and "(vs format or structural errors)". With them, the point is a contrast between kinds of failure; the Reason reads "limit" as a count.
- **0015, 5.5-S2:** left out "Analyzing accuracy by document type and field to". This hides the extraction context.
- **0011 and 0018, 5.3-K4:** left out "or terminating entire workflows on single failures are both anti-patterns". The meaning of the quoted half does not change, but the second anti-pattern is silently dropped.

## 3. ID list mismatches

- **0012:** 1.2-K2 is in the list but not in the Reason. It is only in "How we decided" ("A subagent gives a separate context (1.2-K2)"); that use agrees with the point.
- **0007:** the list says "none. The decision uses Sections 9 and 17". The Reason names Section 9 and task statement 1.1, and does not mention Section 17. The Reason relies on the text of 1.1-S3 without giving the ID.
- All other files: the Reason and the list match.

## 4. Unsupported guide claims

- **0008:** "The exam tests the guide." No reference. Section 1 ("authoritative reference") and Section 6 ("Exam items are written against these objectives") would support it, but neither is cited.
- **0008:** "Where the documentation and the guide disagree, the answer of the guide is the answer of the exam." No reference, and the guide does not say this. The explanations of sample questions 4 and 10 appeal to what is "documented" and what "doesn't exist in Claude Code".
- **0008:** "The guide alone is sufficient for its own sample questions". No section number; it rests on a check of 4 of 12 by the assistant (see the table row).
- **0005 and 0007:** a feature that the guide does not name is "something that the exam does not test". This goes further than Section 17 (see the table row). In 0007 it has no reference at all.
- **0013:** "an open slot goes to a person" is given as a consequence ("So") of 4.4-K2 and 4.4-S2. Neither point says this. The same file lists "who decides on an open slot" as not decided.
- **0004:** the implied claim that "labeled" means labelled by a person. 5.5-K3 does not say who makes the labels.

## 5. Points that the author missed

Where a Reason says "the guide does not cover this" or "no exam guide point":

- **0018** ("what a step returns when it succeeds"): not true.
  - 2.1-S3: "Splitting generic tools into purpose-specific tools with defined input/output contracts" (tools context).
  - 5.1-S6: "Modifying upstream agents to return structured data (key facts, citations, relevance scores) instead of verbose content and reasoning chains" (agents context).
  - 2.2-S4: "valid empty results (representing successful queries with no matches)".
- **0010** ("No exam guide point gives this reason"): not true for two of the three parts, in the Batch API context.
  - 4.5-K4: "custom_id fields for correlating batch request/response pairs" (one record, one ID).
  - 4.5-S3: "Handling batch failures: resubmitting only failed documents (identified by custom_id)" (write only the failed one again).
- **0014** ("the search for a wrong option that repeats", "the code count against the plan"): partly covered.
  - 3.6-S4: "Providing existing test files in context so test generation avoids suggesting duplicate scenarios already covered by the test suite" (CI test generation). This is the guide's method against duplicates, and it works at the writing step; decision 0010 gave that up.
  - 1.2-S3 covers a gap check in part: "the coordinator evaluates synthesis output for gaps".
- **0009** ("a list of slots before the writing"): partly covered by 1.2-S2: "Partitioning research scope across subagents to minimize duplication (e.g., assigning distinct subtopics or source types to each agent)" (subagent research context).
- **0011** ("the code check comes before the model check"): the order is partly covered by 1.4-S1: "Implementing programmatic prerequisites that block downstream tool calls until prerequisite steps have completed". The cost reason ("to save model calls") and the exam-question quality rules are not covered; that part of the statement is true.
- **0017** ("no model copies guide text", "made one time"): partly covered by 5.1-S1: "Extracting transactional facts (amounts, dates, order numbers, statuses) into a persistent "case facts" block included in each prompt, outside summarized history" (customer support context). "Checked character for character" is not covered.
- **0004** ("No exam guide point gives the complete reason"): true as worded. 4.2-K1 gives weak partial support for "copies their style": "Few-shot examples as the most effective technique for achieving consistently formatted, actionable output".
- **0003, 0015, 0016:** the "does not cover" statements are true. I found no point on the number of multiple-response items, on questions per scenario, on blind marking, or on one true copy.

Points that speak against a Reason and are not cited:

- **0006 and 0012:** 4.6-S3: "Running verification passes where the model self-reports confidence alongside each finding to enable calibrated review routing". The guide teaches self-reported confidence as correct here.
  - For 0006: this is outside task statement 5.5 and is not field-level, so limit 1 does not cover it.
  - For 0012: it is in task statement 4.6, from which the Reason cites three other points, and it is about verification passes, which is what step 4 is.
- **0006:** 5.5-S4 ("Routing extractions with low model confidence ... to human review") and 5.5-S3 are further correct uses.
- **0013:** 1.1-S3 names "setting arbitrary iteration caps as the primary stopping mechanism" as an anti-pattern (agentic loop context). It is relevant to a limit of tries and is not cited.

## 6. Errors of fact in a Decision section

- **0007:** "A flag that the guide itself gives as a wrong option ... Example: `--batch` and `CLAUDE_HEADLESS`". In sample question 10, `CLAUDE_HEADLESS` is an "environment variable", not a flag.
- **0003:** "the form that the exam guide gives in Sections 3 and 4" includes "the 6 scenarios of the guide". The 6 scenarios are in Section 5. This is a wrong citation, not a wrong number.

All numbers are correct: 60, 120, 4 of 6, the five weights, 30 task statements, 240 points, 12 sample questions, and the section numbers in 0005.

## 7. Counts

41 rows: 14 "agrees", 26 "agrees in part", 1 "does not agree".

## 8. Not checked

- I did not check the rulings of the owner of 29 September 2026, the "How we decided" sections (except the location of 1.2-K2), or the Anthropic documentation claim in 0012.
- I did not check any other file that the decisions name (`REVIEW3.md`, `HANDOFF.md`, the diagram, the workbook), or `reference/exam-guide.md` against the original guide.
- The points file does match Section 6 of `exam-guide.md`: 240 of 240 points and 30 of 30 titles, compared by code.
