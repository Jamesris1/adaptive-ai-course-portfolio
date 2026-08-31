from types import SimpleNamespace

from src.adaptive_llm_portfolio.openai_service import OpenAIChatService


class FakeResponses:
    def __init__(self) -> None:
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(output_text="Verified fake response")


class FakeClient:
    def __init__(self) -> None:
        self.responses = FakeResponses()


def test_responses_api_request_is_private_and_uses_output_text() -> None:
    client = FakeClient()
    service = OpenAIChatService(api_key="test", model="test-model", client=client)
    output = service.reply("Hello", [{"role": "assistant", "content": "Welcome"}])
    assert output == "Verified fake response"
    assert client.responses.kwargs["model"] == "test-model"
    assert client.responses.kwargs["store"] is False
    assert client.responses.kwargs["input"][-1] == {"role": "user", "content": "Hello"}
