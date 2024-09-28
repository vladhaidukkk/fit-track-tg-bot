from aiogram.fsm.state import State, StatesGroup


class CalcFoodAllocationStates(StatesGroup):
    first_dry_mass = State()
    second_dry_mass = State()
    total_ready_mass = State()
