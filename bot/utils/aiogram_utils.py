from aiogram.types import Update
from aiogram.types import User as TgUser
from aiogram.types.update import UpdateTypeLookupError


def extract_user_from_update(update: Update) -> TgUser | None:
    try:
        return update.event.from_user
    except UpdateTypeLookupError:
        # TODO: log this as a warning, just to be aware that aiogram probably doesn't support a new event type.
        #  But 99.9% that this log won't appear as we use only available in aiogram features.
        return None
    except AttributeError:
        # TODO: log this scenario as a warning. Add event type to extras and maybe something else as well.
        return None
