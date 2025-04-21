from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env.db", extra="ignore")


class YandexCloudSettings(BaseSettings):
    ACCESS_KEY: str = Field(..., alias="YC_ACCESS_KEY")
    SECRET_KEY: str = Field(..., alias="YC_SECRET_KEY")

    model_config = SettingsConfigDict(env_file=".env.yc", extra="ignore")


# Инициализация настроек
settings = Settings()
yc_settings = YandexCloudSettings()

# print("DB URL:", settings.DATABASE_URL_asyncpg)
# print("YC Access Key:", yc_settings.ACCESS_KEY)
