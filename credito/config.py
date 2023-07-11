# """Settings module"""
import os
from functools import lru_cache
from pydantic import BaseSettings, Field

@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"

class EnvironmentSettings(BaseSettings):
    
    APP_NAME: str
    TEST_APP: int = Field(..., env="TEST_APP", cast=int)
    
    # DATABASE
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    DB_CONNECT_ARGS: dict = {}
    DB_ECHO: bool = False

    # API Parceiros
    CLIENT_ID: str
    CLIENT_SECRET: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 600

    # Redis
    CACHE_EXPIRATION_SECONDS: int = 300

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"

    @property
    def DB_URI(self) -> str:
        base_uri = f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"{base_uri}_test" if self.TEST_APP else base_uri

@lru_cache
def get_environment_variables():
    return EnvironmentSettings()

env = get_environment_variables()