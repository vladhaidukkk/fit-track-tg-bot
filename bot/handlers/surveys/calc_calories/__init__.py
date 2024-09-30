from aiogram import F
from aiogram.types import Message

from bot.keyboards.inline.biological_gender import biological_gender_keyboard
from bot.keyboards.reply.root import RootKeyboardText, root_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText, survey_keyboard
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyRouter

from .age import state_router as age_router
from .amr import state_router as amr_router
from .amr_ai_query import state_router as amr_ai_query_router
from .biological_gender import state_router as biological_gender_router
from .fat_pct import state_router as fat_pct_router
from .height import state_router as height_router
from .prompts import BIOLOGICAL_GENDER_PROMPT
from .states import CalcCaloriesStates
from .weight import state_router as weight_router
from .weight_target import state_router as weight_target_router

survey_router = SurveyRouter(CalcCaloriesStates, to_delete_incoming_messages=True)
survey_router.include_state_routers(
    biological_gender_router,
    age_router,
    height_router,
    weight_router,
    fat_pct_router,
    amr_router,
    amr_ai_query_router,
    weight_target_router,
)


@survey_router.before_states.message(F.text == RootKeyboardText.CALC_CALORIES)
async def start_calc_calories_handler(message: Message, survey: SurveyContext) -> None:
    start_message = await message.answer(
        "🥗 Розрахунок калорійності розпочато. Покроково вказуйте вхідні параметри для отримання результату.",
        reply_markup=survey_keyboard(show_prev_step=True),
    )
    await survey.add_messages_to_delete(start_message.message_id)

    await survey.state.set_state(CalcCaloriesStates.biological_gender)

    prompt_message = await message.answer(BIOLOGICAL_GENDER_PROMPT, reply_markup=biological_gender_keyboard())
    await survey.add_messages_to_delete(prompt_message.message_id)


@survey_router.before_states.message(survey_router.all_states_filter, F.text == SurveyKeyboardText.CANCEL)
async def cancel_calc_calories_handler(message: Message, survey: SurveyContext) -> None:
    await survey.clear_messages(bot=message.bot, chat_id=message.chat.id, subset=slice(1, None))
    await survey.state.clear()
    await message.answer(
        "🚫 Розрахунок калорійності скасовано.", reply_markup=root_keyboard(user_id=message.from_user.id)
    )
