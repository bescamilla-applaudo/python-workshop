from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PYFORGE_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    data_dir: str = "data"
    output_format: str = "json"
    max_results: int = 100
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
