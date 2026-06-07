from app.config import Settings
from app.llm.base import (
    BaseLLMProvider,
    MissingProviderConfigError,
    ProviderError,
    ProviderRequestError,
)


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.openai_api_key
        self._model = settings.openai_model

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model_name(self) -> str:
        return self._model

    def generate(self, prompt: str) -> str:
        if not self._api_key:
            raise MissingProviderConfigError(
                "OpenAI API key is not configured. Set OPENAI_API_KEY in your .env file."
            )

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self._api_key)
            response = client.responses.create(model=self._model, input=prompt)
            text = getattr(response, "output_text", "")
            return str(text)
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderRequestError(
                "OpenAI request failed. Check your API key, model name, and network connection."
            ) from exc
