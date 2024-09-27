from aiogram import F, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.core.food_allocation_calculator import calc_food_allocation
from bot.filters import PrivilegedUserFilter
from bot.keyboards.reply.root import RootKeyboardText, root_keyboard
from bot.keyboards.reply.survey import SurveyKeyboardText, survey_keyboard
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


FIRST_DRY_MASS_PROMPT = "1️⃣ Вкажіть суху вагу продукту для першої особи (в грамах):"
SECOND_DRY_MASS_PROMPT = "2️⃣ Вкажіть суху вагу продукту для другої особи (в грамах):"
TOTAL_READY_MASS_PROMPT = "⚖️ Вкажіть загальну вагу приготованого продукту (в грамах):"


@router.message(F.text == RootKeyboardText.CALC_FOOD_ALLOCATION)
async def calc_food_allocation_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CalcFoodAllocationSurvey.first_dry_mass)

    start_message = await message.answer(
        "🍽️ Розрахунок розподілу їжі розпочато. Покроково вказуйте вхідні дані для отримання результату.",
        reply_markup=survey_keyboard(),
    )
    await add_messages_to_delete(state=state, message_ids=[message.message_id, start_message.message_id])

    first_dry_mass_message = await message.answer(FIRST_DRY_MASS_PROMPT)
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.first_dry_mass.state,
        message_ids=[first_dry_mass_message.message_id],
    )


@router.message(or_f(*CalcFoodAllocationSurvey.__states__), F.text == SurveyKeyboardText.CANCEL)
async def calc_food_allocation_survey_cancel_button_handler(message: Message, state: FSMContext) -> None:
    await clear_messages(bot=message.bot, chat_id=message.chat.id, state=state, subset=slice(1, None))
    await state.clear()
    await message.reply("Розрахунок розподілу їжі скасовано.", reply_markup=root_keyboard(user_id=message.from_user.id))


@router.message(CalcFoodAllocationSurvey.first_dry_mass, F.text.regexp(float_regexp))
async def calc_food_allocation_survey_first_dry_mass_handler(message: Message, state: FSMContext) -> None:
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.first_dry_mass.state,
        message_ids=[message.message_id],
    )

    first_dry_mass = parse_float(message.text)
    await state.update_data(first_dry_mass=first_dry_mass)
    await state.set_state(CalcFoodAllocationSurvey.second_dry_mass)

    sent_message = await message.answer(SECOND_DRY_MASS_PROMPT)
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.second_dry_mass.state,
        message_ids=[sent_message.message_id],
    )


@router.message(CalcFoodAllocationSurvey.second_dry_mass, F.text.regexp(float_regexp))
async def calc_food_allocation_survey_second_dry_mass_handler(message: Message, state: FSMContext) -> None:
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.second_dry_mass.state,
        message_ids=[message.message_id],
    )

    second_dry_mass = parse_float(message.text)
    await state.update_data(second_dry_mass=second_dry_mass)
    await state.set_state(CalcFoodAllocationSurvey.total_ready_mass)

    sent_message = await message.answer(TOTAL_READY_MASS_PROMPT)
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.total_ready_mass.state,
        message_ids=[sent_message.message_id],
    )


@router.message(CalcFoodAllocationSurvey.second_dry_mass, F.text == SurveyKeyboardText.UNDO_PREV_STEP)
async def calc_food_allocation_survey_undo_first_dry_mass_handler(message: Message, state: FSMContext) -> None:
    await clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.first_dry_mass.state,
    )
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.second_dry_mass.state,
        message_ids=[message.message_id],
    )
    await clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.second_dry_mass.state,
    )

    await state.update_data(first_dry_mass=None)
    await state.set_state(CalcFoodAllocationSurvey.first_dry_mass)

    sent_message = await message.answer(FIRST_DRY_MASS_PROMPT)
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.first_dry_mass.state,
        message_ids=[sent_message.message_id],
    )


@router.message(CalcFoodAllocationSurvey.total_ready_mass, F.text.regexp(float_regexp))
async def calc_food_allocation_survey_total_ready_mass_handler(message: Message, state: FSMContext) -> None:
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.total_ready_mass.state,
        message_ids=[message.message_id],
    )
    await clear_messages(bot=message.bot, chat_id=message.chat.id, state=state, subset=slice(1, None))

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
        ),
        reply_markup=root_keyboard(user_id=message.from_user.id),
    )


@router.message(CalcFoodAllocationSurvey.total_ready_mass, F.text == SurveyKeyboardText.UNDO_PREV_STEP)
async def calc_food_allocation_survey_undo_second_dry_mass_handler(message: Message, state: FSMContext) -> None:
    await clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.second_dry_mass.state,
    )
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.total_ready_mass.state,
        message_ids=[message.message_id],
    )
    await clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.total_ready_mass.state,
    )

    await state.update_data(second_dry_mass=None)
    await state.set_state(CalcFoodAllocationSurvey.second_dry_mass)

    sent_message = await message.answer(SECOND_DRY_MASS_PROMPT)
    await add_messages_to_delete(
        state=state,
        messages_group_name=CalcFoodAllocationSurvey.second_dry_mass.state,
        message_ids=[sent_message.message_id],
    )


@router.message(CalcFoodAllocationSurvey.first_dry_mass)
@router.message(CalcFoodAllocationSurvey.second_dry_mass)
@router.message(CalcFoodAllocationSurvey.total_ready_mass)
async def calc_food_allocation_survey_invalid_mass_handler(message: Message, state: FSMContext) -> None:
    state_name = await state.get_state()
    sent_message = await message.answer("⚠️ Вага повинна бути числом. Введіть її ще раз:")
    await add_messages_to_delete(
        state=state, messages_group_name=state_name, message_ids=[message.message_id, sent_message.message_id]
    )
