from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.config import settings

engine = create_async_engine(
    settings.db.url,
    echo=settings.alchemy.echo,
    echo_pool=settings.alchemy.echo_pool,
    max_overflow=settings.alchemy.max_overflow,
)
session_factory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

P = ParamSpec("P")
R = TypeVar("R")


def inject_session(fn: Callable[Concatenate[AsyncSession, P], R]) -> Callable[P, R]:
    @wraps(fn)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        async with session_factory() as session:
            return await fn(session, *args, **kwargs)

    return wrapper
