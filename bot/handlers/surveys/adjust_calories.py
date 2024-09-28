from aiogram import F, Router
from aiogram.types import Message

from bot.filters import PrivilegedUserFilter
from bot.keyboards.reply.root import RootKeyboardText
from bot.survey.context import SurveyContext

router = Router(name=__name__)
router.message.filter(PrivilegedUserFilter())
router.callback_query.filter(PrivilegedUserFilter())


@router.message(F.text == RootKeyboardText.ADJUST_CALORIES)
async def adjust_calories_button_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("🔜 Ця функція буде доступна незабаром. Дякуємо за ваше терпіння! 💪")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
