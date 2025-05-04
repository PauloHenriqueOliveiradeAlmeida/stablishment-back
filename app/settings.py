from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = ""
    database_collection: str = "stablishments_app"
    blockchain_difficulty: int = 6
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
