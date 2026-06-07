# Local Install Guide

## Prerequisites

- Git
- Docker Engine with Docker Compose
- OpenAI API key
- Gemini API key
- Node and Python only if running local development without Docker

Docker Engine with Docker Compose is the primary supported runtime. Podman may work, but it is not the primary validation target.

## Docker Install Path

```bash
git clone <repo-url>
cd mythadis-consensus-engine
cp .env.example .env
# edit .env and add backend provider keys
docker compose up --build
```

Open:

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/health`

Stop the stack:

```bash
docker compose down
```

## Local Development Path

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run test -- --run
npm run build
npm run dev
```

## Verifying Install

1. Visit `http://localhost:8000/health`.
2. Confirm the response includes `status: ok`.
3. Visit `http://localhost:5173`.
4. Ask a sample question:

   ```text
   What are the risks of relying on a single AI answer?
   ```

5. Confirm the result displays final answer, agreement, disagreement, uncertainty, follow-ups, primary answer, reviewer critique, and models used.
6. Click `Export Markdown` and confirm a `.md` report downloads.

## Common Issues

### Missing API Key Error

If the UI shows a missing API key error, confirm:

- You copied `.env.example` to `.env`.
- You added provider keys to `.env`.
- Docker Compose was restarted after editing `.env`.
- Provider keys are not placed in frontend env files.

### Gemini Model Error

The default Gemini model is:

```env
GEMINI_MODEL=gemini-2.5-flash
```

If Gemini reports a model error, verify the model name in `.env` against current Gemini provider documentation.

### Docker/Podman Confusion

Docker Engine with Docker Compose is the primary supported runtime. Podman can emulate Docker on some systems, but behavior can differ, especially around networking, storage, and compose compatibility.

### Port Conflict

The app expects:

- Backend: `8000`
- Frontend: `5173`

If either port is already in use, stop the conflicting process or adjust local tooling before starting the app.
