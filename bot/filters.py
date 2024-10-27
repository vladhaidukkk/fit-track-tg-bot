from aiogram.filters import Filter
from aiogram.types import TelegramObject

from bot.config import settings


class AdminFilter(Filter):
    async def __call__(self, event: TelegramObject) -> bool:
        try:
            return event.from_user.id in settings.bot.admin_ids
        except AttributeError:
            # TODO: log this scenario as a warning. Add event type to extras and maybe something else as well.
            return False


class PrivilegedUserFilter(Filter):
    async def __call__(self, event: TelegramObject) -> bool:
        try:
            return event.from_user.id in settings.bot.privileged_user_ids
        except AttributeError:
            # TODO: log this scenario as a warning. Add event type to extras and maybe something else as well.
            return False
