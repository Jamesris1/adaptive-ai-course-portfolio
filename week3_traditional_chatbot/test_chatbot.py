from chatbot import CAPABILITIES, reply, tokenize


def test_tokenize_normalizes_case_and_punctuation() -> None:
    assert tokenize("Hello, PYTHON!") == {"hello", "python"}


def test_capabilities_are_available() -> None:
    assert reply("What can you do?") == CAPABILITIES


def test_assignment_intent() -> None:
    answer = reply("What is required for the assignment report?")
    assert "5-7 page" in answer
    assert "ZIP" in answer


def test_setup_intent() -> None:
    assert "virtual environment" in reply("How do I set up Python?")


def test_testing_intent() -> None:
    assert "pytest" in reply("How should I test this?")


def test_unknown_topic_uses_recovery_message() -> None:
    assert reply("Tell me about gardening").startswith("I do not have a rule")


def test_blank_input_is_handled() -> None:
    assert reply("   ").startswith("Please enter a question")


def test_punctuation_only_input_is_handled() -> None:
    assert reply("?!...").startswith("I could not find any words")


def test_overlong_input_is_handled() -> None:
    assert "too long" in reply("a" * 501)


def test_response_is_repeatable() -> None:
    message = "How do I use GitHub for this project?"
    assert reply(message) == reply(message)
