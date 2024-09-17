from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.db.queries.user import get_user


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, any]], Awaitable[any]],
        event: Update,
        data: dict[str, any],
    ) -> any:
        user_tg_id = self._get_user_tg_id_from_update(event)
        data["user"] = await get_user(id_=user_tg_id) if user_tg_id else None
        return await handler(event, data)

    @staticmethod
    def _get_user_tg_id_from_update(update: Update) -> int | None:
        if update.message:
            return update.message.from_user.id
        if update.callback_query:
            return update.callback_query.from_user.id
        # TODO: log this scenario as a warning to address the issue.
        return None
