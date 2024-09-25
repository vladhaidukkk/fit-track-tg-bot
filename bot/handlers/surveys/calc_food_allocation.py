from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.keyboards.root import RootKeyboardText
from bot.regexps import float_regexp

router = Router(name=__name__)


class CalcFoodAllocationSurvey(StatesGroup):
    first_dry_mass = State()
    second_dry_mass = State()
    total_ready_mass = State()


@router.message(F.text == RootKeyboardText.CALC_FOOD_ALLOCATION)
async def calc_food_allocation_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CalcFoodAllocationSurvey.first_dry_mass)
    await message.answer("1️⃣ Вкажіть суху вагу продукту для першої людини (в грамах):")


@router.message(CalcFoodAllocationSurvey.first_dry_mass, F.text.regexp(float_regexp))
async def calc_food_allocation_survey_first_dry_mass_handler(message: Message, state: FSMContext) -> None:
    first_dry_mass = float(message.text)
    await state.update_data(first_dry_mass=first_dry_mass)
    await state.set_state(CalcFoodAllocationSurvey.second_dry_mass)
    await message.answer("2️⃣ Вкажіть суху вагу продукту для другої людини (в грамах):")


@router.message(CalcFoodAllocationSurvey.second_dry_mass, F.text.regexp(float_regexp))
async def calc_food_allocation_survey_second_dry_mass_handler(message: Message, state: FSMContext) -> None:
    second_dry_mass = float(message.text)
    await state.update_data(second_dry_mass=second_dry_mass)
    await state.set_state(CalcFoodAllocationSurvey.total_ready_mass)
    await message.answer("⚖️ Вкажіть загальну вагу приготованого продукту (в грамах):")


@router.message(CalcFoodAllocationSurvey.total_ready_mass, F.text.regexp(float_regexp))
async def calc_food_allocation_survey_total_ready_mass_handler(message: Message, state: FSMContext) -> None:
    total_ready_mass = float(message.text)
    await state.update_data(total_ready_mass=total_ready_mass)
    data = await state.get_data()  # noqa: F841
    await state.clear()


@router.message(CalcFoodAllocationSurvey.first_dry_mass)
@router.message(CalcFoodAllocationSurvey.second_dry_mass)
@router.message(CalcFoodAllocationSurvey.total_ready_mass)
async def calc_food_allocation_survey_invalid_mass_handler(message: Message) -> None:
    await message.answer("⚠️ Вага повинна бути числом. Введіть її ще раз:")
