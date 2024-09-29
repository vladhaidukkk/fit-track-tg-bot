from collections import defaultdict

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State


class SurveyContext:
    DEFAULT_GROUP_NAME = "default_group"

    def __init__(self, state: FSMContext) -> None:
        self.state = state

    async def add_messages_to_delete(self, *message_ids: int, group_name: str | None = None) -> None:
        data = await self.state.get_data()
        messages_to_delete = data.get("messages_to_delete", defaultdict(list))

        group_name = group_name or await self.state.get_state() or self.DEFAULT_GROUP_NAME
        messages_to_delete[group_name] += message_ids

        # It's not enough to mutate the list, as the data is a deep copy of the real data behind the scenes.
        await self.state.update_data(messages_to_delete=messages_to_delete)

    async def clear_messages(
        self,
        *,
        bot: Bot,
        chat_id: int | str,
        group_names: list[str] | None = None,
        exclude_group_names: list[str] | None = None,
        subset: slice = slice(None),
    ) -> None:
        data = await self.state.get_data()
        messages_to_delete = data.get("messages_to_delete", defaultdict(list))

        group_names = group_names or list(messages_to_delete)
        exclude_group_names = set(exclude_group_names or [])
        group_names = [group_name for group_name in group_names if group_name not in exclude_group_names]

        combined_message_ids = [
            message_id for group_name in group_names for message_id in messages_to_delete[group_name]
        ]
        message_ids_to_delete = combined_message_ids[subset]
        for group_name in group_names:
            # We refer to group messages directly in this case to mutate the original list.
            messages_to_delete[group_name] = [
                message_id for message_id in messages_to_delete[group_name] if message_id not in message_ids_to_delete
            ]

        if message_ids_to_delete:
            await bot.delete_messages(chat_id=chat_id, message_ids=message_ids_to_delete)
            await self.state.update_data(messages_to_delete=messages_to_delete)

    async def go_to_prev_step(
        self,
        *,
        bot: Bot,
        chat_id: int | str,
        prev_state: State,
        clear_prev_state_messages: bool = False,
    ) -> None:
        group_names_to_clear = [await self.state.get_state()]
        if clear_prev_state_messages:
            group_names_to_clear.append(prev_state.state)
        await self.clear_messages(bot=bot, chat_id=chat_id, group_names=group_names_to_clear)

        await self.state.update_data({prev_state.state: None})
        await self.state.set_state(prev_state)
