from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.types import User as TgUser
from aiogram.types.update import UpdateTypeLookupError

from bot.db.queries import add_user, get_user, update_user


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, any]], Awaitable[any]],
        event: Update,
        data: dict[str, any],
    ) -> any:
        tg_user = self._get_tg_user(event)
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

    @staticmethod
    def _get_tg_user(update: Update) -> TgUser | None:
        try:
            return update.message.from_user
        except UpdateTypeLookupError:
            # TODO: log this as a warning, just to be aware that aiogram probably doesn't support a new event type.
            #  But 99.9% that this log won't appear as we use only available in aiogram features.
            return None
        except AttributeError:
            # TODO: log this scenario as a warning. Add event type to extras and maybe something else as well.
            return None
