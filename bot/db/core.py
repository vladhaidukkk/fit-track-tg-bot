from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar
from unittest.mock import MagicMock

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.config import settings

engine_kwargs = {
    "echo": settings.alchemy.echo,
    "echo_pool": settings.alchemy.echo_pool,
}
if not settings.db.url.startswith("sqlite"):
    # SQLite doesn't support max_overflow.
    engine_kwargs["max_overflow"] = settings.alchemy.max_overflow

engine = create_async_engine(settings.db.url, **engine_kwargs) if settings.db.enabled else MagicMock()
session_factory = (
    async_sessionmaker(engine, autoflush=False, expire_on_commit=False) if settings.db.enabled else MagicMock()
)

P = ParamSpec("P")
R = TypeVar("R")


def inject_session(fn: Callable[Concatenate[AsyncSession, P], R]) -> Callable[P, R]:
    @wraps(fn)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        async with session_factory() as session:
            return await fn(session, *args, **kwargs)

    return wrapper
