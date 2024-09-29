from aiogram.fsm.state import State, StatesGroup


class CalcCaloriesStates(StatesGroup):
    biological_gender = State()
    age = State()
    height = State()
    weight = State()
    fat_pct = State()
    amr = State()
    amr_ai_query = State()
    weight_target = State()
