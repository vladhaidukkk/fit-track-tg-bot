from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown as md

from bot.keyboards.inline.biological_gender import BIOLOGICAL_GENDER_TO_DATA, BIOLOGICAL_GENDER_TO_TEXT
from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.dict_utils import get_key_by_value

from .prompts import AGE_PROMPT
from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.biological_gender)


@state_router.callback_query(F.data.in_(BIOLOGICAL_GENDER_TO_DATA.values()))
async def biological_gender_handler(callback_query: CallbackQuery, survey: SurveyContext) -> None:
    biological_gender = get_key_by_value(BIOLOGICAL_GENDER_TO_DATA, callback_query.data)
    await survey.state.update_data(biological_gender=biological_gender)
    await survey.state.set_state(CalcCaloriesStates.age)

    await callback_query.answer()
    icon, output = BIOLOGICAL_GENDER_TO_TEXT[biological_gender].split(maxsplit=1)
    await callback_query.message.edit_text(f"{icon} Ваша біологічна стать: {md.hbold(output)}")
    sent_message = await callback_query.message.answer(AGE_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message(F.text == SurveyKeyboardText.UNDO_PREV_STEP)
async def undo_biological_gender_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer(
        "⚠️ Перший етап не може бути відмінено. Якщо ви хочете скасувати дію, натисніть відповідну кнопку."
    )
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)


@state_router.message()
async def unknown_biological_gender_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Оберіть біологічну стать, натиснувши кнопку під повідомленням.")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
