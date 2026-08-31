from src.adaptive_llm_portfolio.adaptive import analyze_user_context


def test_detects_support_and_urgency() -> None:
    context = analyze_user_context("I am frustrated and need a short answer today")
    assert context.sentiment == "Needs support"
    assert context.urgency == "High"
    assert context.response_density == "Compact"


def test_detects_spanish() -> None:
    context = analyze_user_context("Hola, necesito ayuda con la tarea")
    assert context.language == "Spanish"
    assert "Spanish" in context.tone_instruction
