"""Small smoke test for the development-environment exercise."""

from platform import python_version


def greeting(name: str = "AI learner") -> str:
    return f"Hello, {name}! Python {python_version()} is ready for LLM development."


if __name__ == "__main__":
    print(greeting())
