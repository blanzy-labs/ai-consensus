from app.config import Settings


def test_config_loads_defaults_without_api_keys() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_name == "Mythadis Consensus Engine"
    assert settings.app_env == "development"
    assert settings.backend_host == "0.0.0.0"
    assert settings.backend_port == 8000
    assert settings.frontend_origin == "http://localhost:5173"
    assert settings.openai_api_key == ""
    assert settings.openai_model == "gpt-4.1-mini"
    assert settings.gemini_api_key == ""
    assert settings.gemini_model == "gemini-2.5-flash"
