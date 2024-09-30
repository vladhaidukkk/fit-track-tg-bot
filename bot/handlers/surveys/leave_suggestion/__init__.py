from aiogram import F
from aiogram.types import Message

from bot.keyboards.reply.root import RootKeyboardText, root_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText, survey_keyboard
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyRouter

from .states import LeaveSuggestionStates
from .suggestion import state_router as suggestion_router

survey_router = SurveyRouter(LeaveSuggestionStates, to_delete_incoming_messages=True)
survey_router.include_state_routers(suggestion_router)


@survey_router.before_states.message(F.text == RootKeyboardText.LEAVE_SUGGESTION)
async def start_leave_suggestion_handler(message: Message, survey: SurveyContext) -> None:
    await survey.state.set_state(LeaveSuggestionStates.suggestion)
    prompt_message = await message.answer("✉️ Опишіть своє побажання:", reply_markup=survey_keyboard())
    await survey.add_messages_to_delete(prompt_message.message_id)


@survey_router.before_states.message(survey_router.all_states_filter, F.text == SurveyKeyboardText.CANCEL)
async def cancel_leave_suggestion_handler(message: Message, survey: SurveyContext) -> None:
    await survey.clear_messages(bot=message.bot, chat_id=message.chat.id, subset=slice(1, None))
    await survey.state.clear()
    await message.answer(
        "🚫 Процес залишення побажання скасовано.", reply_markup=root_keyboard(user_id=message.from_user.id)
    )
