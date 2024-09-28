from aiogram import F
from aiogram.types import Message

from bot.filters import PrivilegedUserFilter
from bot.keyboards.reply.root import RootKeyboardText, root_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText, survey_keyboard
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyRouter

from .first_dry_mass import state_router as first_dry_mass_router
from .prompts import FIRST_DRY_MASS_PROMPT
from .second_dry_mass import state_router as second_dry_mass_router
from .states import CalcFoodAllocationStates
from .total_ready_mass import state_router as total_ready_mass_router

survey_router = SurveyRouter(CalcFoodAllocationStates)
survey_router.message.filter(PrivilegedUserFilter())
survey_router.include_state_routers(first_dry_mass_router, second_dry_mass_router, total_ready_mass_router)


@survey_router.before_states.message(F.text == RootKeyboardText.CALC_FOOD_ALLOCATION)
async def start_calc_food_allocation_handler(message: Message, survey: SurveyContext) -> None:
    start_message = await message.answer(
        "🍽️ Розрахунок розподілу їжі розпочато. Покроково вказуйте вхідні дані для отримання результату.",
        reply_markup=survey_keyboard(),
    )
    await survey.add_messages_to_delete(message.message_id, start_message.message_id)

    await survey.state.set_state(CalcFoodAllocationStates.first_dry_mass)

    prompt_message = await message.answer(FIRST_DRY_MASS_PROMPT)
    await survey.add_messages_to_delete(prompt_message.message_id)


@survey_router.before_states.message(survey_router.all_states_filter, F.text == SurveyKeyboardText.CANCEL)
async def cancel_calc_food_allocation_handler(message: Message, survey: SurveyContext) -> None:
    await survey.clear_messages(bot=message.bot, chat_id=message.chat.id, subset=slice(1, None))
    await survey.state.clear()
    await message.answer(
        "🚫 Розрахунок розподілу їжі скасовано.", reply_markup=root_keyboard(user_id=message.from_user.id)
    )


@survey_router.after_states.message(survey_router.all_states_filter)
async def fallback_calc_food_allocation_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Вага повинна бути числом. Введіть її ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
