# Architecture

## Purpose

Mythadis Consensus Engine is a lightweight, local-first, open-source consensus tool. It lets a user ask a question, route that question through multiple AI providers, and receive a structured result that highlights agreement, disagreement, uncertainty, and follow-up questions.

The app is intentionally small: no login, no database, no prompt history, no server-side result storage, no telemetry, and no analytics.

## High-Level Flow

```text
Frontend
  -> FastAPI backend
  -> Primary provider
  -> Reviewer provider
  -> Synthesizer provider
  -> Structured response
  -> Frontend display
  -> Browser-side Markdown export
```

## Components

### React/Vite Frontend

The frontend provides the single-page user interface:

- Backend health status
- Question input
- Provider selectors
- Loading state
- Safe error display
- Structured result display
- Browser-side Markdown export

The frontend calls only the local backend. It does not call OpenAI, Gemini, or other LLM providers directly.

### FastAPI Backend

The backend exposes:

- `GET /health`
- `POST /consensus/run`

It owns configuration, provider selection, prompt construction, provider API calls, synthesis parsing, and safe error handling.

### Provider Abstraction

The backend LLM layer exposes a small provider contract with a `generate(prompt: str) -> str` method. Provider identifiers are lowercase strings.

Currently supported providers:

- `openai`
- `gemini`

### OpenAI Provider

The OpenAI provider reads `OPENAI_API_KEY` and `OPENAI_MODEL` from backend settings and calls the configured OpenAI model.

Default model:

```text
gpt-4.1-mini
```

### Gemini Provider

The Gemini provider reads `GEMINI_API_KEY` and `GEMINI_MODEL` from backend settings and calls the configured Gemini model.

Default model:

```text
gemini-2.5-flash
```

### Consensus Service

The consensus service orchestrates the workflow:

1. Build primary prompt.
2. Call primary provider.
3. Build reviewer prompt.
4. Call reviewer provider.
5. Build synthesis prompt.
6. Call synthesizer provider.
7. Parse synthesis JSON.
8. Return a structured response.

### Prompt Builders

Prompt templates live in `backend/app/llm/prompts.py`.

The prompts are split into:

- Primary answer prompt
- Reviewer critique prompt
- Final synthesis prompt

The synthesis prompt asks for JSON only so the backend can return a stable response shape.

### Markdown Export Utility

Markdown export is implemented in the frontend. It builds a `.md` report from the currently visible consensus result and downloads it in the browser.

The export does not call the backend and does not store reports.

### Docker Compose

Docker Compose runs the backend and frontend together.

The backend service loads `.env`. The frontend receives only `VITE_API_BASE_URL`.

## Provider Boundary

```text
Browser
  -> local backend
      -> OpenAI / Gemini
```

The frontend never calls OpenAI or Gemini directly. Provider API keys remain backend-only and are loaded from `.env`.

The frontend sends:

- User question
- Provider selections

The frontend receives:

- Structured result
- Safe errors
- Backend health status

The frontend does not receive provider API keys.

## Data Flow

```text
User question
  -> frontend
  -> backend /consensus/run
  -> backend builds prompts
  -> backend sends prompt to primary provider
  -> backend sends answer to reviewer provider
  -> backend sends question + answer + critique to synthesizer provider
  -> backend parses synthesis JSON
  -> backend returns structured result
  -> frontend displays result
  -> optional browser-side Markdown export
```

No server-side prompt/result storage exists in V1.

## Failure Handling

- Missing provider keys return safe, readable errors.
- Unsupported providers return safe errors.
- Provider call failures are wrapped in safe errors.
- Invalid synthesis JSON does not crash the workflow.
- If synthesis JSON parsing fails, the raw synthesizer output becomes `final_answer`, list fields are empty, and an uncertainty explains that valid structured JSON was not returned.
- `/health` provides a simple backend readiness check.

## Diagrams

### Runtime Boundary

```text
+-------------------+       +-------------------+       +------------------+
| React/Vite UI     | ----> | FastAPI backend   | ----> | OpenAI / Gemini  |
| localhost:5173    |       | localhost:8000    |       | provider APIs    |
+-------------------+       +-------------------+       +------------------+
        |                           |
        |                           +-- reads .env provider keys
        +-- no provider keys
```

### Consensus Stages

```text
Question
  -> Primary answer
  -> Reviewer critique
  -> Final synthesis JSON
  -> Structured result
```

### Export

```text
Structured result in browser
  -> Export Markdown
  -> local .md download
```
