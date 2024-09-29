from aiogram import F
from aiogram.types import Message

from bot.keyboards.inline.biological_gender import biological_gender_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.regexps import int_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter

from .prompts import BIOLOGICAL_GENDER_PROMPT, HEIGHT_PROMPT
from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.age)


@state_router.message(F.text.regexp(int_regexp))
async def age_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)

    await survey.state.update_data(age=int(message.text))
    await survey.state.set_state(CalcCaloriesStates.height)

    sent_message = await message.answer(HEIGHT_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message(F.text == SurveyKeyboardText.PREV_STEP)
async def prev_step_age_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)
    await survey.clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        group_names=[CalcCaloriesStates.biological_gender.state, CalcCaloriesStates.age.state],
    )

    await survey.state.update_data(biological_gender=None)
    await survey.state.set_state(CalcCaloriesStates.biological_gender)

    sent_message = await message.answer(BIOLOGICAL_GENDER_PROMPT, reply_markup=biological_gender_keyboard())
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message()
async def invalid_age_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Вік повинен бути цілим числом. Введіть його ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
