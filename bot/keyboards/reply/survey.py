from enum import StrEnum

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class SurveyKeyboardText(StrEnum):
    CANCEL = "🚫 Скасувати"
    PREV_STEP = "↩️ Назад"


def survey_keyboard(*, show_prev_step: bool = False) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text=SurveyKeyboardText.CANCEL)
    if show_prev_step:
        builder.button(text=SurveyKeyboardText.PREV_STEP)

    return builder.adjust(2).as_markup(resize_keyboard=True)
