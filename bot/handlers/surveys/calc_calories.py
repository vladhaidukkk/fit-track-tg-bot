from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown as md

from bot.core.nutrition_calculator import calc_nutritional_profile
from bot.keyboards.biological_gender import (
    BIOLOGICAL_GENDER_TO_DATA,
    BIOLOGICAL_GENDER_TO_TEXT,
    biological_gender_keyboard,
)
from bot.keyboards.root import RootKeyboardText
from bot.keyboards.weight_target import WEIGHT_TARGET_TO_DATA, WEIGHT_TARGET_TO_TEXT, weight_target_keyboard
from bot.utils.dict_utils import get_key_by_value
from bot.utils.format_utils import format_age, format_number
from bot.utils.message_utils import build_detailed_message
from bot.utils.string_utils import get_tail

router = Router(name=__name__)


class CalcCaloriesSurvey(StatesGroup):
    biological_gender = State()
    age = State()
    height = State()
    weight = State()
    fat_pct = State()
    amr = State()
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


@router.message(F.text == RootKeyboardText.CALC_CALORIES)
async def calc_calories_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CalcCaloriesSurvey.biological_gender)
    sent_message = await message.answer(
        "🚻 Оберіть вашу біологічну стать, натиснувши кнопку.", reply_markup=biological_gender_keyboard()
    )
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.callback_query(CalcCaloriesSurvey.biological_gender, F.data.in_(BIOLOGICAL_GENDER_TO_DATA.values()))
async def calc_calories_survey_biological_gender_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    biological_gender = get_key_by_value(BIOLOGICAL_GENDER_TO_DATA, callback_query.data)
    await state.update_data(biological_gender=biological_gender)
    await state.set_state(CalcCaloriesSurvey.age)

    await callback_query.answer()
    icon, output = BIOLOGICAL_GENDER_TO_TEXT[biological_gender].split(maxsplit=1)
    await callback_query.message.edit_text(f"{icon} Ваша біологічна стать: {md.hbold(output)}")
    sent_message = await callback_query.message.answer("📅 Вкажіть ваш вік:")
    await add_messages_to_delete(state=state, message_ids=[sent_message.message_id])


@router.message(CalcCaloriesSurvey.biological_gender)
async def calc_calories_survey_unknown_biological_gender_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Оберіть біологічну стать, натиснувши кнопку під повідомленням.")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCaloriesSurvey.age, F.text.regexp(r"^\d+$"))
async def calc_calories_survey_age_handler(message: Message, state: FSMContext) -> None:
    age = int(message.text)
    await state.update_data(age=age)
    await state.set_state(CalcCaloriesSurvey.height)

    sent_message = await message.answer("📏 Вкажіть ваш зріст (в сантиметрах):")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCaloriesSurvey.age, ~F.text.regexp(r"^\d+$"))
async def calc_calories_survey_invalid_age_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Вік повинен бути цілим числом. Введіть його ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCaloriesSurvey.height, F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_height_handler(message: Message, state: FSMContext) -> None:
    height = float(message.text)
    await state.update_data(height=height)
    await state.set_state(CalcCaloriesSurvey.weight)

    sent_message = await message.answer("⚖️ Вкажіть вашу вагу (в кілограмах):")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCaloriesSurvey.height, ~F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_invalid_height_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Зріст повинен бути числом. Введіть його ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCaloriesSurvey.weight, F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_weight_handler(message: Message, state: FSMContext) -> None:
    weight = float(message.text)
    await state.update_data(weight=weight)
    await state.set_state(CalcCaloriesSurvey.fat_pct)

    sent_message = await message.answer("📊 Вкажіть ваш відсоток жиру:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCaloriesSurvey.weight, ~F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_invalid_weight_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Вага повинна бути числом. Введіть її ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCaloriesSurvey.fat_pct, F.text.regexp(r"^\d+$"))
async def calc_calories_survey_fat_pct_handler(message: Message, state: FSMContext) -> None:
    fat_pct = int(message.text)
    await state.update_data(fat_pct=fat_pct)
    await state.set_state(CalcCaloriesSurvey.amr)

    sent_message = await message.answer("🏃 Вкажіть ваш коефіцієнт активності:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCaloriesSurvey.fat_pct, ~F.text.regexp(r"^\d+$"))
async def calc_calories_survey_invalid_fat_pct_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Відсоток жиру повинен бути цілим числом. Введіть його ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcCaloriesSurvey.amr, F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_amr_handler(message: Message, state: FSMContext) -> None:
    await add_messages_to_delete(state=state, message_ids=[message.message_id])
    await clear_messages(bot=message.bot, chat_id=message.chat.id, state=state)

    amr = float(message.text)
    await state.update_data(amr=amr)
    data = await state.get_data()
    await state.set_state(CalcCaloriesSurvey.weight_target)

    await message.answer(
        build_detailed_message(
            title="📋 Вхідні дані",
            details=[
                ("Біологічна стать", get_tail(BIOLOGICAL_GENDER_TO_TEXT[data["biological_gender"]])),
                ("Вік", format_age(data["age"])),
                ("Ріст", format_number(data["height"], "см")),
                ("Вага", format_number(data["weight"], "кг")),
                ("Відсоток жиру", format_number(data["fat_pct"], "%", sep="")),
                ("Коефіцієнт активності", format_number(data["amr"])),
            ],
            footer="🎯 Переконайтесь, що всі дані правильні, та оберіть вашу мету, натиснувши відповідну кнопку.",
        ),
        reply_markup=weight_target_keyboard(),
    )


@router.message(CalcCaloriesSurvey.amr, ~F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_invalid_amr_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Коефіцієнт активності повинен бути числом. Введіть його ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.callback_query(CalcCaloriesSurvey.weight_target, F.data.in_(WEIGHT_TARGET_TO_DATA.values()))
async def calc_calories_survey_weight_target_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
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
                ("Коефіцієнт активності", format_number(data["amr"])),
            ],
            footer=(
                "🎯 Нижче ви бачите рекомендовані поживні показники щоб " +
                md.hbold(get_tail(WEIGHT_TARGET_TO_TEXT[data["weight_target"]]).upper()) +
                ", розраховані на основі вхідних даних."
            ),
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
    await callback_query.message.answer(
        build_detailed_message(
            title="📊 Рекомендовані поживні показники",
            details=[
                ("Калорії", format_number(nutritional_profile["calories"], "ккал")),
                ("Білки", format_number(nutritional_profile["proteins"], "г")),
                ("Жири", format_number(nutritional_profile["fats"], "г")),
                ("Вуглеводи", format_number(nutritional_profile["carbohydrates"], "г")),
                ("Вода", format_number(nutritional_profile["water"], "л")),
                ("Клітковина", format_number(nutritional_profile["fiber"], "г")),
                ("Сіль", format_number(nutritional_profile["salt"], "г")),
                ("Норма кофеїну", format_number(nutritional_profile["caffeine_norm"], "мг")),
                ("Макс. доза кофеїну", format_number(nutritional_profile["caffeine_max"], "мг")),
            ],
            footer=(
                md.hbold("⚠️ Зверніть увагу: ") +
                "ці дані не є достовірно точними, оскільки вони залежать від індивідуальних особливостей вашого " +
                "організму. Використовуйте їх як відправну точку та коригуйте на основі ваших результатів."
            )
        )
    )
    # TODO: add a button to round values & a button to show detailed info (lbm, bmr, tef...).


@router.message(CalcCaloriesSurvey.weight_target)
async def calc_calories_survey_unknown_weight_target_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Оберіть вашу мету, натиснувши кнопку під повідомленням.")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])
