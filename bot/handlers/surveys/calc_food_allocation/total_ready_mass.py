from aiogram import F
from aiogram.types import Message

from bot.core.food_allocation_calculator import calc_food_allocation
from bot.keyboards.reply.root import root_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.regexps import float_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.format_utils import format_number
from bot.utils.message_utils import build_detailed_message
from bot.utils.parse_utils import parse_float

from .prompts import SECOND_DRY_MASS_PROMPT
from .states import CalcFoodAllocationStates

state_router = SurveyStateRouter(CalcFoodAllocationStates.total_ready_mass)


@state_router.message(F.text.regexp(float_regexp))
async def total_ready_mass_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)
    await survey.clear_messages(bot=message.bot, chat_id=message.chat.id, subset=slice(1, None))

    await survey.state.update_data(total_ready_mass=parse_float(message.text))
    data = await survey.state.get_data()
    await survey.state.clear()

    first_ready_mass, second_ready_mass = calc_food_allocation(
        first_dry_mass=data["first_dry_mass"],
        second_dry_mass=data["second_dry_mass"],
        total_ready_mass=data["total_ready_mass"],
    )
    await message.answer(
        build_detailed_message(
            details=[
                ("1️⃣ Першій особі", format_number(first_ready_mass, "г")),
                ("2️⃣ Другій особі", format_number(second_ready_mass, "г")),
            ],
            bold_detail_name=False,
            bold_detail_value=True,
        ),
        reply_markup=root_keyboard(user_id=message.from_user.id),
    )


@state_router.message(F.text == SurveyKeyboardText.UNDO_PREV_STEP)
async def undo_total_ready_mass_handler(message: Message, survey: SurveyContext) -> None:
    await survey.clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        group_name=CalcFoodAllocationStates.second_dry_mass.state,
    )
    await survey.add_messages_to_delete(message.message_id)
    await survey.clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        group_name=CalcFoodAllocationStates.total_ready_mass.state,
    )

    await survey.state.update_data(second_dry_mass=None)
    await survey.state.set_state(CalcFoodAllocationStates.second_dry_mass)

    sent_message = await message.answer(SECOND_DRY_MASS_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)
