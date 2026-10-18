# 0056: Three pull requests, and a new session for the work in the portal

- Date: 19 October 2026
- Status: accepted
- Text confirmed by the owner: 19 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none

## Question

The rules of the portal ask for an approved plan section in its `PLAN.md` before any code, a feature branch, a pull request for each change, and few pull requests. Who does the work in the portal, and in which pull requests?

## Decision

1. A new session, started inside `~/magnetlab-academy`, does all the work in the portal. It starts with `/add-dir /home/triggger/ccar-f-mock-generator` and only reads this repository.
2. This session prepares the draft plan section `academy/portal-plan.md`. It ends with a start note: the decisions, the checked facts, the first step and the files to take.
3. Three pull requests, in this order:
   1. The plan section in `PLAN.md`. Its merge is the approval.
   2. The mocks (decision 0055): the fifth option, the two new columns, the converter, the five files `mock-N.v2.json` and the fixed tests.
   3. The tabs: the React page (decision 0051), the two sidebar entries (decision 0052), the font (decision 0053), the scroll to a `#hash`, the copied pages (decision 0050), and the link from the answer review to tab 1 (decision 0055, item 8).

## Reason

- A session loads the `CLAUDE.md` of its start folder and of the folders above it, not of a folder next to it (code.claude.com/docs/en/memory). A session started in the portal loads the rules of the portal from the start.
- The mocks come first, because they are the core of the portal and do not depend on the tabs. The link to tab 1 needs the route of tab 1, so it goes with the tabs.

## How we decided

The owner asked whether this session can work in both repositories. The assistant checked the official documentation and recommended a new session for the portal. The owner asked whether a handover file is needed, and whether the new session knows where to get the files. The assistant said that the start note must list the files with their paths. The owner agreed to the three pull requests.

## Exam guide points

None.
