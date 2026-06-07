import json
from collections.abc import Callable
from typing import Any

from app.config import Settings
from app.llm.base import BaseLLMProvider
from app.llm.prompts import (
    build_primary_prompt,
    build_reviewer_prompt,
    build_synthesis_prompt,
)
from app.llm.provider_factory import get_provider
from app.schemas import ConsensusRequest, ConsensusResponse, ModelsUsed


StructuredSynthesis = dict[str, str | list[str]]
ProviderFactory = Callable[[str, Settings], BaseLLMProvider]


class ConsensusService:
    def __init__(
        self,
        settings: Settings,
        provider_factory: ProviderFactory = get_provider,
    ) -> None:
        self._settings = settings
        self._provider_factory = provider_factory

    def run(self, request: ConsensusRequest) -> ConsensusResponse:
        primary_provider = self._provider_factory(request.primary_provider, self._settings)
        reviewer_provider = self._provider_factory(request.reviewer_provider, self._settings)
        synthesizer_provider = self._provider_factory(request.synthesizer_provider, self._settings)

        primary_prompt = build_primary_prompt(request.question)
        primary_answer = primary_provider.generate(primary_prompt)

        reviewer_prompt = build_reviewer_prompt(request.question, primary_answer)
        reviewer_critique = reviewer_provider.generate(reviewer_prompt)

        synthesis_prompt = build_synthesis_prompt(
            request.question,
            primary_answer,
            reviewer_critique,
        )
        synthesis_output = synthesizer_provider.generate(synthesis_prompt)
        structured = parse_synthesis_output(synthesis_output)

        return ConsensusResponse(
            question=request.question,
            primary_answer=primary_answer,
            reviewer_critique=reviewer_critique,
            final_answer=str(structured["final_answer"]),
            agreement_points=_as_string_list(structured["agreement_points"]),
            disagreement_points=_as_string_list(structured["disagreement_points"]),
            uncertainties=_as_string_list(structured["uncertainties"]),
            follow_up_questions=_as_string_list(structured["follow_up_questions"]),
            models_used=ModelsUsed(
                primary=_provider_label(primary_provider, request.primary_provider),
                reviewer=_provider_label(reviewer_provider, request.reviewer_provider),
                synthesizer=_provider_label(synthesizer_provider, request.synthesizer_provider),
            ),
        )


def parse_synthesis_output(output: str) -> StructuredSynthesis:
    parsed = _load_synthesis_json(output)

    if not isinstance(parsed, dict):
        return _invalid_synthesis_fallback(output)

    return {
        "final_answer": _as_string(parsed.get("final_answer", "")),
        "agreement_points": _as_string_list(parsed.get("agreement_points", [])),
        "disagreement_points": _as_string_list(parsed.get("disagreement_points", [])),
        "uncertainties": _as_string_list(parsed.get("uncertainties", [])),
        "follow_up_questions": _as_string_list(parsed.get("follow_up_questions", [])),
    }


def _load_synthesis_json(output: str) -> Any:
    for candidate in _json_candidates(output):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    return None


def _json_candidates(output: str) -> list[str]:
    stripped = output.strip()
    candidates = [stripped]

    if stripped.startswith("```") and stripped.endswith("```"):
        lines = stripped.splitlines()
        candidates.append("\n".join(lines[1:-1]).strip())

    object_start = stripped.find("{")
    object_end = stripped.rfind("}")
    if object_start != -1 and object_end > object_start:
        candidates.append(stripped[object_start : object_end + 1])

    return candidates


def _invalid_synthesis_fallback(output: str) -> StructuredSynthesis:
    return {
        "final_answer": output,
        "agreement_points": [],
        "disagreement_points": [],
        "uncertainties": ["The synthesizer did not return valid structured JSON."],
        "follow_up_questions": [],
    }


def _as_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _provider_label(provider: BaseLLMProvider, fallback: str) -> str:
    model_name = getattr(provider, "model_name", "")
    if model_name:
        return str(model_name)

    provider_name = getattr(provider, "provider_name", "")
    if provider_name:
        return str(provider_name)

    return fallback
