from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class SurveyKeyboardText(StrEnum):
    CANCEL = "🚫 Скасувати"
    UNDO_PREV_STEP = "↩️ Назад"


def survey_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=SurveyKeyboardText.CANCEL),
                KeyboardButton(text=SurveyKeyboardText.UNDO_PREV_STEP),
            ],
        ],
        resize_keyboard=True,
    )
