from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.config import settings


class RootKeyboardText(StrEnum):
    CALC_CALORIES = "🥗 Розрахувати калорійність"
    LEAVE_SUGGESTION = "📮 Залишити побажання"
    # For admin users only.
    LIST_USERS = "👥 Список користувачів"
    # For privileged users only.
    CALC_FOOD_ALLOCATION = "🍽️ Розрахувати розподіл їжі"


def root_keyboard(user_id: int | None = None) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=RootKeyboardText.CALC_CALORIES)],
            [KeyboardButton(text=RootKeyboardText.LIST_USERS)] if user_id in settings.bot.admin_ids else [],
            (
                [KeyboardButton(text=RootKeyboardText.CALC_FOOD_ALLOCATION)]
                if user_id in settings.bot.privileged_user_ids
                else []
            ),
            [KeyboardButton(text=RootKeyboardText.LEAVE_SUGGESTION)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Виберіть дію...",
    )
