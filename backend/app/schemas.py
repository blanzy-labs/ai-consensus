from pydantic import BaseModel, Field, field_validator


SUPPORTED_PROVIDERS = {"openai", "gemini"}


class HealthResponse(BaseModel):
    status: str
    service: str


class ConsensusRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=8000)
    primary_provider: str
    reviewer_provider: str
    synthesizer_provider: str

    @field_validator("question")
    @classmethod
    def question_must_have_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Question must not be empty.")
        return value

    @field_validator("primary_provider", "reviewer_provider", "synthesizer_provider")
    @classmethod
    def provider_must_be_supported(cls, value: str) -> str:
        if value != value.lower():
            raise ValueError("Provider names must be lowercase.")

        if value not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {value}")

        return value


class ModelsUsed(BaseModel):
    primary: str
    reviewer: str
    synthesizer: str


class ConsensusResponse(BaseModel):
    question: str
    primary_answer: str
    reviewer_critique: str
    final_answer: str
    agreement_points: list[str]
    disagreement_points: list[str]
    uncertainties: list[str]
    follow_up_questions: list[str]
    models_used: ModelsUsed
