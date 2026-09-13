# Final Submission Checklist

## Personal and course details

- [x] Confirm `MSAI-631-A02: Artificial Intelligence for Human-Computer Interaction` appears in every report.
- [x] Confirm instructor `Alan Dennis` appears in every report.
- [ ] Confirm the author name is exactly as it should appear in the classroom.

## GitHub

- [x] Sign in to GitHub as `jamesris1`.
- [x] Confirm `adaptive-ai-course-portfolio` is private.
- [x] Push the verified `main` branch.
- [ ] In Settings > Collaborators, invite the exact instructor username from the course announcement.
- [ ] Confirm the invitation is shown as pending or accepted.
- [ ] Confirm the private repository and collaborator status directly in GitHub.

## Application and evidence

- [ ] Add `OPENAI_API_KEY` only to a local `.env`; never put it in a report, commit, or ZIP.
- [x] Run `python -m pytest -q` and confirm all tests pass.
- [ ] Run `python scripts/run_analysis.py` and inspect the Python graph.
- [ ] Run `Rscript r/data_science_exercises.R` after installing R and inspect the R graph.
- [ ] Run `python app.py` and manually test all three chatbot modes.
- [ ] With a key configured, manually verify one live OpenAI response and confirm no private data is visible.

## Reports and packaging

- [x] Open `week3_traditional_chatbot/` and confirm the bot is entirely rule-based.
- [x] Run the Week 3 automated tests.
- [ ] Complete the manual browser interactions in `VERIFICATION.md`.
- [x] Confirm the Week 3 ZIP contains source and documentation but no environment, cache, secret, screenshot, or image files.
- [ ] Configure the student's Azure AI Language F0 resource locally.
- [ ] Record one positive, negative, and neutral live Azure result without exposing the key.
- [ ] Complete the Azure chatbot manual browser checks.
- [ ] Confirm the Azure ZIP excludes `.env`, credentials, caches, screenshots, and images.
- [ ] Read every report in full and make the first-person narrative accurately yours.
- [ ] Confirm APA title pages, page numbers, double spacing, in-text citations, and references.
- [ ] Inspect the ZIP and confirm it excludes `.env`, `.venv`, `.git`, caches, and secrets.
- [ ] Submit the required report, repository URL, and source ZIP for each assignment.
