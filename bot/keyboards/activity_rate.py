from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import settings
from bot.core.enums import ActivityRate

ACTIVITY_RATE_TO_TEXT = {activity_rate: str(activity_rate.value) for activity_rate in ActivityRate}

ACTIVITY_RATE_TO_DATA = {activity_rate: f"{activity_rate.name.lower()}_activity_rate" for activity_rate in ActivityRate}

ACTIVITY_RATE_HELP_DATA = "activity_rate_help"
ACTIVITY_RATE_AI_HELP_DATA = "activity_rate_ai_help"


def activity_rate_keyboard(*, show_help: bool = False, show_ai_help: bool = False) -> InlineKeyboardMarkup:
    help_buttons = []
    if show_help:
        help_buttons.append(InlineKeyboardButton(text="ℹ️ Допомога", callback_data=ACTIVITY_RATE_HELP_DATA))
    if show_ai_help and settings.openai.enabled:
        help_buttons.append(InlineKeyboardButton(text="️🤖 Допомога AI", callback_data=ACTIVITY_RATE_AI_HELP_DATA))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ACTIVITY_RATE_TO_TEXT[activity_rate],
                    callback_data=ACTIVITY_RATE_TO_DATA[activity_rate],
                )
                for activity_rate in ActivityRate
            ],
            help_buttons,
        ]
    )
