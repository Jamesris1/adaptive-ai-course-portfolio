"""Mode router that connects traditional, OpenAI, and adaptive behavior."""

from __future__ import annotations

from typing import Any

from .adaptive import UserContext, analyze_user_context
from .openai_service import OpenAIChatService
from .traditional import traditional_reply

TRADITIONAL_MODE = "Traditional rules"
OPENAI_MODE = "OpenAI LLM"
ADAPTIVE_MODE = "Adaptive OpenAI"


class ChatEngine:
    def __init__(self, openai_service: OpenAIChatService | None = None) -> None:
        self.openai_service = openai_service or OpenAIChatService()

    def reply(
        self,
        message: str,
        history: list[dict[str, Any]] | None,
        mode: str,
    ) -> tuple[str, UserContext]:
        context = analyze_user_context(message)
        if mode == TRADITIONAL_MODE:
            return traditional_reply(message), context
        if mode == ADAPTIVE_MODE:
            return (
                self.openai_service.reply(message, history, context.tone_instruction),
                context,
            )
        return self.openai_service.reply(message, history), context
