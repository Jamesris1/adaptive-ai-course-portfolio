# Adaptive LLM Course Portfolio

This repository contains the complete source package for the GitHub, development-environment, chatbot, OpenAI integration, and adaptive-interface exercises. It is designed for the GitHub account **jamesris1** and keeps credentials outside source control.

## What is included

- A reproducible Python 3.12 virtual environment.
- A small Hello World smoke test.
- Python and R data-science exercises with customized graphs and a study-planning program.
- A traditional rule-based chatbot.
- An OpenAI chatbot using the Responses API.
- An adaptive mode that detects language, sentiment, urgency, and preferred response density, then changes its interaction style.
- Automated tests, screenshots, assignment reports, and submission packaging instructions.

## Quick start on Windows

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python hello_world.py
python scripts/run_analysis.py
python app.py
```

Open `http://127.0.0.1:7860` after the final command.

## OpenAI configuration

Set `OPENAI_API_KEY` in a local `.env` file or in the process environment. The application reads the model name from `OPENAI_MODEL`; the example defaults to `gpt-5`. When no key is present, the application stays usable in a clearly labeled offline demonstration mode. The repository never contains a real key.

## Run tests

```powershell
python -m pytest -q
```

The OpenAI integration test uses a local fake client, so it verifies request construction without spending API credits or transmitting test data.

## Run the R exercise

After installing R 4.x:

```powershell
Rscript r/data_science_exercises.R
```

The script uses base R only and writes its graph and summary to `artifacts/`.

## Repository and submission

The intended private remote is:

`https://github.com/jamesris1/adaptive-llm-course-portfolio`

Before submission, confirm that the repository is private, invite the instructor using the exact GitHub username supplied by the course, and replace the bracketed title-page fields in the reports. See `docs/submission_checklist.md` for the final human review.

## Directory guide

```text
app.py                         Gradio application
hello_world.py                 Environment smoke test
src/adaptive_llm_portfolio/    Chatbot and adaptation logic
tests/                         Automated tests
data/                          Exercise dataset
notebooks/                     Python/Jupyter exercise
r/                             R exercise
scripts/                       Reproducible analysis and packaging helpers
docs/reports/                  APA-style assignment reports
docs/figures/                  Verified screenshots and charts
submission/                    Final ZIP archive
```

## Academic-use note

Review every report, screenshot, citation, and result before submitting. Replace the clearly marked personal/course placeholders and ensure the narrative accurately reflects the experience you intend to represent as your own.

