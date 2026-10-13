# Journal of the portal work

One entry for each work session. Newest entry first.

## 12 and 13 October 2026, the start of the MVP discussion

- The owner gave the MVP brief from the Cowork discussion. It is `brief.md`.
- The open question of the brief: can the build guide go into the portal as it is? The assistant read step 4, then all 9 step files and the 12 diagrams. The answer: the step files speak to the builder, not to participants. The diagrams are a good base, but they have layout defects, and diagram 11 shows three real questions of mocks 1 and 2 with the correct option. The tables of guide points in the build guide use only 12 of the 30 task statements, and none of domains 2 and 3.
- The owner described the audience: senior engineers, directors of engineering and senior product managers, with little time. The cohort has 10 to 15 people. The portal must hook them, use many visuals, give depth step by step, and show no code in the text. It also shows the technical competence of the owner to the reader who goes deep.
- Decisions 0001 to 0007:
  - 0001: the section names "Exam guide breakdown" and "Behind the mocks"
  - 0002: two sources for "Behind the mocks"
  - 0003: the public repository with the mock answers
  - 0004: three levels on each page
  - 0005: a preview card for the source of each fact
  - 0006: the label "Beyond the exam"
  - 0007: this separate folder
- An independent agent checked the seven decisions. It found 10 items: a fourth place with the mock answers (the step 4 check files), three questions in diagram 11 and not two, 15 minutes and not one hour for the 30 overviews, and some passive sentences. The assistant checked the items and fixed them.
- The owner confirmed the texts of 0001 to 0007. For 0002 the owner first corrected the reason: the build used only the task statements that it needed, and a good engineer knows what to use and what not to use. So an entry with no example says why the build did not need it.
- The owner asked for a sample page of task statement 1.1. The script `sample/make-1-1.py` makes `sample/1-1-agentic-loops.html`. It takes each guide text from the guide records and each excerpt of a preview card from its source file. The loop is animated. The code of the loop follows the Anthropic page "Tool use with Claude", read on 13 October 2026.
- An independent agent checked the page against the guide and the repository and found 12 items. Examples: sentences in the popups that said more than the guide, the domain weight that the guide calls approximate, and 9 rewrites of the owner that the count of tries of mock 1 included. The assistant checked them and fixed all 12. A headless browser opened all 25 popups and cards at desktop and phone width.
- The owner removed the label of the Depth boxes, and asked if the two sections are on one page in the portal. The answer: only in the sample. In the portal they are separate pages, linked both ways. The sample stays as one page for now.
- The owner installed the plugin visual-explainer and asked for a second copy of the sample with it. The script `sample/make-1-1-ve.py` makes `sample/1-1-agentic-loops-ve.html` in the "Paper" register of the plugin. It runs the data part of `make-1-1.py`, so the checked text, the popups and the cards are the same. New are the figures: a stepper for the loop, small multiples for the anti-patterns, bars for the domain weights, the stop reasons of the API, a grid of the 60 slots of mock 1 and the review cycle. A headless browser opened all 25 popups and cards at 1280 and 390 pixels wide, with no sideways overflow. The first sample did not change.
- The owner compared the two samples and chose the second one. The owner asked if the colors and the looks can change later. The assistant checked the script: all colors and fonts are variables in three blocks, and the figures use them. Decision 0008 records the choice. Its text is not yet confirmed.
- The owner never liked Play in the stepper of Fig. 1: some steps showed several new parts at the same time. The assistant removed Play and the slider. The loop now has 9 steps. Each step lights one event and adds at most one line to the conversation history. The figure still opens on the full picture. A headless browser went through all 9 steps and opened all 25 popups and cards at 1280 and 390 pixels wide.
- The assistant first wrote the decisions into `docs/decisions/` of the mock generator. The owner corrected it: the portal work has its own folder.
