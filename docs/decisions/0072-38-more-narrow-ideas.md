# 0072: 38 more narrow ideas

- Date: 9 October 2026
- Status: accepted
- Text confirmed by the owner: 9 October 2026
- Diagram: `docs/diagrams/11-repeats-across-mocks.html` shows the narrow ideas.

## Question

Before mock 5, the owner asked for a check of all 95 point groups against the guide text: each group where one point gives both the scene and the answer, as for G041 (decision 0068). An independent agent found 38 more groups that are narrow (sure) and 11 that are a judgment call. Which groups join the narrow list?

## Options

1. The 38 sure groups join the list. The 11 judgment calls keep the stricter rule B9.
2. All 49 join the list.
3. No change.

## Decision

Option 1. The list `data/narrow-ideas.json` now has 62 of the 95 groups. These join it:

| Group | Idea |
|---|---|
| G004 | Hub and spoke: all routing through the coordinator |
| G005 | Subagents get no parent context: pass it in the prompt |
| G006 | Coordinator selects subagents by the query |
| G007 | Too narrow decomposition leaves gaps in coverage |
| G008 | Partition the scope so subagents do not duplicate work |
| G017 | Structured handoff summary to a human |
| G018 | Split a multi-concern request into items |
| G019 | PostToolUse hook normalizes data formats |
| G020 | Per-file passes plus a cross-file integration pass |
| G022 | Tell a resumed session which files changed |
| G025 | Keywords in the system prompt override tool descriptions |
| G035 | MCP resources expose content catalogs |
| G040 | Grep for entry points, then Read to follow the flow |
| G043 | User-level CLAUDE.md is not shared with the team |
| G045 | Split a large CLAUDE.md into .claude/rules/ files |
| G050 | Personal skill variants with other names |
| G056 | Plan mode first, then direct execution |
| G058 | Tests first, then share the failures |
| G063 | CLAUDE.md gives CI the testing standards |
| G064 | Independent review instance, not self-review |
| G065 | Give prior findings, report only new issues |
| G066 | Give existing tests to avoid duplicate tests |
| G068 | False positives lose trust: disable the noisy category |
| G069 | Severity criteria with code examples |
| G070 | Tool use with a JSON schema for structured output |
| G073 | Format normalization rules in the prompt |
| G075 | detected_pattern field to analyze dismissals |
| G079 | Batch frequency from the SLA |
| G080 | Refine the prompt on a sample before the batch |
| G082 | Case facts block outside the summarized history |
| G087 | Several matches: ask for more identifiers |
| G088 | Coverage annotations for gaps in the synthesis |
| G089 | Scratchpad files against context degradation |
| G090 | Crash recovery with state manifests |
| G091 | Summarize one phase before the next subagents |
| G092 | Aggregate accuracy hides weak segments |
| G093 | Stratified random sampling of high-confidence output |
| G095 | Each content type in its own format |

The 11 judgment calls keep the stricter rule B9 of decision 0066: G009, G013, G015, G016, G029, G036, G054, G055, G067, G085 and G094.

The agent also doubted 3 groups that are on the list (G060, and weaker G074 and G039). They stay on the list.

**What this means for the mocks.** For a narrow idea, only a copy of an earlier question fails rule B9. So mocks 4 and 5 often test the same problem as mocks 1 to 3, in a new setting. The build guide says this plainly to the participants.

## Reason

Plain reason: in mock 4, the stricter rule failed again and again on ideas with almost only one problem (decision 0068). For such an idea, a new question can change the setting, but not the problem. The 11 judgment calls allow some different problems, so the stricter rule stays for them.

## How we decided

The owner asked for the check. An independent agent made it. The owner decided: "Add the 38 narrow groups to the narrow list in a new decision. Keep the 11 judgment calls strict."

The owner confirmed the text of this file on 9 October 2026. The second review in Cowork checked it. No independent reviewer of Claude Code checked this file.

## Exam guide points

none
