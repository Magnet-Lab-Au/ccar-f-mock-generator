# 0002: The build is a program that uses the Claude API and the Agent SDK

- Date: 5 October 2026
- Status: accepted
- Diagram: none

## Question

What runs the build?

## Options

1. A chat session (Cowork) that starts subagents. The first build used this.
2. Claude Code is the pipeline: it runs each generator and each checker as a subagent.
3. A program is the pipeline. It calls the Claude API for a step that is one request with a fixed output format. It uses the Agent SDK for a step in which the model works in a loop with tools, for example to read files. Claude Code writes and maintains the program.

## Decision

Option 3. The program is a Python program in this repository. A person starts it from the command line. Its output is files. It has no screens, and it is not a part of the portal.

## Reason

The exam guide says that prompt instructions have a non-zero failure rate, and that code must enforce a rule that must always hold (1.4). It says that tool use with a JSON schema is the most reliable method for output in a fixed format (4.3). In the first build, a chat session held the sequence of steps, and the prompts and the code were lost with the session.

The two scenarios of the guide that are nearest to this work are the multi-agent research system (Agent SDK) and structured data extraction (JSON schemas). The guide uses Claude Code to write code and to review in CI, not as a production pipeline.

Not decided yet: which steps the pipeline has, and which steps need the Agent SDK.

## Exam guide points

1.4-K1, 1.4-K2, 1.1-K3, 4.3-K1
