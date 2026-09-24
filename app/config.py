"""Environment settings for local and container deployments."""

from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    """Database, upload and browser settings."""

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "twitter_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: SecretStr = SecretStr("postgres")
    ALLOW_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    MEDIA_DIR: Path = Path("static/media")
    MAX_UPLOAD_BYTES: int = 5 * 1024 * 1024
    SEED_DEMO: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def database_url(self, driver: str) -> URL:
        """Build a URL without interpreting special characters in passwords."""
        return URL.create(
            driver,
            username=self.DB_USER,
            password=self.DB_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


settings = Settings()
