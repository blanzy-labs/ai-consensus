# Security

API keys are backend-only. The frontend must not receive OpenAI, Gemini, or other provider secrets.

`.env` files must not be committed. Use `.env.example` for placeholder configuration only.

When `/consensus/run` is used, the user's question and generated answers are sent to the configured LLM providers as part of the answer, review, and synthesis workflow. Users should only submit content they are comfortable sending to those providers.

Prompt templates are also sent to the configured providers with the user's question and intermediate model outputs. Mythadis Consensus Engine does not browse the web or perform hidden external research in V1.

No prompt storage or result storage is implemented in V1. No login, authentication, database, prompt history, or saved results are implemented in V1.

Provider errors returned by the API must be safe and must not include API keys, request headers, raw secret environment values, or provider stack traces.
