# The portal work: MagnetLab Academy

This folder has the records of the portal work. It is separate from the mock generator (decision 0007).

- `brief.md`: the MVP brief from the Cowork discussion of 12 October 2026.
- `decisions/`: the decisions of the portal work, numbered from 0001. A reference to a decision of the mock generator says "mock decision".
- `journal.md`: one entry for each session of the portal work. Newest entry first.
- `sources/`: the official PDF of the exam guide and `compare-exam-guide.py`, which compares it with `reference/exam-guide.md` (decision 0027). Dated copies of documentation pages also go here (decision 0030).
- `sample/`: the sample pages of task statement 1.1 and the scripts that make them. Decision 0008 makes the fifth sample, `1-1-agentic-loops-kit.html`, the model for the look. `1-1-split-exam-guide.html` and `1-1-split-behind-the-mocks.html` are the fifth sample as two linked pages, as the portal will have them.

The MagnetLab brand kit is in `claude-code-brand-kit/` on the computer of the owner. It is not in the repository, because the repository will become public (decision 0003) and the kit has contact details and the designer files. `sample/make-1-1-kit.py` holds each kit color as a value, with the kit section that it comes from.

## What changed from the brief

Later decisions changed these points of `brief.md`. The brief stays as it is, because it is the record of the discussion of 12 October 2026.

| Line of the brief | What it says | Now | Decision |
|---|---|---|---|
| 12 | "CCA-F" | The pages use "CCAR-F", the exam code of the guide. | none (the guide) |
| 15, 19, 20 | 5 domain pages and 30 task statement pages | Two tabs, each one long page with closed parts. | 0010, 0021 |
| 21 | "Use the visual form of diagrams 09 and 10" | The look of the fifth sample, and four stages for each figure. | 0008, 0009, 0013 |
| 23, 24 | "Case study", one entry per task statement | "Behind the mocks", one entry per step and per part of the build in Claude Code. | 0001, 0010 |
| 26 | "the 26 document gaps" | The story of the three document checks. | 0031 |
| 29 | "written in the portal's code" | HTML prototypes in this folder that obey the security policy of the portal. The owner moves them. | 0010, 0017 |
| 31, 32 | An agent checks each page. The owner reads the flagged pages, plus 3 or 4 at random. | A fact agent and a review agent for each part, a whole-picture agent and a reader agent for each slice. The owner reads the flagged sentences, plus 3 or 4 at random. | 0011, 0012, 0015, 0026 |
| 36, 37 | No mock questions in downloads. Links to mock questions only after the mock. | Still post-MVP. The pages themselves can show a real mock question. | 0016 |
| 51 | Should the build guide go into the portal as it is? | No. Tab 2 is written for participants and replaces the page "How the Mocks Are Built New". The build guide stays as the record of the builder. | 0010, 0018 |
