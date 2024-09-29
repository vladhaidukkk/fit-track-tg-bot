from aiogram import F
from aiogram.types import Message

from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.regexps import float_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.parse_utils import parse_float

from .prompts import AGE_PROMPT, WEIGHT_PROMPT
from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.height)


@state_router.message(F.text.regexp(float_regexp))
async def height_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)

    await survey.state.update_data(height=parse_float(message.text))
    await survey.state.set_state(CalcCaloriesStates.weight)

    sent_message = await message.answer(WEIGHT_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message(F.text == SurveyKeyboardText.UNDO_PREV_STEP)
async def undo_height_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)
    await survey.clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        group_names=[CalcCaloriesStates.age.state, CalcCaloriesStates.height.state],
    )

    await survey.state.update_data(age=None)
    await survey.state.set_state(CalcCaloriesStates.age)

    sent_message = await message.answer(AGE_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message()
async def invalid_height_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Зріст повинен бути числом. Введіть його ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
