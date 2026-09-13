from types import SimpleNamespace

import pytest
from azure_chatbot import CAPABILITIES, reply
from azure_service import AzureSentimentService, AzureServiceError


class FakeClient:
    def __init__(self, document):
        self.document = document
        self.calls = []

    def analyze_sentiment(self, documents, **kwargs):
        self.calls.append((documents, kwargs))
        return [self.document]


def result(label="positive", positive=0.91, neutral=0.07, negative=0.02):
    return SimpleNamespace(
        is_error=False,
        sentiment=label,
        confidence_scores=SimpleNamespace(
            positive=positive,
            neutral=neutral,
            negative=negative,
        ),
    )


def test_azure_request_disables_service_logging() -> None:
    client = FakeClient(result())
    service = AzureSentimentService(client=client)
    analysis = service.analyze("This is working well.")
    assert analysis.label == "Positive"
    assert client.calls[0][0] == ["This is working well."]
    assert client.calls[0][1]["disable_service_logs"] is True


def test_integrated_reply_includes_rule_and_azure_result() -> None:
    service = AzureSentimentService(client=FakeClient(result()))
    answer = reply("I am happy with the assignment report.", service)
    assert "5-7 page APA report" in answer
    assert "Azure AI Language sentiment: Positive" in answer
    assert "positive 0.91" in answer


def test_capabilities_include_sentiment_analysis() -> None:
    service = AzureSentimentService(client=FakeClient(result()))
    assert CAPABILITIES in reply("What can you do?", service)


def test_missing_configuration_is_explained() -> None:
    service = AzureSentimentService(endpoint="", key="")
    answer = reply("This is an ordinary statement.", service)
    assert "Azure status: Not configured" in answer


def test_blank_input_does_not_call_azure() -> None:
    client = FakeClient(result())
    answer = reply("   ", AzureSentimentService(client=client))
    assert answer == "Please enter a question or statement."
    assert client.calls == []


def test_punctuation_only_input_does_not_call_azure() -> None:
    client = FakeClient(result())
    answer = reply("?!...", AzureSentimentService(client=client))
    assert answer.startswith("I could not find any words")
    assert client.calls == []


def test_overlong_input_does_not_call_azure() -> None:
    client = FakeClient(result())
    answer = reply("a" * 501, AzureSentimentService(client=client))
    assert "too long" in answer
    assert client.calls == []


def test_document_error_is_reported() -> None:
    document = SimpleNamespace(
        is_error=True,
        error=SimpleNamespace(code="InvalidDocument"),
    )
    service = AzureSentimentService(client=FakeClient(document))
    with pytest.raises(AzureServiceError, match="InvalidDocument"):
        service.analyze("test")


def test_transport_error_is_wrapped() -> None:
    class BrokenClient:
        def analyze_sentiment(self, *_args, **_kwargs):
            raise RuntimeError("network details")

    service = AzureSentimentService(client=BrokenClient())
    with pytest.raises(AzureServiceError, match="could not analyze"):
        service.analyze("test")
