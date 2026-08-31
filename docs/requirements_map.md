# Exercise Requirements Map

This file distinguishes the user's request from the attached instructional material and shows where each required deliverable is satisfied.

| Source requirement | Implemented deliverable | Verification |
|---|---|---|
| Create a private GitHub repository and initialize it | Private repository `jamesris1/adaptive-ai-course-portfolio` | `git status`, commit history, and remote branch check |
| Add a README and share with instructor | `README.md`; collaborator step in checklist | Instructor username is not present in the source files and must be supplied |
| GitHub report: 2-3 pages of APA-style content plus title and references | `docs/reports/GitHub_Repository_Exercise_Report.docx` | Page/render review |
| Create a development environment linked to GitHub | Python 3.12 `.venv`, requirements, Git configuration, private remote | Environment validation and tests |
| Create a simple Hello World application | `hello_world.py` | Direct execution |
| Document implementation and results | Written reports plus reproducible Python/R scripts | Reports discuss the workflow; scripts regenerate analytical output |
| Include a source-code ZIP | `submission/adaptive-ai-course-portfolio-source.zip` | ZIP content audit |
| Create graphs in Python and R | `scripts/run_analysis.py`, notebook, and `r/data_science_exercises.R` | Python run; R run when the R runtime is available |
| Create a program more complex than a temperature conversion | Study-plan recommender in Python and R | Automated Python test and output summaries |
| Prototype a simple traditional chatbot | Rule-based mode in `traditional.py` and Gradio UI | Unit test and browser test |
| Integrate an AI service and write a 5-7 page APA report | OpenAI Responses API adapter and report | Fake-client integration test; live call requires the user's key |
| Define and demonstrate an AI-based adaptive UI | Language, sentiment, urgency, and response-density adaptation | Unit tests, UI status panel, adaptive report |

## Boundaries and unresolved user-owned inputs

- The instructor's GitHub username was not supplied; no collaborator is invented.
- A live OpenAI key was not present; the app uses transparent offline demonstration mode until the user adds a key locally.
- Course and instructor details were supplied and applied consistently to all report title pages.
- R 4.6.1 was installed and the base-R exercise was executed successfully.
