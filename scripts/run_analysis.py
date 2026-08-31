"""Python graph and study-plan program for the data-science-language exercise."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "study_sessions.csv"
ARTIFACTS = ROOT / "artifacts"


def recommend_study_plan(data: pd.DataFrame, target_score: float = 90) -> dict[str, object]:
    """Create a plan using recent score trend, language balance, and confidence."""

    recent = data.tail(3)
    score_gain = float(recent["quiz_score"].iloc[-1] - recent["quiz_score"].iloc[0])
    current = float(data["quiz_score"].iloc[-1])
    gap = max(0.0, target_score - current)
    python_total = float(data["python_hours"].sum())
    r_total = float(data["r_hours"].sum())
    weaker_language = "R" if r_total < python_total else "Python"
    confidence = int(data["confidence"].iloc[-1])
    extra_hours = round(max(1.0, gap / max(score_gain, 1.0) * 1.5), 1)
    actions = [
        f"Add {extra_hours} focused hours next week, prioritizing {weaker_language}.",
        "Recreate one graph without looking at the example.",
        "Run the chatbot tests and explain one failure mode in plain language.",
    ]
    if confidence < 4:
        actions.append("Schedule a short review session before attempting the next project.")
    return {
        "current_score": current,
        "target_score": target_score,
        "recent_score_gain": score_gain,
        "priority_language": weaker_language,
        "recommended_extra_hours": extra_hours,
        "actions": actions,
    }


def create_graph(data: pd.DataFrame, output: Path) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7.2), height_ratios=[1.4, 1])
    fig.patch.set_facecolor("#f8fafc")

    ax1.plot(data["week"], data["quiz_score"], marker="o", linewidth=2.5, color="#4338ca")
    ax1.fill_between(data["week"], data["quiz_score"], 55, alpha=0.12, color="#4338ca")
    ax1.axhline(90, color="#0f766e", linestyle="--", linewidth=1.5, label="Target: 90")
    ax1.set_title("Learning Progress Across Ten Weeks", loc="left", weight="bold", fontsize=15)
    ax1.set_ylabel("Quiz score")
    ax1.set_ylim(55, 96)
    ax1.legend(frameon=False, loc="lower right")
    ax1.annotate(
        "29-point improvement",
        xy=(10, 91),
        xytext=(6.4, 94),
        arrowprops={"arrowstyle": "->", "color": "#334155"},
        color="#334155",
    )

    ax2.bar(data["week"] - 0.18, data["python_hours"], width=0.36, label="Python", color="#2563eb")
    ax2.bar(data["week"] + 0.18, data["r_hours"], width=0.36, label="R", color="#f97316")
    ax2.set_xlabel("Week")
    ax2.set_ylabel("Practice hours")
    ax2.set_xticks(data["week"])
    ax2.legend(frameon=False, ncol=2, loc="upper left")
    for spine in ("top", "right"):
        ax1.spines[spine].set_visible(False)
        ax2.spines[spine].set_visible(False)

    fig.text(
        0.1,
        0.01,
        "Source: synthetic course-practice dataset created for this exercise.",
        fontsize=9,
        color="#64748b",
    )
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ARTIFACTS.mkdir(exist_ok=True)
    data = pd.read_csv(DATA)
    plan = recommend_study_plan(data)
    create_graph(data, ARTIFACTS / "python_study_progress.png")
    (ARTIFACTS / "python_analysis_summary.json").write_text(
        json.dumps(plan, indent=2), encoding="utf-8"
    )
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
