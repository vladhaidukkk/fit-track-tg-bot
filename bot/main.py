import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

from bot.config import settings

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer(
        markdown.text(
            f"Вас вітає {markdown.hbold(settings.bot.name)}! 👋",
            "Давайте розпочнемо вашу фітнес-подорож разом.",
            sep="\n",
        )
    )


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
