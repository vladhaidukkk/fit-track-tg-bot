from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.core.enums import WeightTarget

WEIGHT_TARGET_TO_TEXT = {
    WeightTarget.LOSE: "🏃 Схуднути",
    WeightTarget.MAINTAIN: "⚖️ Підтримувати вагу",
    WeightTarget.GAIN: "💪 Набрати вагу",
}

WEIGHT_TARGET_TO_DATA = {
    WeightTarget.LOSE: "lose_weight",
    WeightTarget.MAINTAIN: "maintain_weight",
    WeightTarget.GAIN: "gain_weight",
}


def weight_target_keyboard() -> InlineKeyboardMarkup:
    def build_button(weight_target: WeightTarget) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=WEIGHT_TARGET_TO_TEXT[weight_target],
            callback_data=WEIGHT_TARGET_TO_DATA[weight_target],
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [build_button(WeightTarget.MAINTAIN)],
            [build_button(WeightTarget.LOSE), build_button(WeightTarget.GAIN)],
        ]
    )
