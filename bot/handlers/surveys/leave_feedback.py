from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.reply.root import RootKeyboardText
from bot.utils.survey_utils import add_messages_to_delete

router = Router(name=__name__)


@router.message(F.text == RootKeyboardText.LEAVE_FEEDBACK)
async def leave_feedback_button_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("🔜 Ця функція буде доступна незабаром. Дякуємо за ваше терпіння! 💪")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])
