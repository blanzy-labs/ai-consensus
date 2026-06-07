# Contributing

## Welcome

Thanks for your interest in Mythadis Consensus Engine. This project is a small, local-first open-source consensus tool from Mythadis Labs.

The V1 scope is intentionally narrow: no login, no database, no prompt/result history, no server-side storage, no telemetry, no analytics, no streaming, and no share links.

## Development Setup

Start with the [local install guide](docs/local-install.md).

## Branching

Use a feature branch for changes.

```text
feature/short-description
fix/short-description
docs/short-description
```

## Testing

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm run test -- --run
npm run build
```

Docker:

```bash
docker compose up --build
```

## Pull Request Expectations

- Keep changes small and focused.
- Include tests for behavior changes.
- Update docs when behavior or setup changes.
- Do not commit secrets.
- Do not add frontend provider keys.
- Respect the no-storage/no-login V1 scope.
- Note security or privacy impact when relevant.

## Prompt Contributions

Prompt improvements are welcome, especially when they improve clarity, uncertainty handling, and structured output reliability.

Prompt changes should preserve:

- Objectivity
- Uncertainty and limitation handling
- No fake citations
- No unsupported certainty
- No hidden chain-of-thought requests
- The synthesis JSON contract

## Security

Do not open public issues or pull requests containing API keys, `.env` contents, private prompts, sensitive user data, or provider credentials.

If a security concern involves sensitive details, keep the public issue minimal and do not paste secrets.
