# Security and Privacy

## Secret Handling

Provider API keys are backend-only. The frontend must not receive OpenAI, Gemini, or other provider secrets.

Local secrets belong in `.env`, which is ignored by git. `.env.example` contains placeholder values only and is safe to commit. Docker Compose loads `.env` for the backend service.

The frontend receives only non-secret configuration such as `VITE_API_BASE_URL`. Frontend `.env` files must not contain provider API keys.

## Provider Data Flow

1. The user enters a question and provider selections in the browser.
2. The frontend sends the question and provider names to the backend.
3. The backend builds prompts and sends them to the selected LLM providers.
4. Provider responses return to the backend.
5. The backend returns the structured result or a safe error to the frontend.

No prompt storage or result storage is implemented in V1. No login, authentication, database, prompt history, telemetry, analytics, or saved results are implemented in V1.

## Export Data Flow

Markdown export happens locally in the browser from the result currently displayed on screen. The user controls the saved `.md` file.

Mythadis Consensus Engine does not store exported reports, maintain export history, or upload exported reports to the backend.

## Error Handling

API-facing errors must be safe and readable. They must not include API keys, authorization headers, raw request headers, raw secret environment values, `.env` contents, or provider stack traces.

Provider SDK exceptions should be wrapped in safe project errors before they reach API responses.

## Dependency Review

Keep dependencies minimal. Review dependency changes before accepting pull requests, especially provider SDK upgrades.

Useful periodic checks include:

- `pip list --outdated`
- `npm outdated`
- `pip-audit` before releases
- `npm audit` before releases

Do not commit lockfiles with suspicious or unexplained dependency changes. Pin or constrain versions where appropriate. Model and provider SDK behavior may change, so upgrades should be reviewed and tested.

## Limitations

Mythadis Consensus Engine is not a private or offline LLM system. User questions, prompts, and generated answers are sent to the configured providers for each run.

The app does not browse the web or perform hidden external research in V1. Consensus does not guarantee truth. Outputs may contain errors, omissions, or outdated information.

Do not use the app as the sole authority for safety-critical, medical, legal, or financial decisions.
