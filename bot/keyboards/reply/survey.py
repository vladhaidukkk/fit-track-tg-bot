from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class SurveyKeyboardText(StrEnum):
    CANCEL = "🚫 Скасувати"


def survey_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=SurveyKeyboardText.CANCEL)]],
        resize_keyboard=True,
        input_field_placeholder=None,
    )
