from functools import lru_cache

from app.core import settings


@lru_cache
def get_settings() -> settings.Settings:
    return settings.Settings()
