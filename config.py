from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс для хранения переменных окружения"""

    API_TOKEN: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()