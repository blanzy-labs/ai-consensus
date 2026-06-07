from app.config import Settings
from app.llm.base import (
    BaseLLMProvider,
    MissingProviderConfigError,
    ProviderError,
    ProviderRequestError,
)


class GeminiProvider(BaseLLMProvider):
    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.gemini_api_key
        self._model = settings.gemini_model

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self._model

    def generate(self, prompt: str) -> str:
        if not self._api_key:
            raise MissingProviderConfigError(
                "Gemini API key is not configured. Set GEMINI_API_KEY in your .env file."
            )

        try:
            import google.generativeai as genai

            genai.configure(api_key=self._api_key)
            model = genai.GenerativeModel(self._model)
            response = model.generate_content(prompt)
            text = getattr(response, "text", "")
            return str(text)
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderRequestError(
                "Gemini request failed. Check your API key, model name, and network connection."
            ) from exc
