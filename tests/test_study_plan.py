import pandas as pd

from scripts.run_analysis import recommend_study_plan


def test_study_plan_prioritizes_less_practiced_language() -> None:
    data = pd.DataFrame(
        {
            "python_hours": [4, 5, 6],
            "r_hours": [1, 2, 2],
            "quiz_score": [80, 84, 88],
            "confidence": [3, 4, 4],
        }
    )
    result = recommend_study_plan(data)
    assert result["priority_language"] == "R"
    assert result["recommended_extra_hours"] >= 1
