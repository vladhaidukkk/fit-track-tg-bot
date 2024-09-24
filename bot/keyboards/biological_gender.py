from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.core.enums import BiologicalGender

BIOLOGICAL_GENDER_TO_TEXT = {
    BiologicalGender.MALE: "🚹 Чоловік",
    BiologicalGender.FEMALE: "🚺 Жінка",
}

BIOLOGICAL_GENDER_TO_DATA = {
    BiologicalGender.MALE: "male_gender",
    BiologicalGender.FEMALE: "female_gender",
}


def biological_gender_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BIOLOGICAL_GENDER_TO_TEXT[biological_gender],
                    callback_data=BIOLOGICAL_GENDER_TO_DATA[biological_gender],
                )
                for biological_gender in BiologicalGender
            ]
        ]
    )
