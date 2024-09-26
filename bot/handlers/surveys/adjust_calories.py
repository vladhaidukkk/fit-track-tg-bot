from aiogram import F, Router
from aiogram.types import Message

from bot.filters import PrivilegedUserFilter
from bot.keyboards.root import RootKeyboardText

router = Router(name=__name__)
router.message.filter(PrivilegedUserFilter())
router.callback_query.filter(PrivilegedUserFilter())


@router.message(F.text == RootKeyboardText.ADJUST_CALORIES)
async def adjust_calories_button_handler(message: Message) -> None:
    await message.answer("🔜 Ця функція буде доступна незабаром. Дякуємо за ваше терпіння! 💪")
