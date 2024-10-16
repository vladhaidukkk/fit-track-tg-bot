from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.db.queries import update_user


class UsageStatsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, any]], Awaitable[any]],
        event: Update,
        data: dict[str, any],
    ) -> any:
        user = data.get("user")
        if user:
            data["user"] = await update_user(id_=user.id, event_count=user.event_count + 1)
        return await handler(event, data)
