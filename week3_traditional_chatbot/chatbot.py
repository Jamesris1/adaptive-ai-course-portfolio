"""Rule-based help desk chatbot for the Week 3 traditional chatbot project."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Intent:
    name: str
    keywords: frozenset[str]
    response: str


CAPABILITIES = (
    "I can explain my capabilities, course topics, assignment requirements, "
    "Python setup, GitHub steps, testing, and basic troubleshooting. "
    "Try 'What can you do?' or 'How do I test the chatbot?'"
)

INTENTS = (
    Intent(
        "capabilities",
        frozenset({"capabilities", "capability", "help", "options", "topics"}),
        CAPABILITIES,
    ),
    Intent(
        "greeting",
        frozenset({"hello", "hi", "hey", "greetings"}),
        "Hello. I am the Week 3 course-support chatbot. Ask what I can do to see my topics.",
    ),
    Intent(
        "course",
        frozenset({"course", "week", "module", "topic", "learn", "objective"}),
        "Week 3 covers the chatbot development lifecycle, a traditional chatbot prototype, "
        "and preparation for a later AI-service extension.",
    ),
    Intent(
        "assignment",
        frozenset({"assignment", "deliverable", "report", "apa", "zip", "submit"}),
        "The traditional chatbot assignment requires a working source project, a 5-7 page "
        "APA report, a ZIP archive, and the GitHub repository URL.",
    ),
    Intent(
        "setup",
        frozenset({"setup", "install", "environment", "python", "venv", "requirements"}),
        "Create a Python virtual environment, install requirements.txt, and run python app.py. "
        "The local page will open at the address shown in the terminal.",
    ),
    Intent(
        "github",
        frozenset({"github", "repository", "repo", "commit", "push", "url"}),
        "Keep the source in the private course repository, commit the verified files, and "
        "include the repository URL in the report and submission text.",
    ),
    Intent(
        "testing",
        frozenset({"test", "testing", "verify", "pytest", "check"}),
        "Run python -m pytest -q. Then try a known topic, an unknown topic, empty input, "
        "punctuation-only input, and the capabilities question in the browser.",
    ),
    Intent(
        "troubleshooting",
        frozenset({"error", "problem", "stuck", "failed", "trouble", "fix"}),
        "Read the first error line, confirm the virtual environment is active, reinstall the "
        "requirements, and retry the exact command. Do not paste passwords or keys into chat.",
    ),
    Intent(
        "thanks",
        frozenset({"thanks", "thank"}),
        "You are welcome. Testing one expected input and one unexpected input is a good next step.",
    ),
    Intent(
        "goodbye",
        frozenset({"bye", "goodbye", "exit", "quit"}),
        "Goodbye. Save your work and run the tests before packaging the project.",
    ),
)


def tokenize(message: str) -> set[str]:
    """Normalize user text into lowercase alphabetic tokens."""

    return set(re.findall(r"[a-zA-Z]+", message.casefold()))


def reply(message: str | None) -> str:
    """Return a deterministic response or a clear recovery message."""

    clean = (message or "").strip()
    if not clean:
        return "Please enter a question. Ask 'What can you do?' if you need an example."
    if len(clean) > 500:
        return "That message is too long for this simple bot. Please use 500 characters or fewer."

    words = tokenize(clean)
    if not words:
        return "I could not find any words in that input. Please enter a short question."
    if "what can you do" in clean.casefold():
        return CAPABILITIES

    best_intent: Intent | None = None
    best_score = 0
    for intent in INTENTS:
        score = len(words & intent.keywords)
        if score > best_score:
            best_intent = intent
            best_score = score

    if best_intent is not None:
        return best_intent.response

    return (
        "I do not have a rule for that topic. "
        "Ask 'What can you do?' to see the questions I can answer."
    )
