from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from bot.survey.context import SurveyContext


class SurveyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, any]], Awaitable[any]],
        event: Update,
        data: dict[str, any],
    ) -> any:
        if state := data.get("state"):
            data["survey"] = SurveyContext(state)
        return await handler(event, data)


class IncomingMessageTrackerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, any]], Awaitable[any]],
        event: Message,
        data: dict[str, any],
    ) -> any:
        if not isinstance(event, Message):
            raise TypeError(f"{self.__class__.__name__} can only be applied to message events")

        survey: SurveyContext = data.get("survey")
        if not survey:
            raise TypeError(f"{self.__class__.__name__} requires {SurveyMiddleware.__name__} to be applied before it")

        await survey.add_messages_to_delete(event.message_id)
        return await handler(event, data)
