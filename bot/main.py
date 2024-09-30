import asyncio

import sentry_sdk
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings
from bot.handlers import router
from bot.logger import configure_logging
from bot.middlewares.auth import AuthMiddleware
from bot.survey.middlewares import SurveyMiddleware

if settings.sentry.dsn:
    sentry_sdk.init(
        dsn=settings.sentry.dsn,
        # Set traces_sample_rate to 1.0 to capture 100% of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


async def main() -> None:
    dp = Dispatcher()
    dp.update.outer_middleware(SurveyMiddleware())
    dp.update.outer_middleware(AuthMiddleware())
    dp.include_router(router)

    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    configure_logging(level_name=settings.log_level_name)
    asyncio.run(main())
