from aiogram import F, Router
from aiogram.types import Message

from bot.keyboards.reply.root import RootKeyboardText
from bot.survey.context import SurveyContext

router = Router(name=__name__)


@router.message(F.text == RootKeyboardText.LEAVE_FEEDBACK)
async def leave_feedback_button_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("🔜 Ця функція буде доступна незабаром. Дякуємо за ваше терпіння! 💪")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
