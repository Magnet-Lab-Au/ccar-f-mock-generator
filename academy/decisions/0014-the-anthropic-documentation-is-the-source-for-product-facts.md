# 0014: The Anthropic documentation is the source for product facts

- Date: 13 October 2026
- Status: accepted. Decision 0030 adds a dated copy of each documentation page.
- Text confirmed by the owner: 13 October 2026
- Diagram: none
- Changes: decision 0011, adds one source to the order of trust

## Question

The "Beyond the exam" parts, such as the 7 stop reasons of the API, use the Anthropic documentation. The order of trust of decision 0011 does not list it. Where do facts about Claude products come from?

## Decision

The official Anthropic documentation is the source for facts about Claude products: the API, Claude Code and the Agent SDK. The fact agent reads the documentation page live, and records its URL and the date that it read the page.

If the documentation and the exam guide disagree, the page shows both, and says which one the exam uses.

## Reason

The products change, so a fact from memory can be out of date (working rule 9). The exam guide was written at one point in time. A participant must know what the exam expects, and also what is true today.

## How we decided

After decision 0013, the assistant found the gap: Fig. 4 of the 1.1 sample uses the documentation, but decision 0011 does not name it. The assistant recommended the addition. The owner accepted it.

## Exam guide points

none.
