from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

FAT_PCT_HELP_DATA = "fat_pct_help"


def fat_pct_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="ℹ️ Допомога", callback_data=FAT_PCT_HELP_DATA)]]
    )
