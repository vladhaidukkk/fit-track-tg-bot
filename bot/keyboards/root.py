from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.config import settings


class RootKeyboardText(StrEnum):
    CALC_CPFC = "🥗 Розрахувати калорійність"
    CALC_PFC = "🍎 Розрахувати БЖВ"
    LEAVE_FEEDBACK = "💬 Залишити побажання"
    # For privileged users only.
    CALC_FOOD_ALLOCATION = "🍽️ Розрахувати розподіл їжі"


def root_keyboard(user_id: int | None = None) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=RootKeyboardText.CALC_CPFC),
                # KeyboardButton(text=RootKeyboardText.CALC_PFC),
            ],
            (
                [KeyboardButton(text=RootKeyboardText.CALC_FOOD_ALLOCATION)]
                if user_id in settings.bot.privileged_user_ids
                else []
            ),
            [KeyboardButton(text=RootKeyboardText.LEAVE_FEEDBACK)],
        ],
        resize_keyboard=True,
        input_field_placeholder=None,
    )
