from aiogram import F
from aiogram.types import Message

from bot.keyboards.inline.fat_pct import fat_pct_keyboard
from bot.regexps import float_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.parse_utils import parse_float

from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.weight)


@state_router.message(F.text.regexp(float_regexp))
async def weight_handler(message: Message, survey: SurveyContext) -> None:
    await survey.state.update_data(weight=parse_float(message.text))
    await survey.state.set_state(CalcCaloriesStates.fat_pct)

    sent_message = await message.answer("🍔 Вкажіть ваш відсоток жиру:", reply_markup=fat_pct_keyboard())
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)


@state_router.message()
async def invalid_weight_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Вага повинна бути числом. Введіть її ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
