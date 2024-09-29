from aiogram import F
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils import markdown as md
from aiogram.utils.chat_action import ChatActionSender

from bot.keyboards.inline.activity_rate import activity_rate_keyboard
from bot.keyboards.inline.fat_pct import FAT_PCT_HELP_DATA
from bot.keyboards.reply.survey import SurveyKeyboardText
from bot.regexps import float_regexp
from bot.survey.context import SurveyContext
from bot.survey.routers import SurveyStateRouter
from bot.utils.google_utils import generate_search_link
from bot.utils.parse_utils import parse_float

from .prompts import AMR_PROMPT, WEIGHT_PROMPT
from .states import CalcCaloriesStates

state_router = SurveyStateRouter(CalcCaloriesStates.fat_pct)


@state_router.message(F.text.regexp(float_regexp))
async def fat_pct_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)

    await survey.state.update_data(fat_pct=parse_float(message.text))
    await survey.state.set_state(CalcCaloriesStates.amr)

    sent_message = await message.answer(AMR_PROMPT, reply_markup=activity_rate_keyboard(show_help=True))
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.callback_query(F.data == FAT_PCT_HELP_DATA)
async def fat_pct_help_handler(callback_query: CallbackQuery, survey: SurveyContext) -> None:
    async with ChatActionSender.upload_photo(bot=callback_query.bot, chat_id=callback_query.message.chat.id):
        data = await survey.state.get_data()
        fat_pct_helper_path = f"assets/{data['biological_gender']}-fat-pct-helper.jpg"

        await callback_query.answer()
        await callback_query.message.edit_text(
            "🍔 Визначте ваш відсоток жиру, поглянувши на фото, та вкажіть значення:"
        )
        sent_photo = await callback_query.message.answer_photo(
            photo=FSInputFile(path=fat_pct_helper_path),
            caption=md.html_decoration.italic(
                f"Якщо вам важко визначити відсоток жиру за фото, ви можете скористатися "
                f"{md.hlink('каліпером', generate_search_link('каліпер'))}."
            ),
        )
        await survey.add_messages_to_delete(sent_photo.message_id)


@state_router.message(F.text == SurveyKeyboardText.UNDO_PREV_STEP)
async def undo_fat_pct_handler(message: Message, survey: SurveyContext) -> None:
    await survey.add_messages_to_delete(message.message_id)
    await survey.clear_messages(
        bot=message.bot,
        chat_id=message.chat.id,
        group_names=[CalcCaloriesStates.weight.state, CalcCaloriesStates.fat_pct.state],
    )

    await survey.state.update_data(weight=None)
    await survey.state.set_state(CalcCaloriesStates.weight)

    sent_message = await message.answer(WEIGHT_PROMPT)
    await survey.add_messages_to_delete(sent_message.message_id)


@state_router.message()
async def invalid_fat_pct_handler(message: Message, survey: SurveyContext) -> None:
    sent_message = await message.answer("⚠️ Відсоток жиру повинен бути числом. Введіть його ще раз:")
    await survey.add_messages_to_delete(message.message_id, sent_message.message_id)
