from pathlib import Path

from app.config import Settings


REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_SOURCE = REPO_ROOT / "frontend" / "src"
PROVIDER_KEY_NAMES = ("OPENAI_API_KEY", "GEMINI_API_KEY")
DATABASE_DEPENDENCIES = (
    "sqlalchemy",
    "psycopg",
    "psycopg2",
    "asyncpg",
    "sqlite",
    "alembic",
)


def test_env_example_uses_safe_placeholders_and_current_gemini_default() -> None:
    env_example = (REPO_ROOT / ".env.example").read_text()

    assert 'APP_NAME="Mythadis Consensus Engine"' in env_example
    assert "OPENAI_API_KEY=\n" in env_example
    assert "GEMINI_API_KEY=\n" in env_example
    assert "OPENAI_MODEL=gpt-4.1-mini" in env_example
    assert "GEMINI_MODEL=gemini-2.5-flash" in env_example
    assert "sk-" not in env_example


def test_frontend_env_example_does_not_include_provider_keys() -> None:
    env_example = (REPO_ROOT / "frontend" / ".env.example").read_text()

    assert "VITE_API_BASE_URL=http://localhost:8000" in env_example
    for key_name in PROVIDER_KEY_NAMES:
        assert key_name not in env_example


def test_gitignore_excludes_local_env_files() -> None:
    gitignore = (REPO_ROOT / ".gitignore").read_text()

    for pattern in [
        ".env",
        ".env.*",
        "!.env.example",
        "backend/.env",
        "backend/.env.*",
        "!backend/.env.example",
        "frontend/.env",
        "frontend/.env.*",
        "!frontend/.env.example",
    ]:
        assert pattern in gitignore


def test_docker_compose_backend_uses_env_and_frontend_has_no_provider_keys() -> None:
    compose = (REPO_ROOT / "docker-compose.yml").read_text()

    assert "env_file:" in compose
    assert "- .env" in compose
    assert "- .env.example" not in compose

    frontend_block = compose.split("  frontend:", maxsplit=1)[1]
    for key_name in PROVIDER_KEY_NAMES:
        assert key_name not in frontend_block


def test_backend_settings_load_provider_keys_from_environment() -> None:
    settings = Settings(
        _env_file=None,
        openai_api_key="sk-test-secret",
        gemini_api_key="gemini-test-secret",
    )

    assert settings.openai_api_key == "sk-test-secret"
    assert settings.gemini_api_key == "gemini-test-secret"


def test_frontend_source_does_not_reference_provider_key_names() -> None:
    frontend_files = [
        path for path in FRONTEND_SOURCE.rglob("*") if path.is_file() and path.suffix in {".ts", ".tsx"}
    ]

    for path in frontend_files:
        content = path.read_text()
        for key_name in PROVIDER_KEY_NAMES:
            assert key_name not in content, f"{key_name} found in {path.relative_to(REPO_ROOT)}"


def test_no_database_dependencies_are_introduced() -> None:
    requirements = (REPO_ROOT / "backend" / "requirements.txt").read_text().lower()

    for dependency in DATABASE_DEPENDENCIES:
        assert dependency not in requirements


def test_docs_state_no_prompt_or_result_storage() -> None:
    readme = (REPO_ROOT / "README.md").read_text().lower()
    security = (REPO_ROOT / "docs" / "security.md").read_text().lower()

    assert "no prompt/result history" in readme or "no prompt history" in readme
    assert "no prompt storage or result storage" in security
    assert "does not store exported reports" in security
