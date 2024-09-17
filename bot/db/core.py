from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.config import settings

engine = create_async_engine(
    settings.db.url,
    echo=settings.alchemy.echo,
    echo_pool=settings.alchemy.echo_pool,
    max_overflow=settings.alchemy.max_overflow,
)
session_factory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
