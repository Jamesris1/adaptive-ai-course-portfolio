# Final Submission Checklist

## Personal and course details

- [ ] Replace `[Course Number and Name]` in every report.
- [ ] Replace `[Instructor Name]` in every report.
- [ ] Confirm the author name is exactly as it should appear in the classroom.

## GitHub

- [ ] Sign in to GitHub as `jamesris1`.
- [ ] Confirm `adaptive-llm-course-portfolio` is private.
- [ ] Push the verified `main` branch.
- [ ] In Settings > Collaborators, invite the exact instructor username from the course announcement.
- [ ] Confirm the invitation is shown as pending or accepted.
- [ ] Capture the private repository and collaborator-status screenshots; avoid exposing email addresses or tokens.

## Application and evidence

- [ ] Add `OPENAI_API_KEY` only to a local `.env`; never put it in a report, screenshot, commit, or ZIP.
- [ ] Run `python -m pytest -q` and confirm all tests pass.
- [ ] Run `python scripts/run_analysis.py` and inspect the Python graph.
- [ ] Run `Rscript r/data_science_exercises.R` after installing R and inspect the R graph.
- [ ] Run `python app.py` and manually test all three chatbot modes.
- [ ] With a key configured, capture one live OpenAI response and confirm no private data is visible.

## Reports and packaging

- [ ] Read every report in full and make the first-person narrative accurately yours.
- [ ] Confirm every figure is legible, named, and referenced in the surrounding narrative.
- [ ] Confirm APA title pages, page numbers, double spacing, in-text citations, and references.
- [ ] Inspect the ZIP and confirm it excludes `.env`, `.venv`, `.git`, caches, and secrets.
- [ ] Submit the required report, repository URL, and source ZIP for each assignment.

