from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils import markdown as md

from bot.db.queries import get_users
from bot.filters import AdminFilter
from bot.keyboards.reply.root import RootKeyboardText

router = Router(name=__name__)


@router.message(AdminFilter(), F.text == RootKeyboardText.LIST_USERS)
async def list_users_action_handler(message: Message) -> None:
    users = await get_users()
    await message.answer(
        md.text(
            *(
                f"{md.hcode(user.id)} | @{user.username} | {user.event_count}"
                if user.username
                else f"{md.hcode(user.id)} | {user.event_count}"
                for user in users
            ),
            sep="\n",
        )
    )
