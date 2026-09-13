# Week 3 Azure AI Language Chatbot

This project extends the repository's Week 3 traditional chatbot with Azure AI Language sentiment analysis. The traditional bot supplied the local intent-and-response starting point; the Azure adapter was added so valid messages can receive positive, neutral, negative, or mixed sentiment labels and confidence scores.

## Capabilities

- Answers fixed course-support questions about the assignment, setup, GitHub, testing, and troubleshooting.
- Lists its capabilities when asked.
- Sends valid messages to Azure AI Language for sentiment analysis.
- Displays the sentiment label and positive, neutral, and negative confidence scores.
- Handles blank, punctuation-only, overlong, unsupported, unconfigured-service, and service-error cases.

## Create the Azure resource

1. Sign in to the Azure portal with the account you will use for this course.
2. Create an Azure AI Language resource and select the free F0 pricing tier.
3. Keep the resource in an appropriate region and accept the Responsible AI notice.
4. Open the resource's Keys and Endpoint page.
5. Never paste the key into source code, GitHub, the report, screenshots, or chat.

## Configure and run

From this folder in PowerShell:

```powershell
py -3.12 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` locally and add:

```text
AZURE_LANGUAGE_ENDPOINT=https://YOUR-RESOURCE-NAME.cognitiveservices.azure.com/
AZURE_LANGUAGE_KEY=YOUR-LOCAL-KEY
```

Then run:

```powershell
python app.py
```

Open the local address shown in the terminal. The default is `http://127.0.0.1:7860`.

## Verify

```powershell
python -m pytest -q
```

The tests use a fake Azure client. They verify request construction, logging controls, sentiment formatting, malformed input, unavailable configuration, and service errors without transmitting test data or consuming Azure quota.

For the required live check, configure your own resource and send one positive, one negative, and one neutral statement. Record only the sentiment labels and confidence scores. Do not record or share the key.

## AI use disclosure

Codex was used to assist with initial code scaffolding, test-case planning, debugging, and editing the written documentation. Before submission, James Risitne will review the requirements, source code, test results, and final deliverables and will remain responsible for the submitted work.
