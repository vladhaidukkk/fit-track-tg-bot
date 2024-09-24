from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.core.enums import ActivityRate

ACTIVITY_RATE_TO_TEXT = {activity_rate: str(activity_rate.value) for activity_rate in ActivityRate}

ACTIVITY_RATE_TO_DATA = {activity_rate: f"{activity_rate.name.lower()}_activity_rate" for activity_rate in ActivityRate}


def activity_rate_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ACTIVITY_RATE_TO_TEXT[activity_rate],
                    callback_data=ACTIVITY_RATE_TO_DATA[activity_rate],
                )
                for activity_rate in ActivityRate
            ]
        ]
    )
