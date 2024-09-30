from aiogram.fsm.state import State, StatesGroup


class LeaveSuggestionStates(StatesGroup):
    suggestion = State()
