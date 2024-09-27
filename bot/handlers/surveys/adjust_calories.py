from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.filters import PrivilegedUserFilter
from bot.keyboards.root import RootKeyboardText
from bot.utils.survey_utils import add_messages_to_delete

router = Router(name=__name__)
router.message.filter(PrivilegedUserFilter())
router.callback_query.filter(PrivilegedUserFilter())


@router.message(F.text == RootKeyboardText.ADJUST_CALORIES)
async def adjust_calories_button_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("🔜 Ця функція буде доступна незабаром. Дякуємо за ваше терпіння! 💪")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])
