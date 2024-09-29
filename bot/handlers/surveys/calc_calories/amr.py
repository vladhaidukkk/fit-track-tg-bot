from aiogram import F
from aiogram.types import CallbackQuery, Message

from bot.core.enums import ActivityRate
from bot.keyboards.inline.activity_rate import (
    ACTIVITY_RATE_AI_HELP_DATA,
    ACTIVITY_RATE_HELP_DATA,
    ACTIVITY_RATE_TO_DATA,
    activity_rate_keyboard,
)
from bot.keyboards.inline.biological_gender import BIOLOGICAL_GENDER_TO_TEXT
from bot.keyboards.inline.fat_pct import fat_pct_keyboard
from bot.keyboards.inline.weight_target import weight_target_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.dict_utils import get_key_by_value
from bot.utils.format_utils import format_age, format_number
from bot.utils.message_utils import build_detailed_message
from bot.utils.string_utils import get_tail

from .prompts import AMR_AI_QUERY_PROMPT, FAT_PCT_PROMPT, WEIGHT_TARGET_PROMPT
from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.amr)


@state_router.callback_query(F.data.in_(ACTIVITY_RATE_TO_DATA.values()))
async def amr_handler(callback_query: CallbackQuery, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(callback_query.message.message_id)
    await survey.clear_messages(bot=callback_query.bot, chat_id=callback_query.message.chat.id, subset=slice(2, None))

    amr = get_key_by_value(ACTIVITY_RATE_TO_DATA, callback_query.data)
    await survey.state.update_data(amr=amr)
    data = await survey.state.get_data()
    await survey.state.set_state(CalcCaloriesStates.weight_target)

    sent_message = await callback_query.message.answer(
        build_detailed_message(
            title="📋 Вхідні дані",
            details=[
                ("Біологічна стать", get_tail(BIOLOGICAL_GENDER_TO_TEXT[data["biological_gender"]])),
                ("Вік", format_age(data["age"])),
                ("Ріст", format_number(data["height"], "см")),
                ("Вага", format_number(data["weight"], "кг")),
                ("Відсоток жиру", format_number(data["fat_pct"], "%", sep="")),
                ("Коефіцієнт активності", format_number(data["amr"].value, precision=3)),
            ],
            footer=WEIGHT_TARGET_PROMPT,
            bold_detail_name=False,
            bold_detail_value=True,
        ),
        reply_markup=weight_target_keyboard(),
    )
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.callback_query(F.data == ACTIVITY_RATE_HELP_DATA)
async def amr_help_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer()
    await callback_query.message.edit_text(
        build_detailed_message(
            title="ℹ️ Види активності та їх коефіцієнти",
            details=[
                (
                    f"Мінімальна активність (AMR: {ActivityRate.SEDENTARY.value})",
                    "сидячий спосіб життя, майже відсутня фізична активність, відсутність регулярних тренувань",
                ),
                (
                    f"Легка активність (AMR: {ActivityRate.LIGHTLY_ACTIVE.value})",
                    "малорухливий спосіб життя, легкі фізичні навантаження, тренування 1-3 рази на тиждень",
                ),
                (
                    f"Середня активність (AMR: {ActivityRate.MODERATELY_ACTIVE.value})",
                    "активний спосіб життя, тренування 3-5 разів на тиждень",
                ),
                (
                    f"Висока активність (AMR: {ActivityRate.VERY_ACTIVE.value})",
                    "щоденні тренування, інтенсивні спортивні заняття, важка фізична робота",
                ),
                (
                    f"Дуже висока активність (AMR: {ActivityRate.EXTRA_ACTIVE.value})",
                    "тренування двічі на день, професійний спорт, дуже важка фізична праця",
                ),
            ],
            footer="🏃 Оберіть коефіцієнт активності, що найбільше відповідає вашому способу життя, натиснувши кнопку.",
            numerate_details=True,
            details_sep="\n\n",
            italic_footer=False,
        ),
        reply_markup=activity_rate_keyboard(show_ai_help=True),
    )


@state_router.callback_query(F.data == ACTIVITY_RATE_AI_HELP_DATA)
async def amr_ai_help_handler(callback_query: CallbackQuery, survey: SurveyContext) -> None:
    await survey.state.set_state(CalcCaloriesStates.amr_ai_query)

    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=activity_rate_keyboard())
    sent_message = await callback_query.message.answer(AMR_AI_QUERY_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message(F.text == SurveyKeyboardText.PREV_STEP)
async def prev_step_amr_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)
    await survey.go_to_prev_step(
        bot=message.bot,
        chat_id=message.chat.id,
        prev_state=CalcCaloriesStates.fat_pct,
        clear_prev_state_messages=True,
    )

    sent_message = await message.answer(FAT_PCT_PROMPT, reply_markup=fat_pct_keyboard())
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message()
async def unknown_amr_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Оберіть коефіцієнт активності, натиснувши кнопку під повідомленням.")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
