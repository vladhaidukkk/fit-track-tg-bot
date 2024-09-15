from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.keyboards.gender import GENDER_TO_DATA, GENDER_TO_TEXT, gender_keyboard
from bot.keyboards.root import RootKeyboardText, root_keyboard
from bot.utils import get_key_by_value

router = Router(name=__name__)


class CalcCaloriesSurvey(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()


@router.message(F.text == RootKeyboardText.CALC_CALORIES)
async def calc_calories_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CalcCaloriesSurvey.gender)
    await message.answer("🚻 Оберіть біологічну стать, натиснувши кнопку.", reply_markup=gender_keyboard())


@router.callback_query(CalcCaloriesSurvey.gender, F.data.in_(GENDER_TO_DATA.values()))
async def calc_calories_survey_gender_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    gender = get_key_by_value(GENDER_TO_DATA, callback_query.data)
    await state.update_data(gender=gender)
    await state.set_state(CalcCaloriesSurvey.age)

    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(GENDER_TO_TEXT[gender], reply_markup=root_keyboard())

    # TODO: continue survey.
    await state.clear()


@router.message(CalcCaloriesSurvey.gender)
async def calc_calories_survey_unknown_gender_handler(message: Message) -> None:
    await message.answer("⚠️ Оберіть біологічну стать, натиснувши кнопку під повідомленням.")
