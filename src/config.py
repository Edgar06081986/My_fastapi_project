from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field  # Updated import

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    db_echo: bool = True

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:  # Replaced SettingsConfigDict with Config
        env_file = BASE_DIR / ".env.pg4.db"
        extra = "ignore"


class YandexCloudSettings(BaseSettings):
    api_v1_prefix_2: str = "/api/v1"
    ACCESS_KEY: str = Field(alias="YC_ACCESS_KEY")
    SECRET_KEY: str = Field(alias="YC_SECRET_KEY")

    class Config:  # Replaced SettingsConfigDict with Config
        env_file = BASE_DIR / ".env.pg4.yc"
        extra = "ignore"


# Инициализация настроек
settings: Settings = Settings()
yc_settings: YandexCloudSettings = YandexCloudSettings()
