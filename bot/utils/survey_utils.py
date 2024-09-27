from collections import defaultdict

from aiogram import Bot
from aiogram.fsm.context import FSMContext

DEFAULT_MESSAGES_GROUP_NAME = "default_group"


async def add_messages_to_delete(
    *, state: FSMContext, messages_group_name: str = DEFAULT_MESSAGES_GROUP_NAME, message_ids: list[int]
) -> None:
    data = await state.get_data()
    messages_to_delete = data.get("messages_to_delete", defaultdict(list))
    messages_to_delete[messages_group_name] += message_ids
    # It's not enough to mutate the list, as the data is a deep copy of the real data behind the scenes.
    await state.update_data(messages_to_delete=messages_to_delete)


async def clear_messages(
    *,
    bot: Bot,
    chat_id: int | str,
    state: FSMContext,
    messages_group_name: str | None = None,
    subset: slice = slice(None),
) -> None:
    data = await state.get_data()
    messages_to_delete = data.get("messages_to_delete", defaultdict(list))

    if messages_group_name:
        message_ids_to_delete = messages_to_delete[messages_group_name][subset]
        # We delete messages by replacing the sliced content with an empty list, which mutates the original list.
        messages_to_delete[messages_group_name][subset] = []
    else:
        all_message_ids = [
            message_id for group_message_ids in messages_to_delete.values() for message_id in group_message_ids
        ]
        message_ids_to_delete = all_message_ids[subset]
        for group_name, group_message_ids in messages_to_delete.items():
            # We refer to group messages directly in this case to mutate the original list.
            messages_to_delete[group_name] = [
                message_id for message_id in group_message_ids if message_id not in message_ids_to_delete
            ]

    if message_ids_to_delete:
        await bot.delete_messages(chat_id=chat_id, message_ids=message_ids_to_delete)
        await state.update_data(messages_to_delete=messages_to_delete)
