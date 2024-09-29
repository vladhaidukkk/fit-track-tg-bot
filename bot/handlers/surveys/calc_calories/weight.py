from aiogram import F
from aiogram.types import Message

from bot.keyboards.inline.fat_pct import fat_pct_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.regexps import float_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.parse_utils import parse_float

from .prompts import FAT_PCT_PROMPT, HEIGHT_PROMPT
from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.weight)


@state_router.message(F.text.regexp(float_regexp))
async def weight_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)

    await survey.state.update_data(weight=parse_float(message.text))
    await survey.state.set_state(CalcCaloriesStates.fat_pct)

    sent_message = await message.answer(FAT_PCT_PROMPT, reply_markup=fat_pct_keyboard())
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message(F.text == SurveyKeyboardText.PREV_STEP)
async def prev_step_weight_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)
    await survey.clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        group_names=[CalcCaloriesStates.height.state, CalcCaloriesStates.weight.state],
    )

    await survey.state.update_data(height=None)
    await survey.state.set_state(CalcCaloriesStates.height)

    sent_message = await message.answer(HEIGHT_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message()
async def invalid_weight_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Вага повинна бути числом. Введіть її ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
