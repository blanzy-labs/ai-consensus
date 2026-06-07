# Mythadis Consensus Engine

Mythadis Consensus Engine is an open-source companion project from Mythadis Labs. It will explore a simple consensus pattern where one AI answers a question, another AI reviews that answer, and a final synthesis is produced from agreement, disagreement, and uncertainty.

Current status: backend consensus workflow is available. The project has the foundation build, backend LLM provider layer, and a `/consensus/run` API endpoint that runs the three-step answer, review, and synthesis workflow.

The frontend question workflow is not implemented yet. Markdown export, login, database storage, prompt history, and saved results are also not implemented.

Prompt design has been hardened and documented in `docs/prompt-design.md`. The prompts emphasize objective review, uncertainty handling, no fake citations, and structured synthesis output.

## Local Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Verify the backend:

```bash
curl http://localhost:8000/health
```

Run a consensus request:

```bash
curl -X POST http://localhost:8000/consensus/run \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the risks of relying on one AI answer?",
    "primary_provider": "openai",
    "reviewer_provider": "gemini",
    "synthesizer_provider": "openai"
  }'
```

Real consensus calls require valid backend API keys for the selected providers. Tests use mocked providers and do not require real OpenAI or Gemini keys.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Docker Setup

From the repository root:

```bash
docker compose up --build
```

The backend runs at `http://localhost:8000` and the frontend runs at `http://localhost:5173`.

## Environment Variables

Copy `.env.example` to `.env` for local development and update values as needed.

API key values are included as placeholders only. Empty keys are allowed for local setup and tests, but real `/consensus/run` calls need valid keys for the selected providers.

## Security and Privacy

Do not commit `.env` files or real API keys. LLM provider keys remain backend-only and should never be exposed to the frontend.

No login, database, prompt storage, or result storage is implemented in this slice.
