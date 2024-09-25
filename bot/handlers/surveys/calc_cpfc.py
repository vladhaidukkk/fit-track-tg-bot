from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown as md

from bot.core.enums import ActivityRate
from bot.core.nutrition_calculator import calc_nutritional_profile
from bot.keyboards.activity_rate import (
    ACTIVITY_RATE_AI_HELP_DATA,
    ACTIVITY_RATE_HELP_DATA,
    ACTIVITY_RATE_TO_DATA,
    activity_rate_keyboard,
)
from bot.keyboards.biological_gender import (
    BIOLOGICAL_GENDER_TO_DATA,
    BIOLOGICAL_GENDER_TO_TEXT,
    biological_gender_keyboard,
)
from bot.keyboards.root import RootKeyboardText
from bot.keyboards.weight_target import WEIGHT_TARGET_TO_DATA, WEIGHT_TARGET_TO_TEXT, weight_target_keyboard
from bot.utils.ai_utils import generate_text
from bot.utils.dict_utils import get_key_by_value
from bot.utils.format_utils import format_age, format_number, format_numbers_range
from bot.utils.message_utils import build_detailed_message
from bot.utils.string_utils import get_tail

router = Router(name=__name__)


class CalcCPFCSurvey(StatesGroup):
    biological_gender = State()
    age = State()
    height = State()
    weight = State()
    fat_pct = State()
    amr = State()
    amr_ai_query = State()
    weight_target = State()


async def add_messages_to_delete(*, state: FSMContext, message_ids: list[int]) -> None:
    data = await state.get_data()
    messages_to_delete = data.get("messages_to_delete", [])
    await state.update_data(messages_to_delete=[*messages_to_delete, *message_ids])


async def clear_messages(*, bot: Bot, chat_id: int | str, state: FSMContext) -> None:
    data = await state.get_data()
    messages_to_delete = data.get("messages_to_delete", [])
    if messages_to_delete:
        await bot.delete_messages(chat_id=chat_id, message_ids=messages_to_delete)
        await state.update_data(messages_to_delete=[])


@router.message(F.text == RootKeyboardText.CALC_CPFC)
async def calc_cpfc_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CalcCPFCSurvey.biological_gender)
    sent_message = await message.answer(
        "🚻 Оберіть вашу біологічну стать, натиснувши кнопку.", reply_markup=biological_gender_keyboard()
    )
    await add_messages_to_delete(state=state, message_ids=[sent_message.message_id])


@router.callback_query(CalcCPFCSurvey.biological_gender, F.data.in_(BIOLOGICAL_GENDER_TO_DATA.values()))
async def calc_cpfc_survey_biological_gender_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    biological_gender = get_key_by_value(BIOLOGICAL_GENDER_TO_DATA, callback_query.data)
    await state.update_data(biological_gender=biological_gender)
    await state.set_state(CalcCPFCSurvey.age)

    await callback_query.answer()
    icon, output = BIOLOGICAL_GENDER_TO_TEXT[biological_gender].split(maxsplit=1)
    await callback_query.message.edit_text(f"{icon} Ваша біологічна стать: {md.hbold(output)}")
    sent_message = await callback_query.message.answer("📅 Вкажіть ваш вік:")
    await add_messages_to_delete(state=state, message_ids=[sent_message.message_id])


@router.message(CalcCPFCSurvey.biological_gender)
async def calc_cpfc_survey_unknown_biological_gender_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Оберіть біологічну стать, натиснувши кнопку під повідомленням.")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCPFCSurvey.age, F.text.regexp(r"^\d+$"))
async def calc_cpfc_survey_age_handler(message: Message, state: FSMContext) -> None:
    age = int(message.text)
    await state.update_data(age=age)
    await state.set_state(CalcCPFCSurvey.height)

    sent_message = await message.answer("📏 Вкажіть ваш зріст (в сантиметрах):")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCPFCSurvey.age, ~F.text.regexp(r"^\d+$"))
