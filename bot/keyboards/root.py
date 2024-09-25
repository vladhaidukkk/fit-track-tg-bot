from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class RootKeyboardText(StrEnum):
    CALC_CPFC = "🍏 Розрахувати КБЖВ"
    CALC_PFC = "🍎 Розрахувати БЖВ"
    LEAVE_FEEDBACK = "💬 Залишити побажання"


def root_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=RootKeyboardText.CALC_CPFC), KeyboardButton(text=RootKeyboardText.CALC_PFC)],
            [KeyboardButton(text=RootKeyboardText.LEAVE_FEEDBACK)],
        ],
        resize_keyboard=True,
        input_field_placeholder=None,
    )
