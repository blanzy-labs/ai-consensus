# Mythadis Consensus Engine

Ask a question. One AI answers, another reviews, and a final synthesis highlights agreement, disagreement, and uncertainty.

**The books are fiction. The questions are real.**

Mythadis Consensus Engine is the first open-source project from Mythadis Labs, a companion project connected to RC Blanzy's techno-thriller / speculative science fiction universe.

Mythadis Labs explores real-world questions raised by near-future fiction: AI trust, uncertainty, cybersecurity, speculative science, and the fragile relationship between human judgment and machine-generated answers.

## Mythadis Labs and the Books

Mythadis Consensus Engine is part of Mythadis Labs, an open-source companion project inspired by RC Blanzy's near-future fiction. The novels explore artificial intelligence, human judgment, cybersecurity, speculative science, and the systems people trust without fully understanding.

This tool is a small real-world experiment in one of those questions: what happens when one AI answer is reviewed by another before a human decides what to trust?

The books are fiction. The questions are real.

## Features

- OpenAI and Gemini provider support
- Three-stage consensus workflow
- Objective reviewer critique
- Structured final response
- Agreement, disagreement, uncertainty, and follow-up sections
- Local browser Markdown export
- Docker Compose support
- No login
- No database
- No prompt/result history in V1
- Bring-your-own API keys

## Screenshots

Screenshots will be added after the first public demo recording.

## Quick Start

```bash
git clone <repo-url>
cd mythadis-consensus-engine
cp .env.example .env
# edit .env and add provider keys
docker compose up --build
```

Open:

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/health`

Docker Engine with Docker Compose is the primary supported runtime. Podman may work, but it is not the primary validation target.

## Environment Variables

Root `.env` values:

```env
APP_NAME="Mythadis Consensus Engine"
APP_ENV=development
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_ORIGIN=http://localhost:5173

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
```

Provider keys go only in the backend/root `.env`. Do not put OpenAI, Gemini, or other provider keys in frontend env files. `.env` is ignored by git; `.env.example` contains placeholders only and is safe to commit.

If a provider reports a model-not-found or unsupported-model error, update `OPENAI_MODEL` or `GEMINI_MODEL` in `.env`.

## Local Development

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

The frontend uses `VITE_API_BASE_URL` for the backend URL:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Docker

```bash
cp .env.example .env
# edit .env with backend provider keys if needed
docker compose up --build
docker compose down
```

Docker Compose loads `.env` for the backend service. The frontend receives only non-secret configuration.

## Security and Privacy

See [docs/security.md](docs/security.md) for details.

Short version:

- API keys are backend-only.
- User prompts and generated responses are sent to configured providers.
- No prompt/result storage is implemented in V1.
- Markdown export is generated locally in the browser.
- Avoid submitting sensitive or private data unless you are comfortable sending it to the configured providers.

## Limitations

- Consensus does not guarantee truth.
- Models can hallucinate.
- Current facts may require independent verification.
- No web browsing or research mode exists in V1.
- This is not a substitute for professional medical, legal, financial, or safety-critical advice.

## Roadmap

- v0.1.0 Local Consensus MVP
- Optional additional providers
- Optional local model support
- Optional web-grounded research mode
- Prompt versioning
- Better model comparison controls

## Related Mythadis Labs Projects

Planned later projects may include:

- AI Debate Arena
- Guardian HomeScan
- Reality Drift Scanner
- Narrative Threat Mapper
- Signal Hunter

These are planned ideas and are not included in Mythadis Consensus Engine today.

## Documentation

- [Architecture](docs/architecture.md)
- [Security and privacy](docs/security.md)
- [Local install guide](docs/local-install.md)
- [Prompt design](docs/prompt-design.md)
- [Demo script](docs/demo-script.md)
- [Sample report](docs/sample-report.md)
- [Disclaimer](docs/disclaimer.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](LICENSE).

## Disclaimer

See [Disclaimer](docs/disclaimer.md)
