from openai.types import ChatModel
from pydantic import BaseModel, Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from bot.logger import LogLevelName


class BotSettings(BaseModel):
    name: str = "FitTrack Bot"
    token: str
    # TODO: This can be converted into a separate database column for scalability.
    privileged_user_ids: set[int] = set()


class DatabaseSettings(BaseModel):
    enabled: bool = True
    username: str
    password: str | None = None
    host: str
    port: int = Field(ge=1, le=65535)
    name: str

    @computed_field
    @property
    def url(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        ).unicode_string()


class AlchemySettings(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10


class OpenAISettings(BaseModel):
    enabled: bool = True
    api_key: str
    model: ChatModel
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
