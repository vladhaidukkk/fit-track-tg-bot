from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.core.enums import ActivityRate

ACTIVITY_RATE_TO_TEXT = {activity_rate: str(activity_rate.value) for activity_rate in ActivityRate}

ACTIVITY_RATE_TO_DATA = {activity_rate: f"{activity_rate.name.lower()}_activity_rate" for activity_rate in ActivityRate}

ACTIVITY_RATE_HELP_DATA = "activity_rate_help"


def activity_rate_keyboard(*, show_help: bool = False) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ACTIVITY_RATE_TO_TEXT[activity_rate],
                    callback_data=ACTIVITY_RATE_TO_DATA[activity_rate],
                )
                for activity_rate in ActivityRate
            ],
            [InlineKeyboardButton(text="ℹ️ Допомога", callback_data=ACTIVITY_RATE_HELP_DATA)] if show_help else [],
        ]
    )
