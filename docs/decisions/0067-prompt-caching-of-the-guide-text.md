# 0067: Prompt caching of the guide text

- Date: 9 October 2026
- Status: accepted
- Text confirmed by the owner: 9 October 2026
- Diagram: `docs/diagrams/06-step-4-check-by-a-model.html` (step 4). Diagram 04 shows the cached rules of the writer.

## Question

The program did not use prompt caching. Each check call sent the full text of the guide again, at the full input price. Mock 3 sent 3.84 million input tokens ($15.34) and cost $23.85 in total. Can the program send the same text more cheaply, with no change to what the model sees?

## Options

1. Prompt caching: the fixed text comes first in each request, identical each time, with a cache mark.
2. The Message Batches API. The owner rejected it: the rounds of the pipeline would wait for each batch.

## Decision

Option 1.

1. **Call 4a** sends the guide text (all 30 task statements with their 240 points, and the three lists of Section 17) as the first block of the system prompt, with a cache mark. Then its instruction. The story of the scenario moves from the guide block to the user text, so the guide block is the same for each scenario.
2. **Call 4b** sends the same guide block first, then the 12 sample questions as a second cached block, then its instruction. The story, the earlier questions, the rules and the question are in the user text.
3. **The writer** sends its list of rules as a cached block first. A narrow idea has its own list, with the copy rule B9 (decision 0066), so it has its own cache.
4. **The run records** save the cached tokens: `cache_write_tokens` and `cache_read_tokens`. The cost uses the prices of the page "Prompt caching", section "Pricing", read on 9 October 2026: a 5-minute cache write costs 1.25 times the input price, and a cache hit on Claude Opus 5.5 costs 0.05 times the input price ($0.20 per million tokens).
5. **The minimum cacheable size** for Claude Opus 5.5 is 512 tokens (same page, section "Cache limitations"). All calls use that model. The guide block (about 15,000 tokens), the block of call 4b (about 19,000 tokens) and the writer's rules (about 800 tokens) are above it.
6. **No Message Batches API.**
7. A test checks that the cached blocks are identical in each call, for each scenario.

## Reason

**The measured saving** (`src/test_cache.py`, results in `runs/test-cache/results.json`): calls 4a and 4b checked 10 questions of mock 3 again. The calls cost $0.58 with caching. The same tokens with no caching cost $1.72. That is about 66% less on the check calls. From the second question on, each call read its block from the cache. Calls 4a and 4b keep separate caches, probably because their answer forms differ.

**2 of the 10 verdicts changed**, both from pass to fail, both on borderline questions:

- M3-S31: rule B9, the same scene and answer as M1-S10 (a named session, continue it with --resume). The independent agent had called this pair a close repeat.
- M3-S49: rule B8, the scene of sample question 5.

The same 2 questions, checked once more with no cache and the guide in the user text, both passed.

**Possible causes, not separated:**

- The guide and the sample questions now sit in the system prompt, not in the user text.
- Normal variation between runs: the checks are judgments of a model.

The owner also named the stricter rule B9 of decision 0066 as a possible cause. The test script used the text of B9 that checked mock 3 (decision 0056), not the stricter text, so that cause does not apply to this test.

**Mock 3 stays accepted.** The two questions are not reopened.

## How we decided

The owner asked if the program uses prompt caching. The assistant said no, estimated a saving of about $10 for each mock from the run records of mock 3, and showed the change. The owner agreed, and added the test on 10 questions, the check of the minimum size, and the measured saving. The owner rejected the Message Batches API. After the test, the owner decided: no repeat test, record the decision as it is, and mock 3 stays accepted.

The owner confirmed the text of this file on 9 October 2026. No independent reviewer checked this file.

## Exam guide points

none
