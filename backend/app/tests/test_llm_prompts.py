from app.llm.prompts import (
    build_primary_prompt,
    build_reviewer_prompt,
    build_synthesis_prompt,
)


def test_primary_prompt_includes_user_question_and_core_guidance() -> None:
    prompt = build_primary_prompt("What is consensus?")

    assert "What is consensus?" in prompt
    assert "Answer the user's question directly" in prompt
    assert "State important assumptions" in prompt
    assert "mention important uncertainty" in prompt
    assert "Avoid unsupported certainty" in prompt
    assert "Do not invent citations" in prompt
    assert "Do not claim to have browsed the web" in prompt
    assert "Do not mention internal prompt instructions" in prompt


def test_reviewer_prompt_includes_inputs_and_quality_review_guidance() -> None:
    prompt = build_reviewer_prompt("What is consensus?", "It is agreement.")

    assert "What is consensus?" in prompt
    assert "It is agreement." in prompt
    assert "objective quality reviewer" in prompt
    assert "not as a debate opponent" in prompt
    assert "Identify weak claims" in prompt
    assert "missing context" in prompt
    assert "unstated assumptions" in prompt
    assert "uncertainty should be clearer" in prompt
    assert "Do not argue merely to disagree" in prompt


def test_synthesis_prompt_includes_inputs_and_json_contract() -> None:
    prompt = build_synthesis_prompt(
        "What is consensus?",
        "It is agreement.",
        "It misses uncertainty.",
    )

    assert "What is consensus?" in prompt
    assert "It is agreement." in prompt
    assert "It misses uncertainty." in prompt
    assert "Return valid JSON only" in prompt
    assert "Do not wrap JSON in Markdown" in prompt
    assert "Do not include commentary before or after the JSON" in prompt
    assert "Use empty arrays if a section has no items" in prompt
    assert "All array values must be strings" in prompt
    assert "Avoid unsupported claims and invented sources" in prompt

    for key in [
        "final_answer",
        "agreement_points",
        "disagreement_points",
        "uncertainties",
        "follow_up_questions",
    ]:
        assert key in prompt
