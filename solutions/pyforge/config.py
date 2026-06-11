from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    data_dir: str = "data"
    output_format: str = "json"
    max_results: int = 100
    debug: bool = False

    model_config = {
        "env_file": ".env",
        "env_prefix": "PYFORGE_",
        "case_sensitive": False,
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
