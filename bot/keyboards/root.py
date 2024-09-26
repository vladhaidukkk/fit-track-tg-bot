from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.config import settings


class RootKeyboardText(StrEnum):
    CALC_CALORIES = "🥗 Розрахувати калорійність"
    ADJUST_CALORIES = "📝 Підкоригувати калораж"
    LEAVE_FEEDBACK = "💬 Залишити побажання"
    # For privileged users only.
    CALC_FOOD_ALLOCATION = "🍽️ Розрахувати розподіл їжі"


def root_keyboard(user_id: int | None = None) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=RootKeyboardText.CALC_CALORIES),
                # KeyboardButton(text=RootKeyboardText.ADJUST_CALORIES),
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
