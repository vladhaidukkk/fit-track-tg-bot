from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseModel):
    name: str = "FitTrack Bot"
    token: str


class Settings(BaseSettings):
    bot: BotSettings

    model_config = SettingsConfigDict(env_nested_delimiter="__", env_ignore_empty=True)


settings = Settings(_env_file=(".env.example", ".env"))
