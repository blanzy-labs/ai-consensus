from fastapi.testclient import TestClient

from app.llm.base import MissingProviderConfigError, UnsupportedProviderError
from app.main import app
from app.routes.consensus import get_consensus_service
from app.schemas import ConsensusResponse, ModelsUsed


client = TestClient(app)


class SuccessfulConsensusService:
    def run(self, request):
        return ConsensusResponse(
            question=request.question,
            primary_answer="Primary answer",
            reviewer_critique="Reviewer critique",
            final_answer="Final answer",
            agreement_points=["Agreement"],
            disagreement_points=[],
            uncertainties=[],
            follow_up_questions=["Follow up?"],
            models_used=ModelsUsed(
                primary="primary-model",
                reviewer="reviewer-model",
                synthesizer="synthesizer-model",
            ),
        )


class UnsupportedProviderService:
    def run(self, request):
        raise UnsupportedProviderError("Unsupported provider: xyz")


class MissingKeyService:
    def run(self, request):
        raise MissingProviderConfigError(
            "OpenAI API key is not configured. Set OPENAI_API_KEY in your .env file."
        )


def teardown_function() -> None:
    app.dependency_overrides.clear()


def test_consensus_run_returns_structured_response_when_providers_are_mocked() -> None:
    app.dependency_overrides[get_consensus_service] = lambda: SuccessfulConsensusService()

    response = client.post(
        "/consensus/run",
        json={
            "question": "What are the risks of relying on one AI answer?",
            "primary_provider": "openai",
            "reviewer_provider": "gemini",
            "synthesizer_provider": "openai",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["question"] == "What are the risks of relying on one AI answer?"
    assert body["primary_answer"] == "Primary answer"
    assert body["reviewer_critique"] == "Reviewer critique"
    assert body["final_answer"] == "Final answer"
    assert body["agreement_points"] == ["Agreement"]
    assert body["models_used"]["primary"] == "primary-model"


def test_consensus_run_invalid_request_returns_validation_error() -> None:
    response = client.post(
        "/consensus/run",
        json={
            "question": "   ",
            "primary_provider": "openai",
            "reviewer_provider": "gemini",
            "synthesizer_provider": "openai",
        },
    )

    assert response.status_code == 422


def test_consensus_run_unsupported_provider_returns_safe_error() -> None:
    app.dependency_overrides[get_consensus_service] = lambda: UnsupportedProviderService()

    response = client.post(
        "/consensus/run",
        json={
            "question": "What should I know?",
            "primary_provider": "openai",
            "reviewer_provider": "gemini",
            "synthesizer_provider": "openai",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported provider: xyz"


def test_consensus_run_missing_api_key_returns_safe_error() -> None:
    app.dependency_overrides[get_consensus_service] = lambda: MissingKeyService()

    response = client.post(
        "/consensus/run",
        json={
            "question": "What should I know?",
            "primary_provider": "openai",
            "reviewer_provider": "gemini",
            "synthesizer_provider": "openai",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "OpenAI API key is not configured. Set OPENAI_API_KEY in your .env file."
    assert "secret-key" not in response.text


def test_health_endpoint_still_works() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "mythadis-consensus-engine-backend",
    }
