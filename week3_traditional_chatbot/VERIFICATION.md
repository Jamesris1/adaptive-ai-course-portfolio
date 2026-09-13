# Week 3 Verification Record

## Automated checks

The automated suite verifies:

- case and punctuation normalization;
- the capabilities, assignment, setup, and testing intents;
- a consistent fallback for unknown topics;
- recovery from blank and punctuation-only input;
- rejection of messages longer than 500 characters; and
- repeatable output for the same input.

Verified on September 12, 2026: `python -m pytest -q` completed with 10 passed.

Runtime smoke check on September 12, 2026: the local server started on port 7867, returned HTTP 200, and served a page containing the project title.

## Text-only interaction record

**User:** What can you do?

**Bot:** I can explain my capabilities, course topics, assignment requirements, Python setup, GitHub steps, testing, and basic troubleshooting. Try 'What can you do?' or 'How do I test the chatbot?'

**User:** What is required for the assignment report?

**Bot:** The traditional chatbot assignment requires a working source project, a 5-7 page APA report, a ZIP archive, and the GitHub repository URL.

**User:** Tell me about gardening.

**Bot:** I do not have a rule for that topic. Ask 'What can you do?' to see the questions I can answer.

**User:** ?!...

**Bot:** I could not find any words in that input. Please enter a short question.

## Manual browser check

Before submission, confirm that Send and Enter both post a message, Clear removes the conversation, the examples populate the message box, and no model-service status or credential field appears.
