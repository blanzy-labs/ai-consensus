# Architecture

## Purpose

Mythadis Consensus Engine will help compare and synthesize AI responses. The planned product flow is:

1. User asks a question.
2. A primary model produces an answer.
3. A reviewer model critiques the answer.
4. A final synthesis identifies agreement, disagreement, and uncertainty.

## Current Backend Workflow

The backend exposes `/health` and `POST /consensus/run`.

The consensus endpoint runs a three-step workflow:

1. Select the configured primary provider and ask it for an initial answer.
2. Select the configured reviewer provider and ask it to critique the primary answer.
3. Select the configured synthesizer provider and ask it for a final structured JSON result.

Provider selection uses the backend LLM provider factory. Supported provider identifiers are currently `openai` and `gemini`; the provider layer is designed so additional providers can be added later without changing the route contract.

The synthesizer is prompted to return JSON containing `final_answer`, `agreement_points`, `disagreement_points`, `uncertainties`, and `follow_up_questions`. The backend parses that JSON into the response schema. If the synthesizer returns invalid JSON, the backend returns the raw synthesizer output as `final_answer`, leaves list fields empty, and records an uncertainty explaining that structured JSON was not returned.

The frontend still displays the project shell and health status only. No frontend question form, Markdown export, authentication, database, prompt history, stored results, or mock AI product responses are implemented.
