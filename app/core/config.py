from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_TITLE: str = "Simple Books library"
    SQLALCHEMY_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
