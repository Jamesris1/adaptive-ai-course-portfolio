# Week 3 Azure Integration Verification

## Automated checks

The test suite verifies:

- the Azure request and disabled service logging;
- conversion of the Azure response into a local result;
- combined traditional and Azure output;
- capability reporting;
- missing configuration;
- blank, punctuation-only, and overlong input;
- Azure document errors; and
- transport-error handling.

## Local runtime check

Verified September 12, 2026:

- 9 Azure-specific tests passed;
- all 26 repository tests passed;
- code-quality checks passed;
- `azure-ai-textanalytics` 5.4.0 imported successfully;
- the Gradio application constructed successfully; and
- the local application returned HTTP 200 at `http://127.0.0.1:7868/` with the expected page title.

These checks validate the local application and Azure integration boundary. They do not replace the live Azure acceptance test below.

## Required live Azure check

This check must use the student's own Azure AI Language free-tier resource.

| Input type | Example | Expected evidence |
|---|---|---|
| Positive | I am excited that the chatbot is working. | Positive label and three confidence scores |
| Negative | This setup is frustrating and difficult. | Negative label and three confidence scores |
| Neutral | The assignment is due this week. | Neutral or mixed label and three confidence scores |

Do not record the endpoint key. If a label differs from the expectation, record the actual result rather than changing it.
