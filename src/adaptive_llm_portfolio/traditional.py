"""Deterministic intent-based chatbot used as the traditional baseline."""

from __future__ import annotations

import re

INTENTS: tuple[tuple[set[str], str], ...] = (
    (
        {"hello", "hi", "hey", "hola"},
        "Hello! I can explain the project, setup steps, deadlines, or how to run the app.",
    ),
    (
        {"setup", "install", "environment", "python", "venv"},
        "Create a Python 3.12 virtual environment, install requirements.txt, copy "
        ".env.example to .env, and run python app.py.",
    ),
    (
        {"github", "repository", "repo", "commit"},
        "Keep the repository private, commit the verified source and reports, then invite "
        "the instructor from Settings > Collaborators using the exact course username.",
    ),
    (
        {"assignment", "deliverable", "report", "apa"},
        "The portfolio includes separate APA-style reports, source code, figures, tests, "
        "and a ZIP archive. Review the submission checklist before uploading.",
    ),
    (
        {"help", "stuck", "error", "problem"},
        "Start with the failing command, copy only the non-sensitive error text, and compare "
        "it with the verification steps in the README. I can help narrow down the cause.",
    ),
    (
        {"thanks", "thank", "gracias"},
        "You are welcome. A good next step is to run the tests and save the result "
        "for your report.",
    ),
    (
        {"bye", "goodbye"},
        "Goodbye! Remember to remove secrets, review the reports, and verify the "
        "private-repo invitation.",
    ),
)


def tokenize(message: str) -> set[str]:
    return set(re.findall(r"[a-zA-Záéíóúñ]+", message.casefold()))


def traditional_reply(message: str) -> str:
    """Return the response for the highest-overlap known intent."""

    words = tokenize(message)
    best_score = 0
    best_reply = ""
    for keywords, reply in INTENTS:
        score = len(words & keywords)
        if score > best_score:
            best_score = score
            best_reply = reply
    if best_reply:
        return best_reply
    return (
        "I am the traditional rule-based mode, so I only recognize a limited set of topics. "
        "Try asking about setup, GitHub, the assignment, or an error."
    )
