# Security and Privacy

## Secret Handling

Provider API keys are backend-only. The frontend must never receive OpenAI, Gemini, or other provider secrets.

Local secrets belong in `.env`, which is ignored by git. `.env.example` contains placeholder values only and is safe to commit.

Docker Compose loads `.env` for the backend service:

```yaml
services:
  backend:
    env_file:
      - .env
```

The frontend receives only non-secret configuration such as:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Do not put provider API keys in frontend env files.

## Provider Data Flow

Users bring their own provider keys. Provider terms and privacy policies apply to any data sent to those providers.

Runtime flow:

1. User enters a question and provider selections in the browser.
2. Frontend sends the question and provider names to the backend.
3. Backend builds prompts.
4. Backend sends prompts and intermediate outputs to the selected providers.
5. Provider responses return to the backend.
6. Backend returns a structured result or safe error to the frontend.

## No-Storage Default

V1 intentionally has:

- No user accounts
- No database
- No server-side prompt storage
- No server-side result storage
- No prompt/result history
- No telemetry
- No analytics

In short: no prompt storage or result storage is implemented in V1.

## Export Behavior

Markdown export is generated locally in the browser from the result currently displayed on screen. The user controls the downloaded report.

Mythadis Consensus Engine does not store exported reports, maintain export history, or upload exported reports to the backend.

Exported reports should be reviewed before sharing or relying on them.

## Error Handling

API-facing errors should be safe and readable.

They must not include:

- API keys
- Authorization headers
- Raw request headers
- Raw secret environment values
- `.env` contents
- Provider stack traces

Provider SDK exceptions are wrapped in safe project errors before reaching API responses.

## Dependency Review

Keep dependencies minimal. Review dependency changes before accepting pull requests, especially provider SDK upgrades.

Useful periodic checks:

```bash
pip list --outdated
npm outdated
```

Before releases, consider:

```bash
pip-audit
npm audit
```

Do not commit lockfiles with suspicious or unexplained dependency changes. Pin or constrain versions where appropriate. Provider SDK behavior and model names may change, so upgrades should be reviewed and tested.

## Limitations

Mythadis Consensus Engine is not a private or offline LLM system. It sends user questions, prompts, and generated answers to the configured providers for each run.

The app does not browse the web or perform hidden external research in V1.

Consensus does not guarantee truth. Outputs may contain errors, omissions, or outdated information.

Do not use the app as the sole authority for safety-critical, medical, legal, or financial decisions.
