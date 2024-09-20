from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils import markdown as md

from bot.config import settings
from bot.db.models import UserModel
from bot.db.queries import add_user, update_user
from bot.keyboards.root import root_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message, user: UserModel | None) -> None:
    if not user:
        await add_user(id_=message.from_user.id, username=message.from_user.username)
    if user and user.username != message.from_user.username:
        await update_user(id_=message.from_user.id, username=message.from_user.username)

    await message.answer(
        md.text(
            f"Вас вітає {md.hbold(settings.bot.name)}! 👋",
            "Давайте розпочнемо вашу фітнес-подорож разом.",
            sep="\n",
        ),
        reply_markup=root_keyboard(),
    )
