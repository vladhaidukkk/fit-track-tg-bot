from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.db.queries import add_user, get_user, update_user
from bot.utils.aiogram_utils import extract_user_from_update


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, any]], Awaitable[any]],
        event: Update,
        data: dict[str, any],
    ) -> any:
        tg_user = extract_user_from_update(event)
        if not tg_user:
            return await handler(event, data)

        user = await get_user(id_=tg_user.id)
        is_user_existing = user is not None

        if not user:
            user = await add_user(id_=tg_user.id, username=tg_user.username)
        elif user.username != tg_user.username:
            # Ensures the system remains up-to-date when a user changes their username.
            user = await update_user(id_=user.id, username=tg_user.username)

        data["user"] = user
        data["is_user_new"] = not is_user_existing
        return await handler(event, data)
