from aiogram import F, Router
from aiogram.types import Message

from bot.keyboards.root import RootKeyboardText

router = Router(name=__name__)


@router.message(F.text == RootKeyboardText.CALC_FOOD_ALLOCATION)
async def calc_food_allocation_button_handler(message: Message) -> None:
    await message.answer("🔜 Ця функція буде доступна незабаром. Дякуємо за ваше терпіння! 💪")
