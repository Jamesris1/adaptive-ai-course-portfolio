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

## Live Azure acceptance check

Verified September 12, 2026 with the student-owned Azure AI Language F0 resource in Canada Central:

| Input type | Test statement | Actual label | Positive | Neutral | Negative | Result |
|---|---|---:|---:|---:|---:|---:|
| Positive | I am excited that the chatbot is working. | Positive | 1.0000 | 0.0000 | 0.0000 | Pass |
| Negative | This setup is frustrating and difficult. | Negative | 0.0000 | 0.0000 | 1.0000 | Pass |
| Neutral | The assignment is due this week. | Neutral | 0.0000 | 0.9700 | 0.0300 | Pass |

All three live calls returned the intended label and three confidence scores. The Azure key was used only in memory for the acceptance test and was then cleared from the browser clipboard and local process. It was not saved in this repository, the report, or the submission archive.
