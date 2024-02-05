from aiogram import F, Router, flags
from aiogram.dispatcher.flags import get_flag
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, ChatPermissions, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.filters.spam_detection import SpamFilter

spam_router = Router()


class UnRoCallbackData(CallbackData, prefix="unro"):
    user_id: int


def unban_kb(user_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text="UnRO user", callback_data=UnRoCallbackData(user_id=user_id))
    return kb.as_markup()


@spam_router.callback_query.middleware()  # type: ignore
async def chat_admin_middleware(handler, event, data):
    chat_admin_flag = get_flag(data, "chat_admin")
    if not chat_admin_flag:
        return

    bot_admins = data.get("bot_admins")
    if event.from_user.id not in bot_admins:
        return await event.answer("This button is only for admins")
    return await handler(event, data)


@spam_router.message(F.chat.id == -1001041869725, F.text.len() > 10, SpamFilter())
async def spam_handler(message: Message):
    await message.chat.restrict(
        user_id=message.from_user.id,
        permissions=ChatPermissions(
            can_send_messages=False,
        ),
    )
    # message that user has been restricted
    await message.answer(
        f"User {message.from_user.full_name} has been restricted for spamming. Contact @latand if you think it's a mistake.",
        reply_markup=unban_kb(message.from_user.id),
    )
    await message.delete()


@spam_router.callback_query(UnRoCallbackData.filter())
@flags.chat_admin
async def unro_handler(query: CallbackQuery, callback_data: UnRoCallbackData):
    await query.message.chat.restrict(
        user_id=callback_data.user_id,
        permissions=ChatPermissions(
            can_send_messages=True, can_send_other_messages=True
        ),
    )
    mention_user_link = f'<a href="tg://user?id={callback_data.user_id}">User</a>'
    await query.message.edit_text(f"{mention_user_link} has been Restored")
