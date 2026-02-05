from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Pilues"
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    debug: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"  # <-- allows extra keys like APP_NAME and DEBUG in .env


settings = Settings()
