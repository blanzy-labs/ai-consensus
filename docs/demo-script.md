# Demo Script

Suggested demo question:

```text
What are the risks of relying on a single AI answer?
```

Do not include real API keys in the demo. Hide `.env` before recording or screen sharing.

## Short Non-Technical Demo, 60-90 Seconds

Audience: readers, general audience, non-technical followers.

### Flow

1. Introduce the problem: one AI answer can sound confident.
2. Introduce Mythadis Consensus Engine.
3. Show one question.
4. Show primary answer, reviewer critique, and final synthesis.
5. Show uncertainty and follow-up questions.
6. Export Markdown.
7. Close with the tagline.

### Spoken Script Draft

> One AI answer can sound confident, even when it is incomplete or wrong.
>
> Mythadis Consensus Engine is a small open-source experiment from Mythadis Labs. You ask a question, one AI answers, another reviews that answer, and a final synthesis highlights agreement, disagreement, and uncertainty.
>
> For this demo, I will ask: "What are the risks of relying on a single AI answer?"
>
> Here is the primary answer. Now the reviewer critique points out gaps, weak claims, and missing context. The final synthesis pulls both together into a structured result.
>
> The most important part is not just the final answer. It is the uncertainty, the caveats, and the follow-up questions that help a human decide what to verify next.
>
> Finally, I can export the visible result as a local Markdown report. Nothing is stored by the app.
>
> The books are fiction. The questions are real.

### Screen Capture Checklist

- Frontend title and tagline
- Question field
- Provider selectors
- Loading state
- Final answer
- Agreement/disagreement/uncertainty sections
- Export Markdown button
- Downloaded `.md` file

## Technical Walkthrough, 5-8 Minutes

Audience: developers, LinkedIn tech people, GitHub visitors.

### Flow

1. Project purpose
2. Architecture
3. `.env` / backend-only key handling
4. Docker startup
5. Provider selectors
6. Consensus workflow
7. Prompt design
8. Markdown export
9. Security/privacy boundaries
10. How to contribute

### Spoken Script Draft

> Mythadis Consensus Engine is a local-first open-source consensus tool. It is designed around a simple idea: instead of treating one model answer as final, route the answer through a reviewer and a synthesizer.
>
> The architecture is intentionally small. The React/Vite frontend talks only to the FastAPI backend. The backend owns provider calls, prompt construction, and safe error handling. The frontend never receives OpenAI or Gemini API keys.
>
> Local secrets live in `.env`, which is ignored by git. Docker Compose loads that `.env` file for the backend. The frontend only receives `VITE_API_BASE_URL`.
>
> To start the app, copy `.env.example` to `.env`, add backend provider keys, and run `docker compose up --build`.
>
> In the UI, the user enters a question and selects providers for the primary responder, reviewer, and synthesizer. Today the supported providers are OpenAI and Gemini.
>
> The backend runs three prompt stages: primary answer, reviewer critique, and final synthesis. The synthesis prompt requests JSON so the frontend can display final answer, agreement points, disagreement points, uncertainties, and follow-up questions.
>
> The prompt design tries to avoid artificial debate. The reviewer is a quality reviewer, not an opponent. The prompts emphasize uncertainty, no fake citations, no unsupported certainty, and a reminder that consensus does not guarantee truth.
>
> After the result appears, the frontend can export a Markdown report. That export is generated locally in the browser from the current visible result. There is no server-side report storage and no prompt history.
>
> Security-wise, this is not an offline or private LLM. Questions and generated answers are sent to the configured providers. The app is explicit about that boundary, and contributors should preserve it.
>
> Contributions are welcome, especially small focused fixes, documentation improvements, and careful prompt improvements that preserve objectivity and the synthesis JSON contract.

### Screen Capture Checklist

- Repository README quick start
- `.env.example`, without showing real `.env`
- `docker compose up --build`
- Backend health endpoint
- Frontend provider selectors
- A full consensus run
- Prompt design document
- Markdown export
- Security document
- CONTRIBUTING.md and issue templates
