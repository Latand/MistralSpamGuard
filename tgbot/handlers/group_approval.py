import asyncio

from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import StorageKey

from tgbot.filters.groups_filter import AllowedGroupsFilter

group_approval_router = Router()
GroupApprovalState = State("group_approval_state")

REACTIONS = ["👍", "👎", "❤", "🔥", "🥰", "👏"]
GROUP_APPROVE_TEXT = {
    "en": "Welcome to our group! Please react to this message with any of the following reactions 👍, 👎, ❤, 🔥, 🥰, 👏 to be approved. \n\nThis is a special approval function to keep the group spam-free.\n\nYou have 5 minutes and your request will be declined",
    "ru": "Добро пожаловать в нашу группу! Пожалуйста, поставьте реакцию на это сообщение одним из следующих эмодзи 👍, 👎, ❤, 🔥, 🥰, 👏 для подтверждения. \n\nЭто специальная функция одобрения для защиты группы от спама.\n\nУ вас есть 5 минут, после чего заявка будет отклонена.",
    "uk": "Ласкаво просимо до нашої групи! Будь ласка, відреагуйте на це повідомлення будь-якою з наступних реакцій 👍, 👎, ❤, 🔥, 🥰, 👏 для схвалення. \n\nЦе спеціальна функція схвалення для захисту групи від спаму.\n\nУ вас є 5 хвилин, після чого заявка буде скасована",
}


@group_approval_router.chat_join_request(AllowedGroupsFilter())
async def group_enter_captcha(
    chat_join_request: types.ChatJoinRequest, state: FSMContext, bot: Bot
):
    language = chat_join_request.from_user.language_code
    text = GROUP_APPROVE_TEXT.get(language, GROUP_APPROVE_TEXT["en"])
    # await chat_join_request.answer(text)
    await bot.send_message(
        chat_id=chat_join_request.from_user.id,
        text=text,
    )
    private_storage_key = StorageKey(
        bot_id=bot.id,
        chat_id=chat_join_request.from_user.id,
        user_id=chat_join_request.from_user.id,
    )

    await state.storage.set_state(private_storage_key, GroupApprovalState)
    await state.storage.update_data(
        private_storage_key, dict(chat_id=chat_join_request.chat.id)
    )

    await asyncio.sleep(280)
    data = await state.storage.get_data(private_storage_key)
    if data:
        await bot.decline_chat_join_request(
            chat_id=chat_join_request.chat.id,
            user_id=chat_join_request.from_user.id,
        )
        await bot.send_message(
            chat_id=chat_join_request.from_user.id,
            text="Your request has been declined",
        )
        await state.storage.set_state(private_storage_key, None)
        await state.storage.set_data(private_storage_key, {})


@group_approval_router.message_reaction(GroupApprovalState)
async def group_approval_reaction_sent(
    message_reactions: types.MessageReactionUpdated, state: FSMContext, bot: Bot
):
    state_data = await state.get_data()
    group_id = state_data["chat_id"]
    if any(
        [reaction.emoji in REACTIONS for reaction in message_reactions.new_reaction]
    ):
        await bot.approve_chat_join_request(
            chat_id=group_id,
            user_id=message_reactions.user.id,
        )
        await bot.send_message(
            chat_id=message_reactions.user.id,
            text="You have been approved to join the @botoid!",
        )
        await state.clear()

    else:
        await bot.send_message(
            chat_id=message_reactions.user.id,
            text="Invalid reaction. \n\nPlease use one of the following reactions 👍, 👎, ❤, 🔥, 🥰, 👏",
        )
