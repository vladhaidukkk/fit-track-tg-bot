from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.enums import Gender

GENDER_TO_TEXT = {
    Gender.MALE: "🚹 Чоловік",
    Gender.FEMALE: "🚺 Жінка",
}

GENDER_TO_DATA = {
    Gender.MALE: "male_gender",
    Gender.FEMALE: "female_gender",
}


def gender_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=GENDER_TO_TEXT[gender], callback_data=GENDER_TO_DATA[gender])
                for gender in Gender
            ]
        ]
    )
