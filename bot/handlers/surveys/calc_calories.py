from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown

from bot.core.nutrition_calculator import calc_calories
from bot.keyboards.gender import GENDER_TO_DATA, GENDER_TO_TEXT, gender_keyboard
from bot.keyboards.root import RootKeyboardText
from bot.utils.dict_utils import get_key_by_value

router = Router(name=__name__)


class CalcCaloriesSurvey(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    fat_pct = State()
    amr = State()


@router.message(F.text == RootKeyboardText.CALC_CALORIES)
async def calc_calories_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CalcCaloriesSurvey.gender)
    await message.answer("🚻 Оберіть вашу біологічну стать, натиснувши кнопку.", reply_markup=gender_keyboard())


@router.callback_query(CalcCaloriesSurvey.gender, F.data.in_(GENDER_TO_DATA.values()))
async def calc_calories_survey_gender_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    gender = get_key_by_value(GENDER_TO_DATA, callback_query.data)
    await state.update_data(gender=gender)
    await state.set_state(CalcCaloriesSurvey.age)

    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(GENDER_TO_TEXT[gender])
    await callback_query.message.answer("📅 Вкажіть ваш вік:")


@router.message(CalcCaloriesSurvey.gender)
async def calc_calories_survey_unknown_gender_handler(message: Message) -> None:
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
    await state.clear()

    daily_calories = calc_calories(
        gender=data["gender"],
        age=data["age"],
        height=data["height"],
        weight=data["weight"],
        fat_pct=data["fat_pct"],
        amr=data["amr"],
    )
    await message.answer(
        markdown.text("🍽️ Ваша денна норма калорій становить:", markdown.hbold(f"{daily_calories:.2f}"))
    )


@router.message(CalcCaloriesSurvey.amr, ~F.text.regexp(r"^\d+(\.\d+)?$"))
async def calc_calories_survey_invalid_amr_handler(message: Message) -> None:
    await message.answer("⚠️ Коефіцієнт активності повинен бути числом. Введіть його ще раз:")