async def calc_cpfc_survey_invalid_age_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Вік повинен бути цілим числом. Введіть його ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCPFCSurvey.height, F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_cpfc_survey_height_handler(message: Message, state: FSMContext) -> None:
    height = float(message.text)
    await state.update_data(height=height)
    await state.set_state(CalcCPFCSurvey.weight)

    sent_message = await message.answer("⚖️ Вкажіть вашу вагу (в кілограмах):")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCPFCSurvey.height, ~F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_cpfc_survey_invalid_height_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Зріст повинен бути числом. Введіть його ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCPFCSurvey.weight, F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_cpfc_survey_weight_handler(message: Message, state: FSMContext) -> None:
    weight = float(message.text)
    await state.update_data(weight=weight)
    await state.set_state(CalcCPFCSurvey.fat_pct)

    sent_message = await message.answer("📊 Вкажіть ваш відсоток жиру:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCPFCSurvey.weight, ~F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_cpfc_survey_invalid_weight_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Вага повинна бути числом. Введіть її ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCPFCSurvey.fat_pct, F.text.regexp(r"^\d+$"))
async def calc_cpfc_survey_fat_pct_handler(message: Message, state: FSMContext) -> None:
    fat_pct = int(message.text)
    await state.update_data(fat_pct=fat_pct)
    await state.set_state(CalcCPFCSurvey.amr)

    sent_message = await message.answer(
        "🏃 Оберіть ваш коефіцієнт активності, натиснувши кнопку.", reply_markup=activity_rate_keyboard(show_help=True)
    )
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCPFCSurvey.fat_pct, ~F.text.regexp(r"^\d+$"))
async def calc_cpfc_survey_invalid_fat_pct_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Відсоток жиру повинен бути цілим числом. Введіть його ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.callback_query(CalcCPFCSurvey.amr, F.data.in_(ACTIVITY_RATE_TO_DATA.values()))
async def calc_cpfc_survey_amr_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await add_messages_to_delete(state=state, message_ids=[callback_query.message.message_id])
    await clear_messages(bot=callback_query.bot, chat_id=callback_query.message.chat.id, state=state)

    amr = get_key_by_value(ACTIVITY_RATE_TO_DATA, callback_query.data)
    await state.update_data(amr=amr)
    data = await state.get_data()
    await state.set_state(CalcCPFCSurvey.weight_target)

    await callback_query.message.answer(
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
            footer="🎯 Переконайтесь, що всі дані правильні, та оберіть вашу мету, натиснувши відповідну кнопку.",
            bold_detail_name=False,
            bold_detail_value=True,
        ),
        reply_markup=weight_target_keyboard(),
    )


@router.callback_query(CalcCPFCSurvey.amr, F.data == ACTIVITY_RATE_HELP_DATA)
async def calc_cpfc_survey_amr_help_handler(callback_query: CallbackQuery) -> None:
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


@router.callback_query(CalcCPFCSurvey.amr, F.data == ACTIVITY_RATE_AI_HELP_DATA)
async def calc_cpfc_survey_amr_ai_help_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(CalcCPFCSurvey.amr_ai_query)

    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=activity_rate_keyboard())
    sent_message = await callback_query.message.answer(
        "🤖 Детально опишіть ваш спосіб життя, щоб AI міг допомогти вам визначити ваш коефіцієнт активності:"
    )
    await add_messages_to_delete(state=state, message_ids=[sent_message.message_id])


@router.message(CalcCPFCSurvey.amr_ai_query)
async def calc_cpfc_survey_amr_ai_query_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CalcCPFCSurvey.amr)

    query = (
        "Будь ласка, визначте коефіцієнт активності (1.2, 1.375, 1.55, 1.725 або 1.9) для наступного опису: "
        f'"{message.text}".'
    )
    ai_response = await generate_text(query=query)
    sent_message = await message.answer(md.text(md.hbold("🤖 Відповідь AI:"), f'"{ai_response.rstrip(".")}".'))
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCPFCSurvey.amr)
async def calc_cpfc_survey_invalid_amr_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Оберіть коефіцієнт активності, натиснувши кнопку під повідомленням.")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.callback_query(CalcCPFCSurvey.weight_target, F.data.in_(WEIGHT_TARGET_TO_DATA.values()))
async def calc_cpfc_survey_weight_target_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await clear_messages(bot=callback_query.bot, chat_id=callback_query.message.chat.id, state=state)

    weight_target = get_key_by_value(WEIGHT_TARGET_TO_DATA, callback_query.data)
    await state.update_data(weight_target=weight_target)
    data = await state.get_data()
    await state.clear()

    await callback_query.answer()
    await callback_query.message.edit_text(
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

    await callback_query.message.answer(
        build_detailed_message(
            title="📊 Рекомендовані поживні показники",
            details=[
                ("Калорії", format_numbers_range(min_calories, max_calories, "ккал")),
                ("Білки", format_number(nutritional_profile["proteins"], "г")),
                ("Жири", format_number(nutritional_profile["fats"], "г")),
                ("Вуглеводи", format_numbers_range(min_carbohydrates, max_carbohydrates, "г")),
                ("Вода", format_number(nutritional_profile["water"], "л")),
                ("Клітковина", format_numbers_range(min_fiber, max_fiber, "г")),
                ("Сіль", format_number(nutritional_profile["salt"], "г")),
                ("Норма кофеїну", format_number(nutritional_profile["caffeine_norm"], "мг")),
                ("Макс. доза кофеїну", format_number(nutritional_profile["caffeine_max"], "мг")),
            ],
            footer=(
                md.hbold("⚠️ Зверніть увагу: ")
                + "ці дані не є достовірно точними, оскільки вони залежать від індивідуальних особливостей вашого "
                + "організму. Використовуйте їх як відправну точку та коригуйте на основі ваших результатів."
            ),
            bold_detail_name=False,
            bold_detail_value=True,
        )
    )
    # TODO: add a button to round values & a button to show detailed info (lbm, bmr, tef...).


@router.message(CalcCPFCSurvey.weight_target)
async def calc_cpfc_survey_unknown_weight_target_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Оберіть вашу мету, натиснувши кнопку під повідомленням.")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])
