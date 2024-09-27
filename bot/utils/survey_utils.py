from aiogram import Bot
from aiogram.fsm.context import FSMContext


async def add_messages_to_delete(*, state: FSMContext, message_ids: list[int]) -> None:
    data = await state.get_data()
    messages_to_delete = data.get("messages_to_delete", [])
    await state.update_data(messages_to_delete=[*messages_to_delete, *message_ids])


async def clear_messages(*, bot: Bot, chat_id: int | str, state: FSMContext, subset: slice = slice(None)) -> None:
    data = await state.get_data()
    messages_to_delete = data.get("messages_to_delete", [])[subset]
    if messages_to_delete:
        await bot.delete_messages(chat_id=chat_id, message_ids=messages_to_delete)
        await state.update_data(messages_to_delete=[])
