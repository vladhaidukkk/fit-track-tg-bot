from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown as md
from aiogram.utils.chat_action import ChatActionSender

from bot.keyboards.inline.activity_rate import ACTIVITY_RATE_TO_DATA
from bot.keyboards.inline.biological_gender import BIOLOGICAL_GENDER_TO_TEXT
from bot.keyboards.inline.weight_target import weight_target_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.ai_utils import generate_text
from bot.utils.dict_utils import get_key_by_value
from bot.utils.format_utils import format_age, format_number
from bot.utils.message_utils import build_detailed_message
from bot.utils.string_utils import get_tail

from .prompts import WEIGHT_TARGET_PROMPT
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


@state_router.callback_query(F.data.in_(ACTIVITY_RATE_TO_DATA.values()))
async def amr_ai_query_amr_handler(callback_query: CallbackQuery, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(callback_query.message.message_id)
    await survey.clear_messages(bot=callback_query.bot, chat_id=callback_query.message.chat.id, subset=slice(2, None))

    amr = get_key_by_value(ACTIVITY_RATE_TO_DATA, callback_query.data)
    await survey.state.update_data(amr=amr)
    data = await survey.state.get_data()
    await survey.state.set_state(CalcCaloriesStates.weight_target)

    sent_message = await callback_query.message.answer(
        build_detailed_message(
            title="📋 Вхідні дані",
            details=[
                ("Біологічна стать", get_tail(BIOLOGICAL_GENDER_TO_TEXT[data["biological_gender"]])),
                ("Вік", format_age(data["age"])),
                ("Ріст", format_number(data["height"], "см")),
                ("Вага", format_number(data["weight"], "кг")),
                ("Відсоток жиру", format_number(data["fat_pct"], "%", sep="")),
                ("Коефіцієнт активності", format_number(data["amr"].value, precision=3)),
            ],
            footer=WEIGHT_TARGET_PROMPT,
            bold_detail_name=False,
            bold_detail_value=True,
        ),
        reply_markup=weight_target_keyboard(),
    )
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message()
async def invalid_amr_ai_query_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Опис повинен бути повідомленням. Введіть його ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
