"""Transparent, testable adaptation signals for the chatbot interface."""

from __future__ import annotations

from dataclasses import dataclass

SPANISH_MARKERS = {
    "hola",
    "gracias",
    "ayuda",
    "por favor",
    "tarea",
    "necesito",
    "como",
    "cómo",
}
NEGATIVE_MARKERS = {
    "angry",
    "confused",
    "frustrated",
    "hate",
    "lost",
    "overwhelmed",
    "stuck",
    "upset",
    "enojado",
    "confundido",
    "frustrado",
}
POSITIVE_MARKERS = {
    "awesome",
    "excellent",
    "excited",
    "good",
    "great",
    "happy",
    "love",
    "thanks",
    "gracias",
}
URGENT_MARKERS = {"urgent", "asap", "deadline", "today", "now", "ahora", "hoy"}
SHORT_MARKERS = {"brief", "quick", "short", "concise", "resumen", "rápido"}


@dataclass(frozen=True)
class UserContext:
    language: str
    sentiment: str
    urgency: str
    response_density: str

    @property
    def tone_instruction(self) -> str:
        if self.language == "Spanish":
            language = "Respond in clear Spanish."
        else:
            language = "Respond in clear English."

        if self.sentiment == "Needs support":
            tone = "Acknowledge the difficulty once, then give calm numbered steps."
        elif self.sentiment == "Positive":
            tone = "Match the positive energy while staying useful."
        else:
            tone = "Use a neutral, encouraging instructional tone."

        urgency = (
            "Lead with the next immediate action."
            if self.urgency == "High"
            else "Provide the rationale before optional next steps."
        )
        density = (
            "Keep the answer under 120 words unless safety requires more detail."
            if self.response_density == "Compact"
            else "Use a concise explanation with an example when helpful."
        )
        return " ".join((language, tone, urgency, density))


def _contains_any(text: str, markers: set[str]) -> bool:
    lowered = text.casefold()
    return any(marker in lowered for marker in markers)


def analyze_user_context(message: str) -> UserContext:
    """Infer lightweight adaptation signals without collecting identity data."""

    language = "Spanish" if _contains_any(message, SPANISH_MARKERS) else "English"
    if _contains_any(message, NEGATIVE_MARKERS):
        sentiment = "Needs support"
    elif _contains_any(message, POSITIVE_MARKERS):
        sentiment = "Positive"
    else:
        sentiment = "Neutral"

    urgency = "High" if _contains_any(message, URGENT_MARKERS) else "Normal"
    response_density = "Compact" if _contains_any(message, SHORT_MARKERS) else "Guided"
    return UserContext(language, sentiment, urgency, response_density)
