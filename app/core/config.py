from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./db/nutrition.db"
    debug: bool = True
    default_auth_token: str = "default-key-aCW5eV_VAL20k9MToEUOoFHQ2_DIXu80GxJYIkPSAIc"
    severity_alert_threshold: int = 7  # Auto-book appointment if >= this

settings = Settings()
