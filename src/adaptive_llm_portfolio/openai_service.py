"""OpenAI Responses API adapter with an explicit offline demonstration mode."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()


BASE_INSTRUCTIONS = """You are a supportive AI-course assistant. Help with Python, Git,
Gradio, OpenAI API concepts, and assignment planning. Do not claim that work was submitted,
graded, or reviewed by a human. Never request or repeat secrets. Be concise and practical."""


class OpenAIChatService:
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        client: Any | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5")
        self._client = client

    @property
    def available(self) -> bool:
        return bool(self.api_key or self._client)

    def _get_client(self) -> Any:
        if self._client is None:
            from openai import OpenAI

            self._client = OpenAI(api_key=self.api_key)
        return self._client

    @staticmethod
    def _normalize_history(history: list[dict[str, Any]] | None) -> list[dict[str, str]]:
        normalized: list[dict[str, str]] = []
        for item in history or []:
            role = item.get("role")
            content = item.get("content")
            if role in {"user", "assistant"} and isinstance(content, str):
                normalized.append({"role": role, "content": content})
        return normalized[-12:]

    def reply(
        self,
        message: str,
        history: list[dict[str, Any]] | None = None,
        additional_instructions: str = "",
    ) -> str:
        if not self.available:
            return self.offline_reply(message, additional_instructions)

        input_messages = self._normalize_history(history)
        input_messages.append({"role": "user", "content": message})
        instructions = BASE_INSTRUCTIONS
        if additional_instructions:
            instructions += "\n\nAdaptive interaction instructions: " + additional_instructions

        response = self._get_client().responses.create(
            model=self.model,
            instructions=instructions,
            input=input_messages,
            store=False,
        )
        return response.output_text.strip()

    @staticmethod
    def offline_reply(message: str, additional_instructions: str = "") -> str:
        preview = " ".join(message.strip().split())[:120]
        if "Respond in clear Spanish" in additional_instructions:
            return (
                "Modo de demostración sin conexión: analicé tu solicitud "
                f'("{preview}"). Configura OPENAI_API_KEY para generar una respuesta del modelo. '
                "Mientras tanto, revisa README.md para los pasos de configuración."
            )
        supportive = (
            " I detected that a calmer, step-by-step response may help."
            if ("Acknowledge the difficulty" in additional_instructions)
            else ""
        )
        return (
            "Offline demonstration mode: I analyzed your request "
            f'("{preview}").{supportive} Set OPENAI_API_KEY to receive a live model response. '
            "The README contains the verified setup steps."
        )
