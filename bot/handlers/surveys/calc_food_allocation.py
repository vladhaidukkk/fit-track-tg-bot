from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.core.food_allocation_calculator import calc_food_allocation
from bot.filters import PrivilegedUserFilter
from bot.keyboards.root import RootKeyboardText
from bot.regexps import float_regexp
from bot.utils.format_utils import format_number
from bot.utils.message_utils import build_detailed_message
from bot.utils.parse_utils import parse_float
from bot.utils.survey_utils import add_messages_to_delete, clear_messages

router = Router(name=__name__)
router.message.filter(PrivilegedUserFilter())


class CalcFoodAllocationSurvey(StatesGroup):
    first_dry_mass = State()
    second_dry_mass = State()
    total_ready_mass = State()


@router.message(F.text == RootKeyboardText.CALC_FOOD_ALLOCATION)
async def calc_food_allocation_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CalcFoodAllocationSurvey.first_dry_mass)
    sent_message = await message.answer("1️⃣ Вкажіть суху вагу продукту для першої особи (в грамах):")
    await add_messages_to_delete(state=state, message_ids=[sent_message.message_id])


@router.message(CalcFoodAllocationSurvey.first_dry_mass, F.text.regexp(float_regexp))
async def calc_food_allocation_survey_first_dry_mass_handler(message: Message, state: FSMContext) -> None:
    first_dry_mass = parse_float(message.text)
    await state.update_data(first_dry_mass=first_dry_mass)
    await state.set_state(CalcFoodAllocationSurvey.second_dry_mass)

    sent_message = await message.answer("2️⃣ Вкажіть суху вагу продукту для другої особи (в грамах):")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcFoodAllocationSurvey.second_dry_mass, F.text.regexp(float_regexp))
async def calc_food_allocation_survey_second_dry_mass_handler(message: Message, state: FSMContext) -> None:
    second_dry_mass = parse_float(message.text)
    await state.update_data(second_dry_mass=second_dry_mass)
    await state.set_state(CalcFoodAllocationSurvey.total_ready_mass)

    sent_message = await message.answer("⚖️ Вкажіть загальну вагу приготованого продукту (в грамах):")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])


@router.message(CalcFoodAllocationSurvey.total_ready_mass, F.text.regexp(float_regexp))
async def calc_food_allocation_survey_total_ready_mass_handler(message: Message, state: FSMContext) -> None:
    await add_messages_to_delete(state=state, message_ids=[message.message_id])
    await clear_messages(bot=message.bot, chat_id=message.chat.id, state=state)

    total_ready_mass = parse_float(message.text)
    await state.update_data(total_ready_mass=total_ready_mass)
    data = await state.get_data()
    await state.clear()

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
        )
    )


@router.message(CalcFoodAllocationSurvey.first_dry_mass)
@router.message(CalcFoodAllocationSurvey.second_dry_mass)
@router.message(CalcFoodAllocationSurvey.total_ready_mass)
async def calc_food_allocation_survey_invalid_mass_handler(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer("⚠️ Вага повинна бути числом. Введіть її ще раз:")
    await add_messages_to_delete(state=state, message_ids=[message.message_id, sent_message.message_id])
