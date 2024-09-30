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

        existing_user = await get_user(id_=tg_user.id)
        if not existing_user:
            existing_user = await add_user(id_=tg_user.id, username=tg_user.username)
        elif existing_user.username != tg_user.username:
            # Ensures the system remains up-to-date when a user changes their username.
            await update_user(id_=existing_user.id, username=tg_user.username)

        data["user"] = existing_user
        return await handler(event, data)
