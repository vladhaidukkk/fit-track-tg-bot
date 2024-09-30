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
from bot.utils.aiogram_utils import extract_user_from_update

if settings.sentry.dsn:
    sentry_sdk.init(
        dsn=settings.sentry.dsn,
        # Set traces_sample_rate to 1.0 to capture 100% of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


async def process_pending_bot_updates(bot: Bot) -> None:
    pending_updates = await bot.get_updates()

    chat_ids = {tg_user.id for update in pending_updates if (tg_user := extract_user_from_update(update)) is not None}
    await asyncio.gather(
        *[
            bot.send_message(
                chat_id=chat_id,
                text="😖 Вибачте, що не відповідав. Тепер я знову на зв'язку і готовий допомогти!",
            )
            for chat_id in chat_ids
        ]
    )

    await bot.delete_webhook(drop_pending_updates=True)


async def main() -> None:
    dp = Dispatcher()
    dp.update.outer_middleware(SurveyMiddleware())
    dp.update.outer_middleware(AuthMiddleware())
    dp.include_router(router)

    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await process_pending_bot_updates(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    configure_logging(level_name=settings.log_level_name)
    asyncio.run(main())
