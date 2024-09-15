from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class RootKeyboardText(StrEnum):
    CALC_CALORIES = "🍽️ Розрахувати калорії"


def root_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=RootKeyboardText.CALC_CALORIES)]],
        resize_keyboard=True,
        input_field_placeholder=None,
    )
