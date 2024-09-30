from aiogram import F
from aiogram.types import Message

from bot.keyboards.reply.root import root_keyboard
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter

from .states import LeaveSuggestionStates

state_router = SurveyStateRouter(LeaveSuggestionStates.suggestion)


@state_router.message(F.text)
async def suggestion_handler(message: Message, survey: SurveyContext) -> None:
    await survey.clear_messages(bot=message.bot, chat_id=message.chat.id, subset=slice(2, -1))
    await survey.state.clear()

    # TODO: send suggestion (message.text) somewhere.

    await message.answer(
        (
            "😁 Дуже дякую за ваше побажання! "
            "Постараюся якомога швидше втілити його в реальність, щоб стати вам більш корисним."
        ),
        reply_markup=root_keyboard(user_id=message.from_user.id),
    )


@state_router.message()
async def invalid_suggestion_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Опис повиннен бути текстовим. Введіть його ще раз:")
    await survey.add_messages_to_delete(sent_message.message_id)
