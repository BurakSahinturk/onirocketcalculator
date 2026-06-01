"""Is this where secrets lie?"""
# filename: config.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    pass

@lru_cache
def get_settings() -> Settings:
    return Settings()

MAX_FUEL_TANKS = 12
MAX_OXI_TANKS = 4
MAX_THRUSTERS = 10
MAX_EXTRA_MODULE_COUNT = 20

def weight_penalty_formula(mass: float) -> float:
    return max(mass, (mass / 300) ** 3.2) # formula is retreieved from https://forums.kleientertainment.com/forums/topic/96211-new-rocketry-mechanics/
