from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown as md

from bot.config import settings
from bot.db.models import UserModel
from bot.db.queries import add_user, update_user
from bot.keyboards.reply.root import root_keyboard
from bot.utils.survey_utils import clear_messages

primary_router = Router(name=f"{__name__}:primary")


@primary_router.message(CommandStart())
async def start_command_handler(message: Message, state: FSMContext, user: UserModel | None) -> None:
    await clear_messages(bot=message.bot, chat_id=message.chat.id, state=state)
    await state.clear()

    if not user:
        await add_user(id_=message.from_user.id, username=message.from_user.username)
    if user and user.username != message.from_user.username:
        await update_user(id_=message.from_user.id, username=message.from_user.username)

    text = (
        "З поверненням! Готові до нових вершин? 💪"
        if user
        else md.text(
            f"Вас вітає {md.hbold(settings.bot.name)}! 👋",
            (
                f"Я роблю підрахунок калорій {md.hbold('простим')} і {md.hbold('точним')}, використовуючи "
                f"{md.hbold('найновіші рекомендації')}. Вам більше не потрібно робити це вручну."
            ),
            "Почнімо досягати нових вершин у вашій фітнес-подорожі разом! 💪",
            sep="\n\n",
        )
    )
    await message.answer(text, reply_markup=root_keyboard(user_id=message.from_user.id))


@primary_router.message(Command("cancel"))
async def cancel_command_handler(message: Message, state: FSMContext) -> None:
    await clear_messages(bot=message.bot, chat_id=message.chat.id, state=state, subset=slice(1, None))
    await state.clear()
    await message.reply("🚫 Поточну дію скасовано.", reply_markup=root_keyboard(user_id=message.from_user.id))


secondary_router = Router(name=f"{__name__}:secondary")


@secondary_router.message(Command("id"))
async def id_command_handler(message: Message) -> None:
    await message.answer(md.hcode(message.from_user.id))
