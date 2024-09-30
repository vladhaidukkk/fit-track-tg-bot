from aiogram import Router
from aiogram.dispatcher.event.event import CallbackType
from aiogram.filters import Filter, or_f
from aiogram.fsm.state import State, StatesGroup

from bot.survey.middlewares import IncomingMessageTrackerMiddleware


class SurveyStateRouter(Router):
    def __init__(self, state: State) -> None:
        super().__init__(name=state.state)

        # Apply the survey state filter to all event types.
        for observer in self.observers.values():
            observer.filter(state)


class SurveyRouter(Router):
    def __init__(self, states: type[StatesGroup], *, to_delete_incoming_messages: bool = False) -> None:
        super().__init__(name=states.__name__)

        self.states = states
        self.before_states_router = Router(name=f"{states.__name__}:before")
        self.after_states_router = Router(name=f"{states.__name__}:after")

        if to_delete_incoming_messages:
            self.message.middleware(IncomingMessageTrackerMiddleware())

    @property
    def before_states(self) -> Router:
        return self.before_states_router

    @property
    def after_states(self) -> Router:
        return self.after_states_router

    @property
    def all_states_filter(self) -> Filter:
        return or_f(*self.states)

    def filter(self, *filters: CallbackType) -> None:
        for observer in self.observers.values():
            observer.filter(*filters)

    def include_state_routers(self, *state_routers: SurveyStateRouter) -> None:
        self.include_routers(self.before_states_router, *state_routers, self.after_states_router)
