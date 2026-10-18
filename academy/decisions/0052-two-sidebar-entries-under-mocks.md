# 0052: Two sidebar entries under "Mocks"

- Date: 16 October 2026
- Status: accepted
- Text confirmed by the owner: 16 October 2026 (accepted in the discussion, working rule 35)
- Diagram: none

## Question

Where do the two tabs go in the navigation of the portal?

## Decision

Two new entries in the sidebar (`frontend/src/layouts/nav.ts`), directly under "Mocks", with `sectionSlug: 'learning'`:

- "Exam guide breakdown" at `/exam-guide-breakdown`
- "Behind the mocks" at `/behind-the-mocks`

## Reason

Decision 0010 says: "Each section is one tab of the portal." The paths use the names of decision 0001, so each link says which tab it opens. The same participants who can open the mocks can open the tabs.

## How we decided

The assistant recommended it. The owner agreed.

## Exam guide points

None.
