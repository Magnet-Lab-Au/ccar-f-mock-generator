# Intended takeaways of slice 1 (academy decision 0026)

The reader agent does not see this file. The assistant compares the one-sentence summary of the reader agent with these takeaways.

- **The top of tab 2:** the mock builder is a fixed sequence of 9 steps that code moves forward. It has one automatic loop (a failed question goes back to the writer), and every other way back waits for a decision of the owner.
- **Step 5, Try again:** a question that fails a check goes back to the writer with the failed try and the exact findings, and a pass, not the limit of 3 tries, stops the loop.
