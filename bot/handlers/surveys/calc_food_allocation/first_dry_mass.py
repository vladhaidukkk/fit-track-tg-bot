from aiogram import F
from aiogram.types import Message

from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.regexps import float_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.parse_utils import parse_float

from .prompts import SECOND_DRY_MASS_PROMPT
from .states import CalcFoodAllocationStates

state_router = SurveyStateRouter(CalcFoodAllocationStates.first_dry_mass)


@state_router.message(F.text.regexp(float_regexp))
async def first_dry_mass_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)

    await survey.state.update_data(first_dry_mass=parse_float(message.text))
    await survey.state.set_state(CalcFoodAllocationStates.second_dry_mass)

    sent_message = await message.answer(SECOND_DRY_MASS_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message(F.text == SurveyKeyboardText.UNDO_PREV_STEP)
async def undo_first_dry_mass_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer(
        "⚠️ Перший етап не може бути відмінено. Якщо ви хочете скасувати дію, натисніть відповідну кнопку."
    )
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
