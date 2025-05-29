from pathlib import Path
import os
from pydantic_settings import BaseSettings
from pydantic import Field, BaseModel  # Updated import

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    db_echo: bool = True
    auth_jwt: AuthJWT = AuthJWT()

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


BOT_TOKEN = os.getenv("BOT_TOKEN")
# Инициализация настроек
settings: Settings = Settings()
yc_settings: YandexCloudSettings = YandexCloudSettings()
