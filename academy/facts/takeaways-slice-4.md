# Intended takeaways of slice 4 (academy decision 0026)

The reader agent does not see this file. The assistant compares the one-sentence summary of the reader agent with these takeaways.

- **The map:** the exam guide has 5 domains with weights and 30 task statements, and an exam draws 4 of its 6 scenarios.
- **How we broke it down:** each task statement has Knowledge of (K) and Skills in (S) points, with our labels such as 1.1-K2, and opens in three levels.
- **1.1:** the agentic loop continues while stop_reason is "tool_use" and stops on "end_turn", not on text, words or a count.
- **1.2:** a coordinator splits the work, chooses the subagents, and routes all results, and a split that is too narrow leaves gaps.
- **1.3:** a subagent sees none of the conversation of the coordinator, so the prompt of the Task call must hold the complete findings and their sources.
- **1.4:** when an order of steps must hold, code blocks the later tool call, because a prompt instruction can fail, and an escalation gives the human a structured summary.
- **1.5:** a PreToolUse hook can block a call and a PostToolUse hook can replace its result, so code, not the model, enforces a rule and cleans the data.
- **1.6:** a fixed chain of passes suits work whose steps are known, and an adaptive plan suits open work.
- **1.7:** resume a session when its context is mostly valid, fork it to compare approaches, and start fresh with a summary when the tool results are stale.
