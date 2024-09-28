from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update

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
