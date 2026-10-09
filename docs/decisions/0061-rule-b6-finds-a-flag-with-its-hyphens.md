# 0061: Rule B6 finds a flag with its hyphens

- Date: 8 October 2026
- Status: accepted. Decision 0078 corrects one line of this file.
- Text confirmed by the owner: 9 October 2026
- Diagram: none. Diagram 06 shows rule B6, and its text does not change.

## Question

Decision 0041, item 2, says that rule B6 "never finds a name of one character", and that code treats a hyphen as a space. The guide names the flag "-p": "The -p (or --print) flag for running Claude Code in non-interactive mode in automated pipelines" (3.6-K1). Code removed the hyphen and searched "p", so a question that used "-p" always failed B6. In mock 3, slot M3-S48 failed two of its three tries for this reason only. How does B6 treat a flag?

## Options

1. Code searches a name that starts with "-" with its hyphens, as a complete flag.
2. No change. The writer must not use "-p".

## Decision

Option 1. A name like "-p", "--print" or "--json-schema" is searched with its hyphens, as a complete flag, in the text of the records file. Capital letters do not count. A flag that the guide does not name, for example "-x", is still not named. Each other name keeps the rules of decision 0041.

## Reason

Plain reason: B6 must pass a feature that the guide names, and fail one that it does not. "-p" is named in the guide, so a fail is wrong. Decision 0041 made the one-character rule to stop false finds inside other words. A flag with its hyphen cannot match inside a word.

A test checks "-p", "--print", "--json-schema", "--output-format" and "--resume" (named), and "-x", "-r", "p" and "--printx" (not named).

## How we decided

The assistant found the fault in the open slot M3-S48 and suggested option 1. The owner said yes.

The owner confirmed the text of this file on 9 October 2026. No independent reviewer checked this file.

## Exam guide points

none
