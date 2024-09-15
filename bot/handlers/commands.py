from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

from bot.config import settings
from bot.keyboards.root import root_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer(
        markdown.text(
            f"Вас вітає {markdown.hbold(settings.bot.name)}! 👋",
            "Давайте розпочнемо вашу фітнес-подорож разом.",
            sep="\n",
        ),
        reply_markup=root_keyboard(),
    )
