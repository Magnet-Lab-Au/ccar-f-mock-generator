# Intended takeaways of slice 2 (academy decision 0026)

The reader agent does not see this file. The assistant compares the one-sentence summary of the reader agent with these takeaways.

- **Step 0, Prepare the guide records:** a script, not a model, copies the exam guide into one checked file of records once, and every later step takes its guide text from that file by ID.
- **Step 1, Plan the mock:** code fixes all 60 slots of a mock before any question is written, so the counts always hold, and it spreads the ideas so that two slots do not share one idea.
- **Step 2, Write the question:** one new Claude call writes each question from a request that code builds, and code, not the model, gives the letters.
- **Step 3, Check by code:** code checks 12 exact rules before a model checks the question, because a model instruction or a form cannot guarantee a count.
- **Step 4, Check by a model:** a blind answer and a rule check, in two separate calls, find what needs judgment, and code makes the verdict.
- **Step 6, Check the complete mock:** two calls read the questions of a scenario together to find problems of the set, and the owner decides each finding.
- **Step 7, The questions are marked:** a reader marks the questions with no verdict in view, to show whether the checks were right.
- **Step 8, Build the files:** code builds the mock files from the records only after the owner accepts, so the files are always the questions that passed the checks.
