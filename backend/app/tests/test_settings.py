from ..core.config import Settings


def test_settings_imports_with_pydantic_v2() -> None:
    settings = Settings()
    assert settings.APP_ENV
    assert settings.AUTO_CREATE_DB is False
