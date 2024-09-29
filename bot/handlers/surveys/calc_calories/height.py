from aiogram import F
from aiogram.types import Message

from bot.regexps import float_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.parse_utils import parse_float

from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.height)


@state_router.message(F.text.regexp(float_regexp))
async def height_handler(message: Message, survey: SurveyContext) -> None:
    await survey.state.update_data(height=parse_float(message.text))
    await survey.state.set_state(CalcCaloriesStates.weight)

    sent_message = await message.answer("⚖️ Вкажіть вашу вагу (в кілограмах):")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)


@state_router.message()
async def invalid_height_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Зріст повинен бути числом. Введіть його ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
