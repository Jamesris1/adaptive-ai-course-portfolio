from src.adaptive_llm_portfolio.chat_engine import ADAPTIVE_MODE, TRADITIONAL_MODE, ChatEngine
from src.adaptive_llm_portfolio.openai_service import OpenAIChatService


def test_traditional_mode_answers_known_intent() -> None:
    reply, context = ChatEngine().reply("How do I set up Python?", [], TRADITIONAL_MODE)
    assert "virtual environment" in reply
    assert context.language == "English"


def test_adaptive_offline_mode_is_transparent() -> None:
    service = OpenAIChatService(api_key="")
    reply, context = ChatEngine(service).reply(
        "I am stuck and need a brief plan today", [], ADAPTIVE_MODE
    )
    assert reply.startswith("Offline demonstration mode")
    assert "step-by-step" in reply
    assert context.response_density == "Compact"
