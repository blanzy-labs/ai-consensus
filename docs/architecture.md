# Architecture

## Purpose

Mythadis Consensus Engine will help compare and synthesize AI responses. The planned product flow is:

1. User asks a question.
2. A primary model produces an answer.
3. A reviewer model critiques the answer.
4. A final synthesis identifies agreement, disagreement, and uncertainty.

## Current Backend Workflow

The backend exposes `/health` and `POST /consensus/run`. The frontend is a single-page React/Vite app that calls those endpoints from the browser.

The consensus endpoint runs a three-step prompt workflow:

1. Primary answer: select the configured primary provider and ask it for a clear answer with assumptions and uncertainty.
2. Reviewer critique: select the configured reviewer provider and ask it to act as an objective quality reviewer, not a debate opponent.
3. Final synthesis: select the configured synthesizer provider and ask it for a balanced final answer in structured JSON.

Provider selection uses the backend LLM provider factory. Supported provider identifiers are currently `openai` and `gemini`; the provider layer is designed so additional providers can be added later without changing the route contract.

Prompt templates are centralized in `backend/app/llm/prompts.py`. The synthesizer is prompted to return JSON containing `final_answer`, `agreement_points`, `disagreement_points`, `uncertainties`, and `follow_up_questions`. The backend parses that JSON into the response schema. If the synthesizer returns invalid JSON, the backend returns the raw synthesizer output as `final_answer`, leaves list fields empty, and records an uncertainty explaining that structured JSON was not returned.

The frontend now supports question submission, provider selection, loading states, error display, backend health checks, and result display. No Markdown export, authentication, database, prompt history, stored results, or mock AI product responses are implemented.

## Frontend Flow

The frontend has a small set of focused components:

- `StatusBanner` shows backend health as unknown, online, or unavailable.
- `QuestionForm` collects the user question and provider selections.
- `ModelSelector` renders the `openai` and `gemini` provider choices.
- `LoadingSteps` shows static workflow stages while the backend request is running.
- `ErrorMessage` displays safe API and network errors.
- `ResultPanel` displays the final answer, structured lists, primary answer, reviewer critique, and models used.

The frontend sends only the question and provider names to `POST /consensus/run`. It does not send or receive provider API keys. Results are displayed in the browser after the backend responds and are not stored by the app.

No Markdown export, authentication, database, prompt history, stored results, streaming, or websockets are implemented.
