from openai.types import ChatModel
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from bot.logger import LogLevelName


class BotSettings(BaseModel):
    name: str = "FitTrack Bot"
    token: str
    # TODO: These fields can be converted into separate database columns for scalability.
    suggestion_recipient_ids: frozenset[int] = frozenset()
    privileged_user_ids: frozenset[int] = frozenset()


class DatabaseSettings(BaseModel):
    enabled: bool = True
    url: str


class AlchemySettings(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10


class OpenAISettings(BaseModel):
    enabled: bool = True
    api_key: str
    model: ChatModel = "gpt-3.5-turbo"
    stub_responses: bool = False


class SentrySettings(BaseModel):
    dsn: str | None = None


class Settings(BaseSettings):
    log_level_name: LogLevelName = "INFO"

    bot: BotSettings
    db: DatabaseSettings
    alchemy: AlchemySettings = AlchemySettings()
    openai: OpenAISettings
    sentry: SentrySettings = SentrySettings()

    model_config = SettingsConfigDict(env_nested_delimiter="__", env_ignore_empty=True)


settings = Settings(_env_file=(".env.example", ".env"))
