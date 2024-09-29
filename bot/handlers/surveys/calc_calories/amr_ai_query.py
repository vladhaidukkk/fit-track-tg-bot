from aiogram import F
from aiogram.types import Message
from aiogram.utils import markdown as md
from aiogram.utils.chat_action import ChatActionSender

from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.ai_utils import generate_text

from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.amr_ai_query)


@state_router.message(F.text, F.text != SurveyKeyboardText.UNDO_PREV_STEP)
async def amr_ai_query_handler(message: Message, survey: SurveyContext) -> None:
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await survey.state.set_state(CalcCaloriesStates.amr)

        query = (
            "Будь ласка, визначте коефіцієнт активності (1.2, 1.375, 1.55, 1.725 або 1.9) для наступного опису: "
            f'"{message.text}".'
        )
        ai_response = await generate_text(query=query)
        sent_message = await message.answer(md.text(md.hbold("🤖 Відповідь AI:"), f'"{ai_response.rstrip(".")}".'))
        await survey.add_messages_to_delete(message.message_id, sent_message.message_id)


@state_router.message(F.text == SurveyKeyboardText.UNDO_PREV_STEP)
async def undo_amr_ai_query_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)
    await survey.clear_messages(
        bot=message.bot, chat_id=message.chat.id, group_names=[CalcCaloriesStates.amr_ai_query.state]
    )

    await survey.state.update_data(amr=None)
    await survey.state.set_state(CalcCaloriesStates.amr)


@state_router.message()
async def invalid_amr_ai_query_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Опис повинен бути повідомленням. Введіть його ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
