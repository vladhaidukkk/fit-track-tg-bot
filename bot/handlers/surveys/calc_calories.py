from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.root import RootKeyboardText

router = Router(name=__name__)


@router.message(F.text == RootKeyboardText.CALC_CALORIES)
async def calc_calories_button_handler(message: Message) -> None:
    await message.answer("🙈 Я бачу, що ви хочете розрахувати калорії.")
