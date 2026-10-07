# 0019: Corrections to decisions 0003 to 0018 after the independent review

- Date: 6 October 2026
- Status: accepted
- Text confirmed by the owner: 7 October 2026, after a summary of one line for each file
- Diagram: none

## Question

An independent reviewer compared the reasons in decisions 0003 to 0018 with the exam guide. It found errors. The owner confirmed the text of those files, so rule 26 applies. How do we correct the errors?

## Options

1. One new decision file that names each affected file and gives the correction.
2. One new decision file for each affected file.
3. No correction.

## Decision

Option 1. The decisions stay as they are. Only the parts below change. Where this file and an older file disagree, this file is correct.

1. **Decision 0012 (step 4).** The sentence that uses 5.2-K3 is withdrawn. That point is about escalation in customer support, and the checker gives verdicts, not confidence scores. The plain reason stays: a verdict of the checker is not proof, and step 7 tests it with the marks of the owner. One more point applies to step 4: "Running verification passes where the model self-reports confidence alongside each finding to enable calibrated review routing" (4.6-S3). The design of step 4 must decide if the checker reports a confidence value.
2. **Decision 0006 (ruling 2).** The first limit is wider. A use of model confidence that the guide teaches as correct does not count as the wrong option. The guide teaches four such uses: "Field-level confidence scores calibrated using labeled validation sets for routing review attention" (5.5-K3), "Having models output field-level confidence scores, then calibrating review thresholds using labeled validation sets" (5.5-S3), "Routing extractions with low model confidence or ambiguous/contradictory source documents to human review, prioritizing limited reviewer capacity" (5.5-S4) and 4.6-S3 (text above).
3. **Decision 0013 (step 5).** The guide does not give a limit of tries. Points 4.4-K2 and 4.4-S2 say when a retry cannot help. They do not give a number. The limit has a plain reason: with no limit, a slot that cannot pass makes the program try with no end. "An open slot goes to a person" is also a plain reason. The limit is not the main way to stop. The main way to stop is a question that passes the checks. The guide names the opposite as an anti-pattern for agent loops: "setting arbitrary iteration caps as the primary stopping mechanism" (1.1-S3).
4. **Decisions 0005 and 0007 (ruling 1).** The sentence "The guide supports it" is withdrawn. Section 17 lists what "might appear on the exam". It does not say that a feature that it does not name is not tested. The rule stands on the ruling of the owner.
5. **Decision 0008.** The sentence "Where the documentation and the guide disagree, the answer of the guide is the answer of the exam" is a choice of the owner for the mocks. The guide does not say it. The sentence "The exam tests the guide" has this source: "Exam items are written against these objectives" (Section 6).
6. **Decision 0007.** `CLAUDE_HEADLESS` is an environment variable. `--batch` is a flag. Both are wrong options in sample question 10.
7. **Decision 0003.** The 6 scenarios are in Section 5 of the guide. Sections 3 and 4 give the other facts.
8. **Decision 0018.** The guide has points on what a step returns. For tools: "Splitting generic tools into purpose-specific tools with defined input/output contracts (e.g., splitting a generic analyze_document into extract_data_points, summarize_content, and verify_claim_against_source)" (2.1-S3). For agents: "Modifying upstream agents to return structured data (key facts, citations, relevance scores) instead of verbose content and reasoning chains when downstream agents have limited context budgets" (5.1-S6).
9. **Decision 0012, the line "Exam guide points".** The ID 1.2-K2 is in the section "How we decided", not in the Reason.

## Reason

A reason that does not agree with its source is an error in the record, and the build guide takes its content from the Reason sections. The plain reason for one file: the corrections are short, and one file is easier to read than seven.

The guide does not cover this: how to correct a confirmed record.

## How we decided

One independent agent checked 41 uses of the exam guide in the 16 files: 14 agree, 26 agree in part, 1 does not agree. Each quoted text was exact. The full report is in `docs/reviews/review-decisions-0003-to-0018.md`.

The 26 "agrees in part" results have one cause: the reason uses a point that the guide wrote for a different context, for example code review or data extraction, and does not say so. This file does not change those reasons. The build guide and the popups of the diagram will name the context of each point.

The reviewer also said that points 4.5-K4 and 4.5-S3 support the reason of decision 0010 (step 2). The owner decided on 6 October 2026 not to use those points for step 2. That decision stays.

## Exam guide points

4.6-S3, 5.5-K3, 5.5-S3, 5.5-S4, 1.1-S3, 2.1-S3, 5.1-S6
