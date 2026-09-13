# Week 3 Traditional Chatbot

This is a standalone, non-LLM chatbot for the Week 3 assignment. It uses deterministic keyword rules to answer common course-support questions. No account, API key, cloud service, or model call is required.

## Capabilities

The bot responds to greetings and questions about its capabilities, the Week 3 topic, assignment requirements, Python setup, GitHub, testing, and troubleshooting. It also provides recovery messages for unknown topics, blank messages, punctuation-only input, and messages longer than 500 characters.

## Run the project

From this folder in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open the local address shown in the terminal. The default is `http://127.0.0.1:7860`.

## Run the tests

```powershell
python -m pytest -q
```

The tests cover known intents, the capabilities prompt, malformed input, unknown topics, the length limit, and deterministic responses.

## Development lifecycle

1. Requirements: define the required prompts, capabilities response, malformed-input recovery, and submission files.
2. Design: separate the rule engine from the interface so each part is easier to test and replace.
3. Implementation: normalize text, score keyword overlap, and return a fixed response for the best matching intent.
4. Testing: automate representative inputs, then verify the browser controls and conversation history manually.
5. Deployment: run locally for the assignment and keep the source in the private course repository.
6. Maintenance: review failed or unknown questions, add narrowly defined rules, and rerun the tests after each change.

## Project structure

```text
app.py               Gradio interface
chatbot.py           Rule engine and response content
test_chatbot.py      Automated tests
VERIFICATION.md      Text-only test record and sample conversation
requirements.txt     Reproducible dependencies
```

This folder is intentionally independent of the later AI-service and adaptive-interface projects.
