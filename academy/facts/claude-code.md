# Fact sheet: tab 2, "The build in Claude Code" (the six entries of academy decision 0023)

- Fact agent: a new agent (academy decision 0012). Date: 14 October 2026.
- Repository state: commit `8ce49ec` (branch `main`, 2026-10-14 01:33:25 +1100). The working tree was clean before this file.
- Levels of trust (academy decisions 0011 and 0014): 1 = code, tests and run files (here also `git log`). 2 = decisions. 3 = build guide and diagrams. 4 = journal, lessons, reviews, `HANDOFF.md`, `docs/portal-notes.md`. D = Anthropic documentation (decision 0014, product facts only). R = the copy of the exam guide (`reference/task-statements-and-points.md`, `reference/guide-records.json`). "L" = level. "(computed)" = this agent ran a command that reads files.
- `CLAUDE.md` and `WORKING-RULES.md` are not named in the order of trust of decision 0011. This sheet treats them as level 2 (they hold rules that the owner confirmed). The reviewer can change that.
- A path such as `docs/decisions/0078-...md` means the one file in `docs/decisions/` whose name starts with `0078-`.
- The two copies of the exam guide agree for every point that this sheet cites. A script compared the 240 point texts of `reference/guide-records.json` with `reference/task-statements-and-points.md`: 0 real differences (4 IDs differ only by the backslash escapes of the Markdown file) (computed).
- Documentation pages (decision 0014), all read on 14 October 2026 as Markdown from `https://code.claude.com/docs/en/<page>.md`. Line numbers below are lines of those Markdown files on that day:
  - `memory` (https://code.claude.com/docs/en/memory)
  - `skills` (https://code.claude.com/docs/en/skills)
  - `sub-agents` (https://code.claude.com/docs/en/sub-agents)
  - `tools-reference` (https://code.claude.com/docs/en/tools-reference)
  - `permission-modes` (https://code.claude.com/docs/en/permission-modes)
  - `how-claude-code-works` (https://code.claude.com/docs/en/how-claude-code-works)
  - `sessions` (https://code.claude.com/docs/en/sessions)
  - `common-workflows` (https://code.claude.com/docs/en/common-workflows)
- Dated copies (decision 0030): this agent was allowed to write only this file, so it did NOT save the dated copies in `academy/sources/`. The assistant must save a dated copy of each page that the part uses before the page script takes an excerpt.
- Files that this agent did not read (working rules 19 and 28): `marking/*.xlsx`, `responses.json`, all personal files of the owner, `claude-code-brand-kit/`, conversation transcripts, and every file in `~/.claude/` except the two SKILL.md files of entry 4. For `~/.claude/CLAUDE.md` and `~/.claude/rules/` this agent tested only whether they exist. No model call. `src/run.py` was not run.

---

## Facts that apply to all six entries

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| G1 | Claude Code writes the program. The pipeline itself is a Python program that calls the API. It is not Claude Code. | `docs/decisions/0002-...md`, 15 | "A program is the pipeline. ... Claude Code writes and maintains the program." | 2 |
| G2 | Until 7 October 2026 the discussions ran in Cowork, not in Claude Code. | `HANDOFF.md`, 25-26 | "Cowork \| The Claude desktop product that the discussions ran in until 7 October 2026" / "Claude Code \| The Anthropic product that writes the program, from 7 October 2026 (decisions 0002 and 0038). It reads `CLAUDE.md` at the start of each session." | 4 |
| G3 | The first Claude Code session is the "second session" of 7 October. | `docs/journal.md`, 158-160 | "## 7 October 2026, second session" / "The first session in Claude Code." | 4 |
| G4 | So `HANDOFF.md`, `WORKING-RULES.md` (5 October) and the reviews of 5 and 6 October were made in Cowork, before Claude Code. | `docs/journal.md`, 381, 388; `docs/journal.md`, 225 | "Wrote `HANDOFF.md`, `WORKING-RULES.md` and `docs/lessons.md` for a new session." / "Decided: the work moves to Claude Code now." | 4 |
| G5 | 242 commits. 238 carry a `Claude-Session:` line, 240 a `Co-Authored-By: Claude` line. Only 2 different session URLs: `session_01TnghEw...` on 142 commits (7 to 12 October), `session_01UTkgDq...` on 96 commits (13 to 14 October). The 4 commits with no session line: the first two of 7 October, the marks of mock 2 round 1 (8 October), the brief from Cowork (12 October). | `git log` | e.g. `Claude-Session: https://claude.ai/code/session_01TnghEw2ou31QVRW6aTsXeq` | 1 (computed) |
| G6 | The repository has no `.claude/` folder: no `.claude/rules/`, no project skills, no `.claude/commands/`, no project settings. The only instruction file is the root `CLAUDE.md`. No `~/.claude/CLAUDE.md` and no `~/.claude/rules/` exist on this computer. | `ls -la`, `find . -name CLAUDE.md` | (no file) | 1 (computed) |

---

## Entry 1. CLAUDE.md, which imports WORKING-RULES.md (task statement 3.1)

### (a) The link to task statement 3.1

| Point | Exact text | Source | Shown by the build? |
|---|---|---|---|
| 3.1-K3 | "The @import syntax for referencing external files to keep CLAUDE.md modular (e.g., importing specific standards files relevant to each package)" | `reference/task-statements-and-points.md` 144; `reference/guide-records.json` 647 | Yes. `CLAUDE.md` line 9 is `@WORKING-RULES.md`. |
| 3.1-S2 | "Using @import to selectively include relevant standards files in each package's CLAUDE.md based on maintainer domain knowledge" | md 147; json 662 | In part. One import of one rules file. The repository has no packages, so "selectively ... in each package" is not shown. |
| 3.1-K1 | "The CLAUDE.md configuration hierarchy: user-level (~/.claude/CLAUDE.md), project-level (.claude/CLAUDE.md or root CLAUDE.md), and directory-level (subdirectory CLAUDE.md files)" | md 142; json 637 | In part. Only the project level (root `CLAUDE.md`) exists (G6). |
| 3.1-K2 | "That user-level settings apply only to that user—instructions in ~/.claude/CLAUDE.md are not shared with teammates via version control" | md 143; json 642 | In part. The rules are project-level and committed (git log of `CLAUDE.md`, `WORKING-RULES.md`). There are no teammates, and no user-level file. |
| 3.1-K4, 3.1-S3 | `.claude/rules/` | md 145, 148 | No. No `.claude/rules/` (G6). |
| 3.1-S1 | diagnosing hierarchy issues | md 146 | No record. |
| 3.1-S4 | "Using the /memory command to verify which memory files are loaded and diagnose inconsistent behavior across sessions" | md 149; json 672 | No record in the repository of `/memory`. |

Verdict: the link holds, on 3.1-K3 (fully) and 3.1-S2 (in part). It does not show the hierarchy (K1), `.claude/rules/` (K4, S3) or `/memory` (S4).

### (b) Facts

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| 1.1 | The whole `CLAUDE.md` is 22 lines: say to read `HANDOFF.md`, import the rules, two code rules, a 5-item end-of-session checklist. | `CLAUDE.md`, 5, 9, 13-14, 16-22 | "Read `HANDOFF.md` first. It says where the work stopped and what the next step is." / "@WORKING-RULES.md" / "Do not put an API key into a file of the repository." / "A test of the control makes no model call (decision 0038)." / "Before a session stops, check the record and show the owner the result:" | 2 |
| 1.2 | `WORKING-RULES.md` has 36 rules in three parts: A (the owner), B (suggested by the assistant, confirmed 6 October), C (changes after 6 October). | `WORKING-RULES.md`, 9, 45, 58, 66 | "## Part A. Rules that the owner gave" / "## Part B. Rules that the assistant suggested (the owner confirmed them on 6 October 2026)" / "## Part C. Changes after 6 October 2026" / "36. One night only, 14 October 2026, ..." | 2 |
| 1.3 | The rules file says how to change it: a later instruction wins, then record it in the file. | `WORKING-RULES.md`, 7 | "If a rule and a later instruction of the owner disagree, the later instruction is correct. Then record the change in this file." | 2 |
| 1.4 | When and why `CLAUDE.md` was made: on the move to Claude Code, after a check of the documentation. | `docs/journal.md`, 226-227 | "The assistant read the Anthropic documentation on 7 October 2026 (code.claude.com/docs/en/memory): Claude Code reads `CLAUDE.md` in the project folder at the start of each session, and that file can import other files with `@`. It does not read `HANDOFF.md` automatically. The product treats these files as context and does not enforce them." / "A new file, `CLAUDE.md`, imports `WORKING-RULES.md` and says to read `HANDOFF.md` first." | 4 |
| 1.5 | `README.md` describes `CLAUDE.md` the same way. | `README.md`, 21 | "The file that Claude Code reads at the start of each session. It imports `WORKING-RULES.md`." | 4 |
| 1.6 | `CLAUDE.md` changed only once after the first commits: item 5 of the checklist, on 8 October (commit `209898a`). `WORKING-RULES.md` changed in 7 commits (rules 31 to 36 were added). | `git log -- CLAUDE.md WORKING-RULES.md` | `209898a 2026-10-08 10:37:15 +1100 Mock 1, round 1: the blind marks of the owner, and the second review` (diff: `+5. A marking file that the owner filled is committed before anybody else reads it.`) | 1 (computed) |
| 1.7 | Rules 30 to 36 each came from an instruction of the owner in a session (examples). | `WORKING-RULES.md`, 62-63; `docs/journal.md`, 174, 194 | "32. Change of rules 8, 23 and 24 ... the owner wants fewer requests for a yes." / "The owner said that the assistant asks for a yes too often. A new rule 32 in `WORKING-RULES.md` says when the assistant acts without a yes." | 2 / 4 |
| 1.8 | Product: an import is expanded at launch; relative paths resolve from the importing file; at most four hops. | `memory`, 102, 104 | "CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them." / "Imported files can recursively import other files, with a maximum depth of four hops." | D |
| 1.9 | Product: CLAUDE.md is context, not enforcement. | `memory`, 24 | "Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a [PreToolUse hook](/docs/en/hooks-guide) instead." | D |
| 1.10 | Product: the scopes and who shares them. | `memory`, 60-61 | "**User instructions** \| `~/.claude/CLAUDE.md` \| Personal preferences for all projects \| ... \| Only you (all projects)" / "**Project instructions** \| `./CLAUDE.md` or `./.claude/CLAUDE.md` ... \| Team members via source control" | D |
| 1.11 | Product: the root CLAUDE.md survives `/compact`. (Relevant because one Claude Code session ran from 7 to 12 October, G5.) | `memory`, 625 | "Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session." | D |
| 1.12 | Product: `/memory` lists the loaded files. | `memory`, 566 | "The `/memory` command lists your CLAUDE.md, CLAUDE.local.md, and other memory file locations across user and project scopes" | D |
| 1.13 | Product: size advice. `CLAUDE.md` has 22 lines and `WORKING-RULES.md` 66 lines (`wc -l`), so each file is under the target. | `memory`, 88 | "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." | D / 1 (computed) |

### (c) Story

- Story A, the checklist line (8 October). The blind marking file of mock 1 was not in git. Only a SHA-256 fingerprint proved that it came back from the Cowork review unchanged. Then a new line went into `CLAUDE.md`. Sources: `docs/journal.md` 142-143, L4: "The blind file was not in git: only the empty file of the program was committed. The owner had sent the blind file to the Cowork session before the second review, and it came back from there unchanged: SHA-256 a30c0145..." / "A new line in the check at the end of a session in `CLAUDE.md`: a marking file that the owner filled is committed before anybody else reads it." Commit `209898a` (L1) holds the change. Later commits follow the rule: `51761c5 ... Mock 2: the marks of the owner, round 1 (SHA-256 e39069af...), committed before anybody read them`; `3fec57e ... Mock 4: the marks of the owner, round 1, committed before anybody read them` (git log, L1).
- Story B, a rule in context is not enforced (the product fact 1.9 in practice). Records of rule breaks after `CLAUDE.md` existed: `docs/journal.md` 165, L4: "The assistant showed a plan for the control before it read all files that `HANDOFF.md` names. The owner asked if it had read them. It had not." / `academy/journal.md` 84, L4: "The assistant first suggested `/loop`, without checking the documentation. The owner asked it to check." (rule 9). / `academy/journal.md` 40, L4: "The assistant first wrote the decisions into `docs/decisions/` of the mock generator. The owner corrected it: the portal work has its own folder." (this led to rule 34, `WORKING-RULES.md` 64).

### (d) Mechanism for one figure

Two files and one arrow: `CLAUDE.md` (22 lines) with line 9 `@WORKING-RULES.md` expanding into the 36 rules at launch, both in the context of every session. A second, small label: "context, not enforced" (memory, 24) with the checklist of lines 16-22 as the only "check" step, which the assistant runs and shows the owner.

### (e) Conflicts

- C1.1. `CLAUDE.md` lines 18-19 name `docs/journal.md` and `docs/decisions/`. For the portal work, rule 34 (`WORKING-RULES.md` 64) changes these to `academy/journal.md` and `academy/decisions/`. `CLAUDE.md` itself was not changed. The rules file is imported, so both texts reach the session. Not an error, but a page that quotes the checklist must say this.
- C1.2. Rule 9 (`WORKING-RULES.md` 24) names "docs.claude.com and support.claude.com". The Claude Code pages that the build read are on code.claude.com (`docs/journal.md` 226). Small.
- C1.3. The `CLAUDE.md` exists only from 7 October. The rules file is older (5 October, Cowork, G4). A page must not say that the rules were made "in Claude Code".

### (f) Not found

- No record that anybody ran `/memory` or `/context` to check the loaded files (3.1-S4).
- No record of a hierarchy problem (3.1-S1).

---

## Entry 2. HANDOFF.md, the journal and the decision files carry the work from one session to the next (task statement 1.7)

### (a) The link to task statement 1.7

| Point | Exact text | Source | Shown by the build? |
|---|---|---|---|
| 1.7-K4 | "Why starting a new session with a structured summary is more reliable than resuming with stale tool results" | md 72; json 355 | Yes. `HANDOFF.md` is a structured summary for a new session (fact 2.1). |
| 1.7-S3 | "Choosing between session resumption (when prior context is mostly valid) and starting fresh with injected summaries (when prior tool results are stale)" | md 75; json 370 | In part. The records show the "fresh with a summary" side. No record shows a choice between the two. The git trailers suggest that one session also continued over 6 days (G5, conflict C2.1). |
| 1.7-K3 | "The importance of informing the agent about changes to previously analyzed files when resuming sessions after code modifications" | md 71; json 350 | Weak. `HANDOFF.md` and the top journal entry give the new state, but not as "the files that changed". |
| 1.7-S4 | "Informing a resumed session about specific file changes for targeted re-analysis rather than requiring full re-exploration" | md 76; json 375 | Weak, as K3. |
| 1.7-K1, 1.7-S1 | `--resume <session-name>` | md 69, 73 | No record of `--resume` or session names in the repository. |
| 1.7-K2, 1.7-S2 | `fork_session` | md 70, 74 | No. |

Verdict: the link holds on 1.7-K4 (the structured summary for a new session). 1.7-S3 holds only in part. The named resumption and fork points are not shown. Note: mock decision 0001, which set up the decision files and the journal, cites 5.4-K2 and 5.4-K4, not 1.7 (`docs/decisions/0001-...md` 30: "5.4-K2, 5.4-K4, 5.6-K2"). 5.4-K2: "The role of scratchpad files for persisting key findings across context boundaries" (md 315; json 1362). That point fits the journal and the decision files at least as well as 1.7.

### (b) Facts

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| 2.1 | The purpose of `HANDOFF.md`. | `HANDOFF.md`, 1, 3 | "# Handoff: start here" / "This file gives a new session what it needs to continue." | 4 |
| 2.2 | Its structure: the academy work, words, the goal, the build guide, files to read in sequence, where we are, what a finished mock is, the next steps, open items, the old material, what the owner says to start. | `HANDOFF.md`, 5, 14, 32, 37, 47, 63, 100, 127, 156, 167, 178 | "## Read these files first, in this sequence" / "## Where we are" / "## The next steps" / "## Things that are open" | 4 |
| 2.3 | The start of each session is one sentence of the owner. | `HANDOFF.md`, 178-180 | "## What the owner says to start" / "\"Read `HANDOFF.md` in `ccar-f-mock-generator` and follow it.\"" | 4 |
| 2.4 | `CLAUDE.md` sends each session to `HANDOFF.md`, because the product does not read it alone. | `CLAUDE.md`, 5; `docs/journal.md`, 226 | "Read `HANDOFF.md` first." / "It does not read `HANDOFF.md` automatically." | 2 / 4 |
| 2.5 | The end-of-session checklist keeps the three records current. | `CLAUDE.md`, 16-20 | "1. `docs/journal.md` has an entry for this session." / "2. Each decision that the owner made in this session has its file in `docs/decisions/`." / "3. `HANDOFF.md` has the new state and the next step." | 2 |
| 2.6 | The rules for the records. | `WORKING-RULES.md`, 28, 30, 52, 53 | "10. Document the build during the work, so that nobody has to reconstruct it later." / "12. Record each decision on the day the owner makes it, as one file in `docs/decisions/`." / "25. Write one entry at the top of `docs/journal.md` for each session." / "26. Do not change a decision file after the owner has confirmed its text. Write a new file that names the old one." | 2 |
| 2.7 | The reason for the record system: the first build had to be reconstructed. | `docs/decisions/0001-...md`, 24 | "The record of the first build had to be reconstructed from files, and many decisions had no record that they ran." | 2 |
| 2.8 | Counts: 79 mock decisions (`docs/decisions/0001` to `0079`), 34 academy decisions, 14 entries in `docs/journal.md`, 2 entries in `academy/journal.md`. | `ls`, `grep -c "^## "` | (counts) | 1 (computed) |
| 2.9 | Each decision has a "How we decided" section, from 6 October. | `docs/journal.md`, 346 | "Each decision from 0003 to 0017 has a new section \"How we decided\", below the Reason." | 4 |
| 2.10 | The portal work has its own records, and `HANDOFF.md` points to them. | `HANDOFF.md`, 7, 9-10 | "This work has its own records in `academy/` (academy decision 0007)" / "Next step: build slice 1 (academy decision 0022): the top of tab 2 and step 5." | 4 |
| 2.11 | The night run keeps a progress list that is updated after each part. | `academy/journal.md`, 88 | "### Progress of the night (updated after each part)" | 4 |
| 2.12 | Product: a new session starts with no history. | `how-claude-code-works`, 99 | "**Sessions are independent.** Each new session starts with a fresh context window, without the conversation history from previous sessions." | D |
| 2.13 | Product: resume keeps the session ID; fork makes a new one. | `how-claude-code-works`, 111 | "Resuming a session with `claude --continue` or `claude --resume` reopens it under the same session ID and appends new messages to the existing conversation. Forking with `--fork-session` or `/branch` copies the history into a new session ID, leaving the original unchanged" | D |
| 2.14 | Product: resume from a summary loses what the summary leaves out. | `sessions`, 103, 107 | "**Resume from summary**: runs [`/compact`] immediately. Later requests carry the summary instead of the full history." / "whatever the summary leaves out is no longer in Claude's context." | D |

### (c) Story

- Story A, the handoff that was not read (7 October, the first Claude Code session). `docs/journal.md` 165, L4: "The assistant showed a plan for the control before it read all files that `HANDOFF.md` names. The owner asked if it had read them. It had not. It read them, and changed six points of the plan. The owner said yes to the plan." The summary existed, but it worked only when the session read it.
- Story B, "a new chat can take over" (12 October). `docs/journal.md` 5-8, L4: "The owner asked if a new chat can take over from the records. The assistant named the gaps: the check of the diagram popups was only in the temporary folder of the session, and the small practical lessons and the exact words of the discussions are not in the repository." / "The check of the popups is now in the repository: `docs/diagrams/check-popups.py` and `check-popups.js`". The next commits carry a new session URL (G5: the first commit of `session_01UTkgDq...` is `bd4a7bc 2026-10-13 00:09:21`). So the records were checked, and then a new session took over.
- Story C, the earlier version of the same lesson (5 October). `docs/journal.md` 387-388, L4: "Started a discussion of task statement 1.1 and stopped it." / "Wrote `HANDOFF.md`, `WORKING-RULES.md` and `docs/lessons.md` for a new session. Two independent reviewers checked the first version, and a third reviewer checked the second version." (In Cowork, G4.)

### (d) Mechanism for one figure

A row of sessions as boxes along a time line (5 Oct to 14 Oct). Between each pair of boxes, the three records (`HANDOFF.md` = the state and next step, the journal = what happened, the decision files = what was decided and why) are the only thing that passes. Inside a box, the context fills and is lost at the end. One arrow from `CLAUDE.md` "Read `HANDOFF.md` first" into each new box.

### (e) Conflicts

- C2.1 (important). The journal speaks of many sessions ("7 October 2026, second session", "8 October 2026, later session", three entries of 9 October). `HANDOFF.md` 28 defines "Session \| One chat with the assistant". But the git trailers name only one Claude Code session URL from 7 October 11:11 to 12 October 16:16 (142 commits), and one from 13 October 00:09 to now (96 commits) (G5, L1). The product keeps the same session ID on `--continue` and `--resume` (2.13, D). So probably the same Claude Code session was continued over several days, and the journal "sessions" are sittings. How the session continued (resume, or a session left open, with compaction) is not recorded. A page must not say that each journal entry was a new Claude Code session. Level 1 (git) is higher than level 4 (journal).
- C2.2. Mock decision 0001 links the record system to 5.4-K2 and 5.4-K4, academy decision 0023 links it to 1.7. Both can be shown. The page must not say that the build used `--resume` or `fork_session`.
- C2.3. `HANDOFF.md` 3 says "Updated on 9 October 2026, and on 13 October 2026", and 65 says "State on 9 October 2026". The academy state is from 13 October (line 9). It is not updated for the night of 14 October. Not wrong, but out of date for the night work.

### (f) Not found

- No record of `--resume`, `--continue`, `/resume`, session names, `/clear` or `/compact` in the repository (search of all `.md` files outside `reference/`, `data/`, `marking/`, `runs/`, `mocks/`).
- No record of how the 7-to-12 October session was continued.

---

## Entry 3. A new agent reviews each file. Story: the three document checks (task statement 4.6, not 1.3)

### (a) The link to task statement 4.6, and the check of 1.3-K2

| Point | Exact text | Source | Shown by the build? |
|---|---|---|---|
| 4.6-K1 | "Self-review limitations: a model retains reasoning context from generation, making it less likely to question its own decisions in the same session" | md 267; json 1164 | Yes, as the reason of rule 15: the reviewer "did not make the file". |
| 4.6-K2 | "Independent review instances (without prior reasoning context) are more effective at catching subtle issues than self-review instructions or extended thinking" | md 268; json 1169 | Yes. |
| 4.6-S1 | "Using a second independent Claude instance to review generated code without the generator's reasoning context" | md 270; json 1179 | Yes, also for code: two independent reviewers checked the control code (fact 3.6). |
| 4.6-K3 | "Multi-pass review: splitting large reviews into per-file local analysis passes plus cross-file integration passes to avoid attention dilution and contradictory findings" | md 269; json 1174 | Yes for the academy work: one review agent for each part (decision 0012) plus a whole-picture agent for each slice (decision 0015). NOT for the three document checks: each was one agent over all documents (fact 3.10). |
| 4.6-S2 | "Splitting large multi-file reviews into focused per-file passes for local issues plus separate integration passes for cross-file data flow analysis" | md 271; json 1184 | As 4.6-K3. |
| 4.6-S3 | "Running verification passes where the model self-reports confidence alongside each finding to enable calibrated review routing" | md 272; json 1189 | No. Reviews report severity ("high", "medium", "low"), not confidence (`academy/journal.md` 34). |
| 1.3-K2 | "That subagent context must be explicitly provided in the prompt—subagents do not automatically inherit parent context or share memory between invocations" | md 32; json 187 | In part (see below). |
| 1.3-K1 | "The Task tool as the mechanism for spawning subagents, and the requirement that allowedTools must include \"Task\" for a coordinator to invoke subagents" | md 31; json 182 | Not recorded. The product renamed the tool (conflict C3.3). |

Verdict: the link to 4.6 holds (K1, K2, S1 fully; K3 and S2 for the academy reviews only). Check of 1.3-K2: it holds in part. A Claude Code subagent does not get the conversation, so the prompt must carry the task (sub-agents 1066). But it is not "only the prompt": a non-fork subagent also loads every CLAUDE.md level and a git status snapshot (sub-agents 1068-1073), so the review agents of this build also get `CLAUDE.md` and `WORKING-RULES.md`. A fork inherits the full conversation (sub-agents 1196-1198), so a fork is not an independent reviewer. Decision 0023 chose 4.6, not 1.3. These facts support that choice. 1.3-K2 can be a secondary point.

### (b) Facts

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| 3.1 | The rule. | `WORKING-RULES.md`, 35-36 | "14. The owner does not trust the assistant to find everything. A check must not depend on the memory or the judgment of the assistant alone. Use a list or a script that shows each item." / "15. An independent reviewer checks each file that a new session or a participant will rely on, before the assistant says that the file is correct. The reviewer is a new agent that did not make the file." | 2 |
| 3.2 | The academy form: two new agents for each part, and the review agent gets no notes of the assistant. | `academy/decisions/0012-...md`, 14, 19, 27 | "Two new agents for each part. Both use the same model as the assistant, Opus 5.5." / "\| Review agent \| the finished part, the fact sheet, and the sources. It does not get the notes of the assistant. \| each sentence that the source does not support \|" / "The review agent gets no notes of the assistant, so it judges the part only against its sources." | 2 |
| 3.3 | Plus a whole-picture review after each slice. | `academy/decisions/0015-...md`, 15, 21-25 | "A whole-picture review after each slice." / "A new agent reads both tabs as they are so far ... It lists: one thing with two names / two parts that disagree / a part that does not follow the decisions / text that repeats another part" | 2 |
| 3.4 | The reason given in decision 0023. | `academy/decisions/0023-...md`, 28 | "4.6-S1 says: \"Using a second independent Claude instance to review generated code without the generator's reasoning context\". The part review (decision 0012) plus the whole-picture review (decision 0015) also match 4.6-K3: per-file passes plus cross-file integration passes. Task statement 1.3 is about the Task tool and the context that a coordinator passes." | 2 |
| 3.5 | The pipeline uses the same idea in step 4, without a subagent. (So 4.6 appears twice on tab 2.) | `docs/decisions/0012-...md`, 22, 26 | "It does not receive the notes or the reasoning of the writer. The call is not a subagent." / "\"a model retains reasoning context from generation, making it less likely to question its own decisions in the same session\" (4.6-K1)." | 2 |
| 3.6 | Independent review of code, in the first Claude Code session. | `docs/journal.md`, 170 | "Two independent reviewers checked the code, the tests and decision 0039. The first found 4 serious and 6 minor bugs. The second found 1 serious and 3 minor bugs in the fixes. ... For each fix, the assistant removed the fix in a copy of the code and saw a test fail. No reviewer checked the last round of fixes." | 4 |
| 3.7 | More code reviews with counts. | `docs/journal.md`, 181, 185, 188, 191 | "Step 1 is built ... An independent reviewer found 1 serious and 7 minor items" / "Steps 3 and 8 ... An independent reviewer found 4 serious and 6 minor items. ... Two were real faults" / "Step 7 ... An independent reviewer found 3 serious and 6 minor items." / "An independent reviewer found 3 serious items: call 4a had no guide text, the B6 search found names inside other words, and each API error was retried." | 4 |
| 3.8 | The written review reports state the independence. | `docs/reviews/review-decisions-0003-to-0018.md`, 2; `docs/reviews/review-decisions-0026-to-0036.md`, 4 | "Reviewer: one independent agent. It did not write the files and did not see the design discussion." / "Reviewers: two independent agents. They did not write the files. They worked at the same time and did not see the report of the other." | 4 |
| 3.9 | 37 lines of `docs/journal.md` and 11 lines of `academy/journal.md` name "independent" or "reviewer". 41 commit subjects contain "review". | `grep -c`, `git log` | (counts) | 1 / 4 (computed) |
| 3.10 | The academy slice 1 used all four agent kinds. | `academy/journal.md`, 76, 78, 79 | "Two fact agents wrote `facts/top-of-tab-2.md` (65 facts, 10 conflicts) and `facts/step-5.md` (83 facts, 7 conflicts)." / "A review agent for each part found 13 items in the top and 14 in step 5." / "The whole-picture agent (decision 0015) found 20 items and the reader agent (decision 0026) found terms used before they are explained." | 4 |
| 3.11 | Product: a subagent starts fresh and does not see the conversation. | `sub-agents`, 1066 | "Each subagent starts with a fresh, isolated context window. It doesn't see your conversation history, the skills you've already invoked, or the files Claude has already read. Claude composes a delegation message that summarizes the task, and the subagent works from there. The exception is a [fork], which inherits the parent conversation instead of starting fresh." | D |
| 3.12 | Product: but it loads CLAUDE.md and git status. | `sub-agents`, 1071-1073 | "**Task message**: the delegation prompt Claude writes when it hands off the work." / "**CLAUDE.md files**: every level of the [CLAUDE.md hierarchy] the main conversation loads ... The built-in Explore and Plan agents skip this." / "**Git status**: a snapshot Claude Code reads from your repository when the subagent starts." | D |
| 3.13 | Product: fork against non-fork. | `sub-agents`, 1192-1198 | "A fork inherits everything the main session has at the moment it spawns. Any other subagent starts fresh from its definition." / "\| Context \| Full conversation history \| Fresh context with the prompt you pass \|" | D |
| 3.14 | Product: the old name "Task tool". | `sub-agents`, 490 | "In version 2.1.63, the Task tool was renamed to Agent. Existing `Task(...)` references in settings and agent definitions still work as aliases." | D |

### (c) Story: the three document checks (academy decision 0031)

Sources: `docs/journal.md` 37-40 (L4), `docs/decisions/0078-...md` (L2), `git log --date=iso` (L1).

| Order | What happened | Count | Source, quote | L |
|---|---|---|---|---|
| 0 | Before the push, the owner asked for an independent check of all documents. | - | `0078`, 38: "The owner asked for an independent check of all documents before the push, by an agent that did not write them." | 2 |
| 1 | Check 1 found gaps. The assistant fixed diagrams, build guide sections, `HANDOFF.md`, `README.md`, the portal notes, and wrote decision 0078 (errors in confirmed decisions 0047, 0068, 0071). | no count in the journal | journal 37: "an independent agent checked all documents before the push. The assistant fixed the gaps: diagrams 01, 02, 04, 06, 07, 09, 11 and the diagrams README, the build guide sections of steps 2, 4, 5, 7 and 8 ... Decision 0078 records the errors in the confirmed decisions 0047, 0068 and 0071." / `0078`, 38: "The first agent found the errors in 0047, 0068 and 0071." | 4 / 2 |
| 1, commit | `edcd332 2026-10-09 22:43:15 +1100 The check of all documents: fixes of diagrams, build guide, handoff, README and portal notes; decision 0078` (32 files changed) | - | git | 1 |
| 1b, commit | `5244bf6 2026-10-09 22:47:19 +1100 The rule for the step 6 findings in diagram 08 and step 6; the build guide section of step 0` (9 files) | - | git; journal 38 names it: "Commit 5244bf6 added the rule for the step 6 findings to diagram 08" | 1 |
| 2 | Check 2, wider: also diagrams 03, 05, 08, 10 and build guide steps 0, 1, 3, 6. | 26 gaps | journal 38: "a second independent check of all documents, also diagrams 03, 05, 08 and 10 and the build guide sections of steps 0, 1, 3 and 6. ... The assistant then fixed the 26 gaps of the check" / `0078`, 38: "The second check found the others, except the error in 0045, which the assistant found." | 4 / 2 |
| 3 | Check 3, after these fixes. | 20 smaller gaps | journal 39: "a third independent check after these fixes found 20 smaller gaps. The assistant fixed them" / `0078`, 38: "A third check found that some status lines did not name this file." | 4 / 2 |
| 2+3, commit | `76779c6 2026-10-09 23:03:06 +1100 Second and third independent checks of all documents: fixes of diagrams, build guide, records; decision 0078 extended` (52 files changed; the file of 0078 renamed) | - | git | 1 |
| stop | Nobody reviewed the last 20 fixes. The owner stopped the checks. | - | journal 40: "No reviewer checked the 20 fixes after the third check. The owner stopped the document checks there." / commit `3992c49 2026-10-09 23:23:30 +1100 Journal: no reviewer checked the last 20 fixes; the owner stopped the document checks` | 4 / 1 |
| after | The second review in Cowork checked decisions 0073 to 0078. The owner confirmed them. The tag `mocks-v2` went on commit `aca8a23` (23:28:09). | - | journal 41-42; git `aca8a23 2026-10-09 23:28:09 +1100 Decisions 0073 to 0078: fixes of the owner and the second review, confirmed by the owner` | 4 / 1 |

The errors in confirmed decisions (mock decision 0078, table lines 23-30, L2): 0047, 0068 (two rows), 0071, 0061, 0059/0064/0069, 0046/0049/0051/0058, 0045. That is 8 rows and 12 different decisions (the same 12 that `HANDOFF.md` 68 lists). Rule 26 kept the confirmed texts. `0078` 34: "rule 26 keeps the confirmed texts. A reader must still find the correct facts, so this file names each error."

Time: all on 9 October 2026, from 22:43:15 (first fix commit) to 23:23:30 (stop), about 40 minutes of commits (computed from git). The start time of check 1 is not recorded.

### (d) Mechanism for one figure

Three rounds as three bars, each "an agent that did not write the files -> findings -> the assistant fixes -> commit": round 1 (no count, commit `edcd332`), round 2 (26, wider scope), round 3 (20 smaller), then "not reviewed, the owner stopped". A second, small figure for the academy form: per-part review agents (one per part) plus one whole-picture agent per slice (4.6-K3). A third option for 1.3-K2: what a non-fork subagent gets (the task prompt, CLAUDE.md, git status) and what it does not get (the conversation, the notes of the assistant).

### (e) Conflicts

- C3.1. Decision 0031 (line 23) says "Each round found fewer problems." Round 1 has no count (journal 37; decision 0031 line 19 says the same). So "fewer" is shown only from round 2 (26) to round 3 (20). Also round 2 had a wider scope than round 1 (journal 38 "also diagrams 03, 05, 08 and 10 and ..."). The page must not say that round 1 found more than 26.
- C3.2. Decision 0023 links the academy reviews to 4.6-K3 (per-part plus whole-picture). The three document checks were each one agent over "all documents" (journal 37-39), a single pass, not split. So the story of the three checks shows 4.6-K2 and 4.6-S1, not 4.6-K3. The page should not tie 4.6-K3 to this story.
- C3.3. The exam guide says "Task tool" (1.3-K1). The product renamed it "Agent" in v2.1.63 (sub-agents 490, D). Decision 0014: show both.
- C3.4. 1.3-K2 says context must be "explicitly provided in the prompt". In Claude Code a non-fork subagent also loads CLAUDE.md automatically (sub-agents 1072, D). Decision 0014: show both if the page uses 1.3-K2.
- C3.5. The reviews of 5 to 8 October were in Cowork (G4; `docs/reviews/M1-round1-second-review-notes.md` 4: "Who: an assistant in a Cowork session."). The "second review in Cowork" is a Claude model that the owner used in another product, not a Claude Code subagent. Only the reviews from 7 October that the journal calls "independent reviewer" or "independent agent" are in the Claude Code session (G5).

### (f) Not found

- The reports of the three document checks are not in `docs/reviews/` (list of that folder: 9 files, none for 9 October document checks).
- No record says which subagent type (general-purpose, a fork, a custom agent) the review agents were. No record of the exact prompts given to them.
- The 26 and 20 gaps are not listed one by one anywhere. Only the files that the fixes touched are in the journal and in the commits.

---

## Entry 4. Skills, such as ste-writing and discussion-and-brainstorming (task statement 3.2)

### (a) The link to task statement 3.2

| Point | Exact text | Source | Shown by the build? |
|---|---|---|---|
| 3.2-K2 | "Skills in .claude/skills/ with SKILL.md files that support frontmatter configuration including context: fork, allowed-tools, and argument-hint" | md 154; json 689 | In part. Both skills are SKILL.md files with frontmatter, but only `name` and `description`. No `context: fork`, no `allowed-tools`, no `argument-hint`. They are not in `.claude/skills/`. |
| 3.2-K4 | "Personal skill customization: creating personal variants in ~/.claude/skills/ with different names to avoid affecting teammates" | md 156; json 699 | In part. They are under `~/.claude/skills/synced/`, which the product fills from the claude.ai account (fact 4.6). They are not variants of a team skill. |
| 3.2-S5 | "Choosing between skills (on-demand invocation for task-specific workflows) and CLAUDE.md (always-loaded universal standards)" | md 161; json 724 | Yes, as a fact of the files: the same behaviors are in the skill and in `WORKING-RULES.md`, which `CLAUDE.md` loads always (fact 4.4). No record says that this was a deliberate choice. |
| 3.2-K1, 3.2-S1 | `.claude/commands/` | md 153, 157 | No. No `.claude/` folder (G6). |
| 3.2-K3, 3.2-S2 | `context: fork` | md 155, 158 | No. |
| 3.2-S3 | `allowed-tools` | md 159 | No. |
| 3.2-S4 | `argument-hint` | md 160 | No. |

Verdict: the link holds weakly. The two skills exist and are SKILL.md files, and their content is close to the always-loaded working rules (3.2-S5). No frontmatter option of 3.2 is used, and no record in the repository shows that either skill was invoked in the build. The repository records two other skill uses with real effect (facts 4.8 and 4.9). Those are stronger examples, but they are not the two skills that decision 0023 names.

### (b) Facts

Skill files (level: outside the repository, read with the permission of the brief; quoted only here):

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| 4.1 | Path of the two skills. Both files are dated 21 September 2026, before the project started (5 October). | `~/.claude/skills/synced/f4f0321f-..._edbd95ce-.../ste-writing/SKILL.md` and `.../discussion-and-brainstorming/SKILL.md`; `stat` | modification time `2026-09-21 10:50:19` | outside (computed) |
| 4.2 | The frontmatter of discussion-and-brainstorming: only name and description. | `discussion-and-brainstorming/SKILL.md`, 1-4 | `name: "discussion-and-brainstorming"` / `description: "The user's preferred style for open-ended discussion, brainstorming, thinking through decisions, weighing options, or working out an approach together. ..."` | outside |
| 4.3 | The frontmatter of ste-writing: only name and description. | `ste-writing/SKILL.md`, 1-4 | `name: ste-writing` / `description: Rewrite prose (docs, READMEs, PR descriptions, error messages, release notes, comments — never code) into ASD-STE100 Simplified Technical English ...` | outside |
| 4.4 | The same rules are in the skill and in `WORKING-RULES.md` (always loaded through the import). | `discussion-and-brainstorming/SKILL.md` 12, 14, 16, 18, 20, 22; `WORKING-RULES.md` 13-14, 18-19, 23-24 | Skill: "Lead with your recommendation, not a survey of the landscape." / "Raise one concern or decision at a time." / "Do not draft anything (documents, code, long text) until the user explicitly asks. Discussion comes first; drafting is a separate, later step." / "Push back honestly when the user is wrong." / "Do not reintroduce constraints or ideas the user has already dismissed." / "Verify anything current or product-specific before stating it, rather than relying on memory." — Rules: "1. Ask one question at a time. Give a short context, then one recommendation, then the question." / "2. ... Do not give a survey of options." / "6. Tell the owner when the owner is wrong, and say why." / "7. Do not suggest again an idea that the owner rejected." / "8. Discuss first. Do not write a document, a diagram or code before the owner asks for it." / "9. Check each fact about a product ... Do not rely on memory." | outside / 2 |
| 4.5 | ste-writing and rule 5. | `ste-writing/SKILL.md` 13, 20, 27, 30; `WORKING-RULES.md` 17 | Skill: "Use one name for one thing." / "Active voice." / "No contractions." / "No semicolons. Write two sentences." — Rule: "5. Write prose in Simplified Technical English: short sentences, active voice, simple words, no contractions, no semicolons, one name for one thing." | outside / 2 |
| 4.6 | Product: `~/.claude/skills/synced/` holds the skills of the claude.ai account. | `skills`, 239 | "In your terminal, Claude Code syncs those skills in sessions where you sign in with your claude.ai account. When the session starts, Claude Code downloads your account's skills into `~/.claude/skills/synced/` in the background" | D |
| 4.7 | Product: Cowork loads the account skills, but not `~/.claude/skills/` of the machine. So the same synced skills reach both products that this build used. | `skills`, 218 | "Cowork sessions and cloud sessions ... don't read `~/.claude/skills/` on your machine. Both interactive and scheduled Cowork sessions load the skills enabled for your claude.ai account, synced at session start" | D |
| 4.8 | Repository record of a skill in use: the Claude API skill, before the code of the model steps. | `docs/decisions/0040-...md`, 72; `src/model_call.py`, 45 | "The assistant read the skill of the Claude API before it wrote the code of the model steps. The skill said that the current models reject a forced tool call. Rule 9 asks for a check in the documentation, so the assistant read the page \"Define tools\"." / `# The errors that a new call can repair (the Claude API skill, shared/error-codes.md):` | 2 / 1 |
| 4.9 | Repository record of a plugin in use: visual-explainer, for the academy figures. | `academy/journal.md`, 23; `academy/decisions/0013-...md`, 10 | "The owner installed the plugin visual-explainer and asked for a second copy of the sample with it." / "How do we make sure that the figures and animations are the best that the plugin visual-explainer can make?" | 4 / 2 |
| 4.10 | Product: a skill body loads only when used; CLAUDE.md always. | `skills`, 11, 574 | "Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it." / "In a regular session, skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked." | D |
| 4.11 | Product: where skills live. | `skills`, 160-161 | "\| Personal \| `~/.claude/skills/<skill-name>/SKILL.md` \| All your projects on this machine, but not [Cowork or cloud sessions] \|" / "\| Project \| `.claude/skills/<skill-name>/SKILL.md` \| Sessions in this repository. Commit it so your team gets it too \|" | D |
| 4.12 | Product: custom commands are now skills. | `skills`, 16 | "**Custom commands have been merged into skills.** A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way." | D |
| 4.13 | Decision 0023 on the preview card. | `academy/decisions/0023-...md`, 20, 31 | "The preview card says that the skills are outside the repository." / "The skills are in the folder of the owner's user settings, not in the repository. So their preview card cannot link to the repository (decision 0005)." | 2 |

### (c) Story

No story for the two named skills: no record in the repository says when they were used or what went wrong. A story exists for the Claude API skill (fact 4.8): the skill said that the models reject a forced tool call, the assistant checked it in the documentation (rule 9), and this became mock decision 0040 (structured outputs). That story is already on tab 2 in step 2 (`academy/facts/step-2.md` 260 cites it).

### (d) Mechanism for one figure

Two loading paths side by side: the working rules, always in context (`CLAUDE.md` -> `@WORKING-RULES.md` -> every session), and a skill, where only the description is in context and the body loads on use (skills 574). The same rule ("one recommendation, then the question") appears in both, with the rule numbers and the skill lines (fact 4.4). This shows 3.2-S5.

### (e) Conflicts

- C4.1. Decision 0023 names ste-writing and discussion-and-brainstorming. The repository records no use of either. It records the Claude API skill and the visual-explainer plugin (4.8, 4.9). The owner decides which skills the entry names.
- C4.2. Decision 0023 line 31 says the skills are "in the folder of the owner's user settings". True, but more exact: they are synced from the claude.ai account into `~/.claude/skills/synced/` (4.6). A page that says "personal skills in `~/.claude/skills/`" (3.2-K4) must say "synced".
- C4.3. The exam guide (3.2-S3) describes `allowed-tools` as "to restrict tool access during skill execution". The documentation says: "Tools Claude can use without asking permission during the turn that invokes this skill." (`skills`, 407, D). Not used by the build, but decision 0014 applies if the page mentions it.
- C4.4. The skill text is outside the repository. Working rule 28 forbids copying text from the personal files of the owner into this folder. The two skills are not in the list of personal files of rule 19, and the brief of this agent allowed reading them. Whether the page may quote them is a question for the owner.

### (f) Not found

- No record of an invocation of ste-writing or discussion-and-brainstorming in any file of the repository or in a commit message.
- No project skill, no `.claude/commands/`.

---

## Entry 5. The built-in tools of Claude Code (task statement 2.5)

### (a) The link to task statement 2.5

| Point | Exact text | Source | Shown by the build? |
|---|---|---|---|
| 2.5-K1 | "Grep for content search (searching file contents for patterns like function names, error messages, or import statements)" | md 128; json 585 | Not as the Grep tool. On WSL the Grep tool is absent by default; Claude searches with `grep` through Bash (fact 5.3). |
| 2.5-K2 | "Glob for file path pattern matching (finding files by name or extension patterns)" | md 129; json 590 | Not as the Glob tool, same reason (`find` through Bash). |
| 2.5-K3 | "Read/Write for full file operations; Edit for targeted modifications using unique text matching" | md 130; json 595 | Probably yes, but no record in the repository names the tool of an edit. |
| 2.5-K4 | "When Edit fails due to non-unique text matches, using Read + Write as a fallback for reliable file modifications" | md 131; json 600 | No record. |
| 2.5-S1, S2 | selecting Grep, selecting Glob | md 132, 133 | Not as tools (as K1, K2). |
| 2.5-S3 | "Using Read to load full file contents followed by Write when Edit cannot find unique anchor text" | md 134; json 615 | No record. |
| 2.5-S4 | "Building codebase understanding incrementally: starting with Grep to find entry points, then using Read to follow imports and trace flows, rather than reading all files upfront" | md 135; json 620 | No record for this build. Counter-record: the sessions began by reading all files that `HANDOFF.md` names (`HANDOFF.md` 47, 52: "Read them completely."). |
| 2.5-S5 | tracing wrapper modules | md 136 | No record. |

Verdict: the link does NOT hold as written for the repository records. The build used built-in tools (every edit and every commit went through them), but no record in the repository says which tool did what, and on this platform (WSL) Grep and Glob are not in the default tool set. The only verifiable points are the product facts (Edit needs a unique match, Read before Edit). Decision 0002 already called 2.5 "a possible exception". A safe entry: "the build used the built-in tools, the records do not show the choices", plus the WSL fact as "Beyond the exam".

### (b) Facts

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| 5.1 | The folder is in WSL. | `docs/journal.md`, 163 | "The folder is in WSL at `~/ccar-f-mock-generator`. It is a git repository with a private remote on GitHub. The assistant checked this with `git` and `gh`." | 4 |
| 5.2 | Product: the default tools Read, Edit, Write, Bash, and Grep and Glob "absent by default" on macOS, Linux and WSL. | `tools-reference`, 24, 28, 34, 35, 43, 66 | "\| `Bash` \| Executes shell commands in your environment." / "\| `Edit` \| Makes targeted edits to specific files." / "\| `Glob` \| Finds files based on pattern matching. Absent by default on macOS, Linux, and WSL." / "\| `Grep` \| Searches for patterns in file contents. Absent by default on macOS, Linux, and WSL." / "\| `Read` \| Reads the contents of files." / "\| `Write` \| Creates or overwrites files." | D |
| 5.3 | Product: what Claude uses instead. | `tools-reference`, 304 | "On Windows, it's part of the default tool set. On macOS, Linux, and WSL, Claude Code leaves Glob and [Grep] out of the default tool set, and Claude searches with `find` and `grep` through the Bash tool instead. In Claude's shell those two commands run embedded versions of `bfs` and `ugrep`" | D |
| 5.4 | Product: Edit needs an exact, unique match. The documented fallback is a longer string or `replace_all`. | `tools-reference`, 250, 256 | "The Edit tool performs exact string replacement. ... It doesn't use regex or fuzzy matching." / "**Uniqueness**: `old_string` must appear exactly once. When it appears more than once, Claude either supplies a longer string with enough surrounding context to pin down one occurrence, or sets `replace_all: true` to replace them all." | D |
| 5.5 | Product: read before edit; a `cat` or `grep` through Bash counts as a read. | `tools-reference`, 254, 260 | "**Read-before-edit**: Claude reads the file in the current conversation before editing it" / "Claude can also edit a file without a separate Read after it views the file with a Bash command such as `cat` or `grep`." | D |
| 5.6 | Product: Write for whole files, Edit for parts. | `tools-reference`, 670, 682 | "The Write tool creates a new file or overwrites an existing one with the full content provided. It doesn't append or merge." / "For partial changes to an existing file, Claude uses Edit instead of Write." | D |
| 5.7 | Product: Read lists no folders. | `tools-reference`, 512 | "Read only reads files, not directories. Claude lists directory contents with a shell command such as `ls`." | D |
| 5.8 | Records of Bash use (commands named in the records): `git`, `gh`, scripts that a session ran, headless browser checks. | `docs/journal.md`, 163, 8; `academy/journal.md`, 21 | "The assistant checked this with `git` and `gh`." / "The check of the popups is now in the repository: `docs/diagrams/check-popups.py` and `check-popups.js`" / "A headless browser opened all 25 popups and cards at desktop and phone width." | 4 |
| 5.9 | "auto mode" was agreed to cover only tool permissions. | `docs/journal.md`, 172 | "The owner asked if \"auto mode\" also means no yes before a change. The assistant recommended that it covers only the tool permissions. The owner agreed." | 4 |
| 5.10 | The night run used `/goal`, auto mode and a git worktree (built-in features, not 2.5 tools). | `academy/night-plan.md`, 3, 37-39 | "The assistant works alone under `/goal`, in auto mode, in Claude Code 2.1.296." / "The fix lives in a separate worktree" / `git worktree add ../ccar-f-fix-owner-reason -b fix-owner-reason main` | 4 |
| 5.11 | Decision 0002 on 2.5. | `academy/decisions/0002-...md`, 19 | "A possible exception is task statement 2.5: the build in Claude Code uses the built-in tools of Claude Code." | 2 |
| 5.12 | The mocks test the exam form of 2.5 (Grep, Glob) as narrow ideas. | `docs/decisions/0066-...md`, 38-39; `docs/decisions/0072-...md`, 36 | "\| G037 \| Find text inside many files: Grep \|" / "\| G038 \| Find files by name or extension: Glob \|" / "\| G040 \| Grep for entry points, then Read to follow the flow \|" | 2 |

### (c) Story

No story. No record of a tool choice that went wrong, or of an Edit that failed on a non-unique match.

### (d) Mechanism for one figure

A table of the six tools of the task statement title (Read, Write, Edit, Bash, Grep, Glob): what the exam says each does (2.5-K1 to K3), and what this build's platform has (Grep and Glob absent on WSL; `grep` and `find` run through Bash; tools-reference 304). The Edit rule as a small picture: one `old_string`, two matches -> refused -> a longer `old_string` (tools-reference 256).

### (e) Conflicts

- C5.1. The exam guide treats Grep and Glob as tools to select (2.5-K1, K2, S1, S2). The documentation says they are absent by default on macOS, Linux and WSL (tools-reference 34-35, 304). Decision 0014: show both, and say which the exam uses.
- C5.2. The exam fallback for a non-unique Edit is "Read + Write" (2.5-K4, S3). The documentation names "a longer string" or `replace_all` (tools-reference 256). Show both.

### (f) Not found

- No record in the repository of which tool made which change. Commit messages name files, not tools.
- No record of Grep, Glob, an Edit failure or a Read + Write fallback in this build.

---

## Entry 6. "Discuss first", before any code (task statement 3.4: no example, unless the build used the Explore subagent)

### (a) The link to task statement 3.4

| Point | Exact text | Source | Shown by the build? |
|---|---|---|---|
| 3.4-K1 | "Plan mode is designed for complex tasks involving large-scale changes, multiple valid approaches, architectural decisions, and multi-file modifications" | md 174; json 773 | No. Plan mode was not used (fact 6.4). |
| 3.4-K3 | "Plan mode enables safe codebase exploration and design before committing to changes, preventing costly rework" | md 176; json 783 | The aim is the same as rule 8, but the means is a rule in context, not plan mode. |
| 3.4-K4 | "The Explore subagent for isolating verbose discovery output and returning summaries to preserve main conversation context" | md 177; json 788 | No record (fact 6.5). |
| 3.4-S3 | "Using the Explore subagent for verbose discovery phases to prevent context window exhaustion during multi-phase tasks" | md 180; json 803 | No record. |
| 3.4-S4 | "Combining plan mode for investigation with direct execution for implementation (e.g., planning a library migration, then executing the planned approach)" | md 181; json 808 | No plan mode. A close analogue: the night plan was a written plan file, reviewed by an independent agent, then executed (fact 6.8). |
| 3.4-K2, S2 | direct execution for simple changes | md 175, 179 | Not recorded as a choice. |

Verdict: decision 0023 holds. There is no example of 3.4: no record in the repository of plan mode or of the Explore subagent. The entry says that the build used a "discuss first" rule (rule 8) instead. Fact agents and review agents of the academy work are subagents that keep verbose reading out of the main conversation (the aim of 3.4-K4 and 5.4-K3), but no record says that the Explore type was used, and the fact agents write files, which Explore cannot do (fact 6.10).

### (b) Facts

| # | Fact | Source, lines | Exact quote | L |
|---|---|---|---|---|
| 6.1 | The rule. | `WORKING-RULES.md`, 23 | "8. Discuss first. Do not write a document, a diagram or code before the owner asks for it. Exception: the records are standing requests (rules 12, 13 and 25, and a change to this file). For those, show the text to the owner, then write the file." | 2 |
| 6.2 | Rule 30 makes the design of a pipeline step one full proposal. | `WORKING-RULES.md`, 60 | "for the design of a pipeline step, the assistant shows one proposal with all details of the step. The proposal names the exact file format and the exact fields. The owner accepts it or names what to change." | 2 |
| 6.3 | Rule 32 later relaxed rule 8 for small actions. | `WORKING-RULES.md`, 62 | "Change of rules 8, 23 and 24 ... The assistant still asks before: a new design decision, a change to a decision text that the owner confirmed, a push to GitHub, and an action that deletes work." | 2 |
| 6.4 | "Not plan mode" is recorded twice. | `docs/journal.md`, 320; `academy/decisions/0023-...md`, 22, 29 | "The owner confirmed the text of decision 0001, with one change: 3.4-K1 is not in the list of exam guide points, because the decision does not use plan mode." / "\"Discuss first\", before any code \| 3.4: no example. The entry says that the build used a \"discuss first\" rule, not plan mode." / "The build did not use plan mode, so 3.4 has no example." | 4 / 2 |
| 6.5 | Search for the Explore subagent and plan mode (this agent, 14 October): `grep -rniI "explore\b\|plan mode\|EnterPlanMode\|ExitPlanMode\|subagent_type"` over the repository, without `.git`, `marking/`, `runs/`, `mocks/`, `claude-code-brand-kit/`. Hits only in: the exam guide copies, mock questions and point groups about plan mode, academy decisions 0023 and the night plan (which ask for this check), `docs/journal.md` 320, and `reference/practice-audit-first-build.*` (the first build of August, not this build). No hit says that this build used plan mode or the Explore subagent. Commit messages: no hit for "explore" or "plan mode". | `grep`, `git log` | (search result) | 1 (computed) |
| 6.6 | Where the rule came from: on 5 October a discussion started from an assumption and was stopped. | `docs/journal.md`, 387; `docs/decisions/0001-...md`, 26 | "Started a discussion of task statement 1.1 and stopped it. The assistant had assumed a pipeline sequence that nobody had agreed on." / "That method made the assistant assume a pipeline that nobody had agreed on." | 4 / 2 |
| 6.7 | The design was in discussion and decision files before code: decisions 0001 to 0037 (5 to 6 October), then the first code on 7 October. | `docs/journal.md`, 312, 169; git `ed742b7 2026-10-07 11:11:12 +1100 Add the control with tests, decision 0039, and the new folder name` | "The folder is not a git repository." / "New code: `src/control.py`, `tests/fakes.py` and `tests/test_control.py`." | 4 / 1 |
| 6.8 | The night plan: a written plan, checked by an independent agent, accepted by the owner, then executed. | `academy/journal.md`, 85-86 | "The assistant wrote `academy/night-plan.md`. An independent agent checked it and found 20 items, 2 high" / "The owner accepted the night plan." | 4 |
| 6.9 | Product: what plan mode does, and that it blocks edits. | `permission-modes`, 266, 274 | "Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source. Except in interactive terminal sessions with [bypass permissions available], edits stay blocked until you approve the plan." / "Enter plan mode by pressing `Shift+Tab` or prefixing a single prompt with `/plan`." | D |
| 6.10 | Product: Explore is read-only and keeps results out of the main context. | `sub-agents`, 37, 47, 33 | "A fast, read-only agent optimized for searching and analyzing codebases." / "Claude delegates to Explore when it needs to search or understand a codebase without making changes. This keeps exploration results out of your main conversation context." / "Explore and Plan skip your CLAUDE.md files and the git status snapshot" | D |
| 6.11 | Product: CLAUDE.md is not enforcement (so rule 8 is a soft rule; plan mode is a hard block). | `memory`, 24 | "Claude treats them as context, not enforced configuration." | D |
| 6.12 | Why the build did not need plan mode (decision 0002 asks for this): the owner directs every step in discussion, and a decision file records the design before any change. One reason in the records: | `academy/decisions/0002-...md`, 23 | "The owner's reason: not all task statements fit the mock generator. A good engineer knows what to use and what not to use." | 2 |

### (c) Story

- Story A, the rule held off a premature design (5 October, Cowork, before Claude Code): fact 6.6.
- Story B, the soft rule was broken, and the owner stopped it (the reason a hard block like plan mode exists). `academy/journal.md` 41, L4: "The assistant moved to the build too soon once, and the owner stopped it." `academy/decisions/0010-...md` 85 (How we decided, item 5), L2: "The assistant moved to the build too soon. The owner stopped it: the outline was not finished." `docs/journal.md` 165, L4: "The assistant showed a plan for the control before it read all files that `HANDOFF.md` names." `docs/journal.md` 271, L4: "The assistant changed the new file of decision 0026 for the second answer before it told the owner. It told the owner after."

### (d) Mechanism for one figure

Two gates before an edit, side by side: (1) plan mode, a gate in the product: edits blocked until the plan is approved (permission-modes 266); (2) "discuss first", a gate in the context: a rule in `WORKING-RULES.md` that the model reads at launch but that the product does not enforce (memory 24), and that the owner enforced by stopping the assistant (story B). The build used gate 2.

### (e) Conflicts

- C6.1. Decision 0023 says the build "did not use plan mode". The records support it (fact 6.5), but no record proves the absence. A page should say "no record shows plan mode or the Explore subagent".
- C6.2. Rule 8 and the skill discussion-and-brainstorming have the same "discussion comes first" text (entry 4, fact 4.4). The page can link entries 4 and 6.

### (f) Not found

- No record of plan mode, `/plan`, `Shift+Tab`, `EnterPlanMode`, or the Explore or Plan subagents in this build.
- No record of the subagent type of the academy fact agents and review agents.
