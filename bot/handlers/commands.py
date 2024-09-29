from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils import markdown as md

from bot.config import settings
from bot.db.models import UserModel
from bot.keyboards.reply.root import root_keyboard
from bot.survey.context import SurveyContext

primary_router = Router(name=f"{__name__}:primary")


@primary_router.message(CommandStart())
async def start_command_handler(message: Message, survey: SurveyContext, user: UserModel | None) -> None:
    await survey.clear_messages(bot=message.bot, chat_id=message.chat.id)
    await survey.state.clear()

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
async def cancel_command_handler(message: Message, survey: SurveyContext) -> None:
    await survey.clear_messages(bot=message.bot, chat_id=message.chat.id, subset=slice(1, None))

    active_state = await survey.state.get_state()
    await survey.state.clear()

    text = "🚫 Активну дію скасовано." if active_state else "ℹ️ Ніяка дія не активована."
    await message.answer(text, reply_markup=root_keyboard(user_id=message.from_user.id))


secondary_router = Router(name=f"{__name__}:secondary")


@secondary_router.message(Command("id"))
async def id_command_handler(message: Message) -> None:
    await message.answer(md.hcode(message.from_user.id))
