import pytest
from pydantic import ValidationError

from app.schemas import ConsensusRequest, ConsensusResponse, ModelsUsed


def test_valid_consensus_request_passes() -> None:
    request = ConsensusRequest(
        question="What are the risks of relying on one AI answer?",
        primary_provider="openai",
        reviewer_provider="gemini",
        synthesizer_provider="openai",
    )

    assert request.question == "What are the risks of relying on one AI answer?"


def test_empty_question_fails() -> None:
    with pytest.raises(ValidationError):
        ConsensusRequest(
            question="",
            primary_provider="openai",
            reviewer_provider="gemini",
            synthesizer_provider="openai",
        )


def test_whitespace_only_question_fails() -> None:
    with pytest.raises(ValidationError):
        ConsensusRequest(
            question="   ",
            primary_provider="openai",
            reviewer_provider="gemini",
            synthesizer_provider="openai",
        )


def test_overlong_question_fails() -> None:
    with pytest.raises(ValidationError):
        ConsensusRequest(
            question="x" * 8001,
            primary_provider="openai",
            reviewer_provider="gemini",
            synthesizer_provider="openai",
        )


def test_uppercase_provider_fails() -> None:
    with pytest.raises(ValidationError):
        ConsensusRequest(
            question="What should I consider?",
            primary_provider="OpenAI",
            reviewer_provider="gemini",
            synthesizer_provider="openai",
        )


def test_unsupported_provider_fails() -> None:
    with pytest.raises(ValidationError):
        ConsensusRequest(
            question="What should I consider?",
            primary_provider="claude",
            reviewer_provider="gemini",
            synthesizer_provider="openai",
        )


def test_consensus_response_accepts_valid_structured_output() -> None:
    response = ConsensusResponse(
        question="Question",
        primary_answer="Primary",
        reviewer_critique="Critique",
        final_answer="Final",
        agreement_points=["Agreement"],
        disagreement_points=["Disagreement"],
        uncertainties=["Uncertainty"],
        follow_up_questions=["Follow up?"],
        models_used=ModelsUsed(
            primary="gpt-test",
            reviewer="gemini-test",
            synthesizer="gpt-test",
        ),
    )

    assert response.final_answer == "Final"
    assert response.models_used.primary == "gpt-test"
