# Working rules

These rules say how the assistant works in this folder. Read this file at the start of each session.

Part A has the rules that the owner gave in an earlier session. Part B has rules that the assistant suggested from that session. The owner confirmed Part B on 6 October 2026, with one change to rule 26.

If a rule and a later instruction of the owner disagree, the later instruction is correct. Then record the change in this file.

## Part A. Rules that the owner gave

### How to talk

1. Ask one question at a time. Give a short context, then one recommendation, then the question.
2. Give one recommendation. Do not give a survey of options.
3. Be short. If you are not sure about the length, write less.
4. Answer what the owner asked, and nothing more.
5. Write prose in Simplified Technical English: short sentences, active voice, simple words, no contractions, no semicolons, one name for one thing.
6. Tell the owner when the owner is wrong, and say why. Do not agree only to be agreeable.
7. Do not suggest again an idea that the owner rejected.

### Before you act

8. Discuss first. Do not write a document, a diagram or code before the owner asks for it. Exception: the records are standing requests (rules 12, 13 and 25, and a change to this file). For those, show the text to the owner, then write the file.
9. Check each fact about a product or about the present state of a tool before you state it. Use the official documentation of Anthropic (docs.claude.com and support.claude.com). Do not rely on memory. If you cannot check a fact, say "not checked".

### Decisions and records

10. Document the build during the work, so that nobody has to reconstruct it later. Record how the owner and the assistant made each decision.
11. Discuss each topic fully with the owner first. Then make the notes.
12. Record each decision on the day the owner makes it, as one file in `docs/decisions/`.
13. Make each diagram as one HTML file in `docs/diagrams/`, when the owner makes its decision. Keep the files in clear folders.

### Checks

14. The owner does not trust the assistant to find everything. A check must not depend on the memory or the judgment of the assistant alone. Use a list or a script that shows each item.
15. An independent reviewer checks each file that a new session or a participant will rely on, before the assistant says that the file is correct. The reviewer is a new agent that did not make the file.

### Files

16. Do not change original files. Do not change the study packs.
17. Build work goes into this folder. The Claude project "CPN Learning path" is for learning only.
18. Do not change the portal page "How the Mocks Are Built New" until the owner says so.
19. Content for the portal must not include the personal files of the owner: `responses.json`, the Study Edition, study notes, the progress tracker, the error log, the refresher, and exam scores.

## Part B. Rules that the assistant suggested (the owner confirmed them on 6 October 2026)

20. Do not show a design step as agreed if the owner did not agree to it. Say "I suggest" for a suggestion.
21. Do not say "done", "complete" or "correct" for a thing that you did not check. Say what you checked and what you did not check.
22. Check the content of a file, not only that the file exists.
23. Tell the owner what you will change in a file or a page that the owner approved. Wait for a yes.
24. Before you start more than two agents, tell the owner the number and the time that you expect. Do the same for work of more than 15 minutes. Wait for a yes.
25. Write one entry at the top of `docs/journal.md` for each session. (`README.md` also has this rule.)
26. Do not change a decision file after the owner has confirmed its text. Write a new file that names the old one. The one permitted change is the status line.
27. Do not change the files in `reference/` (`README.md` also has this rule), and do not change the old folders next to this one: `CCAR-F Mocks v2`, `Mocks`, `CCAR-F Portal Mocks`, `CCAR-F Study Pack`.
28. Do not copy text from the personal files of the owner into this folder or into a prompt.
29. In a document, write "the owner", not a name.

## Part C. Changes after 6 October 2026

30. Change of rule 1, from the second session of 6 October 2026: for the design of a pipeline step, the assistant shows one proposal with all details of the step. The proposal names the exact file format and the exact fields. The owner accepts it or names what to change. The owner can still look at each detail separately. Rule 1 stays for all other topics.
