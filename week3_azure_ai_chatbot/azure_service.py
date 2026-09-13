"""Azure AI Language sentiment-analysis adapter."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

load_dotenv()


class AzureServiceError(RuntimeError):
    """Raised when Azure AI Language cannot analyze a message."""


@dataclass(frozen=True)
class SentimentResult:
    label: str
    positive: float
    neutral: float
    negative: float


class AzureSentimentService:
    """Small testable wrapper around Azure TextAnalyticsClient."""

    def __init__(
        self,
        endpoint: str | None = None,
        key: str | None = None,
        client: Any | None = None,
    ) -> None:
        self.endpoint = endpoint if endpoint is not None else os.getenv(
            "AZURE_LANGUAGE_ENDPOINT", ""
        )
        self.key = key if key is not None else os.getenv("AZURE_LANGUAGE_KEY", "")
        self._client = client

    @property
    def available(self) -> bool:
        return self._client is not None or bool(self.endpoint and self.key)

    def _get_client(self) -> Any:
        if self._client is None:
            from azure.ai.textanalytics import TextAnalyticsClient
            from azure.core.credentials import AzureKeyCredential

            self._client = TextAnalyticsClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(self.key),
            )
        return self._client

    def analyze(self, message: str) -> SentimentResult:
        if not self.available:
            raise AzureServiceError(
                "Azure AI Language is not configured. Add the endpoint and key to .env."
            )

        try:
            response = self._get_client().analyze_sentiment(
                [message],
                show_opinion_mining=False,
                disable_service_logs=True,
            )
            document = response[0]
        except Exception as exc:
            raise AzureServiceError(
                "Azure AI Language could not analyze the message."
            ) from exc

        if getattr(document, "is_error", False):
            error = getattr(document, "error", None)
            code = getattr(error, "code", "Unknown")
            raise AzureServiceError(f"Azure AI Language returned an error: {code}.")

        scores = document.confidence_scores
        return SentimentResult(
            label=str(document.sentiment).capitalize(),
            positive=float(scores.positive),
            neutral=float(scores.neutral),
            negative=float(scores.negative),
        )
