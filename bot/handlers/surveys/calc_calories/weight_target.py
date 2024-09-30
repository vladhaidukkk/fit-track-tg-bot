from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown as md

from bot.core.nutrition_calculator import calc_nutritional_profile
from bot.keyboards.inline.activity_rate import activity_rate_keyboard
from bot.keyboards.inline.biological_gender import BIOLOGICAL_GENDER_TO_TEXT
from bot.keyboards.inline.weight_target import WEIGHT_TARGET_TO_DATA, WEIGHT_TARGET_TO_TEXT
from bot.keyboards.reply.root import root_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.dict_utils import get_key_by_value
from bot.utils.format_utils import format_age, format_number, format_numbers_range
from bot.utils.message_utils import build_detailed_message
from bot.utils.string_utils import get_tail

from .prompts import AMR_PROMPT
from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.weight_target)


@state_router.callback_query(F.data.in_(WEIGHT_TARGET_TO_DATA.values()))
async def weight_target_handler(callback_query: CallbackQuery, survey: SurveyContext) -> None:
    await survey.clear_messages(
        bot=callback_query.bot,
        chat_id=callback_query.message.chat.id,
        exclude_message_ids=[callback_query.message.message_id],
        subset=slice(1, None),
    )

    weight_target = get_key_by_value(WEIGHT_TARGET_TO_DATA, callback_query.data)
    await survey.state.update_data(weight_target=weight_target)
    data = await survey.state.get_data()
    await survey.state.clear()

    await callback_query.answer()
    await callback_query.message.edit_text(
        build_detailed_message(
            title="📋 Вхідні параметри",
            details=[
                ("Біологічна стать", get_tail(BIOLOGICAL_GENDER_TO_TEXT[data["biological_gender"]])),
                ("Вік", format_age(data["age"])),
                ("Ріст", format_number(data["height"], "см")),
                ("Вага", format_number(data["weight"], "кг")),
                ("Відсоток жиру", format_number(data["fat_pct"], "%", sep="")),
                ("Коефіцієнт активності", format_number(data["amr"].value, precision=3)),
            ],
            footer=(
                "🎯 Нижче ви бачите рекомендовані поживні показники щоб "
                + md.hbold(get_tail(WEIGHT_TARGET_TO_TEXT[data["weight_target"]]).upper())
                + ", розраховані на основі вхідних даних."
            ),
            bold_detail_name=False,
            bold_detail_value=True,
        )
    )

    nutritional_profile = calc_nutritional_profile(
        gender=data["biological_gender"],
        age=data["age"],
        height=data["height"],
        weight=data["weight"],
        fat_pct=data["fat_pct"],
        amr=data["amr"],
        target=data["weight_target"],
    )
    min_calories, max_calories = nutritional_profile["calories"]
    min_carbohydrates, max_carbohydrates = nutritional_profile["carbohydrates"]
    min_fiber, max_fiber = nutritional_profile["fiber"]
    norm_sugar, max_sugar = nutritional_profile["sugar"]
    norm_caffeine, max_caffeine = nutritional_profile["caffeine"]

    await callback_query.message.answer(
        build_detailed_message(
            title="📊 Рекомендовані поживні показники",
            details=[
                ("Калорії", format_numbers_range(min_calories, max_calories, "ккал", precision=0)),
                ("Білки", format_number(nutritional_profile["proteins"], "г", precision=0)),
                ("Жири", format_number(nutritional_profile["fats"], "г", precision=0)),
                ("Вуглеводи", format_numbers_range(min_carbohydrates, max_carbohydrates, "г", precision=0)),
                ("Вода", format_number(nutritional_profile["water"], "л", precision=2)),
                ("Клітковина", format_numbers_range(min_fiber, max_fiber, "г")),
                ("Цукор", format_numbers_range(norm_sugar, max_sugar, "г")),
                ("Сіль", format_number(nutritional_profile["salt"], "г")),
                ("Кофеїн", format_numbers_range(norm_caffeine, max_caffeine, "мг", precision=0)),
            ],
            footer=(
                md.hbold("⚠️ Зверніть увагу: ")
                + "ці дані не є достовірно точними, оскільки вони залежать від індивідуальних особливостей вашого "
                + "організму. Використовуйте їх як відправну точку та коригуйте на основі ваших результатів."
            ),
            bold_detail_name=False,
            bold_detail_value=True,
        ),
        reply_markup=root_keyboard(user_id=callback_query.from_user.id),
    )
    # TODO: add a button to show detailed info (lbm, bmr, tef...).


@state_router.message(F.text == SurveyKeyboardText.PREV_STEP)
async def prev_step_weight_target_handler(message: Message, survey: SurveyContext) -> None:
    await survey.go_to_prev_step(
        bot=message.bot,
        chat_id=message.chat.id,
        prev_state=CalcCaloriesStates.amr,
        clear_prev_state_messages=True,
    )

    sent_message = await message.answer(AMR_PROMPT, reply_markup=activity_rate_keyboard(show_help=True))
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message()
async def unknown_weight_target_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Оберіть вашу мету, натиснувши кнопку під повідомленням.")
    await survey.add_messages_to_delete(sent_message.message_id)
