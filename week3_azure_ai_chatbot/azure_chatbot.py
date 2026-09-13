"""Traditional course-support chatbot extended with Azure sentiment analysis."""

from __future__ import annotations

import re
from dataclasses import dataclass

try:
    from .azure_service import AzureSentimentService, AzureServiceError, SentimentResult
except ImportError:  # Support direct execution and tests from this directory.
    from azure_service import AzureSentimentService, AzureServiceError, SentimentResult


@dataclass(frozen=True)
class Intent:
    keywords: frozenset[str]
    response: str


CAPABILITIES = (
    "I can explain the assignment, setup, GitHub, testing, and troubleshooting. "
    "For valid messages, Azure AI Language also reports sentiment and confidence scores."
)

INTENTS = (
    Intent(
        frozenset({"capabilities", "capability", "help", "options", "topics"}),
        CAPABILITIES,
    ),
    Intent(
        frozenset({"hello", "hi", "hey", "greetings"}),
        "Hello. Ask what I can do or enter a short statement for sentiment analysis.",
    ),
    Intent(
        frozenset({"assignment", "deliverable", "report", "apa", "zip", "submit"}),
        "Submit a 5-7 page APA report, the Azure chatbot source ZIP, and the GitHub URL.",
    ),
    Intent(
        frozenset({"setup", "install", "environment", "python", "requirements", "azure"}),
        "Install requirements.txt, copy .env.example to .env, add your Azure Language "
        "endpoint and key locally, and run python app.py.",
    ),
    Intent(
        frozenset({"github", "repository", "repo", "commit", "push", "url"}),
        "Commit only source and documentation. Keep .env and the Azure key out of GitHub "
        "and out of the ZIP archive.",
    ),
    Intent(
        frozenset({"test", "testing", "verify", "pytest", "check"}),
        "Run python -m pytest -q, then verify positive, negative, neutral, malformed, "
        "and unavailable-service cases.",
    ),
    Intent(
        frozenset({"error", "problem", "stuck", "failed", "trouble", "fix"}),
        "Confirm the endpoint begins with https, verify the resource key in your local "
        ".env file, and check that the Azure Language resource is active.",
    ),
    Intent(
        frozenset({"thanks", "thank"}),
        "You are welcome. Try one positive and one negative sentence to compare the scores.",
    ),
    Intent(
        frozenset({"bye", "goodbye", "exit", "quit"}),
        "Goodbye. Remove credentials from the environment before sharing diagnostic output.",
    ),
)


def tokenize(message: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z]+", message.casefold()))


def validate_message(message: str | None) -> tuple[str, str | None]:
    clean = (message or "").strip()
    if not clean:
        return clean, "Please enter a question or statement."
    if len(clean) > 500:
        return clean, "That message is too long. Please use 500 characters or fewer."
    if not tokenize(clean):
        return clean, "I could not find any words. Please enter a short question or statement."
    return clean, None


def traditional_reply(message: str) -> str:
    words = tokenize(message)
    if "what can you do" in message.casefold():
        return CAPABILITIES

    best: Intent | None = None
    best_score = 0
    for intent in INTENTS:
        score = len(words & intent.keywords)
        if score > best_score:
            best = intent
            best_score = score
    if best is not None:
        return best.response
    return (
        "I do not have a local rule for that topic, but I can still report its "
        "Azure sentiment result."
    )


def format_sentiment(result: SentimentResult) -> str:
    return (
        f"Azure AI Language sentiment: {result.label} "
        f"(positive {result.positive:.2f}, neutral {result.neutral:.2f}, "
        f"negative {result.negative:.2f})."
    )


def reply(
    message: str | None,
    service: AzureSentimentService | None = None,
) -> str:
    clean, validation_error = validate_message(message)
    if validation_error:
        return validation_error

    local_answer = traditional_reply(clean)
    service = service or AzureSentimentService()
    if not service.available:
        return (
            f"{local_answer}\n\nAzure status: Not configured. "
            "Add AZURE_LANGUAGE_ENDPOINT and AZURE_LANGUAGE_KEY to a local .env file."
        )

    try:
        result = service.analyze(clean)
    except AzureServiceError as exc:
        return f"{local_answer}\n\nAzure status: {exc}"
    return f"{local_answer}\n\n{format_sentiment(result)}"
