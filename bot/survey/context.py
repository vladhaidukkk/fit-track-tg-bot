from collections import defaultdict

from aiogram import Bot
from aiogram.fsm.context import FSMContext

DEFAULT_GROUP_NAME = "default_group"


class SurveyContext:
    def __init__(self, state: FSMContext) -> None:
        self.state = state

    async def add_messages_to_delete(self, *message_ids: int, group_name: str | None = None) -> None:
        data = await self.state.get_data()
        messages_to_delete = data.get("messages_to_delete", defaultdict(list))

        group_name = group_name or await self.state.get_state() or DEFAULT_GROUP_NAME
        messages_to_delete[group_name] += message_ids

        # It's not enough to mutate the list, as the data is a deep copy of the real data behind the scenes.
        await self.state.update_data(messages_to_delete=messages_to_delete)

    async def clear_messages(
        self, *, bot: Bot, chat_id: int | str, group_name: str | None = None, subset: slice = slice(None)
    ) -> None:
        data = await self.state.get_data()
        messages_to_delete = data.get("messages_to_delete", defaultdict(list))

        if group_name:
            message_ids_to_delete = messages_to_delete[group_name][subset]
            # We delete messages by replacing the sliced content with an empty list, which mutates the original list.
            messages_to_delete[group_name][subset] = []
        else:
            all_message_ids = [
                message_id for group_message_ids in messages_to_delete.values() for message_id in group_message_ids
            ]
            message_ids_to_delete = all_message_ids[subset]
            for group_name_key, group_message_ids in messages_to_delete.items():
                # We refer to group messages directly in this case to mutate the original list.
                messages_to_delete[group_name_key] = [
                    message_id for message_id in group_message_ids if message_id not in message_ids_to_delete
                ]

        if message_ids_to_delete:
            await bot.delete_messages(chat_id=chat_id, message_ids=message_ids_to_delete)
            await self.state.update_data(messages_to_delete=messages_to_delete)
