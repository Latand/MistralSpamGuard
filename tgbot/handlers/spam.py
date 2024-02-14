import json
import logging
import typing
from datetime import timedelta

from aiogram import F, Router, flags
from aiogram.dispatcher.flags import get_flag
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, ChatPermissions, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.config import BOT_ADMINS_STORAGE_KEY
from tgbot.filters.groups_filter import AllowedGroupsFilter
from tgbot.filters.spam_detection import SpamFilter

spam_router = Router()


class UnRoCallbackData(CallbackData, prefix="unro"):
    user_id: int
    message_id: typing.Optional[int] = None


def unban_kb(user_id: int, message_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="UnRO user",
        callback_data=UnRoCallbackData(user_id=user_id, message_id=message_id),
    )
    return kb.as_markup()


@spam_router.callback_query.middleware()  # type: ignore
async def chat_admin_middleware(handler, event: CallbackQuery, data):
    chat_admin_flag = get_flag(data, "chat_admin")
    if not chat_admin_flag:
        return await handler(event, data)

    storage: RedisStorage = data.get("storage")
    bot_admins = await storage.redis.get(BOT_ADMINS_STORAGE_KEY)
    print(f"Bot admins: {bot_admins}")
    logging.info(f"Bot admins: {bot_admins}")
    if not bot_admins:
        bot_admins = [
            admin.user.id for admin in await event.message.chat.get_administrators()
        ]
        await storage.redis.set(
            BOT_ADMINS_STORAGE_KEY, json.dumps(bot_admins), ex=timedelta(days=1)
        )
    else:
        try:
            bot_admins = json.loads(bot_admins)
        except json.JSONDecodeError:
            logging.error(f"Can't decode bot_admins: {bot_admins}")

    print(f"Bot admins: {bot_admins}")
    if event.from_user.id not in bot_admins:
        return await event.answer("This button is only for admins")
    return await handler(event, data)


@spam_router.message(AllowedGroupsFilter(), F.text.len() > 10, SpamFilter())
async def spam_handler(message: Message, storage: RedisStorage):
    await message.chat.restrict(
        user_id=message.from_user.id,
        permissions=ChatPermissions(
            can_send_messages=False,
        ),
    )
    # message that user has been restricted
    await message.answer(
        f"User {message.from_user.full_name} has been restricted for spamming. Contact @latand if you think it's a mistake.",
        reply_markup=unban_kb(message.from_user.id, message.message_id),
    )
    KEY_SPAM_MESSAGES = f"spam_messages:{message.chat.id}:{message.message_id}"
    await storage.redis.set(KEY_SPAM_MESSAGES, message.html_text, ex=timedelta(days=7))
    await message.delete()


@spam_router.callback_query(UnRoCallbackData.filter())
@flags.chat_admin
async def unro_handler(
    query: CallbackQuery, callback_data: UnRoCallbackData, storage: RedisStorage
):
    await query.message.chat.restrict(
        user_id=callback_data.user_id,
        permissions=ChatPermissions(
            can_send_messages=True, can_send_other_messages=True
        ),
    )
    mention_user_link = f'<a href="tg://user?id={callback_data.user_id}">User</a>'

    if callback_data.message_id:
        KEY_SPAM_MESSAGE = (
            f"spam_messages:{query.message.chat.id}:{callback_data.message_id}"
        )
        message = await storage.redis.get(KEY_SPAM_MESSAGE)
        if message:
            if isinstance(message, bytes):
                message = message.decode("utf-8")

            await query.message.answer(
                f"{mention_user_link} has been Restored.\n\n"
                f"Original message:\n\n{message}"
            )
            await storage.redis.delete(KEY_SPAM_MESSAGE)
    else:
        await query.message.answer(f"{mention_user_link} has been Restored.")

    await query.message.delete()
