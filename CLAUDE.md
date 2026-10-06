# mock-builder-v3

A program that writes and checks mock exam questions for the CCAR-F exam.

Read `HANDOFF.md` first. It says where the work stopped and what the next step is.

The rules of the owner apply in each session:

@WORKING-RULES.md

Two more rules for code:

- Do not put an API key into a file of the repository.
- A test of the control makes no model call (decision 0038).

Before a session stops, check the record and show the owner the result:

1. `docs/journal.md` has an entry for this session.
2. Each decision that the owner made in this session has its file in `docs/decisions/`.
3. `HANDOFF.md` has the new state and the next step.
4. Each pipeline step that was built in this session has its build guide section and a correct diagram.
