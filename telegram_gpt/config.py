"""
App configs
"""

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Base variables for application
    """

    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    OPENAI_TEMPERATURE: float
    OPENAI_TOP_P: float
    OPENAI_PRESENCE_PENALTY: float
    OPENAI_FREQUENCY_PENALTY: float

    TELEGRAM_BOT_TOKEN: str

    class Config:
        """
        Settings parser settings
        """

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()


@lru_cache
def get_openai_request_settings() -> dict[str, str | int]:
    """
    Collect OpenAI request settings from env variables

    Returns:
        dict[str, str | int]: OpenAI settings dict
    """
    return {
        "model": settings.OPENAI_MODEL,
        "temperature": settings.OPENAI_TEMPERATURE,
        "top_p": settings.OPENAI_TOP_P,
        "presence_penalty": settings.OPENAI_PRESENCE_PENALTY,
        "frequency_penalty": settings.OPENAI_FREQUENCY_PENALTY,
    }
