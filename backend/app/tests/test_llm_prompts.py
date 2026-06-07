from app.llm.prompts import (
    build_primary_prompt,
    build_reviewer_prompt,
    build_synthesis_prompt,
)


def test_primary_prompt_includes_user_question() -> None:
    prompt = build_primary_prompt("What is consensus?")

    assert "What is consensus?" in prompt


def test_reviewer_prompt_includes_question_and_primary_answer() -> None:
    prompt = build_reviewer_prompt("What is consensus?", "It is agreement.")

    assert "What is consensus?" in prompt
    assert "It is agreement." in prompt


def test_synthesis_prompt_includes_inputs_and_asks_for_json() -> None:
    prompt = build_synthesis_prompt(
        "What is consensus?",
        "It is agreement.",
        "It misses uncertainty.",
    )

    assert "What is consensus?" in prompt
    assert "It is agreement." in prompt
    assert "It misses uncertainty." in prompt
    assert "Return JSON only" in prompt
    assert "final_answer" in prompt
