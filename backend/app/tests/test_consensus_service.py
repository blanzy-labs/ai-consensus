import pytest

from app.config import Settings
from app.llm.base import MissingProviderConfigError
from app.schemas import ConsensusRequest
from app.services.consensus_service import ConsensusService, parse_synthesis_output


class FakeProvider:
    def __init__(self, name: str, model_name: str, output: str, calls: list[str]) -> None:
        self.provider_name = name
        self.model_name = model_name
        self._output = output
        self._calls = calls

    def generate(self, prompt: str) -> str:
        self._calls.append(self.provider_name)
        return self._output


def test_consensus_service_calls_providers_in_order_and_returns_outputs() -> None:
    calls: list[str] = []
    providers = [
        FakeProvider("primary", "primary-model", "Primary answer", calls),
        FakeProvider("reviewer", "reviewer-model", "Reviewer critique", calls),
        FakeProvider(
            "synthesizer",
            "synthesizer-model",
            """{
                "final_answer": "Final answer",
                "agreement_points": ["A"],
                "disagreement_points": ["D"],
                "uncertainties": ["U"],
                "follow_up_questions": ["F?"]
            }""",
            calls,
        ),
    ]

    def factory(provider_name: str, settings: Settings) -> FakeProvider:
        return providers.pop(0)

    service = ConsensusService(Settings(_env_file=None), provider_factory=factory)
    request = ConsensusRequest(
        question="What should I know?",
        primary_provider="openai",
        reviewer_provider="gemini",
        synthesizer_provider="openai",
    )

    response = service.run(request)

    assert calls == ["primary", "reviewer", "synthesizer"]
    assert response.primary_answer == "Primary answer"
    assert response.reviewer_critique == "Reviewer critique"
    assert response.final_answer == "Final answer"
    assert response.agreement_points == ["A"]
    assert response.disagreement_points == ["D"]
    assert response.uncertainties == ["U"]
    assert response.follow_up_questions == ["F?"]
    assert response.models_used.primary == "primary-model"


def test_parse_synthesis_output_handles_invalid_json_gracefully() -> None:
    parsed = parse_synthesis_output("This is not JSON.")

    assert parsed["final_answer"] == "This is not JSON."
    assert parsed["agreement_points"] == []
    assert parsed["disagreement_points"] == []
    assert parsed["uncertainties"] == ["The synthesizer did not return valid structured JSON."]
    assert parsed["follow_up_questions"] == []


def test_parse_synthesis_output_handles_json_wrapped_in_markdown() -> None:
    parsed = parse_synthesis_output(
        """```json
{
  "final_answer": "Final",
  "agreement_points": ["A"],
  "disagreement_points": [],
  "uncertainties": [],
  "follow_up_questions": []
}
```"""
    )

    assert parsed["final_answer"] == "Final"
    assert parsed["agreement_points"] == ["A"]


def test_consensus_service_does_not_expose_secrets_in_errors() -> None:
    def factory(provider_name: str, settings: Settings) -> FakeProvider:
        raise MissingProviderConfigError(
            "OpenAI API key is not configured. Set OPENAI_API_KEY in your .env file."
        )

    service = ConsensusService(Settings(_env_file=None, openai_api_key="secret-key"), provider_factory=factory)
    request = ConsensusRequest(
        question="What should I know?",
        primary_provider="openai",
        reviewer_provider="gemini",
        synthesizer_provider="openai",
    )

    with pytest.raises(MissingProviderConfigError) as exc_info:
        service.run(request)

    assert "secret-key" not in str(exc_info.value)
