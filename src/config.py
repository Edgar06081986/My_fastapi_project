from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

  
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()




class YandexCloudSettings(BaseSettings):
    # Автоматически загружает переменные из .env или окружения
    YC_ACCESS_KEY: str
    YC_SECRET_KEY: str

    # Указываем, откуда читать конфиг (опционально, Pydantic ищет .env по умолчанию)
    model_config = SettingsConfigDict(env_file=".env", extra="forbid")

# Создаём инстанс конфига
config_yandex = YandexCloudSettings()