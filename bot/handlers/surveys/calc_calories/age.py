from aiogram import F
from aiogram.types import Message

from bot.regexps import int_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter

from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.age)


@state_router.message(F.text.regexp(int_regexp))
async def age_handler(message: Message, survey: SurveyContext) -> None:
    await survey.state.update_data(age=int(message.text))
    await survey.state.set_state(CalcCaloriesStates.height)

    sent_message = await message.answer("📏 Вкажіть ваш зріст (в сантиметрах):")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)


@state_router.message()
async def invalid_age_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Вік повинен бути цілим числом. Введіть його ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
