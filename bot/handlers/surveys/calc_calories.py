from aiogram import F, Router
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

router = Router(name=__name__)


class CalcCaloriesSurvey(StatesGroup):
    biological_gender = State()
    age = State()
    height = State()
    weight = State()
    fat_pct = State()
    amr = State()
    weight_target = State()


@router.message(F.text == RootKeyboardText.CALC_CALORIES)
async def calc_calories_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CalcCaloriesSurvey.biological_gender)
    await message.answer(
        "🚻 Оберіть вашу біологічну стать, натиснувши кнопку.", reply_markup=biological_gender_keyboard()
    )


@router.callback_query(CalcCaloriesSurvey.biological_gender, F.data.in_(BIOLOGICAL_GENDER_TO_DATA.values()))
async def calc_calories_survey_biological_gender_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    biological_gender = get_key_by_value(BIOLOGICAL_GENDER_TO_DATA, callback_query.data)
    await state.update_data(biological_gender=biological_gender)
    await state.set_state(CalcCaloriesSurvey.age)

    await callback_query.answer()
    icon, output = BIOLOGICAL_GENDER_TO_TEXT[biological_gender].split(maxsplit=1)
    await callback_query.message.edit_text(f"{icon} Ваша біологічна стать: {md.hbold(output)}")
    await callback_query.message.answer("📅 Вкажіть ваш вік:")


@router.message(CalcCaloriesSurvey.biological_gender)
async def calc_calories_survey_unknown_biological_gender_handler(message: Message) -> None:
    await message.answer("⚠️ Оберіть біологічну стать, натиснувши кнопку під повідомленням.")


@router.message(CalcCaloriesSurvey.age, F.text.regexp(r"^\d+$"))
async def calc_calories_survey_age_handler(message: Message, state: FSMContext) -> None:
    age = int(message.text)
    await state.update_data(age=age)
    await state.set_state(CalcCaloriesSurvey.height)
    await message.answer("📏 Вкажіть ваш зріст (в сантиметрах):")


@router.message(CalcCaloriesSurvey.age, ~F.text.regexp(r"^\d+$"))
async def calc_calories_survey_invalid_age_handler(message: Message) -> None:
    await message.answer("⚠️ Вік повинен бути цілим числом. Введіть його ще раз:")


@router.message(CalcCaloriesSurvey.height, F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_height_handler(message: Message, state: FSMContext) -> None:
    height = float(message.text)
    await state.update_data(height=height)
    await state.set_state(CalcCaloriesSurvey.weight)
    await message.answer("⚖️ Вкажіть вашу вагу (в кілограмах):")


@router.message(CalcCaloriesSurvey.height, ~F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_invalid_height_handler(message: Message) -> None:
    await message.answer("⚠️ Зріст повинен бути числом. Введіть його ще раз:")


@router.message(CalcCaloriesSurvey.weight, F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_weight_handler(message: Message, state: FSMContext) -> None:
    weight = float(message.text)
    await state.update_data(weight=weight)
    await state.set_state(CalcCaloriesSurvey.fat_pct)
    await message.answer("📊 Вкажіть ваш відсоток жиру:")


@router.message(CalcCaloriesSurvey.weight, ~F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_invalid_weight_handler(message: Message) -> None:
    await message.answer("⚠️ Вага повинна бути числом. Введіть її ще раз:")


@router.message(CalcCaloriesSurvey.fat_pct, F.text.regexp(r"^\d+$"))
async def calc_calories_survey_fat_pct_handler(message: Message, state: FSMContext) -> None:
    fat_pct = int(message.text)
    await state.update_data(fat_pct=fat_pct)
    await state.set_state(CalcCaloriesSurvey.amr)
    await message.answer("🏃 Вкажіть ваш коефіцієнт активності:")


@router.message(CalcCaloriesSurvey.fat_pct, ~F.text.regexp(r"^\d+$"))
async def calc_calories_survey_invalid_fat_pct_handler(message: Message) -> None:
    await message.answer("⚠️ Відсоток жиру повинен бути цілим числом. Введіть його ще раз:")


@router.message(CalcCaloriesSurvey.amr, F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_amr_handler(message: Message, state: FSMContext) -> None:
    amr = float(message.text)
    await state.update_data(amr=amr)
    data = await state.get_data()
    await state.set_state(CalcCaloriesSurvey.weight_target)

    _biological_gender_icon, biological_gender_output = BIOLOGICAL_GENDER_TO_TEXT[data["biological_gender"]].split(
        maxsplit=1
    )
    age = data["age"]
    if age % 10 == 1 and age % 100 != 11:
        age_word = "рік"
    elif 2 <= age % 10 <= 4 and not (12 <= age % 100 <= 14):
        age_word = "роки"
    else:
        age_word = "років"
    await message.answer(
        md.text(
            f"Біологічна стать: {md.hbold(biological_gender_output)}",
            f"Вік: {md.hbold(f"{data["age"]} {age_word}")}",
            f"Ріст: {md.hbold(f"{data["height"]} см")}",
            f"Вага: {md.hbold(f"{data["weight"]} кг")}",
            f"Відсоток жиру: {md.hbold(f"{data["fat_pct"]}%")}",
            f"Коефіцієнт активності: {md.hbold(data["amr"])}",
            sep="\n",
        )
    )
    await message.answer(
        (
            "🎯 Переконайтесь, що всі дані правильні, та оберіть вашу мету, натиснувши відповідну кнопку. "
            "Тоді ви отримаєте детальний опис поживних показників відповідно до обраної мети."
        ),
        reply_markup=weight_target_keyboard(),
    )


@router.message(CalcCaloriesSurvey.amr, ~F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_invalid_amr_handler(message: Message) -> None:
    await message.answer("⚠️ Коефіцієнт активності повинен бути числом. Введіть його ще раз:")


@router.callback_query(CalcCaloriesSurvey.weight_target, F.data.in_(WEIGHT_TARGET_TO_DATA.values()))
async def calc_calories_survey_weight_target_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    weight_target = get_key_by_value(WEIGHT_TARGET_TO_DATA, callback_query.data)
    await state.update_data(weight_target=weight_target)
    data = await state.get_data()
    await state.clear()

    await callback_query.answer()
    _icon, output = WEIGHT_TARGET_TO_TEXT[weight_target].split(maxsplit=1)
    await callback_query.message.edit_text(f"🎯 Ваша мета: {md.hbold(output)}")

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
        md.text("🍽️ Ваша денна норма калорій становить:", md.hbold(f"{nutritional_profile["calories"]:.2f}"))
    )


@router.message(CalcCaloriesSurvey.weight_target)
async def calc_calories_survey_unknown_weight_target_handler(message: Message) -> None:
    await message.answer("⚠️ Оберіть вашу мету, натиснувши кнопку під повідомленням.")
