from aiogram import F
from aiogram.types import Message

from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.regexps import float_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.parse_utils import parse_float

from .prompts import FIRST_DRY_MASS_PROMPT, TOTAL_READY_MASS_PROMPT
from .states import CalcFoodAllocationStates

state_router = SurveyStateRouter(CalcFoodAllocationStates.second_dry_mass)


@state_router.message(F.text.regexp(float_regexp))
async def second_dry_mass_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)

    await survey.state.update_data(second_dry_mass=parse_float(message.text))
    await survey.state.set_state(CalcFoodAllocationStates.total_ready_mass)

    sent_message = await message.answer(TOTAL_READY_MASS_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message(F.text == SurveyKeyboardText.UNDO_PREV_STEP)
async def undo_second_dry_mass_handler(message: Message, survey: SurveyContext) -> None:
    await survey.clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        group_name=CalcFoodAllocationStates.first_dry_mass.state,
    )
    await survey.add_messages_to_delete(message.message_id)
    await survey.clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        group_name=CalcFoodAllocationStates.second_dry_mass.state,
    )

    await survey.state.update_data(first_dry_mass=None)
    await survey.state.set_state(CalcFoodAllocationStates.first_dry_mass)

    sent_message = await message.answer(FIRST_DRY_MASS_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)
