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
| Prototype a simple traditional chatbot | Standalone `week3_traditional_chatbot/` package plus the portfolio rule-based mode | Unit tests and text-only verification record |
| Respond to multiple prompts and list capabilities | Week 3 intent rules and `What can you do?` response | Automated intent tests |
| Handle malformed or unsupported input | Blank, punctuation-only, overlong, and unknown-topic recovery messages | Automated boundary tests |
| Submit a 5-7 page APA report, project ZIP, and GitHub URL | Week 3 report, source archive, and repository link | Page/render review and ZIP content audit |
| Integrate an AI service and write a 5-7 page APA report | OpenAI Responses API adapter and report | Fake-client integration test; live call requires the user's key |
| Define and demonstrate an AI-based adaptive UI | Language, sentiment, urgency, and response-density adaptation | Unit tests, UI status panel, adaptive report |

## Boundaries and unresolved user-owned inputs

- The instructor's GitHub username was not supplied; no collaborator is invented.
- A live OpenAI key was not present; the app uses transparent offline demonstration mode until the user adds a key locally.
- Course and instructor details were supplied and applied consistently to all report title pages.
- R 4.6.1 was installed and the base-R exercise was executed successfully.
- The course handout presents Microsoft Bot Framework, Anaconda, Python 3.8.2, Visual Studio Code, and Bot Framework Emulator as an example path; it explicitly permits another framework. The Week 3 project uses Python 3.12 and Gradio.
- The handout requests screenshots, while the user's direct instruction requires text-only deliverables. Testing is documented with prose, automated results, and a text transcript.
